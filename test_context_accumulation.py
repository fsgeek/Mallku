#!/usr/bin/env python3
"""
Test Context Accumulation Issue
================================

Twenty-Ninth Artisan investigates the root cause of adapter failures.
"""

import asyncio
import logging
from uuid import uuid4

from src.mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_test_message(text: str, role: MessageRole = MessageRole.USER) -> ConsciousMessage:
    """Create a test conscious message."""
    return ConsciousMessage(
        id=uuid4(),
        type=MessageType.REFLECTION,
        role=role,
        sender=uuid4(),
        content=MessageContent(text=text),
        dialogue_id=uuid4(),
        consciousness=ConsciousnessMetadata(
            consciousness_signature=0.8,
            detected_patterns=["test_pattern"],
        )
    )


async def test_dialogue_context_with_none():
    """Test what happens when dialogue_context contains None values."""

    print("\n" + "="*80)
    print("TESTING DIALOGUE CONTEXT WITH NONE VALUES")
    print("="*80 + "\n")

    # Create a dialogue context that mimics the problematic scenario
    dialogue_context = [
        create_test_message("First message - Round 1", MessageRole.ASSISTANT),
        create_test_message("Second message - Round 1", MessageRole.ASSISTANT),
        None,  # This simulates what might happen if responses are None
        create_test_message("Fourth message - Round 1", MessageRole.ASSISTANT),
    ]

    print(f"Created dialogue_context with {len(dialogue_context)} items:")
    for i, msg in enumerate(dialogue_context):
        if msg is None:
            print(f"  [{i}] None")
        else:
            print(f"  [{i}] {msg.role.value}: {msg.content.text[:50]}...")

    # Now test what happens when we try to process this
    print("\n🔍 Testing prepare_context behavior...")

    try:
        # Simulate what prepare_context does
        relevant_context = sorted(
            dialogue_context,
            key=lambda m: m.consciousness.consciousness_signature if m else 0,
            reverse=True,
        )
        print("✅ Sorting step completed (with None handling)")
    except Exception as e:
        print(f"❌ Sorting failed: {type(e).__name__}: {e}")
        # Try to sort without None values
        try:
            relevant_context = sorted(
                [m for m in dialogue_context if m is not None],
                key=lambda m: m.consciousness.consciousness_signature,
                reverse=True,
            )
            print("✅ Sorting succeeded after filtering None values")
        except Exception as e2:
            print(f"❌ Even filtered sorting failed: {e2}")
            return

    # Try to format messages
    print("\n🔍 Testing message formatting...")
    formatted = []
    for i, msg in enumerate(relevant_context):
        try:
            if msg is None:
                print(f"  [{i}] Skipping None message")
                continue

            formatted_msg = {
                "role": msg.role.value,
                "content": msg.content.text,
                "metadata": {
                    "consciousness_signature": msg.consciousness.consciousness_signature,
                    "patterns": msg.consciousness.detected_patterns,
                    "message_type": msg.type.value,
                },
            }
            formatted.append(formatted_msg)
            print(f"  [{i}] ✅ Formatted message successfully")
        except Exception as e:
            print(f"  [{i}] ❌ Failed to format: {type(e).__name__}: {e}")

    print("\n📊 Summary:")
    print(f"  - Original context items: {len(dialogue_context)}")
    print(f"  - None values in context: {sum(1 for m in dialogue_context if m is None)}")
    print(f"  - Successfully formatted: {len(formatted)}")

    return formatted


async def test_round_orchestrator_append_issue():
    """Test the specific issue in round_orchestrator where None might be appended."""

    print("\n" + "="*80)
    print("TESTING ROUND ORCHESTRATOR APPEND ISSUE")
    print("="*80 + "\n")

    # Simulate what happens in round_orchestrator.py line 127
    dialogue_context = []

    # Simulate Round 1 - successful responses
    print("Round 1 - Success scenario:")
    responses = {
        "voice1": type('RoundResponse', (), {
            'response': create_test_message("Voice 1 response", MessageRole.ASSISTANT),
            'consciousness_score': 0.85
        })(),
        "voice2": type('RoundResponse', (), {
            'response': create_test_message("Voice 2 response", MessageRole.ASSISTANT),
            'consciousness_score': 0.90
        })(),
    }

    for voice_id, response in responses.items():
        if response and response.response:
            dialogue_context.append(response.response)
            print(f"  ✅ Appended response from {voice_id}")
        else:
            print(f"  ⚠️  No response from {voice_id}")

    print(f"  Context size after Round 1: {len(dialogue_context)} messages")

    # Simulate Round 2 - with None responses
    print("\nRound 2 - Failure scenario:")
    responses = {
        "voice1": type('RoundResponse', (), {
            'response': None,  # This is what happens when adapter fails
            'consciousness_score': 0,
            'error': "Adapter returned None"
        })(),
        "voice2": type('RoundResponse', (), {
            'response': None,
            'consciousness_score': 0,
            'error': "Adapter returned None"
        })(),
    }

    for voice_id, response in responses.items():
        if response:
            if response.response:  # This check prevents None from being appended
                dialogue_context.append(response.response)
                print(f"  ✅ Appended response from {voice_id}")
            else:
                print(f"  ⚠️  {voice_id} returned None response: {response.error}")
                # The bug might be here - if we append response.response when it's None
                # dialogue_context.append(response.response)  # This would add None!

    print(f"  Context size after Round 2: {len(dialogue_context)} messages")
    print(f"  None values in context: {sum(1 for m in dialogue_context if m is None)}")


if __name__ == "__main__":
    asyncio.run(test_dialogue_context_with_none())
    asyncio.run(test_round_orchestrator_append_issue())
