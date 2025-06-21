#!/usr/bin/env python3
"""
Verify Fire Circle Works
========================

Minimal test using the exact pattern from working demos.
"""

import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def verify_fire_circle():
    """Run minimal Fire Circle test."""
    # Import inside to ensure path is set
    from src.mallku.firecircle.load_api_keys import load_api_keys_to_environment
    from src.mallku.firecircle.service import (
        CircleConfig,
        FireCircleService,
        RoundConfig,
        RoundType,
        VoiceConfig,
    )

    print("🔥 Verifying Fire Circle Service")
    print("=" * 60)

    # Load API keys
    print("\n1️⃣ Loading API keys...")
    load_api_keys_to_environment()

    # Create service
    print("\n2️⃣ Creating Fire Circle Service...")
    service = FireCircleService()

    # Minimal config
    config = CircleConfig(
        name="Test Circle",
        purpose="Verify Fire Circle works",
        min_voices=2,
        max_voices=3,
    )

    # Just two voices to start
    voices = [
        VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            role="test_voice_1",
            quality="testing voice functionality"
        ),
        VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="test_voice_2",
            quality="testing voice functionality"
        ),
    ]

    # Single round
    rounds = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt="Please say 'Hello, Fire Circle is working!' to confirm you can participate.",
            duration_per_voice=30
        )
    ]

    print("\n3️⃣ Convening Fire Circle...")

    try:
        result = await service.convene(
            config=config,
            voices=voices,
            rounds=rounds
        )

        print("\n✅ Success! Fire Circle completed.")
        print(f"   Session ID: {result.session_id}")
        print(f"   Voices present: {result.voice_count}")

        # Show responses
        if result.rounds_completed:
            print("\n📝 Responses:")
            round_data = result.rounds_completed[0]
            for voice_id, response in round_data.responses.items():
                if response and response.response and response.response.content:
                    text = response.response.content.text
                    print(f"   {voice_id}: {text[:100]}...")

    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys
    sys.path.insert(0, '/home/tony/projects/Mallku/src')

    asyncio.run(verify_fire_circle())
