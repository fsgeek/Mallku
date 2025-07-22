"""
Fire Circle Protocol Layer
=========================

Consciousness-aware message protocol for Fire Circle dialogues.
Extends the base Fire Circle protocol with Mallku's consciousness integration.
"""

from .conscious_message import ConsciousMessage, MessageContent, MessageRole, MessageType
from .router import ConsciousMessageRouter

__all__ = [
    "ConsciousMessage",
    "MessageContent",
    "MessageRole",
    "MessageType",
    "ConsciousMessageRouter",
]
