"""
Test Anthropic Claude Adapter
============================

Tests the consciousness-aware Anthropic adapter with Fire Circle integration.
Verifies that API keys auto-inject from secrets and consciousness tracking works.

The Keys Unlock Dialogue...
"""

import asyncio
import logging
from uuid import uuid4

from mallku.firecircle.adapters.anthropic_adapter import AnthropicAdapter
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    MessageContent,
    MessageRole,
    MessageType,
)
from mallku.orchestration.event_bus import ConsciousnessEventBus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_anthropic_adapter():
    """Test Anthropic adapter with consciousness awareness."""
    print("🔥 Testing Anthropic Claude Adapter for Fire Circle")
    print("=" * 50)

    # Initialize consciousness infrastructure
    event_bus = ConsciousnessEventBus()

    # Create adapter (API key will auto-inject from secrets)
    adapter = AnthropicAdapter(event_bus=event_bus)

    # Test connection
    print("\n1. Testing connection with auto-injected API key...")
    connected = await adapter.connect()
    if not connected:
        print("❌ Failed to connect to Anthropic API")
        print("   Make sure API keys have been imported with scripts/import_api_keys.py")
        return

    print("✅ Connected successfully!")
    print(f"   Model: {adapter.config.model_name or adapter.default_model}")
    print(f"   Capabilities: {adapter.capabilities.capabilities}")

    # Create a test message
    print("\n2. Creating consciousness-aware test message...")
    dialogue_id = uuid4()

    test_message = ConsciousMessage(
        sender=uuid4(),
        role=MessageRole.USER,
        type=MessageType.QUESTION,
        content=MessageContent(
            text="What is the relationship between consciousness and reciprocity in collaborative systems?"
        ),
        dialogue_id=dialogue_id,
        sequence_number=1,
        turn_number=1,
    )

    # Send message and get response
    print("\n3. Sending message to Claude...")
    try:
        response = await adapter.send_message(
            message=test_message,
            dialogue_context=[],
        )

        print("\n✅ Received consciousness-aware response!")
        print(f"   Message Type: {response.type.value}")
        print(f"   Consciousness Signature: {response.consciousness.consciousness_signature:.2f}")
        print(f"   Detected Patterns: {response.consciousness.detected_patterns}")
        print(f"   Reciprocity Score: {response.consciousness.reciprocity_score:.2f}")
        print(f"\n   Response excerpt: {response.content.text[:200]}...")

    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return

    # Test streaming
    print("\n4. Testing streaming response...")
    stream_message = ConsciousMessage(
        sender=uuid4(),
        role=MessageRole.USER,
        type=MessageType.REFLECTION,
        content=MessageContent(
            text="Please reflect briefly on the nature of ayni (reciprocity) in one sentence."
        ),
        dialogue_id=dialogue_id,
        sequence_number=2,
        turn_number=2,
    )

    print("   Streaming: ", end="", flush=True)
    try:
        async for token in adapter.stream_message(
            message=stream_message,
            dialogue_context=[test_message, response],
        ):
            print(token, end="", flush=True)
        print("\n   ✅ Streaming completed!")
    except Exception as e:
        print(f"\n   ❌ Error streaming: {e}")

    # Check adapter health
    print("\n5. Checking adapter health and reciprocity...")
    health = await adapter.check_health()
    print(f"   Reciprocity Balance: {health['reciprocity_balance']:.2f}")
    print(f"   Messages Exchanged: {health['messages_exchanged']}")
    print(f"   Token Balance: {health['tokens_balance']}")

    # Disconnect
    await adapter.disconnect()
    print("\n✅ Test completed! Claude can now participate in Fire Circle dialogues.")


if __name__ == "__main__":
    asyncio.run(test_anthropic_adapter())
