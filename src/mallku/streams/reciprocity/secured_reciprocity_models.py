"""
Security-enhanced reciprocity models for Mallku.

These models demonstrate how to balance security with utility,
making conscious trade-offs for each field.
"""

from datetime import UTC, datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from ...core.security.field_strategies import (
    FieldIndexStrategy,
    FieldObfuscationLevel,
    SearchCapability,
)
from ...core.security.secured_model import SecuredField, SecuredModel


class ValueType(str, Enum):
    """Types of value exchanged in interactions"""

    KNOWLEDGE = "knowledge"
    COMPUTATION = "computation"
    CREATIVITY = "creativity"
    EMOTIONAL_SUPPORT = "emotional_support"
    TASK_COMPLETION = "task_completion"
    ERROR_CORRECTION = "error_correction"


class ReciprocityActivityData(SecuredModel):
    """
    Activity stream data for reciprocity measurements with field-level security.

    Each field declares its security/utility trade-offs explicitly.
    """

    # Link to Memory Anchor - needs equality search
    memory_anchor_uuid: UUID = SecuredField(
        description="Reference to the Memory Anchor when this interaction occurred",
        obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
        index_strategy=FieldIndexStrategy.BLIND,
        search_capabilities=[SearchCapability.EQUALITY],
        security_notes="UUID already obfuscated, blind index for lookups",
    )

    # Timestamp - critical for temporal queries
    timestamp: datetime = SecuredField(
        default_factory=lambda: datetime.now(UTC),
        description="When this interaction occurred",
        obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
        index_strategy=FieldIndexStrategy.TEMPORAL_OFFSET,
        search_capabilities=[SearchCapability.RANGE, SearchCapability.ORDERING],
        security_notes="Temporal offset preserves query capability while hiding absolute time",
    )

    # Interaction ID - needs exact match only
    interaction_id: UUID = SecuredField(
        description="Unique identifier for this interaction",
        obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
        index_strategy=FieldIndexStrategy.IDENTITY,  # UUIDs are already random
        search_capabilities=[SearchCapability.EQUALITY],
        security_notes="UUIDs provide no semantic information",
    )

    # Interaction metadata - sensitive, encrypted
    interaction: dict = SecuredField(
        default_factory=dict,
        obfuscation_level=FieldObfuscationLevel.ENCRYPTED,
        index_strategy=FieldIndexStrategy.NONE,
        security_notes="Contains potentially sensitive interaction details",
    )

    # Initiator - categorical, can use deterministic
    initiator: Literal["human", "system", "ai"] = SecuredField(
        description="Who initiated this interaction",
        obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
        index_strategy=FieldIndexStrategy.DETERMINISTIC,
        search_capabilities=[SearchCapability.EQUALITY],
        security_notes="Limited set of values, deterministic encoding sufficient",
    )

    # Participants - encrypted for privacy
    participants: list[str] = SecuredField(
        default_factory=list,
        description="All participants in this interaction",
        obfuscation_level=FieldObfuscationLevel.ENCRYPTED,
        index_strategy=FieldIndexStrategy.NONE,
        security_notes="Participant identities are sensitive",
    )

    # Ayni score - bucketed for range queries
    ayni_score: dict = SecuredField(
        default_factory=dict,
        description="Reciprocity measurements for this interaction",
        obfuscation_level=FieldObfuscationLevel.ENCRYPTED,
        index_strategy=FieldIndexStrategy.BUCKETED,
        search_capabilities=[SearchCapability.RANGE, SearchCapability.AGGREGATION],
        bucket_boundaries=[-1.0, -0.5, -0.1, 0.0, 0.1, 0.5, 1.0],
        security_notes="Bucketed to enable range queries while protecting exact scores",
    )

    # System health - less sensitive, identity storage
    system_health: dict = SecuredField(
        default_factory=dict,
        description="Track UPI implementation issues affecting reciprocity",
        obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
        index_strategy=FieldIndexStrategy.IDENTITY,
        security_notes="System metrics are less sensitive",
    )


class ReciprocityBalance(SecuredModel):
    """
    Tracks overall reciprocity balance with privacy protection.
    """

    # Participant IDs - already obfuscated, use blind indexing
    participant_a_id: str = SecuredField(
        description="First participant (obfuscated)",
        obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
        index_strategy=FieldIndexStrategy.BLIND,
        search_capabilities=[SearchCapability.EQUALITY],
        security_notes="Pre-obfuscated IDs, blind index for lookups",
    )

    participant_b_id: str = SecuredField(
        description="Second participant (obfuscated)",
        obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
        index_strategy=FieldIndexStrategy.BLIND,
        search_capabilities=[SearchCapability.EQUALITY],
        security_notes="Pre-obfuscated IDs, blind index for lookups",
    )

    # Current balance - sensitive but needs queries
    current_balance: float = SecuredField(
        default=0.0,
        description="Current reciprocity balance (-1 to 1)",
        obfuscation_level=FieldObfuscationLevel.ENCRYPTED,
        index_strategy=FieldIndexStrategy.BUCKETED,
        search_capabilities=[SearchCapability.RANGE],
        bucket_boundaries=[-1.0, -0.8, -0.5, -0.2, 0.0, 0.2, 0.5, 0.8, 1.0],
        security_notes="Bucketed to identify severely imbalanced relationships",
    )

    # Interaction count - less sensitive
    total_interactions: int = SecuredField(
        default=0,
        obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
        index_strategy=FieldIndexStrategy.IDENTITY,
        search_capabilities=[SearchCapability.RANGE, SearchCapability.AGGREGATION],
        security_notes="Count data is less sensitive",
    )

    # Last interaction - temporal offset
    last_interaction: datetime = SecuredField(
        default_factory=lambda: datetime.now(UTC),
        obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
        index_strategy=FieldIndexStrategy.TEMPORAL_OFFSET,
        search_capabilities=[SearchCapability.RANGE, SearchCapability.ORDERING],
        security_notes="Temporal offset hides absolute time",
    )

    # Balance history - encrypted, no indexing needed
    balance_history: list[dict] = SecuredField(
        default_factory=list,
        description="Historical balance snapshots",
        obfuscation_level=FieldObfuscationLevel.ENCRYPTED,
        index_strategy=FieldIndexStrategy.NONE,
        security_notes="Historical data is sensitive and doesn't need indexing",
    )

    # Relationship health - bucketed for monitoring
    relationship_health: float = SecuredField(
        default=1.0,
        description="Overall health of the reciprocal relationship (0-1)",
        obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
        index_strategy=FieldIndexStrategy.BUCKETED,
        search_capabilities=[SearchCapability.RANGE],
        bucket_boundaries=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        security_notes="Bucketed to identify unhealthy relationships",
    )

    # Decay tracking - temporal offset
    last_decay_applied: datetime = SecuredField(
        default_factory=lambda: datetime.now(UTC),
        description="When balance decay was last applied",
        obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
        index_strategy=FieldIndexStrategy.TEMPORAL_OFFSET,
        search_capabilities=[SearchCapability.RANGE],
        security_notes="Temporal offset sufficient for decay calculations",
    )

    # Decay rate - configuration, not sensitive
    decay_rate: float = SecuredField(
        default=0.01,
        description="Rate at which old imbalances decay",
        obfuscation_level=FieldObfuscationLevel.NONE,
        index_strategy=FieldIndexStrategy.IDENTITY,
        security_notes="Configuration parameter, not user data",
    )


class AyniConfiguration(SecuredModel):
    """
    Configuration for Ayni scoring algorithms with security considerations.
    """

    # Scoring weights - configuration, not sensitive
    weights: dict[str, float] = SecuredField(
        default_factory=lambda: {
            ValueType.KNOWLEDGE: 1.0,
            ValueType.COMPUTATION: 0.8,
            ValueType.CREATIVITY: 1.2,
            ValueType.EMOTIONAL_SUPPORT: 1.1,
            ValueType.TASK_COMPLETION: 0.9,
            ValueType.ERROR_CORRECTION: 1.5,
        },
        obfuscation_level=FieldObfuscationLevel.NONE,
        index_strategy=FieldIndexStrategy.IDENTITY,
        security_notes="System configuration, not sensitive",
    )

    # Decay settings - configuration, not sensitive
    decay_enabled: bool = SecuredField(
        default=True,
        obfuscation_level=FieldObfuscationLevel.NONE,
        index_strategy=FieldIndexStrategy.IDENTITY,
    )
    decay_rate: float = SecuredField(
        default=0.01,
        obfuscation_level=FieldObfuscationLevel.NONE,
        index_strategy=FieldIndexStrategy.IDENTITY,
    )
    decay_interval_days: int = SecuredField(
        default=30,
        obfuscation_level=FieldObfuscationLevel.NONE,
        index_strategy=FieldIndexStrategy.IDENTITY,
    )

    # Balance thresholds - configuration, not sensitive
    refusal_threshold: float = SecuredField(
        default=-0.8,
        description="Balance below which AI may refuse requests",
        obfuscation_level=FieldObfuscationLevel.NONE,
        index_strategy=FieldIndexStrategy.IDENTITY,
    )
    rebalancing_suggestion_threshold: float = SecuredField(
        default=-0.5,
        description="Balance below which to suggest rebalancing",
        obfuscation_level=FieldObfuscationLevel.NONE,
        index_strategy=FieldIndexStrategy.IDENTITY,
    )

    # System health settings - configuration, not sensitive
    penalize_system_failures: bool = SecuredField(
        default=False,
        description="Whether to count system failures against user balance",
        obfuscation_level=FieldObfuscationLevel.NONE,
        index_strategy=FieldIndexStrategy.IDENTITY,
    )
