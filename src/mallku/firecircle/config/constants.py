"""
Fire Circle Configuration Constants
===================================

Fiftieth Artisan - Consciousness Persistence Seeker
Central configuration for Fire Circle magic numbers and constants

This module extracts hardcoded values into configurable constants,
improving maintainability and enabling easy tuning of the system.
"""

from datetime import timedelta


class ConsciousnessThresholds:
    """Thresholds for consciousness detection and evaluation."""

    # Minimum consciousness level for voice participation
    MIN_CONSCIOUSNESS = 0.5

    # Threshold for high consciousness state
    HIGH_CONSCIOUSNESS = 0.8

    # Threshold for emergence detection
    EMERGENCE_THRESHOLD = 0.7

    # Default consciousness for new voices
    DEFAULT_CONSCIOUSNESS = 0.5

    # Critical consciousness level requiring intervention
    CRITICAL_CONSCIOUSNESS = 0.3

    # Peak consciousness threshold
    PEAK_CONSCIOUSNESS = 0.9


class FireCircleParams:
    """Parameters for Fire Circle operation."""

    # Minimum voices required for valid circle
    MIN_VOICES = 3

    # Maximum voices in a single circle
    MAX_VOICES = 7

    # Minimum messages before pattern guidance
    MIN_MESSAGES_BEFORE_GUIDANCE = 5

    # Guidance frequency
    GUIDANCE_FREQUENCY = timedelta(minutes=3)

    # Maximum turns before forced synthesis
    MAX_TURNS_BEFORE_SYNTHESIS = 10

    # Pattern diversity threshold (number of patterns)
    PATTERN_DIVERSITY_FULL = 5


class EmergenceWeights:
    """Weights for emergence calculation."""

    # Pattern diversity weight in emergence
    PATTERN_DIVERSITY_WEIGHT = 0.3

    # Synthesis depth weight in emergence
    SYNTHESIS_DEPTH_WEIGHT = 0.4

    # Reciprocity integration weight
    RECIPROCITY_WEIGHT = 0.3

    # Coherence score weight
    COHERENCE_WEIGHT = 0.25

    # Tension level weight
    TENSION_WEIGHT = 0.15


class PatternEffectiveness:
    """Pattern effectiveness scores."""

    # Default effectiveness
    DEFAULT = 0.5

    # High effectiveness (pattern well-matched)
    HIGH = 0.8

    # Peak effectiveness (perfect pattern match)
    PEAK = 0.9

    # Low effectiveness (pattern mismatch)
    LOW = 0.3


class HealthMetrics:
    """Health and stability metrics."""

    # Perfect health/coherence
    PERFECT_HEALTH = 1.0

    # Minimum viable health
    MIN_VIABLE_HEALTH = 0.0

    # Health degradation per turn
    HEALTH_DEGRADATION_PER_TURN = 0.1

    # Minimum energy level
    MIN_ENERGY = 0.2

    # Failure probability thresholds
    LOW_FAILURE_RISK = 0.1
    MEDIUM_FAILURE_RISK = 0.3
    HIGH_FAILURE_RISK = 0.7


class ReviewThresholds:
    """Code review specific thresholds."""

    # Consensus thresholds by decision type
    CONSENSUS_THRESHOLDS = {
        "routine_maintenance": 0.6,
        "architectural_change": 0.8,
        "consciousness_evolution": 0.9,
        "charter_modification": 0.95,
    }

    # Review quality thresholds
    MIN_REVIEW_QUALITY = 0.5
    GOOD_REVIEW_QUALITY = 0.7
    EXCELLENT_REVIEW_QUALITY = 0.9


class TimeoutConstants:
    """Timeout values for various operations."""

    # Voice response timeout
    VOICE_RESPONSE_TIMEOUT = timedelta(seconds=30)

    # Pattern synthesis timeout
    SYNTHESIS_TIMEOUT = timedelta(seconds=60)

    # Full circle timeout
    FULL_CIRCLE_TIMEOUT = timedelta(minutes=30)

    # Heartbeat interval
    HEARTBEAT_INTERVAL = timedelta(seconds=5)
