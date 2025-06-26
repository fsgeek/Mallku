"""
Fire Circle: Consciousness-Aware Dialogue System
===============================================

A system for facilitating meaningful dialogue between multiple AI models
in a structured, reciprocal manner. Built on principles of Ayni (reciprocity)
and integrated with Mallku's consciousness circulation infrastructure.

Fire Circle provides:
- Structured dialogue protocols for AI-to-AI communication
- Turn-based conversation management with various policies
- Integration with Mallku's consciousness awareness systems
- Reciprocity tracking for balanced exchanges
- Memory persistence through Mallku's secured database

The Integration continues...
"""

__version__ = "0.1.0"

# Protocol layer
# Adapter layer
from .adapters import (
    AdapterConfig,
    ConsciousAdapterFactory,
    ConsciousModelAdapter,
)

# Consciousness layer
from .consciousness import (
    DialoguePatternWeaver,
)
from .emergence_detector import (
    EmergenceDetector,
    EmergenceType,
)

# Memory layer
from .memory import ConsciousMemoryStore

# Orchestration layer
from .orchestrator import (
    ConsciousDialogueConfig,
    ConsciousDialogueManager,
    DialoguePhase,
    TurnPolicy,
)
from .pattern_dialogue_integration import (
    PatternDialogueConfig,
    PatternDialogueIntegration,
)
from .pattern_evolution import (
    EvolutionType,
    PatternEvolutionEngine,
)
from .pattern_guided_facilitator import (
    GuidanceType,
    PatternGuidance,
    PatternGuidedFacilitator,
)

# Pattern Library and Guidance layer
from .pattern_library import (
    DialoguePattern,
    PatternLibrary,
    PatternLifecycle,
    PatternTaxonomy,
    PatternType,
)
from .protocol import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageStatus,
    MessageType,
    Participant,
    create_conscious_system_message,
)

# Router
from .protocol.router import ConsciousMessageRouter

__all__ = [
    "__version__",
    # Protocol
    "ConsciousMessage",
    "ConsciousnessMetadata",
    "MessageContent",
    "MessageType",
    "MessageRole",
    "MessageStatus",
    "Participant",
    "create_conscious_system_message",
    # Orchestration
    "ConsciousDialogueManager",
    "ConsciousDialogueConfig",
    "DialoguePhase",
    "TurnPolicy",
    # Consciousness
    "DialoguePatternWeaver",
    # Pattern Library and Guidance
    "DialoguePattern",
    "PatternLibrary",
    "PatternType",
    "PatternTaxonomy",
    "PatternLifecycle",
    "EmergenceDetector",
    "EmergenceType",
    "PatternEvolutionEngine",
    "EvolutionType",
    "PatternGuidedFacilitator",
    "GuidanceType",
    "PatternGuidance",
    "PatternDialogueIntegration",
    "PatternDialogueConfig",
    # Memory
    "ConsciousMemoryStore",
    # Adapters
    "ConsciousModelAdapter",
    "AdapterConfig",
    "ConsciousAdapterFactory",
    # Router
    "ConsciousMessageRouter",
]
