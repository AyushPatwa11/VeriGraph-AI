"""
Test suite for Propagation Metrics Service

Tests all metric calculation functions with sample data.
"""

import pytest
from datetime import datetime, timedelta, timezone
from services.propagation_metrics import PropagationMetrics


class TestPropagationMetrics:
    """Test suite for propagation metrics calculations."""
    
    @pytest.fixture
    def sample_posts(self):
        """Sample posts from different platforms for testing."""
        now = datetime.now(timezone.utc)
        yesterday = now - timedelta(hours=24)
        week_ago = now - timedelta(days=7)
        
        return [
            # Facebook posts
            {
                'post_id': 'fb_123_1',
                'author_id': 'user_123',
                'username': 'john_doe',
                'created_at': now.isoformat(),
                'text': 'Check out this amazing claim!',
                'likes': 150,
                'shares': 45,
                'comments': 30,
                'engagement': 225,
                'platform': 'facebook'
            },
            {
                'post_id': 'fb_124_2',
                'author_id': 'user_124',
                'username': 'jane_smith',
                'created_at': yesterday.isoformat(),
                'text': 'Sharing this important information',
                'likes': 200,
                'shares': 60,
                'comments': 50,
                'engagement': 310,
                'platform': 'facebook'
            },
            # News posts
            {
                'post_id': 'news_001',
                'author_id': 'news_outlet',
                'username': 'Reuters',
                'created_at': now.isoformat(),
                'text': 'Breaking news about the claim',
                'likes': 500,
                'shares': 150,
                'comments': 200,
                'engagement': 850,
                'platform': 'news'
            },
            # GDELT posts
            {
                'post_id': 'gdelt_001',
                'author_id': 'gdelt',
                'username': 'gdelt_monitor',
                'created_at': week_ago.isoformat(),
                'text': 'Event detected',
                'likes': 50,
                'shares': 15,
                'comments': 10,
                'engagement': 75,
                'platform': 'gdelt'
            },
            # Telegram posts
            {
                'post_id': 'telegram_001',
                'author_id': 'channel_123',
                'username': 'TelegramChannel',
                'created_at': now.isoformat(),
                'text': 'Forwarding this claim',
                'likes': 100,
                'shares': 50,
                'comments': 25,
                'engagement': 175,
                'platform': 'telegram'
            },
            # CommonCrawl posts
            {
                'post_id': 'cc_001',
                'author_id': 'blog_author',
                'username': 'BlogWriter',
                'created_at': yesterday.isoformat(),
                'text': 'Analysis of the claim',
                'likes': 75,
                'shares': 30,
                'comments': 15,
                'engagement': 120,
                'platform': 'commoncrawl'
            }
        ]
    
    def test_calculate_total_reach_with_posts(self, sample_posts):
        """Test total reach calculation with valid posts."""
        result = PropagationMetrics.calculate_total_reach(sample_posts)
        
        assert result['total_reach'] == 1755  # Sum of all engagement
        assert result['total_likes'] == 1075
        assert result['total_shares'] == 350
        assert result['total_comments'] == 330
        assert result['post_count'] == 6
        assert result['average_engagement_per_post'] == 1755 / 6
    
    def test_calculate_total_reach_empty(self):
        """Test total reach calculation with empty posts."""
        result = PropagationMetrics.calculate_total_reach([])
        
        assert result['total_reach'] == 0
        assert result['post_count'] == 0
        assert result['average_engagement_per_post'] == 0.0
    
    def test_breakdown_by_platform(self, sample_posts):
        """Test platform breakdown calculation."""
        result = PropagationMetrics.breakdown_by_platform(sample_posts)
        
        assert 'platform_distribution' in result
        assert 'platforms_with_posts' in result
        
        distribution = result['platform_distribution']
        assert 'facebook' in distribution
        assert 'news' in distribution
        assert 'gdelt' in distribution
        assert 'telegram' in distribution
        assert 'commoncrawl' in distribution
        
        # Check Facebook stats
        fb_stats = distribution['facebook']
        assert fb_stats['post_count'] == 2
        assert fb_stats['total_engagement'] == 535
        
        # Check News stats (highest engagement)
        news_stats = distribution['news']
        assert news_stats['post_count'] == 1
        assert news_stats['total_engagement'] == 850
    
    def test_breakdown_by_platform_percentages(self, sample_posts):
        """Test that platform breakdowns add up to 100%."""
        result = PropagationMetrics.breakdown_by_platform(sample_posts)
        
        distribution = result['platform_distribution']
        total_percentage = sum(p['reach_percentage'] for p in distribution.values())
        
        assert abs(total_percentage - 100.0) < 0.01  # Account for floating point precision
    
    def test_calculate_timeline(self, sample_posts):
        """Test timeline calculation."""
        result = PropagationMetrics.calculate_timeline(sample_posts)
        
        assert 'timeline_buckets' in result
        assert 'spread_pattern' in result
        assert 'peak_period' in result
        
        timeline_buckets = result['timeline_buckets']
        assert '24h' in timeline_buckets
        assert '7d' in timeline_buckets
        assert '30d' in timeline_buckets
        
        # Check structure
        for bucket_name, bucket_data in timeline_buckets.items():
            assert 'post_count' in bucket_data
            assert 'total_engagement' in bucket_data
            assert 'growth_rate' in bucket_data
            assert 'date_range' in bucket_data
    
    def test_identify_top_spreaders(self, sample_posts):
        """Test top spreaders identification."""
        result = PropagationMetrics.identify_top_spreaders(sample_posts, limit=3)
        
        assert len(result) <= 3
        assert all('username' in spreader for spreader in result)
        assert all('total_engagement' in spreader for spreader in result)
        
        # First spreader should have highest engagement
        if len(result) > 0:
            assert result[0]['total_engagement'] >= result[-1]['total_engagement']
    
    def test_identify_top_spreaders_empty(self):
        """Test top spreaders with empty posts."""
        result = PropagationMetrics.identify_top_spreaders([])
        assert result == []
    
    def test_identify_top_spreaders_limit(self, sample_posts):
        """Test that top spreaders respects limit."""
        result = PropagationMetrics.identify_top_spreaders(sample_posts, limit=2)
        assert len(result) <= 2
        
        result = PropagationMetrics.identify_top_spreaders(sample_posts, limit=100)
        assert len(result) <= len(sample_posts)
    
    def test_calculate_viral_coefficient(self, sample_posts):
        """Test viral coefficient calculation."""
        result = PropagationMetrics.calculate_viral_coefficient(sample_posts)
        
        assert 'viral_coefficient' in result
        assert 'doubling_time_hours' in result
        assert 'growth_rate' in result
        assert 'viral_classification' in result
        assert 'virality_score' in result
        
        # Viral coefficient should be between 0 and 1
        assert 0 <= result['viral_coefficient'] <= 1.0
        
        # Virality score should be 0-100
        assert 0 <= result['virality_score'] <= 100
        
        # Check valid classification
        valid_classifications = ['non-viral', 'slow', 'moderate', 'fast', 'explosive']
        assert result['viral_classification'] in valid_classifications
    
    def test_calculate_viral_coefficient_empty(self):
        """Test viral coefficient with empty posts."""
        result = PropagationMetrics.calculate_viral_coefficient([])
        
        assert result['viral_coefficient'] == 0.0
        assert result['doubling_time_hours'] is None or result['doubling_time_hours'] == float('inf')
        assert result['viral_classification'] == 'non-viral'
        assert result['virality_score'] == 0
    
    def test_analyze_spread_complete(self, sample_posts):
        """Test complete spread analysis."""
        result = PropagationMetrics.analyze_spread(sample_posts)
        
        assert 'total_reach' in result
        assert 'platform_breakdown' in result
        assert 'timeline' in result
        assert 'top_spreaders' in result
        assert 'virality' in result
        
        # Verify structure of each component
        assert 'total_reach' in result['total_reach']
        assert 'platform_distribution' in result['platform_breakdown']
        assert 'timeline_buckets' in result['timeline']
        assert isinstance(result['top_spreaders'], list)
        assert 'viral_coefficient' in result['virality']
    
    def test_analyze_spread_empty(self):
        """Test analyze_spread with empty posts."""
        result = PropagationMetrics.analyze_spread([])
        
        assert result['total_reach']['post_count'] == 0
        assert result['platform_breakdown']['platform_distribution'] == {}
        assert result['virality']['viral_coefficient'] == 0.0


class TestMetricsEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_posts_with_missing_engagement_fields(self):
        """Test handling of posts missing engagement fields."""
        posts = [
            {
                'post_id': 'test_1',
                'author_id': 'user_1',
                'username': 'testuser',
                'created_at': datetime.now(timezone.utc).isoformat(),
                'text': 'Test post',
                'platform': 'test'
                # Missing likes, shares, comments
            }
        ]
        
        result = PropagationMetrics.calculate_total_reach(posts)
        assert result['total_reach'] == 0  # Should default to 0
    
    def test_posts_with_zero_engagement(self):
        """Test handling of posts with zero engagement."""
        posts = [
            {
                'post_id': 'test_1',
                'author_id': 'user_1',
                'username': 'testuser',
                'created_at': datetime.now(timezone.utc).isoformat(),
                'text': 'Test post',
                'likes': 0,
                'shares': 0,
                'comments': 0,
                'engagement': 0,
                'platform': 'test'
            }
        ]
        
        result = PropagationMetrics.calculate_total_reach(posts)
        assert result['total_reach'] == 0
        assert result['post_count'] == 1
    
    def test_single_post(self):
        """Test metrics with single post."""
        posts = [
            {
                'post_id': 'test_1',
                'author_id': 'user_1',
                'username': 'testuser',
                'created_at': datetime.now(timezone.utc).isoformat(),
                'text': 'Test post',
                'likes': 10,
                'shares': 5,
                'comments': 3,
                'engagement': 18,
                'platform': 'test'
            }
        ]
        
        result = PropagationMetrics.analyze_spread(posts)
        assert result['total_reach']['post_count'] == 1
        assert result['top_spreaders'][0]['username'] == 'testuser'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
