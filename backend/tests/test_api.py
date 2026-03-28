"""
Integration tests for Flask API
"""

import pytest
import json
from app import app, cache_manager, metrics_collector


@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def cleanup():
    """Cleanup before each test"""
    cache_manager.clear()
    metrics_collector.reset()
    yield


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_check(self, client):
        """Test /health endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data
    
    def test_status_endpoint(self, client):
        """Test /status endpoint"""
        response = client.get("/status")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["service_status"] == "running"
        assert "metrics" in data


class TestVerificationEndpoints:
    """Test claim verification endpoints"""
    
    def test_verify_basic(self, client):
        """Test basic verification request"""
        payload = {
            "query": "The Earth is round",
            "use_cache": False
        }
        
        response = client.post(
            "/api/verify",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "request_id" in data
        assert "verdict_score" in data
        assert "confidence" in data
    
    def test_verify_with_sources(self, client):
        """Test verification with sources"""
        payload = {
            "query": "COVID-19 is a virus",
            "sources": ["wikipedia.org", "cdc.gov"],
            "use_cache": False
        }
        
        response = client.post(
            "/api/verify",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "sources" in data
    
    def test_verify_empty_query(self, client):
        """Test verification with empty query"""
        payload = {
            "query": "",
            "use_cache": False
        }
        
        response = client.post(
            "/api/verify",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_verify_missing_query(self, client):
        """Test verification with missing query field"""
        payload = {
            "use_cache": False
        }
        
        response = client.post(
            "/api/verify",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 400
    
    def test_verify_invalid_json(self, client):
        """Test verification with invalid JSON"""
        response = client.post(
            "/api/verify",
            data="not json",
            content_type="application/json"
        )
        
        assert response.status_code == 400
    
    def test_verify_caching(self, client):
        """Test that caching works for repeated queries"""
        payload = {
            "query": "The Earth is round",
            "use_cache": True
        }
        
        # First request
        response1 = client.post(
            "/api/verify",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response1.status_code == 200
        data1 = json.loads(response1.data)
        assert data1["cached"] == False
        
        # Second request should be cached
        response2 = client.post(
            "/api/verify",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response2.status_code == 200
        data2 = json.loads(response2.data)
        assert data2["cached"] == True
        
        # Results should be identical
        assert data1["verdict_score"] == data2["verdict_score"]


class TestBatchVerificationEndpoints:
    """Test batch verification endpoints"""
    
    def test_batch_verify_basic(self, client):
        """Test basic batch verification"""
        payload = {
            "queries": ["Claim 1", "Claim 2", "Claim 3"],
            "use_cache": False
        }
        
        response = client.post(
            "/api/batch-verify",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "batch_id" in data
        assert "results" in data
        assert len(data["results"]) == 3
    
    def test_batch_verify_empty(self, client):
        """Test batch verification with empty queries"""
        payload = {
            "queries": [],
            "use_cache": False
        }
        
        response = client.post(
            "/api/batch-verify",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 400
    
    def test_batch_verify_invalid(self, client):
        """Test batch verification with invalid queries format"""
        payload = {
            "queries": "not a list",  # Should be list
            "use_cache": False
        }
        
        response = client.post(
            "/api/batch-verify",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 400


class TestCacheManagementEndpoints:
    """Test cache management endpoints"""
    
    def test_cache_status(self, client):
        """Test cache status endpoint"""
        response = client.get("/api/cache/status")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "size" in data
    
    def test_cache_clear(self, client):
        """Test cache clear endpoint"""
        # Add something to cache first
        payload = {
            "query": "Test claim",
            "use_cache": True
        }
        client.post(
            "/api/verify",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        # Clear cache
        response = client.post("/api/cache/clear")
        assert response.status_code == 200
        
        # Verify cache is empty
        status_response = client.get("/api/cache/status")
        data = json.loads(status_response.data)
        assert data["size"] == 0


class TestMetricsEndpoints:
    """Test metrics endpoints"""
    
    def test_metrics_report(self, client):
        """Test metrics report endpoint"""
        # Do some requests first
        payload = {"query": "Test claim", "use_cache": False}
        client.post(
            "/api/verify",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        # Get metrics
        response = client.get("/api/metrics")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert "system" in data
        assert "performance" in data
        assert "accuracy" in data
    
    def test_metrics_reset(self, client):
        """Test metrics reset endpoint"""
        # Do some requests
        payload = {"query": "Test claim", "use_cache": False}
        client.post(
            "/api/verify",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        # Reset
        response = client.post("/api/metrics/reset")
        assert response.status_code == 200
        
        # Verify reset
        metrics_response = client.get("/api/metrics")
        data = json.loads(metrics_response.data)
        assert data["system"]["total_requests"] == 0
    
    def test_add_groundtruth(self, client):
        """Test adding ground truth data"""
        payload = {
            "query": "The Earth is round",
            "verdict": "true"
        }
        
        response = client.post(
            "/api/metrics/groundtruth",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "message" in data
    
    def test_add_invalid_groundtruth(self, client):
        """Test adding invalid ground truth"""
        payload = {
            "query": "Claim",
            "verdict": "invalid"
        }
        
        response = client.post(
            "/api/metrics/groundtruth",
            data=json.dumps(payload),
            content_type="application/json"
        )
        
        assert response.status_code == 400


class TestErrorHandling:
    """Test error handling"""
    
    def test_not_found_endpoint(self, client):
        """Test 404 error"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
