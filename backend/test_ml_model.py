#!/usr/bin/env python3
"""
Quick test of the ML fact-checker model
"""
import asyncio
from services.ml_fact_checker import MLFactChecker


async def main():
    print("Initializing ML Fact Checker...")
    checker = MLFactChecker()
    
    test_claims = [
        "The Earth is flat",
        "Water boils at 100 degrees Celsius",
        "COVID-19 was a hoax",
    ]
    
    for claim in test_claims:
        print(f"\nTesting claim: {claim}")
        result = await checker.analyze(claim)
        print(f"Result: {result}")
        print(f"  Score: {result['score']}")
        print(f"  Status: {result['status']}")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Explanation: {result['explanation']}")


if __name__ == "__main__":
    asyncio.run(main())
