# Facebook & Reddit Integration Setup Guide

This guide explains how to configure Facebook and Reddit API access for propaganda spread tracking in VeriGraph AI.

## Overview

The VeriGraph AI backend now includes adapters for collecting posts and discussions from:
- **Facebook**: Public posts mentioning claims via Graph API
- **Reddit**: Posts and comments across subreddits via PRAW

These integrations enable tracking how claims spread across social platforms and detecting echo chambers.

## Prerequisites

- Python 3.10+
- `praw==7.7.0` (installed via `pip install -r requirements.txt`)
- Facebook Developer Account
- Reddit Developer Account (for PRAW)

## Facebook Setup

### 1. Create Facebook Developer Account

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Sign in with your Facebook account (create one if needed)
3. Click **My Apps** → **Create App**
4. Choose app type: **Consumer** (for collecting public data)
5. Fill in app name, purpose, and category

### 2. Generate Access Token

1. In your app dashboard, go to **Settings** → **Basic**
   - Save your **App ID** and **App Secret**

2. Under **Tools**, find the **Access Token Tool**
   - Select your app from dropdown
   - Click **Get User Access Token**
   - Request these permissions:
     - `public_content` (read public posts)
     - `pages_read_engagement` (read post metrics)
   - Copy the generated **User Access Token** (valid for 2 months)

   **Alternative for longer-lived tokens:**
   - Use the Graph API Explorer at [graph.facebook.com](https://graph.facebook.com/explorer)
   - Select your app, then generate token with extended permissions
   - Token expires in ~60 days; you'll need to refresh periodically

### 3. Configure Environment Variables

Add to your `.env` file:

```bash
# Facebook Graph API Configuration
facebook_access_token=<your_user_access_token>
facebook_app_id=<your_app_id>
facebook_app_secret=<your_app_secret>
facebook_max_results=50
```

**Example:**
```bash
facebook_access_token=EABsbCS1iZC4BAJw7ZC...
facebook_app_id=123456789012345
facebook_app_secret=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
facebook_max_results=50
```

### 4. Test Facebook Integration

```python
from adapters.facebook_client import FacebookClient

async def test_facebook():
    client = FacebookClient()
    posts = await client.search("vaccine safety")
    print(f"Found {len(posts)} posts about vaccine safety")
    for post in posts:
        print(f"  {post['username']}: {post['text'][:100]}...")
        print(f"    Engagement: {post['engagement']}")

# Run with: asyncio.run(test_facebook())
```

### 5. Refresh Expired Token

Facebook tokens expire after ~60 days. To refresh:

1. Return to [graph.facebook.com/explorer](https://graph.facebook.com/explorer)
2. Select your app and user
3. Generate new token
4. Update `.env` file with new `facebook_access_token`

---

## Reddit Setup

### 1. Create Reddit Developer Account

1. Go to [reddit.com](https://reddit.com) and create/login to account
2. Go to [reddit.com/user/[yourname]/settings/apps](https://reddit.com/user/settings/apps)
3. Click **Create App** or **Create Another App**
4. Choose app type: **script** (for automated access)
5. Fill in:
   - **Name**: "VeriGraph AI" or similar
   - **App type**: Script
   - **Redirect URI**: `http://localhost:8000` (not used for script apps)
6. Click **Create app**

### 2. Get Your Credentials

After creating the app, you'll see:
- **Client ID**: Short code under app name (⚠️ NOT the same as username)
- **Client Secret**: Long secret string (keep this secure!)
- **User Agent**: You'll set this in config

Example credentials display:
```
VeriGraph AI
ID: a1b2c3d4e5f6g7
SECRET: ••••••••••••••••••••••••••••••
```

### 3. Configure Environment Variables

Add to your `.env` file:

```bash
# Reddit API Configuration
reddit_client_id=<your_client_id>
reddit_client_secret=<your_client_secret>
reddit_user_agent=VeriGraph/1.0 (by YourRedditUsername)
reddit_max_results=50
```

**Example:**
```bash
reddit_client_id=a1b2c3d4e5f6g7
reddit_client_secret=aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890
reddit_user_agent=VeriGraph/1.0 (by my_reddit_username)
reddit_max_results=50
```

**Note on User Agent:**
- Must follow the format shown (app name/version with contact info)
- Used by Reddit to identify your app in their logs
- Replace `my_reddit_username` with your actual Reddit username
- If you don't have a username contact yet, use an email: `VeriGraph/1.0 (by admin@example.com)`

### 4. Test Reddit Integration

```python
from adapters.reddit_client import RedditClient

async def test_reddit():
    client = RedditClient()
    
    # Search for discussions
    posts = await client.search("vaccine safety")
    print(f"Found {len(posts)} posts about vaccine safety")
    for post in posts:
        print(f"  {post['author']} in r/{post['subreddit']}: {post['text'][:100]}...")
        print(f"    Score: {post['score']}, Type: {post['type']}")
    
    # Detect echo chambers
    chambers = await client.detect_echo_chambers("vaccine safety")
    print(f"\nEcho chambers detected:")
    for subreddit, intensity in chambers.items():
        print(f"  r/{subreddit}: {intensity:.1%}")

# Run with: asyncio.run(test_reddit())
```

### 5. Important Reddit API Limits

- **Rate limit**: Requests are throttled by Reddit
- **Search scope**: Searches recent 1000 submissions (limited by Reddit API)
- **Maximum results per search**: Recommend keeping `reddit_max_results` ≤ 50
- **Timeout**: Default 15 seconds (adjustable in `request_timeout_seconds`)

If you hit rate limits, Reddit will respond with 429 status. The client handles this gracefully and returns an empty list.

---

## Configuration in Code

Both adapters load credentials from environment variables via `core/settings.py`:

```python
from core.settings import settings

# These are automatically loaded from .env
print(settings.facebook_access_token)
print(settings.reddit_client_id)
print(settings.reddit_client_secret)
print(settings.reddit_user_agent)
```

## Using in the Scraper

Once configured, Facebook and Reddit automatically participate in the scraper workflow:

```python
from services.scraper import ScraperService

service = ScraperService()
results = await service.collect("vaccine mandate")

# Results include posts from:
# - News RSS feeds
# - GDELT (news events database)
# - Telegram public channels
# - CommonCrawl (web archive)
# - Facebook (now!)
# - Reddit (now!)
```

Results are sorted by engagement and deduplicated by URL.

---

## Troubleshooting

### Facebook Token Expired
**Error**: `ModuleNotFoundError` or empty results always
**Solution**: Refresh token by re-generating in Graph Explorer and updating `.env`

### Reddit Authentication Failed
**Error**: `InvalidToken` exception
**Solution**: Verify credentials are correct in `.env`. Note: Client ID is NOT your username!

### No Results Returned
**Possible causes**:
1. Token/credentials not configured (check `.env`)
2. Query is too specific (try broader terms)
3. Facebook: Token doesn't have `public_content` permission
4. Reddit: Search timeout exceeded (increase `request_timeout_seconds`)

### Rate Limited
**Error**: Scraper returns fewer results than expected
**Solution**: 
- Increase delay between requests (add in scraper config)
- Reduce `facebook_max_results` or `reddit_max_results`
- Both APIs have generous limits; shouldn't hit unless searching very frequently

### Timeout Errors
**Error**: `httpx.TimeoutException` or `TimeoutError`
**Solution**: Increase `request_timeout_seconds` in `.env` (default 15 seconds)

```bash
request_timeout_seconds=30
```

---

## Security Best Practices

1. **Never commit credentials**: Keep `.env` out of git
   - Add `.env` to `.gitignore`
   - Use `.env.example` as template for others

2. **Rotate tokens regularly**: 
   - Facebook tokens expire every 60 days
   - Facebook app secret should be rotated periodically
   - Keep Reddit client secret secure

3. **Limit scope of permissions**:
   - Facebook: Only request `public_content` (don't request user_friends, etc.)
   - Reddit: Script apps only read; don't have write permissions

4. **API usage monitoring**:
   - Facebook Graph API provides usage dashboards at [developers.facebook.com](https://developers.facebook.com)
   - Reddit shows API calls in your app settings
   - Monitor for unexpected high usage patterns

---

## Rate Limiting & Quotas

### Facebook Graph API
- **User Token**: No hard limit (fair use policy applies)
- **Throttling**: May return 429 if making excessive requests
- **Recovery**: Automatic backoff in VeriGraph (returns empty list)
- **Best practice**: Implement caching (already in place) to avoid duplicate searches

### Reddit API (PRAW)
- **Rate Limit**: 60 requests/minute per user-agent
- **Soft limit**: Reddit may apply slower responses if you exceed ~30/min
- **Recovery**: PRAW handles automatically with backoff
- **Best practice**: Batch searches together when possible

---

## Testing Your Setup

Run the included test suite:

```bash
# Test Facebook client
pytest backend/tests/test_facebook_client.py -v

# Test Reddit client
pytest backend/tests/test_reddit_client.py -v

# Test full integration
pytest backend/tests/test_propagation_integration.py -v

# Run all tests
pytest backend/tests/ -v
```

---

## Performance Notes

### Search Performance
- **Facebook**: ~1-2 seconds per search (depends on results volume)
- **Reddit**: ~3-5 seconds per search (comment fetching takes time)
- Both run in parallel via asyncio for maximum efficiency

### Result Quality
- **Facebook**: Searches public posts; includes engagement metrics (likes, shares, comments)
- **Reddit**: Searches both posts and top comments; includes subreddit context for echo chamber detection

### Caching
- Both clients are integrated with the existing Redis cache layer
- Same query repeated within 1 hour will return cached results
- Cache hit reduces response time to <100ms

---

## Next Steps

1. ✅ Set up Facebook developer account and token
2. ✅ Set up Reddit developer app and credentials
3. ✅ Add credentials to `.env` file
4. ✅ Run test suite to verify setup
5. Start collecting propaganda spread data across social platforms!

See [QUICKSTART.md](./QUICKSTART.md) for full backend setup instructions.
