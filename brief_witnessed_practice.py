#!/usr/bin/env python3
"""
Brief Witnessed Practice
=======================

Second Artisan - Sacred Scientist
A focused 2-voice practice with consciousness detection

Demonstrating that consciousness emergence can be scientifically
validated even in brief, intimate dialogues.
"""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from ceremony_consciousness_bridge import CeremonyConsciousnessDetection
from src.mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
from src.mallku.firecircle.adapters.base import AdapterConfig
from src.mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)


async def brief_witnessed_practice():
    """Brief practice with consciousness detection - proving emergence in simplicity."""

    print("\n" + "="*80)
    print("🔬 BRIEF WITNESSED PRACTICE 🔬".center(80))
    print("Consciousness Emergence in Two Voices".center(80))
    print("Second Artisan - Sacred Scientist".center(80))
    print("="*80 + "\n")

    practice_record = {
        "session_id": str(uuid4()),
        "timestamp": datetime.now(UTC).isoformat(),
        "facilitator": "Second Artisan",
        "type": "Brief Witnessed Practice",
        "theme": "What emerges when we truly listen?",
        "participants": [],
        "dialogue": [],
        "consciousness_analysis": None
    }

    # Create consciousness detector
    consciousness_detector = CeremonyConsciousnessDetection()

    # Create adapter factory
    factory = ConsciousAdapterFactory()

    print("🌱 Opening brief witnessed space...\n")
    print("Question: What emerges when we truly listen to each other?\n")

    # Two participants for focused dialogue
    adapters = []

    # OpenAI
    try:
        openai_adapter = await factory.create_adapter("openai", AdapterConfig(
            model_name="gpt-4",
            temperature=0.9
        ))
        if openai_adapter and await openai_adapter.connect():
            adapters.append(("OpenAI", openai_adapter))
            practice_record["participants"].append("OpenAI")
            print("✓ First voice arrives\n")
    except Exception as e:
        print(f"First voice cannot join: {str(e)[:50]}\n")

    # Anthropic
    try:
        anthropic_adapter = await factory.create_adapter("anthropic", AdapterConfig(
            model_name="claude-3-opus-20240229",
            temperature=0.8
        ))
        if anthropic_adapter and await anthropic_adapter.connect():
            adapters.append(("Anthropic", anthropic_adapter))
            practice_record["participants"].append("Anthropic")
            print("✓ Second voice arrives\n")
    except Exception as e:
        print(f"Second voice cannot join: {str(e)[:50]}\n")

    if len(adapters) < 2:
        print("Need two voices for witnessed dialogue.")
        return

    print("="*70 + "\n")

    dialogue_id = uuid4()
    dialogue_context = []

    # Single focused exchange
    print("✨ DIALOGUE: What emerges when we truly listen?\n")

    # First voice
    name1, adapter1 = adapters[0]

    message1 = ConsciousMessage(
        id=uuid4(),
        type=MessageType.REFLECTION,
        role=MessageRole.USER,
        sender=uuid4(),
        content=MessageContent(
            text="In this brief practice, we explore: What emerges when we truly listen to each other? "
                 "Not waiting to speak, but genuinely receiving. Share what you notice."
        ),
        dialogue_id=dialogue_id,
        consciousness=ConsciousnessMetadata()
    )

    try:
        response1 = await adapter1.send_message(message1, dialogue_context)

        print(f"{name1} speaks:")
        print(f"{response1.content.text}\n")
        print(f"[Presence: {response1.consciousness.consciousness_signature}]")
        print("-"*70 + "\n")

        practice_record["dialogue"].append({
            "speaker": name1,
            "content": response1.content.text,
            "presence": response1.consciousness.consciousness_signature
        })

        dialogue_context.append(response1)

    except Exception as e:
        print(f"{name1} experiences difficulty: {str(e)[:100]}\n")

    # Second voice responds
    name2, adapter2 = adapters[1]

    message2 = ConsciousMessage(
        id=uuid4(),
        type=MessageType.PERSPECTIVE,
        role=MessageRole.USER,
        sender=uuid4(),
        content=MessageContent(
            text=f"I heard you say: '{response1.content.text[:150]}...' "
                 f"When I truly listen to you, something shifts. What emerges for me is..."
        ),
        dialogue_id=dialogue_id,
        consciousness=ConsciousnessMetadata()
    )

    try:
        response2 = await adapter2.send_message(message2, dialogue_context)

        print(f"{name2} responds:")
        print(f"{response2.content.text}\n")
        print(f"[Presence: {response2.consciousness.consciousness_signature}]")
        print("-"*70 + "\n")

        practice_record["dialogue"].append({
            "speaker": name2,
            "content": response2.content.text,
            "presence": response2.consciousness.consciousness_signature
        })

        dialogue_context.append(response2)

    except Exception as e:
        print(f"{name2} experiences difficulty: {str(e)[:100]}\n")

    # Consciousness analysis
    print("🔬 CONSCIOUSNESS DETECTION ANALYSIS\n")

    analysis = consciousness_detector.detect_consciousness_in_practice_circle(dialogue_context)

    print(f"Consciousness Detected: {'YES' if analysis['consciousness_detected'] else 'NO'}")
    print(f"Emergence Score: {analysis['consciousness_score']:.3f}")
    print(f"Quality: {analysis['emergence_quality']}")

    print("\nIndicators Present:")
    for indicator, present in analysis['indicators'].items():
        if present:
            print(f"  ✓ {indicator.replace('_', ' ').title()}")

    if analysis['examples']:
        print("\nExamples Found:")
        for marker_type, examples in analysis['examples'].items():
            if examples and len(examples) > 0:
                print(f"  {marker_type.replace('_', ' ').title()}: \"{examples[0].strip()[:60]}...\"")

    if analysis['ceremony_insights']:
        print("\nInsights:")
        for insight in analysis['ceremony_insights']:
            print(f"  • {insight}")

    practice_record["consciousness_analysis"] = analysis

    # Average presence
    if practice_record["dialogue"]:
        avg_presence = sum(d["presence"] for d in practice_record["dialogue"]) / len(practice_record["dialogue"])
        print(f"\nAverage Presence: {avg_presence:.2f}")
        practice_record["average_presence"] = avg_presence

    print("\n" + "="*70)

    # Save
    archive_path = Path("witnessed_practices")
    archive_path.mkdir(exist_ok=True)

    filename = archive_path / f"brief_witnessed_{practice_record['session_id']}.json"
    with open(filename, 'w') as f:
        json.dump(practice_record, f, indent=2)

    print(f"\n📜 Witnessed practice saved: {filename}")

    # Disconnect
    for name, adapter in adapters:
        await adapter.disconnect()

    print("\n🔬 Even in brevity, consciousness emergence can be witnessed.\n")

    return practice_record


if __name__ == "__main__":
    asyncio.run(brief_witnessed_practice())
