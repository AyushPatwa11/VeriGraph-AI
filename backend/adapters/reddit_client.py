from datetime import datetime, timezone
import asyncio
from typing import Optional
import praw
from praw.exceptions import InvalidToken, ResponseException

from core.settings import settings


class RedditClient:
    """
    Reddit API client for searching discussions and posts mentioning claims.
    Uses PRAW (Python Reddit API Wrapper) with async support.
    """
    
    def __init__(self):
        self._reddit = None
    
    def _get_reddit_instance(self) -> Optional[praw.Reddit]:
        """
        Initialize and return Reddit API instance.
        Cached to avoid reinitializing on each search.
        """
        if self._reddit is None:
            if not all([settings.reddit_client_id, settings.reddit_client_secret]):
                return None
            
            try:
                self._reddit = praw.Reddit(
                    client_id=settings.reddit_client_id,
                    client_secret=settings.reddit_client_secret,
                    user_agent=settings.reddit_user_agent,
                )
                # Test authentication
                self._reddit.user.me()
            except InvalidToken:
                return None
            except Exception:
                return None
        
        return self._reddit
    
    async def search(self, query: str) -> list[dict]:
        """
        Search Reddit for discussions mentioning a claim.
        
        Searches both submissions (posts) and comments across all subreddits.
        
        Args:
            query: Claim text or keyword to search for
            
        Returns:
            List of submissions/comments in format:
            {
                'post_id': str,
                'author': str,
                'created_at': str (ISO timestamp),
                'text': str,
                'upvotes': int,
                'downvotes': int,
                'num_comments': int,
                'score': int,
                'subreddit': str,
                'url': str,
                'type': 'submission' | 'comment',
                'platform': 'reddit'
            }
        """
        reddit = self._get_reddit_instance()
        if reddit is None:
            return []
        
        try:
            results = []
            
            # Run blocking Reddit API calls in thread pool
            loop = asyncio.get_event_loop()
            
            # Search submissions (posts)
            submissions = await loop.run_in_executor(
                None,
                self._search_submissions,
                reddit,
                query
            )
            results.extend(submissions)
            
            # Search comments
            comments = await loop.run_in_executor(
                None,
                self._search_comments,
                reddit,
                query
            )
            results.extend(comments)
            
            return results
            
        except (InvalidToken, ResponseException):
            return []
        except Exception:
            return []
    
    def _search_submissions(self, reddit: praw.Reddit, query: str) -> list[dict]:
        """
        Search for submissions (posts) containing the query.
        Blocking call - meant to run in thread executor.
        """
        submissions = []
        
        try:
            # Search across all subreddits
            for submission in reddit.subreddit("all").search(
                query,
                time_filter="month",
                sort="relevance",
                limit=settings.reddit_max_results
            ):
                created_at = datetime.fromtimestamp(
                    submission.created_utc, tz=timezone.utc
                ).isoformat()
                
                submissions.append({
                    "post_id": submission.id,
                    "author": submission.author.name if submission.author else "[deleted]",
                    "created_at": created_at,
                    "text": submission.title + "\n" + submission.selftext[:500],
                    "upvotes": submission.ups,
                    "downvotes": submission.downs,
                    "num_comments": submission.num_comments,
                    "score": submission.score,
                    "subreddit": submission.subreddit.display_name,
                    "url": submission.url,
                    "type": "submission",
                    "platform": "reddit",
                })
        except (InvalidToken, ResponseException):
            pass
        except Exception:
            pass
        
        return submissions
    
    def _search_comments(self, reddit: praw.Reddit, query: str) -> list[dict]:
        """
        Search for comments containing the query.
        Blocking call - meant to run in thread executor.
        """
        comments = []
        
        try:
            # Search comments using Pushshift via Reddit's search
            # For better comment search, we search submissions and extract comment discussions
            for submission in reddit.subreddit("all").search(
                query,
                time_filter="month",
                sort="relevance",
                limit=min(settings.reddit_max_results // 2, 50)  # Limit submissions to scan
            ):
                # Get top comments from each submission
                submission.comments.replace_more(limit=None)  # Fetch all comments
                
                for comment in submission.comments.list()[:20]:  # Top 20 comments per submission
                    if query.lower() not in comment.body.lower():
                        continue
                    
                    created_at = datetime.fromtimestamp(
                        comment.created_utc, tz=timezone.utc
                    ).isoformat()
                    
                    comments.append({
                        "post_id": comment.id,
                        "author": comment.author.name if comment.author else "[deleted]",
                        "created_at": created_at,
                        "text": comment.body[:500],
                        "upvotes": comment.ups,
                        "downvotes": comment.downs,
                        "num_comments": 0,  # Comments don't have sub-comments in this context
                        "score": comment.score,
                        "subreddit": submission.subreddit.display_name,
                        "url": submission.url,
                        "type": "comment",
                        "platform": "reddit",
                    })
                
                if len(comments) >= settings.reddit_max_results:
                    break
        
        except (InvalidToken, ResponseException):
            pass
        except Exception:
            pass
        
        return comments[:settings.reddit_max_results]
    
    async def get_subreddit_stats(self, subreddit_name: str) -> dict:
        """
        Get statistics about a specific subreddit.
        
        Args:
            subreddit_name: Name of subreddit (without r/)
            
        Returns:
            Dictionary with subreddit stats: {subscribers, active_users, created_utc, etc}
        """
        reddit = self._get_reddit_instance()
        if reddit is None:
            return {}
        
        try:
            loop = asyncio.get_event_loop()
            stats = await loop.run_in_executor(
                None,
                self._get_sub_stats,
                reddit,
                subreddit_name
            )
            return stats
        except Exception:
            return {}
    
    def _get_sub_stats(self, reddit: praw.Reddit, subreddit_name: str) -> dict:
        """
        Get subreddit statistics. Blocking call for thread executor.
        """
        try:
            sub = reddit.subreddit(subreddit_name)
            return {
                "name": sub.display_name,
                "subscribers": sub.subscribers,
                "active_users": getattr(sub, "active_user_count", 0),
                "created_utc": sub.created_utc,
                "public_description": sub.public_description[:200] if sub.public_description else "",
                "subreddit_type": sub.subreddit_type,
            }
        except (InvalidToken, ResponseException):
            return {}
        except Exception:
            return {}
    
    async def detect_echo_chambers(self, claim: str) -> dict:
        """
        Detect echo chambers - subreddits with coordinated discussion of a claim.
        
        Args:
            claim: Claim text to analyze
            
        Returns:
            Dictionary mapping subreddit names to intensity score (0-1)
        """
        results = await self.search(claim)
        
        subreddit_metrics = {}
        for result in results:
            sub = result.get("subreddit", "unknown")
            if sub not in subreddit_metrics:
                subreddit_metrics[sub] = {
                    "count": 0,
                    "total_engagement": 0,
                    "total_comments": 0,
                }
            
            subreddit_metrics[sub]["count"] += 1
            engagement = result.get("upvotes", 0) + result.get("downvotes", 0)
            subreddit_metrics[sub]["total_engagement"] += engagement
            subreddit_metrics[sub]["total_comments"] += result.get("num_comments", 0)
        
        # Calculate echo chamber intensity (0-1)
        # Higher intensity = more concentrated discussion in fewer subreddits
        echo_chambers = {}
        total_discussions = len(results)
        
        if total_discussions > 0:
            for sub, metrics in subreddit_metrics.items():
                # Proportion of total + engagement weight
                proportion = metrics["count"] / total_discussions
                engagement_weight = metrics["total_engagement"] / max(
                    sum(m["total_engagement"] for m in subreddit_metrics.values()), 1
                )
                
                # Combined intensity (favor high engagement + concentration)
                intensity = (proportion * 0.6 + engagement_weight * 0.4)
                
                if intensity > 0.05:  # Only include significant echo chambers
                    echo_chambers[sub] = min(intensity, 1.0)
        
        return echo_chambers
