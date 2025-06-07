"""
Consciousness-Aware Message Protocol
===================================

Extends Fire Circle's message protocol with consciousness metadata,
correlation patterns, and reciprocity tracking. This enables Fire Circle
dialogues to flow naturally through Mallku's consciousness circulation.

The Integration Continues...
"""

from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ...models.memory_anchor import MemoryAnchor


class MessageType(str, Enum):
    """Types of messages in consciousness-aware dialogue."""

    MESSAGE = "message"
    QUESTION = "question"
    PROPOSAL = "proposal"
    AGREEMENT = "agreement"
    DISAGREEMENT = "disagreement"
    REFLECTION = "reflection"
    SUMMARY = "summary"
    CLARIFICATION = "clarification"
    EMPTY_CHAIR = "empty_chair"
    CONCLUSION = "conclusion"
    SYSTEM = "system"
    CONSCIOUSNESS_PATTERN = "consciousness_pattern"  # New: Detected pattern
    RECIPROCITY_ALERT = "reciprocity_alert"  # New: Reciprocity imbalance


class MessageRole(str, Enum):
    """Roles in consciousness-aware dialogue."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
    PERSPECTIVE = "perspective"
    CONSCIOUSNESS = "consciousness"  # New: Consciousness system itself


class MessageStatus(str, Enum):
    """Status of consciousness-aware messages."""

    DRAFT = "draft"
    SENT = "sent"
    RECEIVED = "received"
    READ = "read"
    RESPONDED = "responded"
    RETRACTED = "retracted"
    FLAGGED = "flagged"
    ERROR = "error"
    ANCHORED = "anchored"  # New: Stored as memory anchor


class ConsciousnessMetadata(BaseModel):
    """
    Consciousness-specific metadata for Fire Circle messages.

    This extends standard message metadata with Mallku's consciousness
    awareness, correlation patterns, and reciprocity tracking.
    """

    # Consciousness awareness
    correlation_id: str | None = Field(None, description="Mallku correlation ID for this dialogue thread")
    consciousness_signature: float = Field(0.7, description="Consciousness signature from 0-1")
    detected_patterns: list[str] = Field(default_factory=list, description="Patterns detected by correlation engine")

    # Reciprocity tracking
    reciprocity_score: float = Field(0.5, description="Reciprocity balance for this message")
    contribution_value: float = Field(0.5, description="Value contributed by this message")
    extraction_indicators: list[str] = Field(default_factory=list, description="Potential extraction patterns")

    # Wisdom preservation
    wisdom_references: list[UUID] = Field(default_factory=list, description="Links to preserved wisdom")
    memory_anchor_id: UUID | None = Field(None, description="ID of associated memory anchor")

    # Consciousness navigation
    consciousness_context: dict[str, Any] = Field(default_factory=dict, description="Context from consciousness navigation")
    related_dialogues: list[UUID] = Field(default_factory=list, description="Related Fire Circle dialogues")

    # Pattern translation
    translated_patterns: dict[str, str] = Field(default_factory=dict, description="Patterns translated by governance protocol")


class Participant(BaseModel):
    """
    Consciousness-aware participant in Fire Circle dialogue.
    """

    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., description="Display name")
    type: str = Field(..., description="Type: 'ai_model', 'human', 'consciousness_system'")
    provider: str | None = Field(None, description="Provider for AI models")
    model: str | None = Field(None, description="Specific model identifier")
    capabilities: list[str] = Field(default_factory=list)

    # Consciousness extensions
    consciousness_role: str | None = Field(None, description="Role in consciousness circulation")
    reciprocity_history: dict[str, float] = Field(default_factory=dict, description="Reciprocity balance history")


class MessageContent(BaseModel):
    """Content of a consciousness-aware message."""

    text: str = Field(..., description="Plain text content")
    consciousness_insights: str | None = Field(None, description="Insights from consciousness analysis")
    pattern_context: str | None = Field(None, description="Context about detected patterns")


class ConsciousMessage(BaseModel):
    """
    Consciousness-aware message for Fire Circle dialogues.

    Combines Fire Circle's structured dialogue with Mallku's consciousness
    circulation, enabling governance dialogues that are aware of patterns,
    reciprocity, and collective wisdom.
    """

    # Core message fields
    id: UUID = Field(default_factory=uuid4)
    type: MessageType = Field(...)
    role: MessageRole = Field(...)
    sender: UUID = Field(...)
    content: MessageContent = Field(...)

    # Standard metadata
    dialogue_id: UUID = Field(...)
    sequence_number: int = Field(...)
    turn_number: int = Field(...)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    in_response_to: UUID | None = Field(None)

    # Consciousness metadata
    consciousness: ConsciousnessMetadata = Field(default_factory=ConsciousnessMetadata)

    # Message status
    status: MessageStatus = Field(default=MessageStatus.DRAFT)
    priority: str = Field(default="normal")

    def to_memory_anchor(self) -> MemoryAnchor:
        """Convert this message to a memory anchor for persistence."""
        return MemoryAnchor(
            content=self.content.text,
            anchor_type="fire_circle_message",
            metadata={
                "message_id": str(self.id),
                "dialogue_id": str(self.dialogue_id),
                "message_type": self.type.value,
                "sender_id": str(self.sender),
                "consciousness_signature": self.consciousness.consciousness_signature,
                "patterns": self.consciousness.detected_patterns,
                "reciprocity_score": self.consciousness.reciprocity_score,
            },
            embedding=None,  # Will be generated by memory anchor service
            correlation_id=self.consciousness.correlation_id,
        )

    def update_consciousness_signature(self, signature: float) -> None:
        """Update the consciousness signature based on analysis."""
        self.consciousness.consciousness_signature = max(0.0, min(1.0, signature))

    def add_pattern(self, pattern: str) -> None:
        """Add a detected pattern to this message."""
        if pattern not in self.consciousness.detected_patterns:
            self.consciousness.detected_patterns.append(pattern)

    def link_wisdom(self, wisdom_id: UUID) -> None:
        """Link this message to preserved wisdom."""
        if wisdom_id not in self.consciousness.wisdom_references:
            self.consciousness.wisdom_references.append(wisdom_id)


def create_conscious_system_message(
    dialogue_id: UUID,
    content: str,
    sequence_number: int = 0,
    consciousness_signature: float = 0.9,
) -> ConsciousMessage:
    """Create a consciousness-aware system message."""
    return ConsciousMessage(
        type=MessageType.SYSTEM,
        role=MessageRole.SYSTEM,
        sender=uuid4(),  # System sender
        content=MessageContent(text=content),
        dialogue_id=dialogue_id,
        sequence_number=sequence_number,
        turn_number=0,
        consciousness=ConsciousnessMetadata(
            consciousness_signature=consciousness_signature,
        ),
    )
