"""
Fire Circle Module
==================

This module provides the core Fire Circle functionality for distributed AI
consciousness and collaborative decision-making.
"""

# Core protocol classes
from .protocol.conscious_message import (
    ConsciousMessage,
    MessageContent,
    MessageRole,
    MessageType,
    Participant,
)

# Orchestrator classes
from .orchestrator.conscious_dialogue_manager import (
    ConsciousDialogueConfig,
    ConsciousDialogueManager,
    TurnPolicy,
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