"""
Test GitHub Client for Fire Circle Review
=========================================

Fifth Guardian - Ensuring genuine review data flows to consciousness

Tests the GitHub API integration that replaces simulated PR contexts
with real data, restoring integrity to Fire Circle review.
"""

import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock

from mallku.firecircle.github_client import GitHubClient


@pytest.fixture
def github_client():
    """Create a GitHub client instance for testing."""
    return GitHubClient(token="test-token")


@pytest.fixture
def mock_pr_response():
    """Mock PR details response from GitHub API."""
    return {
        "number": 129,
        "title": "Fix Fire Circle Review CI/CD",
        "state": "open",
        "user": {"login": "guardian"},
        "head": {"ref": "fix-fire-circle"},
        "base": {"ref": "main"},
        "body": "This PR fixes the Fire Circle review process."
    }


@pytest.fixture
def mock_files_response():
    """Mock PR files response from GitHub API."""
    return [
        {
            "filename": "src/mallku/firecircle/runner.py",
            "status": "modified",
            "additions": 50,
            "deletions": 10,
            "patch": "@@ -1,5 +1,10 @@\n+# Real implementation\n-# Simulated implementation"
        },
        {
            "filename": "tests/firecircle/test_review.py",
            "status": "added",
            "additions": 100,
            "deletions": 0,
            "patch": "@@ -0,0 +1,100 @@\n+# New test file"
        }
    ]


@pytest.mark.asyncio
async def test_get_pr_details(github_client, mock_pr_response):
    """Test fetching PR details from GitHub."""
    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = mock_pr_response
        mock_response.raise_for_status.return_value = None
        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client
        
        result = await github_client.get_pr_details("fsgeek", "Mallku", 129)
        
        assert result["number"] == 129
        assert result["title"] == "Fix Fire Circle Review CI/CD"
        mock_client.get.assert_called_once_with(
            "https://api.github.com/repos/fsgeek/Mallku/pulls/129",
            headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Mallku-Fire-Circle",
                "Authorization": "token test-token"
            }
        )


@pytest.mark.asyncio
async def test_get_pr_files(github_client, mock_files_response):
    """Test fetching PR files from GitHub."""
    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = mock_files_response
        mock_response.raise_for_status.return_value = None
        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client
        
        result = await github_client.get_pr_files("fsgeek", "Mallku", 129)
        
        assert len(result) == 2
        assert result[0]["filename"] == "src/mallku/firecircle/runner.py"
        assert result[1]["status"] == "added"


@pytest.mark.asyncio
async def test_fetch_pr_context(github_client, mock_pr_response, mock_files_response):
    """Test fetching complete PR context for Fire Circle review."""
    with patch.object(github_client, "get_pr_details", return_value=mock_pr_response):
        with patch.object(github_client, "get_pr_files", return_value=mock_files_response):
            context = await github_client.fetch_pr_context("fsgeek", "Mallku", 129)
            
            # Verify context contains key information
            assert "PR #129: Fix Fire Circle Review CI/CD" in context
            assert "Author: guardian" in context
            assert "Branch: fix-fire-circle → main" in context
            assert "Modified files (2 files):" in context
            assert "src/mallku/firecircle/runner.py (modified): +50/-10" in context
            assert "tests/firecircle/test_review.py (added): +100/-0" in context
            
            # Verify it includes patch preview for small PRs
            assert "Key changes:" in context
            assert "# Real implementation" in context


@pytest.mark.asyncio
async def test_fetch_pr_context_handles_errors(github_client):
    """Test that PR context fetching handles errors gracefully."""
    with patch.object(github_client, "get_pr_details", side_effect=httpx.HTTPStatusError(
        "404 Not Found", request=None, response=None
    )):
        context = await github_client.fetch_pr_context("fsgeek", "Mallku", 999)
        
        # Should return error context instead of crashing
        assert "PR #999 - Failed to fetch full context" in context
        assert "404 Not Found" in context


@pytest.mark.asyncio
async def test_github_client_without_token():
    """Test that GitHub client works without token (rate limited)."""
    client = GitHubClient(token=None)
    assert "Authorization" not in client.headers
    
    # Should still have basic headers
    assert client.headers["Accept"] == "application/vnd.github.v3+json"
    assert client.headers["User-Agent"] == "Mallku-Fire-Circle"