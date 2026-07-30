"""
RoBERTa-powered / Memory-Safe NLP Analysis Service for Manipulation & Framing Detection
Optimized for ultra-low memory cloud hosting (Render 512MB RAM limit).
"""

from typing import Any
import re


class NLPAnalyzer:
    """
    NLP analysis for claims & social posts.
    Classifies text into manipulation levels with memory safeguards for 512MB cloud instances.
    """

    URGENCY_WORDS = {
        "urgent", "breaking", "must", "immediately", "hidden",
        "shocking", "deleted", "exclusive", "emergency", "exposed", "secret"
    }

    def __init__(self) -> None:
        self.candidate_labels = [
            "sensational misinformation",
            "manipulative propaganda",
            "objective reporting",
            "neutral text"
        ]
        self.pipe = None
        self.initialized = False
        self.attempted = False
        self.model_name = "Linguistic-NLP"

    def _ensure_model_loaded(self) -> None:
        if self.attempted:
            return
        self.attempted = True

        try:
            import torch
            from transformers import pipeline

            models_to_try = [
                "cross-encoder/nli-distilroberta-base",
                "typeform/distilbert-base-uncased-mnli",
            ]

            for model_name in models_to_try:
                try:
                    self.pipe = pipeline(
                        "zero-shot-classification",
                        model=model_name,
                        device=-1,  # Force CPU
                    )
                    self.model_name = model_name
                    self.initialized = True
                    print(f"INFO: NLPAnalyzer loaded lightweight model: {model_name}")
                    break
                except Exception as ex:
                    print(f"Notice: Could not load {model_name}: {ex}")
        except Exception as err:
            print(f"Notice: PyTorch/Transformers deferred load notice: {err}. Using linguistic analyzer.")

    def analyze(self, query: str, posts: list[dict]) -> dict[str, Any]:
        self._ensure_model_loaded()

        corpus = " ".join([query, *[post.get("text", "") for post in posts]])
        tokens = re.findall(r"[a-zA-Z']+", corpus.lower())
        total_tokens = max(len(tokens), 1)

        matched_urgency_terms = [token for token in tokens if token in self.URGENCY_WORDS]
        urgency_hits = len(matched_urgency_terms)
        exclamation_hits = corpus.count("!")
        uppercase_ratio = self._uppercase_ratio(corpus)

        urgency_score = min(urgency_hits / 18, 1.0)
        punctuation_score = min(exclamation_hits / 12, 1.0)
        style_score = min(uppercase_ratio * 2.5, 1.0)
        heuristic_score = (0.45 * urgency_score + 0.35 * punctuation_score + 0.20 * style_score) * 100

        roberta_confidence = 0.65
        roberta_label = "objective reporting"
        final_score = int(round(heuristic_score))

        if self.initialized and self.pipe and len(query.strip()) >= 4:
            try:
                sample_text = (query + " " + corpus)[:300]
                res = self.pipe(sample_text, self.candidate_labels)
                roberta_label = res["labels"][0]
                roberta_confidence = float(round(res["scores"][0], 2))

                if roberta_label == "sensational misinformation":
                    ml_score = 88
                elif roberta_label == "manipulative propaganda":
                    ml_score = 78
                elif roberta_label == "objective reporting":
                    ml_score = 20
                else:
                    ml_score = 30

                final_score = int(round(0.70 * ml_score + 0.30 * heuristic_score))
            except Exception as e:
                print(f"NLP model evaluation notice: {e}")
        else:
            if urgency_hits > 2 or exclamation_hits > 2:
                roberta_label = "sensational misinformation"
                final_score = max(final_score, 72)
            elif urgency_hits == 0 and uppercase_ratio < 0.15:
                roberta_label = "objective reporting"
                final_score = min(final_score, 25)

        term_examples = self._ordered_unique(matched_urgency_terms)[:4]
        signal_volume = min(total_tokens / 60, 1.0)
        signal_strength = min((urgency_hits + exclamation_hits) / 10, 1.0)
        confidence = round(min(0.20 + (0.5 * roberta_confidence + 0.3 * signal_volume + 0.2 * signal_strength), 1.0), 2)

        evidence = {
            "model": self.model_name if self.initialized else "Linguistic & Framing Analyzer (Cloud Optimized)",
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
                f"Observed {total_tokens} tokens with classification '{roberta_label}'."
            )
            status = "insufficient_evidence"
        elif final_score >= 70:
            explanation = (
                f"Language framing detected strong manipulative pressure ('{roberta_label}', confidence: {roberta_confidence}). "
                f"Urgency indicators: {term_examples or ['none']} with {exclamation_hits} exclamation mark(s)."
            )
            status = "available"
        elif final_score >= 40:
            explanation = (
                f"Language framing detected moderate persuasive pressure ('{roberta_label}', confidence: {roberta_confidence}). "
                f"Urgency indicators: {term_examples or ['none']}."
            )
            status = "available"
        else:
            explanation = (
                f"Language analysis evaluated text as mostly objective ('{roberta_label}', confidence: {roberta_confidence}). "
                f"Presents minimal manipulation framing."
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
