#!/usr/bin/env python3
"""
Test the ML fact-checker via API
"""
import asyncio
import httpx
import json


async def test_api():
    async with httpx.AsyncClient() as client:
        # Test health endpoint
        print("Testing health endpoint...")
        response = await client.get("http://localhost:8000/health")
        print(f"Health: {response.json()}\n")
        
        # Test analysis endpoint
        test_claim = "The Earth is flat"
        print(f"Testing analysis with claim: '{test_claim}'")
        
        response = await client.post(
            "http://localhost:8000/api/analyze",
            json={"query": test_claim}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Final Score: {result.get('finalScore')}")
            print(f"✓ Risk Level: {result.get('riskLevel')}")
            print(f"✓ Confidence: {result.get('confidence')}")
            print(f"✓ Summary: {result.get('summary')}")
            print(f"\n✓ Layers:")
            for layer in result.get('layers', []):
                print(f"  - {layer.get('name')}: score={layer.get('score')}, status={layer.get('status')}")
        else:
            print(f"✗ Status: {response.status_code}")
            print(f"Error: {response.text}")


if __name__ == "__main__":
    asyncio.run(test_api())
