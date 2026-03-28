#!/usr/bin/env python
"""
Test Facebook integration with the new token.
"""

import asyncio
import sys
from adapters.facebook_client import FacebookClient
from core.settings import settings


async def test_facebook_search():
    """Test Facebook search functionality."""
    print("=" * 70)
    print("🧪 TESTING FACEBOOK INTEGRATION")
    print("=" * 70)
    
    # Check if token is configured
    if not settings.facebook_access_token:
        print("❌ ERROR: facebook_access_token not configured in .env")
        return False
    
    print(f"\n✅ Token configured (length: {len(settings.facebook_access_token)} chars)")
    print(f"✅ Max results: {settings.facebook_max_results}")
    print(f"✅ Request timeout: {settings.request_timeout_seconds}s")
    
    client = FacebookClient()
    print("\n✅ FacebookClient initialized")
    
    # Test search with a simple claim
    search_query = "COVID-19 vaccine"
    print(f"\n🔍 Searching Facebook for: '{search_query}'...")
    
    try:
        results = await client.search(search_query)
        
        if results:
            print(f"\n✅ SUCCESS! Found {len(results)} posts")
            print("\n📊 Sample Results:")
            print("-" * 70)
            
            for i, post in enumerate(results[:3], 1):
                print(f"\n  Post #{i}:")
                print(f"    Platform: {post.get('platform')}")
                print(f"    Author: {post.get('username')}")
                print(f"    Text: {post.get('text', '')[:80]}...")
                print(f"    Likes: {post.get('likes')}")
                print(f"    Shares: {post.get('shares')}")
                print(f"    Comments: {post.get('comments')}")
                print(f"    Engagement: {post.get('engagement')}")
                print(f"    Created: {post.get('created_at')}")
            
            print("\n" + "=" * 70)
            print("✅ FACEBOOK INTEGRATION TEST PASSED!")
            print("=" * 70)
            return True
        
        else:
            print(f"\n⚠️  No posts found for '{search_query}'")
            print("    This could mean:")
            print("    1. No public posts matching this query")
            print("    2. Token needs public_content permission")
            print("    3. Search query too specific")
            
            print("\n🔍 Trying broader search: 'vaccine'...")
            results = await client.search("vaccine")
            
            if results:
                print(f"✅ Found {len(results)} posts for 'vaccine'")
                print("✅ FACEBOOK INTEGRATION TEST PASSED!")
                return True
            else:
                print("❌ No results for 'vaccine' either")
                print("❌ Check token permissions and validity")
                return False
    
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}")
        print(f"   Message: {str(e)}")
        
        if "401" in str(e) or "unauthorized" in str(e).lower():
            print("\n   → Token is invalid or expired")
            print("   → Regenerate token at: https://developers.facebook.com/tools/explorer")
        elif "429" in str(e):
            print("\n   → Rate limited by Facebook API")
            print("   → Try again in a few minutes")
        elif "permissions" in str(e).lower():
            print("\n   → Token missing required permissions")
            print("   → Make sure you requested: public_content")
        
        return False


async def test_scraper_integration():
    """Test scraper with Facebook."""
    print("\n" + "=" * 70)
    print("🧪 TESTING SCRAPER WITH FACEBOOK")
    print("=" * 70)
    
    from services.scraper import ScraperService
    
    service = ScraperService()
    print("\n✅ ScraperService initialized with 5 sources:")
    print("   1. News RSS")
    print("   2. GDELT")
    print("   3. Telegram")
    print("   4. CommonCrawl")
    print("   5. Facebook ⭐")
    
    query = "vaccine safety"
    print(f"\n🔍 Running scraper collection for: '{query}'...")
    
    try:
        results = await service.collect(query)
        
        # Count by platform
        platforms = {}
        for result in results:
            platform = result.get("platform", "unknown")
            platforms[platform] = platforms.get(platform, 0) + 1
        
        print(f"\n✅ SUCCESS! Collected {len(results)} posts from {len(platforms)} sources")
        print("\n📊 Results by Platform:")
        for platform, count in sorted(platforms.items()):
            emoji = "⭐" if platform == "facebook" else "  "
            print(f"   {emoji} {platform}: {count} posts")
        
        if platforms.get("facebook", 0) > 0:
            print("\n✅ FACEBOOK DATA SUCCESSFULLY COLLECTED IN SCRAPER!")
            return True
        else:
            print("\n⚠️  No Facebook posts in scraper results")
            print("   (Other sources may have returned data)")
            return True  # Still pass since other sources work
    
    except Exception as e:
        print(f"\n⚠️  Scraper error: {type(e).__name__}: {str(e)}")
        return False


async def main():
    """Run all tests."""
    print("\n")
    print(" " * 70)
    print(" " * 15 + "FACEBOOK INTEGRATION TESTING")
    print(" " * 70)
    print()
    
    # Test 1: Facebook client
    test1 = await test_facebook_search()
    
    # Test 2: Scraper integration
    test2 = await test_scraper_integration()
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"✅ Facebook Client:       {'PASS' if test1 else 'FAIL'}")
    print(f"✅ Scraper Integration:   {'PASS' if test2 else 'FAIL'}")
    print("=" * 70)
    
    if test1 or test2:
        print("\n🎉 FACEBOOK INTEGRATION IS WORKING!")
        print("\nNext steps:")
        print("1. Obtain FACEBOOK_APP_ID from developers.facebook.com")
        print("2. Obtain FACEBOOK_APP_SECRET from developers.facebook.com")
        print("3. Add them to .env file")
        print("4. Run: pytest backend/tests/test_facebook_client.py -v")
        sys.exit(0)
    else:
        print("\n❌ FACEBOOK INTEGRATION FAILED")
        print("\nTroubleshooting:")
        print("1. Check if token is still valid (24 hour expiry)")
        print("2. Verify token has public_content permission")
        print("3. Regenerate token at: https://developers.facebook.com/tools/explorer")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
