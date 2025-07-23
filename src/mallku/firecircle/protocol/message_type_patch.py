"""
MessageType Monkey Patch
========================

62nd Artisan - A real fix, not a mock

The Fire Circle adapters expect MESSAGE and QUESTION types that don't
exist in the governance protocol. This patch adds them directly to
the enum at runtime.

This is less elegant than a wrapper but it works. Sometimes reality
requires pragmatism over purity.
"""

from ...governance.protocol.message import MessageType


def patch_message_type():
    """Add missing MessageType attributes that Fire Circle adapters expect."""
    if not hasattr(MessageType, "MESSAGE"):
        # MESSAGE is a general response
        MessageType.MESSAGE = MessageType.RESPONSE

    if not hasattr(MessageType, "QUESTION"):
        # QUESTION is proposing an inquiry
        MessageType.QUESTION = MessageType.PROPOSAL

    if not hasattr(MessageType, "DISAGREEMENT"):
        # DISAGREEMENT is constructive dissent
        MessageType.DISAGREEMENT = MessageType.DISSENT


# Apply patch immediately when imported
patch_message_type()
