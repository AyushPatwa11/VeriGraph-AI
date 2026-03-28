from services.fusion_engine import FusionEngine
from services.gnn_analyzer import GNNAnalyzer
from services.nlp_analyzer import NLPAnalyzer


def test_nlp_reports_insufficient_evidence_for_short_input() -> None:
    analyzer = NLPAnalyzer()
    result = analyzer.analyze("calm update", [])

    assert result["name"] == "NLP"
    assert result["status"] == "insufficient_evidence"
    assert "Insufficient language evidence" in result["explanation"]
    assert result["evidence"]["tokenCount"] < 8


def test_gnn_reports_sparse_network_details() -> None:
    analyzer = GNNAnalyzer()
    result = analyzer.analyze([], [], {})

    assert result["name"] == "GNN"
    assert result["status"] == "insufficient_evidence"
    assert "Insufficient network evidence" in result["explanation"]
    assert result["evidence"]["nodeCount"] == 0
    assert result["evidence"]["linkCount"] == 0


def test_fusion_marks_inconclusive_with_sparse_inputs() -> None:
    fusion = FusionEngine()

    response = fusion.fuse(
        query="US announced Iran wants to negotiate ceasefire",
        nlp_result={
            "name": "NLP",
            "score": 6,
            "status": "insufficient_evidence",
            "confidence": 0.3,
            "evidence": {"tokenCount": 7},
            "explanation": "Insufficient language evidence.",
        },
        gnn_result={
            "name": "GNN",
            "score": 0,
            "status": "insufficient_evidence",
            "confidence": 0.1,
            "evidence": {"nodeCount": 0, "linkCount": 0},
            "explanation": "Insufficient network evidence.",
        },
        gemini_result={
            "name": "Gemini",
            "score": 0,
            "status": "unavailable",
            "confidence": None,
            "evidence": {"httpStatus": 429},
            "errorCode": "GEMINI_UPSTREAM_HTTP_ERROR",
            "explanation": "Gemini unavailable.",
        },
        nodes=[],
        links=[],
        posts=[],
    )

    assert response.riskLevel == "Inconclusive"
    assert response.resultStatus == "inconclusive"
    assert "inconclusive" in response.summary.lower()
    assert response.confidence <= 0.2


def test_fusion_returns_final_when_multi_layer_evidence_exists() -> None:
    fusion = FusionEngine()

    response = fusion.fuse(
        query="Coordinated accounts push false update",
        nlp_result={
            "name": "NLP",
            "score": 74,
            "status": "available",
            "confidence": 0.82,
            "evidence": {"urgencyHits": 5},
            "explanation": "Strong manipulation pressure.",
        },
        gnn_result={
            "name": "GNN",
            "score": 68,
            "status": "available",
            "confidence": 0.76,
            "evidence": {"nodeCount": 6, "linkCount": 10},
            "explanation": "Moderate-to-strong coordination.",
        },
        gemini_result={
            "name": "Gemini",
            "score": 86,
            "status": "available",
            "confidence": 0.88,
            "evidence": {"verdict": "FALSE"},
            "explanation": "Claim contradicted by verified reports.",
        },
        nodes=[
            {"id": "a1", "label": "@a", "followers": 10, "cluster": 1},
            {"id": "a2", "label": "@b", "followers": 12, "cluster": 1},
            {"id": "a3", "label": "@c", "followers": 9, "cluster": 2},
        ],
        links=[
            {"source": "a1", "target": "a2", "kind": "semantic"},
            {"source": "a1", "target": "a3", "kind": "temporal"},
        ],
        posts=[
            {"id": "p1", "username": "@a", "timestamp": "now", "text": "x", "likes": 1, "shares": 1},
            {"id": "p2", "username": "@b", "timestamp": "now", "text": "y", "likes": 1, "shares": 1},
            {"id": "p3", "username": "@c", "timestamp": "now", "text": "z", "likes": 1, "shares": 1},
        ],
    )

    assert response.resultStatus == "final"
    assert response.riskLevel in {"Medium", "High"}
    assert response.confidence >= 0.65


def test_confidence_capped_when_zero_posts() -> None:
    """Verify confidence is hard-capped to 0.15 when no posts collected."""
    fusion = FusionEngine()

    response = fusion.fuse(
        query="Test claim",
        nlp_result={
            "name": "NLP",
            "score": 50,
            "status": "available",
            "confidence": 0.9,  # High individual confidence
            "evidence": {},
            "explanation": "Test",
        },
        gnn_result={
            "name": "GNN",
            "score": 50,
            "status": "available",
            "confidence": 0.9,  # High individual confidence
            "evidence": {},
            "explanation": "Test",
        },
        gemini_result={
            "name": "Gemini",
            "score": 50,
            "status": "available",
            "confidence": 0.9,  # High individual confidence
            "evidence": {},
            "explanation": "Test",
        },
        nodes=[],
        links=[],
        posts=[],  # Zero posts
    )

    assert response.confidence <= 0.15, "Confidence should be capped at 0.15 when zero posts"
    assert response.riskLevel == "Inconclusive"


def test_confidence_capped_when_inconclusive() -> None:
    """Verify confidence is hard-capped to 0.25 for inconclusive results."""
    fusion = FusionEngine()

    response = fusion.fuse(
        query="Test claim",
        nlp_result={
            "name": "NLP",
            "score": 50,
            "status": "available",
            "confidence": 0.9,  # High individual confidence
            "evidence": {},
            "explanation": "Test",
        },
        gnn_result={
            "name": "GNN",
            "score": 0,
            "status": "insufficient_evidence",
            "confidence": 0.1,
            "evidence": {},
            "explanation": "Test",
        },
        gemini_result={
            "name": "Gemini",
            "score": 0,
            "status": "unavailable",
            "confidence": None,
            "evidence": {},
            "explanation": "Test",
        },
        nodes=[],  # Sparse network
        links=[],
        posts=[{
            "id": "p1",
            "username": "@a",
            "timestamp": "now",
            "text": "test",
            "likes": 0,
            "shares": 0
        }],  # Only 1 post
    )

    assert response.confidence <= 0.25, "Confidence should be capped at 0.25 for inconclusive"
    assert response.riskLevel == "Inconclusive"