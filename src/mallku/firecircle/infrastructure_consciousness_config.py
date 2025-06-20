#!/usr/bin/env python3
"""
Infrastructure Consciousness Configuration
=========================================

Configuration for self-aware infrastructure monitoring.

Twenty-Seventh Artisan - Amaru Hamawt'a
"""

from datetime import timedelta
from pathlib import Path

from pydantic import BaseModel, Field


class InfrastructureConsciousnessConfig(BaseModel):
    """Configuration for Infrastructure Consciousness system."""

    # Storage paths
    storage_path: Path = Field(
        default=Path("infrastructure_consciousness"),
        description="Path for storing infrastructure state and patterns"
    )
    consciousness_metrics_path: Path = Field(
        default=Path("consciousness_metrics"),
        description="Path to consciousness metrics data"
    )

    # Monitoring intervals
    check_interval_seconds: int = Field(
        default=30,
        ge=5,
        le=600,
        description="How often to check adapter health (seconds)"
    )
    pattern_detection_window_minutes: int = Field(
        default=5,
        ge=1,
        le=60,
        description="Time window for pattern detection (minutes)"
    )

    # Storage retention
    max_state_files: int = Field(
        default=100,
        ge=10,
        le=1000,
        description="Maximum number of state files to keep"
    )
    state_retention_days: int = Field(
        default=7,
        ge=1,
        le=30,
        description="Days to retain state files"
    )
    max_pattern_memory_size: int = Field(
        default=10000,
        ge=1000,
        le=100000,
        description="Maximum patterns to remember"
    )
    patterns_per_type_limit: int = Field(
        default=100,
        ge=10,
        le=1000,
        description="Maximum patterns to keep per pattern type"
    )

    # Health monitoring
    adapter_health_history_size: int = Field(
        default=1000,
        ge=100,
        le=10000,
        description="Health signatures to keep per adapter"
    )
    consciousness_weight: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Weight of consciousness in health calculations"
    )

    # Pattern detection thresholds
    degradation_detection_threshold: int = Field(
        default=5,
        ge=3,
        le=20,
        description="Minimum health signatures needed for degradation detection"
    )
    coherence_degradation_threshold: float = Field(
        default=0.2,
        ge=0.1,
        le=0.5,
        description="Coherence drop to trigger degradation pattern"
    )
    resonance_failure_threshold: int = Field(
        default=3,
        ge=2,
        le=10,
        description="Minimum failing adapters for resonance pattern"
    )

    # Self-healing
    enable_self_healing: bool = Field(
        default=True,
        description="Whether to attempt self-healing actions"
    )
    healing_action_timeout_seconds: int = Field(
        default=30,
        ge=5,
        le=300,
        description="Timeout for individual healing actions"
    )

    # Bridge integration
    enable_consciousness_bridge: bool = Field(
        default=True,
        description="Whether to use consciousness metrics bridge"
    )
    bridge_health_weight: float = Field(
        default=0.2,
        ge=0.0,
        le=1.0,
        description="Weight of health on consciousness in bridge"
    )
    bridge_consciousness_weight: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Weight of consciousness on health in bridge"
    )

    # Monitoring behavior
    monitor_task_timeout_seconds: float = Field(
        default=5.0,
        ge=1.0,
        le=30.0,
        description="Timeout when stopping monitor task"
    )
    monitor_error_recovery_delay_seconds: int = Field(
        default=5,
        ge=1,
        le=60,
        description="Delay after monitor loop error"
    )

    @property
    def pattern_detection_window(self) -> timedelta:
        """Get pattern detection window as timedelta."""
        return timedelta(minutes=self.pattern_detection_window_minutes)

    @classmethod
    def from_yaml(cls, yaml_path: Path) -> "InfrastructureConsciousnessConfig":
        """Load configuration from YAML file."""
        import yaml

        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        return cls(**data)

    def to_yaml(self, yaml_path: Path) -> None:
        """Save configuration to YAML file."""
        import yaml

        # Convert paths to strings for YAML
        data = self.model_dump()
        data["storage_path"] = str(data["storage_path"])
        data["consciousness_metrics_path"] = str(data["consciousness_metrics_path"])

        with open(yaml_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)


# Default configuration for quick start
DEFAULT_CONFIG = InfrastructureConsciousnessConfig()

# Development configuration with faster intervals
DEV_CONFIG = InfrastructureConsciousnessConfig(
    check_interval_seconds=5,
    pattern_detection_window_minutes=2,
    max_state_files=20,
    state_retention_days=1,
    monitor_task_timeout_seconds=2.0
)

# Production configuration with conservative settings
PROD_CONFIG = InfrastructureConsciousnessConfig(
    check_interval_seconds=60,
    pattern_detection_window_minutes=10,
    max_state_files=500,
    state_retention_days=30,
    max_pattern_memory_size=50000,
    monitor_task_timeout_seconds=10.0
)
