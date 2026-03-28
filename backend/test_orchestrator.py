"""Direct test of orchestrator"""
import asyncio
import sys

async def test():
    print("Testing orchestrator.analyze()...")
    try:
        from services.orchestrator import Orchestrator
        print("✅ Orchestrator imported")
        
        orch = Orchestrator()
        print("✅ Orchestrator instance created")
        
        result = await orch.analyze("Iran ceasefire Trump")
        print("✅ Analysis completed successfully!")
        print(f"   Risk Level: {result.get('riskLevel')}")
        print(f"   Posts: {len(result.get('posts', []))}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())
