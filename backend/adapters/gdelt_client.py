"""GDELT 2.0 API adapter for global events and news data"""
import hashlib
from datetime import datetime
from urllib.parse import urlparse
import httpx

from core.settings import settings


class GDELTClient:
    BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
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
        """Search GDELT 2.0 API for articles matching keywords."""
        keywords = self._extract_keywords(query)
        if not keywords:
            return []
        
        search_query = " ".join(keywords)
        max_results = getattr(settings, "gdelt_max_results", 40)
        
        params = {
            "query": search_query,
            "mode": "ArtList",
            "format": "json",
            "sortby": "PublDate",
            "maxrecords": max_results,
            "timespan": "1y",  # Search past year for more results
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
                response = await client.get(self.BASE_URL, params=params, headers=headers)
                if response.status_code != 200:
                    return []
                
                data = response.json()
                return self._parse_response(data)
        except Exception as e:
            return []

    def _parse_response(self, data: dict) -> list[dict]:
        """Parse GDELT JSON response and extract articles."""
        results: list[dict] = []
        
        try:
            # Handle different response structures
            articles = data.get("articles", [])
            
            # If articles is empty, try alternative keys
            if not articles:
                # Some GDELT responses might have data in different format
                if isinstance(data.get("data"), list):
                    articles = data["data"]
                elif "docs" in data:
                    articles = data["docs"]
            
            for article in articles:
                try:
                    # Try different field names for title
                    title = article.get("title") or article.get("Title") or article.get("headline") or ""
                    
                    # Try different field names for URL
                    url = article.get("url") or article.get("URL") or article.get("sourceurl") or ""
                    
                    # Try different field names for date
                    pub_date = article.get("sedate") or article.get("date") or article.get("pubDate") or ""
                    
                    if not title or not url:
                        continue
                    
                    # Parse timestamp
                    timestamp = self._friendly_time(pub_date)
                    
                    # Extract domain from URL as username
                    domain = self._extract_domain(url)
                    
                    article_id = hashlib.sha256(f"{title}:{url}".encode()).hexdigest()[:12]
                    
                    results.append({
                        "id": f"gd_{article_id}",
                        "platform": "gdelt",
                        "username": domain,
                        "timestamp": timestamp,
                        "text": title,
                        "likes": 0,
                        "shares": 0,
                        "followers": 0,
                        "urls": [url],
                    })
                except Exception:
                    # Skip malformed articles
                    continue
        except Exception:
            pass
        
        return results

    def _extract_keywords(self, query: str) -> list[str]:
        """Extract keywords from query, filtering stop words and short tokens."""
        tokens = query.lower().split()
        keywords = [
            token for token in tokens
            if len(token) >= 3 and token not in self.STOP_WORDS
        ]
        return keywords

    def _friendly_time(self, gdelt_date: str) -> str:
        """Convert GDELT timestamp (YYYYMMDDHHMMSS) to friendly relative time format."""
        if not gdelt_date or len(gdelt_date) < 14:
            return "recently"
        
        try:
            # Parse YYYYMMDDHHMMSS format
            pub_time = datetime.strptime(gdelt_date, "%Y%m%d%H%M%S")
            now = datetime.now()
            delta = now - pub_time
            
            if delta.total_seconds() < 60:
                return "just now"
            elif delta.total_seconds() < 3600:
                minutes = int(delta.total_seconds() // 60)
                return f"{minutes}m ago"
            elif delta.total_seconds() < 86400:
                hours = int(delta.total_seconds() // 3600)
                return f"{hours}h ago"
            elif delta.total_seconds() < 604800:
                days = int(delta.total_seconds() // 86400)
                return f"{days}d ago"
            else:
                weeks = int(delta.total_seconds() // 604800)
                return f"{weeks}w ago"
        except Exception:
            return "recently"

    def _extract_domain(self, url: str) -> str:
        """Extract domain name from URL."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path
            # Remove www. prefix if present
            if domain.startswith("www."):
                domain = domain[4:]
            return domain or "GDELT"
        except Exception:
            return "GDELT"
