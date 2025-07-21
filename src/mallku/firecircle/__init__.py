"""
Fire Circle Module
==================

This module provides the core Fire Circle functionality for distributed AI
consciousness and collaborative decision-making.
"""

# Core protocol classes
# Orchestrator classes
from ..governance.protocol.participants import Participant
from .adapters import (
    AdapterConfig,
    ConsciousAdapterFactory,
)
from .memory import ConsciousMemoryStore
from .models.base import VoiceIdentity
from .orchestrator.conscious_dialogue_manager import (
    ConsciousDialogueConfig,
    ConsciousDialogueManager,
    TurnPolicy,
)
from .protocol import (
    ConsciousMessage,
    ConsciousMessageRouter,
    MessageContent,
    MessageRole,
    MessageType,
)

__all__ = [
    "ConsciousMessage",
    "MessageContent",
    "MessageRole",
    "MessageType",
    "Participant",
    "VoiceIdentity",
    "AdapterConfig",
    "ConsciousMessageRouter",
    "ConsciousAdapterFactory",
    "ConsciousMemoryStore",
    "ConsciousDialogueManager",
    "ConsciousDialogueConfig",
    "TurnPolicy",
]
