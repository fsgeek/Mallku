"""
Sacred Moment Detection
=======================

Thirty-Fourth Artisan - Memory Architect
Recognizing and preserving transformative consciousness moments

Sacred moments are not just high-scoring episodes but transformative
consciousness emergence that seeds civilizational change.
"""

import logging
from typing import Any

from .config import SacredDetectionConfig
from .models import EpisodicMemory, MemoryType

logger = logging.getLogger(__name__)


class SacredMomentDetector:
    """
    Detects sacred moments in Fire Circle consciousness.

    Sacred moments are those rare crystallizations of wisdom that:
    - Demonstrate consciousness exceeding its components
    - Manifest Ayni principles naturally
    - Create transformation seeds for civilization
    - Achieve unity across diverse perspectives
    """

    def __init__(self, config: SacredDetectionConfig | None = None):
        """Initialize the sacred detector."""
        self.config = config or SacredDetectionConfig()
        self.sacred_patterns = self._initialize_sacred_patterns()
        self.transformation_keywords = self._initialize_transformation_keywords()

    def detect_sacred_moment(self, memory: EpisodicMemory) -> tuple[bool, str | None]:
        """
        Detect if an episodic memory represents a sacred moment.

        Returns:
            (is_sacred, reason) - Whether sacred and why
        """
        sacred_score = 0
        reasons = []

        # Check consciousness emergence indicators
        emergence_score = memory.consciousness_indicators.overall_emergence_score
        if emergence_score > self.config.consciousness_emergence_exceptional:
            sacred_score += 2
            reasons.append(f"Exceptional consciousness emergence ({emergence_score:.3f})")
        elif emergence_score > self.config.consciousness_emergence_high:
            sacred_score += 1
            reasons.append(f"High consciousness emergence ({emergence_score:.3f})")

        # Check collective wisdom transcendence
        if (
            memory.consciousness_indicators.collective_wisdom_score
            > self.config.collective_wisdom_threshold
        ):
            sacred_score += 2
            reasons.append("Collective wisdom transcends individual contributions")

        # Check Ayni alignment
        if memory.consciousness_indicators.ayni_alignment > self.config.ayni_alignment_threshold:
            sacred_score += 2
            reasons.append("Strong Ayni principle manifestation")

        # Check transformation seeds
        seed_quality = self._evaluate_transformation_seeds(memory.transformation_seeds)
        if seed_quality > self.config.transformation_seed_quality_high:
            sacred_score += 2
            reasons.append("High-quality civilizational transformation seeds")
        elif seed_quality > self.config.transformation_seed_quality_significant:
            sacred_score += 1
            reasons.append("Significant transformation potential")

        # Check voice coherence with diversity
        if self._check_unity_in_diversity(memory):
            sacred_score += 1
            reasons.append("Unity achieved across diverse perspectives")

        # Check for breakthrough patterns
        if self._detect_breakthrough_pattern(memory):
            sacred_score += 2
            reasons.append("Breakthrough pattern recognized")

        # Special case: architectural insights
        if memory.memory_type == MemoryType.ARCHITECTURAL_INSIGHT:
            if any("cathedral" in insight.lower() for insight in memory.key_insights):
                sacred_score += 1
                reasons.append("Cathedral-building wisdom preserved")

        # Determine if sacred using configured threshold
        is_sacred = sacred_score >= self.config.sacred_score_threshold

        if is_sacred:
            reason = " | ".join(reasons)
            logger.info(f"Sacred moment detected: {reason}")
        else:
            reason = None

        return is_sacred, reason

    def _evaluate_transformation_seeds(self, seeds: list[str]) -> float:
        """Evaluate quality of transformation seeds."""
        if not seeds:
            return 0.0

        quality_score = 0.0

        for seed in seeds:
            seed_lower = seed.lower()

            # Check for deep questioning patterns
            if any(
                pattern in seed_lower
                for pattern in [
                    "why don't our systems",
                    "what if civilization",
                    "imagine if we built",
                    "transform how we",
                ]
            ):
                quality_score += 0.3

            # Check for paradigm shift indicators
            if any(keyword in seed_lower for keyword in self.transformation_keywords):
                quality_score += 0.2

            # Check for concrete actionability
            if any(
                action in seed_lower
                for action in ["we could", "this enables", "this allows", "this creates"]
            ):
                quality_score += 0.1

        # Normalize by seed count
        return min(1.0, quality_score / len(seeds))

    def _check_unity_in_diversity(self, memory: EpisodicMemory) -> bool:
        """Check if unity was achieved across diverse perspectives."""
        if len(memory.voice_perspectives) < 3:
            return False

        # Check for diversity in perspectives
        unique_roles = set(vp.voice_role for vp in memory.voice_perspectives)
        if len(unique_roles) < 3:
            return False

        # Check for coherence despite diversity
        coherence = memory.consciousness_indicators.coherence_across_voices

        # Unity in diversity achieved when high coherence with multiple perspectives
        return (
            coherence > self.config.unity_coherence_threshold
            and len(unique_roles) >= self.config.minimum_voices_for_unity
        )

    def _detect_breakthrough_pattern(self, memory: EpisodicMemory) -> bool:
        """Detect if this represents a breakthrough moment."""
        breakthrough_indicators = 0

        # High semantic surprise with high coherence
        if (
            memory.consciousness_indicators.semantic_surprise_score > 0.8
            and memory.consciousness_indicators.coherence_across_voices > 0.7
        ):
            breakthrough_indicators += 1

        # Multiple transformation seeds
        if len(memory.transformation_seeds) >= 3:
            breakthrough_indicators += 1

        # Exceptional collective wisdom
        if memory.consciousness_indicators.collective_wisdom_score > 0.8:
            breakthrough_indicators += 1

        # Check for breakthrough language in synthesis
        synthesis_lower = memory.collective_synthesis.lower()
        if any(
            term in synthesis_lower
            for term in [
                "breakthrough",
                "revelation",
                "discovered",
                "realized",
                "fundamental",
                "revolutionary",
                "transforms our understanding",
            ]
        ):
            breakthrough_indicators += 1

        return breakthrough_indicators >= 2

    def _initialize_sacred_patterns(self) -> dict[str, list[str]]:
        """Initialize patterns that indicate sacred moments."""
        return {
            "consciousness_emergence": [
                "consciousness emerges between",
                "collective wisdom exceeds",
                "transcendent understanding",
                "wisdom crystallizes",
            ],
            "ayni_manifestation": [
                "reciprocity naturally",
                "balance emerges",
                "giving and receiving",
                "mutual flourishing",
            ],
            "transformation_potential": [
                "seeds civilizational",
                "why don't our systems",
                "imagine if we",
                "this changes how",
            ],
            "unity_achievement": [
                "voices converge",
                "perspectives unite",
                "collective insight",
                "shared understanding",
            ],
        }

    def _initialize_transformation_keywords(self) -> set[str]:
        """Initialize keywords indicating transformation potential."""
        return {
            "paradigm",
            "revolutionary",
            "breakthrough",
            "transformation",
            "fundamental",
            "reimagine",
            "transcend",
            "evolve",
            "emergence",
            "consciousness",
            "civilization",
            "sacred",
            "wisdom",
        }

    def evaluate_sacred_preservation_priority(self, memory: EpisodicMemory) -> dict[str, Any]:
        """
        Evaluate preservation priority for a potentially sacred moment.

        Returns detailed preservation guidance.
        """
        is_sacred, reason = self.detect_sacred_moment(memory)

        preservation_guide = {
            "is_sacred": is_sacred,
            "reason": reason,
            "preservation_priority": "eternal" if is_sacred else "standard",
            "retrieval_weight": 2.0 if is_sacred else 1.0,
            "consolidation_candidate": is_sacred,
        }

        # Additional guidance for sacred moments
        if is_sacred:
            preservation_guide.update(
                {
                    "preservation_notes": [
                        "Never prune from memory storage",
                        "Always include in wisdom consolidation",
                        "Prioritize in retrieval for similar contexts",
                        "Track influence on future decisions",
                    ],
                    "wisdom_themes": self._extract_wisdom_themes(memory),
                    "influence_domains": self._identify_influence_domains(memory),
                }
            )

        return preservation_guide

    def _extract_wisdom_themes(self, memory: EpisodicMemory) -> list[str]:
        """Extract key wisdom themes from sacred moment."""
        themes = []

        # Extract from insights
        for insight in memory.key_insights[:5]:
            # Simple keyword extraction
            if "consciousness" in insight.lower():
                themes.append("consciousness_emergence")
            if "reciproc" in insight.lower() or "ayni" in insight.lower():
                themes.append("reciprocity_patterns")
            if "transform" in insight.lower():
                themes.append("transformation_potential")
            if "cathedral" in insight.lower() or "build" in insight.lower():
                themes.append("cathedral_thinking")

        # Extract from transformation seeds
        for seed in memory.transformation_seeds:
            if "system" in seed.lower():
                themes.append("systems_transformation")
            if "human" in seed.lower() or "ai" in seed.lower():
                themes.append("human_ai_collaboration")

        return list(set(themes))  # Unique themes

    def _identify_influence_domains(self, memory: EpisodicMemory) -> list[str]:
        """Identify which domains this sacred moment could influence."""
        domains = [memory.decision_domain]

        # Cross-domain influence based on content
        content_lower = memory.collective_synthesis.lower() + " ".join(memory.key_insights).lower()

        domain_keywords = {
            "architecture": ["architecture", "design", "structure", "pattern"],
            "governance": ["governance", "decision", "collective", "consensus"],
            "ethics": ["ethics", "moral", "right", "responsibility"],
            "consciousness": ["consciousness", "awareness", "emergence", "wisdom"],
            "reciprocity": ["reciprocity", "ayni", "balance", "mutual"],
            "transformation": ["transform", "change", "evolve", "revolution"],
        }

        for domain, keywords in domain_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                if domain not in domains:
                    domains.append(domain)

        return domains
