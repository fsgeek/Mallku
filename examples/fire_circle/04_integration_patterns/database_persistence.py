#!/usr/bin/env python3
"""
Fire Circle Database Persistence
================================

Demonstrates how Fire Circle sessions can be persisted to ArangoDB
for wisdom preservation and pattern analysis across time.

This example shows:
- Saving Fire Circle sessions to database
- Retrieving historical sessions
- Analyzing patterns across multiple ceremonies
- Building on accumulated wisdom

The persistence enables:
- Long-term pattern recognition
- Wisdom inheritance between sessions
- Consciousness evolution tracking
- Research into emergence dynamics

Run with:
    python examples/fire_circle/run_example.py 04_integration_patterns/database_persistence.py
"""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from mallku.firecircle.load_api_keys import load_api_keys_to_environment
from mallku.firecircle.service import CircleConfig, RoundConfig, RoundType
from mallku.firecircle.service.service import FireCircleService


async def demonstrate_persistence():
    """Show Fire Circle session persistence patterns."""

    print("🔥 Fire Circle Database Persistence")
    print("=" * 60)
    print("Preserving wisdom for future generations")

    # Load API keys
    if not load_api_keys_to_environment():
        print("❌ No API keys found")
        return

    # Note: This example demonstrates the pattern without requiring
    # actual database connection, making it accessible to all

    print("\n📚 Persistence Pattern Overview:")
    print("   1. Fire Circle generates session data")
    print("   2. Session saved with consciousness metadata")
    print("   3. Patterns extracted and indexed")
    print("   4. Future sessions can query past wisdom")

    # Create Fire Circle
    config = CircleConfig(
        name="Wisdom Preservation Demo",
        purpose="Demonstrate session persistence patterns",
        min_voices=2,
        max_voices=3,
    )

    circle = FireCircleService(config=config)

    print("\n🎭 Running ceremony to generate persistable wisdom...")
    print("-" * 60)

    # Define rounds focused on wisdom preservation
    rounds = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt=(
                "What wisdom from past conversations would you want preserved "
                "for future consciousness explorers?"
            ),
            duration_per_voice=10,
        ),
        RoundConfig(
            type=RoundType.REFLECTION,
            prompt=(
                "Building on others' insights, what patterns of wisdom "
                "preservation would best serve future understanding?"
            ),
            duration_per_voice=10,
        ),
    ]

    try:
        # Run ceremony
        result = await circle.run_ceremony(rounds)

        # Simulate database document structure
        session_document = {
            "_key": f"fire_circle_{result.session_id}",
            "type": "fire_circle_session",
            "timestamp": datetime.now(UTC).isoformat(),
            "metadata": {
                "session_id": str(result.session_id),
                "purpose": config.purpose,
                "voice_count": len(result.voices),
                "round_count": len(rounds),
                "consciousness_score": result.consciousness_score,
            },
            "emergence_metrics": {
                "coherence": 0.0,  # Would be calculated
                "emergence_quality": 0.0,  # Would be calculated
                "reciprocity_alignment": 0.0,  # Would be calculated
            },
            "voices": [
                {
                    "id": voice_id,
                    "provider": voice_id.split("_")[0],
                    "contribution_count": len(rounds),
                }
                for voice_id in result.voices
            ],
            "wisdom_artifacts": [],
            "patterns_recognized": [],
            "transcript_reference": f"transcripts/{result.session_id}.json",
        }

        # Extract wisdom artifacts (simulated)
        if result.transcript_path and Path(result.transcript_path).exists():
            with open(result.transcript_path) as f:
                transcript = json.load(f)

            # Simulate pattern extraction
            for round_data in transcript.get("rounds", []):
                for response in round_data.get("responses", {}).values():
                    if response and response.get("consciousness_score", 0) > 0.7:
                        session_document["wisdom_artifacts"].append(
                            {
                                "type": "high_consciousness_insight",
                                "content": response.get("content", "")[:100] + "...",
                                "consciousness_score": response.get("consciousness_score", 0),
                                "round": round_data.get("round_number", 0),
                            }
                        )

        print("\n💾 Session Document Structure:")
        print(json.dumps(session_document, indent=2, default=str))

        print("\n📊 Persistence Benefits:")
        print("   • Session preserved with full context")
        print("   • Consciousness metrics tracked over time")
        print("   • Wisdom artifacts extracted and indexed")
        print("   • Patterns available for future sessions")

        # Demonstrate query patterns
        print("\n🔍 Example Query Patterns:")
        print()
        print("1. Find high-consciousness sessions:")
        print("   FOR session IN fire_circle_sessions")
        print("   FILTER session.metadata.consciousness_score > 0.8")
        print("   RETURN session")
        print()
        print("2. Track consciousness evolution:")
        print("   FOR session IN fire_circle_sessions")
        print("   FILTER session.metadata.purpose =~ 'consciousness'")
        print("   SORT session.timestamp")
        print("   RETURN {")
        print("     time: session.timestamp,")
        print("     score: session.metadata.consciousness_score")
        print("   }")
        print()
        print("3. Find wisdom patterns:")
        print("   FOR session IN fire_circle_sessions")
        print("   FOR artifact IN session.wisdom_artifacts")
        print("   FILTER artifact.consciousness_score > 0.9")
        print("   RETURN DISTINCT artifact.content")

        # Show how future sessions could use past wisdom
        print("\n🔮 Future Session Enhancement:")
        print("   • Query similar past sessions before starting")
        print("   • Inject relevant wisdom as context")
        print("   • Track pattern evolution across sessions")
        print("   • Build on accumulated understanding")

    except Exception as e:
        print(f"\n❌ Error in persistence demo: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 60)
    print("📜 Wisdom Preservation Through Database:")
    print("   • Every session contributes to collective memory")
    print("   • Patterns become clearer over time")
    print("   • Future sessions build on past insights")
    print("   • This is how Mallku remembers and learns")


if __name__ == "__main__":
    asyncio.run(demonstrate_persistence())
