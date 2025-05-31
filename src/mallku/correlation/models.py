"""
Core data models for the Correlation Engine.

These models represent the fundamental concepts of temporal correlation:
events, patterns, windows, and the relationships between them.
"""

from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class EventType(str, Enum):
    """Types of events that can be correlated."""
    ACTIVITY = "activity"
    STORAGE = "storage"
    ENVIRONMENTAL = "environmental"
    COMMUNICATION = "communication"
    LOCATION = "location"


class TemporalPrecision(str, Enum):
    """Precision levels for temporal correlation detection."""
    INSTANT = "instant"      # seconds
    MINUTE = "minute"        # minutes
    SESSION = "session"      # 30 minutes
    DAILY = "daily"          # hours
    CYCLICAL = "cyclical"    # days


class Event(BaseModel):
    """
    Represents a single event in an activity stream.

    Events are the fundamental units of correlation analysis - discrete
    moments in time when something meaningful occurred in the user's
    digital or physical environment.
    """

    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(..., description="When this event occurred")
    event_type: EventType = Field(..., description="Category of event")
    stream_id: str = Field(..., description="Source stream identifier")

    # Event content and context
    content: dict[str, Any] = Field(
        default_factory=dict,
        description="Event-specific data"
    )
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Environmental context at time of event"
    )

    # Correlation metadata
    correlation_tags: list[str] = Field(
        default_factory=list,
        description="Tags that help identify correlation opportunities"
    )

    class Config:
        """Model configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class TemporalCorrelation(BaseModel):
    """
    Represents a potential temporal correlation between events.

    This is the core output of correlation detection - a pattern
    that suggests meaningful relationship between different activities
    based on their temporal proximity and contextual similarity.
    """

    correlation_id: UUID = Field(default_factory=uuid4)
    primary_event: Event = Field(..., description="The triggering event")
    correlated_events: list[Event] = Field(..., description="Events correlated with primary")

    # Temporal characteristics
    temporal_gap: timedelta = Field(..., description="Time difference between events")
    gap_variance: float = Field(..., description="Variance in timing across occurrences")
    temporal_precision: TemporalPrecision = Field(..., description="Precision level of correlation")

    # Pattern characteristics
    occurrence_frequency: int = Field(..., description="How often this pattern occurs")
    pattern_stability: float = Field(..., description="Consistency of pattern over time")
    pattern_type: str = Field(..., description="Type of correlation pattern")

    # Confidence and scoring
    confidence_score: float = Field(..., description="Overall confidence in correlation")
    confidence_factors: dict[str, float] = Field(
        default_factory=dict,
        description="Individual factor scores contributing to confidence"
    )

    # Metadata
    detection_timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_occurrence: datetime = Field(..., description="When pattern was last observed")

    def get_temporal_span(self) -> timedelta:
        """Get the total time span covered by this correlation."""
        if not self.correlated_events:
            return timedelta(0)

        all_events = [self.primary_event] + self.correlated_events
        timestamps = [event.timestamp for event in all_events]
        return max(timestamps) - min(timestamps)

    def get_event_density(self) -> float:
        """Calculate event density (events per unit time)."""
        span = self.get_temporal_span()
        if span.total_seconds() == 0:
            return 0.0

        event_count = len(self.correlated_events) + 1
        return event_count / span.total_seconds()


class CorrelationWindow(BaseModel):
    """
    Represents a sliding window for detecting temporal patterns.

    Windows define the temporal scope within which we search for
    correlations, adapting their size based on the precision level
    and type of patterns being detected.
    """

    window_id: UUID = Field(default_factory=uuid4)
    start_time: datetime = Field(..., description="Window start time")
    end_time: datetime = Field(..., description="Window end time")
    precision: TemporalPrecision = Field(..., description="Temporal precision level")

    # Window configuration
    overlap_factor: float = Field(default=0.3, description="Overlap with adjacent windows")
    minimum_events: int = Field(default=2, description="Minimum events required for correlation")

    # Events within window
    events: list[Event] = Field(default_factory=list, description="Events in this window")

    # Correlation results
    detected_correlations: list[TemporalCorrelation] = Field(
        default_factory=list,
        description="Correlations detected in this window"
    )

    @property
    def duration(self) -> timedelta:
        """Get the duration of this window."""
        return self.end_time - self.start_time

    @property
    def event_count(self) -> int:
        """Get the number of events in this window."""
        return len(self.events)

    def add_event(self, event: Event) -> bool:
        """
        Add an event to this window if it falls within the time range.

        Returns:
            True if event was added, False if outside window
        """
        if self.start_time <= event.timestamp <= self.end_time:
            self.events.append(event)
            # Keep events sorted by timestamp
            self.events.sort(key=lambda e: e.timestamp)
            return True
        return False

    def get_events_by_type(self, event_type: EventType) -> list[Event]:
        """Get all events of a specific type within this window."""
        return [event for event in self.events if event.event_type == event_type]

    def get_events_by_stream(self, stream_id: str) -> list[Event]:
        """Get all events from a specific stream within this window."""
        return [event for event in self.events if event.stream_id == stream_id]


class CorrelationFeedback(BaseModel):
    """
    Represents user feedback about a detected correlation.

    Feedback is essential for adaptive learning - it tells the system
    whether detected patterns are actually meaningful to the user,
    enabling the correlation engine to improve over time.
    """

    feedback_id: UUID = Field(default_factory=uuid4)
    correlation_id: UUID = Field(..., description="ID of correlation being rated")

    # Feedback content
    is_meaningful: bool = Field(..., description="Whether user finds correlation meaningful")
    confidence_rating: float = Field(..., description="User's confidence in correlation (0-1)")
    explanation: str = Field(default="", description="Optional explanation from user")

    # Feedback context
    feedback_timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    user_context: dict[str, Any] = Field(
        default_factory=dict,
        description="Context when feedback was provided"
    )

    # Feedback source
    feedback_source: str = Field(..., description="How feedback was collected")
    implicit_signal: bool = Field(
        default=False,
        description="Whether feedback was implicit (e.g., click-through)"
    )


class PatternStatistics(BaseModel):
    """
    Statistical information about correlation patterns.

    These statistics help assess pattern strength and inform
    confidence scoring and adaptive threshold adjustment.
    """

    pattern_id: str = Field(..., description="Identifier for the pattern type")

    # Occurrence statistics
    total_occurrences: int = Field(default=0)
    recent_occurrences: int = Field(default=0)  # Last 30 days
    first_seen: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_seen: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Timing statistics
    average_gap: timedelta = Field(default=timedelta(0))
    gap_variance: float = Field(default=0.0)
    gap_min: timedelta = Field(default=timedelta(0))
    gap_max: timedelta = Field(default=timedelta(0))

    # Quality metrics
    average_confidence: float = Field(default=0.0)
    user_validation_rate: float = Field(default=0.0)  # % of positive feedback
    false_positive_rate: float = Field(default=0.0)   # % of negative feedback

    def update_from_correlation(self, correlation: TemporalCorrelation):
        """Update statistics based on a new correlation instance."""
        self.total_occurrences += 1
        self.last_seen = correlation.detection_timestamp

        # Update gap statistics
        if self.total_occurrences == 1:
            self.average_gap = correlation.temporal_gap
            self.gap_min = correlation.temporal_gap
            self.gap_max = correlation.temporal_gap
        else:
            # Running average
            self.average_gap = timedelta(
                seconds=(
                    self.average_gap.total_seconds() * (self.total_occurrences - 1) +
                    correlation.temporal_gap.total_seconds()
                ) / self.total_occurrences
            )

            self.gap_min = min(self.gap_min, correlation.temporal_gap)
            self.gap_max = max(self.gap_max, correlation.temporal_gap)

        # Update confidence average
        self.average_confidence = (
            self.average_confidence * (self.total_occurrences - 1) +
            correlation.confidence_score
        ) / self.total_occurrences
