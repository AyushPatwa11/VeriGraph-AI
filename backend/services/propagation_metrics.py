"""
Propagation Metrics Service

Analyzes how claims/content spread across sources (Facebook, News, GDELT, Telegram, CommonCrawl).
Calculates metrics including: total reach, platform breakdown, timeline analysis, top spreaders, viral coefficient.
"""

from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional


class PropagationMetrics:
    """Calculate propagation and spread metrics for analyzed claims."""
    
    @staticmethod
    def calculate_total_reach(posts: list[dict]) -> dict:
        """
        Calculate total reach by summing all engagement metrics.
        
        Args:
            posts: List of posts from scraper.collect()
            
        Returns:
            {
                'total_reach': int (total engagement across all posts),
                'total_likes': int,
                'total_shares': int,
                'total_comments': int,
                'post_count': int,
                'average_engagement_per_post': float
            }
        """
        if not posts:
            return {
                'total_reach': 0,
                'total_likes': 0,
                'total_shares': 0,
                'total_comments': 0,
                'post_count': 0,
                'average_engagement_per_post': 0.0
            }
        
        total_likes = sum(post.get('likes', 0) for post in posts)
        total_shares = sum(post.get('shares', 0) for post in posts)
        total_comments = sum(post.get('comments', 0) for post in posts)
        total_engagement = total_likes + total_shares + total_comments
        
        return {
            'total_reach': total_engagement,
            'total_likes': total_likes,
            'total_shares': total_shares,
            'total_comments': total_comments,
            'post_count': len(posts),
            'average_engagement_per_post': total_engagement / len(posts) if posts else 0.0
        }
    
    @staticmethod
    def breakdown_by_platform(posts: list[dict]) -> dict:
        """
        Break down posts and engagement by platform.
        
        Args:
            posts: List of posts from scraper.collect()
            
        Returns:
            {
                'platform_distribution': {
                    'facebook': {
                        'post_count': int,
                        'total_engagement': int,
                        'avg_engagement': float,
                        'reach_percentage': float (0-100)
                    },
                    'news': {...},
                    'gdelt': {...},
                    'telegram': {...},
                    'commoncrawl': {...}
                },
                'platforms_with_posts': list[str] (platforms that have posts)
            }
        """
        if not posts:
            return {
                'platform_distribution': {},
                'platforms_with_posts': []
            }
        
        # Group by platform
        platform_stats = defaultdict(lambda: {
            'post_count': 0,
            'total_likes': 0,
            'total_shares': 0,
            'total_comments': 0,
            'total_engagement': 0
        })
        
        for post in posts:
            platform = post.get('platform', 'unknown')
            platform_stats[platform]['post_count'] += 1
            platform_stats[platform]['total_likes'] += post.get('likes', 0)
            platform_stats[platform]['total_shares'] += post.get('shares', 0)
            platform_stats[platform]['total_comments'] += post.get('comments', 0)
            platform_stats[platform]['total_engagement'] += post.get('engagement', 0)
        
        # Calculate percentages
        total_engagement = sum(s['total_engagement'] for s in platform_stats.values())
        
        distribution = {}
        for platform, stats in platform_stats.items():
            distribution[platform] = {
                'post_count': stats['post_count'],
                'total_engagement': stats['total_engagement'],
                'avg_engagement': stats['total_engagement'] / stats['post_count'] if stats['post_count'] > 0 else 0.0,
                'reach_percentage': (stats['total_engagement'] / total_engagement * 100) if total_engagement > 0 else 0.0,
                'likes': stats['total_likes'],
                'shares': stats['total_shares'],
                'comments': stats['total_comments']
            }
        
        return {
            'platform_distribution': distribution,
            'platforms_with_posts': sorted(list(platform_stats.keys()))
        }
    
    @staticmethod
    def calculate_timeline(posts: list[dict], bins: Optional[list[str]] = None) -> dict:
        """
        Analyze how claims spread over time in different windows.
        
        Args:
            posts: List of posts from scraper.collect()
            bins: Time window labels (default: ['24h', '7d', '30d'])
            
        Returns:
            {
                'timeline_buckets': {
                    '24h': {
                        'post_count': int,
                        'total_engagement': int,
                        'growth_rate': float (0-100, percentage),
                        'date_range': {'start': str (ISO), 'end': str (ISO)}
                    },
                    '7d': {...},
                    '30d': {...}
                },
                'spread_pattern': str ('exponential' | 'linear' | 'declining' | 'flat'),
                'peak_period': str (which time window had most engagement)
            }
        """
        if not posts:
            return {
                'timeline_buckets': {},
                'spread_pattern': 'none',
                'peak_period': None
            }
        
        if bins is None:
            bins = ['24h', '7d', '30d']
        
        # Parse post timestamps
        now = datetime.now(datetime.now().astimezone().tzinfo)
        
        timeline_buckets = {}
        for bin_name in bins:
            if bin_name == '24h':
                time_delta = timedelta(hours=24)
            elif bin_name == '7d':
                time_delta = timedelta(days=7)
            elif bin_name == '30d':
                time_delta = timedelta(days=30)
            else:
                continue
            
            cutoff_time = now - time_delta
            
            # Filter posts within this window
            posts_in_window = []
            for post in posts:
                created_at = post.get('created_at', '')
                try:
                    # Handle both ISO format timestamps and other formats
                    if isinstance(created_at, str) and created_at:
                        # Try parsing ISO format
                        post_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        if post_time.tzinfo is None:
                            post_time = post_time.replace(tzinfo=datetime.now().astimezone().tzinfo)
                        
                        if post_time >= cutoff_time:
                            posts_in_window.append(post)
                except (ValueError, AttributeError):
                    # If timestamp parsing fails, include in all buckets for broader coverage
                    posts_in_window.append(post)
            
            engagement = sum(p.get('engagement', 0) for p in posts_in_window)
            
            timeline_buckets[bin_name] = {
                'post_count': len(posts_in_window),
                'total_engagement': engagement,
                'growth_rate': 0.0,
                'date_range': {
                    'start': cutoff_time.isoformat(),
                    'end': now.isoformat()
                }
            }
        
        # Calculate growth rates between consecutive buckets
        bucket_order = ['24h', '7d', '30d']
        for i in range(len(bucket_order) - 1):
            current = bucket_order[i]
            previous = bucket_order[i + 1]
            
            if current in timeline_buckets and previous in timeline_buckets:
                prev_engagement = timeline_buckets[previous]['total_engagement']
                curr_engagement = timeline_buckets[current]['total_engagement']
                
                if prev_engagement > 0:
                    growth_rate = ((curr_engagement - prev_engagement) / prev_engagement) * 100
                    timeline_buckets[current]['growth_rate'] = growth_rate
        
        # Determine spread pattern
        engagements = [timeline_buckets.get(b, {}).get('total_engagement', 0) for b in bucket_order if b in timeline_buckets]
        if all(e == 0 for e in engagements):
            spread_pattern = 'none'
        elif len(engagements) >= 2 and engagements[0] > engagements[-1]:
            spread_pattern = 'declining'
        elif len(engagements) >= 2 and sum(engagements[:len(engagements)//2]) < sum(engagements[len(engagements)//2:]):
            spread_pattern = 'exponential'
        else:
            spread_pattern = 'linear'
        
        # Find peak period
        peak_period = max(bucket_order, key=lambda b: timeline_buckets.get(b, {}).get('total_engagement', 0))
        if timeline_buckets.get(peak_period, {}).get('total_engagement', 0) == 0:
            peak_period = None
        
        return {
            'timeline_buckets': timeline_buckets,
            'spread_pattern': spread_pattern,
            'peak_period': peak_period
        }
    
    @staticmethod
    def identify_top_spreaders(posts: list[dict], limit: int = 10) -> list[dict]:
        """
        Identify top accounts/users by engagement.
        
        Args:
            posts: List of posts from scraper.collect()
            limit: Number of top spreaders to return (default: 10)
            
        Returns:
            [
                {
                    'username': str,
                    'author_id': str,
                    'platform': str,
                    'post_count': int,
                    'total_engagement': int,
                    'avg_engagement_per_post': float,
                    'total_likes': int,
                    'total_shares': int,
                    'total_comments': int
                },
                ...
            ]
        """
        if not posts:
            return []
        
        # Aggregate by author
        author_stats = defaultdict(lambda: {
            'username': '',
            'author_id': '',
            'platform': '',
            'post_count': 0,
            'total_likes': 0,
            'total_shares': 0,
            'total_comments': 0,
            'total_engagement': 0
        })
        
        for post in posts:
            author_key = (post.get('author_id', ''), post.get('username', ''))
            
            if author_key[1]:  # Skip if username is empty
                author_stats[author_key]['username'] = post.get('username', '')
                author_stats[author_key]['author_id'] = post.get('author_id', '')
                author_stats[author_key]['platform'] = post.get('platform', 'unknown')
                author_stats[author_key]['post_count'] += 1
                author_stats[author_key]['total_likes'] += post.get('likes', 0)
                author_stats[author_key]['total_shares'] += post.get('shares', 0)
                author_stats[author_key]['total_comments'] += post.get('comments', 0)
                author_stats[author_key]['total_engagement'] += post.get('engagement', 0)
        
        # Calculate averages and sort
        top_spreaders = []
        for author_data in author_stats.values():
            author_data['avg_engagement_per_post'] = (
                author_data['total_engagement'] / author_data['post_count']
                if author_data['post_count'] > 0
                else 0.0
            )
            top_spreaders.append(author_data)
        
        # Sort by total engagement
        top_spreaders.sort(key=lambda x: x['total_engagement'], reverse=True)
        
        return top_spreaders[:limit]
    
    @staticmethod
    def calculate_viral_coefficient(posts: list[dict]) -> dict:
        """
        Calculate virality metrics including doubling time and viral coefficient.
        
        Args:
            posts: List of posts from scraper.collect()
            
        Returns:
            {
                'viral_coefficient': float (0-1 scale, 0=not viral, 1=highly viral),
                'doubling_time_hours': float (hours for engagement to double),
                'growth_rate': float (percentage growth per day),
                'viral_classification': str ('non-viral' | 'slow' | 'moderate' | 'fast' | 'explosive'),
                'virality_score': int (0-100 scale)
            }
        """
        if not posts or len(posts) < 2:
            return {
                'viral_coefficient': 0.0,
                'doubling_time_hours': float('inf'),
                'growth_rate': 0.0,
                'viral_classification': 'non-viral',
                'virality_score': 0
            }
        
        # Get timeline data to calculate growth
        timeline = PropagationMetrics.calculate_timeline(posts)
        timeline_buckets = timeline.get('timeline_buckets', {})
        
        # Calculate growth rate (24h to 7d)
        engagement_24h = timeline_buckets.get('24h', {}).get('total_engagement', 0)
        engagement_7d = timeline_buckets.get('7d', {}).get('total_engagement', 0)
        
        if engagement_24h > 0 and engagement_7d > 0:
            daily_growth_rate = ((engagement_7d / engagement_24h) ** (1/6) - 1) * 100  # 6 days of growth
        else:
            daily_growth_rate = 0.0
        
        # Estimate doubling time using growth rate
        if daily_growth_rate > 0:
            doubling_time_days = 70 / daily_growth_rate  # Rule of 70 for exponential growth
            doubling_time_hours = doubling_time_days * 24
        else:
            doubling_time_hours = float('inf')
        
        # Calculate viral coefficient (0-1 scale)
        # Considers: growth rate, post count, engagement concentration spread
        post_count = len(posts)
        max_posts_for_virality = 100  # Normalize by expected max
        
        platform_diversity = len(timeline.get('platforms_with_posts', []))
        max_platforms = 5
        
        reach_metrics = PropagationMetrics.calculate_total_reach(posts)
        avg_engagement = reach_metrics.get('average_engagement_per_post', 0)
        
        # Viral coefficient: combination of growth, diversity, and engagement
        growth_component = min(daily_growth_rate / 50, 1.0) if daily_growth_rate > 0 else 0.0  # Max 50% growth = max score
        diversity_component = (platform_diversity / max_platforms) * 0.3
        engagement_component = min(avg_engagement / 100, 1.0) * 0.3  # Normalize by 100 avg engagement
        
        viral_coefficient = growth_component * 0.4 + diversity_component + engagement_component
        viral_coefficient = min(max(viral_coefficient, 0.0), 1.0)  # Clamp to 0-1
        
        # Classify virality
        if viral_coefficient < 0.1:
            viral_classification = 'non-viral'
        elif viral_coefficient < 0.3:
            viral_classification = 'slow'
        elif viral_coefficient < 0.6:
            viral_classification = 'moderate'
        elif viral_coefficient < 0.85:
            viral_classification = 'fast'
        else:
            viral_classification = 'explosive'
        
        # Virality score (0-100)
        virality_score = int(viral_coefficient * 100)
        
        return {
            'viral_coefficient': round(viral_coefficient, 3),
            'doubling_time_hours': round(doubling_time_hours, 2) if doubling_time_hours != float('inf') else None,
            'growth_rate': round(daily_growth_rate, 2),
            'viral_classification': viral_classification,
            'virality_score': virality_score
        }
    
    @staticmethod
    def analyze_spread(posts: list[dict]) -> dict:
        """
        Generate complete propagation analysis combining all metrics.
        
        Args:
            posts: List of posts from scraper.collect()
            
        Returns:
            Comprehensive spread analysis with all metrics
        """
        return {
            'total_reach': PropagationMetrics.calculate_total_reach(posts),
            'platform_breakdown': PropagationMetrics.breakdown_by_platform(posts),
            'timeline': PropagationMetrics.calculate_timeline(posts),
            'top_spreaders': PropagationMetrics.identify_top_spreaders(posts),
            'virality': PropagationMetrics.calculate_viral_coefficient(posts)
        }
