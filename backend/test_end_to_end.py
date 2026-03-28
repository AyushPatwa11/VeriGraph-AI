import asyncio
import httpx

async def test():
    payload = {'query': 'No negotiations have taken place with US says Iran ceasefire'}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post('http://localhost:8000/api/analyze', json=payload, timeout=45)
            print(f'Status: {response.status_code}')
            data = response.json()
            riskLevel = data.get('riskLevel')
            finalScore = data.get('finalScore')
            resultStatus = data.get('resultStatus')
            confidence = data.get('confidence')
            posts = len(data.get('posts', []))
            nodes = len(data.get('nodes', []))
            links = len(data.get('links', []))
            summary = data.get('summary', '')[:300]
            
            print(f'\n✅ Response received successfully\n')
            print(f'Risk Level: {riskLevel}')
            print(f'Final Score: {finalScore}')
            print(f'Result Status: {resultStatus}')
            print(f'Confidence: {confidence}')
            print(f'Posts Collected: {posts}')
            print(f'Nodes Found: {nodes}')
            print(f'Links Found: {links}')
            print(f'Summary: {summary}...')
            
            # Show layer details
            print(f'\n--- Layer Details ---')
            for layer in data.get('layers', []):
                print(f'{layer.get("name")}: score={layer.get("score")}, status={layer.get("status")}, confidence={layer.get("confidence")}')
        except Exception as e:
            print(f'Error: {e}')

asyncio.run(test())
