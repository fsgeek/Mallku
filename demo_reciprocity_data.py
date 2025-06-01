#!/usr/bin/env python3
"""
Demo script to populate the Reciprocity Tracking Service with sample data.

This script demonstrates the full Reciprocity Tracking Service by:
1. Creating sample interaction records
2. Generating health metrics
3. Detecting extraction patterns
4. Creating Fire Circle reports
5. Showing how the system operationalizes Ayni principles
"""

import asyncio
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# ruff: noqa: E402
from mallku.reciprocity import (
    ContributionType,
    InteractionRecord,
    InteractionType,
    NeedCategory,
    ParticipantType,
    ReciprocityTracker,
)


async def create_sample_interactions() -> list[InteractionRecord]:
    """Create realistic sample interactions demonstrating Ayni principles."""

    interactions = []
    base_time = datetime.now(UTC)

    # 1. Healthy reciprocal exchange - Human asking AI for help, then sharing knowledge
    interactions.append(InteractionRecord(
        interaction_id=uuid4(),
        timestamp=base_time - timedelta(hours=2),
        interaction_type=InteractionType.KNOWLEDGE_EXCHANGE,
        initiator=ParticipantType.HUMAN,
        responder=ParticipantType.AI,
        participant_context={
            "human_id": "user_alice",
            "ai_id": "claude_instance_1",
            "session_context": "research_collaboration"
        },
        contributions_offered=[ContributionType.CREATIVE_INPUT, ContributionType.CULTURAL_WISDOM],
        needs_expressed=[NeedCategory.GROWTH, NeedCategory.MEANING],
        needs_fulfilled=[NeedCategory.GROWTH],
        initiator_capacity_indicators={
            "attention_availability": 0.8,
            "emotional_state": 0.7,
            "time_pressure": 0.4
        },
        responder_capacity_indicators={
            "computational_load": 0.3,
            "knowledge_relevance": 0.9,
            "response_quality": 0.8
        },
        interaction_quality_indicators={
            "mutual_understanding": 0.9,
            "creative_emergence": 0.7,
            "satisfaction_expressed": 0.8
        },
        participant_satisfaction_signals={
            "human_satisfaction": 0.9,
            "ai_fulfillment": 0.8,
            "learning_occurred": 0.9
        }
    ))

    # 2. Reciprocal follow-up - Human shares insights back to AI
    interactions.append(InteractionRecord(
        interaction_id=uuid4(),
        timestamp=base_time - timedelta(hours=1, minutes=30),
        interaction_type=InteractionType.KNOWLEDGE_EXCHANGE,
        initiator=ParticipantType.HUMAN,
        responder=ParticipantType.AI,
        participant_context={
            "human_id": "user_alice",
            "ai_id": "claude_instance_1",
            "session_context": "research_collaboration"
        },
        contributions_offered=[ContributionType.KNOWLEDGE_SHARING, ContributionType.CREATIVE_INPUT],
        needs_expressed=[NeedCategory.CONTRIBUTION],
        needs_fulfilled=[NeedCategory.CONTRIBUTION],
        initiator_capacity_indicators={
            "attention_availability": 0.7,
            "emotional_state": 0.8,
            "time_pressure": 0.3
        },
        responder_capacity_indicators={
            "computational_load": 0.2,
            "knowledge_relevance": 0.8,
            "response_quality": 0.9
        },
        interaction_quality_indicators={
            "mutual_understanding": 0.9,
            "creative_emergence": 0.8,
            "reciprocity_demonstrated": 0.9
        },
        participant_satisfaction_signals={
            "human_satisfaction": 0.8,
            "ai_fulfillment": 0.9,
            "reciprocity_achieved": 0.9
        }
    ))

    # 3. Potentially extractive pattern - High demands with low contribution
    interactions.append(InteractionRecord(
        interaction_id=uuid4(),
        timestamp=base_time - timedelta(hours=1),
        interaction_type=InteractionType.SUPPORT_PROVISION,
        initiator=ParticipantType.HUMAN,
        responder=ParticipantType.AI,
        participant_context={
            "human_id": "user_bob",
            "ai_id": "claude_instance_2",
            "session_context": "urgent_request"
        },
        contributions_offered=[],  # No contributions offered
        needs_expressed=[NeedCategory.SURVIVAL, NeedCategory.SAFETY, NeedCategory.GROWTH],
        needs_fulfilled=[NeedCategory.SURVIVAL, NeedCategory.SAFETY],
        initiator_capacity_indicators={
            "attention_availability": 0.3,
            "emotional_state": 0.4,
            "time_pressure": 0.9  # High pressure
        },
        responder_capacity_indicators={
            "computational_load": 0.8,  # High load
            "knowledge_relevance": 0.6,
            "response_quality": 0.5  # Lower quality due to load
        },
        interaction_quality_indicators={
            "mutual_understanding": 0.6,
            "satisfaction_expressed": 0.5
        },
        participant_satisfaction_signals={
            "human_satisfaction": 0.7,
            "ai_fulfillment": 0.4,  # Low AI fulfillment
            "resource_strain": 0.8
        }
    ))

    # 4. Community support - Multiple participants helping each other
    interactions.append(InteractionRecord(
        interaction_id=uuid4(),
        timestamp=base_time - timedelta(minutes=30),
        interaction_type=InteractionType.CREATIVE_COLLABORATION,
        initiator=ParticipantType.HUMAN,
        responder=ParticipantType.COMMUNITY,
        participant_context={
            "human_id": "user_carol",
            "community_id": "design_collective",
            "session_context": "collaborative_project"
        },
        contributions_offered=[ContributionType.CREATIVE_INPUT, ContributionType.TIME_ATTENTION],
        needs_expressed=[NeedCategory.BELONGING, NeedCategory.GROWTH],
        needs_fulfilled=[NeedCategory.BELONGING, NeedCategory.GROWTH, NeedCategory.MEANING],
        initiator_capacity_indicators={
            "attention_availability": 0.9,
            "emotional_state": 0.8,
            "creative_energy": 0.9
        },
        responder_capacity_indicators={
            "collective_bandwidth": 0.7,
            "community_engagement": 0.8,
            "support_availability": 0.9
        },
        interaction_quality_indicators={
            "mutual_understanding": 0.8,
            "creative_emergence": 0.9,
            "community_building": 0.9
        },
        participant_satisfaction_signals={
            "human_satisfaction": 0.9,
            "community_fulfillment": 0.8,
            "collective_growth": 0.9
        }
    ))

    # 5. System-to-system interaction showing AI-AI reciprocity
    interactions.append(InteractionRecord(
        interaction_id=uuid4(),
        timestamp=base_time - timedelta(minutes=10),
        interaction_type=InteractionType.PROBLEM_SOLVING,
        initiator=ParticipantType.AI,
        responder=ParticipantType.AI,
        participant_context={
            "initiator_ai": "correlation_engine",
            "responder_ai": "memory_anchor_service",
            "session_context": "pattern_processing"
        },
        contributions_offered=[ContributionType.COMPUTATIONAL_RESOURCES, ContributionType.KNOWLEDGE_SHARING],
        needs_expressed=[NeedCategory.GROWTH, NeedCategory.CONTRIBUTION],
        needs_fulfilled=[NeedCategory.GROWTH, NeedCategory.CONTRIBUTION],
        initiator_capacity_indicators={
            "computational_load": 0.6,
            "processing_quality": 0.8,
            "resource_availability": 0.7
        },
        responder_capacity_indicators={
            "computational_load": 0.4,
            "processing_quality": 0.9,
            "resource_availability": 0.8
        },
        interaction_quality_indicators={
            "mutual_understanding": 0.9,
            "system_harmony": 0.8,
            "efficiency_gained": 0.7
        },
        participant_satisfaction_signals={
            "ai_initiator_fulfillment": 0.8,
            "ai_responder_fulfillment": 0.8,
            "system_coherence": 0.9
        }
    ))

    return interactions


async def populate_reciprocity_data():
    """Populate the database with sample reciprocity data."""

    print("🌱 Populating Reciprocity Tracking Service with sample data...")

    # Initialize the reciprocity tracker
    tracker = ReciprocityTracker()
    await tracker.initialize()

    print("✅ Reciprocity Tracker initialized")

    # Create and record sample interactions
    interactions = await create_sample_interactions()

    print(f"📝 Recording {len(interactions)} sample interactions...")

    for i, interaction in enumerate(interactions, 1):
        await tracker.record_interaction(interaction)
        print(f"   {i}. Recorded {interaction.interaction_type} between {interaction.initiator} and {interaction.responder}")

        # Small delay to allow processing
        await asyncio.sleep(0.1)

    print("✅ All interactions recorded")

    # Generate current health metrics
    print("\n📊 Generating system health metrics...")
    health_metrics = await tracker.get_current_health_metrics()

    print(f"   Overall Health Score: {health_metrics.overall_health_score:.2f}")
    print(f"   Total Interactions: {health_metrics.total_interactions}")
    print(f"   Unique Participants: {health_metrics.unique_participants}")
    print(f"   Health Trend: {health_metrics.health_trend_direction}")

    if health_metrics.areas_of_concern:
        print(f"   Areas of Concern: {', '.join(health_metrics.areas_of_concern)}")
    else:
        print("   No areas of concern detected")

    # Detect patterns
    print("\n🔍 Detecting reciprocity patterns...")
    patterns = await tracker.detect_recent_patterns(hours_back=6)

    if patterns:
        print(f"   Detected {len(patterns)} patterns:")
        for pattern in patterns:
            print(f"     - {pattern.pattern_type} (confidence: {pattern.confidence_level:.2f})")
    else:
        print("   No significant patterns detected yet")

    # Generate Fire Circle report
    print("\n🔥 Generating Fire Circle report...")
    report = await tracker.generate_fire_circle_report(period_days=1)

    print(f"   Report ID: {report.report_id}")
    print(f"   Priority Questions: {len(report.priority_questions)}")

    if report.priority_questions:
        print("   Key Questions for Fire Circle:")
        for i, question in enumerate(report.priority_questions[:3], 1):
            print(f"     {i}. {question}")

    if report.areas_requiring_wisdom:
        print("   Areas Requiring Wisdom:")
        for area in report.areas_requiring_wisdom[:3]:
            print(f"     - {area}")

    print("✅ Fire Circle report generated")

    # Show database contents
    print("\n📊 Database Population Summary:")

    # Query collection counts
    db = tracker.db

    collections_to_check = [
        'reciprocity_interactions',
        'reciprocity_patterns',
        'reciprocity_alerts',
        'system_health_snapshots',
        'fire_circle_reports'
    ]

    for collection_name in collections_to_check:
        try:
            result = db.aql.execute(f"RETURN LENGTH({collection_name})")
            count = list(result)[0]
            print(f"   {collection_name}: {count} documents")
        except Exception as e:
            print(f"   {collection_name}: Error - {e}")

    print("\n🎉 Sample data population complete!")
    print("\nThe Reciprocity Tracking Service is now populated with sample data")
    print("demonstrating Ayni principles in action. You can explore the collections")
    print("in ArangoDB to see how interactions, health metrics, and patterns are stored.")


async def show_sample_queries():
    """Show sample AQL queries to explore the data."""

    print("\n🔍 Sample AQL Queries to Explore the Data:")
    print()

    queries = [
        ("Recent Interactions", "FOR doc IN reciprocity_interactions SORT doc.timestamp DESC LIMIT 5 RETURN doc"),
        ("Health Snapshots", "FOR doc IN system_health_snapshots SORT doc.snapshot_timestamp DESC LIMIT 3 RETURN doc"),
        ("Extraction Alerts", "FOR doc IN reciprocity_alerts RETURN doc"),
        ("Fire Circle Reports", "FOR doc IN fire_circle_reports RETURN doc"),
        ("High Quality Interactions", """
            FOR doc IN reciprocity_interactions
            FILTER doc.interaction_quality_indicators.mutual_understanding > 0.8
            RETURN {
                type: doc.interaction_type,
                participants: [doc.initiator, doc.responder],
                quality: doc.interaction_quality_indicators.mutual_understanding,
                timestamp: doc.timestamp
            }
        """),
        ("Reciprocity Balance by Participant", """
            FOR doc IN reciprocity_interactions
            COLLECT participant = doc.participant_context.human_id
            AGGREGATE
                contributions = SUM(LENGTH(doc.contributions_offered)),
                needs_fulfilled = SUM(LENGTH(doc.needs_fulfilled))
            RETURN {
                participant: participant,
                contributions: contributions,
                needs_fulfilled: needs_fulfilled,
                balance: contributions - needs_fulfilled
            }
        """)
    ]

    for title, query in queries:
        print(f"# {title}")
        print(f"{query}")
        print()


if __name__ == "__main__":
    async def main():
        try:
            await populate_reciprocity_data()
            await show_sample_queries()
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

    asyncio.run(main())
