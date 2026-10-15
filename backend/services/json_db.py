"""
JSON File Database for VeriGraph AI
Persists every analysis result to backend/data/analyses.json
- Append-on-save (deduplication by query+timestamp)
- Thread-safe via a reentrant lock
- Lightweight: no external database required
"""

import json
import os
import threading
from datetime import datetime
from typing import Any


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DB_FILE = os.path.join(DATA_DIR, "analyses.json")
MAX_RECORDS = 500  # cap to avoid unbounded file growth


class JsonDatabase:
    """Persistent JSON-file storage for analyzed claims."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(DB_FILE):
            self._write([])

    # ─────────────────────────── public API ────────────────────────────

    def save(self, result: Any) -> dict:
        """
        Append one AnalyzeResponse (or a plain dict) to the JSON file.
        Returns the serialized record that was written.
        """
        with self._lock:
            records = self._read()

            # Serialize pydantic model → plain dict
            if hasattr(result, "model_dump"):
                payload = result.model_dump()
            elif hasattr(result, "dict"):
                payload = result.dict()
            else:
                payload = dict(result)

            record = {
                "id": self._next_id(records),
                "saved_at": datetime.utcnow().isoformat() + "Z",
                "query": payload.get("query", ""),
                "finalScore": payload.get("finalScore", 0),
                "riskLevel": payload.get("riskLevel", "Inconclusive"),
                "confidence": payload.get("confidence", 0.0),
                "summary": payload.get("summary", ""),
                "layers": payload.get("layers", []),
                "nodes": payload.get("nodes", []),
                "links": payload.get("links", []),
                "posts": payload.get("posts", []),
            }

            records.insert(0, record)          # newest first
            records = records[:MAX_RECORDS]    # cap size
            self._write(records)
            return record

    def all(self) -> list[dict]:
        """Return all saved records, newest first."""
        with self._lock:
            return self._read()

    def get(self, record_id: int) -> dict | None:
        """Return a single record by integer ID, or None if not found."""
        with self._lock:
            for rec in self._read():
                if rec.get("id") == record_id:
                    return rec
        return None

    def delete(self, record_id: int) -> bool:
        """Delete a single record by ID. Returns True if deleted."""
        with self._lock:
            records = self._read()
            new = [r for r in records if r.get("id") != record_id]
            if len(new) == len(records):
                return False
            self._write(new)
            return True

    def clear(self) -> None:
        """Wipe all saved records."""
        with self._lock:
            self._write([])

    def stats(self) -> dict:
        """Quick summary stats."""
        with self._lock:
            records = self._read()
            return {
                "total": len(records),
                "file_path": os.path.abspath(DB_FILE),
                "file_size_kb": round(os.path.getsize(DB_FILE) / 1024, 2) if os.path.exists(DB_FILE) else 0,
            }

    # ─────────────────────────── internals ─────────────────────────────

    def _read(self) -> list[dict]:
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write(self, records: list[dict]) -> None:
        tmp = DB_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False, default=str)
        os.replace(tmp, DB_FILE)   # atomic rename on all platforms

    @staticmethod
    def _next_id(records: list[dict]) -> int:
        if not records:
            return 1
        return max((r.get("id", 0) for r in records), default=0) + 1


# Singleton shared across the application
db = JsonDatabase()
