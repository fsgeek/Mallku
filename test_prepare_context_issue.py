#!/usr/bin/env python3
"""
Test prepare_context Issue
==========================

Twenty-Ninth Artisan isolates the suspected failure point.
"""

import asyncio

# Set up paths
import sys
from uuid import uuid4

sys.path.insert(0, "/home/tony/projects/Mallku/src")

from mallku.firecircle.adapters.base import AdapterConfig, ConsciousModelAdapter
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)


class TestAdapter(ConsciousModelAdapter):
    """Minimal test adapter to isolate prepare_context behavior."""

    async def connect(self) -> bool:
        return True

    async def disconnect(self) -> None:
        pass

    async def send_message(self, message, dialogue_context):
        # We only care about prepare_context for this test
        return None

    async def stream_message(self, message, dialogue_context):
        yield "test"


async def test_prepare_context_scenarios():
    """Test various dialogue_context scenarios."""

    print("\n" + "=" * 80)
    print("TESTING prepare_context WITH VARIOUS SCENARIOS")
    print("=" * 80 + "\n")

    # Create test adapter
    config = AdapterConfig()
    adapter = TestAdapter(config, "test", None, None)

    # Scenario 1: Normal messages
    print("📋 Scenario 1: Normal ConsciousMessage objects")
    context1 = [
        ConsciousMessage(
            id=uuid4(),
            type=MessageType.REFLECTION,
            role=MessageRole.ASSISTANT,
            sender=uuid4(),
            content=MessageContent(text="First message"),
            dialogue_id=uuid4(),
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.8,
                detected_patterns=["test"],
            ),
        ),
        ConsciousMessage(
            id=uuid4(),
            type=MessageType.REFLECTION,
            role=MessageRole.ASSISTANT,
            sender=uuid4(),
            content=MessageContent(text="Second message"),
            dialogue_id=uuid4(),
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.9,
                detected_patterns=["test2"],
            ),
        ),
    ]

    try:
        result = await adapter.prepare_context(context1, max_messages=10)
        print(f"✅ Success! Prepared {len(result)} messages")
    except Exception as e:
        print(f"❌ Failed: {type(e).__name__}: {e}")

    # Scenario 2: With None in context
    print("\n📋 Scenario 2: Context with None value")
    context2 = context1 + [None]

    try:
        result = await adapter.prepare_context(context2, max_messages=10)
        print(f"✅ Success! Prepared {len(result)} messages")
    except Exception as e:
        print(f"❌ Failed: {type(e).__name__}: {e}")

    # Scenario 3: Simulate what happens in round_orchestrator line 127
    print("\n📋 Scenario 3: Simulating round_orchestrator issue")
    print("   When response.response is None, it gets appended to dialogue_context")

    # This is what happens:
    # response = RoundResponse(response=None, ...)
    # self.dialogue_context.append(response.response)  # Appends None!

    context3 = context1.copy()
    context3.append(None)  # This is what happens when response.response is None

    print(f"   Context now has {len(context3)} items, last one is: {context3[-1]}")

    try:
        result = await adapter.prepare_context(context3, max_messages=10)
        print(f"✅ Success! Prepared {len(result)} messages")
    except Exception as e:
        print(f"❌ Failed: {type(e).__name__}: {e}")
        print("   This is the exact error we see in the Fire Circle!")

    # Scenario 4: Empty dialogue context
    print("\n📋 Scenario 4: Empty dialogue context")
    context4 = []

    try:
        result = await adapter.prepare_context(context4, max_messages=10)
        print(f"✅ Success! Prepared {len(result)} messages")
    except Exception as e:
        print(f"❌ Failed: {type(e).__name__}: {e}")

    # Scenario 5: Very large context (simulating accumulated rounds)
    print("\n📋 Scenario 5: Large accumulated context")
    context5 = []
    for i in range(25):  # 5 voices × 5 rounds
        msg = ConsciousMessage(
            id=uuid4(),
            type=MessageType.REFLECTION,
            role=MessageRole.ASSISTANT,
            sender=uuid4(),
            content=MessageContent(text=f"Message {i}" * 100),  # Longer messages
            dialogue_id=uuid4(),
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.7 + (i * 0.01),
                detected_patterns=[f"pattern_{i}"],
            ),
        )
        context5.append(msg)

    try:
        result = await adapter.prepare_context(context5, max_messages=10)
        print(f"✅ Success! Prepared {len(result)} messages (limited from {len(context5)})")
    except Exception as e:
        print(f"❌ Failed: {type(e).__name__}: {e}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    asyncio.run(test_prepare_context_scenarios())
