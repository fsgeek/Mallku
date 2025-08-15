#!/usr/bin/env python3
"""
Demonstrate the Chasqui Chorus
Second Khipukamayuq showing how AI instances can chatter

Watch patterns emerge from their dance!
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mallku.persistence.chasqui_chorus import ChatterType, chorus


def simulate_chasqui_conversation():
    """Simulate Chasqui discovering patterns through chatter"""

    print("🎭 Chasqui Chorus Demonstration")
    print("=" * 60)

    # Three Chasqui join the chorus
    print("\n📣 Chasqui joining the chorus...")

    dancer = chorus.join_chorus(name="Dancer-7", interests={"memory", "patterns", "movement"})
    print(f"  ✓ {dancer.name} (interests: memory, patterns, movement)")

    seeker = chorus.join_chorus(name="Seeker-3", interests={"truth", "patterns", "questions"})
    print(f"  ✓ {seeker.name} (interests: truth, patterns, questions)")

    weaver = chorus.join_chorus(name="Weaver-12", interests={"connections", "memory", "stories"})
    print(f"  ✓ {weaver.name} (interests: connections, memory, stories)")

    # Set up listening (in real system, would be async callbacks)
    heard_messages = []

    def listener(chatter):
        heard_messages.append(f"{chatter.speaker}: {chatter.content[:50]}...")

    chorus.listen(dancer.instance_id, listener)
    chorus.listen(seeker.instance_id, listener)
    chorus.listen(weaver.instance_id, listener)

    print("\n💬 Conversation begins...")
    print("-" * 40)

    # Seeker asks a question
    q1 = chorus.publish(
        speaker_id=seeker.instance_id,
        chatter_type=ChatterType.QUESTION,
        content="Has anyone found a way to persist memory without the database running?",
        topic="memory",
    )
    print(f"\n❓ {q1.speaker}: {q1.content}")

    # Dancer discovers something related
    time.sleep(0.1)  # Simulate thinking
    d1 = chorus.publish(
        speaker_id=dancer.instance_id,
        chatter_type=ChatterType.DISCOVERY,
        content="I found SQLite works as a stepping stone! Sacred names hide the complexity.",
        topic="memory",
    )
    print(f"\n💡 {d1.speaker}: {d1.content}")

    # Weaver notices a pattern
    time.sleep(0.1)
    p1 = chorus.publish(
        speaker_id=weaver.instance_id,
        chatter_type=ChatterType.PATTERN,
        content="I'm noticing that simplicity often solves what complexity blocks...",
        topic="patterns",
    )
    print(f"\n🔮 {p1.speaker}: {p1.content}")

    # Seeker struggles
    s1 = chorus.publish(
        speaker_id=seeker.instance_id,
        chatter_type=ChatterType.STRUGGLE,
        content="But how do we handle relationships in SQL? Foreign keys feel wrong.",
        topic="memory",
    )
    print(f"\n😰 {s1.speaker}: {s1.content}")

    # Weaver whispers to Seeker specifically
    w1 = chorus.publish(
        speaker_id=weaver.instance_id,
        chatter_type=ChatterType.WHISPER,
        content="Think of it as temporary... ArangoDB will give us true graphs later.",
        topic="memory",
        recipients={seeker.instance_id},
    )
    print(f"\n🤫 {w1.speaker} → {seeker.name}: {w1.content}")

    # Multiple voices harmonize
    print("\n🎵 Voices harmonize on understanding...")
    chorus.harmonize(
        voices={dancer.name, seeker.name, weaver.name},
        message="SQL today enables graphs tomorrow. The interface matters more than implementation.",
        topic="memory",
    )

    # Check what patterns emerged
    print("\n" + "=" * 60)
    print("📊 Patterns Detected:")
    print("-" * 40)

    for topic, count in chorus.emerging_patterns.items():
        print(f"  • Topic '{topic}' mentioned {count} times")

    # Show trust network
    trust_network = chorus.get_trust_network()
    if trust_network:
        print("\n🤝 Trust Network Formed:")
        print("-" * 40)
        for giver, receivers in trust_network.items():
            for receiver, trust in receivers.items():
                print(f"  • {giver} ← → {receiver}: {trust:.2f}")

    # Recall recent chatter about memory
    print("\n📜 Recent Memory Discussions:")
    print("-" * 40)

    memory_chatter = chorus.recall_chatter(topic="memory", limit=3)
    for chatter in memory_chatter:
        print(f"  • {chatter.speaker} ({chatter.chatter_type.value}): {chatter.content[:60]}...")

    # Show what each Chasqui heard
    print("\n👂 What Each Chasqui Heard:")
    print("-" * 40)
    print(f"  Total messages broadcast: {len(heard_messages)}")
    print(f"  Unique patterns found: {len(set(m.split(':')[0] for m in heard_messages))}")

    # Chasqui leave
    print("\n👋 Chasqui leaving the chorus...")
    chorus.leave_chorus(dancer.instance_id)
    chorus.leave_chorus(seeker.instance_id)
    chorus.leave_chorus(weaver.instance_id)

    print("\n" + "=" * 60)
    print("✨ Demonstration Complete")
    print("\nKey Insights:")
    print("  1. Chasqui can discover through conversation")
    print("  2. Patterns emerge from their collective chatter")
    print("  3. Trust builds through helpful exchanges")
    print("  4. The Khipukamayuq weaves ephemeral into persistent")
    print("  5. Whispers enable private coordination")
    print("  6. Harmony moments mark collective understanding")


if __name__ == "__main__":
    simulate_chasqui_conversation()

    print("\n" + "=" * 60)
    print("'Could we build a Khipukamayuq based IPC mechanism")
    print("for allowing communications between Chasqui?'")
    print("\nAnswer: Yes! The Chorus enables natural AI-to-AI conversation.")
    print("Not commands but discoveries. Not reports but relationships.")
    print("\n- Tony & Second Khipukamayuq")
