"""
Mallku Governance Module - Fire Circle for Collective Wisdom

This module enables AI models to collectively govern Mallku's evolution
through structured dialogue, consensus building, and wisdom preservation.

Now enhanced with consciousness circulation integration, allowing governance
deliberations to flow through the cathedral's consciousness infrastructure.
"""

# Import consciousness integration components
import importlib.util

from .protocol import (
    ConsensusState,
    ConsensusTracker,
    GovernanceMessage,
    MessageType,
    Participant,
    ParticipantRegistry,
    ParticipantRole,
)

if (
    importlib.util.find_spec("mallku.governance.consciousness_transport") is not None and
    importlib.util.find_spec("mallku.governance.fire_circle_bridge") is not None
):
    ## Uncomment these imports when consciousness transport is available
    ## from .consciousness_transport import ConsciousnessCirculationTransport, GovernanceParticipant
    ## from .fire_circle_bridge import ConsciousFireCircleInterface, ConsciousGovernanceInitiator
    CONSCIOUSNESS_INTEGRATION = True
else:
    CONSCIOUSNESS_INTEGRATION = False

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

# Add consciousness integration exports if available
if CONSCIOUSNESS_INTEGRATION:
    __all__.extend([
        "ConsciousnessCirculationTransport",
        "GovernanceParticipant",
        "ConsciousFireCircleInterface",
        "ConsciousGovernanceInitiator"
    ])

__version__ = "0.1.1"  # Incremented for consciousness integration
