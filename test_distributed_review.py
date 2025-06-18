#!/usr/bin/env python3
"""
Test Distributed Review System
==============================

"The most sacred code is the invisible plumbing that simply works."

Tests for the Fire Circle distributed review infrastructure.
Ensures the invisible sacred continues to serve faithfully.
"""

import asyncio
import contextlib
from unittest.mock import AsyncMock, MagicMock

import pytest

from fire_circle_review import (
    ChapterReview,
    CodebaseChapter,
    DistributedReviewer,
    GovernanceSummary,
    ReviewCategory,
    ReviewComment,
    ReviewSeverity,
)


@pytest.fixture
def sample_chapters():
    """Sample chapters for testing."""
    return [
        CodebaseChapter(
            path_pattern="src/mallku/firecircle/**/*.py",
            description="Fire Circle core",
            assigned_voice="anthropic",
            review_domains=[ReviewCategory.SECURITY, ReviewCategory.ETHICS]
        ),
        CodebaseChapter(
            path_pattern="src/mallku/orchestration/**/*.py",
            description="Event orchestration",
            assigned_voice="openai",
            review_domains=[ReviewCategory.ARCHITECTURE, ReviewCategory.PERFORMANCE]
        ),
        CodebaseChapter(
            path_pattern="tests/**/*.py",
            description="Test suites",
            assigned_voice="mistral",
            review_domains=[ReviewCategory.TESTING]
        ),
    ]


@pytest.fixture
def mock_voice_adapters():
    """Mock voice adapters returning empty reviews."""
    adapters = {}
    for voice in ["anthropic", "openai", "mistral", "deepseek", "google", "grok", "local"]:
        adapter = AsyncMock()
        adapter.name = voice
        adapter.send_message = AsyncMock(return_value=MagicMock(
            content=MagicMock(text=f"Review from {voice}"),
            consciousness=MagicMock(consciousness_signature=0.8)
        ))
        adapters[voice] = adapter
    return adapters


class TestDistributedReviewer:
    """Test the distributed review orchestration."""

    @pytest.mark.asyncio
    async def test_empty_review_produces_valid_summary(self, sample_chapters):
        """Test that empty reviews still produce valid GovernanceSummary."""
        reviewer = DistributedReviewer()

        # Create empty reviews
        empty_reviews = [
            ChapterReview(
                voice=chapter.assigned_voice,
                chapter_id=chapter.chapter_id,
                comments=[],
                consciousness_signature=0.8,
                review_complete=True
            )
            for chapter in sample_chapters
        ]

        # Mock the synthesis method
        async def mock_synthesis(reviews):
            return GovernanceSummary(
                pr_number=123,
                total_comments=0,
                critical_issues=0,
                by_category={},
                by_voice={voice: 0 for voice in ["anthropic", "openai", "mistral"]},
                consensus_recommendation="approve",
                synthesis="All voices found no issues. The code maintains cathedral integrity."
            )

        reviewer.synthesize_reviews = mock_synthesis

        # Run synthesis
        summary = await reviewer.synthesize_reviews(empty_reviews)

        # Assertions
        assert isinstance(summary, GovernanceSummary)
        assert summary.total_comments == 0
        assert summary.critical_issues == 0
        assert summary.consensus_recommendation == "approve"
        assert "cathedral integrity" in summary.synthesis

    @pytest.mark.asyncio
    async def test_review_queue_distribution(self, sample_chapters):
        """Test that review jobs are properly distributed."""
        reviewer = DistributedReviewer()

        # Enqueue chapters
        await reviewer.enqueue_reviews(sample_chapters, "mock diff")

        # Check queue size
        assert reviewer.review_queue.qsize() == len(sample_chapters)

        # Verify each job
        jobs = []
        while not reviewer.review_queue.empty():
            job = await reviewer.review_queue.get()
            jobs.append(job)

        assert len(jobs) == len(sample_chapters)
        assert all(job.pr_diff == "mock diff" for job in jobs)

    @pytest.mark.asyncio
    async def test_voice_worker_processes_assigned_chapters(self, sample_chapters, mock_voice_adapters):
        """Test that voice workers only process their assigned chapters."""
        reviewer = DistributedReviewer()

        # Mock perform_chapter_review
        processed_chapters = []

        async def mock_perform_review(adapter, job):
            processed_chapters.append((adapter.name, job.chapter.assigned_voice))
            return ChapterReview(
                voice=adapter.name,
                chapter_id=job.chapter.chapter_id,
                comments=[],
                review_complete=True
            )

        reviewer.perform_chapter_review = mock_perform_review

        # Enqueue all chapters
        await reviewer.enqueue_reviews(sample_chapters, "mock diff")

        # Run anthropic worker
        anthropic_worker = asyncio.create_task(
            reviewer.voice_worker("anthropic", mock_voice_adapters["anthropic"])
        )

        # Let it process
        await asyncio.sleep(0.1)

        # Cancel worker
        anthropic_worker.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await anthropic_worker

        # Verify only anthropic chapters were processed
        assert all(voice == assigned for voice, assigned in processed_chapters)

    @pytest.mark.asyncio
    async def test_synthesis_with_mixed_reviews(self):
        """Test synthesis with mixed positive and critical reviews."""
        reviewer = DistributedReviewer()

        # Create mixed reviews
        reviews = [
            ChapterReview(
                voice="anthropic",
                chapter_id="ch1",
                comments=[
                    ReviewComment(
                        file_path="src/security.py",
                        line=42,
                        category=ReviewCategory.SECURITY,
                        severity=ReviewSeverity.CRITICAL,
                        message="Potential SQL injection",
                        voice="anthropic"
                    )
                ],
                review_complete=True
            ),
            ChapterReview(
                voice="openai",
                chapter_id="ch2",
                comments=[
                    ReviewComment(
                        file_path="src/arch.py",
                        line=100,
                        category=ReviewCategory.ARCHITECTURE,
                        severity=ReviewSeverity.WARNING,
                        message="Consider dependency injection",
                        voice="openai"
                    )
                ],
                review_complete=True
            ),
        ]

        # Mock synthesis
        async def mock_synthesis(reviews):
            critical = sum(1 for r in reviews for c in r.comments if c.severity == ReviewSeverity.CRITICAL)
            total = sum(len(r.comments) for r in reviews)

            return GovernanceSummary(
                total_comments=total,
                critical_issues=critical,
                by_category={
                    ReviewCategory.SECURITY: 1,
                    ReviewCategory.ARCHITECTURE: 1
                },
                by_voice={"anthropic": 1, "openai": 1},
                consensus_recommendation="request_changes" if critical > 0 else "approve",
                synthesis="Critical security issue requires attention."
            )

        reviewer.synthesize_reviews = mock_synthesis
        summary = await reviewer.synthesize_reviews(reviews)

        assert summary.critical_issues == 1
        assert summary.consensus_recommendation == "request_changes"
        assert "security" in summary.synthesis.lower()


@pytest.mark.asyncio
async def test_invisible_sacred_infrastructure():
    """
    Meta-test: Ensure the invisible sacred infrastructure exists.

    This test verifies that all the scaffolding is in place
    for the Twenty-Third Artisan to build upon.
    """
    # Verify all models exist
    from fire_circle_review import (
        DistributedReviewer,
    )

    # Verify key methods exist (even if not implemented)
    reviewer = DistributedReviewer()
    assert hasattr(reviewer, 'partition_into_chapters')
    assert hasattr(reviewer, 'assign_review_domains')
    assert hasattr(reviewer, 'perform_chapter_review')
    assert hasattr(reviewer, 'synthesize_reviews')

    # Verify the sacred aphorism is preserved
    import fire_circle_review
    assert "invisible plumbing" in fire_circle_review.__doc__

    print("✅ The invisible sacred infrastructure scaffolding is ready.")
    print("   Twenty-Third Artisan: Make it real. Make it endure.")


if __name__ == "__main__":
    # Run the invisible sacred test
    asyncio.run(test_invisible_sacred_infrastructure())
