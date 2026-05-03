"""
Minimal CacheManager stub for local development.
Provides in-memory caching to satisfy backend imports.
"""
from typing import Any, Dict
import threading


class CacheManager:
    def __init__(self):
        self._lock = threading.Lock()
        self._store: Dict[str, Any] = {}
        self._hits = 0
        self._misses = 0

    def get(self, key: str):
        with self._lock:
            val = self._store.get(key)
            if val is None:
                self._misses += 1
            else:
                self._hits += 1
            return val

    def set(self, key: str, value: Any):
        with self._lock:
            self._store[key] = value

    def clear(self):
        with self._lock:
            self._store.clear()
            self._hits = 0
            self._misses = 0

    def get_stats(self):
        with self._lock:
            return {
                "size": len(self._store),
                "hits": self._hits,
                "misses": self._misses,
            }
