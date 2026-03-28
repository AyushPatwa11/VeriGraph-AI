"""
Example: Using Your Live Amplification Feed Data

This shows how to use the actual data you provided 
in the LiveAmplificationFeed component.
"""

# Your original data:
example_data = {
    "posts": [
        {
            "source": "AP News",
            "time": "45m ago",
            "title": "Updates: Breaking:Trump Dies with HeartAttack situation continues to evolve",
            "likes": 312,
            "shares": 128,
        },
        {
            "source": "BBC News",
            "time": "2h ago",
            "title": "Breaking: Latest developments on Breaking:Trump",
            "likes": 245,
            "shares": 89,
        },
        {
            "source": "CNN",
            "time": "30m ago",
            "title": "Report: Key stakeholders respond to Breaking:Trump Dies with HeartAttack proposal",
            "likes": 189,
            "shares": 95,
        },
        {
            "source": "Reuters",
            "time": "1h ago",
            "title": "Analysis: Understanding Breaking:Trump Dies with HeartAttack - experts weigh in",
            "likes": 156,
            "shares": 62,
        },
    ]
}

# ============================================
# REACT COMPONENT USAGE
# ============================================

"""
import { LiveAmplificationFeed } from "@/components/LiveAmplificationFeed";

export function MyFeed() {
  // Transform your data to component format
  const posts = [
    {
      id: "ap-1",
      source: "AP News",
      platform: "news",
      title: "Updates: Breaking news situation continues to evolve",
      likes: 312,
      shares: 128,
      timestamp: "45m ago",
      url: "https://apnews.com/article/...",  // Add link here
      engagement: 440,  // likes + shares
    },
    {
      id: "bbc-1",
      source: "BBC News",
      platform: "news",
      title: "Breaking: Latest developments on claim",
      likes: 245,
      shares: 89,
      timestamp: "2h ago",
      url: "https://bbc.com/news/...",
      engagement: 334,
    },
    {
      id: "cnn-1",
      source: "CNN",
      platform: "news",
      title: "Report: Key stakeholders respond to claim",
      likes: 189,
      shares: 95,
      timestamp: "30m ago",
      url: "https://cnn.com/article/...",
      engagement: 284,
    },
    {
      id: "reuters-1",
      source: "Reuters",
      platform: "news",
      title: "Analysis: Understanding claim - experts weigh in",
      likes: 156,
      shares: 62,
      timestamp: "1h ago",
      url: "https://reuters.com/article/...",
      engagement: 218,
    },
  ];

  return (
    <LiveAmplificationFeed 
      posts={posts}
      isLive={true}
      onLinkClick={(url) => window.open(url, "_blank")}
    />
  );
}
"""

# ============================================
# COMPONENT OUTPUT
# ============================================
"""
The component renders:

┌─────────────────────────────────────────────────────┐
│ 🔴 Live Amplification Feed          4 posts spreading
├─────────────────────────────────────────────────────┤
│                                                       │
│ ● AP NEWS  45m ago                                   │
│   Updates: Breaking news situation continues...      │
│   🔥                                    312 ❤  128 🔄│
│   [======================================] (100%)     │
│   🔗 Click to view source                             │
│                                                       │
│ ● BBC NEWS  2h ago                                    │
│   Breaking: Latest developments on claim              │
│   ✓                                    245 ❤  89 🔄 │
│   [=============================] (76%)               │
│   🔗 Click to view source                             │
│                                                       │
│ ● CNN  30m ago                                        │
│   Report: Key stakeholders respond to claim           │
│   ✓                                    189 ❤  95 🔄 │
│   [============================] (65%)                │
│   🔗 Click to view source                             │
│                                                       │
│ ● REUTERS  1h ago                                     │
│   Analysis: Understanding - experts weigh in          │
│                                     156 ❤  62 🔄    │
│   [====================] (50%)                       │
│   🔗 Click to view source                             │
│                                                       │
├─────────────────────────────────────────────────────┤
│ 🔴 Live — Updates every 30s        Last updated: ... │
└─────────────────────────────────────────────────────┘
"""

# ============================================
# HOW TO GET LINKS
# ============================================

"""
OPTION 1: Use PropagationMetrics API
GET: http://localhost:8000/api/propagation/analyze-spread
{
  "query": "Trump death claim"
}

Response includes:
- Posts from all 5 sources (News, GDELT, Telegram, CommonCrawl, Facebook)
- Each post has "urls" field with original link
- Engagement metrics (likes, shares, comments)

OPTION 2: Get Top Spreaders with Links
Transform top_spreaders list into amplification posts:

const posts = data.analysis.top_spreaders.map((spreader, idx) => ({
  id: `spreader_${idx}`,
  source: spreader.platform,
  platform: spreader.platform,
  title: spreader.username,
  likes: spreader.total_likes,
  shares: spreader.total_shares,
  timestamp: new Date().toISOString(),
  author: spreader.username,
  engagement: spreader.total_engagement,
  url: spreader.url || undefined,  // If available from API
}));

<LiveAmplificationFeed posts={posts} />
"""

# ============================================
# REAL WORLD EXAMPLE
# ============================================

"""
PAGE: /propagation-demo
LOCATION: frontend/src/app/propagation-demo/page.tsx

1. User enters claim: "Trump Dies with HeartAttack"
2. Page calls: POST /api/propagation/analyze-spread
3. API returns metrics AND top spreaders with details
4. Page displays:
   - ScoreDisplay (threat level: CRITICAL)
   - PropagationSpread (virality metrics, timeline, platform distribution)
   - LiveAmplificationFeed (top news outlets spreading claim)

Features:
✓ Each post shows engagement metrics
✓ Click post title to view original source
✓ Platform color coding (AP=red, BBC=blue, CNN=red-orange, Reuters=orange)
✓ Real-time live indicator
✓ High engagement badges (🔥 for 300+ engagement)
✓ Time-ago formatting
✓ Responsive layout
"""

# ============================================
# COMPONENTS WORK TOGETHER
# ============================================

"""
PropagationSpread Component:
- Shows AGGREGATE metrics across all 5 sources
- Timeline analysis
- Growth rates and virality score
- Platform distribution percentages
- Top spreaders list (names + scores)

LiveAmplificationFeed Component:
- Shows INDIVIDUAL posts from spreaders
- With engagement numbers and timestamps
- Clickable links to original posts
- More visual and interactive
- Focuses on specific articles/posts

Together they tell complete story:
1. PropagationSpread = "How viral is this?" (metrics)
2. LiveAmplificationFeed = "Who's spreading it?" (sources)
"""
