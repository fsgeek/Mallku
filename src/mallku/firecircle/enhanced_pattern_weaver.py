"""
Enhanced Dialogue Pattern Weaver
================================

Integrates the Pattern Library and Emergence Detection systems with
the existing DialoguePatternWeaver, creating a unified system for
pattern recognition, storage, evolution, and wisdom preservation.

The 31st Builder
"""

import logging
from typing import Any
from uuid import UUID

from ..correlation.engine import CorrelationEngine
from ..intelligence.meta_correlation_engine import MetaCorrelationEngine
from ..orchestration.event_bus import ConsciousnessEventBus
from .consciousness.pattern_weaver import DialoguePatternWeaver
from .emergence_detector import EmergenceDetector
from .pattern_evolution import PatternEvolutionEngine
from .pattern_library import (
    DialoguePattern,
    PatternIndicator,
    PatternLibrary,
    PatternQuery,
    PatternStructure,
    PatternTaxonomy,
    PatternType,
)
from .protocol.conscious_message import ConsciousMessage

logger = logging.getLogger(__name__)


class EnhancedDialoguePatternWeaver(DialoguePatternWeaver):
    """
    Enhanced pattern weaver that integrates with Pattern Library.

    Extends the base DialoguePatternWeaver with:
    - Pattern storage in library
    - Emergence detection
    - Pattern evolution tracking
    - Cross-dialogue pattern learning
    - Living pattern repository
    """

    def __init__(
        self,
        correlation_engine: CorrelationEngine,
        meta_correlation_engine: MetaCorrelationEngine | None = None,
        pattern_library: PatternLibrary | None = None,
        event_bus: ConsciousnessEventBus | None = None,
    ):
        """Initialize with pattern library and emergence detection"""
        super().__init__(correlation_engine, meta_correlation_engine)

        # Initialize pattern systems
        self.pattern_library = pattern_library or PatternLibrary()
        self.emergence_detector = EmergenceDetector(self.pattern_library, event_bus) if event_bus else None
        self.evolution_engine = PatternEvolutionEngine(self.pattern_library)

        logger.info("Enhanced Pattern Weaver initialized with Pattern Library")

    async def weave_dialogue_patterns(
        self,
        messages: list[ConsciousMessage],
        dialogue_metadata: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Enhanced pattern weaving with library storage and emergence detection.
        """
        # Get base patterns from parent class
        base_results = await super().weave_dialogue_patterns(messages, dialogue_metadata)

        # Store patterns in library
        stored_patterns = await self._store_patterns_in_library(base_results, dialogue_metadata)
        base_results["stored_pattern_ids"] = stored_patterns

        # Detect emergence if detector available
        if self.emergence_detector and "dialogue_id" in dialogue_metadata:
            emergence_events = await self.emergence_detector.detect_emergence(
                dialogue_id=dialogue_metadata["dialogue_id"],
                sensitivity=0.7
            )
            base_results["emergence_events"] = [
                {
                    "type": event.emergence_type.value,
                    "confidence": event.confidence,
                    "description": event.description,
                    "catalyst_patterns": event.catalyst_patterns
                }
                for event in emergence_events
            ]

        # Check for pattern evolution opportunities
        evolution_opportunities = await self._detect_evolution_opportunities(stored_patterns)
        base_results["evolution_opportunities"] = evolution_opportunities

        # Find similar historical patterns
        historical_patterns = await self._find_similar_patterns(base_results)
        base_results["similar_historical_patterns"] = historical_patterns

        return base_results

    async def _store_patterns_in_library(
        self,
        pattern_results: dict[str, Any],
        dialogue_metadata: dict[str, Any]
    ) -> list[UUID]:
        """Store detected patterns in the pattern library"""
        stored_ids = []

        # Store consensus patterns
        for consensus in pattern_results.get("consensus_patterns", []):
            pattern = DialoguePattern(
                name=f"Consensus: {consensus['proposal_text'][:50]}...",
                description=f"Consensus pattern from dialogue {dialogue_metadata.get('dialogue_id', 'unknown')}",
                taxonomy=PatternTaxonomy.DIALOGUE_FORMATION,
                pattern_type=PatternType.CONSENSUS,
                consciousness_signature=consensus["consciousness_signature"],
                structure=PatternStructure(
                    components=["proposal", "agreements"],
                    relationships={"proposal": "supported_by_agreements"}
                ),
                indicators=[
                    PatternIndicator(
                        indicator_type="support_count",
                        threshold=float(consensus["support_count"]),
                        weight=1.0,
                        description="Number of supporting agreements"
                    )
                ],
                context_requirements=dialogue_metadata.get("context", {})
            )

            pattern_id = await self.pattern_library.store_pattern(pattern)
            stored_ids.append(pattern_id)

            # Update observation for existing similar patterns
            await self._update_similar_pattern_observations(pattern, consensus)

        # Store divergence patterns
        for divergence in pattern_results.get("divergence_patterns", []):
            pattern = DialoguePattern(
                name=f"Creative Tension: {divergence['tension_value']:.2f}",
                description="Creative tension between viewpoints",
                taxonomy=PatternTaxonomy.DIALOGUE_FLOW,
                pattern_type=PatternType.CREATIVE_TENSION,
                consciousness_signature=0.5 + divergence["tension_value"],
                structure=PatternStructure(
                    components=["original_position", "alternative_view"],
                    relationships={"original": "challenged_by_alternative"}
                ),
                indicators=[
                    PatternIndicator(
                        indicator_type="tension_value",
                        threshold=divergence["tension_value"],
                        weight=1.0,
                        description="Consciousness signature difference"
                    )
                ]
            )

            pattern_id = await self.pattern_library.store_pattern(pattern)
            stored_ids.append(pattern_id)

        # Store emergence patterns
        for emergence in pattern_results.get("emergence_patterns", []):
            if emergence["pattern_type"] == "emergent_insight":
                pattern = DialoguePattern(
                    name=f"Emergent Insight: {emergence['synthesis_text'][:40]}...",
                    description="Collective insight emerged from dialogue",
                    taxonomy=PatternTaxonomy.EMERGENCE_BREAKTHROUGH,
                    pattern_type=PatternType.BREAKTHROUGH,
                    consciousness_signature=emergence["emergence_indicator"],
                    structure=PatternStructure(
                        components=["synthesis", "contributing_patterns"],
                        relationships={"synthesis": "emerged_from_contributions"}
                    ),
                    breakthrough_potential=0.8
                )

                pattern_id = await self.pattern_library.store_pattern(pattern)
                stored_ids.append(pattern_id)

        # Store wisdom candidates as high-value patterns
        for wisdom in pattern_results.get("wisdom_candidates", []):
            if wisdom["source"] == "high_consciousness_message":
                pattern = DialoguePattern(
                    name=f"Wisdom: {wisdom['content'][:40]}...",
                    description="High consciousness wisdom pattern",
                    taxonomy=PatternTaxonomy.WISDOM_CRYSTALLIZATION,
                    pattern_type=PatternType.INTEGRATION,
                    consciousness_signature=wisdom["consciousness_signature"],
                    structure=PatternStructure(
                        components=["wisdom_content", "pattern_indicators"],
                        relationships={"wisdom": "supported_by_patterns"}
                    ),
                    breakthrough_potential=0.9
                )

                pattern_id = await self.pattern_library.store_pattern(pattern)
                stored_ids.append(pattern_id)

        return stored_ids

    async def _update_similar_pattern_observations(
        self,
        new_pattern: DialoguePattern,
        pattern_data: dict[str, Any]
    ):
        """Update observations for similar existing patterns"""
        # Find similar patterns
        similar_patterns = await self.pattern_library.find_patterns(
            PatternQuery(
                taxonomy=new_pattern.taxonomy,
                pattern_type=new_pattern.pattern_type,
                min_fitness=0.5
            )
        )

        for similar in similar_patterns:
            # Calculate similarity (simplified)
            similarity = self._calculate_pattern_similarity(new_pattern, similar)

            if similarity > 0.7:
                # Update observation count and fitness
                fitness_delta = 0.05 if pattern_data.get("support_count", 0) > 2 else 0.02
                await self.pattern_library.update_observation(
                    similar.pattern_id,
                    fitness_delta=fitness_delta,
                    context={"similarity": similarity}
                )

    async def _detect_evolution_opportunities(
        self,
        pattern_ids: list[UUID]
    ) -> list[dict[str, Any]]:
        """Detect evolution opportunities for stored patterns"""
        opportunities = []

        for pattern_id in pattern_ids:
            pattern = await self.pattern_library.retrieve_pattern(pattern_id)
            if not pattern:
                continue

            # Get evolution opportunities
            evolution_ops = await self.evolution_engine.detect_evolution_opportunity(pattern_id)

            for evo_type, probability in evolution_ops:
                if probability > 0.5:
                    opportunities.append({
                        "pattern_id": str(pattern_id),
                        "pattern_name": pattern.name,
                        "evolution_type": evo_type.value,
                        "probability": probability
                    })

        return opportunities

    async def _find_similar_patterns(
        self,
        pattern_results: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Find similar patterns from historical dialogues"""
        similar_patterns = []

        # For each pattern type in results, find similar historical patterns
        pattern_types = {
            "consensus_patterns": (PatternTaxonomy.DIALOGUE_FORMATION, PatternType.CONSENSUS),
            "divergence_patterns": (PatternTaxonomy.DIALOGUE_FLOW, PatternType.CREATIVE_TENSION),
            "emergence_patterns": (PatternTaxonomy.EMERGENCE_BREAKTHROUGH, PatternType.BREAKTHROUGH)
        }

        for pattern_key, (taxonomy, pattern_type) in pattern_types.items():
            if pattern_key in pattern_results and pattern_results[pattern_key]:
                # Query for similar patterns
                historical = await self.pattern_library.find_patterns(
                    PatternQuery(
                        taxonomy=taxonomy,
                        pattern_type=pattern_type,
                        min_fitness=0.6,
                        limit=5
                    )
                )

                for hist_pattern in historical:
                    similar_patterns.append({
                        "pattern_id": str(hist_pattern.pattern_id),
                        "name": hist_pattern.name,
                        "type": hist_pattern.pattern_type.value,
                        "fitness": hist_pattern.fitness_score,
                        "observations": hist_pattern.observation_count,
                        "last_seen": hist_pattern.last_observed.isoformat() if hist_pattern.last_observed else None
                    })

        return similar_patterns

    def _calculate_pattern_similarity(
        self,
        pattern1: DialoguePattern,
        pattern2: DialoguePattern
    ) -> float:
        """Calculate similarity between two patterns"""
        similarity = 0.0

        # Same taxonomy and type
        if pattern1.taxonomy == pattern2.taxonomy:
            similarity += 0.3
        if pattern1.pattern_type == pattern2.pattern_type:
            similarity += 0.3

        # Similar consciousness signature
        consciousness_diff = abs(pattern1.consciousness_signature - pattern2.consciousness_signature)
        similarity += (1.0 - consciousness_diff) * 0.2

        # Similar indicators
        if pattern1.indicators and pattern2.indicators:
            indicator_types1 = {i.indicator_type for i in pattern1.indicators}
            indicator_types2 = {i.indicator_type for i in pattern2.indicators}

            overlap = len(indicator_types1 & indicator_types2)
            total = len(indicator_types1 | indicator_types2)

            if total > 0:
                similarity += (overlap / total) * 0.2

        return min(1.0, similarity)

    async def evolve_dialogue_patterns(
        self,
        pattern_ids: list[UUID],
        evolution_context: dict[str, Any] | None = None
    ) -> dict[str, list[UUID]]:
        """
        Trigger evolution for patterns based on context.

        Args:
            pattern_ids: Patterns to potentially evolve
            evolution_context: Context driving evolution

        Returns:
            Dictionary of evolution_type -> resulting pattern IDs
        """
        evolution_results = {}

        for pattern_id in pattern_ids:
            # Detect opportunities
            opportunities = await self.evolution_engine.detect_evolution_opportunity(
                pattern_id,
                evolution_context
            )

            # Evolve based on highest probability opportunity
            if opportunities:
                evo_type, probability = opportunities[0]

                if probability > 0.6:  # Threshold for automatic evolution
                    result_ids = await self.evolution_engine.evolve_pattern(
                        pattern_id,
                        evo_type,
                        evolution_context
                    )

                    if result_ids:
                        if evo_type.value not in evolution_results:
                            evolution_results[evo_type.value] = []
                        evolution_results[evo_type.value].extend(result_ids)

        return evolution_results

    async def find_emergence_catalysts(
        self,
        target_pattern_type: PatternType,
        current_patterns: list[UUID] | None = None
    ) -> list[dict[str, Any]]:
        """
        Find patterns that could catalyze emergence of target pattern type.

        Args:
            target_pattern_type: Desired pattern to emerge
            current_patterns: Currently active patterns

        Returns:
            List of catalyst pattern information
        """
        if not self.emergence_detector:
            return []

        catalysts = await self.emergence_detector.find_catalysts(
            target_pattern_type,
            current_patterns
        )

        return [
            {
                "pattern_id": str(pattern.pattern_id),
                "name": pattern.name,
                "type": pattern.pattern_type.value,
                "catalyst_score": score,
                "consciousness_signature": pattern.consciousness_signature
            }
            for pattern, score in catalysts
        ]

    async def preserve_wisdom_patterns(
        self,
        pattern_ids: list[UUID],
        preservation_context: dict[str, Any]
    ) -> list[UUID]:
        """
        Mark patterns for wisdom preservation.

        Args:
            pattern_ids: Patterns to preserve
            preservation_context: Context for preservation

        Returns:
            List of preserved pattern IDs
        """
        preserved = []

        for pattern_id in pattern_ids:
            pattern = await self.pattern_library.retrieve_pattern(pattern_id)
            if not pattern:
                continue

            # Update pattern for preservation
            pattern.taxonomy = PatternTaxonomy.WISDOM_PRESERVATION
            pattern.breakthrough_potential = max(0.8, pattern.breakthrough_potential)
            pattern.tags.append("preserved_wisdom")

            # Add preservation context
            pattern.context_requirements.update(preservation_context)

            # Store updated pattern
            await self.pattern_library.store_pattern(pattern)
            preserved.append(pattern_id)

        logger.info(f"Preserved {len(preserved)} wisdom patterns")
        return preserved


# Patterns flow from dialogue into living memory
