class GNNAnalyzer:
    def analyze(self, nodes: list[dict], links: list[dict], metrics: dict) -> dict:
        node_count = len(nodes or [])
        link_count = len(links or [])

        if node_count == 0:
            return {
                "name": "GNN",
                "score": 0,
                "status": "insufficient_evidence",
                "confidence": 0.05,
                "evidence": {
                    "nodeCount": 0,
                    "linkCount": 0,
                    "coordinationDensity": 0.0,
                    "clusterCount": 0,
                    "linkKinds": {},
                },
                "explanation": "Insufficient network evidence: no accounts were collected, so coordination analysis cannot be established.",
            }

        density = self._to_float(metrics.get("coordinationDensity"), 0.0)
        cluster_count = self._to_int(metrics.get("clusterCount"), 1)
        edge_factor = min(link_count / max(node_count, 1), 1.0)
        kind_counts = self._kind_counts(links)
        top_node = self._highest_degree_node(nodes, links)

        confidence = round(
            min(
                0.1
                + (0.45 * min(node_count / 12, 1.0))
                + (0.35 * min(link_count / max(node_count, 1), 1.0))
                + (0.2 * min(density / 0.6, 1.0)),
                1.0,
            ),
            2,
        )

        evidence = {
            "nodeCount": node_count,
            "linkCount": link_count,
            "coordinationDensity": round(density, 3),
            "clusterCount": cluster_count,
            "linkKinds": kind_counts,
            "highestDegreeNode": top_node,
        }

        if node_count < 3 or link_count == 0:
            return {
                "name": "GNN",
                "score": 10,
                "status": "insufficient_evidence",
                "confidence": round(min(confidence, 0.35), 2),
                "evidence": evidence,
                "explanation": (
                    "Insufficient coordination evidence: the graph is too sparse for reliable attribution "
                    f"({node_count} accounts, {link_count} links, density {density:.2f})."
                ),
            }

        score = int(round((0.5 * density + 0.35 * edge_factor + 0.15 * min(cluster_count / 4, 1.0)) * 100))

        if score >= 70:
            explanation = (
                "Strong coordination pattern detected with dense coupling and repeated relational overlap. "
                f"Observed {node_count} accounts, {link_count} links, density {density:.2f}, "
                f"and dominant node {top_node or 'n/a'}."
            )
        elif score >= 40:
            explanation = (
                "Moderate coordination signals are present but not uniformly strong across the network. "
                f"Observed {node_count} accounts, {link_count} links, density {density:.2f}, "
                f"and dominant node {top_node or 'n/a'}."
            )
        else:
            explanation = (
                "Weak coordination structure detected with low edge convergence. "
                f"Observed {node_count} accounts, {link_count} links, density {density:.2f}, "
                f"and dominant node {top_node or 'n/a'}."
            )

        return {
            "name": "GNN",
            "score": score,
            "explanation": explanation,
            "status": "available",
            "confidence": confidence,
            "evidence": evidence,
        }

    def _to_float(self, value: object, fallback: float) -> float:
        try:
            if value is None:
                return fallback
            return float(value)
        except (TypeError, ValueError):
            return fallback

    def _to_int(self, value: object, fallback: int) -> int:
        try:
            if value is None:
                return fallback
            return int(value)
        except (TypeError, ValueError):
            return fallback

    def _kind_counts(self, links: list[dict]) -> dict[str, int]:
        counts: dict[str, int] = {"semantic": 0, "temporal": 0, "url": 0}
        for link in links or []:
            kind = str(link.get("kind", "semantic"))
            if kind in counts:
                counts[kind] += 1
        return counts

    def _highest_degree_node(self, nodes: list[dict], links: list[dict]) -> str | None:
        if not nodes:
            return None
        degree: dict[str, int] = {str(node.get("id", "")): 0 for node in nodes}
        for link in links or []:
            source = str(link.get("source", ""))
            target = str(link.get("target", ""))
            if source in degree:
                degree[source] += 1
            if target in degree:
                degree[target] += 1
        top_id = max(degree.items(), key=lambda item: item[1])[0]
        if not top_id:
            return None
        for node in nodes:
            if str(node.get("id", "")) == top_id:
                return str(node.get("label", top_id))
        return top_id
