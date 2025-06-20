"""
Pipeline models for the End-to-End Integration Service.

These models capture the flow of events and status through our
Memory Anchor Discovery Trail pipeline.
"""

from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class PipelineStage(str, Enum):
    """Stages in the Memory Anchor Discovery Trail pipeline."""

    ACTIVITY_CAPTURE = "activity_capture"
    CORRELATION_DETECTION = "correlation_detection"
    ANCHOR_CREATION = "anchor_creation"
    PERSISTENCE = "persistence"
    COMPLETED = "completed"
    FAILED = "failed"


class PipelineEvent(BaseModel):
    """
    Represents an event flowing through the integration pipeline.

    Tracks the transformation journey from raw activity to memory anchor.
    """

    pipeline_id: UUID = Field(default_factory=uuid4)
    source_event_id: UUID = Field(..., description="Original event ID from activity stream")
    current_stage: PipelineStage = Field(default=PipelineStage.ACTIVITY_CAPTURE)

    # Timing information
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    stage_started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = Field(None)

    # Pipeline data
    activity_event: dict[str, Any] | None = Field(None, description="Original activity event")
    detected_correlations: list[dict[str, Any]] = Field(default_factory=list)
    created_anchors: list[str] = Field(default_factory=list, description="Memory anchor IDs")

    # Error handling
    error_message: str | None = Field(None)
    retry_count: int = Field(default=0)
    max_retries: int = Field(default=3)

    # Processing metadata
    processing_time_ms: dict[str, float] = Field(default_factory=dict)

    def advance_stage(
        self, new_stage: PipelineStage, processing_time_ms: float | None = None
    ) -> None:
        """Advance the pipeline event to the next stage."""
        if processing_time_ms is not None:
            self.processing_time_ms[self.current_stage.value] = processing_time_ms

        self.current_stage = new_stage
        self.stage_started_at = datetime.now(UTC)

        if new_stage in [PipelineStage.COMPLETED, PipelineStage.FAILED]:
            self.completed_at = datetime.now(UTC)

    def record_error(self, error_message: str) -> None:
        """Record an error in pipeline processing."""
        self.error_message = error_message
        self.retry_count += 1

        if self.retry_count >= self.max_retries:
            self.advance_stage(PipelineStage.FAILED)

    def get_total_processing_time(self) -> timedelta:
        """Get total time from creation to completion."""
        end_time = self.completed_at or datetime.now(UTC)
        return end_time - self.created_at

    def get_stage_processing_time(self, stage: PipelineStage) -> float | None:
        """Get processing time for a specific stage in milliseconds."""
        return self.processing_time_ms.get(stage.value)


class PipelineStatus(BaseModel):
    """Current status of the integration pipeline."""

    pipeline_id: str
    is_running: bool
    start_time: datetime

    # Component status
    file_connector_status: str = Field(default="unknown")
    correlation_engine_status: str = Field(default="unknown")
    memory_service_status: str = Field(default="unknown")

    # Event processing
    events_in_pipeline: int = Field(default=0)
    events_processed: int = Field(default=0)
    events_failed: int = Field(default=0)

    # Performance metrics
    avg_processing_time_ms: float = Field(default=0.0)
    events_per_second: float = Field(default=0.0)

    # Error tracking
    recent_errors: list[str] = Field(default_factory=list)
    error_rate: float = Field(default=0.0)


class PipelineStatistics(BaseModel):
    """Comprehensive statistics for the integration pipeline."""

    # Timing statistics
    uptime: timedelta
    total_events_processed: int
    successful_events: int
    failed_events: int

    # Stage performance
    stage_performance: dict[str, dict[str, float]] = Field(default_factory=dict)

    # Component statistics
    component_stats: dict[str, dict[str, Any]] = Field(default_factory=dict)

    # Correlation statistics
    correlations_detected: int = Field(default=0)
    correlation_types: dict[str, int] = Field(default_factory=dict)
    avg_correlation_confidence: float = Field(default=0.0)

    # Memory anchor statistics
    anchors_created: int = Field(default=0)
    anchor_types: dict[str, int] = Field(default_factory=dict)
    avg_anchor_creation_time_ms: float = Field(default=0.0)

    # Error analysis
    error_breakdown: dict[str, int] = Field(default_factory=dict)
    retry_statistics: dict[str, int] = Field(default_factory=dict)

    def calculate_success_rate(self) -> float:
        """Calculate overall pipeline success rate."""
        if self.total_events_processed == 0:
            return 0.0
        return self.successful_events / self.total_events_processed

    def calculate_throughput(self) -> float:
        """Calculate events per second throughput."""
        if self.uptime.total_seconds() == 0:
            return 0.0
        return self.total_events_processed / self.uptime.total_seconds()

    def get_performance_summary(self) -> dict[str, Any]:
        """Get a summary of pipeline performance metrics."""
        return {
            "success_rate": self.calculate_success_rate(),
            "throughput_eps": self.calculate_throughput(),
            "avg_processing_time_ms": sum(
                stats.get("avg_time_ms", 0) for stats in self.stage_performance.values()
            ),
            "total_processed": self.total_events_processed,
            "correlations_per_event": (
                self.correlations_detected / self.total_events_processed
                if self.total_events_processed > 0
                else 0
            ),
            "anchors_per_correlation": (
                self.anchors_created / self.correlations_detected
                if self.correlations_detected > 0
                else 0
            ),
        }


class PipelineConfiguration(BaseModel):
    """Configuration for the End-to-End Integration Service."""

    # Service configuration
    pipeline_id: str = Field(default_factory=lambda: str(uuid4()))
    max_concurrent_events: int = Field(default=100)
    event_queue_size: int = Field(default=1000)

    # File system connector configuration
    watch_directories: list[str] = Field(default_factory=list)
    file_filter_config: dict[str, Any] = Field(default_factory=dict)

    # Correlation engine configuration
    correlation_window_size_hours: int = Field(default=12)
    correlation_window_overlap: float = Field(default=0.3)
    correlation_confidence_threshold: float = Field(default=0.6)

    # Memory anchor configuration
    anchor_creation_threshold: float = Field(default=0.7)
    anchor_batch_size: int = Field(default=10)
    anchor_batch_timeout_seconds: int = Field(default=30)

    # Error handling
    max_retry_attempts: int = Field(default=3)
    retry_delay_seconds: float = Field(default=1.0)
    dead_letter_queue_enabled: bool = Field(default=True)

    # Performance tuning
    processing_timeout_seconds: int = Field(default=60)
    metrics_collection_interval_seconds: int = Field(default=30)
    health_check_interval_seconds: int = Field(default=10)

    # Debugging and monitoring
    enable_detailed_logging: bool = Field(default=False)
    enable_performance_profiling: bool = Field(default=False)
    log_correlation_details: bool = Field(default=False)
