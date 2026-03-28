from schemas.contracts import AnalyzeResponse


class FusionEngine:
    def fuse(
        self,
        query: str,
        nlp_result: dict,
        gnn_result: dict,
        gemini_result: dict,
        nodes: list[dict],
        links: list[dict],
        posts: list[dict],
    ) -> AnalyzeResponse:
        layers = [nlp_result, gnn_result, gemini_result]
        available_layers = [layer for layer in layers if layer.get("status", "available") == "available"]
        scored_layers = [int(layer.get("score", 0)) for layer in available_layers]
        if not scored_layers:
            scored_layers = [int(nlp_result.get("score", 0)), int(gnn_result.get("score", 0))]

        final_score = int(round(sum(scored_layers) / max(len(scored_layers), 1)))
        inconclusive = self._is_inconclusive(layers, nodes, links, posts)

        if inconclusive:
            risk = "Inconclusive"
            result_status = "inconclusive"
        elif final_score >= 70:
            risk = "High"
            result_status = "final"
        elif final_score >= 40:
            risk = "Medium"
            result_status = "final"
        else:
            risk = "Low"
            result_status = "final"

        confidence = self._compute_confidence(layers, len(posts), len(nodes), len(links))
        summary = self._build_summary(
            risk=risk,
            result_status=result_status,
            confidence=confidence,
            nlp_result=nlp_result,
            gnn_result=gnn_result,
            gemini_result=gemini_result,
            node_count=len(nodes),
            edge_count=len(links),
        )

        return AnalyzeResponse(
            query=query,
            finalScore=final_score,
            riskLevel=risk,
            resultStatus=result_status,
            confidence=confidence,
            summary=summary,
            layers=layers,
            nodes=nodes,
            links=links,
            posts=posts,
        )

    def _build_summary(
        self,
        risk: str,
        result_status: str,
        confidence: float,
        nlp_result: dict,
        gnn_result: dict,
        gemini_result: dict,
        node_count: int,
        edge_count: int,
    ) -> str:
        fact_check_available = gemini_result.get("status", "available") == "available"
        fact_check_score = str(gemini_result.get("score", 0)) if fact_check_available else "unavailable"
        fact_check_name = gemini_result.get("name", "FactCheck")
        primary_driver = self._primary_driver(nlp_result, gnn_result, gemini_result)
        disagreement = abs(int(nlp_result.get("score", 0)) - int(gnn_result.get("score", 0))) >= 30

        if result_status == "inconclusive":
            return (
                "Result is inconclusive due to limited or inconsistent evidence across layers. "
                f"Current signals: NLP={nlp_result.get('score', 0)}, GNN={gnn_result.get('score', 0)}, {fact_check_name}={fact_check_score}; "
                f"network observed {node_count} accounts and {edge_count} coordination edges. "
                f"Confidence {int(round(confidence * 100))}% and additional data is recommended before a firm risk verdict."
            )

        disagreement_text = (
            " Layer disagreement is elevated, so treat this score with caution."
            if disagreement
            else " Layer agreement is reasonably consistent."
        )

        return (
            f"{risk} risk assessment driven primarily by {primary_driver}. "
            f"Signals: NLP={nlp_result.get('score', 0)}, GNN={gnn_result.get('score', 0)}, {fact_check_name}={fact_check_score}; "
            f"network observed {node_count} accounts and {edge_count} coordination edges. "
            f"Estimated confidence is {int(round(confidence * 100))}%."
            f"{disagreement_text}"
        )

    def _is_inconclusive(self, layers: list[dict], nodes: list[dict], links: list[dict], posts: list[dict]) -> bool:
        available_count = sum(1 for layer in layers if layer.get("status", "available") == "available")
        insufficient_count = sum(1 for layer in layers if layer.get("status") == "insufficient_evidence")
        if available_count < 2:
            return True
        if insufficient_count >= 2:
            return True
        if len(posts) < 2:
            return True
        if len(nodes) < 3 or len(links) < 1:
            return True
        return False

    def _compute_confidence(self, layers: list[dict], post_count: int, node_count: int, edge_count: int) -> float:
        available_layers = [layer for layer in layers if layer.get("status", "available") == "available"]
        if not available_layers:
            return 0.1

        layer_confidences = [
            float(layer.get("confidence", 0.45) if layer.get("confidence") is not None else 0.45)
            for layer in available_layers
        ]
        coverage = len(available_layers) / max(len(layers), 1)
        scores = [int(layer.get("score", 0)) for layer in available_layers]
        agreement = 1 - ((max(scores) - min(scores)) / 100 if len(scores) > 1 else 0.2)

        base_confidence = 0.55 * (sum(layer_confidences) / len(layer_confidences)) + 0.25 * coverage + 0.2 * max(0.0, agreement)
        computed_confidence = round(min(max(base_confidence, 0.05), 1.0), 2)
        
        # Hard confidence caps for sparse/inconclusive data
        if post_count == 0:
            # No posts collected - extremely low confidence
            return round(min(computed_confidence, 0.15), 2)
        
        # Check if result is inconclusive (determined by result_status, inferred here from data)
        inconclusive_indicators = (
            len([l for l in layers if l.get("status", "available") == "available"]) < 2 or
            post_count < 2 or
            node_count < 3 or
            edge_count < 1
        )
        if inconclusive_indicators:
            return round(min(computed_confidence, 0.25), 2)
        
        return computed_confidence

    def _primary_driver(self, nlp_result: dict, gnn_result: dict, gemini_result: dict) -> str:
        candidates = [
            ("language manipulation signals", int(nlp_result.get("score", 0))),
            ("network coordination patterns", int(gnn_result.get("score", 0))),
        ]
        if gemini_result.get("status", "available") == "available":
            candidates.append(("external fact-check contradiction", int(gemini_result.get("score", 0))))

        return max(candidates, key=lambda item: item[1])[0]
