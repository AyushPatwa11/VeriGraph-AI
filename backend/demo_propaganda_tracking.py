#!/usr/bin/env python
"""
Demo: Propaganda Tracking with Facebook
Shows how to search for claim spread across Facebook
"""

import asyncio
import sys


async def demo_facebook_propaganda_tracking():
    """Demo propaganda tracking with Facebook."""
    print("\n" + "=" * 80)
    print("📊 VERIGRAPH AI - PROPAGANDA TRACKING WITH FACEBOOK")
    print("=" * 80)
    
    # Import services
    from services.scraper import ScraperService
    
    print("\n✅ Services initialized")
    print("   • News RSS Feed")
    print("   • GDELT (Global Event, Language & Tone Dataset)")
    print("   • Telegram Public Channels")
    print("   • CommonCrawl (Web Archive)")
    print("   • Facebook Public Posts ⭐")
    
    # Example claim to track
    claim = "COVID-19 vaccine causes infertility"
    
    print(f"\n📋 TRACKING PROPAGANDA SPREAD")
    print(f"   Claim: '{claim}'")
    print(f"\n🔍 Searching across all platforms...")
    
    try:
        scraper = ScraperService()
        results = await scraper.collect(claim)
        
        # Organize results
        by_platform = {}
        for result in results:
            platform = result.get("platform", "unknown")
            if platform not in by_platform:
                by_platform[platform] = []
            by_platform[platform].append(result)
        
        print(f"\n" + "=" * 80)
        print(f"✅ FOUND {len(results)} TOTAL POSTS")
        print("=" * 80)
        
        # Show breakdown
        print("\n📊 BREAKDOWN BY PLATFORM:")
        print("-" * 80)
        for platform in sorted(by_platform.keys()):
            count = len(by_platform[platform])
            emoji = "⭐" if platform == "facebook" else "  "
            bar = "█" * (count // 5)  # Visual representation
            print(f"{emoji} {platform.upper():15} {count:3} posts {bar}")
        
        # Show Facebook results in detail
        if "facebook" in by_platform:
            facebook_posts = by_platform["facebook"]
            
            print(f"\n" + "=" * 80)
            print(f"⭐ FACEBOOK RESULTS ({len(facebook_posts)} posts)")
            print("=" * 80)
            
            if facebook_posts:
                for i, post in enumerate(facebook_posts[:5], 1):
                    print(f"\n📌 POST #{i}")
                    print(f"   Author: {post.get('username', 'Unknown')}")
                    print(f"   Date: {post.get('created_at', 'Unknown')}")
                    print(f"   Text: {post.get('text', '')[:100]}...")
                    print(f"   Engagement Metrics:")
                    print(f"      👍 Likes: {post.get('likes', 0)}")
                    print(f"      🔄 Shares: {post.get('shares', 0)}")
                    print(f"      💬 Comments: {post.get('comments', 0)}")
                    total = post.get('engagement', 0)
                    print(f"      📈 Total Engagement: {total}")
                
                # Analysis
                print(f"\n" + "=" * 80)
                print("📈 PROPAGANDA SPREAD ANALYSIS")
                print("=" * 80)
                
                total_engagement = sum(p.get('engagement', 0) for p in facebook_posts)
                avg_engagement = total_engagement / len(facebook_posts) if facebook_posts else 0
                
                print(f"\nFacebook Statistics:")
                print(f"   Total Posts: {len(facebook_posts)}")
                print(f"   Total Engagement: {total_engagement}")
                print(f"   Average Engagement: {avg_engagement:.1f}")
                
                # Identify top spreaders
                top_spreaders = sorted(
                    facebook_posts,
                    key=lambda x: x.get('engagement', 0),
                    reverse=True
                )[:3]
                
                if top_spreaders:
                    print(f"\n   🔴 TOP SPREADERS:")
                    for i, post in enumerate(top_spreaders, 1):
                        author = post.get('username', 'Unknown')
                        engagement = post.get('engagement', 0)
                        print(f"      {i}. {author} ({engagement} engagement)")
                
                # Identify viral pattern
                if facebook_posts:
                    high_engagement = sum(1 for p in facebook_posts if p.get('engagement', 0) > avg_engagement)
                    viral_rate = (high_engagement / len(facebook_posts)) * 100
                    
                    print(f"\n   📊 VIRALITY SCORE:")
                    if viral_rate > 50:
                        level = "🔴 VERY HIGH - RAPID SPREAD"
                    elif viral_rate > 30:
                        level = "🟠 HIGH - WIDESPREAD SHARING"
                    elif viral_rate > 10:
                        level = "🟡 MODERATE - GROWING"
                    else:
                        level = "🟢 LOW - LIMITED SPREAD"
                    
                    print(f"      {level}")
                    print(f"      {viral_rate:.1f}% of posts have above-average engagement")
        
        else:
            print(f"\n⚠️  NO FACEBOOK DATA FOUND")
            print(f"\nPossible reasons:")
            print(f"   1. Token is invalid or expired")
            print(f"   2. No public posts match this claim")
            print(f"   3. Token needs 'public_content' permission")
            print(f"\nFix:")
            print(f"   → Regenerate token: https://developers.facebook.com/tools/explorer")
            print(f"   → Add 'public_content' permission")
        
        # Other platforms
        if len(by_platform) > 1:
            print(f"\n" + "=" * 80)
            print(f"📰 OTHER SOURCES")
            print("=" * 80)
            for platform in sorted(by_platform.keys()):
                if platform != "facebook":
                    print(f"\n{platform.upper()}: {len(by_platform[platform])} posts")
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}")
        print(f"   {str(e)}")
        
        import traceback
        print(f"\nFull error:")
        traceback.print_exc()
        return False
    
    print(f"\n" + "=" * 80)
    print("✅ DEMO COMPLETE")
    print("=" * 80)
    return True


async def main():
    """Run demo."""
    success = await demo_facebook_propaganda_tracking()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
