"""Google News RSS adapter for fetching news articles"""
import hashlib
import re
from datetime import datetime
from email.utils import parsedate_to_datetime
from urllib.parse import quote
import httpx

from core.settings import settings


class GoogleNewsClient:
    BASE_URL = "https://news.google.com/rss/search"
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
        """Search Google News RSS feed for articles matching the query."""
        keywords = self._extract_keywords(query)
        if not keywords:
            return []
        
        search_query = " ".join(keywords)
        params = {"q": search_query}
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
                response = await client.get(self.BASE_URL, params=params, headers=headers)
                if response.status_code != 200:
                    return []
                
                return self._parse_rss(response.text)
        except Exception as e:
            return []

    def _parse_rss(self, xml_content: str) -> list[dict]:
        """Parse Google News RSS XML and extract articles."""
        import xml.etree.ElementTree as ET
        
        results: list[dict] = []
        try:
            # Remove BOM if present
            if xml_content.startswith('\ufeff'):
                xml_content = xml_content[1:]
            
            root = ET.fromstring(xml_content)
            
            # Find all items - try different XPath patterns
            items = root.findall(".//item")
            if not items:
                # Try alternative pattern
                items = root.findall("item")
            if not items and root.tag == "item":
                # Single item
                items = [root]
            
            max_results = getattr(settings, "google_news_max_results", 40)
            
            for item in items[:max_results]:
                try:
                    # Get elements by tag name
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    pub_date_elem = item.find("pubDate")
                    description_elem = item.find("description")
                    
                    title = (title_elem.text or "").strip() if title_elem is not None else ""
                    link = (link_elem.text or "").strip() if link_elem is not None else ""
                    pub_date = (pub_date_elem.text or "").strip() if pub_date_elem is not None else ""
                    description = (description_elem.text or "").strip() if description_elem is not None else ""
                    
                    if not title or not link:
                        continue
                    
                    # Clean title (remove source suffix)
                    title = self._clean_title(title)
                    
                    # Parse publication date
                    timestamp = self._friendly_time(pub_date)
                    
                    # Extract URLs from description
                    urls = self._extract_urls(description, link)
                    
                    article_id = hashlib.sha256(f"{title}:{link}".encode()).hexdigest()[:12]
                    
                    results.append({
                        "id": f"gn_{article_id}",
                        "platform": "google_news",
                        "username": "Google News",
                        "timestamp": timestamp,
                        "text": title,
                        "likes": 0,
                        "shares": 0,
                        "followers": 0,
                        "urls": [link] + urls,
                    })
                except Exception:
                    # Skip malformed items
                    continue
        except Exception:
            pass
        
        return results

    def _clean_title(self, title: str) -> str:
        """Remove source suffix from Google News titles."""
        # Google News format: "Title - Source"
        if " - " in title:
            return title.rsplit(" - ", 1)[0].strip()
        return title

    def _extract_keywords(self, query: str) -> list[str]:
        """Extract keywords from query, filtering stop words and short tokens."""
        tokens = query.lower().split()
        keywords = [
            token for token in tokens
            if len(token) >= 3 and token not in self.STOP_WORDS
        ]
        return keywords

    def _friendly_time(self, rfc2822_date: str) -> str:
        """Convert RFC 2822 date to friendly relative time format."""
        if not rfc2822_date:
            return "just now"
        
        try:
            pub_time = parsedate_to_datetime(rfc2822_date)
            now = datetime.now(pub_time.tzinfo) if pub_time.tzinfo else datetime.now()
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

    def _extract_urls(self, description: str, main_url: str = "") -> list[str]:
        """Extract URLs from description and add main article URL."""
        urls = []
        
        if main_url:
            urls.append(main_url)
        
        # Extract URLs from description using regex
        url_pattern = r'https?://[^\s<>"\)]*'
        if description:
            found_urls = re.findall(url_pattern, description)
            urls.extend(found_urls)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_urls = []
        for url in urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
        
        return unique_urls[:5]  # Limit to 5 URLs
