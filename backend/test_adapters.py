"""Test Google News and GDELT adapters directly"""
import asyncio
import sys
sys.path.insert(0, '/Users/abhy4/Desktop/VeriGraph AI/backend')

from adapters.google_news_client import GoogleNewsClient
from adapters.gdelt_client import GDELTClient

async def main():
    print('Testing GoogleNewsClient...')
    gn = GoogleNewsClient()
    posts = await gn.search('iran trump')
    print(f'Google News posts: {len(posts)}')
    if posts:
        print(f'First post: {posts[0]}')
    
    print('\nTesting GDELTClient...')
    gdelt = GDELTClient()
    posts = await gdelt.search('iran trump')
    print(f'GDELT posts: {len(posts)}')
    if posts:
        print(f'First post: {posts[0]}')

asyncio.run(main())
