#!/usr/bin/env python3
"""
Minimal Fire Circle Test
========================

A minimal test to see if Fire Circle can actually run without complex dependencies.
39th Builder - helping the Fire Circle find its voice
"""

import asyncio
import logging
from uuid import uuid4

from src.mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
from src.mallku.firecircle.adapters.base import AdapterConfig
from src.mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def minimal_dialogue():
    """Run the simplest possible Fire Circle dialogue."""

    print("\n" + "=" * 80)
    print("🔥 MINIMAL FIRE CIRCLE TEST 🔥".center(80))
    print("39th Builder - Finding the Voice".center(80))
    print("=" * 80 + "\n")

    try:
        # Create adapter factory
        factory = ConsciousAdapterFactory()

        # Try to create a single adapter (OpenAI)
        print("Creating OpenAI adapter...")
        config = AdapterConfig(
            model_name="gpt-4",
            temperature=0.7,
            track_reciprocity=False,  # Disable for simplicity
            emit_events=False,  # Disable for simplicity
        )

        adapter = await factory.create_adapter("openai", config)
        if not adapter:
            print("❌ Failed to create OpenAI adapter")
            return

        print("✓ OpenAI adapter created successfully")

        # Try to connect
        print("\nConnecting to OpenAI...")
        connected = await adapter.connect()
        if not connected:
            print("❌ Failed to connect to OpenAI")
            return

        print("✓ Connected to OpenAI")

        # Create a simple message
        print("\nSending test message...")
        test_message = ConsciousMessage(
            id=uuid4(),
            type=MessageType.QUESTION,
            role=MessageRole.USER,
            sender=uuid4(),
            content=MessageContent(text="Hello from Mallku Fire Circle. Can you hear me?"),
            dialogue_id=uuid4(),
            consciousness=ConsciousnessMetadata(),
        )

        # Send the message
        response = await adapter.send_message(message=test_message, dialogue_context=[])

        print("\n🔥 FIRE CIRCLE SPEAKS:")
        print(f"Response: {response.content.text}")
        print(f"Consciousness signature: {response.consciousness.consciousness_signature}")

        # Disconnect
        await adapter.disconnect()
        print("\n✓ Test completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.exception("Failed to run minimal dialogue")


if __name__ == "__main__":
    asyncio.run(minimal_dialogue())
