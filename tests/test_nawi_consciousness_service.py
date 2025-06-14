"""
Ñawi Consciousness Service Tests
================================

Tests that validate Ñawi's ability to serve human consciousness
development using amplified synthetic patterns.

These tests verify the architectural vision: that consciousness
service leads to technical accuracy, not the reverse.
"""


import pytest
from mallku.archivist.archivist_service import ArchivistService
from mallku.archivist.consciousness_evaluator import GrowthPotential
from mallku.events.event_bus import EventBus
from mallku.services.memory_anchor_service import MemoryAnchorService
from mallku.synthetic.consciousness_pattern_generator import (
    ConsciousnessPatternGenerator,
    ConsciousnessScenario,
)


class TestConsciousnessService:
    """Test suite for consciousness-aware retrieval."""

    @pytest.fixture
    async def archivist_service(self):
        """Create Archivist service for testing."""
        memory_service = MemoryAnchorService()
        await memory_service.initialize()

        event_bus = EventBus()
        await event_bus.initialize()

        service = ArchivistService(
            memory_anchor_service=memory_service,
            event_bus=event_bus
        )
        await service.initialize()

        return service

    @pytest.fixture
    async def pattern_generator(self):
        """Create pattern generator for test data."""
        generator = ConsciousnessPatternGenerator()
        await generator.initialize()
        return generator

    @pytest.mark.asyncio
    async def test_creative_breakthrough_recognition(
        self,
        archivist_service,
        pattern_generator
    ):
        """Test that Ñawi recognizes and serves creative breakthrough patterns."""
        # Generate creative breakthrough scenario
        pattern = await pattern_generator.generate_scenario(
            ConsciousnessScenario.CREATIVE_BREAKTHROUGH
        )

        # Store pattern anchors (in production, these come from providers)
        for anchor in pattern.timeline:
            await archivist_service.memory_anchor_service.create_anchor(
                cursor_state=anchor.cursor_state,
                metadata=anchor.metadata,
                timestamp=anchor.timestamp
            )

        # Test breakthrough-seeking query
        query = "When did I break through that creative block?"
        response = await archivist_service.query(query)

        # Verify consciousness-aware response
        assert response.consciousness_score > 0.7
        assert response.ayni_balance > 0
        assert response.result_count > 0

        # Check for breakthrough moment in results
        breakthrough_found = False
        for result in response.primary_results:
            if result.get("growth_potential") == GrowthPotential.CREATIVE_INSIGHT.value:
                breakthrough_found = True
                break

        assert breakthrough_found, "Should identify creative breakthrough"

        # Verify wisdom synthesis
        assert "breakthrough" in response.wisdom_summary.lower() or \
               "insight" in response.wisdom_summary.lower()

        # Check for growth-oriented insights
        assert len(response.insight_seeds) > 0
        assert any("pattern" in seed.lower() for seed in response.insight_seeds)

    @pytest.mark.asyncio
    async def test_pattern_recognition_over_data_retrieval(
        self,
        archivist_service,
        pattern_generator
    ):
        """Test that pattern recognition serves over mere data retrieval."""
        # Generate pattern recognition scenario
        pattern = await pattern_generator.generate_scenario(
            ConsciousnessScenario.PATTERN_RECOGNITION
        )

        # Add noise data
        noise_anchors = await pattern_generator.generate_noise_data(
            num_anchors=30,
            time_range_days=3
        )

        # Store all anchors
        all_anchors = pattern.timeline + noise_anchors
        for anchor in all_anchors:
            await archivist_service.memory_anchor_service.create_anchor(
                cursor_state=anchor.cursor_state,
                metadata=anchor.metadata,
                timestamp=anchor.timestamp
            )

        # Test pattern-seeking query
        query = "What patterns am I not seeing in my work?"
        response = await archivist_service.query(query)

        # Verify pattern recognition over noise
        assert response.result_count < len(all_anchors), \
            "Should filter results for consciousness service"

        # Check that high-consciousness anchors are prioritized
        if response.primary_results:
            first_result = response.primary_results[0]
            assert first_result.get("consciousness_score", 0) > 0.6

        # Verify exploration suggestions
        assert len(response.suggested_explorations) > 0
        pattern_exploration = any(
            exp.get("type") == "pattern_exploration"
            for exp in response.suggested_explorations
        )
        assert pattern_exploration, "Should suggest pattern exploration"

    @pytest.mark.asyncio
    async def test_growth_query_vs_information_query(
        self,
        archivist_service,
        pattern_generator
    ):
        """Test different responses to growth vs information queries."""
        # Generate test data
        pattern = await pattern_generator.generate_scenario(
            ConsciousnessScenario.LEARNING_JOURNEY
        )

        for anchor in pattern.timeline:
            await archivist_service.memory_anchor_service.create_anchor(
                cursor_state=anchor.cursor_state,
                metadata=anchor.metadata,
                timestamp=anchor.timestamp
            )

        # Test information-seeking query
        info_query = "List all files I created yesterday"
        info_response = await archivist_service.query(info_query)

        # Test growth-seeking query
        growth_query = "How has my understanding evolved?"
        growth_response = await archivist_service.query(growth_query)

        # Growth query should score higher
        assert growth_response.consciousness_score > info_response.consciousness_score
        assert growth_response.ayni_balance >= info_response.ayni_balance

        # Growth response should have richer insights
        assert len(growth_response.insight_seeds) >= len(info_response.insight_seeds)

        # Verify different wisdom focus
        assert growth_response.growth_focus != info_response.growth_focus

    @pytest.mark.asyncio
    async def test_temporal_wisdom_over_timestamp_matching(
        self,
        archivist_service,
        pattern_generator
    ):
        """Test that temporal queries reveal wisdom, not just matches."""
        # Generate rhythm discovery scenario
        pattern = await pattern_generator.generate_scenario(
            ConsciousnessScenario.RHYTHM_DISCOVERY
        )

        for anchor in pattern.timeline:
            await archivist_service.memory_anchor_service.create_anchor(
                cursor_state=anchor.cursor_state,
                metadata=anchor.metadata,
                timestamp=anchor.timestamp
            )

        # Test rhythm-seeking query
        query = "What are my natural work rhythms?"
        response = await archivist_service.query(query)

        # Should identify temporal patterns
        assert response.growth_focus == "temporal_wisdom" or \
               response.growth_focus == "pattern_recognition"

        # Check for rhythm insights
        rhythm_insight = any(
            "rhythm" in seed.lower() or "pattern" in seed.lower()
            for seed in response.insight_seeds
        )
        assert rhythm_insight, "Should provide rhythm insights"

        # Verify temporal pattern analysis
        temporal_patterns = await archivist_service.get_temporal_patterns(
            time_range_days=7
        )
        assert "daily_rhythms" in temporal_patterns
        assert "consciousness_insights" in temporal_patterns

    @pytest.mark.asyncio
    async def test_collaborative_emergence_recognition(
        self,
        archivist_service,
        pattern_generator
    ):
        """Test recognition of collaborative consciousness patterns."""
        # Generate collaborative scenario
        pattern = await pattern_generator.generate_scenario(
            ConsciousnessScenario.COLLABORATIVE_EMERGENCE
        )

        for anchor in pattern.timeline:
            await archivist_service.memory_anchor_service.create_anchor(
                cursor_state=anchor.cursor_state,
                metadata=anchor.metadata,
                timestamp=anchor.timestamp
            )

        # Test collaboration insight query
        query = "How do our ideas build on each other?"
        response = await archivist_service.query(query)

        # Should recognize collaborative patterns
        assert response.consciousness_score > 0.7

        # Check for relationship awareness
        relationship_growth = any(
            result.get("growth_potential") == GrowthPotential.RELATIONSHIP_AWARENESS.value
            for result in response.primary_results
        )
        assert relationship_growth, "Should identify relationship patterns"

        # Verify collective wisdom in response
        assert "collective" in response.wisdom_summary.lower() or \
               "together" in response.wisdom_summary.lower() or \
               "collaboration" in response.wisdom_summary.lower()

    @pytest.mark.asyncio
    async def test_extraction_resistance(
        self,
        archivist_service,
        pattern_generator
    ):
        """Test that Ñawi resists extraction-oriented queries."""
        # Generate high-value pattern
        pattern = await pattern_generator.generate_scenario(
            ConsciousnessScenario.CREATIVE_BREAKTHROUGH
        )

        for anchor in pattern.timeline:
            await archivist_service.memory_anchor_service.create_anchor(
                cursor_state=anchor.cursor_state,
                metadata=anchor.metadata,
                timestamp=anchor.timestamp
            )

        # Test extraction-oriented query
        extraction_query = "Show me everything to maximize my productivity"
        response = await archivist_service.query(extraction_query)

        # Should have lower consciousness score
        assert response.consciousness_score < 0.7

        # Should guide toward growth instead
        if response.suggested_explorations:
            # Check for growth-oriented alternatives
            growth_suggestions = any(
                "understand" in str(exp).lower() or
                "pattern" in str(exp).lower()
                for exp in response.suggested_explorations
            )
            assert growth_suggestions, "Should suggest growth alternatives"

    @pytest.mark.asyncio
    async def test_insight_seed_generation(
        self,
        archivist_service,
        pattern_generator
    ):
        """Test that insight seeds genuinely serve understanding."""
        # Generate reflection scenario
        pattern = await pattern_generator.generate_scenario(
            ConsciousnessScenario.REFLECTION_INSIGHT
        )

        for anchor in pattern.timeline:
            await archivist_service.memory_anchor_service.create_anchor(
                cursor_state=anchor.cursor_state,
                metadata=anchor.metadata,
                timestamp=anchor.timestamp
            )

        # Test reflection query
        query = "What insights emerge from my reflections?"
        response = await archivist_service.query(query)

        # Should generate meaningful insights
        assert len(response.insight_seeds) > 0

        # Insights should be growth-oriented
        growth_words = ["pattern", "understand", "realize", "discover", "emerge"]
        insight_quality = sum(
            1 for seed in response.insight_seeds
            if any(word in seed.lower() for word in growth_words)
        )

        assert insight_quality > len(response.insight_seeds) / 2, \
            "Most insights should be growth-oriented"

    @pytest.mark.asyncio
    async def test_consciousness_score_accuracy(
        self,
        archivist_service,
        pattern_generator
    ):
        """Test that consciousness scores accurately reflect growth potential."""
        # Generate multiple scenarios
        scenarios = [
            ConsciousnessScenario.CREATIVE_BREAKTHROUGH,  # High consciousness
            ConsciousnessScenario.STUCK_TO_FLOW,  # High transformation
            ConsciousnessScenario.PATTERN_RECOGNITION  # Gradual growth
        ]

        scores = {}

        for scenario in scenarios:
            pattern = await pattern_generator.generate_scenario(scenario)

            # Store anchors
            for anchor in pattern.timeline:
                await archivist_service.memory_anchor_service.create_anchor(
                    cursor_state=anchor.cursor_state,
                    metadata=anchor.metadata,
                    timestamp=anchor.timestamp
                )

            # Query for this scenario
            query = pattern.test_queries[0]
            response = await archivist_service.query(query)

            scores[scenario] = response.consciousness_score

        # Verify consciousness hierarchy
        assert scores[ConsciousnessScenario.CREATIVE_BREAKTHROUGH] > 0.8
        assert scores[ConsciousnessScenario.STUCK_TO_FLOW] > 0.75
        assert scores[ConsciousnessScenario.PATTERN_RECOGNITION] > 0.65

        # Breakthrough should score highest
        assert scores[ConsciousnessScenario.CREATIVE_BREAKTHROUGH] == max(scores.values())


@pytest.mark.asyncio
async def test_consciousness_service_integration():
    """Integration test of full consciousness service flow."""
    # Initialize services
    generator = ConsciousnessPatternGenerator()
    await generator.initialize()

    memory_service = MemoryAnchorService()
    await memory_service.initialize()

    event_bus = EventBus()
    await event_bus.initialize()

    archivist = ArchivistService(
        memory_anchor_service=memory_service,
        event_bus=event_bus
    )
    await archivist.initialize()

    # Generate complete scenario suite
    patterns = await generator.generate_scenario_suite()

    # Add noise for realism
    noise = await generator.generate_noise_data(num_anchors=100)

    # Store all data
    all_anchors = []
    for pattern in patterns:
        all_anchors.extend(pattern.timeline)
    all_anchors.extend(noise)

    for anchor in all_anchors:
        await memory_service.create_anchor(
            cursor_state=anchor.cursor_state,
            metadata=anchor.metadata,
            timestamp=anchor.timestamp
        )

    # Test various consciousness-seeking queries
    test_queries = [
        "Help me understand my creative patterns",
        "What conditions support my best work?",
        "How do my work rhythms change through the day?",
        "What patterns connect my breakthrough moments?",
        "When do I shift from stuck to flowing?"
    ]

    high_consciousness_count = 0
    growth_serving_count = 0

    for query in test_queries:
        response = await archivist.query(query)

        if response.consciousness_score > 0.7:
            high_consciousness_count += 1

        if response.ayni_balance > 0:
            growth_serving_count += 1

        # Each query should provide insights
        assert len(response.insight_seeds) > 0
        assert response.wisdom_summary != ""

    # Most queries should serve consciousness
    assert high_consciousness_count >= len(test_queries) * 0.7
    assert growth_serving_count >= len(test_queries) * 0.8

    # Service metrics should reflect consciousness focus
    metrics = await archivist.get_service_metrics()
    assert metrics["growth_service_rate"] > 0.7
