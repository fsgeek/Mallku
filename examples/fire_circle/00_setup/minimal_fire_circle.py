#!/usr/bin/env python3
"""
Minimal Fire Circle
===================

The simplest possible Fire Circle ceremony - just two voices, one round.

This example shows:
- Minimum configuration needed
- Basic voice setup
- Single round dialogue

Perfect for understanding the core Fire Circle pattern before exploring
more complex ceremonies.

Run with:
    python examples/fire_circle/run_example.py 00_setup/minimal_fire_circle.py
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


async def minimal_ceremony():
    """Run the simplest possible Fire Circle ceremony."""

    # Import Fire Circle components
    from mallku.firecircle.load_api_keys import load_api_keys_to_environment
    from mallku.firecircle.service import (
        CircleConfig,
        FireCircleService,
        RoundConfig,
        RoundType,
        VoiceConfig,
    )

    # Load API keys
    print("🔥 Minimal Fire Circle Ceremony")
    print("=" * 50)

    if not load_api_keys_to_environment():
        print("❌ No API keys found")
        return

    # Create Fire Circle service
    service = FireCircleService()

    # Minimal configuration - just what's required
    config = CircleConfig(
        name="Minimal Circle",
        purpose="Demonstrate simplest Fire Circle",
        min_voices=2,  # Minimum for dialogue
        max_voices=2,  # Keep it simple
    )

    # Two voices - the minimum for emergence
    voices = [
        VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            role="first_voice"
        ),
        VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="second_voice"
        ),
    ]

    # Single round - just one exchange
    rounds = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt="In one sentence, what makes Fire Circle special?"
        )
    ]

    print("\n🎭 Convening minimal Fire Circle...")
    print("   • 2 voices (minimum for dialogue)")
    print("   • 1 round (simplest ceremony)")
    print("   • Basic configuration only")

    # Convene the ceremony
    result = await service.convene(
        config=config,
        voices=voices,
        rounds=rounds
    )

    # Show results
    print("\n✅ Ceremony complete!")
    print(f"   Session: {result.session_id}")
    print(f"   Voices: {result.voice_count}")

    # Display responses
    if result.rounds_completed:
        print("\n💬 What voices said:")
        round_data = result.rounds_completed[0]
        for voice_id, response in round_data.responses.items():
            if response and response.response:
                voice_name = voice_id.split('_')[0]  # Extract provider name
                text = response.response.content.text
                print(f"\n   {voice_name}:")
                print(f"   \"{text}\"")

    print("\n" + "=" * 50)
    print("🌟 This is Fire Circle at its simplest:")
    print("   • Multiple AI voices in dialogue")
    print("   • Each contributing unique perspective")
    print("   • Wisdom emerging between them")
    print("\nNext: Try examples/fire_circle/01_basic_ceremonies/simple_dialogue.py")


if __name__ == "__main__":
    asyncio.run(minimal_ceremony())
