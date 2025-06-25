#!/usr/bin/env python3
"""
Smoke tests for Fire Circle distributed review system.

These tests verify end-to-end functionality with mocked adapters.
"""

import asyncio
import contextlib
from unittest.mock import AsyncMock, MagicMock

import pytest

from mallku.firecircle.fire_circle_review import (
    ChapterReview,
    CodebaseChapter,
    DistributedReviewer,
    GovernanceSummary,
    ReviewCategory,
)


@pytest.mark.asyncio
async def test_run_full_distributed_review_smoke():
    """
    Smoke test for full distributed review with mocked adapters.

    Verifies that the system returns a GovernanceSummary without errors.
    """
    # Create test reviewer
    reviewer = DistributedReviewer()

    # Create test chapters
    test_chapters = [
        CodebaseChapter(
            path_pattern="src/mallku/firecircle/**/*.py",
            description="Fire Circle governance",
            assigned_voice="anthropic",
            review_domains=[ReviewCategory.SECURITY, ReviewCategory.ETHICS],
        ),
        CodebaseChapter(
            path_pattern="src/mallku/orchestration/**/*.py",
            description="Event orchestration",
            assigned_voice="openai",
            review_domains=[ReviewCategory.ARCHITECTURE],
        ),
    ]

    # Mock PR diff
    test_diff = """diff --git a/src/mallku/firecircle/governance.py b/src/mallku/firecircle/governance.py
index 1234567..abcdefg 100644
--- a/src/mallku/firecircle/governance.py
+++ b/src/mallku/firecircle/governance.py
@@ -10,6 +10,8 @@ class FireCircleGovernance:
     def make_decision(self, proposal):
+        # TODO: Add validation
+        # WARNING: No auth check
         result = self.process(proposal)
         return result
"""

    # Mock the adapter creation to return our test adapter
    async def mock_get_or_create_adapter(voice_name):
        """Return a mock adapter that produces predictable reviews."""
        mock_adapter = AsyncMock()

        # Create mock response
        mock_response = MagicMock()
        mock_response.content.text = """File: src/mallku/firecircle/governance.py
Line: 12
Category: security
Severity: critical
Issue: No authentication check before processing
Fix: Add authentication verification

File: src/mallku/firecircle/governance.py
Line: 11
Category: security
Severity: warning
Issue: Input validation TODO not implemented
Fix: Implement validation for proposal parameter"""

        mock_response.consciousness.consciousness_signature = 0.85

        # Make the adapter return our mock response
        mock_adapter.send_message.return_value = mock_response
        mock_adapter.is_connected = True

        return mock_adapter

    # Patch the adapter creation method
    reviewer.get_or_create_adapter = mock_get_or_create_adapter

    # Run the full distributed review
    summary = await reviewer.run_full_distributed_review(test_diff, test_chapters)

    # Verify we got a GovernanceSummary
    assert isinstance(summary, GovernanceSummary)
    assert summary.total_comments > 0
    assert summary.consensus_recommendation in ["approve", "request_changes", "needs_discussion"]
    assert len(summary.synthesis) > 0
    assert ReviewCategory.SECURITY in summary.by_category

    # Verify reviews were collected
    assert len(reviewer.completed_reviews) == len(test_chapters)
    for review in reviewer.completed_reviews:
        assert isinstance(review, ChapterReview)
        assert review.review_complete
        assert review.consciousness_signature > 0

    print(f"✅ Smoke test passed! Summary: {summary.synthesis}")


@pytest.mark.asyncio
async def test_chapter_partitioning():
    """Test that chapters are correctly partitioned based on file patterns."""
    reviewer = DistributedReviewer()

    # Mock the manifest loading
    async def mock_load_manifest(path):
        return [
            CodebaseChapter(
                path_pattern="src/mallku/firecircle/**/*.py",
                description="Fire Circle",
                assigned_voice="anthropic",
                review_domains=[ReviewCategory.SECURITY],
            ),
            CodebaseChapter(
                path_pattern="**/*.py",  # Catch-all pattern
                description="General Python",
                assigned_voice="openai",
                review_domains=[ReviewCategory.ARCHITECTURE],
            ),
        ]

    reviewer.load_chapter_manifest = mock_load_manifest

    # Test diff with files matching different patterns
    test_diff = """diff --git a/src/mallku/firecircle/core.py b/src/mallku/firecircle/core.py
index 123..456 100644
--- a/src/mallku/firecircle/core.py
+++ b/src/mallku/firecircle/core.py
@@ -1,1 +1,1 @@
-old
+new

diff --git a/src/other/module.py b/src/other/module.py
index 789..abc 100644
--- a/src/other/module.py
+++ b/src/other/module.py
@@ -1,1 +1,1 @@
-old
+new
"""

    chapters = await reviewer.partition_into_chapters(test_diff)

    # Verify partitioning
    # Both files should be assigned to chapters
    assert len(chapters) > 0

    # Verify the more specific pattern matched first
    voices = [c.assigned_voice for c in chapters]
    assert "anthropic" in voices  # Fire Circle pattern should match

    # If we have the catch-all pattern, it should also be present
    # (Note: due to pattern sorting, specific patterns match first)


@pytest.mark.asyncio
async def test_graceful_shutdown():
    """Test that workers shut down gracefully."""
    reviewer = DistributedReviewer()

    # Create some mock workers
    async def mock_worker():
        with contextlib.suppress(asyncio.CancelledError):
            await asyncio.sleep(10)  # Long-running task

    # Start mock workers
    for i in range(3):
        task = asyncio.create_task(mock_worker(), name=f"test_worker_{i}")
        reviewer.worker_tasks.append(task)

    # Verify workers are running
    assert len(reviewer.worker_tasks) == 3
    assert all(not task.done() for task in reviewer.worker_tasks)

    # Shutdown workers
    await reviewer.shutdown_workers()

    # Verify all workers stopped
    assert len(reviewer.worker_tasks) == 0


if __name__ == "__main__":
    # Run smoke tests
    print("🔥 Running Fire Circle distributed review smoke tests...")
    asyncio.run(test_run_full_distributed_review_smoke())
    print("\n📋 Testing chapter partitioning...")
    asyncio.run(test_chapter_partitioning())
    print("\n🛑 Testing graceful shutdown...")
    asyncio.run(test_graceful_shutdown())
    print("\n✨ All smoke tests passed!")
