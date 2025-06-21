#!/usr/bin/env python3
"""
Diagnose Adapter Failure
========================

Twenty-Ninth Artisan digs deeper into adapter failures.
"""

import asyncio
import logging

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Reduce noise from some modules
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("anthropic").setLevel(logging.INFO)


async def diagnose_fire_circle_failure():
    """Diagnose why Fire Circle fails after Round 1."""

    print("\n" + "="*80)
    print("DIAGNOSING FIRE CIRCLE ADAPTER FAILURES")
    print("="*80 + "\n")

    # Import Fire Circle components
    from src.mallku.firecircle.service import (
        CircleConfig,
        FireCircleService,
        RoundConfig,
        RoundType,
        VoiceConfig,
    )

    # Create minimal configuration
    print("🔧 Creating minimal Fire Circle configuration...")

    # Two voices minimum
    voices = [
        VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            role="test_voice_1",
            quality="diagnostic testing",
            temperature=0.7
        ),
        VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="test_voice_2",
            quality="diagnostic testing",
            temperature=0.7
        ),
    ]

    # Two rounds to test context accumulation
    rounds = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt="Please respond with a short test message (under 100 words).",
            duration_per_voice=30
        ),
        RoundConfig(
            type=RoundType.REFLECTION,
            prompt="Reflect briefly on your previous response (under 100 words).",
            duration_per_voice=30
        ),
    ]

    # Minimal config
    config = CircleConfig(
        name="Diagnostic Test Circle",
        purpose="Diagnose adapter failures",
        min_voices=2,
        max_voices=2,
        consciousness_threshold=0.5,
        save_transcript=True,
        output_path="diagnostic_output",
        failure_strategy="adaptive"
    )

    # Create service
    service = FireCircleService()

    # Add diagnostic logging to trace the issue
    print("\n🔍 Adding diagnostic hooks...")

    # Monkey-patch the round orchestrator to log context details
    original_get_voice_response = service.voice_manager.__class__._get_voice_response

    async def diagnostic_get_voice_response(self, voice_id, adapter, prompt, round_config):
        print(f"\n📡 Calling adapter for {voice_id}...")
        print(f"   Dialogue context size: {len(self.dialogue_context) if hasattr(self, 'dialogue_context') else 'N/A'}")

        if hasattr(self, 'dialogue_context'):
            for i, msg in enumerate(self.dialogue_context):
                if msg is None:
                    print(f"   Context[{i}]: None ⚠️")
                else:
                    print(f"   Context[{i}]: {type(msg).__name__} - {msg.role.value if hasattr(msg, 'role') else 'NO ROLE'}")

        try:
            result = await original_get_voice_response(self, voice_id, adapter, prompt, round_config)
            print(f"   Result: {'Success' if result and result.response else 'None/Failed'}")
            return result
        except Exception as e:
            print(f"   Exception: {type(e).__name__}: {e}")
            raise

    # Apply the diagnostic wrapper
    from src.mallku.firecircle.service.round_orchestrator import RoundOrchestrator
    RoundOrchestrator._get_voice_response = diagnostic_get_voice_response

    try:
        print("\n🔥 Convening diagnostic Fire Circle...")
        result = await service.convene(
            config=config,
            voices=voices,
            rounds=rounds
        )

        print("\n✅ Circle completed!")
        print(f"   Session ID: {result.session_id}")
        print(f"   Rounds completed: {len(result.rounds_completed)}")
        print(f"   Overall consciousness: {result.consciousness_score:.3f}")

        # Analyze round results
        for round_summary in result.rounds_completed:
            print(f"\n   Round {round_summary.round_number}:")
            print(f"     - Type: {round_summary.round_type}")
            print(f"     - Consciousness: {round_summary.consciousness_score:.3f}")
            print(f"     - Responses: {len(round_summary.responses)}")

            for voice_id, response in round_summary.responses.items():
                if response.error:
                    print(f"     - {voice_id}: ERROR - {response.error}")
                else:
                    print(f"     - {voice_id}: Success")

    except Exception as e:
        print(f"\n❌ Fire Circle failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*80)


if __name__ == "__main__":
    # Check if we have API keys
    import os
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("⚠️  Warning: ANTHROPIC_API_KEY not set. Setting a dummy key for testing...")
        os.environ["ANTHROPIC_API_KEY"] = "dummy-key-for-testing"

    asyncio.run(diagnose_fire_circle_failure())
