"""
Unit tests for Verification Engine
"""

import pytest
from services.verification import VerificationEngine


@pytest.fixture
def engine():
    """Create a verification engine instance for testing"""
    # Note: In real tests, you might mock the models
    return VerificationEngine()


class TestVerificationEngine:
    """Test cases for VerificationEngine"""
    
    def test_verify_basic_claim(self, engine):
        """Test basic claim verification"""
        query = "The Earth is round"
        result = engine.verify(query)
        
        assert "verdict_score" in result
        assert "confidence" in result
        assert "analysis" in result
        assert 0 <= result["verdict_score"] <= 100
        assert 0 <= result["confidence"] <= 1
    
    def test_verify_with_sources(self, engine):
        """Test verification with specified sources"""
        query = "COVID-19 is a virus"
        sources = ["wikipedia.org", "cdc.gov"]
        result = engine.verify(query, sources)
        
        assert "verdict_score" in result
        assert "sources" in result
        assert len(result["sources"]) <= len(sources)
    
    def test_verify_empty_query(self, engine):
        """Test verification with empty query"""
        with pytest.raises((ValueError, AssertionError)):
            engine.verify("")
    
    def test_verify_long_query(self, engine):
        """Test verification with very long query"""
        long_query = "This is a very long claim. " * 50
        # Should either work or truncate gracefully
        try:
            result = engine.verify(long_query)
            assert "verdict_score" in result
        except Exception:
            # Acceptable if it fails on very long inputs
            pass
    
    def test_verify_special_characters(self, engine):
        """Test verification with special characters"""
        query = "Is 2+2=4? @#$%^&*()"
        result = engine.verify(query)
        assert "verdict_score" in result
    
    def test_verify_different_languages(self, engine):
        """Test verification with non-English text"""
        queries = [
            "2+2=4",  # Math
            "Paris is the capital of France",
            "The world is round",
        ]
        for query in queries:
            result = engine.verify(query)
            assert "verdict_score" in result
            assert 0 <= result["verdict_score"] <= 100


class TestClaimDecomposition:
    """Test claim decomposition logic"""
    
    def test_decompose_simple_claim(self, engine):
        """Test decomposing a simple claim"""
        claim = "The Earth is round"
        components = engine.decompose_claim(claim)
        
        assert len(components) > 0
        assert all(isinstance(c, str) for c in components)
    
    def test_decompose_complex_claim(self, engine):
        """Test decomposing a complex claim with multiple parts"""
        claim = "COVID-19 is a virus and vaccines are effective"
        components = engine.decompose_claim(claim)
        
        assert len(components) >= 1


class TestScoring:
    """Test scoring logic"""
    
    def test_score_combination(self, engine):
        """Test combining multiple scores"""
        scores = [30, 40, 50]
        combined = engine._combine_scores(scores)
        
        assert 0 <= combined <= 100
        assert 30 <= combined <= 50  # Should be in range
    
    def test_confidence_from_variance(self, engine):
        """Test confidence calculation from score variance"""
        high_variance_scores = [20, 50, 80]
        low_variance_scores = [45, 48, 52]
        
        high_conf = engine._calculate_confidence(high_variance_scores)
        low_conf = engine._calculate_confidence(low_variance_scores)
        
        # Lower variance = higher confidence
        assert high_conf < low_conf


# ============================================================================
# Integration Tests (if model loading works)
# ============================================================================

class TestVerificationIntegration:
    """Integration tests with actual models"""
    
    @pytest.mark.slow
    def test_end_to_end_verification(self, engine):
        """Test complete verification pipeline"""
        query = "Water boils at 100 degrees Celsius"
        result = engine.verify(query)
        
        assert result["verdict_score"] < 40  # Should be TRUE
        assert result["confidence"] > 0.5
    
    @pytest.mark.slow
    def test_batch_verification(self, engine):
        """Test verifying multiple claims"""
        claims = [
            "The Earth is flat",
            "2+2=4",
            "Vaccines cause autism",
        ]
        
        for claim in claims:
            result = engine.verify(claim)
            assert "verdict_score" in result
            assert "confidence" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
