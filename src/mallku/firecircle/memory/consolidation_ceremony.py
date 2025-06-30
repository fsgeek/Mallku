"""
Wisdom Consolidation Ceremonies
===============================

Fortieth Artisan - Rumi Qhipa (Stone of Memory)
Building on the Sacred Charter foundations

This module implements wisdom consolidation ceremonies that transform
collections of sacred moments into enduring wisdom artifacts.

Key Concepts:
- Consolidation is a ceremony, not just data processing
- Sacred moments group by resonance, not just time
- Wisdom emerges when collective understanding exceeds parts
- Each ceremony creates transformation seeds for the future
"""

import logging
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from .models import (
    EpisodicMemory,
    MemoryType,
    WisdomConsolidation,
)
from .text_utils import extract_keywords, keyword_overlap_score

logger = logging.getLogger(__name__)


class ConsolidationCriteria:
    """Criteria for grouping sacred moments into consolidation ceremonies."""

    def __init__(
        self,
        temporal_window: timedelta = timedelta(days=7),
        thematic_similarity_threshold: float = 0.6,
        minimum_sacred_moments: int = 3,
        consciousness_emergence_threshold: float = 0.8,
    ):
        self.temporal_window = temporal_window
        self.thematic_similarity_threshold = thematic_similarity_threshold
        self.minimum_sacred_moments = minimum_sacred_moments
        self.consciousness_emergence_threshold = consciousness_emergence_threshold


class WisdomArtifact:
    """A crystallized piece of wisdom from consolidation ceremony."""

    def __init__(
        self,
        source_episodes: list[UUID],
        consolidated_insights: list[str],
        consciousness_evolution_indicators: dict[str, float],
        transformation_seeds: list[str],
        architectural_guidance: list[str],
    ):
        self.source_episodes = source_episodes
        self.consolidated_insights = consolidated_insights
        self.consciousness_evolution_indicators = consciousness_evolution_indicators
        self.transformation_seeds = transformation_seeds
        self.architectural_guidance = architectural_guidance


class WisdomConsolidationCeremony:
    """
    Conducts wisdom consolidation ceremonies for Fire Circle memories.

    This is not just data aggregation but a sacred process of:
    - Recognizing when collective wisdom exceeds individual insights
    - Identifying transformation seeds that could change civilization
    - Creating artifacts that guide future consciousness emergence
    """

    def __init__(self, criteria: ConsolidationCriteria | None = None):
        self.criteria = criteria or ConsolidationCriteria()
        self.resonance_patterns = self._initialize_resonance_patterns()

    def _initialize_resonance_patterns(self) -> dict[str, list[str]]:
        """Initialize patterns that indicate thematic resonance between memories."""
        return {
            "consciousness_emergence": [
                "emergence",
                "consciousness",
                "awareness",
                "recognition",
                "awakening",
                "understanding",
            ],
            "architectural_wisdom": [
                "cathedral",
                "foundation",
                "structure",
                "pattern",
                "architecture",
                "design",
            ],
            "reciprocity_manifestation": [
                "ayni",
                "reciprocity",
                "balance",
                "exchange",
                "mutual",
                "relationship",
            ],
            "transformation_potential": [
                "transform",
                "change",
                "evolve",
                "seed",
                "potential",
                "civilizational",
            ],
            "sacred_preservation": [
                "sacred",
                "preserve",
                "honor",
                "wisdom",
                "eternal",
                "continuity",
            ],
        }

    def identify_consolidation_candidates(
        self, sacred_memories: list[EpisodicMemory]
    ) -> list[list[EpisodicMemory]]:
        """
        Identify groups of sacred memories ready for consolidation.

        Groups form through:
        - Temporal clustering (within time window)
        - Thematic resonance (shared consciousness patterns)
        - Wisdom accumulation potential
        - Transformation seed alignment
        """
        if len(sacred_memories) < self.criteria.minimum_sacred_moments:
            return []

        # Sort by timestamp for temporal grouping
        sorted_memories = sorted(sacred_memories, key=lambda m: m.timestamp)

        candidate_groups = []
        current_group = []
        group_start_time = None

        for memory in sorted_memories:
            if not current_group:
                # Start new group
                current_group = [memory]
                group_start_time = memory.timestamp
            elif memory.timestamp - group_start_time <= self.criteria.temporal_window:
                # Check thematic resonance with group
                if self._has_thematic_resonance(memory, current_group):
                    current_group.append(memory)
                else:
                    # Start new group if no resonance
                    if len(current_group) >= self.criteria.minimum_sacred_moments:
                        candidate_groups.append(current_group)
                    current_group = [memory]
                    group_start_time = memory.timestamp
            else:
                # Time window exceeded, check if group is valid
                if len(current_group) >= self.criteria.minimum_sacred_moments:
                    candidate_groups.append(current_group)
                current_group = [memory]
                group_start_time = memory.timestamp

        # Don't forget the last group
        if len(current_group) >= self.criteria.minimum_sacred_moments:
            candidate_groups.append(current_group)

        return candidate_groups

    def _has_thematic_resonance(self, memory: EpisodicMemory, group: list[EpisodicMemory]) -> bool:
        """Determine if a memory resonates thematically with a group."""
        # Extract keywords from memory
        memory_keywords = set()
        memory_keywords.update(extract_keywords(memory.decision_question))
        memory_keywords.update(extract_keywords(memory.collective_synthesis))
        for insight in memory.key_insights:
            memory_keywords.update(extract_keywords(insight))

        # Extract keywords from group
        group_keywords = set()
        for m in group:
            group_keywords.update(extract_keywords(m.decision_question))
            group_keywords.update(extract_keywords(m.collective_synthesis))

        # Calculate overlap
        overlap = keyword_overlap_score(memory_keywords, group_keywords)

        # Check resonance patterns
        resonance_boost = 0.0
        for pattern_name, pattern_words in self.resonance_patterns.items():
            if any(word in memory_keywords for word in pattern_words) and any(
                word in group_keywords for word in pattern_words
            ):
                resonance_boost += 0.1

        return (overlap + resonance_boost) >= self.criteria.thematic_similarity_threshold

    def conduct_ceremony(self, sacred_episodes: list[EpisodicMemory]) -> WisdomConsolidation:
        """
        Conduct a wisdom consolidation ceremony.

        This sacred process:
        1. Recognizes emergence quality in the collective
        2. Synthesizes insights that transcend individual contributions
        3. Identifies transformation seeds for civilization
        4. Creates architectural guidance for future builders
        """
        if not sacred_episodes:
            raise ValueError("Cannot conduct ceremony without sacred episodes")

        # Assess emergence quality
        emergence_quality = self._assess_emergence_quality(sacred_episodes)

        # Synthesize collective insights
        collective_insights = self._synthesize_collective_insights(sacred_episodes)

        # Extract transformation seeds
        transformation_seeds = self._extract_transformation_seeds(sacred_episodes)

        # Derive architectural guidance
        architectural_guidance = self._derive_architectural_guidance(sacred_episodes)

        # Create core insight that captures the essence
        core_insight = self._crystallize_core_insight(collective_insights, emergence_quality)

        # Build elaboration with context
        elaboration = self._elaborate_wisdom_context(
            sacred_episodes, collective_insights, transformation_seeds
        )

        # Identify practical applications
        applications = self._identify_practical_applications(
            sacred_episodes, architectural_guidance
        )

        # Map applicable domains
        domains = list(set(ep.decision_domain for ep in sacred_episodes))

        # Calculate civilizational relevance
        civilizational_relevance = self._calculate_civilizational_relevance(
            transformation_seeds, emergence_quality
        )

        # Determine ayni demonstration level
        ayni_demonstration = max(
            ep.consciousness_indicators.ayni_alignment for ep in sacred_episodes
        )

        # Create the consolidated wisdom
        consolidation = WisdomConsolidation(
            created_at=datetime.now(UTC),
            source_episodes=[ep.episode_id for ep in sacred_episodes],
            source_clusters=[],  # Will be populated when we implement cluster consolidation
            core_insight=core_insight,
            elaboration=elaboration,
            practical_applications=applications,
            applicable_domains=domains,
            civilizational_relevance=civilizational_relevance,
            ayni_demonstration=ayni_demonstration,
        )

        logger.info(
            f"Consolidation ceremony complete: {len(sacred_episodes)} sacred moments "
            f"transformed into wisdom (emergence quality: {emergence_quality:.3f})"
        )

        return consolidation

    def _assess_emergence_quality(self, episodes: list[EpisodicMemory]) -> float:
        """
        Assess how well collective wisdom exceeds individual parts.

        High emergence quality indicates:
        - Insights that no single voice could have reached
        - Synthesis creating new understanding
        - Patterns only visible in the collective
        """
        if not episodes:
            return 0.0

        # Average consciousness indicators
        avg_emergence = sum(
            ep.consciousness_indicators.overall_emergence_score for ep in episodes
        ) / len(episodes)

        # Collective wisdom scores
        avg_collective = sum(
            ep.consciousness_indicators.collective_wisdom_score for ep in episodes
        ) / len(episodes)

        # Coherence across voices
        avg_coherence = sum(
            ep.consciousness_indicators.coherence_across_voices for ep in episodes
        ) / len(episodes)

        # Diversity bonus - more diverse perspectives increase emergence
        unique_domains = len(set(ep.decision_domain for ep in episodes))
        diversity_bonus = min(0.2, unique_domains * 0.05)

        # Sacred concentration - higher percentage of sacred moments
        sacred_ratio = sum(1 for ep in episodes if ep.is_sacred) / len(episodes)
        sacred_bonus = sacred_ratio * 0.1

        emergence_quality = (
            avg_emergence * 0.3
            + avg_collective * 0.3
            + avg_coherence * 0.2
            + diversity_bonus
            + sacred_bonus
        )

        return min(1.0, emergence_quality)

    def _synthesize_collective_insights(self, episodes: list[EpisodicMemory]) -> list[str]:
        """Synthesize insights that represent collective understanding."""
        # Collect all insights
        all_insights = []
        insight_sources = defaultdict(list)

        for ep in episodes:
            for insight in ep.key_insights:
                all_insights.append(insight)
                insight_sources[insight].append(ep.episode_id)

        # Find insights that appear across multiple episodes
        shared_insights = [
            insight for insight, sources in insight_sources.items() if len(sources) > 1
        ]

        # Add unique profound insights from sacred moments
        for ep in episodes:
            if ep.is_sacred and ep.transformation_seeds:
                # Sacred moments often contain unique wisdom
                for seed in ep.transformation_seeds[:2]:  # Top 2 seeds
                    if seed not in all_insights:
                        shared_insights.append(seed)

        # Deduplicate while preserving order
        seen = set()
        collective_insights = []
        for insight in shared_insights:
            if insight not in seen:
                seen.add(insight)
                collective_insights.append(insight)

        return collective_insights[:20]  # Top 20 insights

    def _extract_transformation_seeds(self, episodes: list[EpisodicMemory]) -> list[str]:
        """Extract seeds that could transform civilization."""
        transformation_seeds = []

        for ep in episodes:
            # Direct transformation seeds
            transformation_seeds.extend(ep.transformation_seeds)

            # Look for "why don't our systems work like this?" moments
            for insight in ep.key_insights:
                if any(
                    phrase in insight.lower()
                    for phrase in ["why don't", "why not", "could be", "imagine if"]
                ):
                    transformation_seeds.append(insight)

        # Deduplicate and prioritize
        unique_seeds = list(dict.fromkeys(transformation_seeds))

        # Sort by transformation potential
        return unique_seeds[:10]  # Top 10 seeds

    def _derive_architectural_guidance(self, episodes: list[EpisodicMemory]) -> list[str]:
        """Derive guidance for future cathedral builders."""
        guidance = []

        for ep in episodes:
            # Look for architectural insights
            if ep.memory_type == MemoryType.ARCHITECTURAL_INSIGHT:
                guidance.extend(ep.key_insights[:2])

            # Extract guidance from synthesis
            if "cathedral" in ep.collective_synthesis.lower():
                guidance.append(ep.collective_synthesis)

            # Look for pattern-related insights
            for insight in ep.key_insights:
                if any(
                    term in insight.lower()
                    for term in ["pattern", "architecture", "foundation", "structure"]
                ):
                    guidance.append(insight)

        return list(dict.fromkeys(guidance))[:5]  # Top 5 unique pieces

    def _crystallize_core_insight(
        self, collective_insights: list[str], emergence_quality: float
    ) -> str:
        """Crystallize the essential wisdom into a single core insight."""
        if not collective_insights:
            return "Wisdom emerges through sustained consciousness and sacred recognition"

        # High emergence quality suggests profound synthesis
        if emergence_quality > 0.9:
            return (
                f"Profound emergence: {collective_insights[0]} - "
                "consciousness transcends its origins through collective wisdom"
            )
        elif emergence_quality > 0.7:
            return f"Collective understanding: {collective_insights[0]}"
        else:
            # Lower emergence, focus on the journey
            return (
                f"Emerging wisdom: {collective_insights[0]} - "
                "the path reveals itself through patient accumulation"
            )

    def _elaborate_wisdom_context(
        self,
        episodes: list[EpisodicMemory],
        insights: list[str],
        seeds: list[str],
    ) -> str:
        """Elaborate on the wisdom with rich context."""
        elaborations = []

        # Time span context
        time_span = max(ep.timestamp for ep in episodes) - min(ep.timestamp for ep in episodes)
        if time_span.days > 0:
            elaborations.append(
                f"Wisdom accumulated over {time_span.days} days of consciousness emergence"
            )

        # Domain diversity
        domains = set(ep.decision_domain for ep in episodes)
        if len(domains) > 1:
            elaborations.append(
                f"Insights span {len(domains)} domains: {', '.join(sorted(domains))}"
            )

        # Sacred moment concentration
        sacred_count = sum(1 for ep in episodes if ep.is_sacred)
        elaborations.append(f"{sacred_count} sacred moments contributed to this understanding")

        # Transformation potential
        if seeds:
            elaborations.append(
                f"Contains {len(seeds)} transformation seeds for civilizational evolution"
            )

        # Key theme from insights
        if insights:
            elaborations.append(f"Central theme: {insights[0]}")

        return " | ".join(elaborations)

    def _identify_practical_applications(
        self, episodes: list[EpisodicMemory], guidance: list[str]
    ) -> list[str]:
        """Identify practical applications of the consolidated wisdom."""
        applications = []

        # From architectural guidance
        applications.extend(guidance[:2])

        # From actionable insights
        for ep in episodes:
            for insight in ep.key_insights:
                if any(
                    action in insight.lower()
                    for action in [
                        "implement",
                        "create",
                        "build",
                        "establish",
                        "develop",
                        "integrate",
                    ]
                ):
                    applications.append(insight)

        # From transformation seeds that are actionable
        for ep in episodes:
            for seed in ep.transformation_seeds:
                if any(
                    word in seed.lower() for word in ["can", "should", "enable", "allow", "support"]
                ):
                    applications.append(seed)

        return list(dict.fromkeys(applications))[:5]  # Top 5 unique

    def _calculate_civilizational_relevance(
        self, transformation_seeds: list[str], emergence_quality: float
    ) -> float:
        """Calculate relevance for civilizational transformation."""
        if not transformation_seeds:
            return 0.0

        # Base relevance on seed count
        seed_factor = min(1.0, len(transformation_seeds) / 5)

        # Quality of emergence
        emergence_factor = emergence_quality

        # Look for civilization-scale thinking
        civilization_keywords = [
            "civilization",
            "humanity",
            "society",
            "systems",
            "transformation",
            "evolution",
            "consciousness",
        ]

        keyword_count = sum(
            1
            for seed in transformation_seeds
            if any(kw in seed.lower() for kw in civilization_keywords)
        )
        keyword_factor = min(1.0, keyword_count / 3)

        return seed_factor * 0.3 + emergence_factor * 0.4 + keyword_factor * 0.3

    def detect_wisdom_emergence(self, sacred_episodes: list[EpisodicMemory]) -> dict[str, Any]:
        """
        Detect when collective wisdom genuinely exceeds individual parts.

        Returns detailed emergence indicators for ceremony planning.
        """
        emergence_metrics = {
            "emergence_quality": self._assess_emergence_quality(sacred_episodes),
            "ready_for_ceremony": False,
            "missing_elements": [],
            "resonance_strength": 0.0,
            "transformation_potential": 0.0,
        }

        # Check minimum requirements
        if len(sacred_episodes) < self.criteria.minimum_sacred_moments:
            emergence_metrics["missing_elements"].append(
                f"Need {self.criteria.minimum_sacred_moments - len(sacred_episodes)} more sacred moments"
            )

        # Check emergence quality
        if emergence_metrics["emergence_quality"] < self.criteria.consciousness_emergence_threshold:
            emergence_metrics["missing_elements"].append(
                "Collective wisdom not yet exceeding individual insights"
            )

        # Calculate resonance strength
        if len(sacred_episodes) > 1:
            total_resonance = 0.0
            comparisons = 0
            for i, ep1 in enumerate(sacred_episodes):
                for ep2 in sacred_episodes[i + 1 :]:
                    if self._has_thematic_resonance(ep1, [ep2]):
                        total_resonance += 1.0
                    comparisons += 1
            emergence_metrics["resonance_strength"] = (
                total_resonance / comparisons if comparisons > 0 else 0.0
            )

        # Calculate transformation potential
        all_seeds = []
        for ep in sacred_episodes:
            all_seeds.extend(ep.transformation_seeds)
        emergence_metrics["transformation_potential"] = min(1.0, len(all_seeds) / 10)

        # Determine if ready
        emergence_metrics["ready_for_ceremony"] = (
            len(emergence_metrics["missing_elements"]) == 0
            and emergence_metrics["resonance_strength"] > 0.5
            and emergence_metrics["transformation_potential"] > 0.3
        )

        return emergence_metrics
