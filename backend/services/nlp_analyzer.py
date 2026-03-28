import re


class NLPAnalyzer:
    URGENCY_WORDS = {
        "urgent",
        "breaking",
        "must",
        "immediately",
        "hidden",
        "shocking",
        "deleted",
        "exclusive",
        "emergency",
    }

    def analyze(self, query: str, posts: list[dict]) -> dict:
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

        score = int(round((0.45 * urgency_score + 0.35 * punctuation_score + 0.20 * style_score) * 100))
        term_examples = self._ordered_unique(matched_urgency_terms)[:4]

        signal_volume = min(total_tokens / 60, 1.0)
        signal_strength = min((urgency_hits + exclamation_hits) / 10, 1.0)
        confidence = round(min(0.15 + (0.6 * signal_volume + 0.25 * signal_strength + 0.15 * (1 - style_score)), 1.0), 2)

        evidence = {
            "urgencyHits": urgency_hits,
            "urgencyTerms": term_examples,
            "exclamationHits": exclamation_hits,
            "uppercaseRatio": round(uppercase_ratio, 3),
            "tokenCount": total_tokens,
            "urgencyScore": round(urgency_score, 3),
            "punctuationScore": round(punctuation_score, 3),
            "styleScore": round(style_score, 3),
        }

        if total_tokens < 8:
            explanation = (
                "Insufficient language evidence for a strong manipulation verdict. "
                f"Observed {total_tokens} tokens, {urgency_hits} urgency terms, and {exclamation_hits} exclamation marks."
            )
            status = "insufficient_evidence"
        elif score >= 70:
            explanation = (
                "Language shows strong manipulation pressure with concentrated urgency framing. "
                f"Detected urgency terms {term_examples or ['none']}, {exclamation_hits} exclamation marks, "
                f"and uppercase ratio {uppercase_ratio:.2f}."
            )
            status = "available"
        elif score >= 40:
            explanation = (
                "Language contains moderate persuasive pressure but not consistent high-intensity manipulation. "
                f"Detected urgency terms {term_examples or ['none']}, {exclamation_hits} exclamation marks, "
                f"and uppercase ratio {uppercase_ratio:.2f}."
            )
            status = "available"
        else:
            explanation = (
                "Language appears mostly neutral with limited manipulation indicators. "
                f"Detected urgency terms {term_examples or ['none']}, {exclamation_hits} exclamation marks, "
                f"and uppercase ratio {uppercase_ratio:.2f}."
            )
            status = "available"

        return {
            "name": "NLP",
            "score": score,
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
