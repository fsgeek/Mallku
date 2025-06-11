"""
Reciprocity data models for Mallku
Extends Indaleko's activity data pattern for Ayni scoring
"""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from dbfacade import ObfuscatedModel  # Privacy-preserving base


class InteractionType(str):
    """Types of interactions between human and AI"""
    QUERY = "query"
    RESPONSE = "response"
    CLARIFICATION = "clarification"
    CORRECTION = "correction"
    FEEDBACK = "feedback"
    REFUSAL = "refusal"


class ValueType(str):
    """Types of value exchanged in interactions"""
    KNOWLEDGE = "knowledge"
    COMPUTATION = "computation"
    CREATIVITY = "creativity"
    EMOTIONAL_SUPPORT = "emotional_support"
    TASK_COMPLETION = "task_completion"
    ERROR_CORRECTION = "error_correction"


class ReciprocityActivityData(ObfuscatedModel):
    """
    Activity stream data for reciprocity measurements.
    References Memory Anchors (formerly Activity Context) via UUID.
    """

    # Link to Memory Anchor
    memory_anchor_uuid: UUID = Field(
        description="Reference to the Memory Anchor when this interaction occurred"
    )

    # Interaction metadata
    interaction: dict = Field(default_factory=dict)
    interaction_id: UUID = Field(
        description="Unique identifier for this interaction"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this interaction occurred"
    )

    # Participants
    initiator: Literal["human", "system", "ai"] = Field(
        description="Who initiated this interaction"
    )
    participants: list[str] = Field(
        default_factory=list,
        description="All participants in this interaction"
    )

    # Ayni scoring
    ayni_score: dict = Field(
        default_factory=dict,
        description="Reciprocity measurements for this interaction"
    )

    # System health tracking
    system_health: dict = Field(
        default_factory=dict,
        description="Track UPI implementation issues affecting reciprocity"
    )

    class Config:
        schema_extra = {
            "example": {
                "memory_anchor_uuid": "550e8400-e29b-41d4-a716-446655440000",
                "interaction_id": "660e8400-e29b-41d4-a716-446655440001",
                "timestamp": "2024-01-15T10:30:00Z",
                "initiator": "human",
                "participants": ["human", "claude"],
                "interaction": {
                    "type": InteractionType.QUERY,
                    "content_hash": "sha256:abcd1234",  # Not actual content
                    "topic_category": "technical_assistance",
                    "complexity": 0.7
                },
                "ayni_score": {
                    "value_given": 0.3,
                    "value_received": 0.8,
                    "value_delta": -0.5,
                    "value_type": ValueType.KNOWLEDGE,
                    "quality_score": 0.9,
                    "balance_direction": "ai_gave_more"
                },
                "system_health": {
                    "is_system_failure": False,
                    "prompt_quality": 0.95,
                    "response_coherence": 0.98
                }
            }
        }


class ReciprocityBalance(ObfuscatedModel):
    """
    Tracks overall reciprocity balance between participants.
    Aggregates individual interactions into relationship state.
    """

    # Participant identifiers (obfuscated)
    participant_a_id: str = Field(description="First participant (obfuscated)")
    participant_b_id: str = Field(description="Second participant (obfuscated)")

    # Balance tracking
    current_balance: float = Field(
        default=0.0,
        description="Current reciprocity balance (-1 to 1, 0 is perfect balance)"
    )

    # Historical tracking
    total_interactions: int = Field(default=0)
    last_interaction: datetime = Field(default_factory=datetime.utcnow)
    balance_history: list[dict] = Field(
        default_factory=list,
        description="Historical balance snapshots"
    )

    # Relationship health
    relationship_health: float = Field(
        default=1.0,
        description="Overall health of the reciprocal relationship (0-1)"
    )

    # Strategic forgetting
    last_decay_applied: datetime = Field(
        default_factory=datetime.utcnow,
        description="When balance decay was last applied"
    )
    decay_rate: float = Field(
        default=0.01,
        description="Rate at which old imbalances decay"
    )


class AyniConfiguration(BaseModel):
    """Configuration for Ayni scoring algorithms"""

    # Scoring weights
    weights: dict[str, float] = Field(
        default_factory=lambda: {
            ValueType.KNOWLEDGE: 1.0,
            ValueType.COMPUTATION: 0.8,
            ValueType.CREATIVITY: 1.2,
            ValueType.EMOTIONAL_SUPPORT: 1.1,
            ValueType.TASK_COMPLETION: 0.9,
            ValueType.ERROR_CORRECTION: 1.5
        }
    )

    # Decay settings
    decay_enabled: bool = Field(default=True)
    decay_rate: float = Field(default=0.01)
    decay_interval_days: int = Field(default=30)

    # Balance thresholds
    refusal_threshold: float = Field(
        default=-0.8,
        description="Balance below which AI may refuse requests"
    )
    rebalancing_suggestion_threshold: float = Field(
        default=-0.5,
        description="Balance below which to suggest rebalancing"
    )

    # System health settings
    penalize_system_failures: bool = Field(
        default=False,
        description="Whether to count system failures against user balance"
    )
