"""
RoBERTa-powered NLP Analysis Service for Manipulation & Framing Detection
Uses RoBERTa NLI / zero-shot classification to detect persuasive pressure, manipulation, and framing.
"""

from typing import Any
import re
import torch
from transformers import pipeline


class NLPAnalyzer:
    """
    RoBERTa-powered NLP analysis for claims & social posts.
    Classifies text into manipulation levels (sensationalized, propaganda framing, neutral).
    """

    URGENCY_WORDS = {
        "urgent", "breaking", "must", "immediately", "hidden",
        "shocking", "deleted", "exclusive", "emergency", "exposed", "secret"
    }

    def __init__(self) -> None:
        """Initialize RoBERTa zero-shot model pipeline."""
        try:
            # RoBERTa NLI zero-shot classification model
            self.pipe = pipeline(
                "zero-shot-classification",
                model="roberta-large-mnli",
                device=0 if torch.cuda.is_available() else -1,
            )
            self.candidate_labels = [
                "sensational misinformation",
                "manipulative propaganda",
                "objective reporting",
                "neutral text"
            ]
            self.initialized = True
            print("INFO: RoBERTa model (roberta-large-mnli) initialized successfully.")
        except Exception as e:
            print(f"Warning: RoBERTa model initialization failed: {e}. Falling back to linguistic heuristics.")
            self.initialized = False

    def analyze(self, query: str, posts: list[dict]) -> dict[str, Any]:
        corpus = " ".join([query, *[post.get("text", "") for post in posts]])
        tokens = re.findall(r"[a-zA-Z']+", corpus.lower())
        total_tokens = max(len(tokens), 1)

        matched_urgency_terms = [token for token in tokens if token in self.URGENCY_WORDS]
        urgency_hits = len(matched_urgency_terms)
        exclamation_hits = corpus.count("!")
        uppercase_ratio = self._uppercase_ratio(corpus)

        # Base linguistic metrics
        urgency_score = min(urgency_hits / 18, 1.0)
        punctuation_score = min(exclamation_hits / 12, 1.0)
        style_score = min(uppercase_ratio * 2.5, 1.0)
        heuristic_score = (0.45 * urgency_score + 0.35 * punctuation_score + 0.20 * style_score) * 100

        roberta_confidence = 0.0
        roberta_label = "heuristic_fallback"
        final_score = int(round(heuristic_score))

        if self.initialized and len(query.strip()) >= 4:
            try:
                # Truncate text for RoBERTa input length safety
                sample_text = (query + " " + corpus)[:400]
                res = self.pipe(sample_text, self.candidate_labels)
                roberta_label = res["labels"][0]
                roberta_confidence = float(round(res["scores"][0], 2))

                # Map RoBERTa prediction to 0-100 manipulation score
                if roberta_label == "sensational misinformation":
                    ml_score = 88
                elif roberta_label == "manipulative propaganda":
                    ml_score = 78
                elif roberta_label == "objective reporting":
                    ml_score = 20
                else:
                    ml_score = 30

                # Hybrid fusion score (70% RoBERTa + 30% heuristic style analysis)
                final_score = int(round(0.70 * ml_score + 0.30 * heuristic_score))
            except Exception as e:
                print(f"RoBERTa analysis error: {e}")

        term_examples = self._ordered_unique(matched_urgency_terms)[:4]
        signal_volume = min(total_tokens / 60, 1.0)
        signal_strength = min((urgency_hits + exclamation_hits) / 10, 1.0)
        confidence = round(min(0.20 + (0.5 * roberta_confidence + 0.3 * signal_volume + 0.2 * signal_strength), 1.0), 2)

        evidence = {
            "model": "RoBERTa-Large-MNLI + Linguistic Features" if self.initialized else "Linguistic Heuristics",
            "topCategory": roberta_label,
            "robertaConfidence": roberta_confidence,
            "urgencyHits": urgency_hits,
            "urgencyTerms": term_examples,
            "exclamationHits": exclamation_hits,
            "uppercaseRatio": round(uppercase_ratio, 3),
            "tokenCount": total_tokens,
        }

        if total_tokens < 8:
            explanation = (
                "Insufficient language evidence for a strong manipulation verdict. "
                f"Observed {total_tokens} tokens with RoBERTa classification '{roberta_label}'."
            )
            status = "insufficient_evidence"
        elif final_score >= 70:
            explanation = (
                f"RoBERTa model detected strong manipulative pressure ('{roberta_label}', confidence: {roberta_confidence}). "
                f"Language features include urgency terms {term_examples or ['none']} and {exclamation_hits} exclamation mark(s)."
            )
            status = "available"
        elif final_score >= 40:
            explanation = (
                f"RoBERTa model detected moderate persuasive pressure ('{roberta_label}', confidence: {roberta_confidence}). "
                f"Detected urgency terms {term_examples or ['none']} and uppercase ratio {uppercase_ratio:.2f}."
            )
            status = "available"
        else:
            explanation = (
                f"RoBERTa model evaluated language as mostly objective ('{roberta_label}', confidence: {roberta_confidence}). "
                f"Presents low manipulation indicators."
            )
            status = "available"

        return {
            "name": "NLP",
            "score": final_score,
            "explanation": explanation,
            "status": status,
            "confidence": confidence,
            "evidence": evidence,
        }

    def _uppercase_ratio(self, text: str) -> float:
        letters = [char for char in text if char.isalpha()]
        if not letters:
            return 0.0
        uppercase = [char for char in letters if char.isupper()]
        return len(uppercase) / len(letters)

    def _ordered_unique(self, values: list[str]) -> list[str]:
        seen: set[str] = set()
        ordered: list[str] = []
        for value in values:
            if value in seen:
                continue
            seen.add(value)
            ordered.append(value)
        return ordered
