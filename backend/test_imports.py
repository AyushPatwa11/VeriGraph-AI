"""Test imports to find the error"""
import sys
import traceback

print("Testing imports...")

try:
    print("1. Importing adapters...")
    from adapters.news_rss_adapter import NewsRSSAdapter
    print("   ✅ NewsRSSAdapter imported")
    from adapters.gdelt_client import GDELTClient
    print("   ✅ GDELTClient imported")
    from adapters.telegram_client import TelegramClient
    print("   ✅ TelegramClient imported")
except Exception as e:
    print(f"   ❌ Error importing adapters: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("2. Importing services...")
    from services.scraper import ScraperService
    print("   ✅ ScraperService imported")
    from services.orchestrator import Orchestrator
    print("   ✅ Orchestrator imported")
except Exception as e:
    print(f"   ❌ Error importing services: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("3. Importing main app...")
    from main import app
    print("   ✅ main.app imported")
except Exception as e:
    print(f"   ❌ Error importing main: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n✅ All imports successful!")
