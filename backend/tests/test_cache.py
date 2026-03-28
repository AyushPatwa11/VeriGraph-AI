"""
Unit tests for Cache Manager
"""

import pytest
from services.cache import CacheManager


@pytest.fixture
def cache():
    """Create a cache manager instance for testing"""
    manager = CacheManager()
    yield manager
    manager.clear()  # Cleanup after each test


class TestCacheManager:
    """Test cases for CacheManager"""
    
    def test_cache_set_get(self, cache):
        """Test basic set and get operations"""
        key = "test_query"
        value = {
            "verdict_score": 45,
            "confidence": 0.85,
            "analysis": "Test analysis"
        }
        
        cache.set(key, value)
        result = cache.get(key)
        
        assert result is not None
        assert result["verdict_score"] == 45
    
    def test_cache_miss(self, cache):
        """Test cache miss returns None"""
        result = cache.get("nonexistent_key")
        assert result is None
    
    def test_cache_update(self, cache):
        """Test updating cached value"""
        key = "test_query"
        value1 = {"score": 50}
        value2 = {"score": 60}
        
        cache.set(key, value1)
        assert cache.get(key)["score"] == 50
        
        cache.set(key, value2)
        assert cache.get(key)["score"] == 60
    
    def test_cache_delete(self, cache):
        """Test deleting from cache"""
        key = "test_query"
        cache.set(key, {"score": 50})
        assert cache.get(key) is not None
        
        cache.delete(key)
        assert cache.get(key) is None
    
    def test_cache_clear(self, cache):
        """Test clearing entire cache"""
        cache.set("key1", {"score": 50})
        cache.set("key2", {"score": 60})
        
        assert cache.size() > 0
        cache.clear()
        assert cache.size() == 0
    
    def test_cache_size(self, cache):
        """Test cache size tracking"""
        cache.set("key1", {"score": 50})
        assert cache.size() == 1
        
        cache.set("key2", {"score": 60})
        assert cache.size() == 2
        
        cache.delete("key1")
        assert cache.size() == 1
    
    def test_cache_stats(self, cache):
        """Test cache statistics"""
        # Initially empty
        stats = cache.get_stats()
        assert stats["size"] == 0
        
        # Add items
        cache.set("key1", {"score": 50})
        cache.set("key2", {"score": 60})
        
        # Retrieve once
        cache.get("key1")  # miss
        cache.get("key1")  # hit
        
        stats = cache.get_stats()
        assert stats["size"] == 2
        assert "hits" in stats
        assert "misses" in stats
    
    def test_cache_max_size(self, cache):
        """Test cache respects max size limit"""
        cache.max_size = 3
        
        cache.set("key1", {"score": 1})
        cache.set("key2", {"score": 2})
        cache.set("key3", {"score": 3})
        assert cache.size() == 3
        
        # Adding 4th item should evict oldest
        cache.set("key4", {"score": 4})
        assert cache.size() <= 3
    
    def test_cache_ttl_expiry(self, cache):
        """Test TTL-based cache expiration"""
        import time
        
        cache.ttl = 1  # 1 second TTL
        cache.set("key1", {"score": 50})
        
        # Should be available immediately
        assert cache.get("key1") is not None
        
        # After expiry
        time.sleep(1.1)
        assert cache.get("key1") is None


class TestCachePerformance:
    """Test cache performance characteristics"""
    
    def test_cache_hit_rate(self, cache):
        """Test hit rate calculation"""
        cache.set("key1", {"score": 50})
        
        # 10 gets: 1 miss, 9 hits
        cache.get("key1")
        for _ in range(9):
            cache.get("key1")
        
        stats = cache.get_stats()
        assert stats["hits"] == 9
        assert stats["misses"] == 0
    
    def test_cache_performance_metadata(self, cache):
        """Test cache metadata tracking"""
        cache.set("key1", {"score": 50})
        cache.set("key2", {"score": 60})
        
        # Populate some stats
        cache.get("key1")
        cache.get("key1")
        cache.get("missing")
        
        stats = cache.get_stats()
        
        assert "size" in stats
        assert "hits" in stats
        assert "misses" in stats
        assert "hit_rate" in stats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
