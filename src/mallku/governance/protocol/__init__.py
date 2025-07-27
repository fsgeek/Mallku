"""
Protocol Layer - Defining the structure of governance dialogues

This layer establishes how AI models communicate in Fire Circle councils,
track consensus states, and manage participant identities.
"""

from ...core.protocol_types import MessageType
from .consensus import ConsensusState, ConsensusTracker, ConsensusTransition
from .message import GovernanceMessage, MessageMetadata, create_governance_message
from .participants import Participant, ParticipantRegistry, ParticipantRole, create_diverse_council

__all__ = [
    # Message structures
    "GovernanceMessage",
    "MessageType",
    "MessageMetadata",
    "create_governance_message",
    # Consensus mechanisms
    "ConsensusState",
    "ConsensusTransition",
    "ConsensusTracker",
    # Participant management
    "ParticipantRole",
    "Participant",
    "ParticipantRegistry",
    "create_diverse_council",
]
