"""Test API response structure"""
import httpx
import json

try:
    client = httpx.Client(timeout=30)
    response = client.post(
        'http://127.0.0.1:8000/api/analyze',
        json={'query': 'Iran ceasefire'}
    )
    
    if response.status_code == 200:
        data = response.json()
        print("Status: 200 OK")
        print(f"\nResponse keys: {list(data.keys())}")
        print(f"Posts: {len(data.get('posts', []))}")
        print(f"Nodes: {len(data.get('nodes', []))}")
        print(f"Links: {len(data.get('links', []))}")
        
        if data.get('nodes'):
            print(f"\nFirst node: {data['nodes'][0]}")
        if data.get('links'):
            print(f"First link: {data['links'][0]}")
            
        # Show the full structure
        print(f"\nFull response (truncated):")
        print(json.dumps(data, indent=2)[:1000])
    else:
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
finally:
    client.close()
