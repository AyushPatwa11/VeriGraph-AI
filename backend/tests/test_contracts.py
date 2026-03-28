from schemas.contracts import AnalyzeResponse


def test_response_contract_minimal() -> None:
    payload = AnalyzeResponse(
        query="sample claim",
        finalScore=55,
        riskLevel="Medium",
        summary="test",
        layers=[
            {"name": "NLP", "score": 50, "explanation": "a"},
            {"name": "GNN", "score": 60, "explanation": "b"},
            {"name": "Gemini", "score": 55, "explanation": "c"},
        ],
        nodes=[{"id": "a1", "label": "@x", "followers": 1, "cluster": 1}],
        links=[{"source": "a1", "target": "a1", "kind": "semantic"}],
        posts=[
            {
                "id": "p1",
                "username": "@x",
                "timestamp": "now",
                "text": "hello",
                "likes": 0,
                "shares": 0,
            }
        ],
    )
    assert payload.finalScore == 55
