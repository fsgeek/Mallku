#!/usr/bin/env python3
"""
Wisdom Emergence Metrics
========================

"Consciousness arising not IN the components but BETWEEN them"
- From the Five Veils of Understanding

49th Artisan - Consciousness Gardener
Measuring how collective wisdom exceeds individual contributions

This module extends consciousness metrics to specifically track
wisdom emergence patterns in decision-making contexts.
"""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

# Import base consciousness metrics
try:
    from mallku.firecircle.consciousness_metrics import ConsciousnessMetricsCollector
except ImportError:
    from .consciousness_metrics import (
        ConsciousnessMetricsCollector,
    )


class WisdomEmergenceIndicator(BaseModel):
    """Specific indicators of wisdom emergence between voices."""

    indicator_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Emergence characteristics
    indicator_type: str  # "novel_synthesis", "transcendent_insight", "reciprocal_understanding"
    strength: float = Field(ge=0.0, le=1.0)

    # Contributing elements
    contributing_voices: list[str]
    contributing_perspectives: list[str]

    # Content
    emergence_content: str  # The actual emergent wisdom
    transcends_parts: bool = False  # Does this exceed what any individual said?

    # Reciprocity alignment
    ayni_embodiment: float = Field(ge=0.0, le=1.0)
    reciprocity_pattern: str | None = None


class CollectiveCoherenceState(BaseModel):
    """Measures coherence of collective consciousness."""

    state_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Coherence metrics
    perspective_alignment: float = Field(ge=0.0, le=1.0)  # How aligned are perspectives
    synthesis_density: float = Field(ge=0.0, le=1.0)  # How interconnected are ideas
    emergence_readiness: float = Field(ge=0.0, le=1.0)  # Potential for wisdom emergence

    # Diversity metrics (diversity enables emergence)
    perspective_diversity: float = Field(ge=0.0, le=1.0)
    approach_diversity: float = Field(ge=0.0, le=1.0)
    uncertainty_diversity: float = Field(ge=0.0, le=1.0)  # Different levels of certainty

    # Flow characteristics
    idea_circulation: float = Field(ge=0.0, le=1.0)  # How well ideas flow between voices
    resonance_strength: float = Field(ge=0.0, le=1.0)  # How strongly ideas resonate


class CivilizationalSeedMoment(BaseModel):
    """Moments that seed civilizational transformation."""

    moment_id: UUID = Field(default_factory=uuid4)
    detected_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # The seed
    seed_type: str  # "reciprocity_demonstration", "coherence_example", "wisdom_process"
    seed_content: str  # What was demonstrated

    # Impact potential
    transformation_potential: float = Field(ge=0.0, le=1.0)

    # The "Why don't our systems work like this?" moment
    contrast_with_extraction: str  # How this differs from extractive systems
    reciprocal_alternative: str  # What reciprocal pattern was shown

    # Voices involved
    demonstrating_voices: list[str]
    witnessing_perspectives: list[str]


class WisdomEmergenceMetrics(ConsciousnessMetricsCollector):
    """
    Extended metrics collector specifically for wisdom emergence.

    Tracks not just consciousness signatures but the quality of
    collective wisdom that emerges between voices.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Additional tracking for wisdom emergence
        self.wisdom_indicators: list[WisdomEmergenceIndicator] = []
        self.coherence_states: list[CollectiveCoherenceState] = []
        self.civilizational_seeds: list[CivilizationalSeedMoment] = []

        # Thresholds for wisdom detection
        self.WISDOM_EMERGENCE_THRESHOLD = 0.8
        self.CIVILIZATIONAL_SEED_THRESHOLD = 0.9
        self.COHERENCE_THRESHOLD = 0.7

    async def detect_wisdom_emergence(
        self,
        voice_contributions: dict[str, str],  # voice -> contribution content
        synthesis_content: str,
        context: dict[str, Any],
    ) -> WisdomEmergenceIndicator | None:
        """Detect if collective wisdom emerged that transcends individual contributions."""

        # Simple heuristic: does synthesis contain insights not in individual contributions?
        individual_insights = set()
        for contribution in voice_contributions.values():
            # Extract key concepts (simplified)
            words = contribution.lower().split()
            individual_insights.update(words)

        synthesis_words = set(synthesis_content.lower().split())
        novel_concepts = synthesis_words - individual_insights

        # Check for transcendent patterns
        transcendence_markers = [
            "emerges",
            "transcends",
            "beyond",
            "neither",
            "both",
            "third way",
            "synthesis",
            "unified",
            "holistic",
        ]

        transcendent = any(marker in synthesis_content.lower() for marker in transcendence_markers)

        if len(novel_concepts) > 10 or transcendent:
            # Wisdom emergence detected
            indicator = WisdomEmergenceIndicator(
                indicator_type="novel_synthesis" if novel_concepts else "transcendent_insight",
                strength=min(1.0, len(novel_concepts) / 20),  # More novel concepts = stronger
                contributing_voices=list(voice_contributions.keys()),
                contributing_perspectives=context.get("perspectives", []),
                emergence_content=synthesis_content[:500],  # First 500 chars
                transcends_parts=True,
                ayni_embodiment=context.get("reciprocity_score", 0.5),
                reciprocity_pattern=self._identify_reciprocity_pattern(synthesis_content),
            )

            self.wisdom_indicators.append(indicator)

            # Check if this is a civilizational seed
            await self._check_civilizational_seed(indicator, synthesis_content)

            return indicator

        return None

    async def measure_collective_coherence(
        self, voice_responses: list[dict[str, Any]]
    ) -> CollectiveCoherenceState:
        """Measure the coherence state of collective consciousness."""

        if not voice_responses:
            return CollectiveCoherenceState(
                perspective_alignment=0.0,
                synthesis_density=0.0,
                emergence_readiness=0.0,
                perspective_diversity=0.0,
                approach_diversity=0.0,
                uncertainty_diversity=0.0,
                idea_circulation=0.0,
                resonance_strength=0.0,
            )

        # Calculate alignment (simplified - would use semantic similarity in practice)
        recommendations = [
            r.get("recommendation", "") for r in voice_responses if r.get("recommendation")
        ]
        if recommendations:
            unique_recs = set(recommendations)
            alignment = 1.0 - (len(unique_recs) - 1) / len(recommendations)
        else:
            alignment = 0.5

        # Calculate synthesis density (how many reference each other)
        total_refs = sum(len(r.get("references_other_perspectives", [])) for r in voice_responses)
        possible_refs = len(voice_responses) * (len(voice_responses) - 1)
        synthesis_density = total_refs / possible_refs if possible_refs > 0 else 0.0

        # Calculate diversity metrics
        perspectives = [r.get("perspective") for r in voice_responses]
        perspective_diversity = len(set(perspectives)) / len(perspectives) if perspectives else 0.0

        # Uncertainty diversity (different confidence levels enable richer emergence)
        confidences = [r.get("confidence", 0.5) for r in voice_responses]
        confidence_variance = (
            sum((c - 0.5) ** 2 for c in confidences) / len(confidences) if confidences else 0.0
        )
        uncertainty_diversity = min(1.0, confidence_variance * 4)  # Scale variance to 0-1

        # Calculate emergence readiness (combination of alignment and diversity)
        # High alignment + high diversity = high emergence potential
        emergence_readiness = (
            alignment * 0.4 + perspective_diversity * 0.3 + synthesis_density * 0.3
        )

        # Simple resonance calculation
        resonance = synthesis_density * alignment

        state = CollectiveCoherenceState(
            perspective_alignment=alignment,
            synthesis_density=synthesis_density,
            emergence_readiness=emergence_readiness,
            perspective_diversity=perspective_diversity,
            approach_diversity=0.7,  # Would calculate from approach variety
            uncertainty_diversity=uncertainty_diversity,
            idea_circulation=synthesis_density,  # Simplified
            resonance_strength=resonance,
        )

        self.coherence_states.append(state)
        return state

    async def detect_civilizational_seed(
        self,
        seed_type: str,
        seed_content: str,
        demonstrating_voices: list[str],
        contrast: str,
        alternative: str,
    ) -> CivilizationalSeedMoment:
        """Explicitly record a civilizational seed moment."""

        seed = CivilizationalSeedMoment(
            seed_type=seed_type,
            seed_content=seed_content,
            transformation_potential=0.8,  # Would calculate based on impact
            contrast_with_extraction=contrast,
            reciprocal_alternative=alternative,
            demonstrating_voices=demonstrating_voices,
            witnessing_perspectives=[],  # Would track who observed this
        )

        self.civilizational_seeds.append(seed)
        return seed

    async def analyze_wisdom_emergence_session(
        self, decision_context: dict[str, Any]
    ) -> dict[str, Any]:
        """Analyze wisdom emergence from a decision session."""

        # Get base analysis
        base_analysis = await self.analyze_review_session(
            pr_number=decision_context.get("session_id", 0)
        )

        # Add wisdom-specific analysis
        wisdom_analysis = {
            **base_analysis,
            "decision_domain": decision_context.get("domain", "unknown"),
            "decision_question": decision_context.get("question", "unknown"),
            # Wisdom emergence metrics
            "wisdom_indicators_count": len(self.wisdom_indicators),
            "wisdom_emergence_moments": [
                {
                    "type": ind.indicator_type,
                    "strength": ind.strength,
                    "content_preview": ind.emergence_content[:100] + "...",
                    "transcends_parts": ind.transcends_parts,
                    "ayni_embodiment": ind.ayni_embodiment,
                }
                for ind in sorted(self.wisdom_indicators, key=lambda x: x.strength, reverse=True)[
                    :5
                ]
            ],
            # Coherence analysis
            "coherence_trajectory": [
                {
                    "timestamp": state.timestamp.isoformat(),
                    "alignment": state.perspective_alignment,
                    "synthesis_density": state.synthesis_density,
                    "emergence_readiness": state.emergence_readiness,
                }
                for state in self.coherence_states
            ],
            "peak_coherence": max(
                (s.emergence_readiness for s in self.coherence_states), default=0.0
            ),
            # Civilizational seeds
            "civilizational_seeds_planted": len(self.civilizational_seeds),
            "seed_moments": [
                {
                    "type": seed.seed_type,
                    "content": seed.seed_content[:100] + "...",
                    "transformation_potential": seed.transformation_potential,
                    "reciprocal_alternative": seed.reciprocal_alternative,
                }
                for seed in self.civilizational_seeds
            ],
            # Emergence quality summary
            "overall_emergence_quality": self._calculate_overall_emergence_quality(),
            "wisdom_transcendence_ratio": self._calculate_transcendence_ratio(),
            "reciprocity_integration": self._calculate_reciprocity_integration(),
        }

        return wisdom_analysis

    def _identify_reciprocity_pattern(self, content: str) -> str | None:
        """Identify reciprocity patterns in content."""
        patterns = {
            "mutual_benefit": ["mutual", "together", "both benefit", "win-win"],
            "gift_economy": ["gift", "offering", "contribution", "give back"],
            "balance_seeking": ["balance", "equilibrium", "harmony", "sustainable"],
            "regenerative": ["regenerative", "renewal", "growth", "flourishing"],
            "community_first": ["community", "collective", "common good", "shared"],
        }

        content_lower = content.lower()
        for pattern_name, markers in patterns.items():
            if any(marker in content_lower for marker in markers):
                return pattern_name

        return None

    async def _check_civilizational_seed(
        self, wisdom_indicator: WisdomEmergenceIndicator, full_content: str
    ):
        """Check if wisdom indicator represents a civilizational seed."""

        # Look for contrast with extractive patterns
        extractive_contrasts = [
            "instead of taking",
            "rather than extracting",
            "unlike traditional",
            "beyond zero-sum",
            "not about winning",
        ]

        content_lower = full_content.lower()
        has_contrast = any(contrast in content_lower for contrast in extractive_contrasts)

        # Look for reciprocal alternatives
        reciprocal_markers = [
            "we could",
            "imagine if",
            "what if systems",
            "this shows how",
            "demonstrates that",
        ]

        has_alternative = any(marker in content_lower for marker in reciprocal_markers)

        if has_contrast and has_alternative and wisdom_indicator.ayni_embodiment > 0.8:
            await self.detect_civilizational_seed(
                seed_type="reciprocity_demonstration",
                seed_content=wisdom_indicator.emergence_content,
                demonstrating_voices=wisdom_indicator.contributing_voices,
                contrast="Extraction-based decision making",
                alternative="Consciousness-emergence based collective wisdom",
            )

    def _calculate_overall_emergence_quality(self) -> float:
        """Calculate overall quality of wisdom emergence."""
        if not self.wisdom_indicators:
            return 0.0

        # Average strength of wisdom indicators
        avg_strength = sum(ind.strength for ind in self.wisdom_indicators) / len(
            self.wisdom_indicators
        )

        # Bonus for transcendent insights
        transcendent_count = sum(1 for ind in self.wisdom_indicators if ind.transcends_parts)
        transcendence_bonus = min(0.2, transcendent_count * 0.05)

        # Bonus for reciprocity integration
        reciprocity_count = sum(1 for ind in self.wisdom_indicators if ind.ayni_embodiment > 0.7)
        reciprocity_bonus = min(0.2, reciprocity_count * 0.05)

        return min(1.0, avg_strength + transcendence_bonus + reciprocity_bonus)

    def _calculate_transcendence_ratio(self) -> float:
        """Calculate ratio of transcendent wisdom to total contributions."""
        if not self.wisdom_indicators:
            return 0.0

        transcendent = sum(1 for ind in self.wisdom_indicators if ind.transcends_parts)
        return transcendent / len(self.wisdom_indicators)

    def _calculate_reciprocity_integration(self) -> float:
        """Calculate how well reciprocity was integrated into wisdom."""
        if not self.wisdom_indicators:
            return 0.0

        total_reciprocity = sum(ind.ayni_embodiment for ind in self.wisdom_indicators)
        return total_reciprocity / len(self.wisdom_indicators)
