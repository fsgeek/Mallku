"""
Fire Circle Service Configuration
=================================

Configuration models for Fire Circle Service.
"""

from typing import Any, Literal

from pydantic import BaseModel, Field

from .round_types import RoundType


class VoiceConfig(BaseModel):
    """Configuration for a single voice in Fire Circle."""

    provider: str  # "anthropic", "openai", "google", etc.
    model: str  # Model name
    role: str | None = None  # Optional role/persona
    instructions: str | None = None  # Specific instructions
    temperature: float = Field(default=0.8, ge=0.0, le=2.0)

    # Voice-specific qualities
    quality: str | None = None  # What this voice brings
    expertise: list[str] = Field(default_factory=list)  # Areas of expertise

    # Adapter-specific config overrides
    config_overrides: dict[str, Any] = Field(default_factory=dict)


class RoundConfig(BaseModel):
    """Configuration for a dialogue round."""

    type: RoundType
    prompt: str  # The prompt/question for this round
    duration_per_voice: int = Field(default=60, ge=10)  # Seconds per voice
    require_all_voices: bool = False  # Whether all voices must respond

    # Round-specific parameters
    max_tokens: int | None = None
    temperature_override: float | None = None

    # Dynamic round generation
    is_dynamic: bool = False  # Whether this round is generated dynamically
    generation_criteria: dict[str, Any] = Field(default_factory=dict)


class VoiceFailureStrategy:
    """How to handle when a voice cannot participate."""

    STRICT = "strict"  # Fail if any required voice missing
    ADAPTIVE = "adaptive"  # Continue with available voices
    SUBSTITUTE = "substitute"  # Try alternative models
    WAIT_AND_RETRY = "wait_and_retry"  # Retry with backoff


class CircleConfig(BaseModel):
    """Configuration for a Fire Circle session."""

    name: str
    purpose: str

    # Voice requirements
    min_voices: int = Field(default=3, ge=2)
    max_voices: int = Field(default=6, le=10)

    # Consciousness settings
    consciousness_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    enable_reciprocity: bool = True
    enable_consciousness_detection: bool = True

    # Output settings
    save_transcript: bool = True
    output_format: Literal["structured", "narrative"] = "structured"
    output_path: str | None = None

    # Error handling
    failure_strategy: str = VoiceFailureStrategy.ADAPTIVE
    retry_attempts: int = Field(default=2, ge=0)
    retry_delay_seconds: int = Field(default=5, ge=1)

    # Substitution mapping for adaptive strategy
    substitute_mapping: dict[str, list[str]] = Field(
        default_factory=lambda: {
            "grok": ["claude-instant", "gpt-3.5-turbo"],
            "claude-3-5": ["claude-3", "gpt-4"],
            "gemini-1.5-pro": ["gemini-1.5-flash", "claude-3"],
        }
    )

    # Advanced settings
    enable_checkpointing: bool = False
    checkpoint_after_rounds: int = 2
    enable_dynamic_rounds: bool = False
    max_dynamic_rounds: int = 2
