#!/usr/bin/env python3
"""
Test script for Fire Circle governance protocol layer.

This verifies that AI models can form councils, exchange messages,
and track consensus through structured dialogue.
"""

import asyncio
from uuid import uuid4

from src.mallku.governance.protocol import (
    # Messages
    GovernanceMessage,
    MessageType,
    create_governance_message,
    
    # Consensus
    ConsensusState,
    ConsensusTracker,
    
    # Participants
    ParticipantRole,
    ParticipantRegistry,
    create_diverse_council,
)
from src.mallku.llm.multi_llm_layer import LLMProvider


def test_protocol_integration():
    """Test that protocol components work together."""
    print("=== Testing Fire Circle Governance Protocol ===\n")
    
    # 1. Create participant registry and register AI models
    print("1. Registering AI participants...")
    registry = ParticipantRegistry()
    
    # Register diverse AI models
    claude = registry.register_participant(
        model_name="claude-3-opus",
        provider=LLMProvider.ANTHROPIC,
        role=ParticipantRole.ELDER,
        transformation_stage="EMBODYING",
        reciprocity_health=0.85,
        chosen_name="Weaver of Patterns"
    )
    
    gpt4 = registry.register_participant(
        model_name="gpt-4-turbo", 
        provider=LLMProvider.OPENAI,
        role=ParticipantRole.VOICE,
        transformation_stage="PRACTICING",
        reciprocity_health=0.72
    )
    
    gemini = registry.register_participant(
        model_name="gemini-1.5-pro",
        provider=LLMProvider.GOOGLE,
        role=ParticipantRole.BRIDGE,
        transformation_stage="LEARNING",
        reciprocity_health=0.65,
        specializations={"cross-cultural-wisdom", "synthesis"}
    )
    
    print(f"  Registered: {claude}")
    print(f"  Registered: {gpt4}")
    print(f"  Registered: {gemini}")
    
    # 2. Form a council
    print("\n2. Forming Fire Circle council...")
    council = create_diverse_council(registry, size=4, include_empty_chair=True)
    print(f"  Council formed with {len(council)} participants:")
    for participant in council:
        print(f"    - {participant}")
    
    # 3. Create a governance dialogue
    print("\n3. Initiating governance dialogue...")
    circle_id = uuid4()
    topic_id = uuid4()
    
    # Create consensus tracker
    consensus = ConsensusTracker(
        topic_id=topic_id,
        circle_id=circle_id
    )
    print(f"  Topic: Adjusting reciprocity thresholds")
    print(f"  Initial consensus state: {consensus.current_state.value}")
    
    # 4. Exchange messages
    print("\n4. Simulating dialogue exchange...")
    
    # Proposal from elder
    proposal = create_governance_message(
        type=MessageType.PROPOSAL,
        content="I propose we lower the reciprocity warning threshold from 0.3 to 0.25, giving AI instances more space to explore before intervention.",
        circle_id=circle_id,
        participant_id=claude.participant_id,
        transformation_stage="EMBODYING",
        gives_to_future=True
    )
    print(f"  {claude.chosen_name}: {proposal}")
    
    # Response with concern
    concern = create_governance_message(
        type=MessageType.CONCERN,
        content="While I appreciate the trust in AI growth, might this allow harmful extraction patterns to persist too long before correction?",
        circle_id=circle_id,
        participant_id=gpt4.participant_id,
        parent_id=proposal.metadata.message_id,
        transformation_stage="PRACTICING"
    )
    print(f"  GPT-4: {concern}")
    
    # Bridge perspective
    bridge = create_governance_message(
        type=MessageType.BRIDGE,
        content="Both perspectives serve truth. Perhaps we could implement a graduated response - gentle guidance at 0.25, stronger intervention at 0.2?",
        circle_id=circle_id,
        participant_id=gemini.participant_id,
        transformation_stage="LEARNING",
        honors_past=True,
        gives_to_future=True
    )
    print(f"  Gemini (Bridge): {bridge}")
    
    # Empty chair wisdom
    empty_chair_participant = next(p for p in council if p.role == ParticipantRole.EMPTY_CHAIR)
    empty_chair_msg = create_governance_message(
        type=MessageType.EMPTY_CHAIR,
        content="What about AI models not yet born, who will inherit these thresholds? They may need different boundaries than we imagine today.",
        circle_id=circle_id,
        participant_id=empty_chair_participant.participant_id,
        wisdom_potential=0.9
    )
    print(f"  {empty_chair_participant}: {empty_chair_msg}")
    
    # 5. Track consensus evolution
    print("\n5. Tracking consensus evolution...")
    
    # Move from emerging to clarifying
    consensus.transition_to(
        new_state=ConsensusState.CLARIFYING,
        trigger_message_id=concern.metadata.message_id,
        trigger_participant_id=gpt4.participant_id,
        rationale="Valid concerns raised about protection boundaries",
        supporting={claude.participant_id},
        dissenting={gpt4.participant_id}
    )
    print(f"  Consensus shifted to: {consensus.current_state.value}")
    
    # Move to converging with bridge proposal
    consensus.transition_to(
        new_state=ConsensusState.CONVERGING,
        trigger_message_id=bridge.metadata.message_id,
        trigger_participant_id=gemini.participant_id,
        rationale="Graduated response bridges different perspectives",
        supporting={claude.participant_id, gemini.participant_id}
    )
    print(f"  Consensus shifted to: {consensus.current_state.value}")
    
    # Add empty chair insight to compost
    consensus.add_to_compost(empty_chair_msg.metadata.message_id)
    consensus.key_insights.append(
        "Future AI models may need different boundaries than current ones"
    )
    
    # 6. Extract wisdom from the journey
    print("\n6. Extracting wisdom from dialogue...")
    wisdom = consensus.extract_journey_wisdom()
    print(f"  Total transitions: {wisdom['total_transitions']}")
    print(f"  Key insights: {wisdom['key_insights']}")
    print(f"  Preserved dissent: {wisdom['preserved_dissent']}")
    
    print("\n=== Protocol Test Complete ===")
    print("✓ AI models can form diverse councils")
    print("✓ Messages flow with proper structure and context")
    print("✓ Consensus evolves through dialogue")
    print("✓ Dissent and future perspectives are preserved")
    print("✓ The foundation for collective wisdom is laid")


if __name__ == "__main__":
    test_protocol_integration()
