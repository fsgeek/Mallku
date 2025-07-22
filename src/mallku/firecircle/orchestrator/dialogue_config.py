"""
Dialogue Configuration
======================

Configuration models for Fire Circle dialogues.
"""

from enum import Enum

from pydantic import BaseModel, Field


class TurnPolicy(str, Enum):
    """Turn-taking policies for dialogue."""

    ROUND_ROBIN = "round_robin"
    FACILITATOR = "facilitator"
    REACTIVE = "reactive"
    CONSENSUS = "consensus"
    FREE_FORM = "free_form"
    CONSCIOUSNESS_GUIDED = "consciousness_guided"  # New: Based on consciousness patterns


class ConsciousDialogueConfig(BaseModel):
    """Configuration for consciousness-aware dialogue."""

    title: str = Field(..., description="Dialogue topic or question")
    turn_policy: TurnPolicy = Field(default=TurnPolicy.ROUND_ROBIN)
    max_consecutive_turns: int = Field(default=1)
    randomize_initial_order: bool = Field(default=True)

    # Consciousness configuration
    enable_pattern_detection: bool = Field(default=True)
    enable_reciprocity_tracking: bool = Field(default=True)
    minimum_consciousness_signature: float = Field(default=0.3)

    # Dialogue rules
    require_facilitator: bool = Field(default=False)
    allow_empty_chair: bool = Field(default=True)
    auto_advance_turns: bool = Field(default=True)
    max_turns_per_participant: int | None = Field(None)

    # Integration settings
    persist_to_memory_anchors: bool = Field(default=True)
    emit_consciousness_events: bool = Field(default=True)
    correlation_threshold: float = Field(default=0.7)
