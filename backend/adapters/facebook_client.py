from datetime import datetime, timezone
import httpx
import json

from core.settings import settings


class FacebookClient:
    BASE_URL = "https://graph.facebook.com/v18.0"
    
    async def search(self, query: str) -> list[dict]:
        """
        Search for public posts mentioning a claim across Facebook.
        
        Args:
            query: Claim text or keyword to search for
            
        Returns:
            List of posts with engagement metrics, posts format:
            {
                'post_id': str,
                'author_id': str,
                'username': str,
                'created_at': str (ISO timestamp),
                'text': str,
                'likes': int,
                'shares': int,
                'comments': int,
                'engagement': int (likes + shares + comments),
                'platform': 'facebook'
            }
        """
        if not settings.facebook_access_token:
            return []
        
        try:
            # Search public posts using the Graph API /search endpoint
            search_endpoint = f"{self.BASE_URL}/search"
            
            params = {
                "type": "post",
                "q": query,
                "fields": "id,created_time,message,story,permalink_url,likes.summary(true).limit(0),comments.summary(true).limit(0),shares",
                "limit": min(settings.facebook_max_results, 100),
                "access_token": settings.facebook_access_token,
            }
            
            posts = []
            async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
                response = await client.get(search_endpoint, params=params)
                
                if response.status_code == 401:
                    # Invalid token
                    return []
                elif response.status_code == 429:
                    # Rate limited
                    return []
                elif response.status_code != 200:
                    return []
                
                data = response.json()
                if "error" in data:
                    return []
                
                for post in data.get("data", []):
                    # Get likes count
                    likes_count = 0
                    if "likes" in post and "summary" in post["likes"]:
                        likes_count = post["likes"]["summary"].get("total_count", 0)
                    
                    # Get comments count
                    comments_count = 0
                    if "comments" in post and "summary" in post["comments"]:
                        comments_count = post["comments"]["summary"].get("total_count", 0)
                    
                    # Get shares count
                    shares_count = post.get("shares", 0)
                    if isinstance(shares_count, dict):
                        shares_count = shares_count.get("count", 0)
                    
                    # Calculate total engagement
                    engagement = likes_count + comments_count + shares_count
                    
                    # Extract text content
                    text = post.get("message") or post.get("story", "")
                    
                    # Parse post ID (format: page_id_post_id)
                    post_id = post.get("id", "")
                    
                    # Extract author info from post (limited by Graph API for non-owned posts)
                    author_id = post_id.split("_")[0] if "_" in post_id else ""
                    
                    # Timestamp conversion (Facebook returns ISO format)
                    created_at = post.get("created_time", "")
                    
                    # Get permalink URL
                    permalink_url = post.get("permalink_url", "")
                    
                    posts.append({
                        "post_id": post_id,
                        "author_id": author_id,
                        "username": f"facebook_user_{author_id}",
                        "created_at": created_at,
                        "text": text[:500],  # Limit text length
                        "likes": likes_count,
                        "shares": shares_count,
                        "comments": comments_count,
                        "engagement": engagement,
                        "platform": "facebook",
                        "urls": [permalink_url] if permalink_url else [],
                    })
            
            return posts
            
        except Exception:
            # Gracefully handle any connection/parsing errors
            return []
    
    async def get_post_reach(self, post_id: str) -> dict:
        """
        Get detailed reach metrics for a specific post.
        
        Args:
            post_id: Facebook post ID
            
        Returns:
            Reach metrics: {impressions, reach, shares, likes, comments}
        """
        if not settings.facebook_access_token or not post_id:
            return {}
        
        try:
            endpoint = f"{self.BASE_URL}/{post_id}"
            params = {
                "fields": "impressions,reach,shares,likes.summary(true).limit(0),comments.summary(true).limit(0)",
                "access_token": settings.facebook_access_token,
            }
            
            async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
                response = await client.get(endpoint, params=params)
                if response.status_code != 200:
                    return {}
                
                data = response.json()
                if "error" in data:
                    return {}
                
                return {
                    "impressions": data.get("impressions", 0),
                    "reach": data.get("reach", 0),
                    "shares": data.get("shares", 0),
                    "likes": data.get("likes", {}).get("summary", {}).get("total_count", 0),
                    "comments": data.get("comments", {}).get("summary", {}).get("total_count", 0),
                }
        except Exception:
            return {}
    
    async def search_by_hashtag(self, hashtag: str) -> list[dict]:
        """
        Search posts by hashtag.
        
        Args:
            hashtag: Hashtag to search (with or without #)
            
        Returns:
            List of posts with the hashtag
        """
        if not settings.facebook_access_token or not hashtag:
            return []
        
        try:
            # Clean hashtag
            if not hashtag.startswith("#"):
                hashtag = f"#{hashtag}"
            
            return await self.search(hashtag)
        except Exception:
            return []
