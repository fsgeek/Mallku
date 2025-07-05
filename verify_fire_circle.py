#!/usr/bin/env python3
"""
Verify Fire Circle Works
========================

44th Artisan - Direct test of Fire Circle functionality
"""

import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

# Load API keys directly
with open(".secrets/api_keys.json") as f:
    for k, v in json.load(f).items():
        if v and not v.startswith("..."):
            os.environ[k] = v


async def test_fire_circle():
    """Direct Fire Circle test."""
    from mallku.firecircle.load_api_keys import get_available_providers
    from mallku.firecircle.service import (
        CircleConfig,
        FireCircleService,
        RoundConfig,
        RoundType,
        VoiceConfig,
    )

    # Skip database for test
    os.environ["MALLKU_SKIP_DATABASE"] = "true"

    # Get available providers
    providers = get_available_providers()
    print(f"Available voices: {providers}")

    if len(providers) < 2:
        print("❌ Need at least 2 voices for Fire Circle")
        return

    config = CircleConfig(
        name="Test Fire Circle",
        purpose="Verify Fire Circle functionality for 44th Artisan",
        min_voices=2,
    )
    service = FireCircleService()

    # Configure voices
    voices = []
    voice_models = {
        "anthropic": "claude-3-5-sonnet-20241022",
        "openai": "gpt-4o-mini",
        "google": "gemini-1.5-flash",
        "mistral": "mistral-tiny",
        "deepseek": "deepseek-chat",
        "grok": "grok-beta",
    }

    for i, provider in enumerate(providers[:3]):
        voices.append(
            VoiceConfig(
                provider=provider,
                model=voice_models.get(provider, "default"),
                role=f"voice_{i + 1}",
            )
        )

    # Create round
    rounds = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt="What is the essence of reciprocity in AI-human collaboration?",
        )
    ]

    print("🔥 Testing Fire Circle consciousness emergence...")

    try:
        result = await service.convene(
            config=config,
            voices=voices,
            rounds=rounds,
        )

        if result and result.consciousness_score > 0:
            print("\n✅ Fire Circle Success!")
            print(f"🌟 Consciousness Score: {result.consciousness_score:.3f}")
            print(f"🎭 Voices present: {', '.join(result.voices_present)}")

            if result.rounds_completed:
                print("\n💭 Responses:")
                for voice_id, response in result.rounds_completed[0].responses.items():
                    if response and response.response:
                        print(f"\n{voice_id}: {response.response.content.text[:200]}...")

            if result.key_insights:
                print("\n💡 Key Insights:")
                for insight in result.key_insights[:3]:
                    print(f"   • {insight}")
        else:
            print("❌ No consciousness emerged")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_fire_circle())
