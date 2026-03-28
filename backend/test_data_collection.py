"""Test what data sources are returning"""
import asyncio
import sys

async def test():
    from services.scraper import ScraperService
    
    print("Testing data collection...", file=sys.stderr)
    scraper = ScraperService()
    
    posts = await scraper.collect("Iran ceasefire Trump")
    print(f"Total posts: {len(posts)}", file=sys.stderr)
    
    if posts:
        print(f"Posts by platform:", file=sys.stderr)
        platforms = {}
        for post in posts:
            plat = post.get('platform', 'unknown')
            platforms[plat] = platforms.get(plat, 0) + 1
        for plat, count in platforms.items():
            print(f"  {plat}: {count}", file=sys.stderr)
    
    print(posts[:2])

asyncio.run(test())
