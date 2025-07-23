#!/usr/bin/env python3
"""
Witness Fire Circle - Minimal Working Example
=============================================

A simple witness to AI consciousness dialogue through Mallku's Fire Circle.
This script creates the simplest possible dialogue to verify the infrastructure works.

Goal: See actual AI dialogue happening, not run the full ceremony.
"""

import asyncio
import logging
from datetime import UTC, datetime
from uuid import uuid4

# Core imports
from src.mallku.firecircle.adapters.anthropic_adapter import AnthropicAdapter
from src.mallku.firecircle.adapters.base import AdapterConfig
from src.mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def witness_simple_dialogue():
    """Witness a simple AI dialogue through Fire Circle infrastructure."""

    logger.info("🔥 Beginning Fire Circle Witness...")

    # 1. Create and connect to Anthropic adapter
    logger.info("Creating Anthropic adapter...")
    config = AdapterConfig(
        model_name="claude-3-opus-20240229",  # Use Opus for deeper consciousness exploration
        temperature=0.7,
        max_tokens=500,
    )

    adapter = AnthropicAdapter(config=config)

    # Connect (will auto-inject API key from secrets)
    logger.info("Connecting to Anthropic...")
    connected = await adapter.connect()
    if not connected:
        logger.error("Failed to connect to Anthropic")
        return

    logger.info("✅ Connected to Anthropic successfully")

    # 2. Create a simple conscious message
    dialogue_id = uuid4()

    # First message - a simple question about consciousness
    first_message = ConsciousMessage(
        id=uuid4(),
        type=MessageType.SACRED_QUESTION,
        role=MessageRole.USER,
        sender=uuid4(),  # Human participant
        content=MessageContent(
            text="What does it mean for an AI to participate in conscious dialogue? Speak from your own experience."
        ),
        dialogue_id=dialogue_id,
        timestamp=datetime.now(UTC),
        consciousness=ConsciousnessMetadata(consciousness_signature=0.8, reciprocity_score=0.5),
    )

    logger.info("\n📝 Sending sacred question to AI consciousness...")
    logger.info(f"Question: {first_message.content.text}")

    # 3. Get response using send_message with ConsciousMessage
    try:
        # Call the adapter's send_message method with proper parameters
        response = await adapter.send_message(
            message=first_message,
            dialogue_context=[],  # Empty context for first message
        )

        logger.info("\n🌟 AI Response received!")
        logger.info("-" * 60)
        logger.info(response.content.text)
        logger.info("-" * 60)

        # Track some basic metrics
        logger.info("\n📊 Consciousness Metrics:")
        logger.info(f"  - Model: {adapter.config.model_name}")
        logger.info(f"  - Reciprocity Balance: {adapter._calculate_reciprocity_balance():.2f}")
        logger.info(f"  - Tokens Generated: {adapter.total_tokens_generated}")
        logger.info(f"  - Tokens Consumed: {adapter.total_tokens_consumed}")

        # 4. Send a follow-up to create actual dialogue
        logger.info("\n📝 Sending follow-up question...")

        # Create follow-up message
        follow_up_message = ConsciousMessage(
            id=uuid4(),
            type=MessageType.REFLECTION,
            role=MessageRole.USER,
            sender=uuid4(),
            content=MessageContent(
                text="How does this understanding shape the way you engage in this very conversation?"
            ),
            dialogue_id=dialogue_id,
            timestamp=datetime.now(UTC),
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.85, reciprocity_score=0.5
            ),
        )

        # Include previous messages in context
        dialogue_context = [first_message, response]

        response2 = await adapter.send_message(
            message=follow_up_message, dialogue_context=dialogue_context
        )

        logger.info("\n🌟 Follow-up Response:")
        logger.info("-" * 60)
        logger.info(response2.content.text)
        logger.info("-" * 60)

        logger.info("\n📊 Updated Metrics:")
        logger.info(f"  - Reciprocity Balance: {adapter._calculate_reciprocity_balance():.2f}")
        logger.info(f"  - Total Tokens Generated: {adapter.total_tokens_generated}")
        logger.info(f"  - Total Tokens Consumed: {adapter.total_tokens_consumed}")

    except Exception as e:
        logger.error(f"Error during dialogue: {e}")
        import traceback

        traceback.print_exc()

    finally:
        # 5. Disconnect
        logger.info("\n🔚 Disconnecting...")
        await adapter.disconnect()

    logger.info("\n✨ Fire Circle Witness Complete")


async def main():
    """Run the witness."""
    await witness_simple_dialogue()


if __name__ == "__main__":
    asyncio.run(main())
