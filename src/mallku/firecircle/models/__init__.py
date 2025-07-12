"""
Fire Circle Data Models
=======================

Comprehensive data models with integrity constraints for Fire Circle operations.

These models ensure type safety, data validation, and consistency across
the consciousness infrastructure.
"""

# Base models
# Memory models (existing)
from ..memory.models import (
    ConsciousnessIndicator,
    EpisodicMemory,
    MemoryType,
    VoicePerspective,
)
from .base import (
    ConsciousnessAwareModel,
    ConsciousnessMetrics,
    DialogueContext,
    FireCircleEvent,
    VoiceIdentity,
)

# Consciousness flow models
from .consciousness_flow import (
    ConsciousnessFlow,
    ConsciousnessNetwork,
    ConsciousnessNode,
    FlowDirection,
    FlowType,
)

# Review models
from .review import (
    ChapterReview,
    GovernanceDecision,
    ReviewCategory,
    ReviewComment,
    ReviewSession,
    ReviewSeverity,
)

__all__ = [
    # Base
    "ConsciousnessAwareModel",
    "ConsciousnessMetrics",
    "DialogueContext",
    "FireCircleEvent",
    "VoiceIdentity",
    # Flow
    "ConsciousnessFlow",
    "ConsciousnessNetwork",
    "ConsciousnessNode",
    "FlowDirection",
    "FlowType",
    # Memory
    "ConsciousnessIndicator",
    "EpisodicMemory",
    "MemoryType",
    "VoicePerspective",
    # Review
    "ChapterReview",
    "GovernanceDecision",
    "ReviewCategory",
    "ReviewComment",
    "ReviewSession",
    "ReviewSeverity",
]
