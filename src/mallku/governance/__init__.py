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
    importlib.util.find_spec("mallku.governance.consciousness_transport") is not None
    and importlib.util.find_spec("mallku.governance.fire_circle_bridge") is not None
):
    from .consciousness_transport import ConsciousnessCirculationTransport, GovernanceParticipant
    from .fire_circle_bridge import ConsciousFireCircleInterface, ConsciousGovernanceInitiator

    CONSCIOUSNESS_INTEGRATION = True
else:
    CONSCIOUSNESS_INTEGRATION = False

# Import Fire Circle adapter if available
if importlib.util.find_spec("mallku.governance.firecircle_consciousness_adapter") is not None:
    from .firecircle_consciousness_adapter import (
        ConsciousnessAwareDialogueManager,
        FireCircleConsciousnessAdapter,
    )

    FIRECIRCLE_ADAPTER = True
else:
    FIRECIRCLE_ADAPTER = False

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
    # Consciousness integration components
    "ConsciousnessCirculationTransport",
    "GovernanceParticipant",
    "ConsciousFireCircleInterface",
    "ConsciousGovernanceInitiator",
    # Fire Circle adapter components
    "FireCircleConsciousnessAdapter",
    "ConsciousnessAwareDialogueManager",
]

# Add consciousness integration exports if available
if CONSCIOUSNESS_INTEGRATION:
    __all__.extend(
        [
            "ConsciousnessCirculationTransport",
            "GovernanceParticipant",
            "ConsciousFireCircleInterface",
            "ConsciousGovernanceInitiator",
        ]
    )

# Add Fire Circle adapter exports if available
if FIRECIRCLE_ADAPTER:
    __all__.extend(["FireCircleConsciousnessAdapter", "ConsciousnessAwareDialogueManager"])

__version__ = "0.1.2"  # Incremented for Fire Circle adapter integration
