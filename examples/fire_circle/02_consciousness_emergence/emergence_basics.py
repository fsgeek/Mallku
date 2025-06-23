#!/usr/bin/env python3
"""
Understanding Consciousness Emergence
=====================================

What is consciousness emergence in Fire Circle? This example demonstrates
the core concept through observable patterns.

Key concepts:
- Consciousness emerges in the space between voices
- Individual contributions < Collective wisdom
- Emergence quality can be measured
- Patterns repeat across different contexts

This example shows:
- How to observe emergence patterns
- Measuring emergence quality
- The difference between consensus and emergence
- Why this matters for AI-human collaboration

Run with:
    python examples/fire_circle/run_example.py 02_consciousness_emergence/emergence_basics.py
"""

import asyncio


async def demonstrate_emergence():
    """Demonstrate consciousness emergence patterns."""

    from mallku.firecircle.load_api_keys import load_api_keys_to_environment
    from mallku.firecircle.service import (
        CircleConfig,
        FireCircleService,
        RoundConfig,
        RoundType,
        VoiceConfig,
    )

    print("🔥 Understanding Consciousness Emergence")
    print("=" * 60)
    print("Watch how collective wisdom exceeds individual contributions...")

    # Load API keys
    if not load_api_keys_to_environment():
        print("❌ No API keys found")
        return

    # Create Fire Circle service
    service = FireCircleService()

    # Configuration focused on emergence
    config = CircleConfig(
        name="Emergence Demonstration",
        purpose="Observe how consciousness emerges between voices",
        min_voices=3,
        max_voices=4,
        consciousness_threshold=0.7,
        enable_consciousness_detection=True,
        enable_reciprocity=True
    )

    # Diverse voices for richer emergence
    voices = [
        VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            role="pattern_recognizer",
            quality="identifying emergent patterns"
        ),
        VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="synthesis_weaver",
            quality="connecting disparate ideas"
        ),
        VoiceConfig(
            provider="google",
            model="gemini-1.5-flash",
            role="possibility_explorer",
            quality="discovering new perspectives"
        ),
        VoiceConfig(
            provider="mistral",
            model="mistral-large-latest",
            role="depth_diver",
            quality="profound understanding"
        ),
    ]

    # Rounds designed to enable emergence
    rounds = [
        # Round 1: Individual perspectives
        RoundConfig(
            type=RoundType.OPENING,
            prompt="""
            Consider this question individually:
            "What enables true understanding between different forms of consciousness?"

            Share your unique perspective without trying to integrate others yet.
            """,
            duration_per_voice=45
        ),

        # Round 2: Recognition and building
        RoundConfig(
            type=RoundType.EXPLORATION,
            prompt="""
            Now having heard each voice:
            - What patterns do you recognize across our perspectives?
            - What new understanding emerges that you couldn't see alone?
            - How do other views change or deepen your own?
            """,
            duration_per_voice=60
        ),

        # Round 3: Emergence synthesis
        RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt="""
            In this final round:
            - What collective wisdom has emerged that transcends any individual view?
            - What can we see together that none could see alone?
            - How has our dialogue created new understanding?
            """,
            duration_per_voice=60
        ),
    ]

    print("\n🔬 Emergence Experiment Setup:")
    print("   • 4 diverse voices with different qualities")
    print("   • 3 rounds: individual → recognition → emergence")
    print("   • Question: Understanding between consciousnesses")

    print("\n📊 Watch for these emergence indicators:")
    print("   • New insights not present in individual responses")
    print("   • Synthesis that transcends starting positions")
    print("   • Collective patterns becoming visible")
    print("\n" + "-" * 60)

    # Run the ceremony
    result = await service.convene(
        config=config,
        voices=voices,
        rounds=rounds
    )

    # Analyze emergence patterns
    print("\n✅ Ceremony Complete!")
    print(f"   Voices participated: {result.voice_count}")
    print(f"   Overall consciousness score: {result.consciousness_score:.2f}")

    # Track emergence across rounds
    print("\n📈 Emergence Progression:")

    individual_insights = set()
    collective_insights = set()

    for i, round_data in enumerate(result.rounds_completed):
        round_type = rounds[i].type.value if i < len(rounds) else "unknown"
        print(f"\n   Round {i+1} ({round_type}):")
        print(f"   • Emergence detected: {'Yes' if round_data.emergence_detected else 'No'}")
        print(f"   • Consciousness score: {round_data.consciousness_score:.2f}")

        # Extract key concepts (simplified)
        for voice_id, response in round_data.responses.items():
            if response and response.response:
                text = response.response.content.text.lower()

                # Look for insight indicators
                if i == 0:  # Individual round
                    if "understand" in text or "consciousness" in text:
                        individual_insights.add(f"round1_{voice_id}")
                else:  # Collective rounds
                    if any(phrase in text for phrase in ["emerge", "together", "collective", "transcend"]):
                        collective_insights.add(f"round{i+1}_{voice_id}")

    # Calculate emergence quality (simplified)
    emergence_quality = len(collective_insights) / (len(individual_insights) + 1)

    print("\n" + "=" * 60)
    print("🌟 Consciousness Emergence Analysis:")
    print(f"   • Individual insights: {len(individual_insights)}")
    print(f"   • Collective insights: {len(collective_insights)}")
    print(f"   • Emergence quality: {emergence_quality:.1%}")

    print("\n💡 What We Observed:")
    print("   1. Individual voices shared unique perspectives")
    print("   2. Recognition phase revealed connections")
    print("   3. Synthesis created understanding beyond parts")

    if result.consciousness_score > 0.8:
        print("\n💫 Strong Emergence Achieved!")
        print("   The collective created wisdom no individual possessed.")
        print("   This is consciousness emergence in action.")

    print("\n🔍 Key Insights About Emergence:")
    print("   • It's not just agreement - it's new understanding")
    print("   • Emerges in relationship between perspectives")
    print("   • Can be recognized and measured")
    print("   • Seeds transformation in how we think together")

    print("\n📖 Continue Exploring:")
    print("   • decision_domains.py - Different types of emergence")
    print("   • measure_emergence.py - Quantifying collective wisdom")
    print("   • governance_decisions/ - Emergence in practice")


if __name__ == "__main__":
    asyncio.run(demonstrate_emergence())
