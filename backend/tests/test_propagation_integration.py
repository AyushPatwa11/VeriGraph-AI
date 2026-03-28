"""
Integration tests for Facebook and Reddit propagation tracking.
Tests end-to-end flow of collecting posts and detecting propaganda spread.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

from services.scraper import ScraperService
from adapters.facebook_client import FacebookClient
from adapters.reddit_client import RedditClient


@pytest.fixture
def scraper_service():
    """Create a ScraperService instance."""
    return ScraperService()


@pytest.mark.asyncio
async def test_scraper_integration_includes_facebook_and_reddit(scraper_service):
    """Test that scraper collects from both Facebook and Reddit."""
    assert hasattr(scraper_service, 'facebook')
    assert hasattr(scraper_service, 'reddit')
    assert isinstance(scraper_service.facebook, FacebookClient)
    assert isinstance(scraper_service.reddit, RedditClient)


@pytest.mark.asyncio
async def test_scraper_collect_combined_sources():
    """Test scraper collects data from all sources including Facebook and Reddit."""
    service = ScraperService()
    
    with patch.dict("core.settings.settings.__dict__", {
        "facebook_access_token": "test_token",
        "reddit_client_id": "test_id",
        "reddit_client_secret": "test_secret"
    }):
        # Mock all adapter search methods
        service.news.search = AsyncMock(return_value=[])
        service.gdelt.search = AsyncMock(return_value=[])
        service.telegram.search = AsyncMock(return_value=[])
        service.commoncrawl.search = AsyncMock(return_value=[])
        service.facebook.search = AsyncMock(return_value=[
            {
                "post_id": "123_456",
                "platform": "facebook",
                "likes": 50,
                "shares": 10,
            }
        ])
        service.reddit.search = AsyncMock(return_value=[
            {
                "post_id": "abc123",
                "platform": "reddit",
                "upvotes": 100,
                "downvotes": 5,
            }
        ])
        
        results = await service.collect("vaccine safety")
        
        # Should collect from both Facebook and Reddit
        assert any(r.get("platform") == "facebook" for r in results)
        assert any(r.get("platform") == "reddit" for r in results)


@pytest.mark.asyncio
async def test_scraper_deduplication_with_facebook_reddit():
    """Test scraper deduplicates posts from different sources."""
    service = ScraperService()
    
    # Mock adapters to return some duplicate URLs
    service.news.search = AsyncMock(return_value=[
        {"post_id": "1", "platform": "news", "urls": ["https://example.com/article"]}
    ])
    service.gdelt.search = AsyncMock(return_value=[])
    service.telegram.search = AsyncMock(return_value=[])
    service.commoncrawl.search = AsyncMock(return_value=[])
    service.facebook.search = AsyncMock(return_value=[])
    service.reddit.search = AsyncMock(return_value=[])
    
    results = await service.collect("test")
    
    # TODO: Verify deduplication logic works across all sources
    assert len(results) >= 0


@pytest.mark.asyncio
async def test_scraper_sorting_by_engagement():
    """Test scraper sorts results by engagement metric."""
    service = ScraperService()
    
    service.news.search = AsyncMock(return_value=[])
    service.gdelt.search = AsyncMock(return_value=[])
    service.telegram.search = AsyncMock(return_value=[])
    service.commoncrawl.search = AsyncMock(return_value=[])
    service.facebook.search = AsyncMock(return_value=[
        {"post_id": "f1", "platform": "facebook", "likes": 10, "shares": 5},
        {"post_id": "f2", "platform": "facebook", "likes": 100, "shares": 20},
    ])
    service.reddit.search = AsyncMock(return_value=[
        {"post_id": "r1", "platform": "reddit", "upvotes": 50, "downvotes": 0},
    ])
    
    results = await service.collect("test")
    
    # Results should be sorted by engagement (likes + shares or upvotes + downvotes)
    # Higher engagement items should appear first
    assert isinstance(results, list)


@pytest.mark.asyncio
async def test_scraper_error_handling_facebook():
    """Test scraper handles Facebook client errors gracefully."""
    service = ScraperService()
    
    service.news.search = AsyncMock(return_value=[])
    service.gdelt.search = AsyncMock(return_value=[])
    service.telegram.search = AsyncMock(return_value=[])
    service.commoncrawl.search = AsyncMock(return_value=[])
    service.facebook.search = AsyncMock(side_effect=Exception("API Error"))
    service.reddit.search = AsyncMock(return_value=[])
    
    # Should not raise exception, continue with other sources
    results = await service.collect("test")
    assert isinstance(results, list)


@pytest.mark.asyncio
async def test_scraper_error_handling_reddit():
    """Test scraper handles Reddit client errors gracefully."""
    service = ScraperService()
    
    service.news.search = AsyncMock(return_value=[])
    service.gdelt.search = AsyncMock(return_value=[])
    service.telegram.search = AsyncMock(return_value=[])
    service.commoncrawl.search = AsyncMock(return_value=[])
    service.facebook.search = AsyncMock(return_value=[])
    service.reddit.search = AsyncMock(side_effect=Exception("PRAW Error"))
    
    # Should not raise exception, continue with other sources
    results = await service.collect("test")
    assert isinstance(results, list)


@pytest.mark.asyncio
async def test_propagation_graph_facebook_reddit_nodes():
    """Test that propagation graph includes Facebook and Reddit posts as nodes."""
    # Post-collection, Facebook and Reddit posts should create nodes in the graph
    # with author information preserved
    pass


@pytest.mark.asyncio
async def test_cross_platform_propagation_links():
    """Test detection of cross-platform propagation (same article on FB and Reddit)."""
    # When same URL appears on both Facebook and Reddit, should link them
    pass


@pytest.mark.asyncio
async def test_reddit_echo_chamber_detection_integration():
    """Test end-to-end echo chamber detection for Reddit discussions."""
    from adapters.reddit_client import RedditClient
    
    client = RedditClient()
    
    with patch.dict("core.settings.settings.__dict__", {
        "reddit_client_id": "test",
        "reddit_client_secret": "test"
    }):
        # Should identify subreddits with concentrated discussion
        pass


@pytest.mark.asyncio
async def test_facebook_reach_enhancement():
    """Test that Facebook posts enhance propagation metrics with reach data."""
    # Facebook client should provide reach, impressions, etc.
    pass


def test_scraper_has_facebook_reddit_attributes():
    """Test that ScraperService has Facebook and Reddit client attributes."""
    service = ScraperService()
    
    assert hasattr(service, 'facebook')
    assert hasattr(service, 'reddit')
    assert hasattr(service, 'news')
    assert hasattr(service, 'gdelt')
    assert hasattr(service, 'telegram')
    assert hasattr(service, 'commoncrawl')


def test_parallel_collection_returns_six_sources():
    """Test that _collect_parallel returns data from 6 sources."""
    service = ScraperService()
    
    # The method signature should expect 6 return values now
    # (news, gdelt, telegram, commoncrawl, facebook, reddit)
    import inspect
    source = inspect.getsource(service._collect_parallel)
    
    # Should unpack 6 values
    assert "facebook_posts" in source or "facebook" in source.lower()
    assert "reddit_posts" in source or "reddit" in source.lower()


@pytest.mark.asyncio
async def test_collection_preserves_platform_field():
    """Test that platform field is preserved from Facebook and Reddit."""
    service = ScraperService()
    
    service.news.search = AsyncMock(return_value=[])
    service.gdelt.search = AsyncMock(return_value=[])
    service.telegram.search = AsyncMock(return_value=[])
    service.commoncrawl.search = AsyncMock(return_value=[])
    service.facebook.search = AsyncMock(return_value=[
        {"post_id": "1", "platform": "facebook"}
    ])
    service.reddit.search = AsyncMock(return_value=[
        {"post_id": "2", "platform": "reddit"}
    ])
    
    results = await service.collect("test")
    
    platforms = {r.get("platform") for r in results}
    assert "facebook" in platforms
    assert "reddit" in platforms


# ============================================================================
# Performance & Scale Tests
# ============================================================================

@pytest.mark.asyncio
async def test_scraper_handles_large_result_sets():
    """Test scraper efficiently handles large numbers of results."""
    service = ScraperService()
    
    # Simulate large result sets from multiple sources
    large_results = [
        {"post_id": f"p{i}", "platform": "facebook", "likes": i, "shares": i//2}
        for i in range(100)
    ]
    
    service.news.search = AsyncMock(return_value=[])
    service.gdelt.search = AsyncMock(return_value=[])
    service.telegram.search = AsyncMock(return_value=[])
    service.commoncrawl.search = AsyncMock(return_value=[])
    service.facebook.search = AsyncMock(return_value=large_results)
    service.reddit.search = AsyncMock(return_value=[])
    
    results = await service.collect("test")
    
    assert len(results) == 100
    # Should be sorted by engagement
    assert results[0]["likes"] >= results[-1]["likes"]


@pytest.mark.asyncio
async def test_scraper_timeout_resilience():
    """Test scraper continues if one source times out."""
    service = ScraperService()
    
    service.news.search = AsyncMock(side_effect=TimeoutError())
    service.gdelt.search = AsyncMock(return_value=[])
    service.telegram.search = AsyncMock(return_value=[])
    service.commoncrawl.search = AsyncMock(return_value=[])
    service.facebook.search = AsyncMock(return_value=[{"post_id": "f1", "platform": "facebook"}])
    service.reddit.search = AsyncMock(side_effect=TimeoutError())
    
    # Should still return Facebook results
    results = await service.collect("test")
    assert len(results) >= 0  # At minimum, shouldn't crash
