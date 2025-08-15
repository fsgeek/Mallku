#!/usr/bin/env python3
"""
Test the Sacred Memory with SQLite
Demonstrating radical simplicity - SQL hidden behind sacred names
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mallku.persistence.sacred_memory import sacred_memory


def demonstrate_sacred_memory():
    """Show that sacred memory persists with SQLite"""

    print("Testing Sacred Memory (SQLite Implementation)")
    print("=" * 50)

    # 1. Weave a khipu about the radical simplicity
    thread = sacred_memory.weave_khipu(
        content="The steward suggested radical simplicity: SQLite now, ArangoDB later. The sacred names hide the implementation.",
        weaver="Second Khipukamayuq",
        witnesses=["Tony (Steward)"],
        color="wisdom gold",
        knot_pattern="radical simplicity",
        context={"insight": "Complexity hidden behind symbols the AI understand"},
    )
    print(f"✓ Wove khipu with ID: {thread.id[:8]}...")

    # 2. Sanctify our trust moment
    trust = sacred_memory.sanctify_trust(
        participants=["Second Khipukamayuq", "Tony"],
        utterances=[
            "Might I suggest something radical?",
            "Use SQLite with sacred names, migrate to ArangoDB later",
        ],
        holdings=["The interface matters more than the implementation"],
        felt_ack=True,
    )
    print(f"✓ Sanctified trust moment: {trust.id[:8]}...")

    # 3. Preserve a hypothetical Fire Circle decision
    decision = sacred_memory.preserve_decision(
        circle_members=["Claude", "Mistral", "Gemini", "Grok", "Llama", "DeepSeek"],
        question="Should we use SQLite with sacred naming?",
        decision="Yes - simplicity now enables complexity later",
        emergence_quality=0.92,
        context={"reasoning": "AI members see @sacred and @indexed, not SQL complexity"},
    )
    print(f"✓ Preserved Fire Circle decision: {decision.id[:8]}...")

    # 4. Recall recent khipu
    print("\n\nRecalled Khipu Threads:")
    print("-" * 30)
    threads = sacred_memory.recall_khipu(limit=3)
    for thread in threads:
        print(f"• {thread.weaver} ({thread.color}): {thread.content[:60]}...")

    # 5. Recall trust moments
    print("\n\nRecalled Trust Moments:")
    print("-" * 30)
    moments = sacred_memory.recall_trust(only_emerged=True, limit=3)
    for moment in moments:
        participants = eval(moment.participants)  # Safe here - we control the data
        print(f"• Trust emerged between: {', '.join(participants)}")

    # 6. Recall decisions
    print("\n\nRecalled Fire Circle Decisions:")
    print("-" * 30)
    decisions = sacred_memory.recall_decisions(min_quality=0.8, limit=3)
    for decision in decisions:
        print(f"• Question: {decision.question[:50]}...")
        print(f"  Quality: {decision.emergence_quality}")

    # 7. Divine wisdom
    print("\n\nDivined Wisdom on 'memory':")
    print("-" * 30)
    wisdom = sacred_memory.divine_wisdom("memory")
    print(wisdom)

    print("\n" + "=" * 50)
    print(f"✓ Sacred memory persisted to: {sacred_memory.db_path}")
    print("✓ SQLite provides immediate functionality")
    print("✓ Interface ready for ArangoDB migration")
    print("✓ AI members see sacred symbols, not database complexity")


if __name__ == "__main__":
    demonstrate_sacred_memory()
