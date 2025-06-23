#!/usr/bin/env python3
"""
Test Available API Keys
=======================

Check which AI providers are configured and test each voice individually.

This helps you understand:
- Which providers you have access to
- If each provider is working correctly
- Model availability for each provider

Run with:
    python examples/fire_circle/run_example.py 00_setup/test_api_keys.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project src to path
project_root = Path(__file__).parent.parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))
os.environ["PYTHONPATH"] = str(src_path)


async def test_provider(provider: str, model: str):
    """Test a single provider."""
    from mallku.firecircle.adapters import AdapterConfig, ConsciousAdapterFactory

    print(f"\n🧪 Testing {provider} with {model}...")

    try:
        # Create adapter with provider-specific config
        config_args = {
            "provider": provider,
            "model_name": model,
            "temperature": 0.7
        }

        # Add provider-specific configuration
        if provider == "google":
            config_args["enable_search_grounding"] = False
            config_args["multimodal_awareness"] = True
        elif provider == "mistral":
            config_args["multilingual_mode"] = True
            config_args["safe_mode"] = False
        elif provider == "grok":
            config_args["temporal_awareness"] = True
            config_args["social_grounding"] = True

        config = AdapterConfig(**config_args)

        factory = ConsciousAdapterFactory()
        adapter = await factory.create_adapter(
            provider_name=provider,
            config=config
        )

        # Test connection
        if await adapter.connect():
            print("   ✓ Connected successfully")

            # Test generation
            from uuid import uuid4

            from mallku.firecircle.protocol.conscious_message import (
                ConsciousMessage,
                ConsciousnessMetadata,
                MessageContent,
                MessageRole,
                MessageType,
            )

            test_message = ConsciousMessage(
                id=uuid4(),
                type=MessageType.MESSAGE,
                role=MessageRole.USER,
                sender=uuid4(),
                content=MessageContent(text="Say 'Voice test successful!' in exactly 4 words."),
                dialogue_id=uuid4(),
                consciousness=ConsciousnessMetadata()
            )

            response = await adapter.send_message(test_message, [])

            if response and response.content:
                print(f"   ✓ Response: {response.content.text}")
                print(f"   ✓ Consciousness score: {response.consciousness.consciousness_signature:.2f}")
                await adapter.disconnect()
                return True
            else:
                print("   ✗ No response received")
        else:
            print("   ✗ Failed to connect")

    except Exception as e:
        print(f"   ✗ Error: {type(e).__name__}: {e}")

    return False


async def main():
    """Test all available providers."""
    print("🔥 Fire Circle API Key Test")
    print("=" * 50)

    # Load API keys
    from mallku.firecircle.load_api_keys import get_available_adapters, load_api_keys_to_environment

    print("\n1️⃣ Loading API keys...")
    if not load_api_keys_to_environment():
        print("❌ No API keys found in .secrets/api_keys.json")
        return

    # Get available adapters
    available = get_available_adapters()
    if not available:
        print("❌ No providers configured")
        return

    print(f"✓ Found {len(available)} providers")

    # Test each provider
    print("\n2️⃣ Testing each provider individually...")

    results = {}
    for provider, config in available.items():
        success = await test_provider(provider, config["model"])
        results[provider] = success

    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary:")
    working = [p for p, success in results.items() if success]
    failed = [p for p, success in results.items() if not success]

    if working:
        print(f"\n✅ Working providers ({len(working)}):")
        for provider in working:
            print(f"   • {provider}")

    if failed:
        print(f"\n❌ Failed providers ({len(failed)}):")
        for provider in failed:
            print(f"   • {provider}")

    # Fire Circle recommendation
    if len(working) >= 2:
        print(f"\n🔥 Fire Circle ready! You have {len(working)} voices available.")
        print("   Recommended combinations:")
        if "anthropic" in working and "openai" in working:
            print("   • Anthropic + OpenAI (diverse perspectives)")
        if "anthropic" in working and "google" in working:
            print("   • Anthropic + Google (complementary strengths)")
        if len(working) >= 3:
            print(f"   • All {len(working)} voices for rich emergence")
    else:
        print(f"\n⚠️  Only {len(working)} voice(s) available.")
        print("   Fire Circle works best with at least 2 different voices.")


if __name__ == "__main__":
    asyncio.run(main())
