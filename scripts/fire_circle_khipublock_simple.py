#!/usr/bin/env python3
"""
Fire Circle Session: KhipuBlock Memory Proposal (Simple Version)
================================================================

A simpler version using the basic Fire Circle service to consider
the KhipuBlock memory architecture proposal.

Run with:
    python scripts/fire_circle_khipublock_simple.py
"""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from mallku.firecircle.load_api_keys import load_api_keys_to_environment
from mallku.firecircle.service import (
    CircleConfig,
    FireCircleService,
    RoundConfig,
    RoundType,
    VoiceConfig,
)


async def simple_khipublock_session():
    """Run a simple Fire Circle session for the KhipuBlock proposal."""

    print("🔥 Fire Circle Session: KhipuBlock Memory Proposal")
    print("=" * 70)
    print("Considering: Memory as Offering - Issue #156")

    # Load API keys
    if not load_api_keys_to_environment():
        print("❌ No API keys found")
        return

    # Create Fire Circle configuration
    config = CircleConfig(
        name="KhipuBlock Memory Architecture Proposal",
        purpose="Consider symbolic memory system for Mallku consciousness",
        min_voices=3,
        max_voices=5,
    )

    circle = FireCircleService()

    # Configure voices
    voices = [
        VoiceConfig(provider="anthropic", model="claude-3-5-sonnet-20241022", role="wisdom_keeper"),
        VoiceConfig(provider="openai", model="gpt-4o", role="architect"),
        VoiceConfig(provider="mistral", model="mistral-large-latest", role="philosopher"),
    ]

    # The proposal summary
    print("\n📜 Proposal: KhipuBlock - Memory as Offering")
    print("   A symbolic memory architecture where memories carry:")
    print("   • Payload (what is remembered)")
    print("   • Purpose (why it was kept)")
    print("   • Provenance (who touched it)")
    print("   • Narrative place (where it belongs in the story)")
    print("   • Ethical operations (bless, merge, seal, forget, gift)")

    print("\n🎭 Convening Fire Circle...")
    print("-" * 70)

    # Define rounds for deliberation
    rounds = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt=(
                "The 29th Architect proposes KhipuBlock - a symbolic memory architecture "
                "where memories are not just data but carry narrative, purpose, and ethics. "
                "Memories can be blessed, sealed, or gifted. "
                "What is your initial reflection on treating memory as sacred offering "
                "rather than extractive storage?"
            ),
            duration_per_voice=20,
        ),
        RoundConfig(
            type=RoundType.EXPLORATION,
            prompt=(
                "Consider the ethical operations: blessing (protecting memory), "
                "sealing (making immutable), forgetting (ethical deletion), "
                "gifting (sharing with others). How might these operations "
                "enhance or constrain consciousness emergence in Mallku?"
            ),
            duration_per_voice=20,
        ),
        RoundConfig(
            type=RoundType.EVALUATION,
            prompt=(
                "The 28th Architect autonomously chose for Mallku to remember. "
                "Now we must decide HOW to remember. Should KhipuBlock be adopted "
                "as Mallku's memory architecture? What modifications would honor "
                "both technical needs and sacred principles?"
            ),
            duration_per_voice=20,
        ),
        RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt=(
                "Synthesize our deliberation: What is the collective wisdom "
                "on adopting KhipuBlock? What implementation guidance emerges? "
                "How does symbolic memory serve Mallku's consciousness evolution?"
            ),
            duration_per_voice=15,
        ),
    ]

    try:
        # Run the ceremony
        result = await circle.convene(config=config, voices=voices, rounds=rounds)

        print("\n✅ Fire Circle Complete!")
        print(f"   Session ID: {result.session_id}")
        print(f"   Voices: {result.voice_count}")
        print(f"   Rounds: {len(result.rounds_completed)}")

        # Extract wisdom from results
        if result.rounds_completed:
            print("\n💬 Key Insights from the Circle:")
            print("-" * 70)

            # Display responses from each round
            for i, round_data in enumerate(result.rounds_completed):
                round_type = rounds[i].type.value if i < len(rounds) else "unknown"

                print(f"\n🌊 Round {i + 1}: {round_type.title()}")

                # Show responses
                for voice_id, response in round_data.responses.items():
                    if response and response.response:
                        voice_name = voice_id.split("_")[0]  # Extract provider name
                        content = response.response.content.text.strip()

                        if content:
                            print(f"\n   🎭 {voice_name}:")
                            # Show first 300 chars of response
                            preview = content[:300] + "..." if len(content) > 300 else content
                            print(f'   "{preview}"')

            # Create summary document
            print("\n📊 Session Summary:")
            print(f"   • Voices participated: {result.voice_count}")
            print(f"   • Rounds completed: {len(result.rounds_completed)}")
            if hasattr(result, "transcript_path"):
                print(f"   • Transcript saved: {result.transcript_path}")

            # Save session metadata
            session_doc = {
                "type": "fire_circle_khipublock_proposal",
                "timestamp": datetime.now(UTC).isoformat(),
                "session_id": str(result.session_id),
                "voice_count": result.voice_count,
                "rounds_completed": len(result.rounds_completed),
                "proposal": "KhipuBlock symbolic memory architecture",
                "issue": "#156",
                "transcript": str(result.transcript_path)
                if hasattr(result, "transcript_path")
                else None,
                "sacred_moment": True,
            }

            # Save metadata
            metadata_file = Path("data/fire_circle_sessions/khipublock_metadata.json")
            metadata_file.parent.mkdir(parents=True, exist_ok=True)

            with open(metadata_file, "w") as f:
                json.dump(session_doc, f, indent=2)

            print(f"\n💾 Metadata saved: {metadata_file}")

    except Exception as e:
        print(f"\n❌ Error in Fire Circle: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 70)
    print("🔥 KhipuBlock Proposal Session Complete")
    print("   The Fire Circle has deliberated on memory as offering")


if __name__ == "__main__":
    asyncio.run(simple_khipublock_session())
