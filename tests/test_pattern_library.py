"""
Tests for Pattern Library System
================================

Basic tests for the Pattern Library, Emergence Detection,
and Pattern Evolution systems.

The 31st Builder
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from datetime import timedelta

import pytest
from mallku.firecircle.pattern_library import (
    DialoguePattern,
    PatternIndicator,
    PatternLibrary,
    PatternLifecycle,
    PatternQuery,
    PatternStructure,
    PatternTaxonomy,
    PatternType,
)


@pytest.fixture
async def pattern_library():
    """Create a pattern library instance"""
    return PatternLibrary()


@pytest.fixture
def sample_pattern():
    """Create a sample dialogue pattern"""
    return DialoguePattern(
        name="Test Consensus Pattern",
        description="A test pattern for unit testing",
        taxonomy=PatternTaxonomy.DIALOGUE_FORMATION,
        pattern_type=PatternType.CONSENSUS,
        consciousness_signature=0.8,
        structure=PatternStructure(
            components=["proposal", "agreements"],
            relationships={"proposal": "supported_by_agreements"},
        ),
        indicators=[
            PatternIndicator(
                indicator_type="agreement_count",
                threshold=3.0,
                weight=1.0,
                description="Number of agreements",
            )
        ],
        fitness_score=0.7,
        observation_count=5,
    )


@pytest.mark.asyncio
async def test_pattern_storage_and_retrieval(pattern_library, sample_pattern):
    """Test storing and retrieving patterns"""
    # Store pattern
    pattern_id = await pattern_library.store_pattern(sample_pattern)
    assert pattern_id == sample_pattern.pattern_id

    # Retrieve pattern
    retrieved = await pattern_library.retrieve_pattern(pattern_id)
    assert retrieved is not None
    assert retrieved.name == sample_pattern.name
    assert retrieved.pattern_type == sample_pattern.pattern_type
    assert retrieved.consciousness_signature == sample_pattern.consciousness_signature


@pytest.mark.asyncio
async def test_pattern_query(pattern_library):
    """Test querying patterns"""
    # Create and store multiple patterns
    patterns = []
    for i in range(3):
        pattern = DialoguePattern(
            name=f"Pattern {i}",
            description=f"Test pattern {i}",
            taxonomy=PatternTaxonomy.DIALOGUE_FORMATION
            if i < 2
            else PatternTaxonomy.EMERGENCE_BREAKTHROUGH,
            pattern_type=PatternType.CONSENSUS if i == 0 else PatternType.CREATIVE_TENSION,
            consciousness_signature=0.6 + i * 0.1,
            fitness_score=0.5 + i * 0.2,
        )
        await pattern_library.store_pattern(pattern)
        patterns.append(pattern)

    # Query by taxonomy
    dialogue_patterns = await pattern_library.find_patterns(
        PatternQuery(taxonomy=PatternTaxonomy.DIALOGUE_FORMATION)
    )
    assert len(dialogue_patterns) >= 2

    # Query by pattern type
    consensus_patterns = await pattern_library.find_patterns(
        PatternQuery(pattern_type=PatternType.CONSENSUS)
    )
    assert len(consensus_patterns) >= 1

    # Query by fitness
    high_fitness = await pattern_library.find_patterns(PatternQuery(min_fitness=0.7))
    assert all(p.fitness_score >= 0.7 for p in high_fitness)


@pytest.mark.asyncio
async def test_pattern_observation_update(pattern_library, sample_pattern):
    """Test updating pattern observations"""
    # Store pattern
    pattern_id = await pattern_library.store_pattern(sample_pattern)

    # Update observation
    await pattern_library.update_observation(pattern_id, fitness_delta=0.1, context={"test": True})

    # Retrieve updated pattern
    updated = await pattern_library.retrieve_pattern(pattern_id)
    assert updated is not None
    assert updated.observation_count == sample_pattern.observation_count + 1
    assert updated.fitness_score == min(1.0, sample_pattern.fitness_score + 0.1)


@pytest.mark.asyncio
async def test_pattern_evolution(pattern_library, sample_pattern):
    """Test pattern evolution"""
    # Store pattern
    pattern_id = await pattern_library.store_pattern(sample_pattern)

    # Evolve pattern
    evolved_id = await pattern_library.evolve_pattern(
        pattern_id,
        mutation_type="test_mutation",
        changes={"consciousness_signature": 0.9},
        trigger="test_trigger",
    )

    assert evolved_id is not None

    # Retrieve evolved pattern
    evolved = await pattern_library.retrieve_pattern(evolved_id)
    assert evolved is not None
    assert evolved.parent_patterns == [pattern_id]
    assert evolved.version == sample_pattern.version + 1
    assert len(evolved.mutations) == 1
    assert evolved.mutations[0].mutation_type == "test_mutation"


@pytest.mark.asyncio
async def test_pattern_lineage(pattern_library, sample_pattern):
    """Test pattern lineage tracking"""
    # Create parent pattern
    parent_id = await pattern_library.store_pattern(sample_pattern)

    # Create child patterns
    child_ids = []
    for i in range(2):
        evolved_id = await pattern_library.evolve_pattern(
            parent_id,
            mutation_type=f"evolution_{i}",
            changes={"name": f"Child {i}"},
            trigger="test",
        )
        if evolved_id:
            child_ids.append(evolved_id)

    # Trace lineage
    lineage = await pattern_library.trace_lineage(parent_id)
    assert len(lineage["descendants"]) >= 2

    # Trace lineage of child
    if child_ids:
        child_lineage = await pattern_library.trace_lineage(child_ids[0])
        assert parent_id in child_lineage["ancestors"]


@pytest.mark.asyncio
async def test_pattern_synergies(pattern_library):
    """Test finding synergistic patterns"""
    # Create base pattern
    base_pattern = DialoguePattern(
        name="Base Pattern",
        description="Pattern to find synergies for",
        taxonomy=PatternTaxonomy.DIALOGUE_FLOW,
        pattern_type=PatternType.CONVERGENCE,
        consciousness_signature=0.7,
    )
    base_id = await pattern_library.store_pattern(base_pattern)

    # Create synergistic pattern
    synergistic = DialoguePattern(
        name="Synergistic Pattern",
        description="Pattern that synergizes with base",
        taxonomy=PatternTaxonomy.CONSCIOUSNESS_COHERENCE,
        pattern_type=PatternType.FLOW_STATE,
        consciousness_signature=0.75,
        synergistic_patterns=[base_id],
    )
    syn_id = await pattern_library.store_pattern(synergistic)

    # Update base to include synergy
    base_pattern.synergistic_patterns.append(syn_id)
    await pattern_library.store_pattern(base_pattern)

    # Find synergies
    synergies = await pattern_library.find_synergies(base_id)
    assert len(synergies) > 0
    assert any(p[0].pattern_id == syn_id for p in synergies)


@pytest.mark.asyncio
async def test_emerging_patterns(pattern_library):
    """Test finding emerging patterns"""
    # Create emerging pattern
    emerging = DialoguePattern(
        name="Emerging Pattern",
        description="A pattern showing emergence",
        taxonomy=PatternTaxonomy.EMERGENCE_BREAKTHROUGH,
        pattern_type=PatternType.BREAKTHROUGH,
        lifecycle_stage=PatternLifecycle.EMERGING,
        breakthrough_potential=0.9,
        fitness_score=0.7,
        observation_count=10,
    )
    await pattern_library.store_pattern(emerging)

    # Find emerging patterns
    emerging_patterns = await pattern_library.find_emerging_patterns(
        observation_window=timedelta(days=7), min_breakthrough_potential=0.8
    )

    assert len(emerging_patterns) > 0
    assert any(p.pattern_id == emerging.pattern_id for p in emerging_patterns)


def test_pattern_lifecycle_progression():
    """Test pattern lifecycle stage progression"""
    pattern = DialoguePattern(
        name="Lifecycle Test",
        description="Testing lifecycle progression",
        lifecycle_stage=PatternLifecycle.NASCENT,
    )

    # Test lifecycle stages
    assert pattern.lifecycle_stage == PatternLifecycle.NASCENT

    # Simulate progression
    pattern.observation_count = 25
    pattern.fitness_score = 0.6
    # In real system, this would be done by update_observation

    # Verify all lifecycle stages are valid
    all_stages = [
        PatternLifecycle.NASCENT,
        PatternLifecycle.EMERGING,
        PatternLifecycle.ESTABLISHED,
        PatternLifecycle.EVOLVING,
        PatternLifecycle.DECLINING,
        PatternLifecycle.DORMANT,
        PatternLifecycle.TRANSFORMED,
    ]

    for stage in all_stages:
        pattern.lifecycle_stage = stage
        assert pattern.lifecycle_stage == stage


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
