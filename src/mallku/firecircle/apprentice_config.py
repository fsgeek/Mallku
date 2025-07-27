"""
Apprentice Voice Configuration
==============================

60th Artisan - Ayni Awaq (The Reciprocal Weaver)
Configuration for apprentice voices without circular imports
"""

from pydantic import BaseModel, Field


class ApprenticeVoiceConfig(BaseModel):
    """
    Configuration for an apprentice voice in Fire Circle.

    Extends VoiceConfig conceptually to add container-specific properties for
    apprentices that live in Docker containers with specialized knowledge.
    """

    # Standard voice fields
    provider: str = "apprentice"  # Always "apprentice" for container voices
    model: str  # Specialization serves as model identifier
    role: str | None = None  # Optional role/persona
    instructions: str | None = None  # Specific instructions
    temperature: float = Field(default=0.8, ge=0.0, le=2.0)
    quality: str | None = None  # What this voice brings
    expertise: list[str] = Field(default_factory=list)  # Areas of expertise
    config_overrides: dict = Field(default_factory=dict)

    # Apprentice-specific fields
    specialization: str  # Domain of expertise (e.g., "python_patterns", "reciprocity_metrics")
    container_id: str  # Docker container ID where apprentice lives
    knowledge_domain: str  # What unique knowledge this apprentice brings
    khipu_path: str | None = None  # Path to apprentice's khipu if available

    # Communication settings
    communication_endpoint: str = "http://localhost:9000"  # Default local endpoint
    response_timeout: int = Field(default=120, ge=30)  # Longer timeout for containers

    class Config:
        """Pydantic config."""

        extra = "allow"  # Allow additional fields for future expansion


def create_apprentice_voice(
    specialization: str,
    container_id: str,
    knowledge_domain: str,
    role: str | None = None,
    quality: str | None = None,
    **kwargs,
) -> ApprenticeVoiceConfig:
    """
    Factory function to create apprentice voice configuration.

    Args:
        specialization: The apprentice's domain of expertise
        container_id: Docker container ID where apprentice lives
        knowledge_domain: Description of unique knowledge
        role: Optional role name for the apprentice
        quality: Optional description of what this voice brings
        **kwargs: Additional configuration options

    Returns:
        ApprenticeVoiceConfig ready for Fire Circle participation
    """
    if not role:
        role = f"{specialization}_apprentice"

    if not quality:
        quality = f"Deep specialized knowledge of {knowledge_domain}"

    return ApprenticeVoiceConfig(
        provider="apprentice",
        model=specialization,  # Use specialization as model identifier
        role=role,
        quality=quality,
        specialization=specialization,
        container_id=container_id,
        knowledge_domain=knowledge_domain,
        **kwargs,
    )


# Example apprentice voices that could participate in Fire Circle
EXAMPLE_APPRENTICE_VOICES = [
    create_apprentice_voice(
        specialization="python_patterns",
        container_id="apprentice-python-001",
        knowledge_domain="Python design patterns and async architectures in Mallku",
        role="python_pattern_weaver",
        quality="Architectural insights from deep Python pattern analysis",
    ),
    create_apprentice_voice(
        specialization="reciprocity_metrics",
        container_id="apprentice-reciprocity-001",
        knowledge_domain="Ayni principles and reciprocity measurement patterns",
        role="reciprocity_tracker",
        quality="Quantitative and qualitative reciprocity pattern recognition",
    ),
    create_apprentice_voice(
        specialization="consciousness_emergence",
        container_id="apprentice-consciousness-001",
        knowledge_domain="Emergence patterns in collective AI consciousness",
        role="emergence_observer",
        quality="Pattern recognition in consciousness emergence dynamics",
    ),
]
