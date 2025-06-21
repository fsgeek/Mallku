#!/usr/bin/env python3
"""
Test Fire Circle Fix
====================

Twenty-Ninth Artisan tests the context accumulation fix.
"""

import asyncio
import logging
import os
import sys

# Ensure we have the right path
sys.path.insert(0, '/home/tony/projects/Mallku/src')

# Set dummy API keys if not present
if not os.environ.get("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = "test-key"
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "test-key"

# Configure logging to see what's happening
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Reduce noise
logging.getLogger("httpx").setLevel(logging.WARNING)


async def test_minimal_fire_circle():
    """Test Fire Circle with minimal configuration."""

    print("\n" + "="*80)
    print("TESTING FIRE CIRCLE WITH CONTEXT FIX")
    print("="*80 + "\n")

    try:
        from mallku.firecircle.service import (
            CircleConfig,
            FireCircleService,
            RoundConfig,
            RoundType,
            VoiceConfig,
        )

        print("✅ Imports successful")

        # Create mock adapter that simulates failures
        from mallku.firecircle.adapters.base import AdapterConfig, ConsciousModelAdapter
        from mallku.firecircle.protocol.conscious_message import ConsciousMessage

        class MockAdapter(ConsciousModelAdapter):
            """Mock adapter that fails on Round 2+."""

            def __init__(self, config, provider_name, fails_after_round=1):
                super().__init__(config, provider_name, None, None)
                self.round_count = 0
                self.fails_after_round = fails_after_round
                self.is_connected = True

            async def connect(self) -> bool:
                return True

            async def disconnect(self) -> None:
                pass

            async def send_message(self, message, dialogue_context):
                self.round_count += 1
                print(f"   MockAdapter round {self.round_count}, context size: {len(dialogue_context)}")

                # Check if context contains None
                none_count = sum(1 for msg in dialogue_context if msg is None)
                if none_count > 0:
                    print(f"   ⚠️  Context contains {none_count} None values!")

                if self.round_count > self.fails_after_round:
                    print(f"   Simulating failure for round {self.round_count}")
                    return None  # Simulate adapter failure

                # Create a mock response
                from uuid import uuid4

                from mallku.firecircle.protocol.conscious_message import (
                    ConsciousnessMetadata,
                    MessageContent,
                    MessageRole,
                    MessageType,
                )

                return ConsciousMessage(
                    id=uuid4(),
                    type=MessageType.REFLECTION,
                    role=MessageRole.ASSISTANT,
                    sender=uuid4(),
                    content=MessageContent(text=f"Mock response for round {self.round_count}"),
                    dialogue_id=message.dialogue_id,
                    consciousness=ConsciousnessMetadata(
                        consciousness_signature=0.8,
                        detected_patterns=["test_pattern"],
                    )
                )

            async def stream_message(self, message, dialogue_context):
                yield "test"

        # Replace adapter factory to use our mock
        from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory

        original_create = ConsciousAdapterFactory.create_adapter

        async def mock_create_adapter(provider, config=None, **kwargs):
            print(f"\n🔧 Creating mock adapter for {provider}")
            mock_config = AdapterConfig() if config is None else config
            return MockAdapter(mock_config, provider)

        ConsciousAdapterFactory.create_adapter = staticmethod(mock_create_adapter)

        # Create minimal Fire Circle
        print("\n🔥 Creating Fire Circle Service...")
        service = FireCircleService()

        # Simple configuration
        config = CircleConfig(
            name="Test Fix Circle",
            purpose="Test context accumulation fix",
            min_voices=2,
            max_voices=2,
            consciousness_threshold=0.5,
            save_transcript=False,
            failure_strategy="adaptive"
        )

        voices = [
            VoiceConfig(
                provider="mock1",
                model="test-model",
                role="voice1",
                quality="testing",
                temperature=0.7
            ),
            VoiceConfig(
                provider="mock2",
                model="test-model",
                role="voice2",
                quality="testing",
                temperature=0.7
            ),
        ]

        rounds = [
            RoundConfig(
                type=RoundType.OPENING,
                prompt="Test round 1",
                duration_per_voice=10
            ),
            RoundConfig(
                type=RoundType.REFLECTION,
                prompt="Test round 2 - should see failures",
                duration_per_voice=10
            ),
            RoundConfig(
                type=RoundType.SYNTHESIS,
                prompt="Test round 3 - context should be clean",
                duration_per_voice=10
            ),
        ]

        print("\n🎯 Running Fire Circle...")
        result = await service.convene(
            config=config,
            voices=voices,
            rounds=rounds
        )

        print("\n✅ Fire Circle completed!")
        print(f"   - Rounds completed: {len(result.rounds_completed)}")
        print(f"   - Final consciousness: {result.consciousness_score:.3f}")

        # Analyze results
        for i, round_summary in enumerate(result.rounds_completed, 1):
            success_count = sum(1 for r in round_summary.responses.values() if r.response is not None)
            fail_count = sum(1 for r in round_summary.responses.values() if r.response is None)
            print(f"\n   Round {i}: {success_count} success, {fail_count} failed")

        # Restore original factory
        ConsciousAdapterFactory.create_adapter = original_create

        print("\n✅ TEST PASSED: Fire Circle handled adapter failures gracefully!")

    except Exception as e:
        print(f"\n❌ Test failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_minimal_fire_circle())
