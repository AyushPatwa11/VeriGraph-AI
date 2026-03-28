#!/usr/bin/env python3
"""Test API via simple HTTP request"""
import httpx
import json
import sys

def test_api():
    client = httpx.Client(timeout=30)
    try:
        print("Making POST request to /api/analyze...", file=sys.stderr)
        response = client.post(
            'http://127.0.0.1:8000/api/analyze',
            json={'query': 'Iran ceasefire Trump'}
        )
        print(f"Status: {response.status_code}", file=sys.stderr)
        print(f"Response: {response.text}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
    finally:
        client.close()

if __name__ == '__main__':
    test_api()
