import hashlib
import httpx

from core.settings import settings


class TelegramClient:
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
        if not settings.telegram_bot_token:
            return []

        channels = [item.strip() for item in settings.telegram_channels.split(",") if item.strip()]
        if not channels:
            return []

        keywords = self._extract_keywords(query)
        if not keywords:
            return []

        results: list[dict] = []
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            # Fetch all updates once
            url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/getUpdates"
            resp = await client.get(url)
            if resp.status_code != 200:
                return []
            
            payload = resp.json()
            
            # Filter and match updates
            for update in payload.get("result", []):
                message = update.get("message") or update.get("channel_post") or {}
                text = message.get("text", "")
                if not text:
                    continue
                
                # Use keyword-overlap matching
                if not self._matches_query(text, keywords):
                    continue
                
                chat = message.get("chat", {})
                chat_username = chat.get("username", "")
                
                # Filter by configured channels
                matching_channel = None
                for channel in channels:
                    if channel.lower() in chat_username.lower() or channel.lower() in text.lower()[:30]:
                        matching_channel = channel
                        break
                
                if not matching_channel and chat_username not in channels:
                    continue

                message_id = message.get("message_id", "")
                if not message_id:
                    message_id = hashlib.sha256(f"{chat_username}:{text}".encode()).hexdigest()[:12]

                username = chat_username or matching_channel or "telegram_user"
                results.append(
                    {
                        "id": f"tg_{message_id}",
                        "platform": "telegram",
                        "username": f"@{username}",
                        "timestamp": "now",
                        "text": text,
                        "likes": 0,
                        "shares": 0,
                        "followers": 0,
                        "urls": self._extract_urls(text),
                    }
                )
                if len(results) >= settings.telegram_max_results:
                    return results

        return results

    def _extract_keywords(self, query: str) -> list[str]:
        """Extract keywords from query, filtering stop words and short tokens."""
        tokens = query.lower().split()
        keywords = [
            token for token in tokens
            if len(token) >= 3 and token not in self.STOP_WORDS
        ]
        return keywords

    def _matches_query(self, text: str, keywords: list[str]) -> bool:
        """Check if text contains sufficient keyword overlap."""
        if not keywords:
            return False
        
        text_lower = text.lower()
        matching_keywords = sum(1 for kw in keywords if kw in text_lower)
        
        # For single-word queries, require 1 match; for multi-word, require at least 1
        required_overlap = 1 if len(keywords) <= 1 else 1
        return matching_keywords >= required_overlap

    def _extract_urls(self, text: str) -> list[str]:
        parts = text.split()
        return [part for part in parts if part.startswith("http://") or part.startswith("https://")]
