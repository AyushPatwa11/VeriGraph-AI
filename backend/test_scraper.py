"""Test just the scraper"""
import asyncio
import sys

async def test():
    print("Testing ScraperService.collect()...")
    try:
        from services.scraper import ScraperService
        print("✅ ScraperService imported")
        
        scraper = ScraperService()
        print("✅ ScraperService instance created")
        
        print("Starting search for 'test'...")
        result = await scraper.collect("test")
        print(f"✅ Scraper completed, got {len(result)} posts")
        
        if result:
            print(f"   First post platform: {result[0].get('platform')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())
