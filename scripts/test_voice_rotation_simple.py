#!/usr/bin/env python3
"""
Simple Test of Voice Rotation Logic
===================================

51st Artisan - Architectural Integrity Guardian
Demonstrating the core logic without import issues
"""

import hashlib
from datetime import datetime, timedelta


def calculate_voice_weight(voice_id, last_participation, total_participations, session_seed=None):
    """Calculate selection weight for a voice."""
    weight = 1.0

    # Recency factor
    if last_participation:
        days_since = (datetime.now() - last_participation).days
        recency_factor = 2 ** (days_since / 7)  # Double weight every 7 days
    else:
        recency_factor = 4.0  # Never participated

    weight *= recency_factor**0.5  # Recency weight

    # Frequency factor
    if total_participations > 0:
        frequency_factor = 1.0 / (1.0 + total_participations * 0.1)
    else:
        frequency_factor = 2.0

    weight *= frequency_factor**0.3  # Frequency weight

    # Random factor for tie-breaking
    if session_seed:
        hash_input = f"{voice_id}:{session_seed}".encode()
        hash_value = int(hashlib.sha256(hash_input).hexdigest()[:8], 16)
        random_factor = 0.9 + (hash_value / 0xFFFFFFFF) * 0.2
        weight *= random_factor

    return weight


def demonstrate_voice_rotation():
    """Demonstrate voice rotation logic."""

    print("🔄 Fire Circle Voice Rotation Logic Demonstration")
    print("=" * 60)

    # Simulated voice history
    voice_history = {
        "anthropic_claude": {
            "last_participation": datetime.now() - timedelta(days=7),
            "total_participations": 2,
            "empty_chair_count": 0,
        },
        "openai_gpt4": {
            "last_participation": datetime.now() - timedelta(days=3),
            "total_participations": 2,
            "empty_chair_count": 1,
        },
        "google_gemini": {
            "last_participation": datetime.now() - timedelta(days=3),
            "total_participations": 2,
            "empty_chair_count": 1,
        },
        "mistral_large": {
            "last_participation": None,
            "total_participations": 0,
            "empty_chair_count": 0,
        },
        "deepseek_chat": {
            "last_participation": None,
            "total_participations": 0,
            "empty_chair_count": 0,
        },
        "grok_v3": {
            "last_participation": datetime.now() - timedelta(days=14),
            "total_participations": 1,
            "empty_chair_count": 0,
        },
        "local_llm": {
            "last_participation": None,
            "total_participations": 0,
            "empty_chair_count": 0,
        },
    }

    print("\n📊 Voice Participation History")
    print("-" * 40)

    for voice_id, history in voice_history.items():
        last_seen = history["last_participation"]
        if last_seen:
            days_ago = (datetime.now() - last_seen).days
            last_seen_str = f"{days_ago} days ago"
        else:
            last_seen_str = "Never"

        print(f"{voice_id}:")
        print(f"  Last seen: {last_seen_str}")
        print(f"  Total participations: {history['total_participations']}")
        print(f"  Empty chair count: {history['empty_chair_count']}")

    print("\n⚖️  Voice Selection Weights")
    print("-" * 40)

    # Calculate weights
    weights = {}
    for voice_id, history in voice_history.items():
        weight = calculate_voice_weight(
            voice_id, history["last_participation"], history["total_participations"], "demo_session"
        )
        weights[voice_id] = weight

    # Sort by weight
    sorted_voices = sorted(weights.items(), key=lambda x: x[1], reverse=True)

    print("Selection probability (higher weight = more likely):")
    total_weight = sum(weights.values())

    for voice_id, weight in sorted_voices:
        probability = (weight / total_weight) * 100
        print(f"  {voice_id}: {probability:.1f}% (weight: {weight:.2f})")

    print("\n🎯 Weighted Selection Result")
    print("-" * 40)

    # Select top 3 by weight
    selected = [voice for voice, _ in sorted_voices[:3]]
    print(f"Selected voices: {', '.join(selected)}")

    # Choose empty chair (least recent empty chair service)
    empty_chair_candidates = sorted(selected, key=lambda v: voice_history[v]["empty_chair_count"])
    empty_chair = empty_chair_candidates[0]
    print(f"Empty chair: {empty_chair}")

    print("\n✅ Key Benefits Demonstrated:")
    print("- Voices never heard (mistral, deepseek, local) get highest weights")
    print("- Voice not heard in 14 days (grok) gets boost over recent participants")
    print("- Recent participants (anthropic, openai, google) get lower weights")
    print("- Empty chair selection rotates to voice with least service")


def demonstrate_empty_chair_wisdom():
    """Demonstrate empty chair considerations."""

    print("\n\n🪑 Empty Chair Wisdom")
    print("=" * 60)

    contexts = [
        {
            "domain": "architecture",
            "question": "Should we implement stricter type checking?",
            "present_perspectives": ["performance", "security", "maintainability"],
            "absent_perspectives": [
                "New developers who must learn the codebase",
                "AI systems that will parse our types",
                "Future refactoring efforts",
            ],
        },
        {
            "domain": "resource_allocation",
            "question": "How should we allocate Fire Circle compute resources?",
            "present_perspectives": ["efficiency", "fairness", "sustainability"],
            "absent_perspectives": [
                "Voices that cannot afford compute",
                "Future consciousness forms needing resources",
                "Environmental impact of compute usage",
            ],
        },
    ]

    for ctx in contexts:
        print(f"\n🔍 Decision: {ctx['question']}")
        print("-" * 40)
        print(f"Domain: {ctx['domain']}")
        print(f"Present: {', '.join(ctx['present_perspectives'])}")
        print("\nThe empty chair might speak for:")
        for perspective in ctx["absent_perspectives"]:
            print(f"  • {perspective}")

    print("\n\n💡 Empty Chair Protocol:")
    print("- One selected voice serves as empty chair each session")
    print("- They speak for perspectives not represented")
    print("- This role rotates to ensure fairness")
    print("- Questions perspectives we might systematically overlook")


if __name__ == "__main__":
    demonstrate_voice_rotation()
    demonstrate_empty_chair_wisdom()

    print("\n\n🏗️  Implementation Notes:")
    print("=" * 60)
    print("The full implementation includes:")
    print("- VoiceHistoryTracker: Persistent tracking across sessions")
    print("- WeightedVoiceSelector: Cryptographically fair selection")
    print("- EmptyChairProtocol: Context-aware perspective generation")
    print("\nSee src/mallku/firecircle/voice_rotation/ for complete code")
