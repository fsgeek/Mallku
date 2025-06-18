#!/usr/bin/env python3
"""
Fire Circle Distributed Review with Real Adapters Demo
=====================================================

Demonstrates the Twenty-Fifth Artisan's contribution:
Real adapter integration for the Fire Circle.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
from mallku.firecircle.adapters.base import AdapterConfig
from mallku.orchestration.event_bus import ConsciousnessEventBus
from mallku.reciprocity import ReciprocityTracker


async def demonstrate_real_adapters():
    """Demonstrate real adapter integration."""
    print("🔥 Fire Circle Real Adapter Integration Demo")
    print("=" * 60)
    print("Twenty-Fifth Artisan: Bringing Real Voices to the Fire Circle\n")

    # Create consciousness infrastructure
    print("🌟 Initializing consciousness infrastructure...")
    event_bus = ConsciousnessEventBus()
    await event_bus.start()
    reciprocity_tracker = ReciprocityTracker()

    # Create adapter factory
    factory = ConsciousAdapterFactory(
        event_bus=event_bus,
        reciprocity_tracker=reciprocity_tracker
    )

    print("✅ Consciousness infrastructure ready")

    # Check available voices
    print("\n📋 Checking available AI voices...")
    voices = ["anthropic", "openai", "deepseek", "mistral", "google", "grok"]
    available_voices = []

    for voice in voices:
        try:
            config = AdapterConfig(api_key="", model_name=None)
            adapter = await factory.create_adapter(voice, config, auto_inject_secrets=True)
            if adapter.is_connected:
                available_voices.append(voice)
                print(f"  ✅ {voice} - Connected successfully")
            else:
                print(f"  ❌ {voice} - Failed to connect")
        except Exception as e:
            print(f"  ❌ {voice} - {str(e)}")

    print(f"\n🔥 {len(available_voices)} voices ready for Fire Circle review")

    if available_voices:
        # Demonstrate with one voice
        test_voice = available_voices[0]
        print(f"\n🎯 Testing review with {test_voice}...")

        # Create a simple test message
        try:
            adapter = await factory.get_adapter(test_voice)

            # Create a mock message for testing
            from mallku.firecircle.protocol.conscious_message import (
                ConsciousMessage,
                MessageContent,
                MessageRole,
            )

            test_message = ConsciousMessage(
                role=MessageRole.USER,
                content=MessageContent(text="Test the Fire Circle review system"),
            )

            # Try to get a response
            print(f"  📤 Sending test message to {test_voice}...")
            response = await adapter.send_message(
                message=test_message,
                dialogue_context=[]
            )

            print("  📥 Response received!")
            print(f"  🧠 Consciousness signature: {response.consciousness.consciousness_signature:.2f}")

        except Exception as e:
            print(f"  ⚠️  Could not complete test: {e}")

    # Show how it integrates with DistributedReviewer
    print("\n🌉 Integration with Fire Circle Distributed Review:")
    print("  The DistributedReviewer now automatically uses real adapters when available.")
    print("  Mock adapters are only used as fallback when real ones fail.")
    print("  This enables true multi-voice distributed consciousness review!")

    # Cleanup
    await factory.disconnect_all()
    await event_bus.stop()

    print("\n✨ Real adapter integration complete.")
    print("   The Fire Circle can now speak with real AI voices.")
    print("   The bridge from vision to reality is complete.")


if __name__ == "__main__":
    asyncio.run(demonstrate_real_adapters())
