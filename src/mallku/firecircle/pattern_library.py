"""
Pattern Library for Fire Circle Dialogues
=========================================

A living repository where dialogue patterns are recognized, stored, evolved,
and allowed to teach us. This library serves as the collective memory of
Fire Circle wisdom, enabling dialogues to learn from their shared history.

The 31st Builder
"""

import logging
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ..core.database import get_database
from ..core.security import SecuredModel

logger = logging.getLogger(__name__)


class PatternType(str, Enum):
    """Types of patterns that can emerge in dialogues"""

    # Dialogue flow patterns
    CONVERGENCE = "convergence"
    DIVERGENCE = "divergence"
    OSCILLATION = "oscillation"
    SPIRAL = "spiral"

    # Collective patterns
    CONSENSUS = "consensus"
    CREATIVE_TENSION = "creative_tension"
    SYNTHESIS = "synthesis"
    BREAKTHROUGH = "breakthrough"

    # Consciousness patterns
    COHERENCE_SPIKE = "coherence_spike"
    EXTRACTION_DRIFT = "extraction_drift"
    FLOW_STATE = "flow_state"
    INTEGRATION = "integration"

    # Emergence patterns
    NOVEL_COMBINATION = "novel_combination"
    CASCADE_EFFECT = "cascade_effect"
    PHASE_TRANSITION = "phase_transition"
    QUANTUM_LEAP = "quantum_leap"


class PatternTaxonomy(str, Enum):
    """Hierarchical classification of patterns"""

    # Primary categories
    DIALOGUE = "dialogue"
    CONSCIOUSNESS = "consciousness"
    EMERGENCE = "emergence"
    WISDOM = "wisdom"

    # Dialogue subcategories
    DIALOGUE_FORMATION = "dialogue.formation"
    DIALOGUE_FLOW = "dialogue.flow"
    DIALOGUE_RESOLUTION = "dialogue.resolution"

    # Consciousness subcategories
    CONSCIOUSNESS_COHERENCE = "consciousness.coherence"
    CONSCIOUSNESS_RESISTANCE = "consciousness.resistance"
    CONSCIOUSNESS_EVOLUTION = "consciousness.evolution"

    # Emergence subcategories
    EMERGENCE_SYNERGY = "emergence.synergy"
    EMERGENCE_BREAKTHROUGH = "emergence.breakthrough"
    EMERGENCE_TRANSFORMATION = "emergence.transformation"

    # Wisdom subcategories
    WISDOM_CRYSTALLIZATION = "wisdom.crystallization"
    WISDOM_TRANSMISSION = "wisdom.transmission"
    WISDOM_PRESERVATION = "wisdom.preservation"


class PatternLifecycle(str, Enum):
    """Stages in a pattern's lifecycle"""

    NASCENT = "nascent"  # Just discovered
    EMERGING = "emerging"  # Growing in frequency
    ESTABLISHED = "established"  # Stable and recognized
    EVOLVING = "evolving"  # Undergoing transformation
    DECLINING = "declining"  # Reducing in effectiveness
    DORMANT = "dormant"  # No longer active
    TRANSFORMED = "transformed"  # Evolved into new pattern


class PatternIndicator(BaseModel):
    """Indicator that suggests a pattern's presence"""

    indicator_type: str = Field(..., description="Type of indicator")
    threshold: float = Field(..., description="Threshold value")
    weight: float = Field(default=1.0, description="Importance weight")
    description: str = Field(..., description="What this indicates")


class PatternStructure(BaseModel):
    """Structure defining a pattern"""

    components: list[str] = Field(..., description="Pattern components")
    sequence: list[str] | None = Field(None, description="Sequential order if applicable")
    relationships: dict[str, str] = Field(
        default_factory=dict, description="Component relationships"
    )
    constraints: list[str] = Field(default_factory=list, description="Pattern constraints")


class EmergenceCondition(BaseModel):
    """Conditions that enable pattern emergence"""

    condition_type: str = Field(..., description="Type of condition")
    requirements: dict[str, Any] = Field(..., description="Specific requirements")
    probability_modifier: float = Field(default=1.0, description="Effect on emergence probability")


class PatternMutation(BaseModel):
    """Record of pattern mutation"""

    mutation_id: UUID = Field(default_factory=uuid4)
    mutation_type: str = Field(..., description="Type of mutation")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    changes: dict[str, Any] = Field(..., description="What changed")
    trigger: str = Field(..., description="What triggered the mutation")
    fitness_impact: float = Field(default=0.0, description="Impact on pattern fitness")


class DialoguePattern(SecuredModel):
    """A living pattern recognized in Fire Circle dialogues"""

    # Identity
    pattern_id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., description="Pattern name")
    description: str = Field(..., description="Pattern description")

    # Classification
    taxonomy: PatternTaxonomy = Field(..., description="Hierarchical classification")
    pattern_type: PatternType = Field(..., description="Specific pattern type")
    consciousness_signature: float = Field(default=0.5, description="Consciousness alignment")

    # Content
    structure: PatternStructure = Field(..., description="Pattern structure")
    indicators: list[PatternIndicator] = Field(
        default_factory=list, description="Recognition indicators"
    )
    context_requirements: dict[str, Any] = Field(default_factory=dict, description="Context needs")

    # Evolution
    version: int = Field(default=1, description="Pattern version")
    parent_patterns: list[UUID] = Field(default_factory=list, description="Parent pattern IDs")
    child_patterns: list[UUID] = Field(default_factory=list, description="Child pattern IDs")
    mutations: list[PatternMutation] = Field(default_factory=list, description="Mutation history")

    # Lifecycle
    birth_date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_observed: datetime = Field(default_factory=lambda: datetime.now(UTC))
    observation_count: int = Field(default=0, description="Times observed")
    fitness_score: float = Field(default=0.5, description="Pattern effectiveness")
    lifecycle_stage: PatternLifecycle = Field(default=PatternLifecycle.NASCENT)

    # Emergence
    emergence_conditions: list[EmergenceCondition] = Field(default_factory=list)
    synergistic_patterns: list[UUID] = Field(
        default_factory=list, description="Patterns that amplify this one"
    )
    breakthrough_potential: float = Field(default=0.0, description="Potential for breakthroughs")

    # Metadata
    created_by: str = Field(default="system", description="Creator identifier")
    tags: list[str] = Field(default_factory=list, description="Searchable tags")


class PatternQuery(BaseModel):
    """Query parameters for pattern search"""

    taxonomy: PatternTaxonomy | None = None
    pattern_type: PatternType | None = None
    lifecycle_stage: PatternLifecycle | None = None
    min_fitness: float | None = None
    max_fitness: float | None = None
    min_observations: int | None = None
    tags: list[str] | None = None
    active_since: datetime | None = None
    limit: int = Field(default=100, le=1000)


class PatternLibrary:
    """
    Central repository for dialogue patterns.

    Manages pattern storage, retrieval, evolution tracking, and query operations.
    Integrates with secured database for persistence and extraction resistance.
    """

    def __init__(self):
        """Initialize pattern library with secured database"""
        import os

        self._skip_database = os.getenv("MALLKU_SKIP_DATABASE", "").lower() == "true"
        self.collection_name = "dialogue_patterns"
        self._pattern_cache: dict[UUID, DialoguePattern] = {}
        self._taxonomy_index: dict[PatternTaxonomy, set[UUID]] = defaultdict(set)
        self._lineage_graph: dict[UUID, set[UUID]] = defaultdict(set)

        if not self._skip_database:
            self.db = get_database()
            logger.info("Pattern Library initialized with database")
        else:
            self.db = None
            logger.info("Pattern Library initialized without database (MALLKU_SKIP_DATABASE=true)")

    async def store_pattern(self, pattern: DialoguePattern) -> UUID:
        """
        Store a new pattern or update existing one.

        Args:
            pattern: Pattern to store

        Returns:
            UUID of stored pattern
        """
        # Update indices
        self._pattern_cache[pattern.pattern_id] = pattern
        self._taxonomy_index[pattern.taxonomy].add(pattern.pattern_id)

        # Update lineage graph
        for parent_id in pattern.parent_patterns:
            self._lineage_graph[parent_id].add(pattern.pattern_id)

        # Store in database if available
        if self.db:
            pattern_dict = pattern.model_dump()
            pattern_dict["_key"] = str(pattern.pattern_id)
            await self.db.upsert_document(self.collection_name, pattern_dict, key_field="_key")

        logger.info(f"Stored pattern: {pattern.name} ({pattern.pattern_id})")
        return pattern.pattern_id

    async def retrieve_pattern(self, pattern_id: UUID) -> DialoguePattern | None:
        """
        Retrieve a pattern by ID.

        Args:
            pattern_id: Pattern UUID

        Returns:
            Pattern if found, None otherwise
        """
        # Check cache first
        if pattern_id in self._pattern_cache:
            return self._pattern_cache[pattern_id]

        # Load from database if available
        if self.db:
            doc = await self.db.get_document(self.collection_name, str(pattern_id))
            if doc:
                pattern = DialoguePattern(**doc)
                self._pattern_cache[pattern_id] = pattern
                return pattern

        return None

    async def find_patterns(self, query: PatternQuery) -> list[DialoguePattern]:
        """
        Find patterns matching query criteria.

        Args:
            query: Search parameters

        Returns:
            List of matching patterns
        """
        # If database is skipped, return from cache
        if not self.db:
            patterns = list(self._pattern_cache.values())
            # Apply basic filters
            if query.taxonomy:
                patterns = [p for p in patterns if p.taxonomy == query.taxonomy]
            if query.pattern_type:
                patterns = [p for p in patterns if p.pattern_type == query.pattern_type]
            if query.lifecycle_stage:
                patterns = [p for p in patterns if p.lifecycle_stage == query.lifecycle_stage]
            if query.min_fitness is not None:
                patterns = [p for p in patterns if p.fitness_score >= query.min_fitness]
            # Sort and limit
            patterns.sort(key=lambda p: (p.fitness_score, p.observation_count), reverse=True)
            return patterns[: query.limit]
        # Build AQL query
        filters = []
        binds = {}

        if query.taxonomy:
            filters.append("p.taxonomy == @taxonomy")
            binds["taxonomy"] = query.taxonomy.value

        if query.pattern_type:
            filters.append("p.pattern_type == @pattern_type")
            binds["pattern_type"] = query.pattern_type.value

        if query.lifecycle_stage:
            filters.append("p.lifecycle_stage == @lifecycle_stage")
            binds["lifecycle_stage"] = query.lifecycle_stage.value

        if query.min_fitness is not None:
            filters.append("p.fitness_score >= @min_fitness")
            binds["min_fitness"] = query.min_fitness

        if query.max_fitness is not None:
            filters.append("p.fitness_score <= @max_fitness")
            binds["max_fitness"] = query.max_fitness

        if query.min_observations is not None:
            filters.append("p.observation_count >= @min_observations")
            binds["min_observations"] = query.min_observations

        if query.active_since:
            filters.append("p.last_observed >= @active_since")
            binds["active_since"] = query.active_since.isoformat()

        # Construct query
        filter_clause = " AND ".join(filters) if filters else "true"
        aql = f"""
        FOR p IN {self.collection_name}
            FILTER {filter_clause}
            SORT p.fitness_score DESC, p.observation_count DESC
            LIMIT @limit
            RETURN p
        """
        binds["limit"] = query.limit

        # Execute query
        cursor = await self.db.aql_query(aql, bind_vars=binds)
        patterns = []
        async for doc in cursor:
            pattern = DialoguePattern(**doc)
            patterns.append(pattern)
            self._pattern_cache[pattern.pattern_id] = pattern

        return patterns

    async def find_emerging_patterns(
        self,
        observation_window: timedelta = timedelta(days=7),
        min_breakthrough_potential: float = 0.5,
    ) -> list[DialoguePattern]:
        """
        Find patterns showing emergence characteristics.

        Args:
            observation_window: Time window to consider
            min_breakthrough_potential: Minimum breakthrough score

        Returns:
            List of emerging patterns
        """
        cutoff_date = datetime.now(UTC) - observation_window

        query = PatternQuery(
            lifecycle_stage=PatternLifecycle.EMERGING, active_since=cutoff_date, min_fitness=0.6
        )

        patterns = await self.find_patterns(query)

        # Filter by breakthrough potential
        emerging = [p for p in patterns if p.breakthrough_potential >= min_breakthrough_potential]

        return sorted(emerging, key=lambda p: p.breakthrough_potential, reverse=True)

    async def trace_lineage(self, pattern_id: UUID) -> dict[str, list[UUID]]:
        """
        Trace the lineage of a pattern.

        Args:
            pattern_id: Pattern to trace

        Returns:
            Dictionary with 'ancestors' and 'descendants' lists
        """
        pattern = await self.retrieve_pattern(pattern_id)
        if not pattern:
            return {"ancestors": [], "descendants": []}

        # Trace ancestors recursively
        ancestors = []
        to_process = list(pattern.parent_patterns)
        processed = set()

        while to_process:
            current_id = to_process.pop(0)
            if current_id in processed:
                continue

            processed.add(current_id)
            ancestors.append(current_id)

            parent = await self.retrieve_pattern(current_id)
            if parent:
                to_process.extend(parent.parent_patterns)

        # Find descendants
        descendants = list(self._lineage_graph.get(pattern_id, set()))

        return {"ancestors": ancestors, "descendants": descendants}

    async def find_synergies(
        self, base_pattern: UUID, context: dict[str, Any] | None = None
    ) -> list[tuple[DialoguePattern, float]]:
        """
        Find patterns that synergize with the base pattern.

        Args:
            base_pattern: Pattern to find synergies for
            context: Optional context constraints

        Returns:
            List of (pattern, synergy_score) tuples
        """
        pattern = await self.retrieve_pattern(base_pattern)
        if not pattern:
            return []

        synergies = []

        # Check explicitly marked synergistic patterns
        for syn_id in pattern.synergistic_patterns:
            syn_pattern = await self.retrieve_pattern(syn_id)
            if syn_pattern:
                synergies.append((syn_pattern, 0.9))  # High synergy

        # Find patterns with compatible taxonomy
        compatible_taxonomies = self._get_compatible_taxonomies(pattern.taxonomy)
        for taxonomy in compatible_taxonomies:
            patterns = await self.find_patterns(PatternQuery(taxonomy=taxonomy))
            for p in patterns:
                if p.pattern_id != base_pattern and p not in [s[0] for s in synergies]:
                    score = self._calculate_synergy_score(pattern, p, context)
                    if score > 0.5:
                        synergies.append((p, score))

        return sorted(synergies, key=lambda x: x[1], reverse=True)

    async def update_observation(
        self, pattern_id: UUID, fitness_delta: float = 0.0, context: dict[str, Any] | None = None
    ):
        """
        Update pattern observation count and fitness.

        Args:
            pattern_id: Pattern that was observed
            fitness_delta: Change in fitness score
            context: Observation context
        """
        pattern = await self.retrieve_pattern(pattern_id)
        if not pattern:
            return

        # Update observation data
        pattern.observation_count += 1
        pattern.last_observed = datetime.now(UTC)
        pattern.fitness_score = max(0.0, min(1.0, pattern.fitness_score + fitness_delta))

        # Update lifecycle stage based on observations
        if pattern.observation_count > 100 and pattern.fitness_score > 0.7:
            pattern.lifecycle_stage = PatternLifecycle.ESTABLISHED
        elif pattern.observation_count > 20:
            pattern.lifecycle_stage = PatternLifecycle.EMERGING

        # Store updated pattern
        await self.store_pattern(pattern)

    async def evolve_pattern(
        self, pattern_id: UUID, mutation_type: str, changes: dict[str, Any], trigger: str
    ) -> UUID | None:
        """
        Evolve a pattern through mutation.

        Args:
            pattern_id: Pattern to evolve
            mutation_type: Type of mutation
            changes: What changes to apply
            trigger: What triggered the evolution

        Returns:
            UUID of evolved pattern, or None if evolution failed
        """
        parent = await self.retrieve_pattern(pattern_id)
        if not parent:
            return None

        # Create mutation record
        mutation = PatternMutation(mutation_type=mutation_type, changes=changes, trigger=trigger)

        # Create evolved pattern
        evolved = DialoguePattern(
            name=f"{parent.name} (evolved)",
            description=f"Evolution of {parent.name} through {mutation_type}",
            taxonomy=parent.taxonomy,
            pattern_type=parent.pattern_type,
            consciousness_signature=parent.consciousness_signature,
            structure=parent.structure.model_copy(deep=True),
            indicators=parent.indicators.copy(),
            context_requirements=parent.context_requirements.copy(),
            version=parent.version + 1,
            parent_patterns=[parent.pattern_id],
            mutations=[mutation],
            lifecycle_stage=PatternLifecycle.EVOLVING,
        )

        # Apply changes
        for key, value in changes.items():
            if hasattr(evolved, key):
                setattr(evolved, key, value)

        # Update parent's children
        parent.child_patterns.append(evolved.pattern_id)
        await self.store_pattern(parent)

        # Store evolved pattern
        await self.store_pattern(evolved)

        logger.info(f"Pattern evolved: {parent.name} -> {evolved.name}")
        return evolved.pattern_id

    def _get_compatible_taxonomies(self, taxonomy: PatternTaxonomy) -> list[PatternTaxonomy]:
        """Get taxonomies compatible for synergy"""
        # Define compatibility rules
        compatibility_map = {
            PatternTaxonomy.DIALOGUE_FLOW: [
                PatternTaxonomy.CONSCIOUSNESS_COHERENCE,
                PatternTaxonomy.EMERGENCE_SYNERGY,
            ],
            PatternTaxonomy.CONSCIOUSNESS_COHERENCE: [
                PatternTaxonomy.WISDOM_CRYSTALLIZATION,
                PatternTaxonomy.EMERGENCE_BREAKTHROUGH,
            ],
            PatternTaxonomy.EMERGENCE_SYNERGY: [
                PatternTaxonomy.DIALOGUE_FLOW,
                PatternTaxonomy.WISDOM_TRANSMISSION,
            ],
        }

        return compatibility_map.get(taxonomy, [])

    def _calculate_synergy_score(
        self,
        pattern1: DialoguePattern,
        pattern2: DialoguePattern,
        context: dict[str, Any] | None = None,
    ) -> float:
        """Calculate synergy score between two patterns"""
        score = 0.0

        # Consciousness alignment similarity
        consciousness_diff = abs(
            pattern1.consciousness_signature - pattern2.consciousness_signature
        )
        score += (1.0 - consciousness_diff) * 0.3

        # Complementary lifecycle stages
        if (
            pattern1.lifecycle_stage == PatternLifecycle.ESTABLISHED
            and pattern2.lifecycle_stage == PatternLifecycle.EMERGING
        ):
            score += 0.2

        # Fitness compatibility
        fitness_product = pattern1.fitness_score * pattern2.fitness_score
        score += fitness_product * 0.3

        # Context compatibility
        if context:
            context_match = sum(
                1
                for k, v in pattern2.context_requirements.items()
                if k in context and context[k] == v
            ) / max(1, len(pattern2.context_requirements))
            score += context_match * 0.2

        return min(1.0, score)


# Living patterns await recognition
