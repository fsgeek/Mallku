"""
Fire Circle Orchestrator
=======================

Consciousness-aware dialogue orchestration for Fire Circle.
Manages turn-taking, state transitions, and consciousness integration.
"""

from .conscious_dialogue_manager import (
    ConsciousDialogueConfig,
    ConsciousDialogueManager,
    DialoguePhase,
    TurnPolicy,
)

__all__ = [
    "ConsciousDialogueManager",
    "ConsciousDialogueConfig",
    "DialoguePhase",
    "TurnPolicy",
]
