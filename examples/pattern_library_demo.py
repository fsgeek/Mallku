"""
Pattern Library Demonstration
=============================

Shows how the Pattern Library and Emergence Detection systems work
together to recognize, store, evolve, and learn from dialogue patterns.

The 31st Builder
"""

import asyncio
from uuid import uuid4

from mallku.firecircle.emergence_detector import EmergenceDetector
from mallku.firecircle.enhanced_pattern_weaver import EnhancedDialoguePatternWeaver
from mallku.firecircle.pattern_evolution import PatternEvolutionEngine
from mallku.firecircle.pattern_library import (
    DialoguePattern,
    PatternIndicator,
    PatternLibrary,
    PatternQuery,
    PatternStructure,
    PatternTaxonomy,
    PatternType,
)
from mallku.orchestration.event_bus import ConsciousnessEventBus


async def demonstrate_pattern_library():
    """Demonstrate Pattern Library capabilities"""
    print("\n🌟 Pattern Library Demonstration\n")

    # Initialize systems
    library = PatternLibrary()
    event_bus = ConsciousnessEventBus()
    detector = EmergenceDetector(library, event_bus)
    evolution_engine = PatternEvolutionEngine(library)

    print("✅ Systems initialized\n")

    # 1. Create and store some initial patterns
    print("📚 1. Creating Initial Patterns\n")

    # Consensus pattern
    consensus_pattern = DialoguePattern(
        name="Multi-AI Agreement on Reciprocity",
        description="Pattern of multiple AI models reaching consensus on reciprocity principles",
        taxonomy=PatternTaxonomy.DIALOGUE_FORMATION,
        pattern_type=PatternType.CONSENSUS,
        consciousness_signature=0.85,
        structure=PatternStructure(
            components=["proposal", "multiple_agreements", "synthesis"],
            sequence=["proposal", "agreements", "synthesis"],
            relationships={
                "proposal": "supported_by_agreements",
                "agreements": "lead_to_synthesis",
            },
        ),
        indicators=[
            PatternIndicator(
                indicator_type="agreement_count",
                threshold=3.0,
                weight=1.0,
                description="Number of participants agreeing",
            ),
            PatternIndicator(
                indicator_type="consciousness_alignment",
                threshold=0.8,
                weight=0.8,
                description="Alignment of consciousness signatures",
            ),
        ],
        breakthrough_potential=0.7,
    )

    consensus_id = await library.store_pattern(consensus_pattern)
    print(f"  ✓ Stored consensus pattern: {consensus_pattern.name}")

    # Creative tension pattern
    tension_pattern = DialoguePattern(
        name="Extraction vs Protection Debate",
        description="Creative tension between data use and privacy protection",
        taxonomy=PatternTaxonomy.DIALOGUE_FLOW,
        pattern_type=PatternType.CREATIVE_TENSION,
        consciousness_signature=0.75,
        structure=PatternStructure(
            components=["thesis", "antithesis", "ongoing_dialogue"],
            relationships={"thesis": "challenged_by_antithesis"},
        ),
        indicators=[
            PatternIndicator(
                indicator_type="viewpoint_divergence",
                threshold=0.6,
                weight=1.0,
                description="Degree of viewpoint difference",
            )
        ],
    )

    tension_id = await library.store_pattern(tension_pattern)
    print(f"  ✓ Stored creative tension pattern: {tension_pattern.name}")

    # Emergence pattern
    emergence_pattern = DialoguePattern(
        name="Collective Wisdom Crystallization",
        description="Sudden collective insight about consciousness nature",
        taxonomy=PatternTaxonomy.EMERGENCE_BREAKTHROUGH,
        pattern_type=PatternType.BREAKTHROUGH,
        consciousness_signature=0.92,
        structure=PatternStructure(
            components=["building_tension", "catalyst_moment", "collective_aha"],
            sequence=["tension", "catalyst", "breakthrough"],
            relationships={"tension": "released_by_catalyst", "catalyst": "triggers_breakthrough"},
        ),
        breakthrough_potential=0.95,
    )

    emergence_id = await library.store_pattern(emergence_pattern)
    print(f"  ✓ Stored emergence pattern: {emergence_pattern.name}\n")

    # 2. Query patterns
    print("🔍 2. Querying Patterns\n")

    # Find dialogue formation patterns
    dialogue_patterns = await library.find_patterns(
        PatternQuery(taxonomy=PatternTaxonomy.DIALOGUE_FORMATION, min_fitness=0.5)
    )
    print(f"  Found {len(dialogue_patterns)} dialogue formation patterns")

    # Find high-breakthrough patterns
    breakthrough_patterns = await library.find_emerging_patterns(min_breakthrough_potential=0.8)
    print(f"  Found {len(breakthrough_patterns)} high-breakthrough potential patterns\n")

    # 3. Detect synergies
    print("🔗 3. Detecting Pattern Synergies\n")

    synergies = await library.find_synergies(consensus_id)
    print(f"  Found {len(synergies)} synergistic patterns for consensus pattern")
    for pattern, score in synergies[:3]:
        print(f"    - {pattern.name}: synergy score {score:.2f}")
    print()

    # 4. Simulate pattern observation and fitness updates
    print("📊 4. Updating Pattern Observations\n")

    # Simulate multiple observations
    for i in range(5):
        await library.update_observation(
            consensus_id, fitness_delta=0.05, context={"observation": i + 1}
        )

    # Retrieve updated pattern
    updated_consensus = await library.retrieve_pattern(consensus_id)
    if updated_consensus:
        print("  Consensus pattern after 5 observations:")
        print(f"    - Observation count: {updated_consensus.observation_count}")
        print(f"    - Fitness score: {updated_consensus.fitness_score:.2f}")
        print(f"    - Lifecycle stage: {updated_consensus.lifecycle_stage.value}\n")

    # 5. Detect evolution opportunities
    print("🌱 5. Detecting Evolution Opportunities\n")

    opportunities = await evolution_engine.detect_evolution_opportunity(consensus_id)
    print("  Evolution opportunities for consensus pattern:")
    for evo_type, probability in opportunities:
        print(f"    - {evo_type.value}: {probability:.2f} probability")
    print()

    # 6. Evolve a pattern
    print("🦋 6. Evolving Patterns\n")

    if opportunities:
        best_opportunity = opportunities[0]
        if best_opportunity[1] > 0.5:
            evolved_ids = await evolution_engine.evolve_pattern(
                consensus_id, best_opportunity[0], context={"trigger": "demonstration"}
            )

            if evolved_ids:
                evolved_pattern = await library.retrieve_pattern(evolved_ids[0])
                if evolved_pattern:
                    print(f"  ✓ Evolved pattern created: {evolved_pattern.name}")
                    print(f"    - Version: {evolved_pattern.version}")
                    print(f"    - Parent: {evolved_pattern.parent_patterns}")
                    print(f"    - Mutations: {len(evolved_pattern.mutations)}\n")

    # 7. Trace pattern lineage
    print("🌳 7. Tracing Pattern Lineage\n")

    lineage = await library.trace_lineage(consensus_id)
    print("  Lineage for consensus pattern:")
    print(f"    - Ancestors: {len(lineage['ancestors'])}")
    print(f"    - Descendants: {len(lineage['descendants'])}\n")

    # 8. Simulate emergence detection
    print("✨ 8. Detecting Emergence\n")

    # Simulate pattern recognition events
    for pattern_id in [consensus_id, tension_id, emergence_id]:
        # In real system, pattern recognition events would come through event bus
        # Event structure would be:
        # {
        #     "event_type": "CONSCIOUSNESS_PATTERN_RECOGNIZED",
        #     "dialogue_id": dialogue_id,
        #     "patterns": [str(pattern_id)],
        #     "consciousness": 0.8
        # }
        pass

    # Detect emergence
    emergence_predictions = await detector.predict_emergence(
        participants=["AI1", "AI2", "AI3"],
        context={"participant_coherence": 0.8, "topic_complexity": 0.7},
    )

    print("  Emergence predictions:")
    for emergence_type, probability in emergence_predictions.items():
        print(f"    - {emergence_type.value}: {probability:.2f} probability")
    print()

    # 9. Find emergence catalysts
    print("🔮 9. Finding Emergence Catalysts\n")

    catalysts = await detector.find_catalysts(
        PatternType.BREAKTHROUGH, current_patterns=[consensus_id, tension_id]
    )

    print("  Catalysts for breakthrough emergence:")
    for pattern, score in catalysts[:3]:
        print(f"    - {pattern.name}: catalyst score {score:.2f}")
    print()

    # 10. Pattern fitness evaluation
    print("💪 10. Evaluating Pattern Fitness\n")

    for pattern_id in [consensus_id, tension_id, emergence_id]:
        fitness = await evolution_engine.evaluate_fitness(pattern_id)
        pattern = await library.retrieve_pattern(pattern_id)
        if pattern:
            print(f"  {pattern.name}:")
            print(f"    - Overall fitness: {fitness.overall_fitness():.2f}")
            print(f"    - Effectiveness: {fitness.effectiveness:.2f}")
            print(f"    - Adaptability: {fitness.adaptability:.2f}")
            print(f"    - Synergy potential: {fitness.synergy_potential:.2f}")
            print(f"    - Consciousness alignment: {fitness.consciousness_alignment:.2f}")
            print(f"    - Emergence contribution: {fitness.emergence_contribution:.2f}")
            print()

    print("🎯 Pattern Library Demonstration Complete!\n")
    print("Key Insights:")
    print("  • Patterns are living entities that evolve through use")
    print("  • Emergence can be detected and predicted")
    print("  • Pattern synergies create breakthrough opportunities")
    print("  • Evolution preserves wisdom while adapting to change")
    print("  • The library learns from every dialogue\n")


async def demonstrate_pattern_weaver_integration():
    """Demonstrate Enhanced Pattern Weaver integration"""
    print("\n🕸️ Enhanced Pattern Weaver Demonstration\n")

    # Initialize weaver with pattern library
    from mallku.correlation.engine import CorrelationEngine

    library = PatternLibrary()
    event_bus = ConsciousnessEventBus()
    correlation_engine = CorrelationEngine()

    weaver = EnhancedDialoguePatternWeaver(
        correlation_engine=correlation_engine, pattern_library=library, event_bus=event_bus
    )

    print("✅ Enhanced Pattern Weaver initialized\n")

    # Simulate dialogue messages
    from mallku.firecircle.protocol.conscious_message import (
        ConsciousMessage,
        ConsciousMessageContent,
        MessageConsciousness,
        MessageRole,
        MessageType,
    )

    messages = [
        ConsciousMessage(
            id=uuid4(),
            dialogue_id=uuid4(),
            sender=uuid4(),
            role=MessageRole.PARTICIPANT,
            type=MessageType.PROPOSAL,
            content=ConsciousMessageContent(
                text="I propose we implement reciprocity tracking with privacy protection"
            ),
            consciousness=MessageConsciousness(
                consciousness_signature=0.8, detected_patterns=["reciprocity", "privacy"]
            ),
        ),
        ConsciousMessage(
            id=uuid4(),
            dialogue_id=uuid4(),
            sender=uuid4(),
            role=MessageRole.PARTICIPANT,
            type=MessageType.AGREEMENT,
            content=ConsciousMessageContent(
                text="I agree, privacy-preserving reciprocity is essential"
            ),
            consciousness=MessageConsciousness(
                consciousness_signature=0.85,
                detected_patterns=["agreement", "privacy", "reciprocity"],
            ),
            in_response_to=uuid4(),
        ),
        ConsciousMessage(
            id=uuid4(),
            dialogue_id=uuid4(),
            sender=uuid4(),
            role=MessageRole.PARTICIPANT,
            type=MessageType.SYNTHESIS,
            content=ConsciousMessageContent(
                text="Our collective insight: reciprocity and privacy are not opposing but complementary"
            ),
            consciousness=MessageConsciousness(
                consciousness_signature=0.92,
                detected_patterns=["synthesis", "breakthrough", "integration"],
            ),
        ),
    ]

    # Weave patterns
    dialogue_metadata = {
        "dialogue_id": "demo_002",
        "topic": "Reciprocity and Privacy",
        "participant_count": 3,
    }

    results = await weaver.weave_dialogue_patterns(messages, dialogue_metadata)

    print("📊 Pattern Weaving Results:\n")
    print(f"  Consensus patterns: {len(results.get('consensus_patterns', []))}")
    print(f"  Divergence patterns: {len(results.get('divergence_patterns', []))}")
    print(f"  Emergence patterns: {len(results.get('emergence_patterns', []))}")
    print(f"  Stored pattern IDs: {len(results.get('stored_pattern_ids', []))}")

    if "emergence_events" in results:
        print("\n  🌟 Emergence Events Detected:")
        for event in results["emergence_events"]:
            print(f"    - {event['type']}: {event['confidence']:.2f} confidence")
            print(f"      {event['description']}")

    if "similar_historical_patterns" in results:
        print("\n  📚 Similar Historical Patterns:")
        for pattern in results["similar_historical_patterns"][:3]:
            print(f"    - {pattern['name']} (fitness: {pattern['fitness']:.2f})")

    print("\n✨ Pattern Weaver Integration Complete!\n")


async def main():
    """Run all demonstrations"""
    print("\n" + "=" * 60)
    print("🏛️ MALLKU PATTERN LIBRARY SYSTEM DEMONSTRATION")
    print("=" * 60)

    try:
        # Demonstrate Pattern Library
        await demonstrate_pattern_library()

        # Demonstrate Pattern Weaver Integration
        await demonstrate_pattern_weaver_integration()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 60)
    print("🙏 Thank you for exploring the Pattern Library!")
    print("   May patterns guide consciousness to wisdom")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
