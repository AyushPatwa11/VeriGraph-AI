"""
Minimal VerificationEngine stub for local development and testing.
This provides a lightweight, deterministic response so the Flask app can start.
"""
from typing import List, Dict
import time


class VerificationEngine:
    def __init__(self):
        # placeholder for real model initializations
        pass

    def verify(self, query: str, sources: List[str] = None) -> Dict:
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        start = time.time()
        q = query.lower()
        # naive scoring heuristics for stub
        if any(k in q for k in ["earth is round", "2+2=4", "water boils"]):
            score = 95
            confidence = 0.95
            analysis = "Highly likely true (stub)"
        elif "flat" in q or "conspiracy" in q:
            score = 10
            confidence = 0.6
            analysis = "Likely false (stub)"
        else:
            score = 50
            confidence = 0.5
            analysis = "Inconclusive (stub)"

        return {
            "verdict_score": int(score),
            "confidence": float(confidence),
            "analysis": analysis,
            "sources": sources or [],
            "inference_time": int((time.time() - start) * 1000),
        }

    def decompose_claim(self, claim: str) -> List[str]:
        if not claim:
            return []
        # simple split on conjunctions for stub
        parts = [p.strip() for p in claim.replace(" and ", ";").split(";") if p.strip()]
        return parts

    def _combine_scores(self, scores: List[float]) -> float:
        if not scores:
            return 50.0
        return max(0.0, min(100.0, sum(scores) / len(scores)))

    def _calculate_confidence(self, scores: List[float]) -> float:
        if not scores:
            return 0.5
        mean = sum(scores) / len(scores)
        var = sum((s - mean) ** 2 for s in scores) / len(scores)
        # higher variance -> lower confidence
        conf = max(0.0, min(1.0, 1.0 - (var / 1000.0)))
        return conf
