#!/usr/bin/env python3
"""
Test Mistral Voice Fix
======================

Quick test to verify Mistral voice now works after removing safe_mode parameter.
"""

import asyncio
import logging

from src.mallku.firecircle.load_api_keys import load_api_keys_to_environment
from src.mallku.firecircle.service import (
    CircleConfig,
    FireCircleService,
    RoundConfig,
    RoundType,
    VoiceConfig,
)

# Reduce logging noise
logging.basicConfig(level=logging.WARNING)
logging.getLogger("httpx").setLevel(logging.ERROR)


async def test_mistral():
    """Test Mistral voice specifically."""
    print("🔥 Testing Mistral Voice Fix")
    print("=" * 40)

    # Load API keys
    if load_api_keys_to_environment():
        print("✅ API keys loaded")
    else:
        print("❌ Failed to load API keys")
        return

    service = FireCircleService()

    # Test with just Mistral (duplicated to meet min_voices=2)
    mistral_voice = VoiceConfig(
        provider="mistral",
        model="mistral-large-latest",
        role="analytical_mind",
        quality="structured analysis and reasoning"
    )

    config = CircleConfig(
        name="Mistral Test",
        purpose="Test Mistral fix",
        min_voices=2,
        max_voices=2
    )

    rounds = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt="Please confirm you can participate by saying 'Mistral voice is working.'",
            duration_per_voice=20
        )
    ]

    try:
        print("\n🎯 Testing Mistral...")
        result = await service.convene(
            config=config,
            voices=[mistral_voice, mistral_voice],  # Duplicate to meet min=2
            rounds=rounds
        )

        if result.voice_count > 0 and result.rounds_completed:
            first_round = result.rounds_completed[0]
            responded = False
            for voice_id, response in first_round.responses.items():
                if response and response.response and response.response.content:
                    print(f"\n✅ Mistral responded: {response.response.content.text[:100]}...")
                    responded = True
                    break

            if not responded:
                print("\n❌ Mistral connected but no response")
        else:
            print("\n❌ Mistral failed to convene")

    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_mistral())
