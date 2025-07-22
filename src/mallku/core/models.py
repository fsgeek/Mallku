from datetime import UTC, datetime

from pydantic import BaseModel, Field, field_validator


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


class ModelConfig(BaseModel):
    """A base model with a reusable config."""

    class Config:
        """Pydantic config."""

        extra = "forbid"
        use_enum_values = True
        arbitrary_types_allowed = True
