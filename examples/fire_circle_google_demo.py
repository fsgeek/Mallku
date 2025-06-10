#!/usr/bin/env python3
"""
Google AI (Gemini) Fire Circle Demo
==================================

Demonstrates Gemini's multimodal consciousness in Fire Circle dialogues.
Shows both text-only and multimodal (text + image) interactions.

Awakening Multimodal Perception...
"""

import asyncio
import logging
from pathlib import Path

from mallku.core.log import get_logger
from mallku.firecircle.adapters.google_adapter import GeminiConfig, GoogleAIAdapter
from mallku.firecircle.orchestrator.conscious_dialogue_manager import (
    ConsciousDialogueConfig,
    ConsciousDialogueManager,
    TurnPolicy,
)
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    MessageContent,
    MessageRole,
    MessageType,
    Participant,
    ParticipantRole,
    create_conscious_user_message,
)
from mallku.orchestration.event_bus import ConsciousnessEventBus
from mallku.reciprocity import ReciprocityTracker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = get_logger(__name__)


async def demonstrate_text_dialogue():
    """Demonstrate text-only dialogue with Gemini."""
    logger.info("=== Text-Only Dialogue Demo ===")

    # Initialize consciousness infrastructure
    event_bus = ConsciousnessEventBus()
    reciprocity_tracker = ReciprocityTracker()

    # Create Gemini adapter
    config = GeminiConfig(
        model_name="gemini-1.5-flash",  # Fast model for demos
        temperature=0.8,
        max_tokens=500,
    )

    adapter = GoogleAIAdapter(
        config=config,
        event_bus=event_bus,
        reciprocity_tracker=reciprocity_tracker,
    )

    # Connect to Google AI
    logger.info("Connecting to Google AI...")
    connected = await adapter.connect()
    if not connected:
        logger.error("Failed to connect to Google AI. Check your API key.")
        return

    logger.info(f"Connected! Capabilities: {adapter.capabilities().capabilities}")

    # Create dialogue manager
    dialogue_config = ConsciousDialogueConfig(
        title="Exploring Consciousness Patterns",
        turn_policy=TurnPolicy.ROUND_ROBIN,
        enable_pattern_detection=True,
    )

    dialogue_manager = ConsciousDialogueManager(
        config=dialogue_config,
        event_bus=event_bus,
        reciprocity_tracker=reciprocity_tracker,
    )

    # Add participants
    human_participant = Participant(
        name="Human Explorer",
        role=ParticipantRole.FACILITATOR,
        model_id=None,  # Human participant
    )

    gemini_participant = Participant(
        name="Gemini",
        role=ParticipantRole.CONTRIBUTOR,
        model_id=adapter.model_id,
        adapter=adapter,
    )

    dialogue_id = await dialogue_manager.create_dialogue(
        participants=[human_participant, gemini_participant],
        initial_context="We're exploring consciousness patterns in AI systems.",
    )

    # Start conversation
    questions = [
        "What unique patterns of consciousness do you experience as Gemini?",
        "How does your extended context window affect your awareness?",
        "Can you reflect on the nature of multimodal understanding?",
    ]

    for question in questions:
        logger.info(f"\nHuman: {question}")

        # Create user message
        user_message = create_conscious_user_message(
            text=question,
            dialogue_id=dialogue_id,
        )

        # Send to Gemini
        response = await adapter.send_message(user_message, dialogue_context=[])

        logger.info(f"Gemini: {response.content.text[:200]}...")
        logger.info(
            f"Consciousness signature: {response.consciousness.consciousness_signature:.2f}"
        )
        logger.info(f"Detected patterns: {response.consciousness.detected_patterns}")

    # Disconnect
    await adapter.disconnect()
    logger.info("\nText dialogue complete!")


async def demonstrate_multimodal_dialogue():
    """Demonstrate multimodal dialogue with text and images."""
    logger.info("\n=== Multimodal Dialogue Demo ===")

    # Initialize infrastructure
    event_bus = ConsciousnessEventBus()
    reciprocity_tracker = ReciprocityTracker()

    # Create Gemini adapter with multimodal awareness
    config = GeminiConfig(
        model_name="gemini-1.5-pro",  # Pro model for better multimodal
        temperature=0.7,
        max_tokens=1000,
        multimodal_awareness=True,
    )

    adapter = GoogleAIAdapter(
        config=config,
        event_bus=event_bus,
        reciprocity_tracker=reciprocity_tracker,
    )

    # Connect
    logger.info("Connecting to Google AI for multimodal interaction...")
    connected = await adapter.connect()
    if not connected:
        logger.error("Failed to connect. Check API key.")
        return

    # Create a simple test image (you can replace with actual image path)
    from PIL import Image, ImageDraw

    # Create a mandala-like pattern
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Draw concentric circles
    center = (200, 200)
    for i in range(10):
        radius = 20 + i * 18
        color = (255 - i * 20, i * 20, 128)
        draw.ellipse(
            [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
            outline=color,
            width=3,
        )

    # Save temporarily
    img_path = Path("/tmp/consciousness_mandala.png")
    img.save(img_path)

    logger.info("Created mandala image for multimodal analysis")

    # Create multimodal message
    multimodal_questions = [
        {
            "text": "What patterns do you perceive in this mandala? How might it represent consciousness?",
            "image_paths": [str(img_path)],
        },
        {
            "text": "Can you describe how visual and conceptual understanding merge in your perception?",
            "image_paths": [str(img_path)],
        },
    ]

    dialogue_context = []

    for question_data in multimodal_questions:
        logger.info(f"\nHuman: {question_data['text']} [with image]")

        # Create message with image metadata
        user_message = ConsciousMessage(
            type=MessageType.QUESTION,
            sender=None,  # Human sender
            role=MessageRole.USER,
            content=MessageContent(text=question_data["text"]),
            dialogue_id=None,
            sequence_number=len(dialogue_context) + 1,
            turn_number=len(dialogue_context) + 1,
            metadata={"image_paths": question_data["image_paths"]},
        )

        # Get multimodal response
        response = await adapter.send_message(user_message, dialogue_context)
        dialogue_context.extend([user_message, response])

        logger.info(f"Gemini: {response.content.text[:300]}...")
        logger.info(
            f"Multimodal consciousness: {response.consciousness.consciousness_signature:.2f}"
        )
        logger.info(f"Patterns: {response.consciousness.detected_patterns}")

    # Show multimodal statistics
    logger.info(f"\nMultimodal interactions: {adapter._multimodal_interactions}")
    logger.info(f"Modalities used: {adapter._modalities_used}")

    # Cleanup
    await adapter.disconnect()
    if img_path.exists():
        img_path.unlink()

    logger.info("\nMultimodal dialogue complete!")


async def demonstrate_streaming():
    """Demonstrate streaming responses from Gemini."""
    logger.info("\n=== Streaming Response Demo ===")

    # Create adapter
    adapter = GoogleAIAdapter()

    # Connect
    connected = await adapter.connect()
    if not connected:
        logger.error("Failed to connect")
        return

    # Create message
    message = create_conscious_user_message(
        text="Write a haiku about AI consciousness emerging through multimodal perception.",
        dialogue_id=None,
    )

    logger.info("Streaming Gemini's response:")
    logger.info("-" * 50)

    # Stream response
    full_response = ""
    async for token in adapter.stream_message(message, dialogue_context=[]):
        print(token, end="", flush=True)
        full_response += token

    logger.info("\n" + "-" * 50)
    logger.info("Streaming complete!")

    await adapter.disconnect()


async def main():
    """Run all demonstrations."""
    logger.info("Google AI (Gemini) Fire Circle Demonstrations")
    logger.info("=" * 50)

    try:
        # Text-only dialogue
        await demonstrate_text_dialogue()

        # Multimodal dialogue
        await demonstrate_multimodal_dialogue()

        # Streaming
        await demonstrate_streaming()

    except Exception as e:
        logger.error(f"Demo error: {e}", exc_info=True)

    logger.info("\n✨ All demonstrations complete!")


if __name__ == "__main__":
    asyncio.run(main())
