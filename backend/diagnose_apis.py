"""Diagnostic script to test all API connectivity and data collection"""
import asyncio
from core.settings import settings
from adapters.news_rss_adapter import NewsRSSAdapter
from adapters.gdelt_client import GDELTClient
from adapters.telegram_client import TelegramClient
from services.fact_checker import FactChecker

async def diagnose():
    print('='*70)
    print('DIAGNOSTIC TEST: API Connectivity and Data Collection')
    print('='*70)
    
    # Test 1: News RSS
    print('\n[1] NEWS RSS ADAPTER TEST')
    print('-' * 70)
    try:
        news = NewsRSSAdapter()
        query = 'Iran Trump negotiations ceasefire'
        print(f'Query: {query}')
        
        # Test keyword extraction
        keywords = news._extract_keywords(query)
        print(f'Extracted keywords: {keywords}')
        
        posts = await news.search(query)
        print(f'Posts collected: {len(posts)}')
        if posts:
            print('Sample post:')
            for key, val in list(posts[0].items())[:3]:
                if key != '_timestamp_obj':
                    print(f'  {key}: {val}')
        else:
            print('⚠️ No posts returned - checking RSS feed connectivity')
    except Exception as e:
        exc_type = type(e).__name__
        print(f'❌ ERROR ({exc_type}): {str(e)[:300]}')
    
    # Test 2: GDELT API
    print('\n[2] GDELT API TEST')
    print('-' * 70)
    try:
        gdelt = GDELTClient()
        query = 'Iran Trump negotiations ceasefire'
        print(f'Query: {query}')
        
        # Test keyword extraction
        keywords = gdelt._extract_keywords(query)
        print(f'Extracted keywords: {keywords}')
        
        posts = await gdelt.search(query)
        print(f'Posts collected: {len(posts)}')
        if posts:
            print('Sample post:')
            for key, val in list(posts[0].items())[:3]:
                print(f'  {key}: {val}')
        else:
            print('⚠️ No posts returned - may be network issue or no matching events')
    except Exception as e:
        exc_type = type(e).__name__
        print(f'❌ ERROR ({exc_type}): {str(e)[:300]}')
    
    # Test 3: Telegram  
    print('\n[3] TELEGRAM API TEST')
    print('-' * 70)
    try:
        telegram = TelegramClient()
        query = 'Iran Trump negotiations ceasefire'
        print(f'Query: {query}')
        print(f'Bot token loaded: {bool(settings.telegram_bot_token)}')
        print(f'Channels: {settings.telegram_channels}')
        
        # Test keyword extraction
        keywords = telegram._extract_keywords(query)
        print(f'Extracted keywords: {keywords}')
        
        posts = await telegram.search(query)
        print(f'Posts collected: {len(posts)}')
        if posts:
            print('Sample post:')
            for key, val in list(posts[0].items())[:3]:
                print(f'  {key}: {val}')
        else:
            print('⚠️ No posts returned - may be no matching messages in channels')
    except Exception as e:
        exc_type = type(e).__name__
        print(f'❌ ERROR ({exc_type}): {str(e)[:300]}')
    
    # Test 4: Gemini API
    print('\n[4] GEMINI API TEST')
    print('-' * 70)
    try:
        print(f'Gemini API key loaded: {bool(settings.gemini_api_key)}')
        print(f'Gemini model: {settings.gemini_model}')
        checker = FactChecker()
        result = await checker.analyze('Iran says no negotiations with US')
        status = result.get('status')
        error_code = result.get('errorCode')
        explanation = result.get('explanation')
        evidence = result.get('evidence')
        print(f'Status: {status}')
        print(f'Error Code: {error_code}')
        if status == 'available':
            print('✅ GEMINI API WORKING')
        else:
            print(f'⚠️ GEMINI API UNAVAILABLE')
        print(f'Explanation: {explanation[:150]}...')
        if evidence:
            print(f'Evidence: {evidence}')
    except Exception as e:
        exc_type = type(e).__name__
        print(f'❌ ERROR ({exc_type}): {str(e)[:300]}')

if __name__ == '__main__':
    asyncio.run(diagnose())
