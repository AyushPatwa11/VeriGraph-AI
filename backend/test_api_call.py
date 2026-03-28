"""Test the /api/analyze endpoint"""
import asyncio
import httpx
import json

async def test_analyze():
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.post(
                'http://localhost:8000/api/analyze',
                json={'query': 'Iran ceasefire Trump negotiations'}
            )
            print(f'Status Code: {response.status_code}')
            
            if response.status_code == 200:
                data = response.json()
                print(f'Posts collected: {len(data.get("posts", []))}')
                print(f'Risk Level: {data.get("riskLevel")}')
                print(f'Final Score: {data.get("finalScore")}')
                print(f'Status: {data.get("resultStatus")}')
                
                # Show first few posts
                posts = data.get('posts', [])
                if posts:
                    print(f'\nFirst 3 posts:')
                    for i, post in enumerate(posts[:3]):
                        print(f'  [{i+1}] {post.get("platform")}: {post.get("text")[:60]}...')
                else:
                    print('No posts collected')
            else:
                print(f'Error: {response.text[:300]}')
        except Exception as e:
            print(f'Connection Error: {e}')

asyncio.run(test_analyze())
