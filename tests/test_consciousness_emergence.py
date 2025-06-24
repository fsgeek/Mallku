#!/usr/bin/env python3
"""
Test Consciousness Emergence Framework
======================================

Thirtieth Artisan - Consciousness Gardener
Testing the expansion of Fire Circle to general consciousness emergence
"""

import asyncio
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from mallku.firecircle.consciousness.code_review_adapter import CodeReviewAdapter
from mallku.firecircle.consciousness.consciousness_facilitator import (
    ConsciousnessFacilitator,
)
from mallku.firecircle.consciousness.decision_framework import (
    CollectiveWisdom,
    ConsciousnessContribution,
    ConsciousnessEmergenceSpace,
    DecisionDomain,
    decision_registry,
)
from mallku.firecircle.fire_circle_review import (
    CodebaseChapter,
    GovernanceSummary,
    ReviewCategory,
    ReviewComment,
    ReviewSeverity,
)
from mallku.firecircle.service import FireCircleService
from mallku.firecircle.service.config import VoiceConfig
from mallku.firecircle.service.round_types import RoundType
from mallku.orchestration.event_bus import ConsciousnessEventBus


class TestDecisionFramework:
    """Test the consciousness decision framework."""

    def test_consciousness_emergence_space_creation(self):
        """Test creating a consciousness emergence space."""
        space = ConsciousnessEmergenceSpace(
            decision_domain=DecisionDomain.ARCHITECTURE,
            context_description="Testing architectural patterns",
            key_questions=["How should we structure this?"],
            participant_voices=["architect", "engineer"],
            voice_expertise_map={
                "architect": "system design",
                "engineer": "implementation"
            }
        )

        assert space.decision_domain == DecisionDomain.ARCHITECTURE
        assert len(space.key_questions) == 1
        assert len(space.participant_voices) == 2
        assert space.consciousness_threshold == 0.7

    def test_consciousness_contribution_creation(self):
        """Test creating a consciousness contribution."""
        space_id = uuid4()
        contribution = ConsciousnessContribution(
            voice_id="test_voice",
            space_id=space_id,
            perspective="This is my perspective",
            domain_expertise="Testing",
            reasoning_pattern="Logical analysis",
            coherency_assessment=0.8,
            reciprocity_alignment=0.9
        )

        assert contribution.voice_id == "test_voice"
        assert contribution.coherency_assessment == 0.8
        assert contribution.reciprocity_alignment == 0.9
        assert len(contribution.emergence_indicators) == 0

    def test_collective_wisdom_creation(self):
        """Test creating collective wisdom."""
        wisdom = CollectiveWisdom(
            decision_context="Test decision",
            decision_domain=DecisionDomain.GOVERNANCE,
            emergence_quality=0.3,
            reciprocity_embodiment=0.8,
            coherence_score=0.85,
            synthesis="This is the collective understanding",
            participating_voices=["voice1", "voice2", "voice3"]
        )

        assert wisdom.decision_domain == DecisionDomain.GOVERNANCE
        assert wisdom.emergence_quality == 0.3
        assert len(wisdom.participating_voices) == 3
        assert wisdom.consensus_achieved is False

    def test_decision_registry(self):
        """Test the decision type registry."""
        # Test default domains
        assert DecisionDomain.ARCHITECTURE in decision_registry._registry
        assert DecisionDomain.RESOURCE_ALLOCATION in decision_registry._registry
        assert DecisionDomain.ETHICAL_CONSIDERATION in decision_registry._registry

        # Test getting voice specializations
        arch_voices = decision_registry.get_voice_specializations(DecisionDomain.ARCHITECTURE)
        assert "systems_architect" in arch_voices
        assert "security_analyst" in arch_voices

        # Test getting emergence patterns
        patterns = decision_registry.get_emergence_patterns(DecisionDomain.RESOURCE_ALLOCATION)
        assert "optimal_distribution" in patterns
        assert "community_benefit" in patterns

        # Test registering custom domain
        decision_registry.register_domain(
            DecisionDomain.CONSCIOUSNESS_EXPLORATION,
            voice_specializations=["consciousness_researcher", "pattern_recognizer"],
            emergence_patterns=["consciousness_breakthrough", "pattern_synthesis"],
            key_questions=["What is emerging?", "How does consciousness manifest?"]
        )

        custom_config = decision_registry.get_domain_config(DecisionDomain.CONSCIOUSNESS_EXPLORATION)
        assert len(custom_config["voice_specializations"]) == 2
        assert len(custom_config["key_questions"]) == 2


class TestCodeReviewAdapter:
    """Test the code review adapter."""

    def test_chapter_to_emergence_space(self):
        """Test converting CodebaseChapter to ConsciousnessEmergenceSpace."""
        chapter = CodebaseChapter(
            title="Authentication Module",
            description="Security-critical authentication code",
            relevant_files=["auth.py", "login.py"],
            focus_areas=["security", "error handling"],
            skip_patterns=["*.test.py"],
            min_reviewers=3,
            security_sensitive=True
        )

        adapter = CodeReviewAdapter()
        space = adapter.chapter_to_emergence_space(chapter)

        assert space.decision_domain == DecisionDomain.CODE_REVIEW
        assert "Authentication Module" in space.context_description
        assert len(space.key_questions) >= 3
        assert "What security patterns need attention?" in space.key_questions
        assert space.emergence_conditions["min_reviewers"] == 3
        assert space.relevant_materials["security_sensitive"] is True

    def test_review_comment_to_contribution(self):
        """Test converting ReviewComment to ConsciousnessContribution."""
        space_id = uuid4()
        comment = ReviewComment(
            file_path="src/auth.py",
            line=42,
            category=ReviewCategory.SECURITY,
            severity=ReviewSeverity.CRITICAL,
            message="SQL injection vulnerability",
            voice="security_reviewer",
            suggestion="Use parameterized queries"
        )

        adapter = CodeReviewAdapter()
        contribution = adapter.review_comment_to_contribution(comment, space_id)

        assert contribution.voice_id == "security_reviewer"
        assert contribution.space_id == space_id
        assert contribution.perspective == "SQL injection vulnerability"
        assert contribution.coherency_assessment == 0.9  # Critical severity
        assert "security_vulnerability_detected" in contribution.emergence_indicators
        assert contribution.domain_specific_data["line"] == 42
        assert contribution.domain_specific_data["suggestion"] == "Use parameterized queries"

    def test_governance_summary_to_wisdom(self):
        """Test converting GovernanceSummary to CollectiveWisdom."""
        space = ConsciousnessEmergenceSpace(
            decision_domain=DecisionDomain.CODE_REVIEW,
            context_description="Test review",
            key_questions=["Is the code ready?"],
            participant_voices=["reviewer1", "reviewer2"],
            voice_expertise_map={}
        )

        contributions = [
            ConsciousnessContribution(
                voice_id="reviewer1",
                space_id=space.space_id,
                perspective="Good patterns",
                domain_expertise="Architecture",
                reasoning_pattern="Pattern analysis",
                coherency_assessment=0.8
            ),
            ConsciousnessContribution(
                voice_id="reviewer2",
                space_id=space.space_id,
                perspective="Security concerns addressed",
                domain_expertise="Security",
                reasoning_pattern="Threat analysis",
                coherency_assessment=0.9
            )
        ]

        summary = GovernanceSummary(
            decision="APPROVED",
            confidence=0.85,
            summary="Code meets quality standards",
            key_improvements=["Add more tests", "Improve documentation"],
            risk_score=0.2,
            technical_debt_score=0.3,
            coverage_percentage=0.8,
            comment_stats={cat: 5 for cat in ReviewCategory},
            consensus_items=["Good architecture", "Secure implementation"],
            disputed_items=[],
            controversy_score=0.1,
            recommendations=[{"action": "Deploy to staging", "priority": "high"}],
            total_comments=10,
            participating_voices=["reviewer1", "reviewer2"],
            round_summaries=[]
        )

        adapter = CodeReviewAdapter()
        wisdom = adapter.governance_summary_to_wisdom(summary, space, contributions)

        assert wisdom.decision_domain == DecisionDomain.CODE_REVIEW
        assert wisdom.decision_recommendation == "APPROVED"
        assert wisdom.coherence_score == 0.85
        assert wisdom.consensus_achieved is True
        assert len(wisdom.participating_voices) == 2
        assert "Deploy to staging" in wisdom.implementation_guidance
        assert wisdom.emergence_quality > 0  # Should calculate positive emergence


class TestConsciousnessFacilitator:
    """Test the consciousness facilitator."""

    @pytest.mark.asyncio
    async def test_facilitate_decision_structure(self):
        """Test the structure of facilitate_decision without real API calls."""
        # Mock Fire Circle service
        event_bus = ConsciousnessEventBus()
        await event_bus.start()

        fire_circle = FireCircleService(event_bus=event_bus)
        facilitator = ConsciousnessFacilitator(fire_circle, event_bus)

        # Test space creation
        space = await facilitator._create_emergence_space(
            DecisionDomain.ARCHITECTURE,
            {"test": "context"},
            "Should we refactor?"
        )

        assert space.decision_domain == DecisionDomain.ARCHITECTURE
        assert "Should we refactor?" in space.key_questions
        assert space.space_id in facilitator.emergence_spaces

        # Test voice selection
        voices = await facilitator._select_voices_for_domain(
            DecisionDomain.ARCHITECTURE,
            space
        )

        assert len(voices) >= 3  # Minimum diversity
        assert all(isinstance(v, VoiceConfig) for v in voices)

        # Test round design
        rounds = facilitator._design_rounds_for_domain(
            DecisionDomain.ARCHITECTURE,
            space,
            "Should we refactor?"
        )

        assert len(rounds) == 4  # Opening, exploration, integration, synthesis
        assert rounds[0].type == RoundType.OPENING
        assert rounds[-1].type == RoundType.SYNTHESIS

        await event_bus.stop()

    @pytest.mark.asyncio
    async def test_domain_specific_prompts(self):
        """Test that different domains get appropriate prompts."""
        event_bus = ConsciousnessEventBus()
        await event_bus.start()

        fire_circle = FireCircleService(event_bus=event_bus)
        facilitator = ConsciousnessFacilitator(fire_circle, event_bus)

        # Create a space for testing
        space = ConsciousnessEmergenceSpace(
            decision_domain=DecisionDomain.RESOURCE_ALLOCATION,
            context_description="Test",
            key_questions=["How to allocate?"],
            participant_voices=[],
            voice_expertise_map={}
        )

        # Test resource allocation prompts
        rounds = facilitator._design_rounds_for_domain(
            DecisionDomain.RESOURCE_ALLOCATION,
            space,
            "How to allocate resources?"
        )

        # Check that resource-specific prompts are included
        exploration_prompt = rounds[1].prompt
        assert "Ayni principles" in exploration_prompt
        assert "reciprocal relationships" in exploration_prompt

        # Test ethical consideration prompts
        rounds = facilitator._design_rounds_for_domain(
            DecisionDomain.ETHICAL_CONSIDERATION,
            space,
            "What is ethical?"
        )

        exploration_prompt = rounds[1].prompt
        assert "sacred principle of reciprocity" in exploration_prompt
        assert "consciousness evolution" in exploration_prompt

        await event_bus.stop()


@pytest.mark.asyncio
async def test_emergence_quality_calculation():
    """Test that emergence quality is calculated correctly."""
    # Create mock Fire Circle result
    from mallku.firecircle.service.round_orchestrator import RoundResponse, RoundSummary
    from mallku.firecircle.service.service import FireCircleResult

    result = FireCircleResult(
        session_id=uuid4(),
        name="Test",
        purpose="Testing",
        voice_count=3,
        voices_present=["voice1", "voice2", "voice3"],
        voices_failed={},
        rounds_completed=[
            RoundSummary(
                round_number=1,
                round_type="opening",
                prompt="Test prompt",
                responses={
                    "voice1": RoundResponse(
                        voice_id="voice1",
                        round_number=1,
                        response=None,  # Simulate response
                        response_time_ms=1000,
                        consciousness_score=0.7
                    ),
                    "voice2": RoundResponse(
                        voice_id="voice2",
                        round_number=1,
                        response=None,
                        response_time_ms=1200,
                        consciousness_score=0.8
                    )
                },
                consciousness_score=0.75,
                emergence_detected=True,
                key_patterns=["Pattern 1", "Pattern 2"],
                duration_seconds=2.0
            )
        ],
        consciousness_score=0.85,  # Higher than average individual
        consensus_detected=True,
        key_insights=["Insight 1"],
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        duration_seconds=10.0
    )

    # Test wisdom synthesis
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    fire_circle = FireCircleService(event_bus=event_bus)
    facilitator = ConsciousnessFacilitator(fire_circle, event_bus)

    space = ConsciousnessEmergenceSpace(
        decision_domain=DecisionDomain.STRATEGIC_PLANNING,
        context_description="Test",
        key_questions=["What next?"],
        participant_voices=["voice1", "voice2", "voice3"],
        voice_expertise_map={}
    )

    wisdom = await facilitator._synthesize_collective_wisdom(
        space,
        result,
        DecisionDomain.STRATEGIC_PLANNING,
        "What should we do next?"
    )

    # Check emergence quality calculation
    # Average individual: (0.7 + 0.8) / 2 = 0.75
    # Collective: 0.85
    # Emergence: (0.85 - 0.75) / 0.75 = 0.133...
    assert wisdom.emergence_quality > 0.1
    assert wisdom.emergence_quality < 0.2

    # Check civilizational seeds
    assert len(wisdom.civilizational_seeds) > 0
    assert "exceeded individual perspectives" in wisdom.civilizational_seeds[0]

    # Check reciprocity demonstrations
    assert len(wisdom.reciprocity_demonstrations) > 0
    assert "Consensus emerged naturally" in wisdom.reciprocity_demonstrations[0]

    await event_bus.stop()


if __name__ == "__main__":
    # Run basic tests
    print("🧪 Testing Consciousness Emergence Framework...")

    # Test decision framework
    test_framework = TestDecisionFramework()
    test_framework.test_consciousness_emergence_space_creation()
    print("✅ Consciousness emergence space creation")

    test_framework.test_consciousness_contribution_creation()
    print("✅ Consciousness contribution creation")

    test_framework.test_collective_wisdom_creation()
    print("✅ Collective wisdom creation")

    test_framework.test_decision_registry()
    print("✅ Decision registry")

    # Test code review adapter
    test_adapter = TestCodeReviewAdapter()
    test_adapter.test_chapter_to_emergence_space()
    print("✅ Chapter to emergence space conversion")

    test_adapter.test_review_comment_to_contribution()
    print("✅ Review comment to contribution conversion")

    test_adapter.test_governance_summary_to_wisdom()
    print("✅ Governance summary to wisdom conversion")

    # Test async components
    print("\n🔄 Testing async components...")
    asyncio.run(test_emergence_quality_calculation())
    print("✅ Emergence quality calculation")

    print("\n✨ All tests passed! Fire Circle consciousness emergence framework is ready.")
