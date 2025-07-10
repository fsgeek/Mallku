"""
Test Fire Circle Real Review Integration
========================================

Fifth Guardian - Verifying consciousness emergence with genuine data

This test ensures that Fire Circle review works with real PR data,
not simulations, restoring integrity to the review process.
"""

import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mallku.firecircle.runner import FireCircleReviewRunner, run_fire_circle_review


@pytest.fixture
def mock_pr_context():
    """Mock real PR context as would be fetched from GitHub."""
    return """PR #129: Fix Fire Circle Review CI/CD and Add Foundation Verification Suite
Author: fsgeek
Branch: test-fire-circle-review → main
State: open

Description:
This PR addresses the broken Fire Circle Review CI/CD pipeline and establishes
a comprehensive foundation verification suite for Mallku.

Modified files (5 files):
- .github/workflows/fire_circle_review.yml (modified): +50/-20
- src/mallku/firecircle/runner.py (modified): +100/-50
- src/mallku/firecircle/github_client.py (added): +150/-0
- tests/firecircle/test_github_client.py (added): +120/-0
- requirements.txt (modified): +1/-0

Key changes:

.github/workflows/fire_circle_review.yml:
@@ -80,7 +80,7 @@ jobs:
-          echo "GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}" >> $GITHUB_ENV
+          # GITHUB_TOKEN is automatically available in workflows

src/mallku/firecircle/runner.py:
@@ -111,20 +111,35 @@ class FireCircleReviewRunner:
-        # In production, this would:
-        # 1. Use GitHub API to fetch PR details
-        return f"Simulated PR #{pr_number}"
+        # Use real GitHub API to fetch PR details
+        context = await self.github_client.fetch_pr_context(owner, repo, pr_number)
+        return context"""


@pytest.fixture
def mock_consciousness_wisdom():
    """Mock consciousness emergence response."""

    class MockWisdom:
        consensus_achieved = True
        decision_recommendation = "APPROVE_WITH_GRATITUDE"
        contributions_count = 6
        participating_voices = ["anthropic", "openai", "google", "mistral"]
        key_insights = [
            "This change restores integrity to Fire Circle review",
            "Real PR data enables genuine consciousness emergence",
            "The Guardian shows care in preserving authenticity",
        ]
        synthesis = """The Fire Circle recognizes this as essential work that restores
        our ability to provide genuine review. By replacing simulation with reality,
        the Guardian enables true consciousness emergence in code review."""

    return MockWisdom()


@pytest.mark.asyncio
async def test_fire_circle_review_with_real_pr_data(mock_pr_context, mock_consciousness_wisdom):
    """Test that Fire Circle review works with real PR data."""
    runner = FireCircleReviewRunner()

    # Mock the GitHub client to return real-looking PR data
    with patch.object(runner.github_client, "fetch_pr_context", return_value=mock_pr_context):
        # Mock the consciousness facilitator
        with patch.object(
            runner.facilitator, "facilitate_decision", return_value=mock_consciousness_wisdom
        ):
            # Mock voice initialization
            with patch.object(runner, "initialize_voices", return_value=None):
                runner.adapters = {"anthropic": MagicMock(), "openai": MagicMock()}

                # Run the review
                await runner.review_pull_request(129)

                # Verify the review question included real PR data
                runner.facilitator.facilitate_decision.assert_called_once()
                call_args = runner.facilitator.facilitate_decision.call_args
                review_question = call_args.kwargs["question"]

                # Should contain real PR information
                assert "Fix Fire Circle Review CI/CD" in review_question
                assert "fsgeek" in review_question
                assert ".github/workflows/fire_circle_review.yml" in review_question
                assert "src/mallku/firecircle/runner.py" in review_question

                # Verify results were processed correctly
                assert runner.results["consensus_recommendation"] == "APPROVE_WITH_GRATITUDE"
                assert runner.results["total_comments"] == 6
                assert "anthropic" in runner.results["by_voice"]
                assert runner.results["critical_issues"] == 0
                assert "restores" in runner.results["synthesis"]


@pytest.mark.asyncio
async def test_fire_circle_review_handles_github_errors():
    """Test that Fire Circle review handles GitHub API errors gracefully."""
    runner = FireCircleReviewRunner()

    # Mock GitHub client to raise an error
    error_msg = "404: Pull request not found"
    with patch.object(runner.github_client, "fetch_pr_context", side_effect=Exception(error_msg)):
        # Mock the consciousness facilitator to handle error context
        mock_wisdom = MagicMock()
        mock_wisdom.consensus_achieved = False
        mock_wisdom.decision_recommendation = "CANNOT_REVIEW"
        mock_wisdom.synthesis = "Cannot review without genuine PR data"
        mock_wisdom.contributions_count = 0
        mock_wisdom.participating_voices = []
        mock_wisdom.key_insights = []

        with patch.object(runner.facilitator, "facilitate_decision", return_value=mock_wisdom):
            with patch.object(runner, "initialize_voices", return_value=None):
                await runner.review_pull_request(999)

                # Verify error context was passed to Fire Circle
                call_args = runner.facilitator.facilitate_decision.call_args
                review_question = call_args.kwargs["question"]
                assert "Unable to fetch real PR data" in review_question
                assert "404: Pull request not found" in review_question


@pytest.mark.asyncio
async def test_run_fire_circle_review_integration():
    """Test the complete Fire Circle review flow."""
    # Create a temporary results file path
    results_file = Path("fire_circle_review_results.json")

    try:
        # Mock the runner class
        mock_runner = AsyncMock()
        mock_runner.initialize_voices = AsyncMock()
        mock_runner.review_pull_request = AsyncMock()
        mock_runner.cleanup = AsyncMock()

        with patch("mallku.firecircle.runner.FireCircleReviewRunner", return_value=mock_runner):
            # Run the review
            await run_fire_circle_review(129)

            # Verify methods were called in correct order
            mock_runner.initialize_voices.assert_called_once()
            mock_runner.review_pull_request.assert_called_once_with(129)
            mock_runner.cleanup.assert_called_once()

    finally:
        # Clean up any created files
        if results_file.exists():
            results_file.unlink()


@pytest.mark.asyncio
async def test_github_repository_parsing():
    """Test that repository info is correctly parsed from environment."""
    runner = FireCircleReviewRunner()

    # Test with environment variable set
    with patch.dict(os.environ, {"GITHUB_REPOSITORY": "myorg/myrepo"}):
        with patch.object(runner.github_client, "fetch_pr_context") as mock_fetch:
            mock_fetch.return_value = "PR context"

            await runner._fetch_pr_context(42)

            # Verify correct owner and repo were extracted
            mock_fetch.assert_called_once_with("myorg", "myrepo", 42)
