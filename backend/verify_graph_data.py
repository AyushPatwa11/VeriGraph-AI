"""Test API response now has graph data"""
import httpx
import json

client = httpx.Client(timeout=30)
try:
    response = client.post(
        'http://127.0.0.1:8000/api/analyze',
        json={'query': 'Iran ceasefire'}
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ API Status: 200 OK")
        print(f"Posts: {len(data.get('posts', []))}")
        print(f"Nodes: {len(data.get('nodes', []))}")
        print(f"Links: {len(data.get('links', []))}")
        print(f"Risk Level: {data.get('riskLevel')}")
        
        if data.get('nodes'):
            print("\nNodes (for graph):")
            for node in data['nodes'][:3]:
                print(f"  - {node['label']} (followers: {node['followers']})")
        
        if data.get('posts'):
            print("\nPosts:")
            for post in data['posts'][:2]:
                print(f"  - {post['username']}: {post['text'][:60]}...")
    else:
        print(f"❌ Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
finally:
    client.close()
