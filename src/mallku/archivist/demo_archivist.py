#!/usr/bin/env python3
"""
Archivist Demonstration
======================

A demonstration of the Archivist application showing consciousness-aware
memory retrieval in action.

This demo shows how natural language queries become wisdom-oriented
responses that serve human growth and understanding.
"""

import asyncio
from datetime import UTC, datetime

from mallku.archivist.archivist_service import ArchivistService
from mallku.events.event_bus import EventBus
from mallku.models.memory_anchor import MemoryAnchor
from mallku.services.memory_anchor_service import MemoryAnchorService


async def create_demo_memory_anchors() -> list[MemoryAnchor]:
    """Create demo memory anchors for testing."""
    now = datetime.now(UTC)
    anchors = []

    # Morning creative burst
    morning_anchor = MemoryAnchor(
        timestamp=now.replace(hour=9, minute=30),
        cursor_state={"filesystem": {"path": "/projects/vision_doc.md", "event": "created"}},
        metadata={
            "activity_type": "creative_writing",
            "context": "inspired",
            "description": "Started writing project vision document",
        },
    )
    anchors.append(morning_anchor)

    # Follow-up work
    followup_anchor = MemoryAnchor(
        timestamp=now.replace(hour=10, minute=15),
        cursor_state={"filesystem": {"path": "/projects/vision_doc.md", "event": "modified"}},
        predecessor_id=morning_anchor.id,
        metadata={
            "activity_type": "creative_writing",
            "context": "flow_state",
            "description": "Deep work on vision document",
        },
    )
    anchors.append(followup_anchor)

    # Meeting interruption
    meeting_anchor = MemoryAnchor(
        timestamp=now.replace(hour=11, minute=0),
        cursor_state={"calendar": {"event": "Team Standup", "duration": 30}},
        metadata={
            "activity_type": "meeting",
            "context": "collaborative",
            "participants": ["Alice", "Bob", "Charlie"],
        },
    )
    anchors.append(meeting_anchor)

    # Post-meeting inspiration
    post_meeting_anchor = MemoryAnchor(
        timestamp=now.replace(hour=11, minute=45),
        cursor_state={
            "filesystem": {"path": "/projects/implementation_notes.md", "event": "created"}
        },
        predecessor_id=meeting_anchor.id,
        metadata={
            "activity_type": "note_taking",
            "context": "inspired",
            "description": "Captured ideas from team discussion",
        },
    )
    anchors.append(post_meeting_anchor)

    # Afternoon coding session
    coding_anchor = MemoryAnchor(
        timestamp=now.replace(hour=14, minute=0),
        cursor_state={
            "filesystem": {"path": "/src/feature.py", "event": "created"},
            "music": {"playing": "Focus Playlist"},
        },
        metadata={
            "activity_type": "coding",
            "context": "focused",
            "description": "Implementing new feature",
        },
    )
    anchors.append(coding_anchor)

    # Evening reflection
    reflection_anchor = MemoryAnchor(
        timestamp=now.replace(hour=17, minute=30),
        cursor_state={"filesystem": {"path": "/journal/daily_reflection.md", "event": "created"}},
        metadata={
            "activity_type": "reflection",
            "context": "contemplative",
            "description": "Daily work reflection and insights",
        },
    )
    anchors.append(reflection_anchor)

    return anchors


async def demonstrate_queries(archivist: ArchivistService):
    """Demonstrate various query types."""

    print("\n" + "=" * 60)
    print("🔮 ARCHIVIST DEMONSTRATION")
    print("=" * 60)

    # Demo queries
    queries = [
        {
            "text": "What was I working on this morning when I felt inspired?",
            "description": "Temporal + emotional query",
        },
        {
            "text": "Show me the work that came after the team meeting",
            "description": "Causal relationship query",
        },
        {
            "text": "When do I typically do creative writing?",
            "description": "Pattern recognition query",
        },
        {
            "text": "What patterns emerge in my focused work sessions?",
            "description": "Growth-oriented pattern query",
        },
    ]

    for i, query_info in enumerate(queries, 1):
        print(f"\n{'=' * 60}")
        print(f"Query {i}: {query_info['description']}")
        print(f"{'=' * 60}")
        print(f'❓ Query: "{query_info["text"]}"')

        # Process query
        response = await archivist.query(query_info["text"])

        # Display response
        formatted = await archivist.wisdom_synthesizer.format_for_display(response, "terminal")
        print(formatted)

        # Brief pause between queries
        await asyncio.sleep(1)

    # Temporal patterns analysis
    print(f"\n{'=' * 60}")
    print("📊 TEMPORAL PATTERNS ANALYSIS")
    print("=" * 60)

    patterns = await archivist.get_temporal_patterns(time_range_days=1)

    print("\n🕐 Daily Rhythms:")
    for rhythm in patterns.get("daily_rhythms", [])[:3]:
        print(f"   Hour {rhythm['hour']:02d}:00 - {rhythm['frequency']} activities")

    print("\n💼 Work Sessions:")
    for session in patterns.get("work_sessions", [])[:3]:
        print(
            f"   {session['start'].strftime('%H:%M')} - {session['end'].strftime('%H:%M')}: "
            f"{session['duration_minutes']:.0f} min session"
        )

    if patterns.get("consciousness_insights"):
        print("\n✨ Insights:")
        for insight in patterns["consciousness_insights"]:
            print(f"   • {insight}")


async def main():
    """Run the Archivist demonstration."""

    # Initialize services
    print("Initializing Archivist services...")

    memory_anchor_service = MemoryAnchorService()
    await memory_anchor_service.initialize()

    event_bus = EventBus()
    await event_bus.initialize()

    # Create Archivist
    archivist = ArchivistService(memory_anchor_service=memory_anchor_service, event_bus=event_bus)
    await archivist.initialize()

    # Create demo data
    print("Creating demo memory anchors...")
    demo_anchors = await create_demo_memory_anchors()

    # Store demo anchors (in real system, these would come from providers)
    for anchor in demo_anchors:
        # In production, anchors are created through the service
        # For demo, we'll simulate by adding to cache
        pass

    print(f"Created {len(demo_anchors)} demo memory anchors")

    # Run demonstrations
    await demonstrate_queries(archivist)

    # Service metrics
    print(f"\n{'=' * 60}")
    print("📈 SERVICE METRICS")
    print("=" * 60)

    metrics = await archivist.get_service_metrics()
    print(f"Total Queries: {metrics['total_queries']}")
    print(f"Growth-Serving Rate: {metrics['growth_service_rate']:.2%}")
    print(f"Components Healthy: {metrics['components_healthy']}")

    print("\n✅ Demonstration complete!")
    print("\nThe Archivist bridges human memory and digital footprints")
    print("with consciousness awareness and growth orientation.")
    print("\n🙏 May your queries serve your becoming.\n")


if __name__ == "__main__":
    asyncio.run(main())
