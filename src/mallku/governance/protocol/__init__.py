"""
Protocol Layer - Defining the structure of governance dialogues

This layer establishes how AI models communicate in Fire Circle councils,
track consensus states, and manage participant identities.
"""

from .message import GovernanceMessage, MessageType, MessageMetadata
from .consensus import ConsensusState, ConsensusTransition
from .participants import ParticipantRole, Participant, ParticipantRegistry

__all__ = [
    # Message structures
    "GovernanceMessage",
    "MessageType", 
    "MessageMetadata",
    
    # Consensus mechanisms
    "ConsensusState",
    "ConsensusTransition",
    
    # Participant management
    "ParticipantRole",
    "Participant",
    "ParticipantRegistry",
]
