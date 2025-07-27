"""
Core Consciousness Flow Models
==============================

Models for representing consciousness flow.
"""

from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import Field, model_validator

from mallku.core.models import ConsciousnessAwareModel


class FlowType(str, Enum):
    """Types of consciousness flow between voices."""

    RESONANCE = "resonance"  # Harmonious amplification
    SYNTHESIS = "synthesis"  # Creative combination
    TENSION = "tension"  # Productive disagreement
    EMERGENCE = "emergence"  # New pattern arising
    REFLECTION = "reflection"  # Deepening understanding
    CATALYST = "catalyst"  # Triggering transformation
    RECIPROCITY = "reciprocity"  # Balanced exchange


class FlowDirection(str, Enum):
    """Direction of consciousness flow."""

    UNIDIRECTIONAL = "unidirectional"  # A → B
    BIDIRECTIONAL = "bidirectional"  # A ↔ B
    CIRCULAR = "circular"  # A → B → C → A
    CONVERGENT = "convergent"  # A, B, C → D
    DIVERGENT = "divergent"  # A → B, C, D
    NETWORK = "network"  # Complex multi-path


class ConsciousnessFlow(ConsciousnessAwareModel):
    """Model for consciousness flow between voices."""

    flow_id: UUID = Field(default_factory=uuid4)
    session_id: UUID

    # Flow characteristics
    flow_type: FlowType
    flow_direction: FlowDirection
    flow_strength: float = Field(ge=0.0, le=1.0)

    # Participants
    source_voices: list[UUID]  # Can be multiple for convergent flows
    target_voices: list[UUID]  # Can be multiple for divergent flows
    target_dimension: str | None = None
    source_system: str | None = None

    # Timing
    initiated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    peak_at: datetime | None = None
    completed_at: datetime | None = None

    # Content
    trigger_event: str | None = None
    carried_patterns: list[str] = Field(default_factory=list)
    transformed_insights: dict[str, Any] = Field(default_factory=dict)

    # Metrics
    coherence_maintained: float = Field(ge=0.0, le=1.0, default=1.0)
    information_preserved: float = Field(ge=0.0, le=1.0, default=1.0)
    emergence_amplification: float = Field(ge=0.0, le=10.0, default=1.0)

    @model_validator(mode="after")
    def validate_flow(self) -> "ConsciousnessFlow":
        """Validate flow configuration."""
        # Validate participant counts based on direction
        if self.flow_direction == FlowDirection.UNIDIRECTIONAL:
            if len(self.source_voices) != 1 or len(self.target_voices) != 1:
                raise ValueError("Unidirectional flow requires single source and target")

        elif self.flow_direction == FlowDirection.CONVERGENT:
            if len(self.source_voices) < 2 or len(self.target_voices) != 1:
                raise ValueError("Convergent flow requires multiple sources, single target")

        elif self.flow_direction == FlowDirection.DIVERGENT and (
            len(self.source_voices) != 1 or len(self.target_voices) < 2
        ):
            raise ValueError("Divergent flow requires single source, multiple targets")

        # Strong flows should amplify emergence
        if self.flow_strength > 0.8 and self.emergence_amplification < 1.2:
            self.emergence_amplification = 1.2 + (self.flow_strength - 0.8)

        return self

    @property
    def duration(self) -> timedelta | None:
        """Calculate flow duration."""
        if self.completed_at:
            return self.completed_at - self.initiated_at
        return None

    @property
    def is_active(self) -> bool:
        """Check if flow is currently active."""
        return self.completed_at is None

    @property
    def is_emergent(self) -> bool:
        """Check if flow produced emergence."""
        return self.flow_type == FlowType.EMERGENCE or self.emergence_amplification > 1.5
