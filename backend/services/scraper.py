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
        
        # If scrapers yield few results due to tight timeouts, complement with news search cards
        if len(combined) < 2:
            fallback_news = self.news._demo_data(query)
            combined = self._dedupe_posts([*combined, *fallback_news])

        return sorted(combined, key=lambda item: item.get("likes", 0) + item.get("shares", 0), reverse=True)

    async def _collect_parallel(self, query: str) -> tuple[list[dict], list[dict], list[dict], list[dict], list[dict]]:
        import asyncio

        async def _safe_run(coro, default_val=None):
            if default_val is None:
                default_val = []
            try:
                # Enforce a strict 2.5-second cap per scraper to prevent 502/504 cloud proxy timeouts
                return await asyncio.wait_for(coro, timeout=2.5)
            except Exception:
                return default_val

        results = await asyncio.gather(
            _safe_run(self.news.search(query)),
            _safe_run(self.gdelt.search(query)),
            _safe_run(self.telegram.search(query)),
            _safe_run(self.commoncrawl.search(query)),
            _safe_run(self.facebook.search(query)),
            return_exceptions=True
        )

        news_posts = results[0] if isinstance(results[0], list) else []
        gdelt_posts = results[1] if isinstance(results[1], list) else []
        telegram_posts = results[2] if isinstance(results[2], list) else []
        cc_posts = results[3] if isinstance(results[3], list) else []
        facebook_posts = results[4] if isinstance(results[4], list) else []

        return news_posts, gdelt_posts, telegram_posts, cc_posts, facebook_posts

    def _dedupe_posts(self, posts: list[dict]) -> list[dict]:
        """Deduplicate posts by URL, preserving source diversity."""
        seen_urls: set[str] = set()
        deduped: list[dict] = []
        
        for post in posts:
            urls = post.get("urls", [])
            post_url = urls[0] if urls else post.get("text", "")
            
            if not post_url:
                continue
            
            normalized_url = post_url.lower().strip()
            if normalized_url in seen_urls:
                continue
            
            seen_urls.add(normalized_url)
            deduped.append(post)
        
        return deduped
