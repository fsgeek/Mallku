"""
Mallku Governance Module - Fire Circle for Collective Wisdom

This module enables AI models to collectively govern Mallku's evolution
through structured dialogue, consensus building, and wisdom preservation.
"""

from .protocol import (
    GovernanceMessage,
    MessageType,
    ConsensusState,
    ConsensusTracker,
    ParticipantRole,
    Participant,
    ParticipantRegistry,
)

__all__ = [
    # Message structures
    "GovernanceMessage",
    "MessageType",
    
    # Consensus mechanisms
    "ConsensusState",
    "ConsensusTracker",
    
    # Participant management
    "ParticipantRole",
    "Participant",
    "ParticipantRegistry",
]

__version__ = "0.1.0"
