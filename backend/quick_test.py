"""Simple test without async issues"""
import httpx
import json

try:
    client = httpx.Client(timeout=15)
    response = client.post(
        'http://127.0.0.1:8000/api/analyze',
        json={'query': 'Iran ceasefire Trump'}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"Posts: {len(data.get('posts', []))}")
    else:
        print(f"Error: {response.text}")
finally:
    client.close()
