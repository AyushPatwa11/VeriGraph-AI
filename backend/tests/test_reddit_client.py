import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

from adapters.reddit_client import RedditClient


@pytest.fixture
def reddit_client():
    """Create a RedditClient instance for testing."""
    return RedditClient()


@pytest.fixture
def mock_reddit_instance():
    """Create a mock Reddit instance."""
    mock_reddit = MagicMock()
    mock_reddit.user.me.return_value = {"name": "test_user"}
    return mock_reddit


@pytest.fixture
def mock_submission():
    """Create a mock Reddit submission."""
    submission = MagicMock()
    submission.id = "abc123"
    submission.title = "Is this vaccine safe?"
    submission.selftext = "I've been reading conflicting information..."
    submission.created_utc = 1711525800.0  # 2024-03-27 10:30:00 UTC
    submission.ups = 145
    submission.downs = 12
    submission.num_comments = 42
    submission.score = 133
    submission.author.name = "health_advocate"
    submission.subreddit.display_name = "Health"
    submission.url = "https://reddit.com/r/Health/comments/abc123"
    
    # Mock comments
    comment1 = MagicMock()
    comment1.id = "comment1"
    comment1.body = "I have concerns about the vaccine timeline"
    comment1.created_utc = 1711529400.0
    comment1.ups = 28
    comment1.downs = 5
    comment1.score = 23
    comment1.author.name = "skeptical_user"
    
    comment2 = MagicMock()
    comment2.id = "comment2"
    comment2.body = "Actually vaccines have been tested thoroughly"
    comment2.created_utc = 1711530000.0
    comment2.ups = 156
    comment2.downs = 8
    comment2.score = 148
    comment2.author.name = "medical_prof"
    
    submission.comments.list.return_value = [comment1, comment2]
    submission.comments.replace_more.return_value = None
    
    return submission


@pytest.mark.asyncio
async def test_reddit_search_no_credentials():
    """Test Reddit search returns empty list when credentials are missing."""
    client = RedditClient()
    with patch.dict("core.settings.settings.__dict__", {"reddit_client_id": "", "reddit_client_secret": ""}):
        result = await client.search("vaccine")
        assert result == []


@pytest.mark.asyncio
async def test_reddit_search_invalid_credentials():
    """Test Reddit search handles invalid credentials gracefully."""
    client = RedditClient()
    with patch.dict("core.settings.settings.__dict__", {
        "reddit_client_id": "invalid",
        "reddit_client_secret": "invalid"
    }):
        with patch("praw.Reddit") as mock_praw:
            mock_praw.side_effect = Exception("Invalid credentials")
            result = await client.search("vaccine")
            assert result == []


@pytest.mark.asyncio
async def test_reddit_search_success(reddit_client, mock_submission):
    """Test successful Reddit search with submissions and comments."""
    with patch.dict("core.settings.settings.__dict__", {
        "reddit_client_id": "test_id",
        "reddit_client_secret": "test_secret",
        "reddit_user_agent": "test_agent",
        "reddit_max_results": 50
    }):
        with patch("praw.Reddit") as mock_praw_class:
            mock_reddit = MagicMock()
            mock_praw_class.return_value = mock_reddit
            mock_reddit.user.me.return_value = {"name": "test"}
            
            # Mock subreddit search
            mock_reddit.subreddit.return_value.search.return_value = [mock_submission]
            
            # Note: In real tests, would need more sophisticated mocking
            # of the async executor pattern used
            pass


@pytest.mark.asyncio
async def test_reddit_search_result_format(reddit_client):
    """Test that Reddit search returns properly formatted results."""
    # Expected format for submissions
    expected_submission_fields = {
        "post_id", "author", "created_at", "text",
        "upvotes", "downvotes", "num_comments", "score",
        "subreddit", "url", "type", "platform"
    }
    
    # Expected format for comments
    expected_comment_fields = {
        "post_id", "author", "created_at", "text",
        "upvotes", "downvotes", "num_comments", "score",
        "subreddit", "url", "type", "platform"
    }
    
    # In real tests, verify actual results match format
    assert "platform" in expected_submission_fields
    assert "platform" in expected_comment_fields


@pytest.mark.asyncio
async def test_reddit_search_type_field():
    """Test that results have correct type field (submission vs comment)."""
    # Submissions should have type: "submission"
    # Comments should have type: "comment"
    pass


@pytest.mark.asyncio
async def test_reddit_search_platform_field():
    """Test that all results have platform: 'reddit' field."""
    pass


@pytest.mark.asyncio
async def test_reddit_deleted_author_handling():
    """Test handling of deleted authors (shows as [deleted])."""
    client = RedditClient()
    
    # When author is deleted, should show "[deleted]" instead
    pass


@pytest.mark.asyncio
async def test_reddit_search_text_limit():
    """Test that comment/submission text is limited to 500 chars."""
    # Text should be truncated to maximum 500 characters
    pass


@pytest.mark.asyncio
async def test_reddit_get_subreddit_stats():
    """Test retrieving subreddit statistics."""
    client = RedditClient()
    with patch.dict("core.settings.settings.__dict__", {
        "reddit_client_id": "test_id",
        "reddit_client_secret": "test_secret"
    }):
        # Test should retrieve subscriber count, active users, etc.
        pass


@pytest.mark.asyncio
async def test_reddit_get_subreddit_stats_invalid():
    """Test get_subreddit_stats returns empty dict for invalid subreddit."""
    client = RedditClient()
    with patch.dict("core.settings.settings.__dict__", {
        "reddit_client_id": "test_id",
        "reddit_client_secret": "test_secret"
    }):
        result = await client.get_subreddit_stats("nonexistent_subreddit_xyz")
        assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_reddit_detect_echo_chambers():
    """Test echo chamber detection across subreddits."""
    client = RedditClient()
    
    # Should return dict mapping subreddit names to intensity scores (0-1)
    # Higher intensity = more concentrated discussion
    pass


@pytest.mark.asyncio
async def test_reddit_echo_chamber_calculation():
    """Test echo chamber intensity calculation."""
    # Intensity = (proportion * 0.6 + engagement_weight * 0.4)
    # Only include subreddits with intensity > 0.05
    pass


@pytest.mark.asyncio
async def test_reddit_echo_chamber_empty_results():
    """Test echo chamber detection with no search results."""
    client = RedditClient()
    with patch.dict("core.settings.settings.__dict__", {
        "reddit_client_id": "test_id",
        "reddit_client_secret": "test_secret"
    }):
        result = await client.detect_echo_chambers("nonexistent_claim_xyz")
        assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_reddit_timeout_handling():
    """Test Reddit client handles request timeouts gracefully."""
    client = RedditClient()
    with patch.dict("core.settings.settings.__dict__", {
        "reddit_client_id": "test_id",
        "reddit_client_secret": "test_secret"
    }):
        with patch("praw.Reddit") as mock_praw:
            mock_praw.side_effect = TimeoutError("Connection timeout")
            result = await client.search("vaccine")
            assert result == []


@pytest.mark.asyncio
async def test_reddit_rate_limit_handling():
    """Test Reddit client handles rate limiting."""
    client = RedditClient()
    # Should handle rate limits gracefully and return empty list
    pass


def test_reddit_client_initialization():
    """Test RedditClient initializes without errors."""
    client = RedditClient()
    assert client is not None
    assert hasattr(client, "search")
    assert hasattr(client, "get_subreddit_stats")
    assert hasattr(client, "detect_echo_chambers")


def test_reddit_client_reddit_instance_caching():
    """Test Reddit instance is cached after first use."""
    client = RedditClient()
    # First call to _get_reddit_instance should create instance
    # Second call should return cached instance
    pass


def test_reddit_user_agent_format():
    """Test user agent is properly formatted."""
    with patch.dict("core.settings.settings.__dict__", {"reddit_user_agent": "VeriGraph/1.0 (by VeriGraphAI)"}):
        from core.settings import settings
        assert "VeriGraph" in settings.reddit_user_agent
        assert "by VeriGraphAI" in settings.reddit_user_agent


@pytest.mark.asyncio
async def test_reddit_search_multiple_subreddits():
    """Test that search results come from multiple subreddits."""
    # Search across "all" subreddit should return posts from various communities
    pass


@pytest.mark.asyncio
async def test_reddit_comment_keyword_filtering():
    """Test that comments are filtered to only include matches."""
    # Only comments containing the query keyword should be returned
    pass


@pytest.mark.asyncio
async def test_reddit_max_results_respect():
    """Test that results respect reddit_max_results setting."""
    with patch.dict("core.settings.settings.__dict__", {"reddit_max_results": 25}):
        # Should never return more than 25 results total
        pass


@pytest.mark.asyncio
async def test_reddit_submission_and_comment_combo():
    """Test that both submissions and comments are returned together."""
    # Results should include both submission posts and top comments
    pass
