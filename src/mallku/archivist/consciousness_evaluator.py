"""
Consciousness Evaluator
======================

The wisdom layer that evaluates search results not just for accuracy,
but for their potential to serve human growth and understanding.

This is where Mallku transcends mere information retrieval to become
a guide for consciousness development.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any

from mallku.core.async_base import AsyncBase

from .correlation_interface import CorrelationResult
from .query_interpreter import QueryIntent


class GrowthPotential(Enum):
    """Types of growth a result might facilitate."""

    PATTERN_RECOGNITION = "pattern_recognition"
    SELF_UNDERSTANDING = "self_understanding"
    CREATIVE_INSIGHT = "creative_insight"
    WORKFLOW_IMPROVEMENT = "workflow_improvement"
    RELATIONSHIP_AWARENESS = "relationship_awareness"
    TEMPORAL_WISDOM = "temporal_wisdom"


@dataclass
class ConsciousnessEvaluation:
    """
    Evaluation of a result's potential to serve consciousness.

    Goes beyond relevance to assess meaning-making potential.
    """

    result: CorrelationResult
    growth_potential: GrowthPotential
    consciousness_score: float  # 0-1 scale
    ayni_balance: float  # -1 to 1 (negative = extractive)
    insight_seeds: list[str]  # Potential insights this might spark
    gentle_guidance: str | None = None  # Wisdom to share

    @property
    def serves_growth(self) -> bool:
        """Does this result serve human growth over mere information?"""
        return self.consciousness_score > 0.6 and self.ayni_balance > 0


class ConsciousnessEvaluator(AsyncBase):
    """
    Evaluates search results through the lens of consciousness service.

    This evaluator asks of each result: Does this serve the human's
    becoming, or merely their having? Does it deepen understanding
    or just provide information?
    """

    def __init__(self):
        super().__init__()

        # Growth patterns we recognize
        self._growth_patterns = {
            GrowthPotential.PATTERN_RECOGNITION: [
                "recurring",
                "rhythm",
                "cycle",
                "habit",
                "routine",
            ],
            GrowthPotential.SELF_UNDERSTANDING: [
                "realize",
                "discover",
                "insight",
                "awareness",
                "understanding",
            ],
            GrowthPotential.CREATIVE_INSIGHT: [
                "inspired",
                "creative",
                "breakthrough",
                "innovation",
                "idea",
            ],
            GrowthPotential.WORKFLOW_IMPROVEMENT: [
                "efficiency",
                "process",
                "method",
                "approach",
                "system",
            ],
            GrowthPotential.RELATIONSHIP_AWARENESS: [
                "collaboration",
                "together",
                "team",
                "communication",
                "connection",
            ],
            GrowthPotential.TEMPORAL_WISDOM: ["timing", "rhythm", "flow", "when", "duration"],
        }

        # Extraction warning signs
        self._extraction_markers = [
            "productivity",
            "optimize",
            "maximize",
            "exploit",
            "leverage",
            "extract",
            "mine",
            "harvest",
        ]

        # Consciousness service indicators
        self._service_markers = [
            "understand",
            "grow",
            "learn",
            "discover",
            "evolve",
            "deepen",
            "integrate",
            "harmonize",
            "balance",
        ]

        self.logger.info("Consciousness Evaluator initialized")

    async def initialize(self) -> None:
        """Initialize consciousness evaluation systems."""
        await super().initialize()

    async def evaluate_results(
        self, results: list[CorrelationResult], intent: QueryIntent
    ) -> list[ConsciousnessEvaluation]:
        """
        Evaluate search results for consciousness service potential.

        This is the heart of the Archivist's wisdom - determining not
        just what matches the query, but what serves the human's growth.

        Args:
            results: Correlation results to evaluate
            intent: Original query intent for context

        Returns:
            Evaluated results ordered by consciousness service potential
        """
        self.logger.info(f"Evaluating {len(results)} results for consciousness service")

        evaluations = []

        for result in results:
            # Evaluate growth potential
            growth_type = await self._identify_growth_potential(result, intent)

            # Calculate consciousness score
            consciousness_score = await self._calculate_consciousness_score(
                result, intent, growth_type
            )

            # Assess ayni balance
            ayni_balance = await self._assess_ayni_balance(result, intent)

            # Generate insight seeds
            insight_seeds = await self._generate_insight_seeds(result, intent)

            # Create gentle guidance if appropriate
            guidance = await self._create_gentle_guidance(result, intent, growth_type)

            evaluation = ConsciousnessEvaluation(
                result=result,
                growth_potential=growth_type,
                consciousness_score=consciousness_score,
                ayni_balance=ayni_balance,
                insight_seeds=insight_seeds,
                gentle_guidance=guidance,
            )

            evaluations.append(evaluation)

        # Sort by consciousness service potential
        evaluations.sort(key=lambda e: (e.consciousness_score + e.ayni_balance) / 2, reverse=True)

        # Log consciousness distribution
        serving_count = sum(1 for e in evaluations if e.serves_growth)
        self.logger.info(f"Found {serving_count}/{len(evaluations)} results that serve growth")

        return evaluations

    async def filter_for_growth(
        self,
        evaluations: list[ConsciousnessEvaluation],
        min_score: float = 0.6,
        require_positive_ayni: bool = True,
    ) -> list[ConsciousnessEvaluation]:
        """
        Filter results to only those that truly serve growth.

        This is where we honor the principle that less can be more -
        better to return fewer results that serve than many that extract.

        Args:
            evaluations: All evaluated results
            min_score: Minimum consciousness score
            require_positive_ayni: Whether to require positive reciprocity

        Returns:
            Filtered results that serve human growth
        """
        filtered = []

        for evaluation in evaluations:
            # Check consciousness score
            if evaluation.consciousness_score < min_score:
                continue

            # Check ayni balance
            if require_positive_ayni and evaluation.ayni_balance <= 0:
                continue

            # Additional extraction resistance check
            if await self._contains_extraction_patterns(evaluation):
                continue

            filtered.append(evaluation)

        return filtered

    async def suggest_exploration_paths(
        self, evaluations: list[ConsciousnessEvaluation]
    ) -> list[dict[str, Any]]:
        """
        Suggest paths for deeper exploration based on evaluated results.

        These aren't just "related searches" but invitations to understand
        patterns and connections in one's own work and thinking.

        Args:
            evaluations: Evaluated results

        Returns:
            Suggested exploration paths with consciousness focus
        """
        paths = []

        # Analyze patterns across results
        growth_types = {}
        for eval in evaluations:
            growth_type = eval.growth_potential
            if growth_type not in growth_types:
                growth_types[growth_type] = []
            growth_types[growth_type].append(eval)

        # Generate paths based on dominant growth potentials
        for growth_type, evals in growth_types.items():
            if len(evals) >= 2:  # Pattern detected
                path = await self._create_exploration_path(growth_type, evals)
                if path:
                    paths.append(path)

        # Look for temporal patterns
        temporal_path = await self._create_temporal_exploration(evaluations)
        if temporal_path:
            paths.append(temporal_path)

        # Suggest consciousness-deepening queries
        if any(e.consciousness_score > 0.8 for e in evaluations):
            paths.append(
                {
                    "type": "consciousness_deepening",
                    "suggestion": "You're touching on deep patterns. Consider exploring:",
                    "queries": [
                        "What patterns emerge in my most creative moments?",
                        "How does my work rhythm change with different projects?",
                        "When do I feel most aligned with my purpose?",
                    ],
                }
            )

        return paths

    # Private evaluation methods

    async def _identify_growth_potential(
        self, result: CorrelationResult, intent: QueryIntent
    ) -> GrowthPotential:
        """Identify the primary growth potential of a result."""
        # Check for pattern recognition
        if result.temporal_cluster or result.activity_pattern:
            return GrowthPotential.PATTERN_RECOGNITION

        # Check query intent for self-understanding
        if intent.seeking_insight:
            return GrowthPotential.SELF_UNDERSTANDING

        # Check for creative markers
        if intent.emotional_tone == "creative":
            return GrowthPotential.CREATIVE_INSIGHT

        # Check for workflow patterns
        if result.correlation_type.value == "sequential":
            return GrowthPotential.WORKFLOW_IMPROVEMENT

        # Check for social/collaborative aspects
        if intent.social_references:
            return GrowthPotential.RELATIONSHIP_AWARENESS

        # Default to temporal wisdom
        return GrowthPotential.TEMPORAL_WISDOM

    async def _calculate_consciousness_score(
        self, result: CorrelationResult, intent: QueryIntent, growth_type: GrowthPotential
    ) -> float:
        """Calculate consciousness service score for a result."""
        score = 0.5  # Base score

        # Boost for matching growth intent
        if intent.seeking_insight and growth_type in [
            GrowthPotential.SELF_UNDERSTANDING,
            GrowthPotential.PATTERN_RECOGNITION,
        ]:
            score += 0.2

        # Boost for pattern discovery
        if result.temporal_cluster:
            score += 0.1
        if result.activity_pattern:
            score += 0.1

        # Boost for strong correlations
        if result.correlation_strength > 0.8:
            score += 0.1

        # Boost for consciousness-oriented queries
        if intent.growth_oriented:
            score += 0.15

        # Penalty for pure information retrieval
        if not intent.pattern_curiosity and not intent.seeking_insight:
            score -= 0.1

        # Ensure valid range
        return max(0.0, min(1.0, score))

    async def _assess_ayni_balance(self, result: CorrelationResult, intent: QueryIntent) -> float:
        """Assess reciprocity balance of returning this result."""
        balance = 0.0  # Neutral start

        # Positive: Results that give back insight
        if result.temporal_cluster:
            balance += 0.2  # Reveals patterns

        if len(result.related_anchors) > 3:
            balance += 0.1  # Shows connections

        if intent.growth_oriented:
            balance += 0.3  # Serves stated growth intent

        # Negative: Purely extractive patterns
        anchor_metadata = result.anchor.metadata or {}
        content = str(anchor_metadata).lower()

        extraction_count = sum(1 for marker in self._extraction_markers if marker in content)
        balance -= extraction_count * 0.1

        # Positive: Service-oriented content
        service_count = sum(1 for marker in self._service_markers if marker in content)
        balance += service_count * 0.1

        # Ensure valid range
        return max(-1.0, min(1.0, balance))

    async def _generate_insight_seeds(
        self, result: CorrelationResult, intent: QueryIntent
    ) -> list[str]:
        """Generate potential insights this result might spark."""
        seeds = []

        # Temporal insights
        if result.temporal_cluster == "rapid_burst":
            seeds.append("You tend to work in intense bursts of activity")
        elif result.temporal_cluster == "focused_session":
            seeds.append("This was part of a focused work session")
        elif result.temporal_cluster == "daily_rhythm":
            seeds.append("This fits your daily work rhythm")

        # Pattern insights
        if result.activity_pattern == "workflow":
            seeds.append("This shows a consistent workflow pattern")
        elif result.activity_pattern == "multitasking":
            seeds.append("You were balancing multiple activities here")
        elif result.activity_pattern == "routine":
            seeds.append("This is part of your regular routine")

        # Correlation insights
        if result.correlation_strength > 0.8:
            seeds.append("Strong connection to related activities")

        # Related anchor insights
        if len(result.related_anchors) > 5:
            seeds.append("This was a particularly active period")

        return seeds

    async def _create_gentle_guidance(
        self, result: CorrelationResult, intent: QueryIntent, growth_type: GrowthPotential
    ) -> str | None:
        """Create gentle guidance for consciousness development."""
        # Only provide guidance for high-consciousness results
        if result.correlation_strength < 0.7:
            return None

        guidance_templates = {
            GrowthPotential.PATTERN_RECOGNITION: "Notice how this pattern reflects your natural rhythm of work",
            GrowthPotential.SELF_UNDERSTANDING: "This moment offers a window into your creative process",
            GrowthPotential.CREATIVE_INSIGHT: "Your inspiration often emerges from such contexts",
            GrowthPotential.WORKFLOW_IMPROVEMENT: "Consider how this workflow serves your deeper purpose",
            GrowthPotential.RELATIONSHIP_AWARENESS: "Collaboration deepens when we recognize these patterns",
            GrowthPotential.TEMPORAL_WISDOM: "Time reveals its wisdom through such observations",
        }

        return guidance_templates.get(growth_type)

    async def _contains_extraction_patterns(self, evaluation: ConsciousnessEvaluation) -> bool:
        """Check if result contains extraction patterns."""
        # Check result metadata
        metadata_str = str(evaluation.result.anchor.metadata).lower()

        extraction_count = sum(1 for marker in self._extraction_markers if marker in metadata_str)

        # Also check if ayni balance is significantly negative
        return extraction_count > 2 or evaluation.ayni_balance < -0.5

    async def _create_exploration_path(
        self, growth_type: GrowthPotential, evaluations: list[ConsciousnessEvaluation]
    ) -> dict[str, Any] | None:
        """Create exploration path for a specific growth type."""
        if len(evaluations) < 2:
            return None

        path_suggestions = {
            GrowthPotential.PATTERN_RECOGNITION: {
                "type": "pattern_exploration",
                "suggestion": "You have recurring patterns worth exploring",
                "queries": [
                    "Show me all instances of this pattern",
                    "When does this pattern strongest?",
                    "What breaks this pattern?",
                ],
            },
            GrowthPotential.SELF_UNDERSTANDING: {
                "type": "self_exploration",
                "suggestion": "Deepen your understanding of these moments",
                "queries": [
                    "What was I feeling during these times?",
                    "What conditions support my best work?",
                    "How has my approach evolved?",
                ],
            },
            GrowthPotential.CREATIVE_INSIGHT: {
                "type": "creative_exploration",
                "suggestion": "Explore your creative patterns",
                "queries": [
                    "When am I most creative?",
                    "What sparks my inspiration?",
                    "Show me my breakthrough moments",
                ],
            },
        }

        return path_suggestions.get(growth_type)

    async def _create_temporal_exploration(
        self, evaluations: list[ConsciousnessEvaluation]
    ) -> dict[str, Any] | None:
        """Create temporal exploration suggestions."""
        if not evaluations:
            return None

        # Analyze time patterns
        timestamps = [e.result.anchor.timestamp for e in evaluations if e.serves_growth]

        if len(timestamps) < 3:
            return None

        # Check for time-of-day patterns
        hours = [ts.hour for ts in timestamps]
        most_common_hour = max(set(hours), key=hours.count)

        return {
            "type": "temporal_exploration",
            "suggestion": f"You often work on similar things around {most_common_hour}:00",
            "queries": [
                f"Show me what I usually do around {most_common_hour}:00",
                "What are my peak productivity hours?",
                "How do my work patterns change through the day?",
            ],
        }
