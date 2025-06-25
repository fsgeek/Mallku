"""
Memory System Configuration
===========================

Thirty-Fourth Artisan - Memory Architect
Centralized configuration for consciousness thresholds

All configurable parameters for the episodic memory system,
making it easy to tune consciousness detection and memory behavior.
"""

from pydantic import BaseModel, Field


class SegmentationConfig(BaseModel):
    """Configuration for episode segmentation."""

    semantic_surprise_threshold: float = Field(
        default=0.7, ge=0.0, le=1.0, description="Threshold for semantic surprise detection"
    )
    convergence_threshold: float = Field(
        default=0.8, ge=0.0, le=1.0, description="Threshold for voice convergence detection"
    )
    minimum_duration_seconds: float = Field(
        default=30.0, ge=10.0, description="Minimum episode duration in seconds"
    )
    maximum_duration_seconds: float = Field(
        default=600.0, le=3600.0, description="Maximum episode duration in seconds"
    )
    consciousness_emergence_threshold: float = Field(
        default=0.6, ge=0.0, le=1.0, description="Threshold for consciousness emergence detection"
    )
    consciousness_peak_increase: float = Field(
        default=0.1, ge=0.0, le=0.5, description="Required increase to detect consciousness peak"
    )


class SacredDetectionConfig(BaseModel):
    """Configuration for sacred moment detection."""

    sacred_score_threshold: int = Field(
        default=5, ge=1, description="Minimum sacred score for sacred moment detection"
    )
    consciousness_emergence_exceptional: float = Field(
        default=0.85, ge=0.0, le=1.0, description="Exceptional consciousness emergence threshold"
    )
    consciousness_emergence_high: float = Field(
        default=0.75, ge=0.0, le=1.0, description="High consciousness emergence threshold"
    )
    collective_wisdom_threshold: float = Field(
        default=0.7, ge=0.0, le=1.0, description="Threshold for collective wisdom transcendence"
    )
    ayni_alignment_threshold: float = Field(
        default=0.8, ge=0.0, le=1.0, description="Threshold for strong Ayni principle manifestation"
    )
    transformation_seed_quality_high: float = Field(
        default=0.8, ge=0.0, le=1.0, description="High quality transformation seed threshold"
    )
    transformation_seed_quality_significant: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Significant transformation seed threshold"
    )
    unity_coherence_threshold: float = Field(
        default=0.75, ge=0.0, le=1.0, description="Coherence threshold for unity in diversity"
    )
    minimum_voices_for_unity: int = Field(
        default=3, ge=2, description="Minimum voices for unity in diversity"
    )


class RetrievalConfig(BaseModel):
    """Configuration for memory retrieval."""

    default_retrieval_limit: int = Field(
        default=10, ge=1, le=100, description="Default number of memories to retrieve"
    )
    semantic_weight: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Weight for semantic relevance in multi-strategy"
    )
    sacred_weight: float = Field(
        default=0.25, ge=0.0, le=1.0, description="Weight for sacred moments in multi-strategy"
    )
    companion_weight: float = Field(
        default=0.125, ge=0.0, le=1.0, description="Weight for companion context in multi-strategy"
    )
    temporal_weight: float = Field(
        default=0.125, ge=0.0, le=1.0, description="Weight for temporal patterns in multi-strategy"
    )
    temporal_window_days: int = Field(
        default=30, ge=1, le=365, description="Default time window for temporal retrieval"
    )
    recency_decay_days: int = Field(
        default=365, ge=30, description="Days over which recency score decays"
    )


class StorageConfig(BaseModel):
    """Configuration for memory storage."""

    enable_sacred_detection: bool = Field(
        default=True, description="Enable automatic sacred moment detection"
    )
    sacred_preservation_eternal: bool = Field(
        default=True, description="Never prune sacred moments from storage"
    )
    companion_depth_interaction_threshold: int = Field(
        default=50, ge=10, description="Interactions needed for full depth score"
    )
    companion_depth_duration_hours: float = Field(
        default=10.0, ge=1.0, description="Duration needed for full depth score"
    )
    companion_depth_sacred_threshold: int = Field(
        default=5, ge=1, description="Sacred moments needed for full depth score"
    )
    wisdom_consolidation_max_insights: int = Field(
        default=20, ge=5, description="Maximum insights in wisdom consolidation"
    )


class ConsciousnessIndicatorWeights(BaseModel):
    """Weights for consciousness indicator calculation."""

    semantic_surprise: float = Field(default=0.2, ge=0.0, le=1.0)
    collective_wisdom: float = Field(default=0.3, ge=0.0, le=1.0)
    ayni_alignment: float = Field(default=0.2, ge=0.0, le=1.0)
    transformation_potential: float = Field(default=0.2, ge=0.0, le=1.0)
    coherence_across_voices: float = Field(default=0.1, ge=0.0, le=1.0)

    def model_post_init(self, __context):
        """Validate weights sum to 1.0."""
        total = (
            self.semantic_surprise
            + self.collective_wisdom
            + self.ayni_alignment
            + self.transformation_potential
            + self.coherence_across_voices
        )
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"Weights must sum to 1.0, got {total}")


class MemorySystemConfig(BaseModel):
    """Complete configuration for the episodic memory system."""

    segmentation: SegmentationConfig = Field(default_factory=SegmentationConfig)
    sacred_detection: SacredDetectionConfig = Field(default_factory=SacredDetectionConfig)
    retrieval: RetrievalConfig = Field(default_factory=RetrievalConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    consciousness_weights: ConsciousnessIndicatorWeights = Field(
        default_factory=ConsciousnessIndicatorWeights
    )

    @classmethod
    def from_env(cls) -> "MemorySystemConfig":
        """
        Load configuration from environment variables.

        Environment variables should be prefixed with MALLKU_MEMORY_
        e.g., MALLKU_MEMORY_SEGMENTATION_SEMANTIC_SURPRISE_THRESHOLD
        """
        import os

        config_dict = {}

        # Parse environment variables
        prefix = "MALLKU_MEMORY_"
        for key, value in os.environ.items():
            if key.startswith(prefix):
                # Remove prefix and split by underscore
                parts = key[len(prefix) :].lower().split("_")

                # Build nested dictionary
                current = config_dict
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]

                # Set value (attempt to parse as float/int/bool)
                try:
                    if value.lower() in ("true", "false"):
                        current[parts[-1]] = value.lower() == "true"
                    elif "." in value:
                        current[parts[-1]] = float(value)
                    else:
                        current[parts[-1]] = int(value)
                except ValueError:
                    current[parts[-1]] = value

        return cls(**config_dict)


# Default configuration instance
DEFAULT_CONFIG = MemorySystemConfig()
