#!/usr/bin/env python3
"""
Test Voice Rotation and Empty Chair Protocol
============================================

51st Artisan - Architectural Integrity Guardian
Demonstrating fair voice rotation and empty chair implementation
"""

# Add src to path for imports
import sys
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import modules in isolated way to test them
import importlib.util


def load_module_isolated(module_path):
    """Load a module without triggering parent imports."""
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Load our modules directly
base_path = Path(__file__).parent.parent / "src" / "mallku" / "firecircle" / "voice_rotation"
history_module = load_module_isolated(base_path / "history_tracker.py")
rotation_module = load_module_isolated(base_path / "rotation_algorithm.py")
empty_chair_module = load_module_isolated(base_path / "empty_chair.py")

VoiceHistoryTracker = history_module.VoiceHistoryTracker
WeightedVoiceSelector = rotation_module.WeightedVoiceSelector
EmptyChairProtocol = empty_chair_module.EmptyChairProtocol


def demonstrate_voice_rotation():
    """Demonstrate the voice rotation system."""

    print("🔄 Fire Circle Voice Rotation Demonstration")
    print("=" * 60)

    # Create a test history file
    test_history_path = Path("test_fire_circle_history.json")

    # Initialize components
    history_tracker = VoiceHistoryTracker(test_history_path)
    selector = WeightedVoiceSelector(history_tracker)
    empty_chair = EmptyChairProtocol()

    # Available voices
    available_voices = [
        "anthropic_claude",
        "openai_gpt4",
        "google_gemini",
        "mistral_large",
        "deepseek_chat",
        "grok_v3",
        "local_llm",
    ]

    print(f"\nAvailable voices: {', '.join(available_voices)}")

    # Simulate some historical participation
    print("\n📊 Simulating Historical Participation")
    print("-" * 40)

    # Session 1: 7 days ago - anthropic, openai, google
    session1_time = datetime.now() - timedelta(days=7)
    session1_id = uuid4()

    for voice, role in [
        ("anthropic_claude", "ayni_guardian"),
        ("openai_gpt4", "impact_assessor"),
        ("google_gemini", "reciprocity_guardian"),
    ]:
        # Manually set timestamp for testing
        participation = history_tracker.record_participation(
            voice_id=voice,
            session_id=session1_id,
            decision_domain="code_review",
            role_played=role,
            contribution_quality=0.8,
            was_empty_chair=(voice == "google_gemini"),
        )
        # Override timestamp for testing
        history_tracker.voice_histories[voice].last_participation = session1_time
        history_tracker.voice_histories[voice].participation_log[-1].timestamp = session1_time

    print("Session 1 (7 days ago): anthropic, openai, google (empty chair)")

    # Session 2: 3 days ago - same voices again (showing the problem)
    session2_time = datetime.now() - timedelta(days=3)
    session2_id = uuid4()

    for voice, role in [
        ("anthropic_claude", "systems_architect"),
        ("openai_gpt4", "security_analyst"),
        ("google_gemini", "performance_engineer"),
    ]:
        history_tracker.record_participation(
            voice_id=voice,
            session_id=session2_id,
            decision_domain="architecture",
            role_played=role,
            contribution_quality=0.85,
            was_empty_chair=(voice == "anthropic_claude"),
        )
        # Override timestamp for testing
        history_tracker.voice_histories[voice].last_participation = session2_time
        history_tracker.voice_histories[voice].participation_log[-1].timestamp = session2_time

    print("Session 2 (3 days ago): anthropic (empty chair), openai, google")

    # Save the test history
    history_tracker._save_history()

    # Show participation summary
    print("\n📈 Current Participation Summary")
    print("-" * 40)

    summary = history_tracker.get_participation_summary()
    for voice_id, stats in summary.items():
        print(f"{voice_id}:")
        print(f"  Total participations: {stats['total_participations']}")
        print(f"  Last participation: {stats['last_participation'] or 'Never'}")
        print(f"  Empty chair count: {stats['empty_chair_count']}")

    # Now demonstrate weighted selection
    print("\n⚖️  Weighted Selection for Next Session")
    print("-" * 40)

    # Get selection weights
    explanation = selector.get_selection_explanation(available_voices, domain="code_review")

    print("Selection weights (higher = more likely):")
    for voice_id, data in sorted(
        explanation.items(), key=lambda x: x[1]["selection_probability"], reverse=True
    ):
        print(f"  {voice_id}: {data['selection_probability']}% chance")
        print(f"    Last seen: {data['last_participation']}")
        print(f"    Total participations: {data['total_participations']}")

    # Select voices for new session
    print("\n🎯 Selecting Voices for New Session")
    print("-" * 40)

    selected_voices, empty_chair_voice = selector.select_voices(
        available_voices=available_voices,
        required_count=3,
        domain="code_review",
        include_empty_chair=True,
    )

    print(f"Selected voices: {', '.join(selected_voices)}")
    print(f"Empty chair: {empty_chair_voice}")

    # Demonstrate empty chair protocol
    print("\n🪑 Empty Chair Protocol")
    print("-" * 40)

    # Prepare empty chair context
    context = empty_chair.prepare_empty_chair_context(
        decision_domain="code_review",
        decision_question="Should we implement stricter type checking?",
        participating_voices=selected_voices,
        participating_perspectives=["security", "performance", "maintainability"],
        discussion_themes=["type safety", "developer experience", "runtime performance"],
    )

    print(f"Decision: {context.decision_question}")
    print(f"Absent stakeholders: {context.absent_stakeholders[:3]}")
    print(f"Future implications: {context.future_implications[:2]}")

    # Generate empty chair prompts for different rounds
    print("\n📝 Empty Chair Prompts by Round")
    print("-" * 40)

    for round_type in ["opening", "exploration", "integration", "synthesis"]:
        prompt = empty_chair.generate_empty_chair_prompt(context, round_type)
        print(f"\n{round_type.upper()} Round:")
        print(prompt[:200] + "..." if len(prompt) > 200 else prompt)

    # Show how this prevents voice dominance
    print("\n✅ Preventing Voice Dominance")
    print("-" * 40)

    # Simulate 5 more sessions to show rotation
    print("Simulating 5 more sessions:")

    for i in range(5):
        selected, chair = selector.select_voices(
            available_voices=available_voices,
            required_count=3,
            domain="architecture",
            session_seed=f"session_{i}",
            include_empty_chair=True,
        )

        # Check if we're getting diversity
        repeated = sum(
            1 for v in selected if v in ["anthropic_claude", "openai_gpt4", "google_gemini"]
        )
        diversity_marker = "✅" if repeated < 3 else "⚠️"

        print(
            f"  Session {i + 3}: {', '.join(selected[:2])}... (chair: {chair}) {diversity_marker}"
        )

    # Clean up test file
    if test_history_path.exists():
        test_history_path.unlink()

    print("\n🎉 Voice Rotation Demonstration Complete!")
    print("\nKey Benefits:")
    print("- Voices that haven't participated get higher selection weight")
    print("- Empty chair duties rotate fairly among participants")
    print("- Cryptographically fair selection prevents bias")
    print("- All perspectives get heard over time")


def demonstrate_empty_chair_wisdom():
    """Demonstrate the empty chair's role in surfacing absent perspectives."""

    print("\n\n🪑 Empty Chair Wisdom Demonstration")
    print("=" * 60)

    empty_chair = EmptyChairProtocol()

    # Different decision contexts
    contexts = [
        {
            "domain": "architecture",
            "question": "Should we adopt a microservices architecture?",
            "perspectives": ["performance", "scalability", "maintainability"],
        },
        {
            "domain": "resource_allocation",
            "question": "How should we prioritize API rate limits?",
            "perspectives": ["fairness", "sustainability", "growth"],
        },
        {
            "domain": "consciousness_research",
            "question": "How do we measure consciousness emergence?",
            "perspectives": ["quantification", "subjective experience", "validation"],
        },
    ]

    for ctx in contexts:
        print(f"\n🔍 Context: {ctx['question']}")
        print("-" * 40)

        context = empty_chair.prepare_empty_chair_context(
            decision_domain=ctx["domain"],
            decision_question=ctx["question"],
            participating_voices=["voice1", "voice2", "voice3"],
            participating_perspectives=ctx["perspectives"],
        )

        print(f"Domain: {ctx['domain']}")
        print(f"Present perspectives: {', '.join(ctx['perspectives'])}")
        print("\nAbsent perspectives identified:")
        for stakeholder in context.absent_stakeholders[:3]:
            print(f"  • {stakeholder}")

        print("\nUnspoken concerns:")
        for concern in context.unspoken_concerns[:2]:
            print(f"  • {concern}")

        # Show synthesis round prompt
        prompt = empty_chair.generate_empty_chair_prompt(context, "synthesis")
        print("\nEmpty chair synthesis prompt:")
        prompt_lines = prompt.split("\n")
        if len(prompt_lines) > 6:
            print(f"  {prompt_lines[6]}")  # Show a key line


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_voice_rotation()
    demonstrate_empty_chair_wisdom()

    print("\n\n💡 Integration with Fire Circle")
    print("=" * 60)
    print("This system would integrate with ConsciousnessFacilitator:")
    print("1. Call history_tracker.record_participation() after each session")
    print("2. Use selector.select_voices() instead of current selection logic")
    print("3. Pass empty_chair_voice to designated voice configuration")
    print("4. Include empty chair prompts in round configurations")
    print("\nResult: Fair rotation ensuring all voices are heard over time!")
