"""Debug script to test and fix Google News and GDELT data collection"""
import asyncio
import httpx
import xml.etree.ElementTree as ET
from datetime import datetime

async def test_google_news_raw():
    """Test raw Google News response"""
    print('=' * 70)
    print('[1] GOOGLE NEWS - RAW RESPONSE TEST')
    print('=' * 70)
    
    url = 'https://news.google.com/rss/search'
    params = {'q': 'iran trump'}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            response = await client.get(url, params=params, headers=headers)
            print(f'Status Code: {response.status_code}')
            print(f'Headers: Content-Type={response.headers.get("content-type")}')
            print(f'Response length: {len(response.text)} bytes')
            
            if response.status_code == 200:
                # Try to parse XML
                try:
                    root = ET.fromstring(response.text)
                    items = root.findall('.//item')
                    print(f'✅ XML parsed successfully. Items found: {len(items)}')
                    
                    if items:
                        item = items[0]
                        print(f'\nFirst item tags:')
                        for child in item:
                            text = child.text[:80] if child.text else "(empty)"
                            print(f'  {child.tag}: {text}')
                except ET.ParseError as e:
                    print(f'❌ XML Parse Error: {e}')
                    print(f'First 500 chars: {response.text[:500]}')
            else:
                print(f'Response text preview: {response.text[:300]}')
    except Exception as e:
        print(f'Error: {type(e).__name__}: {e}')


async def test_gdelt_raw():
    """Test raw GDELT response"""
    print('\n' + '=' * 70)
    print('[2] GDELT API - RAW RESPONSE TEST')
    print('=' * 70)
    
    url = 'https://api.gdeltproject.org/api/v2/doc/doc'
    params = {
        'query': 'iran trump',
        'mode': 'ArtList',
        'format': 'json',
        'sortby': 'PublDate',
        'maxrecords': 20,
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url, params=params, headers=headers)
            print(f'Status Code: {response.status_code}')
            print(f'Response length: {len(response.text)} bytes')
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f'✅ JSON parsed successfully')
                    print(f'Top-level keys: {list(data.keys())}')
                    
                    if 'articles' in data:
                        articles = data['articles']
                        print(f'Articles count: {len(articles)}')
                        
                        if articles:
                            print(f'\nFirst article:')
                            for key, val in list(articles[0].items())[:5]:
                                preview = str(val)[:80]
                                print(f'  {key}: {preview}')
                except Exception as e:
                    print(f'JSON parse error: {e}')
                    print(f'Response text: {response.text[:300]}')
            else:
                print(f'Response text: {response.text[:500]}')
    except Exception as e:
        print(f'Error: {type(e).__name__}: {e}')


async def test_adapters():
    """Test the actual adapters with debugging"""
    print('\n' + '=' * 70)
    print('[3] TESTING ADAPTER IMPLEMENTATIONS')
    print('=' * 70)
    
    from adapters.google_news_client import GoogleNewsClient
    from adapters.gdelt_client import GDELTClient
    
    # Test Google News
    print('\nGoogle News Adapter:')
    gn = GoogleNewsClient()
    
    # Test keyword extraction
    query = 'iran trump negotiations'
    keywords = gn._extract_keywords(query)
    print(f'  Keywords extracted: {keywords}')
    
    # Test search
    try:
        posts = await gn.search(query)
        print(f'  Posts collected: {len(posts)}')
        if posts:
            print(f'  First post ID: {posts[0]["id"]}')
            print(f'  First post text: {posts[0]["text"][:80]}')
    except Exception as e:
        print(f'  Error: {e}')
    
    # Test GDELT
    print('\nGDELT Adapter:')
    gdelt = GDELTClient()
    
    keywords = gdelt._extract_keywords(query)
    print(f'  Keywords extracted: {keywords}')
    
    try:
        posts = await gdelt.search(query)
        print(f'  Posts collected: {len(posts)}')
        if posts:
            print(f'  First post ID: {posts[0]["id"]}')
            print(f'  First post text: {posts[0]["text"][:80]}')
    except Exception as e:
        print(f'  Error: {e}')


async def main():
    await test_google_news_raw()
    await test_gdelt_raw()
    await test_adapters()


if __name__ == '__main__':
    asyncio.run(main())
