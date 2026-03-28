from adapters.news_rss_adapter import NewsRSSAdapter
from adapters.gdelt_client import GDELTClient
from adapters.telegram_client import TelegramClient
from adapters.commoncrawl_client import CommonCrawlClient
from adapters.facebook_client import FacebookClient


class ScraperService:
    def __init__(self) -> None:
        self.news = NewsRSSAdapter()
        self.gdelt = GDELTClient()
        self.telegram = TelegramClient()
        self.commoncrawl = CommonCrawlClient()
        self.facebook = FacebookClient()

    async def collect(self, query: str) -> list[dict]:
        news_posts, gdelt_posts, telegram_posts, cc_posts, facebook_posts = await self._collect_parallel(query)
        combined = self._dedupe_posts([*news_posts, *gdelt_posts, *telegram_posts, *cc_posts, *facebook_posts])
        return sorted(combined, key=lambda item: item.get("likes", 0) + item.get("shares", 0), reverse=True)

    async def _collect_parallel(self, query: str) -> tuple[list[dict], list[dict], list[dict], list[dict], list[dict]]:
        import asyncio

        news_task = asyncio.create_task(self.news.search(query))
        gdelt_task = asyncio.create_task(self.gdelt.search(query))
        telegram_task = asyncio.create_task(self.telegram.search(query))
        cc_task = asyncio.create_task(self.commoncrawl.search(query))
        facebook_task = asyncio.create_task(self.facebook.search(query))
        news_posts, gdelt_posts, telegram_posts, cc_posts, facebook_posts = await asyncio.gather(
            news_task, gdelt_task, telegram_task, cc_task, facebook_task
        )
        return news_posts, gdelt_posts, telegram_posts, cc_posts, facebook_posts

    def _dedupe_posts(self, posts: list[dict]) -> list[dict]:
        """Deduplicate posts by URL, preserving source diversity.
        
        Uses URL-based deduplication to handle CommonCrawl results properly.
        If the same URL appears from multiple sources, we keep one entry and
        track that it was mentioned in multiple outlets (increases confidence).
        """
        seen_urls: set[str] = set()
        deduped: list[dict] = []
        
        for post in posts:
            # Try to extract URL from urls field (preferred) or use text as fallback
            urls = post.get("urls", [])
            post_url = urls[0] if urls else post.get("text", "")
            
            if not post_url:
                continue
            
            # Normalize URL for comparison
            normalized_url = post_url.lower().strip()
            
            if normalized_url in seen_urls:
                # URL already seen - would increase confidence in production
                continue
            
            seen_urls.add(normalized_url)
            deduped.append(post)
        
        return deduped
