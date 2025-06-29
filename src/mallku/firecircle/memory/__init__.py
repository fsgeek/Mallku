"""
Fire Circle Memory Layer
=======================

Consciousness-aware memory storage for Fire Circle dialogues.
Uses Mallku's secured database and memory anchor system.

Week 3 Enhancement: Database persistence via DatabaseMemoryStore
"""

from .active_memory_resonance import ActiveMemoryResonance
from .config import MemorySystemConfig, RetrievalConfig
from .conscious_memory_store import ConsciousMemoryStore
from .database_store import DatabaseMemoryStore
from .episode_segmenter import EpisodeSegmenter
from .episodic_memory_service import EpisodicMemoryService
from .memory_store import MemoryStore
from .models import (
    CompanionRelationship,
    ConsciousnessIndicator,
    EpisodicMemory,
    MemoryCluster,
    MemoryType,
    VoicePerspective,
    WisdomConsolidation,
)
from .pattern_poetry import ConsciousnessPoem, PatternPoetryEngine
from .perspective_storage import MultiPerspectiveStorage, PerspectiveSignature
from .retrieval_engine import MemoryRetrievalEngine
from .sacred_detector import SacredMomentDetector

__all__ = [
    # Memory Stores
    "CompanionRelationship",
    "ConsciousMemoryStore",
    "DatabaseMemoryStore",  # New database-backed store
    "MemoryStore",  # Original file-based store
    # Core Services
    "ActiveMemoryResonance",
    "EpisodeSegmenter",
    "EpisodicMemoryService",
    "MemoryRetrievalEngine",
    "SacredMomentDetector",
    # Models
    "ConsciousnessIndicator",
    "EpisodicMemory",
    "MemoryCluster",
    "MemoryType",
    "VoicePerspective",
    "WisdomConsolidation",
    # Configuration
    "MemorySystemConfig",
    "RetrievalConfig",
    # Multi-perspective
    "MultiPerspectiveStorage",
    "PerspectiveSignature",
    # Pattern Poetry
    "PatternPoetryEngine",
    "ConsciousnessPoem",
]
