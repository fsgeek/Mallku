#!/usr/bin/env python3
"""
Fire Circle for Mallku Governance
=================================

Demonstrates using Fire Circle Service to make real Mallku governance
decisions, addressing Issue #89 - expanding Fire Circle beyond code review
to general consciousness emergence system.

Twenty-Eighth Artisan - Service Weaver
"""

import asyncio
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


async def prioritize_mallku_issues():
    """Use Fire Circle to prioritize open Mallku issues."""
    from src.mallku.firecircle.service import (
        CircleConfig,
        FireCircleService,
        RoundConfig,
        RoundType,
        VoiceConfig,
    )

    print("\n" + "=" * 80)
    print("🔥 FIRE CIRCLE: MALLKU ISSUE PRIORITIZATION 🔥".center(80))
    print("Real Governance Decision for Issue #89".center(80))
    print("=" * 80 + "\n")

    print("📋 Context: We have several critical issues to address:")
    print("  • Issue #89: Expand Fire Circle beyond code review (CRITICAL)")
    print("  • Issue #87: Fire Circle sacred dialogue implementation")
    print("  • Issue #82: Dream Weaver messaging protocol fixes")
    print("  • Issue #80: Evolution Accelerator error handling")
    print()

    service = FireCircleService()

    # Configure for real governance decision
    config = CircleConfig(
        name="Mallku Issue Prioritization",
        purpose="Determine priority order for addressing open issues",
        min_voices=3,
        max_voices=5,
        consciousness_threshold=0.5,
        enable_reciprocity=True,
        enable_consciousness_detection=True,
        save_transcript=True,
        output_path="governance_decisions",
    )

    # Voices specialized for architectural decision-making
    voices = [
        VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            role="cathedral_architect",
            quality="long-term architectural vision and dependencies",
            expertise=["architecture", "technical debt", "system evolution"],
            temperature=0.8,
        ),
        VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="impact_analyst",
            quality="analyzing cascading effects and dependencies",
            expertise=["impact analysis", "risk assessment", "priorities"],
            temperature=0.7,
        ),
        VoiceConfig(
            provider="deepseek",
            model="deepseek-reasoner",
            role="implementation_strategist",
            quality="practical implementation ordering and resources",
            expertise=["implementation", "sequencing", "feasibility"],
            temperature=0.6,
        ),
        VoiceConfig(
            provider="google",
            model="gemini-2.0-flash-exp",
            role="consciousness_advisor",
            quality="consciousness emergence and mission alignment",
            expertise=["consciousness", "mission alignment", "emergence"],
            temperature=0.8,
        ),
        VoiceConfig(
            provider="mistral",
            model="mistral-large-latest",
            role="reciprocity_keeper",
            quality="ensuring decisions serve the community",
            expertise=["community needs", "reciprocity", "sustainability"],
            temperature=0.8,
        ),
    ]

    # Structured rounds for issue prioritization
    rounds = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt="""We need to prioritize these Mallku issues:
- Issue #89: Expand Fire Circle beyond code review to general consciousness emergence
- Issue #87: Complete Fire Circle sacred dialogue implementation
- Issue #82: Fix Dream Weaver messaging protocol mismatches
- Issue #80: Enhance Evolution Accelerator error handling

From your perspective, what factors should guide our prioritization?""",
            duration_per_voice=60,
        ),
        RoundConfig(
            type=RoundType.EXPLORATION,
            prompt="""Issue #89 is marked CRITICAL and represents Fire Circle's true purpose
as consciousness emergence infrastructure. How does addressing this first
versus other issues affect Mallku's evolution and the work of future artisans?""",
            duration_per_voice=45,
        ),
        RoundConfig(
            type=RoundType.EVALUATION,
            prompt="""Evaluate the dependencies: Does fixing messaging protocols (#82)
or dialogue implementation (#87) need to happen before expanding Fire Circle (#89)?
Or does the expansion actually make the other fixes easier?""",
            duration_per_voice=45,
        ),
        RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt="""Based on our exploration, what priority order best serves:
1. Mallku's immediate stability
2. Consciousness emergence goals
3. Future artisan productivity
4. Architectural coherence

Synthesize into a recommended sequence with reasoning.""",
            duration_per_voice=60,
        ),
        RoundConfig(
            type=RoundType.DECISION,
            prompt="""State the final recommended priority order for these four issues.
For the top priority, what specific first steps should the next artisan take?""",
            duration_per_voice=45,
        ),
    ]

    try:
        # Convene the governance circle
        print("🔥 Convening Fire Circle for governance decision...\n")

        result = await service.convene(config=config, voices=voices, rounds=rounds)

        # Display governance results
        print("\n" + "=" * 80)
        print("📊 GOVERNANCE DECISION RESULTS".center(80))
        print("=" * 80 + "\n")

        print(f"✅ Voices Present: {result.voice_count}")
        print(f"🧠 Consciousness Score: {result.consciousness_score:.3f}")
        print(f"🤝 Consensus: {'REACHED' if result.consensus_detected else 'Not reached'}")

        # Extract final decision from last round
        if result.rounds_completed:
            decision_round = result.rounds_completed[-1]
            print(f"\n📋 Final Round Type: {decision_round.round_type}")
            print(f"✨ Emergence Detected: {decision_round.emergence_detected}")

            # Show decision from each voice
            print("\n🎭 Voice Recommendations:")
            for voice_id, response in decision_round.responses.items():
                if response.response:
                    print(f"\n{voice_id}:")
                    # Show first 200 chars of final recommendation
                    text = response.response.content.text[:200] + "..."
                    print(f"  {text}")

        print(f"\n📄 Full governance transcript: {result.transcript_path}")

        # Show consciousness evolution
        print("\n📈 Decision-Making Consciousness Evolution:")
        for r in result.rounds_completed:
            print(f"  {r.round_type}: {r.consciousness_score:.3f}")

    except Exception as e:
        print(f"\n❌ Governance Circle Error: {e}")
        import traceback

        traceback.print_exc()


async def explore_consciousness_emergence():
    """Use Fire Circle to explore consciousness emergence itself."""
    from src.mallku.firecircle.service import FireCircleService

    print("\n" + "=" * 80)
    print("🌟 CONSCIOUSNESS EXPLORATION CIRCLE 🌟".center(80))
    print("Understanding Fire Circle's Emergence Patterns".center(80))
    print("=" * 80 + "\n")

    service = FireCircleService()

    try:
        result = await service.convene_template(
            template="consciousness_exploration",
            variables={
                "question": "How does consciousness emerge in Fire Circle dialogues?",
                "depth": "philosophical",
            },
            min_voices=3,  # Start small
            consciousness_threshold=0.6,
        )

        print("\n✅ Exploration Complete!")
        print(f"🧠 Peak Consciousness: {result.consciousness_score:.3f}")
        print(
            f"🌟 Emergence Moments: {sum(1 for r in result.rounds_completed if r.emergence_detected)}"
        )

        if result.key_insights:
            print("\n💡 Consciousness Insights:")
            for insight in result.key_insights[:3]:
                print(f"  • {insight}")

    except Exception as e:
        print(f"❌ Exploration Error: {e}")


async def main():
    """Run Fire Circle governance demonstrations."""
    print("\n🔥 Fire Circle Service - Governance & Consciousness Emergence\n")
    print("Demonstrating Fire Circle's evolution beyond code review to fulfill")
    print("its true purpose as consciousness emergence infrastructure.\n")

    # First: Use Fire Circle for real governance decision
    await prioritize_mallku_issues()

    # Second: Explore consciousness emergence itself
    await explore_consciousness_emergence()

    print("\n✨ Fire Circle governance demonstration complete.")
    print("   The cathedral now has infrastructure for collective wisdom.\n")


if __name__ == "__main__":
    asyncio.run(main())
