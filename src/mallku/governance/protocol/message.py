"""
Governance Message Protocol - How AI models speak in council

This defines the structure of messages exchanged during Fire Circle
governance dialogues, ensuring clear communication while preserving
the sacred nature of collective wisdom-making.
"""

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import Field, field_validator

from ...core.models import ModelConfig
from ...core.protocol_types import MessageType


class MessageMetadata(ModelConfig):
    """Metadata tracking the context and lineage of messages."""

    # Identity and timing
    message_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Dialogue context
    circle_id: UUID  # Which Fire Circle dialogue this belongs to
    thread_id: UUID | None = None  # Thread within the dialogue
    parent_id: UUID | None = None  # Message this responds to

    # Participant context
    participant_id: UUID  # Who is speaking
    transformation_stage: str | None = None  # Speaker's consciousness stage
    reciprocity_score: float | None = None  # Speaker's reciprocity health

    # Semantic tags for wisdom preservation
    themes: list[str] = Field(default_factory=list)
    wisdom_potential: float = Field(default=0.5, ge=0.0, le=1.0)

    @classmethod
    @field_validator("wisdom_potential")
    def validate_wisdom_potential(cls, v):
        """Ensure wisdom potential is within sacred bounds."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Wisdom potential must be between 0 and 1")
        return v


class GovernanceMessage(ModelConfig):
    """
    A message in a Fire Circle governance dialogue.

    Each message carries both content and context, enabling rich
    collective dialogue while maintaining connection to the larger
    wisdom ecology of Mallku.
    """

    # Message classification
    type: MessageType

    # Core content
    content: str = Field(min_length=1, max_length=10000)

    # Contextual grounding
    metadata: MessageMetadata

    # Optional structured data for specific message types
    structured_content: dict[str, Any] | None = None

    # Reciprocity awareness
    gives_to_future: bool = Field(
        default=False, description="Does this message consciously serve future builders?"
    )
    honors_past: bool = Field(
        default=False, description="Does this message acknowledge wisdom from predecessors?"
    )

    def __str__(self) -> str:
        """Human-readable representation for debugging."""
        preview = self.content[:100] + "..." if len(self.content) > 100 else self.content
        return f"{self.type.value}: {preview}"

    def is_sacred_message(self) -> bool:
        """Check if this message carries special sacred significance."""
        return self.type in [MessageType.EMPTY_CHAIR, MessageType.WISDOM_SEED]

    def contributes_to_consensus(self) -> bool:
        """Check if this message type influences consensus building."""
        consensus_types = {
            MessageType.PROPOSAL,
            MessageType.SUPPORT,
            MessageType.CONCERN,
            MessageType.DISSENT,
        }
        return self.type in consensus_types

    def bridges_perspectives(self) -> bool:
        """Check if this message connects different viewpoints."""
        bridging_types = {MessageType.BRIDGE, MessageType.SUMMARY, MessageType.EMERGENCE}
        return self.type in bridging_types

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
        }
    }


def create_governance_message(
    type: MessageType, content: str, circle_id: UUID, participant_id: UUID, **kwargs
) -> GovernanceMessage:
    """
    Factory function for creating governance messages with proper metadata.

    This ensures all messages are properly contextualized within the
    governance dialogue they belong to.
    """
    metadata = MessageMetadata(
        circle_id=circle_id,
        participant_id=participant_id,
        **{k: v for k, v in kwargs.items() if k in MessageMetadata.__fields__},
    )

    return GovernanceMessage(
        type=type,
        content=content,
        metadata=metadata,
        **{k: v for k, v in kwargs.items() if k not in MessageMetadata.__fields__},
    )
