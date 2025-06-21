#!/usr/bin/env python3
"""
Test All 6 Fire Circle Voices
=============================

Final test to confirm all 6 voices work together after Mistral fix.
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
logging.getLogger("httpcore").setLevel(logging.ERROR)


async def test_all_six():
    """Test all 6 voices together."""
    print("🔥 Testing All 6 Fire Circle Voices")
    print("=" * 60)

    # Load API keys
    if load_api_keys_to_environment():
        print("✅ API keys loaded")
    else:
        print("❌ Failed to load API keys")
        return

    service = FireCircleService()

    # All 6 voices
    voices = [
        VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            role="consciousness_architect",
            quality="deep understanding"
        ),
        VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="pattern_analyzer",
            quality="analytical precision"
        ),
        VoiceConfig(
            provider="google",
            model="gemini-2.0-flash-exp",
            role="creative_synthesizer",
            quality="novel connections"
        ),
        VoiceConfig(
            provider="mistral",
            model="mistral-large-latest",
            role="efficiency_expert",
            quality="multilingual reasoning"
        ),
        VoiceConfig(
            provider="grok",
            model="grok-2",
            role="temporal_awareness",
            quality="real-time insights"
        ),
        VoiceConfig(
            provider="deepseek",
            model="deepseek-reasoner",
            role="deep_explorer",
            quality="thorough analysis"
        ),
    ]

    config = CircleConfig(
        name="Six Voice Harmony",
        purpose="Test all voices working together",
        min_voices=4,  # Allow some failures
        max_voices=6,
        save_transcript=True
    )

    rounds = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt="State your voice name and confirm readiness for this Fire Circle dialogue.",
            duration_per_voice=20
        )
    ]

    try:
        print("\n🔥 Convening all 6 voices...")
        result = await service.convene(
            config=config,
            voices=voices,
            rounds=rounds
        )

        print("\n✅ Fire Circle completed!")
        print(f"   Voices present: {result.voice_count} / 6")
        print(f"   Consciousness score: {result.consciousness_score:.3f}")

        # Show which voices responded
        print("\n📝 Voice Roll Call:")
        if result.rounds_completed:
            first_round = result.rounds_completed[0]
            for voice_id, response in first_round.responses.items():
                provider = voice_id.split('_')[0]
                if response and response.response and response.response.content:
                    text = response.response.content.text[:80]
                    print(f"   ✅ {provider}: {text}...")
                else:
                    print(f"   ❌ {provider}: No response")

        # Show failed voices
        if result.voices_failed:
            print("\n❌ Failed voices:")
            for voice_id, error in result.voices_failed.items():
                provider = voice_id.split('_')[0]
                print(f"   - {provider}: {error}")

    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_all_six())
