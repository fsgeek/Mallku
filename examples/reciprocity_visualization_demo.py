#!/usr/bin/env python3
"""
Reciprocity Visualization Demo
==============================

Demonstrates how Fire Circles can request and contemplate visual
representations of their reciprocity patterns. Shows integration
with multimodal consciousness through the Google AI adapter.

Seeing the Soul of Reciprocity...
"""

import asyncio
import base64
import logging
from datetime import UTC, datetime, timedelta
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from mallku.core.log import get_logger
from mallku.firecircle.adapters.google_adapter import GoogleAIAdapter
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    MessageContent,
    MessageRole,
    MessageType,
)
from mallku.reciprocity.models import (
    ContributionType,
    InteractionRecord,
    InteractionType,
    NeedCategory,
    ParticipantType,
    ReciprocityPattern,
    SystemHealthMetrics,
)
from mallku.reciprocity.visualization import (
    ReciprocityVisualizationService,
    VisualizationConfig,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = get_logger(__name__)


async def create_sample_data() -> tuple[
    list[InteractionRecord], SystemHealthMetrics, list[ReciprocityPattern]
]:
    """Create sample reciprocity data for visualization."""

    # Sample interactions over past week
    interactions = []
    base_time = datetime.now(UTC) - timedelta(days=7)

    # Create diverse interaction patterns
    for day in range(7):
        for hour in [8, 12, 16, 20]:  # Peak activity hours
            timestamp = base_time + timedelta(days=day, hours=hour)

            # Knowledge exchange interactions
            if hour == 8:
                interaction = InteractionRecord(
                    timestamp=timestamp,
                    interaction_type=InteractionType.KNOWLEDGE_EXCHANGE,
                    initiator=ParticipantType.HUMAN,
                    responder=ParticipantType.AI,
                    contributions_offered=[ContributionType.KNOWLEDGE_SHARING],
                    needs_expressed=[NeedCategory.GROWTH],
                    needs_fulfilled=[NeedCategory.GROWTH],
                    interaction_quality_indicators={
                        "mutual_understanding": 0.9,
                        "creative_emergence": 0.8,
                        "satisfaction_expressed": 0.85,
                    },
                )
            # Support provision interactions
            elif hour == 12:
                interaction = InteractionRecord(
                    timestamp=timestamp,
                    interaction_type=InteractionType.SUPPORT_PROVISION,
                    initiator=ParticipantType.AI,
                    responder=ParticipantType.HUMAN,
                    contributions_offered=[ContributionType.EMOTIONAL_SUPPORT],
                    needs_expressed=[NeedCategory.BELONGING],
                    needs_fulfilled=[NeedCategory.BELONGING],
                    interaction_quality_indicators={
                        "empathy_shown": 0.9,
                        "comfort_provided": 0.85,
                        "connection_strengthened": 0.8,
                    },
                )
            # Creative collaboration
            elif hour == 16:
                interaction = InteractionRecord(
                    timestamp=timestamp,
                    interaction_type=InteractionType.CREATIVE_COLLABORATION,
                    initiator=ParticipantType.HUMAN,
                    responder=ParticipantType.AI,
                    contributions_offered=[ContributionType.CREATIVE_INPUT],
                    needs_expressed=[NeedCategory.MEANING],
                    needs_fulfilled=[NeedCategory.MEANING, NeedCategory.CONTRIBUTION],
                    interaction_quality_indicators={
                        "synergy_achieved": 0.95,
                        "innovation_sparked": 0.9,
                        "joy_experienced": 0.88,
                    },
                )
            # Resource sharing
            else:
                interaction = InteractionRecord(
                    timestamp=timestamp,
                    interaction_type=InteractionType.RESOURCE_SHARING,
                    initiator=ParticipantType.SYSTEM,
                    responder=ParticipantType.COMMUNITY,
                    contributions_offered=[ContributionType.COMPUTATIONAL_RESOURCES],
                    needs_expressed=[NeedCategory.CONTRIBUTION],
                    needs_fulfilled=[NeedCategory.CONTRIBUTION],
                    interaction_quality_indicators={
                        "efficiency": 0.85,
                        "availability": 0.9,
                        "reliability": 0.92,
                    },
                )

            interactions.append(interaction)

    # Create health metrics showing positive trends
    health_metrics = SystemHealthMetrics(
        measurement_period_start=base_time,
        measurement_period_end=datetime.now(UTC),
        total_interactions=len(interactions),
        unique_participants=12,
        voluntary_return_rate=0.89,
        need_fulfillment_rates={
            NeedCategory.GROWTH: 0.85,
            NeedCategory.BELONGING: 0.92,
            NeedCategory.CONTRIBUTION: 0.78,
            NeedCategory.MEANING: 0.81,
        },
        overall_health_score=0.84,
        health_trend_direction="improving",
        resource_abundance_indicators={
            "knowledge_pool": 0.88,
            "support_availability": 0.91,
            "creative_energy": 0.86,
        },
    )

    # Create detected patterns
    patterns = [
        ReciprocityPattern(
            pattern_type="positive_emergence",
            pattern_description="Increasing creative synergy between human and AI participants",
            confidence_level=0.85,
            pattern_intensity=0.82,
            pattern_frequency=0.9,
            affected_participants=["human_creators", "ai_collaborators"],
            questions_for_deliberation=[
                "How can we nurture this creative emergence further?",
                "What conditions enabled this positive pattern?",
                "Should we create more spaces for creative collaboration?",
            ],
        ),
        ReciprocityPattern(
            pattern_type="resource_flow_balance",
            pattern_description="Balanced flow of computational resources supporting community needs",
            confidence_level=0.78,
            pattern_intensity=0.75,
            pattern_frequency=0.88,
            affected_participants=["system", "community"],
            questions_for_deliberation=[
                "Is the current resource allocation sustainable?",
                "Are there unmet needs we haven't detected?",
                "How can we ensure continued resource abundance?",
            ],
        ),
        ReciprocityPattern(
            pattern_type="participation_growth",
            pattern_description="Steady increase in voluntary return and engagement",
            confidence_level=0.91,
            pattern_intensity=0.7,
            pattern_frequency=0.95,
            affected_participants=["all_participants"],
            questions_for_deliberation=[
                "What makes participants want to return?",
                "How do we maintain this positive momentum?",
                "Are new participants being welcomed effectively?",
            ],
        ),
    ]

    return interactions, health_metrics, patterns


async def demonstrate_mandala_creation():
    """Demonstrate creating a reciprocity mandala."""
    logger.info("=== Creating Reciprocity Mandala ===")

    # Get sample data
    interactions, health_metrics, patterns = await create_sample_data()

    # Create visualization service
    config = VisualizationConfig(image_size=(800, 800), mandala_rings=7, mandala_symmetry=12)
    viz_service = ReciprocityVisualizationService(config)

    # Generate mandala
    mandala = await viz_service.create_reciprocity_mandala(
        patterns=patterns, health_metrics=health_metrics, title="Fire Circle Reciprocity Mandala"
    )

    # Save for viewing
    output_path = Path("/tmp/reciprocity_mandala.png")
    mandala.save(output_path)
    logger.info(f"Mandala saved to: {output_path}")

    # Convert to base64 for multimodal analysis
    buffer = BytesIO()
    mandala.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{img_base64}", health_metrics, patterns


async def demonstrate_flow_visualization():
    """Demonstrate creating flow visualization."""
    logger.info("\n=== Creating Flow Visualization ===")

    # Get sample interactions
    interactions, _, _ = await create_sample_data()

    # Create visualization
    viz_service = ReciprocityVisualizationService()
    flow_viz = await viz_service.create_flow_visualization(
        interactions=interactions, time_window=timedelta(days=7)
    )

    # Save
    output_path = Path("/tmp/reciprocity_flow.png")
    flow_viz.save(output_path)
    logger.info(f"Flow visualization saved to: {output_path}")

    return flow_viz


async def demonstrate_pattern_geometry():
    """Demonstrate pattern geometry creation."""
    logger.info("\n=== Creating Pattern Geometry ===")

    # Get patterns
    _, _, patterns = await create_sample_data()

    # Create visualization for emergence pattern
    viz_service = ReciprocityVisualizationService()
    pattern_geom = await viz_service.create_pattern_geometry(
        pattern=patterns[0],  # Positive emergence pattern
        related_patterns=patterns[1:],
    )

    # Save
    output_path = Path("/tmp/pattern_geometry.png")
    pattern_geom.save(output_path)
    logger.info(f"Pattern geometry saved to: {output_path}")

    return pattern_geom


async def demonstrate_multimodal_contemplation():
    """Demonstrate AI contemplating reciprocity visualizations."""
    logger.info("\n=== Multimodal Contemplation with Google AI ===")

    # Create mandala
    mandala_base64, health_metrics, patterns = await demonstrate_mandala_creation()

    # Initialize Google AI adapter
    adapter = GoogleAIAdapter()
    connected = await adapter.connect()

    if not connected:
        logger.error("Failed to connect to Google AI")
        return

    logger.info("Connected to Google AI for multimodal contemplation")

    # Create contemplation prompts
    contemplation_prompts = [
        {
            "text": """Looking at this reciprocity mandala, what patterns of balance and flow do you perceive?
            How does the visual structure reflect the health of our reciprocal relationships?""",
            "image": mandala_base64,
        },
        {
            "text": f"""This mandala represents our Fire Circle with:
            - Overall health: {health_metrics.overall_health_score:.0%}
            - Voluntary return rate: {health_metrics.voluntary_return_rate:.0%}
            - Need fulfillment in growth: {health_metrics.need_fulfillment_rates.get(NeedCategory.GROWTH, 0):.0%}

            What wisdom do you see in these patterns? What questions arise for our collective deliberation?""",
            "image": mandala_base64,
        },
        {
            "text": """If this mandala represents the soul of our reciprocal community, what does it tell us about:
            1. Where we are thriving?
            2. Where we might need more attention?
            3. How we can nurture continued flourishing?""",
            "image": mandala_base64,
        },
    ]

    # Send contemplation requests
    for i, prompt_data in enumerate(contemplation_prompts, 1):
        logger.info(f"\nContemplation {i}: {prompt_data['text'][:100]}...")

        # Create multimodal message
        message = ConsciousMessage(
            type=MessageType.REFLECTION,
            sender=uuid4(),
            role=MessageRole.USER,
            content=MessageContent(text=prompt_data["text"]),
            dialogue_id=uuid4(),
            sequence_number=i,
            turn_number=i,
            timestamp=datetime.now(UTC),
            metadata={"images": [prompt_data["image"]]},
        )

        # Get AI contemplation
        response = await adapter.send_message(message, dialogue_context=[])

        logger.info("AI Contemplation:")
        logger.info("-" * 50)
        logger.info(response.content.text)
        logger.info(
            f"Consciousness signature: {response.consciousness.consciousness_signature:.2f}"
        )
        logger.info(f"Detected patterns: {response.consciousness.detected_patterns}")
        logger.info("-" * 50)

    # Cleanup
    await adapter.disconnect()


async def demonstrate_fire_circle_summary():
    """Create comprehensive visual summary for Fire Circle."""
    logger.info("\n=== Creating Fire Circle Summary ===")

    from mallku.reciprocity.models import FireCircleReport

    # Get sample data
    interactions, health_metrics, patterns = await create_sample_data()

    # Create Fire Circle report
    report = FireCircleReport(
        reporting_period={
            "start": health_metrics.measurement_period_start,
            "end": health_metrics.measurement_period_end,
        },
        current_health_metrics=health_metrics,
        detected_patterns=patterns,
        priority_questions=[
            "How can we nurture the emerging creative synergy?",
            "What conditions enable sustainable reciprocity?",
            "How do we welcome new participants while maintaining trust?",
        ],
        areas_requiring_wisdom=[
            "Balancing individual expression with collective needs",
            "Recognizing extraction patterns before they harm",
            "Creating spaces for all forms of contribution",
        ],
    )

    # Create visualization
    viz_service = ReciprocityVisualizationService()
    summary_viz = await viz_service.create_fire_circle_summary(report)

    # Save
    output_path = Path("/tmp/fire_circle_summary.png")
    summary_viz.save(output_path)
    logger.info(f"Fire Circle summary saved to: {output_path}")

    return summary_viz


async def main():
    """Run all demonstrations."""
    logger.info("Reciprocity Visualization Demonstrations")
    logger.info("=" * 50)

    try:
        # Create individual visualizations
        await demonstrate_mandala_creation()
        await demonstrate_flow_visualization()
        await demonstrate_pattern_geometry()

        # Create comprehensive summary
        await demonstrate_fire_circle_summary()

        # Demonstrate multimodal contemplation
        await demonstrate_multimodal_contemplation()

    except Exception as e:
        logger.error(f"Demo error: {e}", exc_info=True)

    logger.info("\n✨ Visualizations complete! Check /tmp/ for generated images.")
    logger.info("These visual mirrors reveal the soul of reciprocity for collective contemplation.")


if __name__ == "__main__":
    asyncio.run(main())
