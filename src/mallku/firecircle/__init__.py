"""
Fire Circle Module
==================

This module provides the core Fire Circle functionality for distributed AI
consciousness and collaborative decision-making.
"""

# Core protocol classes
# Orchestrator classes
from ..governance.protocol.participants import Participant
from .orchestrator.conscious_dialogue_manager import (
    ConsciousDialogueConfig,
    ConsciousDialogueManager,
    TurnPolicy,
)
from .protocol.conscious_message import (
    ConsciousMessage,
    MessageContent,
    MessageRole,
    MessageType,
)

__all__ = [
    # Protocol classes
    "ConsciousMessage",
    "MessageContent",
    "MessageRole",
    "MessageType",
    "Participant",
    # Orchestrator classes
    "ConsciousDialogueConfig",
    "ConsciousDialogueManager",
    "TurnPolicy",
]
