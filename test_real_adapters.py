#!/usr/bin/env python3
"""Test script for real adapter integration."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mallku.core.secrets import get_secret
from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
from mallku.firecircle.adapters.base import AdapterConfig
from mallku.orchestration.event_bus import ConsciousnessEventBus
from mallku.reciprocity import ReciprocityTracker


async def test_adapters():
    """Test real adapter availability."""
    print("🔥 Testing Fire Circle Real Adapter Integration")
    print("=" * 60)

    # Check API keys
    voices = ["anthropic", "openai", "deepseek", "mistral", "google", "grok", "local"]
    api_key_status = {}

    for voice in voices:
        if voice == "local":
            api_key_status[voice] = True
            continue

        has_key = False
        for key_pattern in [
            f"{voice}_api_key",
            f"{voice}_key",
            f"{voice.upper()}_API_KEY",
        ]:
            key = await get_secret(key_pattern)
            if key:
                has_key = True
                break

        api_key_status[voice] = has_key
        status = "✅" if has_key else "❌"
        print(f"  {status} {voice}")

    # Try to create factory
    print("\n🏭 Creating Adapter Factory...")
    try:
        event_bus = ConsciousnessEventBus()
        reciprocity_tracker = ReciprocityTracker()

        factory = ConsciousAdapterFactory(
            event_bus=event_bus,
            reciprocity_tracker=reciprocity_tracker
        )

        print("✅ Factory created successfully")

        # Check health
        health = await factory.health_check()
        print(f"🔥 Fire Circle ready: {health['fire_circle_ready']}")
        print(f"📋 Supported providers: {', '.join(health['supported_providers'])}")

        # Try to create local adapter (doesn't need API key)
        print("\n🤖 Testing local adapter...")
        try:
            # Local adapter needs backend in extra_config
            config = AdapterConfig(
                api_key="",
                model_name=None,
                extra_config={"backend": "ollama"}
            )
            adapter = await factory.create_adapter("local", config)
            print("✅ Local adapter created successfully")

            # Check if it's connected
            if adapter.is_connected:
                print("✅ Local adapter connected")
            else:
                print("⚠️  Local adapter created but not connected (Ollama may not be running)")
        except Exception as e:
            print(f"❌ Failed to create local adapter: {e}")

    except Exception as e:
        print(f"❌ Failed to create factory: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_adapters())
