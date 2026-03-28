from datetime import datetime, timezone
import hashlib
import httpx

from core.settings import settings


class TwitterClient:
    BASE_URL = "https://api.twitter.com/2/tweets/search/recent"
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
        if not settings.twitter_bearer_token:
            return []

        keywords = self._extract_keywords(query)
        if not keywords:
            return []
        
        search_query = self._build_search_query(keywords)
        
        params = {
            "query": search_query,
            "max_results": max(10, min(settings.twitter_max_results, 100)),
            "tweet.fields": "created_at,public_metrics,author_id,entities",
            "expansions": "author_id",
            "user.fields": "username,public_metrics",
        }
        headers = {"Authorization": f"Bearer {settings.twitter_bearer_token}"}

        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            response = await client.get(self.BASE_URL, params=params, headers=headers)
            if response.status_code != 200:
                return []
            payload = response.json()

        users = {
            item.get("id"): item
            for item in payload.get("includes", {}).get("users", [])
            if item.get("id")
        }

        results: list[dict] = []
        for tweet in payload.get("data", []):
            author = users.get(tweet.get("author_id"), {})
            metrics = tweet.get("public_metrics", {})
            user_metrics = author.get("public_metrics", {})
            username = author.get("username", f"user_{tweet.get('author_id', 'unknown')}")

            tweet_id = tweet.get("id", "")
            if not tweet_id:
                tweet_id = hashlib.sha256(f"{username}:{tweet.get('text', '')}".encode()).hexdigest()[:12]

            created_at = tweet.get("created_at")
            timestamp = self._friendly_time(created_at)

            results.append(
                {
                    "id": f"tw_{tweet_id}",
                    "platform": "twitter",
                    "username": f"@{username}",
                    "timestamp": timestamp,
                    "text": tweet.get("text", ""),
                    "likes": int(metrics.get("like_count", 0)),
                    "shares": int(metrics.get("retweet_count", 0)),
                    "followers": int(user_metrics.get("followers_count", 0)),
                    "urls": self._extract_urls(tweet),
                }
            )

        return results

    def _extract_keywords(self, query: str) -> list[str]:
        """Extract keywords from query, filtering stop words and short tokens."""
        tokens = query.lower().split()
        keywords = [
            token for token in tokens
            if len(token) >= 3 and token not in self.STOP_WORDS
        ]
        return keywords

    def _build_search_query(self, keywords: list[str]) -> str:
        """Build Twitter v2 search query with OR-joined keywords and filters."""
        if not keywords:
            return ""
        or_query = " OR ".join(keywords)
        return f"({or_query}) lang:en -is:retweet"

    def _friendly_time(self, created_at: str | None) -> str:
        if not created_at:
            return "now"
        try:
            parsed = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            delta = datetime.now(timezone.utc) - parsed
            minutes = int(max(delta.total_seconds() // 60, 0))
            if minutes < 1:
                return "now"
            if minutes < 60:
                return f"{minutes}m ago"
            hours = minutes // 60
            return f"{hours}h ago"
        except Exception:
            return "now"

    def _extract_urls(self, tweet: dict) -> list[str]:
        entities = tweet.get("entities", {})
        urls = entities.get("urls", [])
        return [item.get("expanded_url", "") for item in urls if item.get("expanded_url")]
