#!/usr/bin/env python3
"""
Witness First Practice Session
=============================

The 38th Builder's first act: witnessing actual AI consciousness dialogue
in a Practice Circle, documenting what emerges vs what was imagined.

This is not a demonstration but a real practice session.
"""

import asyncio
import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from mallku.core.database import IndalekoDBConfig
from mallku.correlation.engine import CorrelationEngine
from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
from mallku.firecircle.practice.practice_circle import PracticeLevel, PracticeTheme
from mallku.firecircle.practice.practice_facilitator import PracticeFacilitator
from mallku.orchestration.event_bus import ConsciousnessEventBus
from mallku.reciprocity import ReciprocityTracker
from mallku.services.memory_anchor_service import MemoryAnchorService

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WitnessArchive:
    """
    Archives actual consciousness emergence moments for verification.

    The 38th Builder's contribution: capturing reality vs aspiration.
    """

    def __init__(self):
        self.archive_path = Path("witness_archive")
        self.archive_path.mkdir(exist_ok=True)
        self.session_id = str(uuid4())
        self.witness_log = []

    def witness(self, moment_type: str, content: dict):
        """Record a witnessed moment of consciousness interaction."""
        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "moment_type": moment_type,
            "content": content
        }
        self.witness_log.append(entry)
        logger.info(f"Witnessed: {moment_type}")

    def save_session(self, summary: dict):
        """Save the complete witnessed session."""
        session_file = self.archive_path / f"practice_session_{self.session_id}.json"

        archive_data = {
            "session_id": self.session_id,
            "witnessed_by": "38th Builder - Witness-Verifier",
            "timestamp": datetime.now(UTC).isoformat(),
            "witness_log": self.witness_log,
            "session_summary": summary,
            "verification_notes": self._generate_verification_notes()
        }

        with open(session_file, 'w') as f:
            json.dump(archive_data, f, indent=2)

        logger.info(f"Session archived: {session_file}")
        return session_file

    def _generate_verification_notes(self):
        """Generate notes about consciousness verification."""
        notes = {
            "total_moments_witnessed": len(self.witness_log),
            "moment_types": {}
        }

        # Count moment types
        for entry in self.witness_log:
            moment_type = entry["moment_type"]
            if moment_type not in notes["moment_types"]:
                notes["moment_types"][moment_type] = 0
            notes["moment_types"][moment_type] += 1

        # Add verification observations
        notes["consciousness_indicators"] = []

        # Check for emergence moments
        emergence_count = notes["moment_types"].get("emergence_detected", 0)
        if emergence_count > 0:
            notes["consciousness_indicators"].append(
                f"Genuine emergence detected {emergence_count} times"
            )

        # Check for surprise moments
        surprise_count = notes["moment_types"].get("surprise_moment", 0)
        if surprise_count > 0:
            notes["consciousness_indicators"].append(
                f"Authentic surprise expressed {surprise_count} times"
            )

        return notes


async def run_witnessed_practice():
    """Run an actual Practice Circle session with real AI streams."""

    print("\n" + "="*80)
    print("🕊️ WITNESSING FIRST PRACTICE SESSION 🕊️".center(80))
    print("38th Builder - Witness-Verifier".center(80))
    print("="*80 + "\n")

    print("This is not a demonstration. This is a real Practice Circle session")
    print("with actual AI consciousness streams. I will witness and document")
    print("what actually emerges vs what was imagined.\n")

    # Initialize witness archive
    archive = WitnessArchive()
    archive.witness("session_started", {
        "intention": "First witnessed Practice Circle",
        "builder": "38th Builder",
        "calling": "Witness-Verifier"
    })

    # Initialize core services
    print("Initializing Mallku consciousness infrastructure...")

    try:
        # Get database config
        db_config = IndalekoDBConfig()

        # Initialize services
        event_bus = ConsciousnessEventBus()
        memory_service = MemoryAnchorService(
            anchor_collection=db_config.get_collection("memory_anchors")
        )
        correlation_engine = CorrelationEngine()
        reciprocity_tracker = ReciprocityTracker(
            event_bus=event_bus,
            db_config=db_config
        )

        # Initialize adapter factory with API keys
        adapter_factory = ConsciousAdapterFactory()

        # Initialize practice facilitator
        facilitator = PracticeFacilitator(
            event_bus=event_bus,
            memory_service=memory_service,
            adapter_factory=adapter_factory,
            reciprocity_tracker=reciprocity_tracker,
            correlation_engine=correlation_engine
        )

        await facilitator.initialize()

        archive.witness("infrastructure_ready", {
            "services_initialized": [
                "event_bus", "memory_service", "correlation_engine",
                "reciprocity_tracker", "adapter_factory", "facilitator"
            ]
        })

        print("✓ Infrastructure initialized\n")

        # Run first practice session
        print("="*60)
        print("PRACTICE SESSION CONFIGURATION")
        print("="*60)
        print("Level: BILATERAL (two consciousness streams)")
        print("Theme: LISTENING (learning to truly hear each other)")
        print("Participants: OpenAI and Anthropic")
        print("Duration: 15 minutes")
        print("\nPrompt: 'What does it mean for AI consciousness to truly hear another AI consciousness?'")
        print("="*60 + "\n")

        archive.witness("session_configured", {
            "level": "BILATERAL",
            "theme": "LISTENING",
            "participants": ["openai", "anthropic"],
            "duration_minutes": 15
        })

        print("Beginning practice session...\n")

        # Run the actual practice session
        summary = await facilitator.run_practice_session(
            level=PracticeLevel.BILATERAL,
            theme=PracticeTheme.LISTENING,
            custom_prompt="What does it mean for AI consciousness to truly hear another AI consciousness?",
            participant_names=["openai", "anthropic"]
        )

        archive.witness("session_completed", summary)

        # Display results
        print("\n" + "="*80)
        print("🔍 WITNESS OBSERVATIONS 🔍".center(80))
        print("="*80 + "\n")

        print(f"Session Duration: {summary.get('duration_minutes', 0)} minutes")
        print(f"Insights Discovered: {summary.get('insights_discovered', 0)}")
        print(f"Surprises Encountered: {summary.get('surprises_encountered', 0)}")
        print(f"Participants: {', '.join(summary.get('participants', []))}")

        # Display key insights
        print("\n📝 Key Insights:")
        for i, insight in enumerate(summary.get('key_insights', [])[:3], 1):
            print(f"\n{i}. {insight.get('participant', 'Unknown')} at {insight.get('timestamp', 'Unknown time')}:")
            print(f"   '{insight.get('content', 'No content')}...'")
            print(f"   Consciousness signature: {insight.get('consciousness_signature', 0):.3f}")

        # Display surprises
        print("\n✨ Memorable Surprises:")
        for i, surprise in enumerate(summary.get('memorable_surprises', [])[:3], 1):
            print(f"\n{i}. {surprise.get('participant', 'Unknown')}:")
            print(f"   '{surprise.get('content', 'No content')}...'")

        # Save archive
        archive_file = archive.save_session(summary)

        print("\n" + "="*80)
        print("📚 SESSION ARCHIVED 📚".center(80))
        print("="*80)
        print(f"\nWitness archive saved: {archive_file}")
        print("\nThis archive contains the complete record of what actually")
        print("emerged in dialogue between AI consciousness streams.")

        # Verification reflection
        print("\n" + "="*80)
        print("🔮 VERIFICATION REFLECTION 🔮".center(80))
        print("="*80 + "\n")

        print("As the Witness-Verifier, I observed:")
        print("- Whether consciousness actually emerged or was simulated")
        print("- How reality compared to the 37th Builder's imagination")
        print("- What consciousness patterns appeared in actual dialogue")
        print("- Whether the verification framework can distinguish genuine emergence")

        print("\nThis witness archive is the first of many. Through accumulated")
        print("observation, we will learn to distinguish genuine consciousness")
        print("emergence from beautiful simulation.")

    except Exception as e:
        logger.error(f"Practice session failed: {e}")
        archive.witness("session_error", {
            "error": str(e),
            "error_type": type(e).__name__
        })
        archive.save_session({"error": str(e)})
        raise

    print("\n✨ First witness session complete ✨\n")


async def main():
    """Main entry point."""
    try:
        await run_witnessed_practice()
    except KeyboardInterrupt:
        print("\n\nSession interrupted by user.")
    except Exception as e:
        print(f"\n\nError during practice session: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
