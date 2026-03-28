"""Simple test to check API responses"""
import asyncio
import httpx

async def test():
    print('Testing Google News RSS...')
    url = 'https://news.google.com/rss/search'
    params = {'q': 'iran'}
    headers = {"User-Agent": "Mozilla/5.0"}
    
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        r = await client.get(url, params=params, headers=headers)
        print(f'Status: {r.status_code}')
        print(f'Length: {len(r.text)}')
        print('First 1000 chars:')
        print(r.text[:1000])

asyncio.run(test())
