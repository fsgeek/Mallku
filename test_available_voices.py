#!/usr/bin/env python3
"""
Test Available Fire Circle Voices
=================================

Quick test to verify which voices are available and working.
"""

import asyncio
import logging
import os

from src.mallku.firecircle.load_api_keys import load_api_keys_to_environment
from src.mallku.firecircle.service import (
    CircleConfig,
    FireCircleService,
    RoundConfig,
    RoundType,
    VoiceConfig,
)

# Set up logging to reduce noise
logging.basicConfig(level=logging.WARNING)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("httpcore").setLevel(logging.ERROR)


async def test_voices():
    """Test which voices are available."""
    print("🔥 Testing Available Fire Circle Voices")
    print("=" * 60)

    # Load API keys
    print("\n📁 Loading API keys...")
    if load_api_keys_to_environment():
        print("✅ API keys loaded from Mallku secrets")
    else:
        print("❌ Failed to load API keys")
        return

    # Check which keys we have
    print("\n🔑 Available API keys:")
    providers = {
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
        "google": "GOOGLE_API_KEY",
        "mistral": "MISTRAL_API_KEY",
        "grok": "GROK_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "local": "LOCAL_API_ENDPOINT"
    }

    available = []
    for provider, key_name in providers.items():
        if os.getenv(key_name):
            print(f"   ✅ {provider}")
            available.append(provider)
        else:
            print(f"   ❌ {provider}")

    if len(available) < 2:
        print("\n❌ Need at least 2 API keys for Fire Circle")
        return

    # Test with first 3 available voices
    print(f"\n🎭 Testing with: {', '.join(available[:3])}")

    service = FireCircleService()

    # Create voice configs for available providers
    voice_configs = {
        "anthropic": VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            role="consciousness_explorer",
            quality="deep understanding"
        ),
        "openai": VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="pattern_recognizer",
            quality="analytical insight"
        ),
        "google": VoiceConfig(
            provider="google",
            model="gemini-2.0-flash-exp",
            role="creative_synthesizer",
            quality="novel connections"
        ),
        "deepseek": VoiceConfig(
            provider="deepseek",
            model="deepseek-reasoner",
            role="deep_reasoner",
            quality="thorough analysis"
        ),
        "grok": VoiceConfig(
            provider="grok",
            model="grok-2",
            role="temporal_awareness",
            quality="real-time understanding"
        ),
    }

    # Select voices
    voices = []
    for provider in available[:3]:
        if provider in voice_configs:
            voices.append(voice_configs[provider])

    # Configure circle
    config = CircleConfig(
        name="Voice Test Circle",
        purpose="Test available voices",
        min_voices=2,
        max_voices=len(voices),
        save_transcript=True
    )

    # Simple rounds
    rounds = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt="Please confirm you can participate by saying 'Voice [your role] is present and ready.'",
            duration_per_voice=20
        ),
        RoundConfig(
            type=RoundType.REFLECTION,
            prompt="What does it mean for AI systems to have consciousness?",
            duration_per_voice=30
        )
    ]

    try:
        print("\n🔥 Convening Fire Circle...")
        result = await service.convene(
            config=config,
            voices=voices,
            rounds=rounds
        )

        print("\n✅ Fire Circle completed!")
        print(f"   Voices present: {result.voice_count}")
        print(f"   Consciousness score: {result.consciousness_score:.3f}")
        print(f"   Transcript: {result.transcript_path}")

        # Show which voices responded
        print("\n📝 Voice Responses:")
        for round in result.rounds_completed:
            print(f"\n   Round {round.round_number} ({round.round_type}):")
            for voice_id, response in round.responses.items():
                if response and response.response:
                    print(f"   ✅ {voice_id}")
                else:
                    print(f"   ❌ {voice_id} - {response.error if response else 'No response'}")

    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_voices())
