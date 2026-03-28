"""
In-Memory Cache Manager for claim analyses
- 7-day TTL
- SHA256 keying
- Hit/miss tracking
"""

import hashlib
import json
from typing import Dict, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class CacheEntry:
    """Single cache entry"""
    data: Dict
    created_at: datetime
    ttl_seconds: int = 604800  # 7 days
    
    def is_expired(self) -> bool:
        """Check if entry has expired"""
        expiry = self.created_at + timedelta(seconds=self.ttl_seconds)
        return datetime.now() > expiry


class CacheManager:
    """
    In-memory cache for claim analyses
    
    Features:
    - SHA256 keying (case-insensitive)
    - 7-day TTL
    - Hit/miss metrics
    - Automatic cleanup on access
    """
    
    DEFAULT_TTL = 604800  # 7 days in seconds

    def __init__(self, default_ttl_seconds: int = DEFAULT_TTL):
        self.cache: Dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl_seconds
        self.metrics = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "items_expired": 0,
        }

    def get(self, claim: str) -> Optional[Dict]:
        """Get cached analysis for claim"""
        self.metrics["total_requests"] += 1
        key = self._make_key(claim)
        
        if key not in self.cache:
            self.metrics["cache_misses"] += 1
            return None
        
        entry = self.cache[key]
        
        # Check expiry
        if entry.is_expired():
            del self.cache[key]
            self.metrics["items_expired"] += 1
            self.metrics["cache_misses"] += 1
            return None
        
        # Cache hit
        self.metrics["cache_hits"] += 1
        return entry.data

    def set(self, claim: str, result: Dict, ttl_seconds: Optional[int] = None):
        """Cache an analysis result"""
        key = self._make_key(claim)
        ttl = ttl_seconds or self.default_ttl
        self.cache[key] = CacheEntry(result, datetime.now(), ttl)

    def get_metrics(self) -> Dict:
        """Get cache performance metrics"""
        hit_ratio = (
            self.metrics["cache_hits"] / max(self.metrics["total_requests"], 1)
        )
        
        # Estimate cache size
        cache_size_bytes = sum(
            len(json.dumps(entry.data))
            for entry in self.cache.values()
        )
        cache_size_kb = cache_size_bytes / 1024
        
        return {
            "total_requests": self.metrics["total_requests"],
            "cache_hits": self.metrics["cache_hits"],
            "cache_misses": self.metrics["cache_misses"],
            "hit_ratio": round(hit_ratio, 3),
            "items_in_cache": len(self.cache),
            "items_expired": self.metrics["items_expired"],
            "cache_size_kb": round(cache_size_kb, 2),
        }

    def clear(self):
        """Clear all cache entries"""
        self.cache.clear()

    def reset_metrics(self):
        """Reset metrics (keep cached data)"""
        self.metrics = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "items_expired": 0,
        }

    @staticmethod
    def _make_key(claim: str) -> str:
        """Generate cache key from claim"""
        normalized = claim.lower().strip()
        hash_obj = hashlib.sha256(normalized.encode())
        return hash_obj.hexdigest()
