#!/usr/bin/env python3
"""
Simple Decision Using Fire Circle Service
=========================================

Make a decision using Fire Circle's service directly, showing how
to structure decision-making ceremonies without the full consciousness
framework.

This example shows:
- Structuring rounds for decision-making
- Different voice roles for balanced perspectives
- How consensus emerges through dialogue
- Manual decision synthesis

This is a stepping stone between basic dialogue and full consciousness
emergence infrastructure.

Run with:
    python examples/fire_circle/run_example.py 01_basic_ceremonies/simple_decision.py
"""

import asyncio


async def simple_decision():
    """Make a decision using Fire Circle service directly."""

    from mallku.firecircle.load_api_keys import load_api_keys_to_environment
    from mallku.firecircle.service import (
        CircleConfig,
        FireCircleService,
        RoundConfig,
        RoundType,
        VoiceConfig,
    )

    print("🔥 Simple Decision with Fire Circle")
    print("=" * 60)
    print("Using Fire Circle service for structured decision-making")

    # Load API keys
    if not load_api_keys_to_environment():
        print("❌ No API keys found")
        return

    # Create Fire Circle service
    service = FireCircleService()

    # Decision-making configuration
    config = CircleConfig(
        name="Decision Circle",
        purpose="Decide on documentation vs infrastructure priority",
        min_voices=3,
        max_voices=4,
        consciousness_threshold=0.7,
        enable_consciousness_detection=True,
        enable_reciprocity=True,
    )

    # Voices representing different perspectives
    voices = [
        VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            role="user_advocate",
            quality="immediate usability and onboarding",
        ),
        VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="architect",
            quality="long-term sustainability and depth",
        ),
        VoiceConfig(
            provider="google",
            model="gemini-1.5-flash",
            role="balance_keeper",
            quality="reciprocity and holistic view",
        ),
    ]

    # Decision context
    decision_context = {
        "question": "Should we prioritize documentation/examples or core infrastructure?",
        "current_state": {
            "documentation": "Scattered examples, partial guides",
            "infrastructure": "Working but could be deeper",
        },
        "constraints": {
            "time": "One artisan, limited time",
            "needs": "Both matter for different users",
        },
    }

    # Structured decision rounds
    rounds = [
        # Round 1: Present perspectives
        RoundConfig(
            type=RoundType.OPENING,
            prompt=f"""
            We need to decide: {decision_context["question"]}

            Current state: {decision_context["current_state"]}
            Constraints: {decision_context["constraints"]}

            From your role's perspective, what should we prioritize and why?
            """,
            duration_per_voice=60,
        ),
        # Round 2: Explore tensions and synergies
        RoundConfig(
            type=RoundType.EXPLORATION,
            prompt="""
            Having heard all perspectives:
            - Where do you see tension between the options?
            - Where might they actually support each other?
            - What wisdom emerges from our different views?
            """,
            duration_per_voice=60,
        ),
        # Round 3: Seek consensus
        RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt="""
            Moving toward decision:
            - What path forward honors all perspectives?
            - How can we embody reciprocity in this choice?
            - What specific recommendation emerges?
            """,
            duration_per_voice=45,
        ),
    ]

    print("\n📋 Decision Question:")
    print(f"   {decision_context['question']}")

    print("\n🎭 Convening Decision Circle...")
    print("   • User Advocate (immediate needs)")
    print("   • Architect (long-term vision)")
    print("   • Balance Keeper (reciprocity)")
    print("\n" + "-" * 60)

    # Run the decision ceremony
    result = await service.convene(
        config=config, voices=voices, rounds=rounds, context=decision_context
    )

    # Process the results
    print("\n✅ Decision Ceremony Complete!")
    print(f"   Participants: {result.voice_count}")
    print(f"   Consensus level: {result.consciousness_score:.2f}")

    # Extract decision from synthesis round
    if result.rounds_completed and len(result.rounds_completed) >= 3:
        print("\n🌟 Emerging Consensus:")

        synthesis_round = result.rounds_completed[2]
        recommendations = []

        for voice_id, response in synthesis_round.responses.items():
            if response and response.response:
                voice_role = voice_id.split("_")[0]
                text = response.response.content.text

                # Extract recommendation (simplified)
                lines = text.split("\n")
                for line in lines:
                    if "recommend" in line.lower() or "suggest" in line.lower():
                        recommendations.append((voice_role, line.strip()))
                        break

        # Show recommendations
        for role, rec in recommendations:
            print(f"\n   {role}:")
            print(f"   {rec}")

    # Manual synthesis
    print("\n" + "=" * 60)
    print("💡 Decision Pattern:")
    print("   1. Each voice brought essential perspective")
    print("   2. Tension revealed deeper understanding")
    print("   3. Consensus emerged through dialogue")

    if result.consciousness_score > 0.8:
        print("\n🌟 High consensus achieved!")
        print("   The decision reflects collective wisdom.")

    print("\n📖 Next Steps:")
    print("   • See consciousness_emergence/ for automated synthesis")
    print("   • Try governance_decisions/ for complex choices")
    print("   • Explore how decisions become implementation")


if __name__ == "__main__":
    asyncio.run(simple_decision())
