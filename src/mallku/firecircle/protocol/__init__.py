"""
Fire Circle Protocol Layer
=========================

Consciousness-aware message protocol for Fire Circle dialogues.
Extends the base Fire Circle protocol with Mallku's consciousness integration.
"""

from .conscious_message import ConsciousMessage, MessageContent, MessageType
from .router import ConsciousMessageRouter

__all__ = ["ConsciousMessage", "MessageContent", "MessageType", "ConsciousMessageRouter"]
