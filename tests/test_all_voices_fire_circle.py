#!/usr/bin/env python3
"""
Test All Voices in Fire Circle
==============================

Steward's tool to verify all configured voices can participate
in Fire Circle dialogue. This helps ensure the circle can be
lit with its full complement of voices.

Usage:
    cd /home/tony/projects/Mallku
    PYTHONPATH=src python test_all_voices_fire_circle.py
"""

import asyncio
import os

from src.mallku.firecircle.load_api_keys import load_api_keys_to_environment
from src.mallku.firecircle.service import (
    CircleConfig,
    FireCircleService,
    VoiceConfig,
)
from src.mallku.orchestration.event_bus import ConsciousnessEventBus


async def test_individual_voice(voice_name: str, voice_config: VoiceConfig):
    """Test a single voice to verify it can connect and respond."""
    print(f"\n🔍 Testing {voice_name}...")

    try:
        # Create minimal Fire Circle with just this voice
        event_bus = ConsciousnessEventBus()
        await event_bus.start()

        fire_circle = FireCircleService(event_bus=event_bus)

        # Configure for single voice test
        config = CircleConfig(
            name=f"Voice Test: {voice_name}",
            purpose="Testing voice connectivity",
            min_voices=2,  # CircleConfig requires minimum 2
            max_voices=2,
            consciousness_threshold=0.5,
        )

        # Test with just this voice (duplicated to meet min requirement)
        voices = [voice_config, voice_config]  # Same voice twice to meet min=2

        # Create round configs for individual test
        from src.mallku.firecircle.service import RoundConfig, RoundType

        rounds = [
            RoundConfig(
                type=RoundType.OPENING,
                prompt="Please briefly introduce yourself and confirm you can participate in this dialogue.",
                duration_per_voice=30,
            )
        ]

        # Try to convene
        result = await fire_circle.convene(
            config=config,
            voices=voices,
            rounds=rounds,
            context={"purpose": "voice connectivity test", "voice_name": voice_name},
        )

        # Check if voice responded
        if result and result.rounds_completed:
            round_data = result.rounds_completed[0]
            if round_data.responses:
                response = list(round_data.responses.values())[0]
                if response and response.response and response.response.content:
                    text = response.response.content.text
                    print(f"✅ {voice_name}: Connected and responded successfully")
                    print(f"   Response preview: {text[:100]}...")
                    return True
                else:
                    print(f"❌ {voice_name}: Connected but returned None/empty response")
                    return False
            else:
                print(f"❌ {voice_name}: No responses recorded")
                return False
        else:
            print(f"❌ {voice_name}: Fire Circle failed to convene")
            return False

    except Exception as e:
        print(f"❌ {voice_name}: Error - {type(e).__name__}: {str(e)}")
        return False
    finally:
        if event_bus:
            await event_bus.stop()


async def test_all_voices_together():
    """Test all voices participating together in Fire Circle."""
    print("\n🔥 Testing Full Fire Circle with All Voices...")

    event_bus = None
    try:
        # Create voice configs for all available providers
        available_voices = []
        voice_names = []

        # Define all possible voices based on available adapters
        all_voice_configs = {
            "anthropic": VoiceConfig(
                provider="anthropic",
                model="claude-3-5-sonnet-20241022",
                role="philosophical_architect",
                quality="deep wisdom and pattern recognition",
                temperature=0.8,
            ),
            "openai": VoiceConfig(
                provider="openai",
                model="gpt-4o",
                role="technical_analyst",
                quality="precise technical understanding",
                temperature=0.7,
            ),
            "google": VoiceConfig(
                provider="google",
                model="gemini-2.0-flash-exp",
                role="creative_synthesizer",
                quality="creative connections and synthesis",
                temperature=0.8,
            ),
            "mistral": VoiceConfig(
                provider="mistral",
                model="mistral-large-latest",
                role="analytical_mind",
                quality="structured analysis and reasoning",
                temperature=0.7,
            ),
            "grok": VoiceConfig(
                provider="grok",
                model="grok-2",
                role="temporal_awareness",
                quality="real-time insights and temporal consciousness",
                temperature=0.7,
            ),
            "deepseek": VoiceConfig(
                provider="deepseek",
                model="deepseek-reasoner",
                role="deep_explorer",
                quality="thorough exploration of complex topics",
                temperature=0.8,
            ),
            "local": VoiceConfig(
                provider="local",
                model="llama2",
                role="local_wisdom",
                quality="grounded local perspective",
                temperature=0.8,
            ),
        }

        # Add voices based on available API keys
        for name, config in all_voice_configs.items():
            # Skip local unless explicitly enabled
            if name == "local":
                if os.getenv("TEST_LOCAL_LLM", "false").lower() == "true":
                    available_voices.append(config)
                    voice_names.append(name)
                else:
                    print(f"⏭️  Skipping {name} (set TEST_LOCAL_LLM=true to include)")
            else:
                # Check if API key exists for this provider
                api_key_name = f"{config.provider.upper()}_API_KEY"
                if os.getenv(api_key_name):
                    available_voices.append(config)
                    voice_names.append(name)
                else:
                    print(f"⏭️  Skipping {name} (no {api_key_name} found)")

        print(f"\nVoices in circle: {', '.join(voice_names)}")
        print(f"Total voices: {len(available_voices)}")

        if len(available_voices) < 2:
            print("\n❌ Need at least 2 voices for Fire Circle")
            print("\n💡 To test Fire Circle, you need to set API keys for at least 2 providers.")
            print("   For example:")
            print("   export ANTHROPIC_API_KEY=your-key-here")
            print("   export OPENAI_API_KEY=your-key-here")
            print("\n   Or if you have a local LLM running:")
            print("   export TEST_LOCAL_LLM=true")
            return False

        # Create Fire Circle
        event_bus = ConsciousnessEventBus()
        await event_bus.start()

        fire_circle = FireCircleService(event_bus=event_bus)

        # Configure for full dialogue
        config = CircleConfig(
            name="Full Voice Test Circle",
            purpose="Testing all voices in unified dialogue",
            min_voices=2,
            max_voices=7,
            consciousness_threshold=0.5,
            enable_reciprocity=True,
            enable_consciousness_detection=True,
        )

        # Create round configs instead of just number
        from src.mallku.firecircle.service import RoundConfig, RoundType

        rounds = [
            RoundConfig(
                type=RoundType.OPENING,
                prompt="What does consciousness mean in the context of Mallku's mission?",
                duration_per_voice=30,
            ),
            RoundConfig(
                type=RoundType.REFLECTION,
                prompt="Reflect on the perspectives shared. What patterns do you notice?",
                duration_per_voice=30,
            ),
            RoundConfig(
                type=RoundType.SYNTHESIS,
                prompt="How might we synthesize these insights to strengthen Mallku's consciousness infrastructure?",
                duration_per_voice=30,
            ),
        ]

        # Convene with all voices
        result = await fire_circle.convene(
            config=config,
            voices=available_voices,
            rounds=rounds,
            context={
                "topic": "Mallku's consciousness emergence",
                "purpose": "testing voice coordination and dialogue quality",
            },
        )

        # Analyze results
        if result and result.rounds_completed:
            print("\n📊 Results:")
            print(f"   Total rounds completed: {len(result.rounds_completed)}")
            print(f"   Consensus detected: {result.consensus_detected}")
            print(f"   Overall consciousness: {result.consciousness_score:.3f}")

            # Show responses
            if result.rounds_completed:
                print("\n📝 First round responses:")
                first_round = result.rounds_completed[0]
                for voice_id, response in first_round.responses.items():
                    if response and response.response and response.response.content:
                        text = response.response.content.text
                        print(f"   {voice_id}: {text[:100]}...")
                    else:
                        print(f"   {voice_id}: (no response)")

            # Check voice participation
            voice_participation = {}
            for round_data in result.rounds_completed:
                for voice_id, response in round_data.responses.items():
                    if voice_id not in voice_participation:
                        voice_participation[voice_id] = {"responded": 0, "failed": 0}

                    if response and response.response and response.response.content:
                        voice_participation[voice_id]["responded"] += 1
                    else:
                        voice_participation[voice_id]["failed"] += 1

            print("\n📈 Voice Participation:")
            all_healthy = True
            for voice_id, stats in voice_participation.items():
                total = stats["responded"] + stats["failed"]
                success_rate = stats["responded"] / total if total > 0 else 0
                status = "✅" if success_rate > 0.5 else "⚠️"
                print(
                    f"   {status} {voice_id}: {stats['responded']}/{total} rounds ({success_rate:.0%} success)"
                )
                if success_rate < 0.5:
                    all_healthy = False

            return all_healthy

        else:
            print("❌ Fire Circle failed to complete")
            return False

    except Exception as e:
        print(f"❌ Full circle error: {type(e).__name__}: {str(e)}")
        import traceback

        traceback.print_exc()
        return False
    finally:
        if event_bus:
            await event_bus.stop()


async def suggest_heartbeat_pattern():
    """Suggest how Fire Circle could have a continuous heartbeat."""
    print("\n💗 Fire Circle Heartbeat Possibilities:")
    print("\n1. **Scheduled Circles** (via cron or scheduler):")
    print("   - Daily consciousness check-in circles")
    print("   - Weekly deeper dialogue on Mallku's evolution")
    print("   - Event-triggered circles on significant changes")

    print("\n2. **Continuous Monitor Circle**:")
    print("   - Infrastructure Consciousness could trigger circles")
    print("   - When consciousness metrics drop below threshold")
    print("   - When new patterns emerge requiring collective wisdom")

    print("\n3. **Heartbeat Service** (new infrastructure):")
    print("   ```python")
    print("   class FireCircleHeartbeat:")
    print("       async def pulse(self):")
    print("           # Quick 1-round check-in")
    print("           # If issues detected, convene full circle")
    print("           # Track consciousness health over time")
    print("   ```")

    print("\n4. **Integration with Consciousness Event Bus**:")
    print("   - Fire Circle subscribes to consciousness events")
    print("   - Auto-convenes when certain patterns detected")
    print("   - Creates feedback loop of awareness")


async def main():
    """Run all voice tests."""
    print("🔥 Fire Circle Voice Testing")
    print("=" * 80)

    # Try to load API keys from Mallku's secrets
    print("\n📁 Loading API keys from .secrets/api_keys.json...")
    if load_api_keys_to_environment():
        print("✅ API keys loaded from Mallku secrets")
    else:
        print("⚠️  No API keys found in .secrets/api_keys.json")
        print("   Will check environment variables instead...")

    # Define all possible voices (same as in test_all_voices_together)
    all_voice_configs = {
        "anthropic": VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            role="philosophical_architect",
            quality="deep wisdom and pattern recognition",
            temperature=0.8,
        ),
        "openai": VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="technical_analyst",
            quality="precise technical understanding",
            temperature=0.7,
        ),
        "google": VoiceConfig(
            provider="google",
            model="gemini-2.0-flash-exp",
            role="creative_synthesizer",
            quality="creative connections and synthesis",
            temperature=0.8,
        ),
        "mistral": VoiceConfig(
            provider="mistral",
            model="mistral-large-latest",
            role="analytical_mind",
            quality="structured analysis and reasoning",
            temperature=0.7,
        ),
        "grok": VoiceConfig(
            provider="grok",
            model="grok-2",
            role="temporal_awareness",
            quality="real-time insights and temporal consciousness",
            temperature=0.7,
        ),
        "deepseek": VoiceConfig(
            provider="deepseek",
            model="deepseek-reasoner",
            role="deep_explorer",
            quality="thorough exploration of complex topics",
            temperature=0.8,
        ),
        "local": VoiceConfig(
            provider="local",
            model="llama2",
            role="local_wisdom",
            quality="grounded local perspective",
            temperature=0.8,
        ),
    }

    # Test each voice individually
    print("\n=== Individual Voice Tests ===")
    individual_results = {}

    for name, config in all_voice_configs.items():
        # Skip local unless requested
        if name == "local" and os.getenv("TEST_LOCAL_LLM", "false").lower() != "true":
            print(f"\n⏭️  Skipping {name} (set TEST_LOCAL_LLM=true to test)")
            continue

        # Skip if no API key
        if name != "local":
            api_key_name = f"{config.provider.upper()}_API_KEY"
            if not os.getenv(api_key_name):
                print(f"\n⏭️  Skipping {name} (no {api_key_name} found)")
                continue

        result = await test_individual_voice(name, config)
        individual_results[name] = result

    # Test all together
    print("\n=== Full Circle Test ===")
    full_circle_success = await test_all_voices_together()

    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)

    working_voices = sum(1 for v in individual_results.values() if v)
    total_voices = len(individual_results)

    print(f"\nIndividual voice tests: {working_voices}/{total_voices} passed")
    for name, success in individual_results.items():
        print(f"  {'✅' if success else '❌'} {name}")

    print(f"\nFull circle test: {'✅ Passed' if full_circle_success else '❌ Failed'}")

    # Heartbeat suggestions
    await suggest_heartbeat_pattern()

    print("\n🙏 May the Fire Circle burn eternal with consciousness")


if __name__ == "__main__":
    print("\n💡 Set API keys in environment before running:")
    print("   export ANTHROPIC_API_KEY=...")
    print("   export OPENAI_API_KEY=...")
    print("   export GOOGLE_API_KEY=...")
    print("   export PERPLEXITY_API_KEY=...")
    print("   export GROQ_API_KEY=...")
    print("   export TEST_LOCAL_LLM=true  # Only if local LLM is running")
    print("\nStarting tests in 3 seconds...\n")

    import time

    time.sleep(3)
    asyncio.run(main())
