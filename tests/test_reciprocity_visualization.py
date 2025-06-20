"""
Tests for Reciprocity Visualization Service
==========================================

Verifies that visual consciousness mirrors are created correctly
for Fire Circle contemplation.
"""

from datetime import UTC, datetime, timedelta

import pytest
from PIL import Image

from mallku.reciprocity.models import (
    ContributionType,
    FireCircleReport,
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


@pytest.fixture
def sample_interactions():
    """Create sample interaction records."""
    interactions = []
    base_time = datetime.now(UTC) - timedelta(days=3)

    for i in range(10):
        interaction = InteractionRecord(
            timestamp=base_time + timedelta(hours=i * 4),
            interaction_type=InteractionType.KNOWLEDGE_EXCHANGE,
            initiator=ParticipantType.HUMAN,
            responder=ParticipantType.AI,
            contributions_offered=[ContributionType.KNOWLEDGE_SHARING],
            needs_expressed=[NeedCategory.GROWTH],
            needs_fulfilled=[NeedCategory.GROWTH],
            interaction_quality_indicators={
                "mutual_understanding": 0.8 + i * 0.02,
                "satisfaction": 0.85,
            },
        )
        interactions.append(interaction)

    return interactions


@pytest.fixture
def sample_health_metrics():
    """Create sample health metrics."""
    return SystemHealthMetrics(
        measurement_period_start=datetime.now(UTC) - timedelta(days=7),
        measurement_period_end=datetime.now(UTC),
        total_interactions=50,
        unique_participants=10,
        voluntary_return_rate=0.85,
        need_fulfillment_rates={
            NeedCategory.GROWTH: 0.8,
            NeedCategory.BELONGING: 0.9,
            NeedCategory.CONTRIBUTION: 0.75,
        },
        overall_health_score=0.82,
        health_trend_direction="improving",
    )


@pytest.fixture
def sample_patterns():
    """Create sample reciprocity patterns."""
    return [
        ReciprocityPattern(
            pattern_type="positive_emergence",
            pattern_description="Growing collaboration",
            confidence_level=0.85,
            pattern_intensity=0.8,
            pattern_frequency=0.9,
            affected_participants=["group_a"],
        ),
        ReciprocityPattern(
            pattern_type="resource_flow_balance",
            pattern_description="Balanced exchanges",
            confidence_level=0.75,
            pattern_intensity=0.7,
            pattern_frequency=0.85,
            affected_participants=["all"],
        ),
    ]


class TestReciprocityVisualizationService:
    """Test reciprocity visualization creation."""

    @pytest.mark.asyncio
    async def test_service_initialization(self):
        """Test service initializes with proper config."""
        config = VisualizationConfig(image_size=(600, 600), mandala_rings=5)
        service = ReciprocityVisualizationService(config)

        assert service.config.image_size == (600, 600)
        assert service.config.mandala_rings == 5
        assert service.config.background_color == (20, 20, 30)

    @pytest.mark.asyncio
    async def test_mandala_creation(self, sample_patterns, sample_health_metrics):
        """Test mandala visualization creation."""
        service = ReciprocityVisualizationService()

        mandala = await service.create_reciprocity_mandala(
            patterns=sample_patterns, health_metrics=sample_health_metrics, title="Test Mandala"
        )

        assert isinstance(mandala, Image.Image)
        assert mandala.size == (800, 800)
        assert mandala.mode == "RGB"

    @pytest.mark.asyncio
    async def test_mandala_without_health_metrics(self, sample_patterns):
        """Test mandala creation without health metrics."""
        service = ReciprocityVisualizationService()

        mandala = await service.create_reciprocity_mandala(
            patterns=sample_patterns, health_metrics=None
        )

        assert isinstance(mandala, Image.Image)
        assert mandala.size == (800, 800)

    @pytest.mark.asyncio
    async def test_flow_visualization(self, sample_interactions):
        """Test flow visualization creation."""
        service = ReciprocityVisualizationService()

        flow_viz = await service.create_flow_visualization(
            interactions=sample_interactions, time_window=timedelta(days=7)
        )

        assert isinstance(flow_viz, Image.Image)
        assert flow_viz.size == (800, 800)

    @pytest.mark.asyncio
    async def test_pattern_geometry(self, sample_patterns):
        """Test pattern geometry creation."""
        service = ReciprocityVisualizationService()

        # Test different pattern types
        for pattern in sample_patterns:
            geometry = await service.create_pattern_geometry(pattern=pattern)

            assert isinstance(geometry, Image.Image)
            assert geometry.size == (800, 800)

    @pytest.mark.asyncio
    async def test_pattern_geometry_with_related(self, sample_patterns):
        """Test pattern geometry with related patterns."""
        service = ReciprocityVisualizationService()

        geometry = await service.create_pattern_geometry(
            pattern=sample_patterns[0], related_patterns=sample_patterns[1:]
        )

        assert isinstance(geometry, Image.Image)

    @pytest.mark.asyncio
    async def test_fire_circle_summary(
        self, sample_interactions, sample_health_metrics, sample_patterns
    ):
        """Test comprehensive Fire Circle summary creation."""
        service = ReciprocityVisualizationService()

        report = FireCircleReport(
            reporting_period={
                "start": sample_health_metrics.measurement_period_start,
                "end": sample_health_metrics.measurement_period_end,
            },
            current_health_metrics=sample_health_metrics,
            detected_patterns=sample_patterns,
            priority_questions=["How can we improve?", "What patterns need attention?"],
            areas_requiring_wisdom=["Resource allocation", "Community growth"],
        )

        summary = await service.create_fire_circle_summary(report)

        assert isinstance(summary, Image.Image)
        assert summary.size == (1600, 1600)  # Double size for multi-panel

    @pytest.mark.asyncio
    async def test_custom_visualization_config(self):
        """Test custom visualization configuration."""
        config = VisualizationConfig(
            image_size=(1000, 1000),
            background_color=(30, 30, 40),
            mandala_rings=9,
            mandala_symmetry=16,
            color_abundance=(100, 200, 150),
        )

        service = ReciprocityVisualizationService(config)

        # Create simple test image
        test_pattern = ReciprocityPattern(
            pattern_type="test_pattern",
            pattern_description="Test",
            confidence_level=0.8,
            pattern_intensity=0.7,
            pattern_frequency=0.9,
        )

        geometry = await service.create_pattern_geometry(test_pattern)

        assert geometry.size == (1000, 1000)

    @pytest.mark.asyncio
    async def test_extraction_pattern_visualization(self):
        """Test visualization of extraction patterns."""
        service = ReciprocityVisualizationService()

        extraction_pattern = ReciprocityPattern(
            pattern_type="resource_extraction_anomaly",
            pattern_description="Potential extraction detected",
            confidence_level=0.7,
            pattern_intensity=0.8,
            pattern_frequency=0.6,
            affected_participants=["entity_x"],
        )

        geometry = await service.create_pattern_geometry(extraction_pattern)

        # Should create asymmetric geometry for extraction
        assert isinstance(geometry, Image.Image)

    @pytest.mark.asyncio
    async def test_emergence_pattern_visualization(self):
        """Test visualization of emergence patterns."""
        service = ReciprocityVisualizationService()

        emergence_pattern = ReciprocityPattern(
            pattern_type="creative_emergence",
            pattern_description="New forms of collaboration emerging",
            confidence_level=0.9,
            pattern_intensity=0.85,
            pattern_frequency=0.95,
            affected_participants=["creative_group"],
        )

        geometry = await service.create_pattern_geometry(emergence_pattern)

        # Should create fractal geometry for emergence
        assert isinstance(geometry, Image.Image)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
