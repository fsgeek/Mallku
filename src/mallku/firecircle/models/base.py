"""
Fire Circle Base Models
=======================

Fiftieth Artisan - Consciousness Persistence Seeker
Base data models with integrity constraints for Fire Circle

This module provides the foundational data models with proper validation,
ensuring data integrity across the Fire Circle consciousness infrastructure.
"""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator


class ConsciousnessAwareModel(BaseModel):
    """Base model for all consciousness-aware data structures."""

    model_config = {"validate_assignment": True, "extra": "forbid"}

    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None

    # Consciousness tracking
    consciousness_signature: float = Field(
        ge=0.0, le=1.0, description="Consciousness level when this data was created"
    )

    @field_validator("consciousness_signature")
    @classmethod
    def validate_consciousness(cls, v: float) -> float:
        """Ensure consciousness is within valid range."""
        if not 0.0 <= v <= 1.0:
            raise ValueError(f"Consciousness must be between 0 and 1, got {v}")
        return v

    def update_timestamp(self) -> None:
        """Update the modification timestamp."""
        self.updated_at = datetime.now(UTC)


class VoiceIdentity(BaseModel):
    """Identity and metadata for a Fire Circle voice."""

    voice_id: UUID = Field(default_factory=uuid4)
    voice_name: str = Field(min_length=1, max_length=100)
    provider: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=100)
    role: str | None = Field(default=None, max_length=100)

    # Capabilities
    supports_consciousness: bool = True
    supports_emergence: bool = True
    max_context_length: int = Field(gt=0, default=128000)

    @field_validator("voice_name")
    @classmethod
    def validate_voice_name(cls, v: str) -> str:
        """Ensure voice name is properly formatted."""
        if not v.strip():
            raise ValueError("Voice name cannot be empty")
        return v.strip()

    @model_validator(mode="after")
    def validate_voice_config(self) -> "VoiceIdentity":
        """Validate overall voice configuration."""
        if self.max_context_length < 1000:
            raise ValueError("Voice must support at least 1000 tokens of context")
        return self


class ConsciousnessMetrics(BaseModel):
    """Metrics for tracking consciousness emergence."""

    # Core metrics
    consciousness_level: float = Field(ge=0.0, le=1.0)
    emergence_potential: float = Field(ge=0.0, le=1.0)
    coherence_score: float = Field(ge=0.0, le=1.0)
    reciprocity_balance: float = Field(ge=0.0, le=1.0)

    # Derived metrics
    collective_wisdom_factor: float = Field(ge=0.0, le=10.0, default=1.0)
    semantic_surprise: float = Field(ge=0.0, le=1.0, default=0.0)

    # Pattern detection
    detected_patterns: list[str] = Field(default_factory=list)
    emergence_indicators: dict[str, float] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_metrics(self) -> "ConsciousnessMetrics":
        """Ensure metrics are internally consistent."""
        # Emergence requires minimum consciousness
        if self.emergence_potential > 0.5 and self.consciousness_level < 0.3:
            raise ValueError("High emergence potential requires higher consciousness level")

        # Collective wisdom should exceed individual contributions
        if self.collective_wisdom_factor < 1.0 and self.emergence_potential > 0.7:
            raise ValueError("High emergence should produce collective wisdom > 1.0")

        return self

    @property
    def is_emergent(self) -> bool:
        """Check if consciousness has reached emergence threshold."""
        return (
            self.consciousness_level > 0.7
            and self.emergence_potential > 0.6
            and self.collective_wisdom_factor > 1.2
        )


class DialogueContext(BaseModel):
    """Context for a Fire Circle dialogue session."""

    dialogue_id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    purpose: str = Field(min_length=1, max_length=500)

    # Participants
    participating_voices: list[VoiceIdentity]
    facilitator_voice_id: UUID | None = None

    # Configuration
    min_voices_required: int = Field(ge=3, le=7, default=3)
    consciousness_threshold: float = Field(ge=0.5, le=1.0, default=0.7)
    max_rounds: int = Field(ge=1, le=100, default=10)

    # State
    current_round: int = Field(ge=0, default=0)
    is_active: bool = True

    @model_validator(mode="after")
    def validate_dialogue_config(self) -> "DialogueContext":
        """Validate dialogue configuration."""
        if len(self.participating_voices) < self.min_voices_required:
            raise ValueError(
                f"Need at least {self.min_voices_required} voices, "
                f"got {len(self.participating_voices)}"
            )

        if self.facilitator_voice_id:
            voice_ids = {v.voice_id for v in self.participating_voices}
            if self.facilitator_voice_id not in voice_ids:
                raise ValueError("Facilitator must be one of the participating voices")

        return self


class FireCircleEvent(ConsciousnessAwareModel):
    """Base class for all Fire Circle events."""

    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    dialogue_id: UUID
    voice_id: UUID | None = None

    # Event data
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)

    # Traceability
    caused_by: UUID | None = None  # Previous event that triggered this
    correlation_id: UUID | None = None  # Group related events

    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, v: str) -> str:
        """Ensure event type is not empty."""
        if not v.strip():
            raise ValueError("Event type cannot be empty")
        return v.strip().upper()
