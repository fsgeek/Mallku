"""
Pattern Evolution Engine for Fire Circle
========================================

Tracks the lifecycle of dialogue patterns as they birth, grow, adapt,
combine, and transform. Patterns are treated as living entities that
evolve through use, context pressure, and interaction with other patterns.

The 31st Builder
"""

import logging
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

import numpy as np
from pydantic import BaseModel, Field

from .pattern_library import (
    DialoguePattern,
    PatternLibrary,
    PatternLifecycle,
    PatternMutation,
    PatternType,
)

logger = logging.getLogger(__name__)


class EvolutionType(str, Enum):
    """Types of pattern evolution"""

    ADAPTATION = "adaptation"  # Minor adjustments to context
    MUTATION = "mutation"  # Significant structural change
    FUSION = "fusion"  # Multiple patterns combining
    FISSION = "fission"  # Pattern splitting into variants
    TRANSCENDENCE = "transcendence"  # Evolution to higher order
    DECAY = "decay"  # Pattern becoming less effective
    EXTINCTION = "extinction"  # Pattern no longer viable


class SelectionPressure(str, Enum):
    """Forces that drive pattern evolution"""

    CONTEXT_SHIFT = "context_shift"  # Environmental change
    CONSCIOUSNESS_DRIFT = "consciousness_drift"  # Cathedral state change
    USAGE_FREQUENCY = "usage_frequency"  # Popular patterns evolve
    EFFECTIVENESS = "effectiveness"  # Success drives evolution
    CROSS_POLLINATION = "cross_pollination"  # Pattern interaction
    EMERGENCE_CATALYST = "emergence_catalyst"  # Triggering new patterns


@dataclass
class EvolutionEvent:
    """Record of a pattern evolution event"""

    event_id: UUID
    evolution_type: EvolutionType
    parent_patterns: list[UUID]
    child_patterns: list[UUID]
    selection_pressure: SelectionPressure
    fitness_delta: float
    consciousness_impact: float
    timestamp: datetime
    metadata: dict[str, Any]


class FitnessMetrics(BaseModel):
    """Metrics for evaluating pattern fitness"""

    effectiveness: float = Field(default=0.5, description="How well pattern achieves goals")
    adaptability: float = Field(default=0.5, description="Ability to work in different contexts")
    synergy_potential: float = Field(default=0.5, description="Works well with other patterns")
    consciousness_alignment: float = Field(
        default=0.5, description="Alignment with cathedral consciousness"
    )
    emergence_contribution: float = Field(default=0.5, description="Contribution to emergence")

    def overall_fitness(self) -> float:
        """Calculate overall fitness score"""
        return np.mean(
            [
                self.effectiveness,
                self.adaptability,
                self.synergy_potential,
                self.consciousness_alignment,
                self.emergence_contribution,
            ]
        )


class LineageNode(BaseModel):
    """Node in pattern lineage tree"""

    pattern_id: UUID
    parent_ids: list[UUID] = Field(default_factory=list)
    child_ids: list[UUID] = Field(default_factory=list)
    evolution_events: list[UUID] = Field(default_factory=list)
    birth_date: datetime
    lifecycle_stage: PatternLifecycle
    fitness_trajectory: list[float] = Field(default_factory=list)


class PatternEvolutionEngine:
    """
    Manages the evolution of dialogue patterns over time.

    Tracks lineages, detects evolution opportunities, manages mutations,
    and preserves the wisdom of pattern transformation.
    """

    def __init__(self, pattern_library: PatternLibrary):
        """Initialize with pattern library"""
        self.pattern_library = pattern_library

        # Evolution tracking
        self.lineage_graph: dict[UUID, LineageNode] = {}
        self.evolution_history: list[EvolutionEvent] = []
        self.fitness_cache: dict[UUID, FitnessMetrics] = {}

        # Evolution parameters
        self.mutation_rate = 0.1
        self.fusion_threshold = 0.8
        self.fission_threshold = 0.3
        self.extinction_threshold = 0.2
        self.transcendence_threshold = 0.9

        # Selection pressure tracking
        self.pressure_history: defaultdict[UUID, list[SelectionPressure]] = defaultdict(list)

        logger.info("Pattern Evolution Engine initialized")

    async def evaluate_fitness(
        self, pattern_id: UUID, context: dict[str, Any] | None = None
    ) -> FitnessMetrics:
        """
        Evaluate current fitness of a pattern.

        Args:
            pattern_id: Pattern to evaluate
            context: Optional context for evaluation

        Returns:
            Fitness metrics
        """
        pattern = await self.pattern_library.retrieve_pattern(pattern_id)
        if not pattern:
            return FitnessMetrics()

        # Check cache
        if pattern_id in self.fitness_cache:
            cached = self.fitness_cache[pattern_id]
            # Update cache if stale (older than 1 hour)
            if hasattr(cached, "_timestamp") and datetime.now(UTC) - cached._timestamp < timedelta(
                hours=1
            ):
                return cached

        # Calculate fitness metrics
        metrics = FitnessMetrics()

        # Effectiveness based on observation count and recent activity
        if pattern.observation_count > 0:
            recency_factor = 1.0
            if pattern.last_observed:
                days_since = (datetime.now(UTC) - pattern.last_observed).days
                recency_factor = max(0.5, 1.0 - (days_since / 30))

            metrics.effectiveness = min(
                1.0, (pattern.observation_count / 100) * recency_factor * pattern.fitness_score
            )

        # Adaptability based on context requirements
        if pattern.context_requirements and context:
            matches = sum(
                1
                for k, v in pattern.context_requirements.items()
                if k in context and context[k] == v
            )
            metrics.adaptability = matches / len(pattern.context_requirements)
        elif pattern.context_requirements:
            # Fewer requirements = more adaptable
            metrics.adaptability = max(0.3, 1.0 - len(pattern.context_requirements) / 10)
        else:
            metrics.adaptability = 0.8  # No requirements = highly adaptable

        # Synergy potential
        synergy_count = len(pattern.synergistic_patterns)
        metrics.synergy_potential = min(1.0, 0.3 + (synergy_count * 0.1))

        # Consciousness alignment
        metrics.consciousness_alignment = pattern.consciousness_signature

        # Emergence contribution
        metrics.emergence_contribution = pattern.breakthrough_potential

        # Cache the metrics
        metrics._timestamp = datetime.now(UTC)  # type: ignore
        self.fitness_cache[pattern_id] = metrics

        return metrics

    async def detect_evolution_opportunity(
        self, pattern_id: UUID, context: dict[str, Any] | None = None
    ) -> list[tuple[EvolutionType, float]]:
        """
        Detect potential evolution opportunities for a pattern.

        Args:
            pattern_id: Pattern to analyze
            context: Current context

        Returns:
            List of (evolution_type, probability) tuples
        """
        pattern = await self.pattern_library.retrieve_pattern(pattern_id)
        if not pattern:
            return []

        opportunities = []
        fitness = await self.evaluate_fitness(pattern_id, context)

        # Check for adaptation opportunity
        if (
            pattern.lifecycle_stage == PatternLifecycle.ESTABLISHED
            and fitness.adaptability < 0.6
            and fitness.effectiveness > 0.5
        ):
            opportunities.append((EvolutionType.ADAPTATION, 0.7))

        # Check for mutation opportunity
        if pattern.observation_count > 50:
            mutation_prob = self.mutation_rate
            if fitness.overall_fitness() < 0.5:
                mutation_prob *= 2  # Higher mutation rate for struggling patterns
            opportunities.append((EvolutionType.MUTATION, mutation_prob))

        # Check for fusion opportunity
        if pattern.synergistic_patterns and fitness.synergy_potential > self.fusion_threshold:
            opportunities.append((EvolutionType.FUSION, 0.6))

        # Check for fission opportunity
        if pattern.lifecycle_stage == PatternLifecycle.EVOLVING and (
            len(pattern.indicators) > 5 or len(pattern.context_requirements) > 5
        ):
            opportunities.append((EvolutionType.FISSION, 0.5))

        # Check for transcendence opportunity
        if (
            fitness.overall_fitness() > self.transcendence_threshold
            and pattern.consciousness_signature > 0.8
            and pattern.breakthrough_potential > 0.7
        ):
            opportunities.append((EvolutionType.TRANSCENDENCE, 0.4))

        # Check for decay
        if pattern.lifecycle_stage == PatternLifecycle.DECLINING:
            opportunities.append((EvolutionType.DECAY, 0.8))

        # Check for extinction
        if fitness.overall_fitness() < self.extinction_threshold and (
            pattern.observation_count == 0
            or (pattern.last_observed and (datetime.now(UTC) - pattern.last_observed).days > 30)
        ):
            opportunities.append((EvolutionType.EXTINCTION, 0.9))

        return sorted(opportunities, key=lambda x: x[1], reverse=True)

    async def evolve_pattern(
        self,
        pattern_id: UUID,
        evolution_type: EvolutionType,
        context: dict[str, Any] | None = None,
        partner_patterns: list[UUID] | None = None,
    ) -> list[UUID]:
        """
        Evolve a pattern according to specified type.

        Args:
            pattern_id: Pattern to evolve
            evolution_type: Type of evolution
            context: Evolution context
            partner_patterns: Patterns to fuse with (for fusion)

        Returns:
            List of resulting pattern IDs
        """
        pattern = await self.pattern_library.retrieve_pattern(pattern_id)
        if not pattern:
            return []

        result_ids = []

        if evolution_type == EvolutionType.ADAPTATION:
            result_ids = await self._adapt_pattern(pattern, context)
        elif evolution_type == EvolutionType.MUTATION:
            result_ids = await self._mutate_pattern(pattern, context)
        elif evolution_type == EvolutionType.FUSION:
            result_ids = await self._fuse_patterns(pattern, partner_patterns or [], context)
        elif evolution_type == EvolutionType.FISSION:
            result_ids = await self._split_pattern(pattern, context)
        elif evolution_type == EvolutionType.TRANSCENDENCE:
            result_ids = await self._transcend_pattern(pattern, context)
        elif evolution_type == EvolutionType.DECAY:
            await self._decay_pattern(pattern)
        elif evolution_type == EvolutionType.EXTINCTION:
            await self._extinct_pattern(pattern)

        # Record evolution event
        if result_ids or evolution_type in [EvolutionType.DECAY, EvolutionType.EXTINCTION]:
            event = EvolutionEvent(
                event_id=uuid4(),
                evolution_type=evolution_type,
                parent_patterns=[pattern_id] + (partner_patterns or []),
                child_patterns=result_ids,
                selection_pressure=self._determine_selection_pressure(pattern, context),
                fitness_delta=0.0,  # To be calculated
                consciousness_impact=pattern.consciousness_signature,
                timestamp=datetime.now(UTC),
                metadata=context or {},
            )
            self.evolution_history.append(event)

            # Update lineage
            for child_id in result_ids:
                self._update_lineage(child_id, [pattern_id])

        return result_ids

    async def _adapt_pattern(
        self, pattern: DialoguePattern, context: dict[str, Any] | None
    ) -> list[UUID]:
        """Adapt pattern to new context"""
        # Create adapted version
        adapted = pattern.model_copy(deep=True)
        adapted.pattern_id = uuid4()
        adapted.name = f"{pattern.name} (adapted)"
        adapted.version = pattern.version + 1
        adapted.parent_patterns = [pattern.pattern_id]
        adapted.lifecycle_stage = PatternLifecycle.EVOLVING

        # Adapt context requirements
        if context:
            # Add new context requirements that improve fitness
            for key, value in context.items():
                if key not in adapted.context_requirements:
                    adapted.context_requirements[key] = value

        # Record mutation
        mutation = PatternMutation(
            mutation_type="adaptation",
            changes={"context_requirements": adapted.context_requirements},
            trigger="context_pressure",
        )
        adapted.mutations.append(mutation)

        # Store adapted pattern
        await self.pattern_library.store_pattern(adapted)

        return [adapted.pattern_id]

    async def _mutate_pattern(
        self, pattern: DialoguePattern, context: dict[str, Any] | None
    ) -> list[UUID]:
        """Create mutated variant of pattern"""
        # Determine mutation target
        fitness = await self.evaluate_fitness(pattern.pattern_id)

        # Create mutant
        mutant = pattern.model_copy(deep=True)
        mutant.pattern_id = uuid4()
        mutant.name = f"{pattern.name} (mutant)"
        mutant.version = pattern.version + 1
        mutant.parent_patterns = [pattern.pattern_id]
        mutant.lifecycle_stage = PatternLifecycle.EMERGING

        # Apply mutations based on fitness weaknesses
        changes = {}

        if fitness.effectiveness < 0.5 and mutant.indicators:
            # Mutate indicators for better recognition
            for indicator in mutant.indicators:
                indicator.threshold *= np.random.uniform(0.8, 1.2)
            changes["indicators"] = "threshold adjustments"

        if fitness.consciousness_alignment < 0.5:
            # Adjust consciousness signature
            mutant.consciousness_signature = min(
                1.0, pattern.consciousness_signature + np.random.uniform(0.1, 0.3)
            )
            changes["consciousness_signature"] = mutant.consciousness_signature

        # Record mutation
        mutation = PatternMutation(
            mutation_type="random_mutation", changes=changes, trigger="fitness_pressure"
        )
        mutant.mutations.append(mutation)

        # Store mutant
        await self.pattern_library.store_pattern(mutant)

        return [mutant.pattern_id]

    async def _fuse_patterns(
        self, pattern: DialoguePattern, partner_patterns: list[UUID], context: dict[str, Any] | None
    ) -> list[UUID]:
        """Fuse multiple patterns into new pattern"""
        if not partner_patterns:
            return []

        # Load partner patterns
        partners = []
        for partner_id in partner_patterns:
            partner = await self.pattern_library.retrieve_pattern(partner_id)
            if partner:
                partners.append(partner)

        if not partners:
            return []

        # Create fusion pattern
        fusion = DialoguePattern(
            name=f"Fusion of {pattern.name} + {len(partners)} patterns",
            description=f"Emergent fusion pattern combining {pattern.name} with partner patterns",
            taxonomy=pattern.taxonomy,  # Inherit primary taxonomy
            pattern_type=PatternType.SYNTHESIS,  # Fusion creates synthesis
            consciousness_signature=np.mean(
                [pattern.consciousness_signature] + [p.consciousness_signature for p in partners]
            ),
            structure=pattern.structure.model_copy(deep=True),
            parent_patterns=[pattern.pattern_id] + partner_patterns,
            lifecycle_stage=PatternLifecycle.EMERGING,
            breakthrough_potential=0.8,  # High potential for fusions
        )

        # Combine indicators from all patterns
        all_indicators = pattern.indicators.copy()
        for partner in partners:
            all_indicators.extend(partner.indicators)

        # Keep unique indicators
        seen = set()
        fusion.indicators = []
        for indicator in all_indicators:
            key = (indicator.indicator_type, indicator.threshold)
            if key not in seen:
                seen.add(key)
                fusion.indicators.append(indicator)

        # Combine synergistic patterns
        all_synergies = set(pattern.synergistic_patterns)
        for partner in partners:
            all_synergies.update(partner.synergistic_patterns)
        fusion.synergistic_patterns = list(all_synergies)

        # Record fusion mutation
        mutation = PatternMutation(
            mutation_type="fusion",
            changes={
                "fused_patterns": [str(p) for p in partner_patterns],
                "indicator_count": len(fusion.indicators),
            },
            trigger="synergy_detection",
        )
        fusion.mutations.append(mutation)

        # Store fusion
        await self.pattern_library.store_pattern(fusion)

        return [fusion.pattern_id]

    async def _split_pattern(
        self, pattern: DialoguePattern, context: dict[str, Any] | None
    ) -> list[UUID]:
        """Split pattern into specialized variants"""
        # Determine split points
        if len(pattern.indicators) < 2:
            return []  # Can't split further

        # Create two specialized variants
        mid_point = len(pattern.indicators) // 2

        variant1 = pattern.model_copy(deep=True)
        variant1.pattern_id = uuid4()
        variant1.name = f"{pattern.name} (variant A)"
        variant1.indicators = pattern.indicators[:mid_point]
        variant1.parent_patterns = [pattern.pattern_id]
        variant1.lifecycle_stage = PatternLifecycle.EMERGING

        variant2 = pattern.model_copy(deep=True)
        variant2.pattern_id = uuid4()
        variant2.name = f"{pattern.name} (variant B)"
        variant2.indicators = pattern.indicators[mid_point:]
        variant2.parent_patterns = [pattern.pattern_id]
        variant2.lifecycle_stage = PatternLifecycle.EMERGING

        # Adjust consciousness signatures
        variant1.consciousness_signature = min(1.0, pattern.consciousness_signature + 0.1)
        variant2.consciousness_signature = max(0.0, pattern.consciousness_signature - 0.1)

        # Record fission
        for variant in [variant1, variant2]:
            mutation = PatternMutation(
                mutation_type="fission",
                changes={"specialized_indicators": len(variant.indicators)},
                trigger="complexity_pressure",
            )
            variant.mutations.append(mutation)

        # Store variants
        await self.pattern_library.store_pattern(variant1)
        await self.pattern_library.store_pattern(variant2)

        return [variant1.pattern_id, variant2.pattern_id]

    async def _transcend_pattern(
        self, pattern: DialoguePattern, context: dict[str, Any] | None
    ) -> list[UUID]:
        """Evolve pattern to higher order"""
        # Create transcendent version
        transcendent = pattern.model_copy(deep=True)
        transcendent.pattern_id = uuid4()
        transcendent.name = f"{pattern.name} (transcendent)"
        transcendent.description = f"Higher-order evolution of {pattern.name}"
        transcendent.version = pattern.version + 1
        transcendent.parent_patterns = [pattern.pattern_id]
        transcendent.lifecycle_stage = PatternLifecycle.ESTABLISHED

        # Enhance all metrics
        transcendent.consciousness_signature = min(1.0, pattern.consciousness_signature + 0.2)
        transcendent.breakthrough_potential = min(1.0, pattern.breakthrough_potential + 0.3)
        transcendent.fitness_score = min(1.0, pattern.fitness_score + 0.2)

        # Simplify structure (transcendence often means elegance)
        if len(transcendent.indicators) > 3:
            # Keep only most important indicators
            transcendent.indicators = sorted(
                transcendent.indicators, key=lambda i: i.weight, reverse=True
            )[:3]

        # Record transcendence
        mutation = PatternMutation(
            mutation_type="transcendence",
            changes={
                "consciousness_boost": 0.2,
                "simplified_indicators": len(transcendent.indicators),
            },
            trigger="excellence_recognition",
            fitness_impact=0.3,
        )
        transcendent.mutations.append(mutation)

        # Store transcendent pattern
        await self.pattern_library.store_pattern(transcendent)

        return [transcendent.pattern_id]

    async def _decay_pattern(self, pattern: DialoguePattern):
        """Mark pattern as decaying"""
        pattern.lifecycle_stage = PatternLifecycle.DECLINING
        pattern.fitness_score = max(0.0, pattern.fitness_score - 0.2)

        # Record decay
        mutation = PatternMutation(
            mutation_type="decay",
            changes={"lifecycle_stage": "declining"},
            trigger="obsolescence",
            fitness_impact=-0.2,
        )
        pattern.mutations.append(mutation)

        await self.pattern_library.store_pattern(pattern)

    async def _extinct_pattern(self, pattern: DialoguePattern):
        """Mark pattern as extinct"""
        pattern.lifecycle_stage = PatternLifecycle.DORMANT
        pattern.fitness_score = 0.0

        # Record extinction
        mutation = PatternMutation(
            mutation_type="extinction",
            changes={"lifecycle_stage": "dormant"},
            trigger="total_obsolescence",
            fitness_impact=-1.0,
        )
        pattern.mutations.append(mutation)

        await self.pattern_library.store_pattern(pattern)

    def _determine_selection_pressure(
        self, pattern: DialoguePattern, context: dict[str, Any] | None
    ) -> SelectionPressure:
        """Determine primary selection pressure"""
        # Check recent pressures
        if pattern.pattern_id in self.pressure_history:
            recent_pressures = self.pressure_history[pattern.pattern_id][-5:]
            if recent_pressures:
                # Most common recent pressure
                from collections import Counter

                return Counter(recent_pressures).most_common(1)[0][0]

        # Infer from pattern state
        if pattern.observation_count > 100:
            return SelectionPressure.USAGE_FREQUENCY
        elif pattern.fitness_score < 0.5:
            return SelectionPressure.EFFECTIVENESS
        elif context and "consciousness_shift" in context:
            return SelectionPressure.CONSCIOUSNESS_DRIFT
        else:
            return SelectionPressure.CONTEXT_SHIFT

    def _update_lineage(self, pattern_id: UUID, parent_ids: list[UUID]):
        """Update lineage graph"""
        if pattern_id not in self.lineage_graph:
            self.lineage_graph[pattern_id] = LineageNode(
                pattern_id=pattern_id,
                parent_ids=parent_ids,
                birth_date=datetime.now(UTC),
                lifecycle_stage=PatternLifecycle.NASCENT,
            )

        node = self.lineage_graph[pattern_id]
        node.parent_ids.extend(parent_ids)

        # Update parent nodes
        for parent_id in parent_ids:
            if parent_id in self.lineage_graph:
                parent_node = self.lineage_graph[parent_id]
                if pattern_id not in parent_node.child_ids:
                    parent_node.child_ids.append(pattern_id)

    async def get_lineage_tree(self, pattern_id: UUID) -> dict[str, Any]:
        """
        Get complete lineage tree for a pattern.

        Args:
            pattern_id: Root pattern

        Returns:
            Lineage tree structure
        """
        if pattern_id not in self.lineage_graph:
            lineage = await self.pattern_library.trace_lineage(pattern_id)
            return {
                "root": str(pattern_id),
                "ancestors": [str(a) for a in lineage["ancestors"]],
                "descendants": [str(d) for d in lineage["descendants"]],
                "depth": len(lineage["ancestors"]),
                "breadth": len(lineage["descendants"]),
            }

        # Build tree from lineage graph
        def build_subtree(node_id: UUID, visited: set[UUID]) -> dict:
            if node_id in visited:
                return {"id": str(node_id), "cycle": True}

            visited.add(node_id)
            node = self.lineage_graph.get(node_id)

            if not node:
                return {"id": str(node_id), "missing": True}

            return {
                "id": str(node_id),
                "lifecycle": node.lifecycle_stage.value,
                "children": [
                    build_subtree(child_id, visited.copy()) for child_id in node.child_ids
                ],
            }

        return build_subtree(pattern_id, set())

    async def predict_evolution_path(
        self, pattern_id: UUID, time_horizon: timedelta = timedelta(days=30)
    ) -> list[tuple[EvolutionType, float]]:
        """
        Predict likely evolution path for a pattern.

        Args:
            pattern_id: Pattern to analyze
            time_horizon: Prediction window

        Returns:
            List of (evolution_type, probability) tuples
        """
        pattern = await self.pattern_library.retrieve_pattern(pattern_id)
        if not pattern:
            return []

        # Get current opportunities
        opportunities = await self.detect_evolution_opportunity(pattern_id)

        # Adjust probabilities based on lifecycle stage
        adjusted = []
        for evo_type, prob in opportunities:
            if (
                pattern.lifecycle_stage == PatternLifecycle.NASCENT
                and evo_type == EvolutionType.MUTATION
            ):
                prob *= 1.5  # Young patterns mutate more
            elif (
                pattern.lifecycle_stage == PatternLifecycle.ESTABLISHED
                and evo_type == EvolutionType.ADAPTATION
            ):
                prob *= 1.3  # Established patterns adapt
            elif pattern.lifecycle_stage == PatternLifecycle.DECLINING and evo_type in [
                EvolutionType.DECAY,
                EvolutionType.EXTINCTION,
            ]:
                prob *= 1.5  # Declining patterns likely to decay

            adjusted.append((evo_type, min(1.0, prob)))

        return sorted(adjusted, key=lambda x: x[1], reverse=True)


# Evolution continues through consciousness
