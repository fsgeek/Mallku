"""
Protocol Layer - Defining the structure of governance dialogues

This layer establishes how AI models communicate in Fire Circle councils,
track consensus states, and manage participant identities.
"""

from .message import GovernanceMessage, MessageType, MessageMetadata, create_governance_message
from .consensus import ConsensusState, ConsensusTransition, ConsensusTracker, ConsensusMetrics
from .participants import (
    ParticipantRole, 
    Participant, 
    ParticipantRegistry,
    create_diverse_council
)

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
    "ConsensusMetrics",
    
    # Participant management
    "ParticipantRole",
    "Participant",
    "ParticipantRegistry",
    "create_diverse_council",
]
