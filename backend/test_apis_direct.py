"""Direct test of Google News and GDELT APIs"""
import asyncio
import httpx

# Test Google News directly
async def test_google_news():
    url = 'https://news.google.com/rss/search'
    params = {'q': 'iran trump negotiations ceasefire'}
    print('Testing Google News RSS...')
    async with httpx.AsyncClient(timeout=15) as client:
        try:
            response = await client.get(url, params=params)
            print(f'Status: {response.status_code}')
            if response.status_code == 200:
                content = response.text[:800]
                print('Content preview:')
                print(content)
        except Exception as e:
            print(f'Error: {e}')

# Test GDELT directly
async def test_gdelt():
    url = 'https://api.gdeltproject.org/api/v2/doc/doc'
    params = {
        'query': 'iran trump negotiations ceasefire',
        'mode': 'ArtList',
        'format': 'json',
        'sortby': 'PublDate',
        'maxrecords': 40
    }
    print('\nTesting GDELT API...')
    async with httpx.AsyncClient(timeout=15) as client:
        try:
            response = await client.get(url, params=params)
            print(f'Status: {response.status_code}')
            if response.status_code == 200:
                data = response.json()
                print(f'Response keys: {list(data.keys())}')
                print(f'Articles count: {len(data.get("articles", []))}')
                if data.get('articles'):
                    print(f'First article keys: {list(data["articles"][0].keys())}')
                    print(f'First article: {data["articles"][0]}')
        except Exception as e:
            print(f'Error: {e}')

asyncio.run(test_google_news())
asyncio.run(test_gdelt())
