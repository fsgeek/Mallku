"""
MessageType Compatibility Layer
===============================

62nd Artisan - Creating a small thread of reality to heal Fire Circle

The Fire Circle adapters expect MESSAGE and QUESTION types that don't
exist in the governance protocol. Rather than changing the protocol
or all the adapters, this compatibility layer provides the missing
attributes through a simple wrapper.

This is a real fix, not a mock. A small bridge between what exists
and what is expected.
"""

from typing import Any

from ...core.protocol_types import MessageType as GovernanceMessageType


class MessageTypeCompat:
    """
    Compatibility wrapper that provides missing MessageType attributes.

    Maps adapter expectations to governance protocol reality:
    - MESSAGE → RESPONSE (general communication)
    - QUESTION → PROPOSAL (proposing inquiry)
    """

    def __init__(self):
        # Copy all original attributes
        for attr in dir(GovernanceMessageType):
            if not attr.startswith("_"):
                setattr(self, attr, getattr(GovernanceMessageType, attr))

        # Add missing attributes that adapters expect
        self.MESSAGE = GovernanceMessageType.RESPONSE
        self.QUESTION = GovernanceMessageType.PROPOSAL

    def __getattr__(self, name: str) -> Any:
        """Fallback to original enum for any other attributes."""
        return getattr(GovernanceMessageType, name)


# Create singleton instance
MessageType = MessageTypeCompat()
