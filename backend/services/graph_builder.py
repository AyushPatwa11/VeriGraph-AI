from collections import defaultdict
from datetime import datetime
import math
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class GraphBuilder:
    def build(self, posts: list[dict]) -> tuple[list[dict], list[dict], dict]:
        if not posts:
            return [], [], {"coordinationDensity": 0.0, "clusterCount": 0}

        grouped: dict[str, list[dict]] = defaultdict(list)
        for post in posts:
            grouped[post.get("username", "@unknown")].append(post)

        nodes = []
        username_to_id: dict[str, str] = {}
        for index, (username, account_posts) in enumerate(grouped.items(), start=1):
            node_id = f"a{index}"
            username_to_id[username] = node_id
            followers = max([int(item.get("followers", 0)) for item in account_posts] + [0])
            nodes.append(
                {
                    "id": node_id,
                    "label": username,
                    "followers": followers,
                    "cluster": (index % 3) + 1,
                }
            )

        links = []
        links.extend(self._semantic_links(grouped, username_to_id))
        links.extend(self._url_links(grouped, username_to_id))
        links.extend(self._temporal_links(grouped, username_to_id))

        unique_links = self._unique_links(links)
        max_possible = max(len(nodes) * (len(nodes) - 1) / 2, 1)
        density = min(len(unique_links) / max_possible, 1.0)

        metrics = {
            "coordinationDensity": float(round(density, 3)),
            "clusterCount": len({node["cluster"] for node in nodes}),
        }
        return nodes, unique_links, metrics

    def _semantic_links(self, grouped: dict[str, list[dict]], username_to_id: dict[str, str]) -> list[dict]:
        usernames = list(grouped.keys())
        texts = [" ".join([item.get("text", "") for item in grouped[name]]) for name in usernames]
        if len(texts) < 2:
            return []

        vectorizer = TfidfVectorizer(stop_words="english")
        matrix = vectorizer.fit_transform(texts)
        similarity = cosine_similarity(matrix)

        links: list[dict] = []
        for i in range(len(usernames)):
            for j in range(i + 1, len(usernames)):
                if similarity[i][j] >= 0.35:
                    links.append(
                        {
                            "source": username_to_id[usernames[i]],
                            "target": username_to_id[usernames[j]],
                            "kind": "semantic",
                        }
                    )
        return links

    def _url_links(self, grouped: dict[str, list[dict]], username_to_id: dict[str, str]) -> list[dict]:
        user_urls: dict[str, set[str]] = {}
        for username, items in grouped.items():
            urls: set[str] = set()
            for item in items:
                for url in item.get("urls", []):
                    cleaned = url.strip().lower()
                    if cleaned:
                        urls.add(cleaned)
                text = item.get("text", "")
                for match in re.findall(r"https?://\S+", text):
                    urls.add(match.strip().lower())
            user_urls[username] = urls

        usernames = list(grouped.keys())
        links: list[dict] = []
        for i in range(len(usernames)):
            for j in range(i + 1, len(usernames)):
                shared = user_urls[usernames[i]].intersection(user_urls[usernames[j]])
                if shared:
                    links.append(
                        {
                            "source": username_to_id[usernames[i]],
                            "target": username_to_id[usernames[j]],
                            "kind": "url",
                        }
                    )
        return links

    def _temporal_links(self, grouped: dict[str, list[dict]], username_to_id: dict[str, str]) -> list[dict]:
        minute_values: dict[str, float] = {}
        for username, items in grouped.items():
            values: list[float] = []
            for item in items:
                values.append(self._parse_timestamp(item.get("timestamp", "")))
            minute_values[username] = float(np.mean(values)) if values else 9999.0

        usernames = list(grouped.keys())
        links: list[dict] = []
        for i in range(len(usernames)):
            for j in range(i + 1, len(usernames)):
                if math.fabs(minute_values[usernames[i]] - minute_values[usernames[j]]) <= 6:
                    links.append(
                        {
                            "source": username_to_id[usernames[i]],
                            "target": username_to_id[usernames[j]],
                            "kind": "temporal",
                        }
                    )
        return links

    def _parse_timestamp(self, value: str) -> float:
        value = (value or "").strip().lower()
        if not value:
            return 9999.0
        if value.endswith("m ago"):
            try:
                return float(value.replace("m ago", "").strip())
            except ValueError:
                return 9999.0
        if value.endswith("h ago"):
            try:
                return float(value.replace("h ago", "").strip()) * 60
            except ValueError:
                return 9999.0
        if value == "now":
            return 0.0
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            now = datetime.now(parsed.tzinfo)
            diff = now - parsed
            return max(diff.total_seconds() / 60, 0.0)
        except Exception:
            return 9999.0

    def _unique_links(self, links: list[dict]) -> list[dict]:
        seen: set[str] = set()
        unique: list[dict] = []
        for link in links:
            source = link.get("source", "")
            target = link.get("target", "")
            kind = link.get("kind", "semantic")
            ordered = "::".join(sorted([source, target]))
            key = f"{ordered}::{kind}"
            if source == target or key in seen:
                continue
            seen.add(key)
            unique.append(link)
        return unique
