"""CommonCrawl CDX Index API adapter for massive web-scale claim verification"""
import hashlib
from datetime import datetime
from urllib.parse import urlparse, quote
import httpx

from core.settings import settings


class CommonCrawlClient:
    """Queries CommonCrawl CDX Index to check millions of pages for claim mentions.
    
    The CommonCrawl CDX API provides free access to a comprehensive index of the web,
    currently covering 200+ billion pages across regular crawls. This adapter searches
    for claims across the entire indexed web, not just current news sources.
    
    API: https://index.commoncrawl.org/
    """
    
    BASE_URL = "https://index.commoncrawl.org"
    DEFAULT_INDEX = "CC-MAIN-2024-51"  # Latest or near-latest crawl
    
    STOP_WORDS = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an",
        "and", "any", "are", "aren", "as", "at", "be", "because", "been", "before",
        "being", "below", "between", "both", "but", "by", "can", "could", "did",
        "do", "does", "doing", "down", "during", "each", "few", "for", "from",
        "further", "had", "has", "have", "having", "he", "her", "here", "hers",
        "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is",
        "it", "its", "itself", "just", "me", "might", "more", "most", "must",
        "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only",
        "or", "other", "out", "over", "own", "same", "so", "some", "such", "than",
        "that", "the", "their", "theirs", "them", "themselves", "then", "there",
        "these", "they", "this", "those", "to", "too", "under", "until", "up",
        "very", "was", "we", "were", "what", "when", "where", "which", "while",
        "who", "whom", "why", "will", "with", "would", "you", "your", "yours",
        "yourself", "yourselves"
    }

    async def search(self, query: str) -> list[dict]:
        """Search CommonCrawl CDX Index for pages matching claim keywords.
        
        Args:
            query: The claim or topic to search for
            
        Returns:
            List of dicts with url, title (url), timestamp, platform info
            Ordered by relevance (freshness and domain quality)
        """
        keywords = self._extract_keywords(query)
        if not keywords:
            return []
        
        max_results = getattr(settings, "commoncrawl_max_results", 1000)
        
        # Build search query: multiple keywords (AND operation)
        # Format: "keyword1 keyword2 keyword3"
        search_query = " ".join(keywords)
        
        try:
            results = await self._query_cdx_index(search_query, max_results)
            
            # Sort by recency (newest first)
            sorted_results = sorted(
                results,
                key=lambda x: x.get("_timestamp_obj", datetime.now()),
                reverse=True
            )
            
            # Remove internal timestamp object before returning
            return [
                {k: v for k, v in item.items() if k != "_timestamp_obj"}
                for item in sorted_results[:max_results]
            ]
        except Exception:
            # On any error, return empty list
            return []

    async def _query_cdx_index(self, search_query: str, max_results: int) -> list[dict]:
        """Query CommonCrawl CDX Index API.
        
        The CDX API allows free queries with limits:
        - Default: ~100K results per query
        - Format: JSON with url, timestamp, statuscode, mimetype
        """
        results: list[dict] = []
        
        try:
            # CDX API endpoint for latest captures
            url = f"{self.BASE_URL}/{self.DEFAULT_INDEX}/cdx"
            
            # Query parameters
            params = {
                "url": f"*{quote(search_query)}*",  # Wildcard search
                "output": "json",
                "matchType": "domain",  # Match domain and path
                "filter": "statusCode:200",  # Only successful pages
                "collapse": "urlkey",  # Deduplicate by URL key
                "pageSize": 10000,  # Batch size
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            timeout = getattr(settings, "commoncrawl_timeout", 30)
            
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url, params=params, headers=headers)
                
                if response.status_code != 200:
                    return []
                
                # Parse JSON response
                data = response.json()
                
                if not isinstance(data, list) or len(data) == 0:
                    return []
                
                # First row is headers, subsequent rows are data
                if len(data) > 1:
                    headers_list = data[0]  # ["url", "timestamp", "statuscode", "mimetype", ...]
                    records = data[1:]  # Actual records
                    
                    for record in records[:max_results]:
                        try:
                            if len(record) < 2:
                                continue
                            
                            # Extract fields based on header positions
                            url_val = record[0] if len(record) > 0 else ""
                            timestamp_val = record[1] if len(record) > 1 else ""
                            
                            if not url_val:
                                continue
                            
                            # Add protocol if missing
                            if not url_val.startswith("http"):
                                url_val = "https://" + url_val
                            
                            domain = self._extract_domain(url_val)
                            timestamp_obj = self._parse_timestamp(timestamp_val)
                            timestamp_friendly = self._friendly_time_from_obj(timestamp_obj)
                            
                            article_id = hashlib.sha256(url_val.encode()).hexdigest()[:12]
                            
                            results.append({
                                "id": f"cc_{article_id}",
                                "platform": "commoncrawl",
                                "username": domain,
                                "timestamp": timestamp_friendly,
                                "text": url_val[:200],  # Use URL as title
                                "likes": 0,
                                "shares": 0,
                                "followers": 0,
                                "urls": [url_val],
                                "_timestamp_obj": timestamp_obj,
                            })
                        except Exception:
                            # Skip malformed records
                            continue
            
            return results
        except Exception:
            return []

    def _extract_keywords(self, query: str) -> list[str]:
        """Extract non-stop-word keywords from query."""
        words = query.lower().split()
        keywords = [w.strip(".,!?;:\"'") for w in words if w and len(w) > 2]
        return [k for k in keywords if k not in self.STOP_WORDS][:5]  # Top 5 keywords

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path
            # Remove www. prefix
            if domain.startswith("www."):
                domain = domain[4:]
            return domain[:50]  # Truncate long domains
        except Exception:
            return "unknown"

    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse CommonCrawl timestamp format (YYYYMMDDhhmmss)."""
        try:
            if not timestamp_str or len(timestamp_str) < 8:
                return datetime.now()
            # Parse format: 20240115123456
            return datetime.strptime(timestamp_str[:14], "%Y%m%d%H%M%S")
        except Exception:
            return datetime.now()

    def _friendly_time_from_obj(self, dt: datetime) -> str:
        """Convert datetime object to friendly time string."""
        try:
            now = datetime.now()
            diff = (now - dt).total_seconds()
            
            if diff < 3600:
                return f"{int(diff / 60)}m ago"
            elif diff < 86400:
                return f"{int(diff / 3600)}h ago"
            elif diff < 604800:
                return f"{int(diff / 86400)}d ago"
            elif diff < 2592000:
                return f"{int(diff / 604800)}w ago"
            else:
                return f"{int(diff / 2592000)}mo ago"
        except Exception:
            return "unknown"
