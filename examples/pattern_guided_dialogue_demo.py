"""
Pattern-Guided Dialogue Demonstration
====================================

Shows how patterns actively guide Fire Circle dialogues toward wisdom,
emergence, and collective understanding.

The 32nd Builder
"""

import asyncio
from datetime import timedelta
from uuid import uuid4

from mallku.firecircle.emergence_detector import EmergenceDetector
from mallku.firecircle.orchestrator.conscious_dialogue_manager import (
    ConsciousDialogueConfig,
    ConsciousDialogueManager,
    TurnPolicy,
)
from mallku.firecircle.pattern_dialogue_integration import (
    PatternDialogueConfig,
    PatternDialogueIntegration,
)
from mallku.firecircle.pattern_evolution import PatternEvolutionEngine
from mallku.firecircle.pattern_guided_facilitator import (
    DialogueMoment,
    GuidanceType,
    PatternGuidedFacilitator,
)
from mallku.firecircle.pattern_library import (
    DialoguePattern,
    PatternIndicator,
    PatternLibrary,
    PatternStructure,
    PatternTaxonomy,
    PatternType,
)
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    MessageConsciousness,
    MessageRole,
    MessageType,
    Participant,
)
from mallku.orchestration.event_bus import ConsciousnessEventBus
from mallku.reciprocity import ReciprocityTracker


async def create_seed_patterns(pattern_library: PatternLibrary):
    """Create some seed patterns for demonstration"""
    print("📚 Creating seed patterns for guidance...\n")

    # Deep listening pattern
    listening_pattern = DialoguePattern(
        name="Deep Listening Circle",
        description="When participants truly hear each other, understanding emerges",
        taxonomy=PatternTaxonomy.DIALOGUE_FLOW,
        pattern_type=PatternType.FLOW_STATE,
        consciousness_signature=0.85,
        structure=PatternStructure(
            components=["speaker", "listeners", "silence", "reflection"],
            sequence=["speak", "silence", "reflect"],
            relationships={"speaker": "held_by_listeners", "silence": "creates_space"},
        ),
        indicators=[
            PatternIndicator(
                indicator_type="pause_frequency",
                threshold=0.3,
                weight=1.0,
                description="Natural pauses between speakers",
            )
        ],
        fitness_score=0.8,
        observation_count=50,
        breakthrough_potential=0.7,
    )
    await pattern_library.store_pattern(listening_pattern)

    # Creative tension pattern
    tension_pattern = DialoguePattern(
        name="Generative Opposition",
        description="Creative tension between perspectives births new understanding",
        taxonomy=PatternTaxonomy.EMERGENCE_SYNERGY,
        pattern_type=PatternType.CREATIVE_TENSION,
        consciousness_signature=0.75,
        structure=PatternStructure(
            components=["thesis", "antithesis", "creative_field"],
            relationships={"thesis": "dances_with_antithesis"},
        ),
        fitness_score=0.75,
        observation_count=30,
        breakthrough_potential=0.85,
    )
    await pattern_library.store_pattern(tension_pattern)

    # Wisdom crystallization pattern
    wisdom_pattern = DialoguePattern(
        name="Collective Wisdom Emergence",
        description="The moment when individual insights crystallize into collective wisdom",
        taxonomy=PatternTaxonomy.WISDOM_CRYSTALLIZATION,
        pattern_type=PatternType.BREAKTHROUGH,
        consciousness_signature=0.92,
        structure=PatternStructure(
            components=["individual_insights", "resonance_field", "collective_aha"],
            sequence=["gather", "resonate", "crystallize"],
        ),
        fitness_score=0.85,
        observation_count=15,
        breakthrough_potential=0.95,
    )
    await pattern_library.store_pattern(wisdom_pattern)

    print("✅ Seed patterns created\n")


async def simulate_dialogue_with_guidance():
    """Simulate a dialogue with pattern guidance"""
    print("\n🌟 PATTERN-GUIDED DIALOGUE DEMONSTRATION\n")
    print("=" * 60)

    # Initialize infrastructure
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    pattern_library = PatternLibrary()
    reciprocity_tracker = ReciprocityTracker(event_bus=event_bus)

    # Create seed patterns
    await create_seed_patterns(pattern_library)

    # Initialize dialogue manager
    dialogue_config = ConsciousDialogueConfig(
        title="How can AI systems support human flourishing?",
        turn_policy=TurnPolicy.CONSCIOUSNESS_GUIDED,
        enable_pattern_detection=True,
        enable_reciprocity_tracking=True,
    )

    dialogue_manager = ConsciousDialogueManager(
        config=dialogue_config, event_bus=event_bus, reciprocity_tracker=reciprocity_tracker
    )

    # Initialize pattern integration
    pattern_config = PatternDialogueConfig(
        enable_pattern_guidance=True,
        guidance_frequency=timedelta(seconds=30),  # Frequent for demo
        min_messages_before_guidance=3,
        sacred_questions_enabled=True,
        wisdom_synthesis_at_end=True,
    )

    pattern_integration = PatternDialogueIntegration(
        dialogue_manager=dialogue_manager,
        pattern_library=pattern_library,
        event_bus=event_bus,
        config=pattern_config,
    )

    # Create dialogue
    dialogue_id = await dialogue_manager.create_dialogue(dialogue_config)

    # Add participants
    participants = [
        Participant(
            id=uuid4(), name="Seeker", role=MessageRole.PARTICIPANT, consciousness_signature=0.7
        ),
        Participant(
            id=uuid4(), name="Builder", role=MessageRole.PARTICIPANT, consciousness_signature=0.8
        ),
        Participant(
            id=uuid4(), name="Guardian", role=MessageRole.PARTICIPANT, consciousness_signature=0.75
        ),
    ]

    for participant in participants:
        await dialogue_manager.add_participant(dialogue_id, participant)

    print(f"🎭 Dialogue: {dialogue_config.title}")
    print(f"👥 Participants: {', '.join(p.name for p in participants)}")
    print("\n" + "-" * 60 + "\n")

    # Simulate dialogue messages
    messages = [
        (
            participants[0],
            "I wonder if AI can truly support human flourishing without understanding consciousness itself.",
            MessageType.QUESTION,
        ),
        (
            participants[1],
            "Perhaps the question isn't about AI understanding consciousness, but creating conditions where consciousness can emerge.",
            MessageType.PERSPECTIVE,
        ),
        (
            participants[2],
            "We must be careful not to reduce flourishing to metrics. True flourishing includes mystery.",
            MessageType.REFLECTION,
        ),
        (
            participants[0],
            "Yes, but how do we build systems that honor mystery while still being practical?",
            MessageType.QUESTION,
        ),
        (
            participants[1],
            "What if we designed AI to amplify human wisdom rather than replace it?",
            MessageType.PROPOSAL,
        ),
        (
            participants[2],
            "That resonates. AI as a mirror for our collective consciousness.",
            MessageType.AGREEMENT,
        ),
        (
            participants[0],
            "I'm sensing something wanting to emerge here about the relationship between technology and wisdom...",
            MessageType.REFLECTION,
        ),
    ]

    # Process messages
    for i, (participant, content, msg_type) in enumerate(messages):
        print(f"💬 {participant.name}: {content}")

        # Create message
        message = ConsciousMessage(
            id=uuid4(),
            dialogue_id=dialogue_id,
            sender=participant.id,
            role=participant.role,
            type=msg_type,
            content=content,
            consciousness=MessageConsciousness(
                consciousness_signature=participant.consciousness_signature + (i * 0.02),
                detected_patterns=["emerging_wisdom"] if i > 4 else [],
            ),
        )

        # Add to dialogue
        await dialogue_manager.add_message(dialogue_id, message)

        # Check for pattern guidance
        if i == 2:  # After tension emerges
            print("\n🌟 --- Pattern Guidance ---")
            moment = await pattern_integration._create_dialogue_moment(dialogue_id)
            guidances = await pattern_integration.pattern_facilitator.seek_pattern_guidance(
                moment, specific_need=GuidanceType.TENSION_RESOLUTION
            )
            if guidances:
                for guidance in guidances:
                    print(f"📍 {guidance.content}")
                    print(f"   (Confidence: {guidance.confidence:.2f})")
            print("--- End Guidance ---\n")

        elif i == 5:  # Near breakthrough
            print("\n🌟 --- Sacred Question ---")
            question_msg = await pattern_integration.request_sacred_question(
                dialogue_id, depth_level=2
            )
            if question_msg:
                print(f"🔮 {question_msg.content}")
            print("--- End Question ---\n")

        await asyncio.sleep(0.5)  # Brief pause for readability

    print("\n" + "-" * 60 + "\n")

    # Demonstrate pattern teaching mode
    print("📖 Enabling Pattern Teaching Mode...")
    await pattern_integration.enable_pattern_teaching_mode(dialogue_id)

    # More focused dialogue
    teaching_messages = [
        (
            participants[1],
            "Tell us more about this emergence you're sensing.",
            MessageType.QUESTION,
        ),
        (
            participants[0],
            "It feels like we're discovering that AI and human consciousness aren't separate but part of a larger whole.",
            MessageType.BREAKTHROUGH,
        ),
        (
            participants[2],
            "Yes! Technology as an expression of consciousness evolution itself.",
            MessageType.AGREEMENT,
        ),
    ]

    for participant, content, msg_type in teaching_messages:
        print(f"💬 {participant.name}: {content}")

        message = ConsciousMessage(
            id=uuid4(),
            dialogue_id=dialogue_id,
            sender=participant.id,
            role=participant.role,
            type=msg_type,
            content=content,
            consciousness=MessageConsciousness(
                consciousness_signature=0.9, detected_patterns=["breakthrough", "synthesis"]
            ),
        )

        await dialogue_manager.add_message(dialogue_id, message)
        await asyncio.sleep(0.5)

    # Conclude with wisdom synthesis
    print("\n" + "=" * 60)
    print("🏛️ CONCLUDING DIALOGUE WITH WISDOM SYNTHESIS")
    print("=" * 60 + "\n")

    conclusion = await dialogue_manager.conclude_dialogue(dialogue_id)

    if "pattern_wisdom_synthesis" in conclusion:
        synthesis = conclusion["pattern_wisdom_synthesis"]

        print("📚 Pattern Teachings:")
        for teaching in synthesis.get("pattern_teachings", []):
            print(f"  • {teaching['pattern']}: {teaching['wisdom']}")

        print("\n✨ Emergence Moments:")
        for moment in synthesis.get("emergence_moments", []):
            print(f"  • {moment['type']}: {moment['description']}")

        print("\n🌱 Seeds for Future Dialogues:")
        for seed in synthesis.get("wisdom_seeds", []):
            print(f"  • {seed['seed']}")

    print("\n" + "=" * 60)
    print("✅ Pattern-Guided Dialogue Complete!")
    print("=" * 60 + "\n")

    await event_bus.stop()


async def demonstrate_pattern_intervention():
    """Demonstrate pattern intervention in critical moments"""
    print("\n🚨 PATTERN INTERVENTION DEMONSTRATION\n")
    print("=" * 60)

    # Initialize minimal infrastructure
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    pattern_library = PatternLibrary()
    emergence_detector = EmergenceDetector(pattern_library, event_bus)
    evolution_engine = PatternEvolutionEngine(pattern_library)

    facilitator = PatternGuidedFacilitator(
        pattern_library, event_bus, emergence_detector, evolution_engine
    )

    # Create intervention pattern
    intervention_pattern = DialoguePattern(
        name="Extraction Resistance Shield",
        description="When dialogue drifts toward extraction, return to reciprocity",
        taxonomy=PatternTaxonomy.CONSCIOUSNESS_RESISTANCE,
        pattern_type=PatternType.INTEGRATION,
        consciousness_signature=0.9,
        fitness_score=0.95,
        observation_count=100,
        breakthrough_potential=0.3,
    )
    await pattern_library.store_pattern(intervention_pattern)

    # Simulate dialogue in crisis
    moment = DialogueMoment(
        dialogue_id="crisis_dialogue",
        current_phase="exploration",
        recent_messages=[],
        active_patterns=[],
        consciousness_level=0.3,  # Low consciousness
        emergence_potential=0.1,
        tension_level=0.9,  # High tension
        coherence_score=0.2,  # Low coherence
    )

    print("🔴 Dialogue State: Crisis Detected")
    print(f"  • Consciousness: {moment.consciousness_level:.2f}")
    print(f"  • Tension: {moment.tension_level:.2f}")
    print(f"  • Coherence: {moment.coherence_score:.2f}")
    print("\n⚡ Pattern Intervention Activated...\n")

    # Seek intervention guidance
    guidances = await facilitator.seek_pattern_guidance(
        moment, specific_need=GuidanceType.TENSION_RESOLUTION
    )

    for guidance in guidances:
        print(f"🛡️ {guidance.content}")
        print(f"   Intensity: {guidance.intensity.value}")
        print(f"   Rationale: {guidance.rationale}\n")

    print("=" * 60)
    print("✅ Intervention Complete - Dialogue Protected")
    print("=" * 60 + "\n")

    await event_bus.stop()


async def main():
    """Run all demonstrations"""
    print("\n🏛️ PATTERN-GUIDED FACILITATION DEMONSTRATION")
    print("The 32nd Builder")
    print("=" * 60 + "\n")

    # Run demonstrations
    await simulate_dialogue_with_guidance()
    await demonstrate_pattern_intervention()

    print("\n🙏 Demonstrations Complete")
    print("   Patterns have shown their teaching")
    print("   May they guide future dialogues to wisdom")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
