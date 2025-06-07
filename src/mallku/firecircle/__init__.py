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

# Memory layer
from .memory import ConsciousMemoryStore

# Orchestration layer
from .orchestrator import (
    ConsciousDialogueConfig,
    ConsciousDialogueManager,
    DialoguePhase,
    TurnPolicy,
)
from .protocol import (
    ConsciousMessage,
    ConsciousnessMetadata,
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
    # Memory
    "ConsciousMemoryStore",
    # Adapters
    "ConsciousModelAdapter",
    "AdapterConfig",
    "ConsciousAdapterFactory",
    # Router
    "ConsciousMessageRouter",
]
