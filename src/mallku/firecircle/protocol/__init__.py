"""
Fire Circle Protocol Layer
=========================

Consciousness-aware message protocol for Fire Circle dialogues.
Extends the base Fire Circle protocol with Mallku's consciousness integration.
"""

from .conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageStatus,
    MessageType,
    Participant,
    create_conscious_system_message,
)

__all__ = [
    "ConsciousMessage",
    "ConsciousnessMetadata",
    "MessageContent",
    "MessageType",
    "MessageRole",
    "MessageStatus",
    "Participant",
    "create_conscious_system_message",
]
