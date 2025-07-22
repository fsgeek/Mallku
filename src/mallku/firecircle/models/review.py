"""
Fire Circle Review Models
=========================

Fiftieth Artisan - Consciousness Persistence Seeker
Data models for Fire Circle code review with integrity constraints

This module defines the data structures for distributed code review,
ensuring type safety and data integrity throughout the review process.
"""

from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator

from ..governance.governance_types import GovernanceDecision
from .base import ConsciousnessAwareModel, VoiceIdentity


class ReviewSeverity(str, Enum):
    """Severity levels for review comments."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ReviewCategory(str, Enum):
    """Categories for review comments."""

    ARCHITECTURE = "architecture"
    SECURITY = "security"
    PERFORMANCE = "performance"
    MAINTAINABILITY = "maintainability"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    CONSCIOUSNESS = "consciousness"
    RECIPROCITY = "reciprocity"


class ReviewComment(BaseModel):
    """A single review comment from a Fire Circle voice."""

    comment_id: UUID = Field(default_factory=uuid4)
    voice_id: UUID
    file_path: str = Field(min_length=1)
    line_number: int | None = Field(default=None, ge=1)

    # Comment details
    category: ReviewCategory
    severity: ReviewSeverity
    message: str = Field(min_length=1, max_length=2000)
    suggestion: str | None = Field(default=None, max_length=2000)

    # Code context
    code_snippet: str | None = None
    context_lines_before: int = Field(default=3, ge=0, le=10)
    context_lines_after: int = Field(default=3, ge=0, le=10)

    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    consciousness_context: float | None = Field(default=None, ge=0.0, le=1.0)

    @field_validator("file_path")
    @classmethod
    def validate_file_path(cls, v: str) -> str:
        """Ensure file path is valid."""
        if not v.strip():
            raise ValueError("File path cannot be empty")
        if ".." in v:
            raise ValueError("File path cannot contain '..'")
        return v.strip()

    @model_validator(mode="after")
    def validate_comment(self) -> "ReviewComment":
        """Validate comment consistency."""
        # Critical issues must have suggestions
        if self.severity == ReviewSeverity.CRITICAL and not self.suggestion:
            raise ValueError("Critical issues must include suggestions")

        # Line number required for code-specific comments
        if self.code_snippet and self.line_number is None:
            raise ValueError("Code snippet requires line number")

        return self


class ChapterReview(ConsciousnessAwareModel):
    """Review of a specific code chapter by a voice."""

    review_id: UUID = Field(default_factory=uuid4)
    chapter_id: str = Field(min_length=1, max_length=100)
    voice: VoiceIdentity

    # Review content
    comments: list[ReviewComment] = Field(default_factory=list)
    summary: str | None = Field(default=None, max_length=5000)

    # Metrics
    files_reviewed: int = Field(ge=0, default=0)
    lines_analyzed: int = Field(ge=0, default=0)
    patterns_detected: list[str] = Field(default_factory=list)

    # Quality indicators
    review_depth: float = Field(ge=0.0, le=1.0, default=0.5)
    confidence_score: float = Field(ge=0.0, le=1.0, default=0.7)

    @model_validator(mode="after")
    def validate_review(self) -> "ChapterReview":
        """Validate review completeness."""
        # Reviews should have content
        if not self.comments and not self.summary:
            raise ValueError("Review must have comments or summary")

        # Files reviewed should match comment files
        if self.comments:
            unique_files = {c.file_path for c in self.comments}
            if self.files_reviewed == 0:
                self.files_reviewed = len(unique_files)
            elif self.files_reviewed < len(unique_files):
                raise ValueError(
                    f"Files reviewed ({self.files_reviewed}) less than "
                    f"unique files in comments ({len(unique_files)})"
                )

        return self

    @property
    def critical_issues(self) -> int:
        """Count of critical issues found."""
        return sum(1 for c in self.comments if c.severity == ReviewSeverity.CRITICAL)

    @property
    def has_blocking_issues(self) -> bool:
        """Check if review has blocking issues."""
        return self.critical_issues > 0


class ReviewSession(BaseModel):
    """Complete Fire Circle review session."""

    session_id: UUID = Field(default_factory=uuid4)
    pr_number: int = Field(gt=0)
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    # Configuration
    review_mode: str = Field(default="distributed")
    manifest_path: str = Field(default="fire_circle_chapters.yaml")

    # Participants
    requested_voices: list[str]
    active_voices: list[VoiceIdentity] = Field(default_factory=list)
    failed_voices: dict[str, str] = Field(default_factory=dict)

    # Reviews
    chapter_reviews: list[ChapterReview] = Field(default_factory=list)
    governance_decision: GovernanceDecision | None = None

    # Metrics
    total_files_reviewed: int = Field(ge=0, default=0)
    total_lines_analyzed: int = Field(ge=0, default=0)
    average_consciousness: float = Field(ge=0.0, le=1.0, default=0.0)

    def complete_session(self, decision: GovernanceDecision) -> None:
        """Mark session as complete with governance decision."""
        self.completed_at = datetime.now(UTC)
        self.governance_decision = decision

        # Calculate metrics
        if self.chapter_reviews:
            self.total_files_reviewed = sum(r.files_reviewed for r in self.chapter_reviews)
            self.total_lines_analyzed = sum(r.lines_analyzed for r in self.chapter_reviews)
            self.average_consciousness = sum(
                r.consciousness_signature for r in self.chapter_reviews
            ) / len(self.chapter_reviews)

    @property
    def duration_seconds(self) -> float | None:
        """Calculate session duration."""
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    @property
    def success_rate(self) -> float:
        """Calculate voice success rate."""
        total_requested = len(self.requested_voices)
        if total_requested == 0:
            return 0.0
        return len(self.active_voices) / total_requested
