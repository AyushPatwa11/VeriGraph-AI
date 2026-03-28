"""Minimal test of NewsRSSAdapter"""
import asyncio
import sys

async def test():
    print("Importing NewsRSSAdapter...")
    try:
        from adapters.news_rss_adapter import NewsRSSAdapter
        print("✅ Import successful")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("Creating instance...")
    try:
        adapter = NewsRSSAdapter()
        print("✅ Instance created")
    except Exception as e:
        print(f"❌ Instance creation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("Testing search with query 'test'...")
    try:
        result = await adapter.search('test')
        print(f"✅ Search completed, result type: {type(result)}, length: {len(result) if isinstance(result, list) else 'N/A'}")
        if result and isinstance(result, list):
            print(f"   First result: {result[0].keys() if result else 'empty'}")
    except Exception as e:
        print(f"❌ Search failed: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())
print("Done")
