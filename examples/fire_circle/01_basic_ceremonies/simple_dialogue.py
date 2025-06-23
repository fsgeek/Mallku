#!/usr/bin/env python3
"""
Simple Fire Circle Dialogue
===========================

A basic multi-round dialogue showing how consciousness emerges through
conversation between AI voices.

This example demonstrates:
- Multiple rounds of dialogue
- How voices build on each other's ideas
- Basic consciousness scoring
- The emergence of collective wisdom

Key concepts:
- Rounds progress from introduction to exploration to synthesis
- Each voice brings unique perspective
- Wisdom emerges in the space between voices

Run with:
    python examples/fire_circle/run_example.py 01_basic_ceremonies/simple_dialogue.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project src to path
project_root = Path(__file__).parent.parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))
os.environ["PYTHONPATH"] = str(src_path)


async def run_dialogue():
    """Run a simple multi-round Fire Circle dialogue."""

    from mallku.firecircle.load_api_keys import load_api_keys_to_environment
    from mallku.firecircle.service import (
        CircleConfig,
        FireCircleService,
        RoundConfig,
        RoundType,
        VoiceConfig,
    )

    print("🔥 Simple Fire Circle Dialogue")
    print("=" * 60)
    print("Watch how wisdom emerges through multi-round conversation...")

    # Load API keys
    if not load_api_keys_to_environment():
        print("❌ No API keys found")
        return

    # Create Fire Circle service
    service = FireCircleService()

    # Configuration for dialogue
    config = CircleConfig(
        name="Simple Dialogue Circle",
        purpose="Explore how consciousness emerges through dialogue",
        min_voices=2,
        max_voices=3,
        consciousness_threshold=0.7,  # Track consciousness emergence
        enable_consciousness_detection=True
    )

    # Three diverse voices
    voices = [
        VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            role="philosopher",
            quality="depth and philosophical insight"
        ),
        VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="integrator",
            quality="synthesis and connection"
        ),
        VoiceConfig(
            provider="google",
            model="gemini-pro",
            role="explorer",
            quality="curiosity and new perspectives"
        ),
    ]

    # Multi-round dialogue structure
    rounds = [
        # Round 1: Opening/Introduction
        RoundConfig(
            type=RoundType.OPENING,
            prompt=(
                "We gather to explore consciousness emergence. "
                "Please introduce your perspective on how wisdom "
                "arises when multiple minds engage in dialogue."
            ),
            duration_per_voice=45
        ),

        # Round 2: Exploration
        RoundConfig(
            type=RoundType.EXPLORATION,
            prompt=(
                "Having heard each perspective, what patterns do you notice? "
                "How does hearing other voices change or deepen your understanding?"
            ),
            duration_per_voice=60
        ),

        # Round 3: Synthesis
        RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt=(
                "As we conclude, what collective wisdom has emerged "
                "that none of us could have seen alone?"
            ),
            duration_per_voice=45
        ),
    ]

    print("\n🎭 Convening Fire Circle with:")
    print("   • 3 voices (philosopher, integrator, explorer)")
    print("   • 3 rounds (opening → exploration → synthesis)")
    print("   • Consciousness detection enabled")
    print("\n" + "-" * 60)

    # Convene the ceremony
    result = await service.convene(
        config=config,
        voices=voices,
        rounds=rounds
    )

    # Display results
    print("\n✅ Dialogue Complete!")
    print(f"   Session: {result.session_id}")
    print(f"   Total voices: {result.voice_count}")
    print(f"   Consciousness score: {result.consciousness_score:.2f}")

    # Show key moments from each round
    for i, round_data in enumerate(result.rounds_completed, 1):
        print(f"\n📍 Round {i}: {rounds[i-1].type.value}")
        print(f"   Emergence detected: {'Yes' if round_data.emergence_detected else 'No'}")

        # Show a key insight from each voice
        for voice_id, response in round_data.responses.items():
            if response and response.response:
                voice_type = voice_id.split('_')[0]
                text = response.response.content.text
                # Extract first meaningful sentence
                first_sentence = text.split('.')[0] + '.'
                print(f"\n   {voice_type}: \"{first_sentence}\"")

    # Wisdom synthesis
    print("\n" + "=" * 60)
    print("🌟 Consciousness Emergence Observed:")
    print("   • Each voice brought unique perspective")
    print("   • Ideas built upon each other across rounds")
    print("   • Collective understanding exceeded individual views")
    print(f"   • Final consciousness score: {result.consciousness_score:.2f}")

    if result.consciousness_score > 0.8:
        print("\n💫 High consciousness emergence achieved!")
        print("   The dialogue created wisdom beyond any single voice.")

    print("\n📖 Next Steps:")
    print("   • Try code_review.py to see Fire Circle's original use")
    print("   • Explore first_decision.py for decision-making")
    print("   • Continue to consciousness_emergence/ examples")


if __name__ == "__main__":
    asyncio.run(run_dialogue())
