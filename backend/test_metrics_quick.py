"""Quick test of propagation metrics functionality."""

from datetime import datetime, timezone, timedelta
from services.propagation_metrics import PropagationMetrics

# Create sample posts
now = datetime.now(timezone.utc)
sample_posts = [
    {
        'post_id': 'test_1',
        'author_id': 'user_1',
        'username': 'testuser1',
        'created_at': now.isoformat(),
        'text': 'Test claim',
        'likes': 100,
        'shares': 50,
        'comments': 25,
        'engagement': 175,
        'platform': 'facebook'
    },
    {
        'post_id': 'test_2',
        'author_id': 'user_2',
        'username': 'testuser2',
        'created_at': now.isoformat(),
        'text': 'Test claim',
        'likes': 200,
        'shares': 75,
        'comments': 50,
        'engagement': 325,
        'platform': 'news'
    },
    {
        'post_id': 'test_3',
        'author_id': 'user_1',
        'username': 'testuser1',
        'created_at': now.isoformat(),
        'text': 'Test claim',
        'likes': 80,
        'shares': 30,
        'comments': 20,
        'engagement': 130,
        'platform': 'facebook'
    }
]

print("=" * 60)
print("PROPAGATION METRICS TEST")
print("=" * 60)

# Test 1: Total Reach
print("\n1. TOTAL REACH")
print("-" * 40)
reach = PropagationMetrics.calculate_total_reach(sample_posts)
print(f"Total Reach: {reach['total_reach']}")
print(f"Total Posts: {reach['post_count']}")
print(f"Avg Engagement: {reach['average_engagement_per_post']:.2f}")
print(f"  ├─ Likes: {reach['total_likes']}")
print(f"  ├─ Shares: {reach['total_shares']}")
print(f"  └─ Comments: {reach['total_comments']}")

# Test 2: Platform Breakdown
print("\n2. PLATFORM BREAKDOWN")
print("-" * 40)
breakdown = PropagationMetrics.breakdown_by_platform(sample_posts)
for platform, stats in breakdown['platform_distribution'].items():
    print(f"{platform.upper()}:")
    print(f"  ├─ Posts: {stats['post_count']}")
    print(f"  ├─ Total Engagement: {stats['total_engagement']}")
    print(f"  └─ Reach %: {stats['reach_percentage']:.1f}%")

# Test 3: Top Spreaders
print("\n3. TOP SPREADERS")
print("-" * 40)
spreaders = PropagationMetrics.identify_top_spreaders(sample_posts, limit=5)
for i, spreader in enumerate(spreaders, 1):
    print(f"#{i} {spreader['username']} ({spreader['platform']})")
    print(f"    Engagement: {spreader['total_engagement']} | Posts: {spreader['post_count']}")

# Test 4: Timeline
print("\n4. TIMELINE ANALYSIS")
print("-" * 40)
timeline = PropagationMetrics.calculate_timeline(sample_posts)
for period, data in timeline['timeline_buckets'].items():
    print(f"{period}:")
    print(f"  ├─ Posts: {data['post_count']}")
    print(f"  └─ Engagement: {data['total_engagement']}")
print(f"Spread Pattern: {timeline['spread_pattern']}")

# Test 5: Virality
print("\n5. VIRALITY METRICS")
print("-" * 40)
virality = PropagationMetrics.calculate_viral_coefficient(sample_posts)
print(f"Viral Coefficient: {virality['viral_coefficient']} (0-1 scale)")
print(f"Virality Score: {virality['virality_score']}/100")
print(f"Classification: {virality['viral_classification']}")
print(f"Growth Rate: {virality['growth_rate']:.2f}% per day")
if virality['doubling_time_hours']:
    print(f"Doubling Time: {virality['doubling_time_hours']:.2f} hours")

# Test 6: Complete Analysis
print("\n6. COMPLETE ANALYSIS")
print("-" * 40)
analysis = PropagationMetrics.analyze_spread(sample_posts)
print(f"✓ All metrics calculated successfully")
print(f"✓ Metrics returned: {', '.join(analysis.keys())}")

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED")
print("=" * 60)
