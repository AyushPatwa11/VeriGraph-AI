#!/usr/bin/env python
"""
Diagnostic test for Facebook API issues.
"""

import asyncio
import httpx
from core.settings import settings


async def diagnose_facebook():
    """Diagnose Facebook API issues."""
    print("\n" + "=" * 70)
    print("🔍 FACEBOOK API DIAGNOSTICS")
    print("=" * 70)
    
    # Check 1: Token configuration
    print("\n1️⃣  TOKEN CONFIGURATION")
    print("-" * 70)
    
    if not settings.facebook_access_token:
        print("❌ FATAL: facebook_access_token is EMPTY in .env")
        return False
    
    token = settings.facebook_access_token
    print(f"✅ Token present: {token[:50]}...{token[-20:]}")
    print(f"✅ Token length: {len(token)} characters")
    print(f"✅ Max results: {settings.facebook_max_results}")
    print(f"✅ Timeout: {settings.request_timeout_seconds}s")
    
    # Check 2: Direct API call
    print("\n2️⃣  DIRECT API TEST (no FacebookClient)")
    print("-" * 70)
    
    base_url = "https://graph.facebook.com/v18.0"
    search_endpoint = f"{base_url}/search"
    query = "vaccine"
    
    params = {
        "type": "post",
        "q": query,
        "fields": "id,created_time,message,story,permalink_url,likes.summary(true).limit(0),comments.summary(true).limit(0),shares",
        "limit": 10,
        "access_token": token,
    }
    
    print(f"Endpoint: {search_endpoint}")
    print(f"Query: {query}")
    print(f"Fields: Basic post data")
    print(f"\nSending request...")
    
    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            response = await client.get(search_endpoint, params=params)
            
            print(f"\n✅ Response received!")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                if "error" in data:
                    print(f"\n❌ API ERROR:")
                    error = data["error"]
                    print(f"   Type: {error.get('type')}")
                    print(f"   Code: {error.get('code')}")
                    print(f"   Message: {error.get('message')}")
                    
                    # Detailed error handling
                    if "Invalid OAuth access token" in error.get('message', ''):
                        print(f"\n🔴 TOKEN IS INVALID OR EXPIRED")
                        print(f"   → Need to regenerate at: https://developers.facebook.com/tools/explorer")
                    elif "permission" in error.get('message', '').lower():
                        print(f"\n🔴 MISSING PERMISSIONS")
                        print(f"   → Token needs: public_content")
                    elif "rate limited" in error.get('message', '').lower():
                        print(f"\n🔴 RATE LIMITED")
                        print(f"   → Try again in a few minutes")
                    
                    return False
                
                posts = data.get("data", [])
                print(f"\n✅ SUCCESS! Found {len(posts)} posts")
                
                if posts:
                    print(f"\nSample post:")
                    post = posts[0]
                    print(f"  ID: {post.get('id')}")
                    print(f"  Created: {post.get('created_time')}")
                    print(f"  Message: {post.get('message', post.get('story', 'N/A'))[:100]}")
                    return True
                else:
                    print(f"\n⚠️  No posts found (but API responded OK)")
                    print(f"   This could mean no public posts match your query")
                    return True  # API works, just no results
            
            elif response.status_code == 401:
                print(f"\n❌ AUTHENTICATION FAILED (401)")
                error = response.json()
                if "error" in error:
                    print(f"   {error['error'].get('message')}")
                print(f"   → Token is invalid or expired")
                print(f"   → Regenerate at: https://developers.facebook.com/tools/explorer")
                return False
            
            elif response.status_code == 429:
                print(f"\n❌ RATE LIMITED (429)")
                print(f"   → Facebook API is throttling requests")
                print(f"   → Try again in a few minutes")
                return False
            
            else:
                print(f"\n❌ UNEXPECTED STATUS: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False
    
    except httpx.TimeoutException:
        print(f"\n❌ TIMEOUT")
        print(f"   Request took longer than {settings.request_timeout_seconds}s")
        print(f"   Try increasing REQUEST_TIMEOUT_SECONDS in .env")
        return False
    
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}")
        print(f"   {str(e)}")
        return False


async def test_with_facebook_client():
    """Test using FacebookClient."""
    print("\n\n3️⃣  FACEBOOK CLIENT TEST")
    print("-" * 70)
    
    try:
        from adapters.facebook_client import FacebookClient
        
        client = FacebookClient()
        print(f"✅ FacebookClient created")
        
        results = await client.search("vaccine")
        
        if results:
            print(f"✅ Got {len(results)} results from FacebookClient")
            return True
        else:
            print(f"❌ FacebookClient returned empty list")
            return False
    
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        return False


async def test_scraper():
    """Test scraper with Facebook."""
    print("\n\n4️⃣  SCRAPER TEST (all 5 sources)")
    print("-" * 70)
    
    try:
        from services.scraper import ScraperService
        
        service = ScraperService()
        print(f"✅ ScraperService created with 5 sources")
        
        results = await service.collect("vaccine")
        
        platforms = {}
        for result in results:
            platform = result.get("platform", "unknown")
            platforms[platform] = platforms.get(platform, 0) + 1
        
        print(f"\n✅ Scraper returned {len(results)} total posts")
        print(f"\nBreakdown by platform:")
        for platform, count in sorted(platforms.items()):
            emoji = "⭐" if platform == "facebook" else "  "
            print(f"  {emoji} {platform}: {count}")
        
        if platforms.get("facebook", 0) > 0:
            print(f"\n✅ FACEBOOK DATA IS WORKING!")
            return True
        else:
            print(f"\n❌ No Facebook posts in results")
            return False
    
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        return False


async def main():
    """Run all diagnostics."""
    print("\n")
    print(" " * 70)
    print(" " * 20 + "FACEBOOK TROUBLESHOOTING")
    print(" " * 70)
    
    # Test 1: Direct API
    test1 = await diagnose_facebook()
    
    # Test 2: FacebookClient
    test2 = await test_with_facebook_client()
    
    # Test 3: Scraper
    test3 = await test_scraper()
    
    # Summary
    print("\n\n" + "=" * 70)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 70)
    print(f"Direct API Test:      {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"FacebookClient Test:  {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Scraper Test:         {'✅ PASS' if test3 else '❌ FAIL'}")
    print("=" * 70)
    
    if test1:
        print("\n✅ Facebook API is working correctly!")
    else:
        print("\n❌ Facebook API is not responding")
        print("\nLikely causes:")
        print("1. Token is invalid or expired")
        print("2. Token lacks public_content permission")
        print("3. Network connectivity issue")
        print("\nFix:")
        print("→ Regenerate token: https://developers.facebook.com/tools/explorer")


if __name__ == "__main__":
    asyncio.run(main())
