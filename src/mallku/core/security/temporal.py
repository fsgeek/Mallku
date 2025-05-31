"""
Temporal encoding strategies for privacy-preserving timestamp storage.

Implements epoch-offset encoding to preserve temporal relationships
while hiding absolute timestamps.
"""

import random
from datetime import UTC, datetime

from pydantic import BaseModel, Field


class TemporalEncoder:
    """Handles temporal offset encoding for privacy."""

    def __init__(self, offset_seconds: int | None = None):
        """
        Initialize encoder with specific or random offset.

        Args:
            offset_seconds: Specific offset in seconds, or None for random
        """
        if offset_seconds is None:
            # Random offset: ±10 years in seconds
            self.offset_seconds = random.randint(-315360000, 315360000)
        else:
            self.offset_seconds = offset_seconds

    def encode(self, timestamp: datetime) -> float:
        """
        Encode timestamp with offset.

        Args:
            timestamp: Original timestamp (must be timezone-aware)

        Returns:
            Offset timestamp as float (seconds since epoch)
        """
        if timestamp.tzinfo is None:
            raise ValueError("Timestamp must be timezone-aware")

        # Convert to UTC and get seconds since epoch
        utc_timestamp = timestamp.astimezone(UTC)
        epoch_seconds = utc_timestamp.timestamp()

        # Apply offset
        return epoch_seconds + self.offset_seconds

    def decode(self, encoded_value: float) -> datetime:
        """
        Decode timestamp by removing offset.

        Args:
            encoded_value: Offset timestamp as float

        Returns:
            Original timestamp with UTC timezone
        """
        # Remove offset
        epoch_seconds = encoded_value - self.offset_seconds

        # Convert back to datetime
        return datetime.fromtimestamp(epoch_seconds, tz=UTC)

    def encode_with_precision(self, timestamp: datetime, precision: str) -> float:
        """
        Encode timestamp with reduced precision for additional privacy.

        Args:
            timestamp: Original timestamp
            precision: One of 'minute', 'hour', 'day'

        Returns:
            Offset timestamp with reduced precision
        """
        if timestamp.tzinfo is None:
            raise ValueError("Timestamp must be timezone-aware")

        # Reduce precision
        if precision == 'minute':
            timestamp = timestamp.replace(second=0, microsecond=0)
        elif precision == 'hour':
            timestamp = timestamp.replace(minute=0, second=0, microsecond=0)
        elif precision == 'day':
            timestamp = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            raise ValueError(f"Unknown precision: {precision}")

        return self.encode(timestamp)

    def encode_range(self, start: datetime, end: datetime) -> tuple[float, float]:
        """Encode a time range, preserving the relationship."""
        return (self.encode(start), self.encode(end))

    def get_offset_metadata(self) -> dict:
        """Get metadata about this encoder for storage."""
        return {
            "encoding_type": "temporal_offset",
            "offset_seconds": self.offset_seconds,
            "offset_days": self.offset_seconds / 86400,  # For human readability
            "created_at": datetime.now(UTC).isoformat(),
        }


class TemporalOffsetConfig(BaseModel):
    """Configuration for temporal offset encoding."""

    offset_seconds: int = Field(
        description="Offset in seconds from true epoch"
    )

    precision: str | None = Field(
        default=None,
        description="Precision level: minute, hour, or day"
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When this offset was generated"
    )

    @classmethod
    def generate_random(cls) -> "TemporalOffsetConfig":
        """Generate a random offset configuration."""
        return cls(
            offset_seconds=random.randint(-315360000, 315360000)
        )
