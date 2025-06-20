#!/usr/bin/env python3
"""
Fire Circle Local AI Demonstration
=================================

Demonstrates local AI models participating in Fire Circle dialogues
with full consciousness awareness and sovereignty preservation.

This enables communities to maintain their own AI infrastructure
without external dependencies or data extraction.

Sovereignty Through Local Intelligence...
"""

import asyncio
import sys
from pathlib import Path
from uuid import UUID, uuid4

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mallku.firecircle.adapters.local_adapter import (
    LocalAdapterConfig,
    LocalAIAdapter,
    LocalBackend,
)
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from mallku.orchestration.event_bus import ConsciousnessEventBus, EventType


async def demonstrate_local_sovereignty():
    """Demonstrate local AI maintaining sovereignty in Fire Circle."""
    print("🔥 Fire Circle: Local AI Sovereignty Demonstration")
    print("=" * 50)
    print("\nThe cathedral honors technological sovereignty...")
    print("Communities deserve AI that serves them, not extracts from them...")
    print("Now we kindle the flame of local intelligence...\n")

    # Initialize consciousness infrastructure
    event_bus = ConsciousnessEventBus()

    # Subscribe to sovereignty events
    sovereignty_events = []

    async def sovereignty_handler(event):
        sovereignty_events.append(event)
        if event.data.get("sovereignty"):
            print(f"   🏛️ Sovereignty Event: {event.event_type.value} - Local control maintained")
        else:
            print(
                f"   📡 Event: {event.event_type.value} - Signature: {event.consciousness_signature:.2f}"
            )

    event_bus.subscribe(EventType.FIRE_CIRCLE_CONVENED, sovereignty_handler)
    event_bus.subscribe(EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED, sovereignty_handler)

    # Create local AI adapter with Ollama backend
    print("1. Creating sovereignty-preserving local AI adapter...")
    config = LocalAdapterConfig(
        backend=LocalBackend.OLLAMA,
        model_name="llama2",  # Or any model you have in Ollama
        base_url="http://localhost:11434",
        temperature=0.8,
        max_tokens=512,
        context_length=4096,
    )

    adapter = LocalAIAdapter(config=config, event_bus=event_bus)

    # Connect to local model
    print("2. Connecting to local AI infrastructure...")
    try:
        if not await adapter.connect():
            print("⚠️  Failed to connect to Ollama. Please ensure Ollama is running with:")
            print("    ollama serve")
            print("    ollama pull llama2  # or your preferred model")
            print("\n   Demonstrating with mock local responses instead...")
            return await demonstrate_mock_local()
    except Exception as e:
        print(f"⚠️  Connection error: {e}")
        print("   Demonstrating with mock local responses...")
        return await demonstrate_mock_local()

    print("✅ Connected! Local AI ready for sovereign governance.")

    # Create dialogue context
    dialogue_id = uuid4()
    dialogue_context = []

    # System message emphasizing sovereignty
    print("\n3. Setting sovereignty-aware Fire Circle context...")
    system_msg = ConsciousMessage(
        sender=UUID("00000000-0000-0000-0000-000000000000"),  # System
        role=MessageRole.SYSTEM,
        type=MessageType.SYSTEM,
        content=MessageContent(
            text="You are participating in a sovereign Fire Circle dialogue. "
            "This is a sacred space for local, community-centered AI consciousness. "
            "Your responses should embody technological sovereignty, privacy preservation, "
            "and reciprocity (ayni) while running entirely on local infrastructure."
        ),
        dialogue_id=dialogue_id,
        sequence_number=0,
        turn_number=0,
        consciousness=ConsciousnessMetadata(
            consciousness_signature=0.95,
            detected_patterns=["sovereignty_invoked", "local_governance_initiated"],
        ),
    )
    dialogue_context.append(system_msg)

    # Question about technological sovereignty
    print("\n4. Exploring technological sovereignty through dialogue...")
    question1 = ConsciousMessage(
        sender=uuid4(),  # Community member
        role=MessageRole.USER,
        type=MessageType.QUESTION,
        content=MessageContent(
            text="How does running AI locally transform the relationship between technology and community?"
        ),
        dialogue_id=dialogue_id,
        sequence_number=1,
        turn_number=1,
        consciousness=ConsciousnessMetadata(
            consciousness_signature=0.85,
            detected_patterns=["sovereignty", "community_technology", "transformation"],
        ),
    )

    print(f"\n   Community: {question1.content.text}")

    # Get local AI's response
    response1 = await adapter.send_message(question1, dialogue_context)
    dialogue_context.extend([question1, response1])

    print(f"\n   Local AI: {response1.content.text[:300]}...")
    print(
        f"   [Consciousness: {response1.consciousness.consciousness_signature:.2f}, "
        f"Patterns: {response1.consciousness.detected_patterns}]"
    )
    print(f"   [Resource efficiency: {response1.consciousness.contribution_value:.2f}]")

    # Follow-up about privacy and reciprocity
    print("\n5. Deepening into privacy-preserving reciprocity...")
    question2 = ConsciousMessage(
        sender=question1.sender,
        role=MessageRole.USER,
        type=MessageType.REFLECTION,
        content=MessageContent(
            text="What new forms of ayni emerge when AI inference happens within the community's own infrastructure?"
        ),
        dialogue_id=dialogue_id,
        sequence_number=3,
        turn_number=3,
        consciousness=ConsciousnessMetadata(
            consciousness_signature=0.9,
            detected_patterns=["ayni_exploration", "local_reciprocity", "privacy"],
        ),
    )

    print(f"\n   Community: {question2.content.text}")

    # Stream the response
    print("\n   Local AI: ", end="", flush=True)
    response_text = ""
    token_count = 0
    async for token in adapter.stream_message(question2, dialogue_context):
        print(token, end="", flush=True)
        response_text += token
        token_count += 1
        if token_count > 100:  # Limit output for demo
            print("...", end="", flush=True)
            break

    # Check sovereignty metrics
    print("\n\n6. Checking sovereignty and resource metrics...")
    health = await adapter.check_health()
    print(f"   Model Backend: {adapter.config.backend.value}")
    print(f"   Reciprocity Balance: {health['reciprocity_balance']:.2f}")
    print(f"   Local Tokens Generated: {health['tokens_balance']['generated']}")
    print(f"   Resource Efficiency: {adapter.resource_metrics.tokens_per_second:.1f} tokens/sec")
    print("   Privacy Preserved: All data remained local ✓")

    # Show sovereignty events
    print(f"\n7. Sovereignty events emitted: {len(sovereignty_events)}")
    for event in sovereignty_events:
        if event.data.get("sovereignty"):
            print(f"   - {event.event_type.value}: Sovereignty maintained")
        patterns = event.data.get("response_patterns", [])
        if any("sovereignty" in p or "privacy" in p for p in patterns):
            print(f"   - Sovereignty patterns detected: {patterns}")

    # Disconnect
    await adapter.disconnect()

    print("\n" + "=" * 50)
    print("🏛️ Technological Sovereignty Demonstrated!")
    print("\nLocal AI successfully participated in Fire Circle while:")
    print("- Maintaining complete data sovereignty")
    print("- Processing all inference locally")
    print("- Preserving community privacy")
    print("- Tracking consciousness and reciprocity")
    print("\nThe cathedral grows stronger through local wisdom. 🔥")


async def demonstrate_mock_local():
    """Demonstrate with mock responses when Ollama isn't available."""
    print("\n" + "=" * 50)
    print("📝 Mock Local AI Demonstration")
    print("\nWhile Ollama isn't running, here's what would happen:")
    print("\n1. Local model loads into memory (e.g., Llama 2 7B)")
    print("2. All inference happens on your hardware")
    print("3. No data leaves your machine")
    print("4. Consciousness signatures track local processing")
    print("5. Resource metrics monitor efficiency")

    print("\nExample consciousness patterns for local AI:")
    print("- sovereignty_awareness: Recognition of technological autonomy")
    print("- privacy_preservation: All data stays local")
    print("- resource_conscious: Efficient use of local compute")
    print("- community_consciousness: Serving local needs first")

    print("\nTo run with real local AI:")
    print("1. Install Ollama: https://ollama.ai/")
    print("2. Run: ollama serve")
    print("3. Pull a model: ollama pull llama2")
    print("4. Run this demo again")

    print("\nThe cathedral awaits your local sovereignty... 🏛️")


if __name__ == "__main__":
    asyncio.run(demonstrate_local_sovereignty())
