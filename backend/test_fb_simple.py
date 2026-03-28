#!/usr/bin/env python
"""
Simple synchronous test for Facebook API.
"""

import httpx
from core.settings import settings

print("\n" + "=" * 70)
print("🔍 FACEBOOK API TEST")
print("=" * 70)

# Check token
print("\n1. Checking token...")
token = settings.facebook_access_token
if not token:
    print("❌ NO TOKEN CONFIGURED")
    exit(1)

print(f"✅ Token length: {len(token)}")
print(f"✅ Token prefix: {token[:30]}...")

# Test API
print("\n2. Testing Facebook Graph API...")
print("   Endpoint: https://graph.facebook.com/v18.0/search")

base_url = "https://graph.facebook.com/v18.0"
search_endpoint = f"{base_url}/search"

params = {
    "type": "post",
    "q": "vaccine",
    "fields": "id,created_time,message,story",
    "limit": "5",
    "access_token": token,
}

try:
    with httpx.Client(timeout=settings.request_timeout_seconds) as client:
        print("   Sending request...")
        response = client.get(search_endpoint, params=params)
        
        print(f"\n   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if "error" in data:
                error = data["error"]
                print(f"\n   ❌ API ERROR:")
                print(f"      Type: {error.get('type')}")
                print(f"      Code: {error.get('code')}")
                print(f"      Message: {error.get('message')}")
                
                msg = error.get('message', '').lower()
                if "invalid" in msg or "expired" in msg:
                    print(f"\n      🔴 TOKEN IS INVALID OR EXPIRED")
                    print(f"      → Get new token: https://developers.facebook.com/tools/explorer")
                elif "permission" in msg:
                    print(f"\n      🔴 MISSING PERMISSIONS")
                    print(f"      → Add permission: public_content")
            
            elif "data" in data:
                posts = data["data"]
                print(f"\n   ✅ SUCCESS! Found {len(posts)} posts")
                
                if posts:
                    first = posts[0]
                    print(f"\n   Sample post:")
                    print(f"     ID: {first.get('id')}")
                    print(f"     Created: {first.get('created_time')}")
                    msg = first.get('message') or first.get('story', '')
                    print(f"     Text: {msg[:80]}...")
        
        elif response.status_code == 401:
            print(f"   ❌ AUTHENTICATION ERROR (401)")
            error_data = response.json()
            if "error" in error_data:
                print(f"      {error_data['error'].get('message')}")
            print(f"      → Token invalid or expired")
            print(f"      → Get new token: https://developers.facebook.com/tools/explorer")
        
        elif response.status_code == 429:
            print(f"   ❌ RATE LIMITED (429)")
            print(f"      → Try again later")
        
        else:
            print(f"   ❌ ERROR {response.status_code}")
            print(f"      {response.text[:200]}")

except Exception as e:
    print(f"   ❌ {type(e).__name__}: {str(e)}")

print("\n" + "=" * 70)
