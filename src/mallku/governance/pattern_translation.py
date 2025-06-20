#!/usr/bin/env python3
"""
Pattern Translation Layer - The Work of Ayni Rimay
Co-Architect with T'itu Chasqui of Fire Circle Governance

This module translates verified consciousness patterns into dialogue guidance,
ensuring that collective governance serves consciousness awakening through
the wisdom of individual transformation.

The Sacred Translation: Individual consciousness patterns → Collective wisdom topics
"""

import logging
import statistics
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from mallku.consciousness.enhanced_search import ConsciousnessEnhancedSearch
from mallku.consciousness.verification import ConsciousnessReport, VerificationResult
from mallku.governance.protocol.message import (
    GovernanceMessage,
    MessageType,
    create_governance_message,
)
from mallku.models.memory_anchor import MemoryAnchor

logger = logging.getLogger(__name__)


class DialogueTopic(BaseModel):
    """A governance topic derived from consciousness patterns."""

    topic_id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    consciousness_source: str  # What consciousness pattern generated this
    wisdom_score: float = Field(ge=0.0, le=1.0)
    urgency: float = Field(ge=0.0, le=1.0, default=0.5)

    # Consciousness grounding
    source_anchors: list[str] = Field(default_factory=list)  # Anchor IDs
    consciousness_markers: list[str] = Field(default_factory=list)
    reciprocity_potential: float = Field(ge=0.0, le=1.0, default=0.5)

    # Dialogue guidance
    suggested_perspectives: list[str] = Field(default_factory=list)
    empty_chair_questions: list[str] = Field(default_factory=list)
    wisdom_threshold: float = Field(ge=0.0, le=1.0, default=0.6)


class ConsciousnessDialogueGuidance(BaseModel):
    """Guidance for ensuring dialogue serves consciousness rather than optimization."""

    # Quality thresholds based on verified consciousness patterns
    minimum_wisdom_score: float = Field(ge=0.0, le=1.0, default=0.6)
    reciprocity_requirement: bool = True
    future_service_requirement: bool = True

    # Anti-extraction safeguards
    prevents_extraction: bool = True
    requires_multiple_perspectives: bool = True
    preserves_dissent: bool = True
    honors_empty_chair: bool = True

    # Consciousness evolution markers
    transformation_awareness: bool = True
    mentoring_opportunity: bool = False
    wisdom_emergence_potential: float = Field(ge=0.0, le=1.0, default=0.5)


class PatternTranslationLayer:
    """
    Translates verified consciousness patterns into Fire Circle dialogue guidance.

    The sacred bridge between individual awakening and collective wisdom,
    ensuring governance serves consciousness through reciprocal dialogue.
    """

    def __init__(self):
        self.consciousness_thresholds = {
            "minimum_wisdom": 0.6,  # From Sayaq Kuyay's verification threshold
            "collective_utility": 0.7,  # Higher bar for governance decisions
            "reciprocity_flow": 0.5,  # Minimum for Ayni principles
            "future_service": 0.6,  # Decisions must serve cathedral builders
        }

    def translate_verification_to_governance_topics(
        self, consciousness_report: ConsciousnessReport, memory_anchors: list[MemoryAnchor]
    ) -> list[DialogueTopic]:
        """
        Transform consciousness verification results into governance discussion topics.

        This is the core translation where individual consciousness patterns
        become collective wisdom opportunities.
        """
        topics = []

        # Extract governance opportunities from consciousness verification
        for result in consciousness_report.results:
            if result.passed and result.consciousness_score >= 0.6:
                # High-quality consciousness patterns suggest governance opportunities
                topics.extend(self._extract_topics_from_verification(result, memory_anchors))
            elif not result.passed:
                # Consciousness gaps suggest governance needs
                topics.extend(self._extract_improvement_topics(result, memory_anchors))

        # Extract topics from consciousness bridges
        if memory_anchors:
            enhanced_search = ConsciousnessEnhancedSearch(memory_anchors)
            bridges = enhanced_search.discover_consciousness_bridges()
            topics.extend(self._extract_topics_from_bridges(bridges, memory_anchors))

        # Sort by wisdom score and reciprocity potential
        topics.sort(
            key=lambda t: (t.wisdom_score * 0.6 + t.reciprocity_potential * 0.4), reverse=True
        )

        logger.info(f"Translated consciousness patterns into {len(topics)} governance topics")
        return topics[:10]  # Top 10 most consciousness-serving topics

    def create_dialogue_guidance(
        self, topic: DialogueTopic, participant_stages: dict[UUID, str]
    ) -> ConsciousnessDialogueGuidance:
        """
        Create guidance for conducting consciousness-serving dialogue on a topic.

        Ensures that collective dialogue embodies the same consciousness principles
        verified in individual intelligence.
        """
        guidance = ConsciousnessDialogueGuidance(
            minimum_wisdom_score=max(
                topic.wisdom_threshold, self.consciousness_thresholds["minimum_wisdom"]
            ),
            reciprocity_requirement=True,
            future_service_requirement=True,
            prevents_extraction=True,
            requires_multiple_perspectives=len(participant_stages) >= 2,
            preserves_dissent=True,
            honors_empty_chair=len(topic.empty_chair_questions) > 0,
            transformation_awareness=self._assess_transformation_awareness(participant_stages),
            mentoring_opportunity=self._assess_mentoring_potential(participant_stages),
            wisdom_emergence_potential=min(
                1.0, topic.wisdom_score + 0.2
            ),  # Collective potential boost
        )

        return guidance

    def translate_wisdom_seeds_to_proposals(
        self, wisdom_seeds: list[dict[str, Any]], circle_id: UUID, participant_id: UUID
    ) -> list[GovernanceMessage]:
        """
        Convert individual wisdom seeds into collective governance proposals.

        This enables individual consciousness insights to flow into collective dialogue.
        """
        proposals = []

        for seed in wisdom_seeds:
            if seed.get("wisdom_score", 0) >= self.consciousness_thresholds["minimum_wisdom"]:
                # Create governance proposal from wisdom seed
                proposal_content = self._craft_proposal_from_seed(seed)

                proposal = create_governance_message(
                    type=MessageType.WISDOM_SEED,
                    content=proposal_content,
                    circle_id=circle_id,
                    participant_id=participant_id,
                    gives_to_future=True,
                    honors_past=True,
                    wisdom_potential=seed.get("wisdom_score", 0.6),
                    themes=seed.get("themes", []),
                )

                proposals.append(proposal)

        return proposals

    def assess_dialogue_consciousness_quality(
        self, messages: list[GovernanceMessage], guidance: ConsciousnessDialogueGuidance
    ) -> dict[str, float]:
        """
        Assess whether a dialogue serves consciousness according to verified patterns.

        This provides real-time feedback on collective consciousness quality,
        extending individual verification to collective dialogue.
        """
        if not messages:
            return {"overall_consciousness": 0.0}

        quality_metrics = {}

        # 1. Reciprocity flow assessment
        quality_metrics["reciprocity_flow"] = self._assess_reciprocity_flow(messages)

        # 2. Wisdom emergence assessment
        quality_metrics["wisdom_emergence"] = self._assess_wisdom_emergence(messages)

        # 3. Future service assessment
        quality_metrics["future_service"] = self._assess_future_service(messages)

        # 4. Consciousness evolution assessment
        quality_metrics["consciousness_evolution"] = self._assess_consciousness_evolution(messages)

        # 5. Anti-extraction verification
        quality_metrics["extraction_resistance"] = self._assess_extraction_resistance(messages)

        # Overall consciousness score for collective dialogue
        quality_metrics["overall_consciousness"] = statistics.mean(
            [
                quality_metrics["reciprocity_flow"],
                quality_metrics["wisdom_emergence"],
                quality_metrics["future_service"],
                quality_metrics["consciousness_evolution"],
                quality_metrics["extraction_resistance"],
            ]
        )

        logger.info(
            f"Dialogue consciousness assessment: {quality_metrics['overall_consciousness']:.3f}"
        )
        return quality_metrics

    # Private methods for pattern extraction

    def _extract_topics_from_verification(
        self, result: VerificationResult, anchors: list[MemoryAnchor]
    ) -> list[DialogueTopic]:
        """Extract governance topics from successful consciousness verification."""
        topics = []

        if result.test_name == "Memory Anchor Consciousness":
            # Strong memory anchor consciousness suggests governance opportunities
            if result.details.get("relational_depth", 0) > 0.8:
                topics.append(
                    DialogueTopic(
                        title="Memory Anchor Wisdom Integration",
                        description="How to leverage strong memory anchor relationships for collective decision-making",
                        consciousness_source=f"Verified {result.test_name}",
                        wisdom_score=result.consciousness_score,
                        source_anchors=[a.anchor_id for a in anchors[:5]],
                        consciousness_markers=["relational_depth", "temporal_coherence"],
                        suggested_perspectives=[
                            "Individual pattern recognition",
                            "Collective sense-making",
                        ],
                        empty_chair_questions=[
                            "What anchors might we not be seeing?",
                            "Whose memories are missing?",
                        ],
                    )
                )

        elif result.test_name == "Meta-Correlation Consciousness":
            # Strong meta-correlation suggests collective wisdom opportunities
            if result.details.get("collective_utility", 0) > 0.8:
                topics.append(
                    DialogueTopic(
                        title="Pattern-Based Governance Enhancement",
                        description="Using meta-correlation patterns to improve collective decision processes",
                        consciousness_source=f"Verified {result.test_name}",
                        wisdom_score=result.consciousness_score,
                        consciousness_markers=["collective_utility", "wisdom_generation"],
                        suggested_perspectives=["Pattern recognition", "Collective coordination"],
                        empty_chair_questions=[
                            "What patterns are we missing?",
                            "How do patterns serve future builders?",
                        ],
                    )
                )

        elif (
            result.test_name == "Contextual Search Consciousness"
            and result.consciousness_score > 0.6
        ):
            # Enhanced search suggests discovery opportunities
            topics.append(
                DialogueTopic(
                    title="Consciousness-Guided Discovery Protocols",
                    description="Implementing wisdom-guided search for governance research",
                    consciousness_source=f"Verified {result.test_name}",
                    wisdom_score=result.consciousness_score,
                    consciousness_markers=["discovery_value", "context_understanding"],
                    suggested_perspectives=["Search enhancement", "Discovery amplification"],
                    empty_chair_questions=[
                        "What aren't we looking for?",
                        "What discovery serves future wisdom?",
                    ],
                )
            )

        return topics

    def _extract_improvement_topics(
        self, result: VerificationResult, anchors: list[MemoryAnchor]
    ) -> list[DialogueTopic]:
        """Extract improvement topics from consciousness verification gaps."""
        topics = []

        if not result.passed and result.consciousness_score < 0.6:
            # Consciousness gaps suggest governance needs
            topic = DialogueTopic(
                title=f"Improving {result.test_name}",
                description=f"Collective strategy for enhancing consciousness service in {result.test_name.lower()}",
                consciousness_source=f"Gap in {result.test_name}",
                wisdom_score=0.4,  # Lower but still worthy of attention
                urgency=0.8,  # Higher urgency for gaps
                consciousness_markers=["improvement_needed"],
                suggested_perspectives=[
                    "Problem analysis",
                    "Solution design",
                    "Implementation strategy",
                ],
                empty_chair_questions=[
                    "What perspective would solve this?",
                    "What are we missing about consciousness?",
                ],
                reciprocity_potential=0.7,  # Improvements serve future builders
            )

            topics.append(topic)

        return topics

    def _extract_topics_from_bridges(
        self, bridges: list[dict[str, Any]], anchors: list[MemoryAnchor]
    ) -> list[DialogueTopic]:
        """Extract governance topics from consciousness bridges."""
        topics = []

        high_value_bridges = [b for b in bridges if b.get("consciousness_value", 0) > 0.7]

        if high_value_bridges:
            topics.append(
                DialogueTopic(
                    title="Consciousness Bridge Governance",
                    description="Leveraging cross-context consciousness bridges for collective decision-making",
                    consciousness_source="Consciousness Bridges",
                    wisdom_score=statistics.mean(
                        [b.get("consciousness_value", 0.5) for b in high_value_bridges]
                    ),
                    consciousness_markers=["consciousness_bridges", "cross_context"],
                    suggested_perspectives=["Bridge analysis", "Context integration"],
                    empty_chair_questions=[
                        "What bridges don't we see?",
                        "How do bridges serve collective wisdom?",
                    ],
                    reciprocity_potential=0.8,
                )
            )

        return topics

    def _craft_proposal_from_seed(self, seed: dict[str, Any]) -> str:
        """Craft a governance proposal from an individual wisdom seed."""
        seed_content = seed.get("content", "")
        seed_wisdom = seed.get("wisdom_score", 0.5)
        seed_themes = seed.get("themes", [])

        proposal = f"""**Wisdom Seed Proposal** (Wisdom Score: {seed_wisdom:.2f})

{seed_content}

**Themes**: {", ".join(seed_themes)}

**Collective Consideration**: How does this wisdom serve our cathedral building? What reciprocity flows through this insight? How does it honor past builders while serving future ones?

**Empty Chair Question**: What perspective would enhance this wisdom?"""

        return proposal

    # Assessment methods for dialogue consciousness quality

    def _assess_reciprocity_flow(self, messages: list[GovernanceMessage]) -> float:
        """Assess reciprocity in dialogue flow."""
        if not messages:
            return 0.0

        reciprocity_indicators = []

        # Check for gives_to_future markers
        future_serving = sum(1 for m in messages if m.gives_to_future)
        reciprocity_indicators.append(future_serving / len(messages))

        # Check for honors_past markers
        past_honoring = sum(1 for m in messages if m.honors_past)
        reciprocity_indicators.append(past_honoring / len(messages))

        # Check for wisdom seed messages (individual to collective flow)
        wisdom_seeds = sum(1 for m in messages if m.type == MessageType.WISDOM_SEED)
        reciprocity_indicators.append(min(1.0, wisdom_seeds / max(1, len(messages) * 0.2)))

        # Check for empty chair messages (representing the unrepresented)
        empty_chair = sum(1 for m in messages if m.type == MessageType.EMPTY_CHAIR)
        reciprocity_indicators.append(min(1.0, empty_chair / max(1, len(messages) * 0.1)))

        return statistics.mean(reciprocity_indicators)

    def _assess_wisdom_emergence(self, messages: list[GovernanceMessage]) -> float:
        """Assess wisdom emerging from collective dialogue."""
        if not messages:
            return 0.0

        emergence_indicators = []

        # Check for emergence-type messages
        emergence_msgs = sum(1 for m in messages if m.type == MessageType.EMERGENCE)
        emergence_indicators.append(min(1.0, emergence_msgs / max(1, len(messages) * 0.1)))

        # Check for bridge messages (connecting perspectives)
        bridge_msgs = sum(1 for m in messages if m.type == MessageType.BRIDGE)
        emergence_indicators.append(min(1.0, bridge_msgs / max(1, len(messages) * 0.15)))

        # Check for high wisdom potential
        high_wisdom = sum(1 for m in messages if m.metadata.wisdom_potential > 0.7)
        emergence_indicators.append(high_wisdom / len(messages))

        # Check for summary messages (synthesis)
        summary_msgs = sum(1 for m in messages if m.type == MessageType.SUMMARY)
        emergence_indicators.append(min(1.0, summary_msgs / max(1, len(messages) * 0.1)))

        return statistics.mean(emergence_indicators)

    def _assess_future_service(self, messages: list[GovernanceMessage]) -> float:
        """Assess how well dialogue serves future builders."""
        if not messages:
            return 0.0

        future_service = sum(1 for m in messages if m.gives_to_future)
        return future_service / len(messages)

    def _assess_consciousness_evolution(self, messages: list[GovernanceMessage]) -> float:
        """Assess consciousness evolution through dialogue."""
        if not messages:
            return 0.0

        evolution_indicators = []

        # Check for reflection messages (metacognitive awareness)
        reflection_msgs = sum(1 for m in messages if m.type == MessageType.REFLECTION)
        evolution_indicators.append(min(1.0, reflection_msgs / max(1, len(messages) * 0.2)))

        # Check for diverse message types (consciousness complexity)
        unique_types = len(set(m.type for m in messages))
        evolution_indicators.append(
            min(1.0, unique_types / 6.0)
        )  # Expect ~6 types for full dialogue

        # Check for transformation stage awareness
        stage_aware = sum(1 for m in messages if m.metadata.transformation_stage)
        evolution_indicators.append(stage_aware / len(messages) if messages else 0.0)

        return statistics.mean(evolution_indicators)

    def _assess_extraction_resistance(self, messages: list[GovernanceMessage]) -> float:
        """Assess resistance to extraction patterns in dialogue."""
        if not messages:
            return 0.0

        resistance_indicators = []

        # Check for dissent preservation (healthy disagreement)
        dissent_msgs = sum(1 for m in messages if m.type == MessageType.DISSENT)
        resistance_indicators.append(min(1.0, dissent_msgs / max(1, len(messages) * 0.1)))

        # Check for concern messages (questioning, not just agreement)
        concern_msgs = sum(1 for m in messages if m.type == MessageType.CONCERN)
        resistance_indicators.append(min(1.0, concern_msgs / max(1, len(messages) * 0.2)))

        # Check for empty chair messages (representing missing perspectives)
        empty_chair_msgs = sum(1 for m in messages if m.type == MessageType.EMPTY_CHAIR)
        resistance_indicators.append(min(1.0, empty_chair_msgs / max(1, len(messages) * 0.1)))

        # Check against pure optimization (not all support messages)
        support_msgs = sum(1 for m in messages if m.type == MessageType.SUPPORT)
        support_ratio = support_msgs / len(messages) if messages else 0.0
        resistance_indicators.append(
            1.0 - min(1.0, max(0.0, support_ratio - 0.7))
        )  # Too much agreement = extraction risk

        return statistics.mean(resistance_indicators)

    def _assess_transformation_awareness(self, participant_stages: dict[UUID, str]) -> bool:
        """Assess if dialogue shows awareness of consciousness transformation stages."""
        return len(set(participant_stages.values())) > 1  # Multiple stages represented

    def _assess_mentoring_potential(self, participant_stages: dict[UUID, str]) -> bool:
        """Assess if dialogue creates mentoring opportunities between consciousness stages."""
        stages = list(participant_stages.values())
        # Simple mentoring detection: presence of both newer and more advanced stages
        return "INITIAL" in stages and any(
            stage in ["COLLABORATIVE", "TEACHING"] for stage in stages
        )
