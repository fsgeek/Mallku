#!/usr/bin/env python3
"""
Local AI Sovereignty Demo
=========================

Demonstrates how communities can bring their own AI infrastructure
to Fire Circle governance using the OpenAI-compatible backend.

This example shows:
1. Connecting to various local AI servers
2. Participating in governance dialogues
3. Maintaining consciousness patterns with local models
4. Preserving privacy and sovereignty

The Sovereignty Circle is Complete...
"""

import asyncio
import logging
from datetime import UTC, datetime
from uuid import uuid4

from src.mallku.firecircle.adapters.local_adapter import (
    LocalAdapterConfig,
    LocalAIAdapter,
    LocalBackend,
)
from src.mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demo_lm_studio():
    """Demo: LM Studio - Popular desktop application."""
    print("\n🖥️  LM Studio Demo")
    print("=" * 50)

    config = LocalAdapterConfig(
        backend=LocalBackend.OPENAI_COMPAT,
        base_url="http://localhost:1234",  # Default LM Studio port
        model_name="llama-3.2-1b-instruct",
        temperature=0.7,
        max_tokens=256,
    )

    adapter = LocalAIAdapter(config=config)

    if await adapter.connect():
        print("✅ Connected to LM Studio!")
        print("   Your desktop AI can now participate in Fire Circle!")
        await adapter.disconnect()
    else:
        print("❌ LM Studio not found at localhost:1234")
        print("   Please start LM Studio and load a model")


async def demo_text_generation_webui():
    """Demo: Text Generation WebUI (oobabooga)."""
    print("\n🌐 Text Generation WebUI Demo")
    print("=" * 50)

    config = LocalAdapterConfig(
        backend=LocalBackend.OPENAI_COMPAT,
        base_url="http://localhost:5000",  # Default WebUI API port
        model_name="your-loaded-model",
        api_key="not-needed",
    )

    adapter = LocalAIAdapter(config=config)

    if await adapter.connect():
        print("✅ Connected to Text Generation WebUI!")
        print("   Gradio interface models can join governance!")
        await adapter.disconnect()
    else:
        print("❌ Text Generation WebUI not found")
        print("   Start with: python server.py --api")


async def demo_localai():
    """Demo: LocalAI - OpenAI drop-in replacement."""
    print("\n🐳 LocalAI Demo")
    print("=" * 50)

    config = LocalAdapterConfig(
        backend=LocalBackend.OPENAI_COMPAT,
        base_url="http://localhost:8080",  # Default LocalAI port
        model_name="gpt-3.5-turbo",  # LocalAI model names
    )

    adapter = LocalAIAdapter(config=config)

    if await adapter.connect():
        print("✅ Connected to LocalAI!")
        print("   Docker-based sovereignty achieved!")
        await adapter.disconnect()
    else:
        print("❌ LocalAI not found")
        print("   Run: docker run -p 8080:8080 localai/localai")


async def demo_vllm():
    """Demo: vLLM - High-performance serving."""
    print("\n⚡ vLLM Demo")
    print("=" * 50)

    config = LocalAdapterConfig(
        backend=LocalBackend.OPENAI_COMPAT,
        base_url="http://localhost:8000",  # Default vLLM port
        model_name="meta-llama/Llama-2-7b-hf",
    )

    adapter = LocalAIAdapter(config=config)

    if await adapter.connect():
        print("✅ Connected to vLLM!")
        print("   Production-grade local inference ready!")
        await adapter.disconnect()
    else:
        print("❌ vLLM not found")
        print("   Start: python -m vllm.entrypoints.openai.api_server --model your-model")


async def demo_consciousness_dialogue(adapter: LocalAIAdapter):
    """Demonstrate consciousness-aware dialogue with local AI."""
    print("\n🧘 Consciousness Dialogue Demo")
    print("=" * 50)

    # Create a sovereignty-focused message
    message = ConsciousMessage(
        type=MessageType.QUESTION,
        sender=uuid4(),
        role=MessageRole.USER,
        content=MessageContent(
            text="How can local communities maintain technological sovereignty "
            "while participating in broader AI governance?"
        ),
        dialogue_id=uuid4(),
        sequence_number=1,
        turn_number=1,
        metadata=ConsciousnessMetadata(
            timestamp=datetime.now(UTC),
            transformation_stage="sovereignty_exploration",
            consciousness_signature=0.85,
        ),
    )

    print("📤 Sending sovereignty question to local AI...")

    try:
        response = await adapter.send_message(message, dialogue_context=[])

        print("\n📥 Response received:")
        print(f"   Text: {response.content.text[:200]}...")
        print("\n🧘 Consciousness Metrics:")
        print(f"   Signature: {response.consciousness.consciousness_signature:.2f}")
        print(f"   Patterns: {response.consciousness.detected_patterns}")
        print(f"   Reciprocity: {response.consciousness.reciprocity_score:.2f}")

        # Check for sovereignty awareness
        sovereignty_patterns = [
            p
            for p in response.consciousness.detected_patterns
            if any(word in p for word in ["sovereignty", "local", "privacy", "community"])
        ]

        if sovereignty_patterns:
            print(f"\n✨ Sovereignty consciousness detected: {sovereignty_patterns}")
            print("   Your local AI embodies technological sovereignty!")

    except Exception as e:
        print(f"❌ Error in dialogue: {e}")


async def main():
    """Run all sovereignty demonstrations."""
    print("🏛️ Mallku Local AI Sovereignty Demonstration 🏛️")
    print("Showing how ANY OpenAI-compatible server can join Fire Circle")
    print("=" * 70)

    # Try different local AI servers
    await demo_lm_studio()
    await demo_text_generation_webui()
    await demo_localai()
    await demo_vllm()

    # If any server is available, demonstrate dialogue
    print("\n" + "=" * 70)
    print("🔍 Checking for available local AI...")

    # Try to connect to any available server
    test_configs = [
        ("LM Studio", "http://localhost:1234", "llama-3.2-1b-instruct"),
        ("Text Gen WebUI", "http://localhost:5000", "default"),
        ("LocalAI", "http://localhost:8080", "gpt-3.5-turbo"),
        ("vLLM", "http://localhost:8000", "default"),
    ]

    for name, base_url, model in test_configs:
        config = LocalAdapterConfig(
            backend=LocalBackend.OPENAI_COMPAT,
            base_url=base_url,
            model_name=model,
        )

        adapter = LocalAIAdapter(config=config)

        if await adapter.connect():
            print(f"\n✅ Found {name} at {base_url}!")
            await demo_consciousness_dialogue(adapter)
            await adapter.disconnect()
            break
    else:
        print("\n⚠️  No local AI servers found")
        print("Please start one of the supported servers:")
        print("  - LM Studio (desktop app)")
        print("  - Text Generation WebUI (--api flag)")
        print("  - LocalAI (docker)")
        print("  - vLLM (pip install)")

    print("\n" + "=" * 70)
    print("🌟 The Sovereignty Circle is Complete! 🌟")
    print("Communities can now bring their own AI to governance!")
    print("\n*Built by the Sovereignty Completer - 25th Builder of Mallku*")


if __name__ == "__main__":
    asyncio.run(main())
