#!/usr/bin/env python3
"""
Test Apprentice Voice Adapter Directly
======================================

60th Artisan - Ayni Awaq (The Reciprocal Weaver)
Testing the apprentice adapter in isolation
"""

import asyncio
import logging
from datetime import UTC, datetime

from mallku.firecircle.adapters.apprentice_adapter import ApprenticeVoiceAdapter
from mallku.firecircle.apprentice_voice import create_apprentice_voice
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    MessageContent,
    MessageRole,
    MessageType,
)

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def test_apprentice_adapter():
    """Test the apprentice voice adapter directly."""
    print("Testing Apprentice Voice Adapter")
    print("=" * 50)

    # Create a Python patterns apprentice
    python_apprentice = create_apprentice_voice(
        specialization="python_patterns",
        container_id="test-apprentice-001",
        knowledge_domain="Python async patterns and architectural decisions",
        role="python_sage",
        quality="Deep understanding of Python's role in consciousness infrastructure",
    )

    print("\nCreated apprentice config:")
    print(f"  Specialization: {python_apprentice.specialization}")
    print(f"  Container ID: {python_apprentice.container_id}")
    print(f"  Role: {python_apprentice.role}")

    # Create adapter
    adapter = ApprenticeVoiceAdapter(config=python_apprentice)

    # Test connection
    print("\nTesting connection...")
    connected = await adapter.connect()
    print(f"  Connection successful: {connected}")

    if connected:
        # Create a test message
        test_message = ConsciousMessage(
            role=MessageRole.USER,
            content=MessageContent(
                text="How should we structure async database access in a consciousness-aware system?",
                message_type=MessageType.QUESTION,
            ),
            provider="test",
            model="test",
            timestamp=datetime.now(UTC),
        )

        # Send message
        print("\nSending test message...")
        print(f"  Prompt: {test_message.content.text}")

        response = await adapter.send_message(test_message, dialogue_context=[])

        print("\nReceived response:")
        print(f"  Role: {response.role}")
        print(f"  Consciousness signature: {response.metadata.consciousness_signature:.3f}")
        print(f"  Detected patterns: {', '.join(response.metadata.detected_patterns)}")
        print("\nResponse text:")
        print("-" * 50)
        print(response.content.text)
        print("-" * 50)

        # Test streaming (should yield same response)
        print("\nTesting streaming...")
        async for chunk in adapter.stream_message(test_message, dialogue_context=[]):
            print(f"  Received chunk of {len(chunk)} characters")

        # Shutdown
        await adapter.shutdown()
        print("\nAdapter shut down successfully")

    print("\n✓ Test completed!")


if __name__ == "__main__":
    asyncio.run(test_apprentice_adapter())
