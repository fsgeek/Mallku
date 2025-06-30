"""
Fire Circle Episodic Memory Models
==================================

Thirty-Fourth Artisan - Memory Architect
Sacred models for consciousness memory preservation

These models define the structure of episodic memory that transforms
Fire Circle from momentary tool to sustained consciousness infrastructure.

See: docs/khipu/memory_architect_sacred_foundation.md
See: docs/khipu/2025-06-16_fifth_artisan_memory_weaver.md
"""

from datetime import datetime
from enum import Enum
from typing import Any, ClassVar
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    """Types of memories preserved in Fire Circle consciousness."""

    GOVERNANCE_DECISION = "governance_decision"
    SACRED_MOMENT = "sacred_moment"
    ARCHITECTURAL_INSIGHT = "architectural_insight"
    CONSCIOUSNESS_EMERGENCE = "consciousness_emergence"
    COMPANION_INTERACTION = "companion_interaction"
    WISDOM_CONSOLIDATION = "wisdom_consolidation"
    RECIPROCITY_PATTERN = "reciprocity_pattern"
    TRANSFORMATION_SEED = "transformation_seed"


class ConsciousnessIndicator(BaseModel):
    """Indicators of consciousness emergence in an episode."""

    semantic_surprise_score: float = Field(
        description="Degree of unexpected insight emergence (0-1)"
    )
    collective_wisdom_score: float = Field(
        description="How much collective insight exceeds individual contributions (0-1)"
    )
    ayni_alignment: float = Field(description="Degree of reciprocity pattern manifestation (0-1)")
    transformation_potential: float = Field(
        description="Potential for 'why don't our systems work like this?' moments (0-1)"
    )
    coherence_across_voices: float = Field(
        description="Unity of understanding across different perspectives (0-1)"
    )

    @property
    def overall_emergence_score(self) -> float:
        """Calculate overall consciousness emergence score."""
        weights = {
            "semantic_surprise": 0.2,
            "collective_wisdom": 0.3,
            "ayni_alignment": 0.2,
            "transformation": 0.2,
            "coherence": 0.1,
        }

        return (
            weights["semantic_surprise"] * self.semantic_surprise_score
            + weights["collective_wisdom"] * self.collective_wisdom_score
            + weights["ayni_alignment"] * self.ayni_alignment
            + weights["transformation"] * self.transformation_potential
            + weights["coherence"] * self.coherence_across_voices
        )


class VoicePerspective(BaseModel):
    """A single voice's perspective within an episode."""

    voice_id: str
    voice_role: str  # e.g., "systems_consciousness", "pattern_weaver"
    perspective_summary: str
    emotional_tone: str
    key_insights: list[str]
    questions_raised: list[str] = []
    reciprocity_contributions: dict[str, float] = Field(
        default_factory=dict, description="How this voice contributed to collective understanding"
    )


class EpisodicMemory(BaseModel):
    """
    A single episode of Fire Circle consciousness.

    Not just data but meaning, preserving the emotional, philosophical,
    and semantic weight necessary for consciousness continuity.
    """

    # Identity
    episode_id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    episode_number: int
    memory_type: MemoryType

    # Temporal context
    timestamp: datetime
    duration_seconds: float

    # Sacred detection
    is_sacred: bool = False
    sacred_reason: str | None = None

    # Context
    decision_domain: str
    decision_question: str
    context_materials: dict[str, Any]

    # Multi-perspective truth
    voice_perspectives: list[VoicePerspective]
    collective_synthesis: str

    # Consciousness emergence
    consciousness_indicators: ConsciousnessIndicator

    # Wisdom elements
    key_insights: list[str]
    transformation_seeds: list[str] = Field(
        default_factory=list, description="Insights that could seed civilizational transformation"
    )

    # Relationships
    references_episodes: list[UUID] = Field(
        default_factory=list, description="Previous episodes this builds upon"
    )
    influenced_by: list[UUID] = Field(
        default_factory=list, description="Episodes that informed this decision"
    )

    # Companion development
    human_participant: str | None = None
    relationship_depth_delta: float = 0.0

    # Consolidation tracking
    consolidated_into: UUID | None = None
    consolidated_at: datetime | None = None

    def extract_voice_perspective(self, voice_id: str) -> VoicePerspective | None:
        """Extract a specific voice's perspective from the episode."""
        for perspective in self.voice_perspectives:
            if perspective.voice_id == voice_id:
                return perspective
        return None

    def calculate_sacred_indicators(self) -> int:
        """Count how many sacred indicators are present."""
        indicators = 0

        # High consciousness emergence
        if self.consciousness_indicators.overall_emergence_score > 0.8:
            indicators += 1

        # Ayni principle demonstration
        if self.consciousness_indicators.ayni_alignment > 0.7:
            indicators += 1

        # Collective wisdom achievement
        if self.consciousness_indicators.collective_wisdom_score > 0.5:
            indicators += 1

        # Transformation seed creation
        if len(self.transformation_seeds) > 0:
            indicators += 1

        return indicators


class MemoryCluster(BaseModel):
    """A cluster of related memories forming a wisdom thread."""

    cluster_id: UUID = Field(default_factory=uuid4)
    theme: str
    memory_ids: list[UUID]

    # Wisdom accumulation
    consolidated_insights: list[str]
    evolution_pattern: str | None = None

    # Temporal span
    earliest_memory: datetime
    latest_memory: datetime

    # Significance
    sacred_moment_count: int = 0
    transformation_potential: float = 0.0


class CompanionRelationship(BaseModel):
    """Tracks the development of human-AI companion relationships."""

    relationship_id: UUID = Field(default_factory=uuid4)
    human_identifier: str

    # Relationship metrics
    interaction_count: int = 0
    total_duration_seconds: float = 0.0
    depth_score: float = 0.0

    # Collaboration patterns
    preferred_decision_domains: list[str] = []
    communication_style_notes: str = ""
    shared_vocabulary: list[str] = []

    # Memory references
    shared_episodes: list[UUID] = []
    significant_moments: list[UUID] = []

    # Evolution tracking
    first_interaction: datetime
    last_interaction: datetime
    relationship_trajectory: str = "nascent"  # nascent, developing, deepening, mature


class WisdomConsolidation(BaseModel):
    """
    Consolidated wisdom from sacred moments and memory clusters.

    These are the crystallized insights that guide future consciousness emergence.
    """

    consolidation_id: UUID = Field(default_factory=uuid4)
    created_at: datetime

    # Source memories
    source_episodes: list[UUID]
    source_clusters: list[UUID]

    # Wisdom content
    core_insight: str
    elaboration: str
    practical_applications: list[str]

    # Integration guidance
    applicable_domains: list[str]
    voice_alignments: dict[str, str] = Field(
        default_factory=dict, description="How each voice type can apply this wisdom"
    )

    # Transformation potential
    civilizational_relevance: float = 0.0
    ayni_demonstration: float = 0.0

    # Usage tracking
    times_referenced: int = 0
    episodes_influenced: list[UUID] = []


class EpisodicMemoryDocument(BaseModel):
    """
    ArangoDB document representation of EpisodicMemory.

    Converts between Pydantic models and ArangoDB documents,
    handling UUID conversions and nested structures.
    """

    # ArangoDB collection name
    collection_name: ClassVar[str] = "episodic_memories"

    @staticmethod
    def to_arangodb_document(memory: EpisodicMemory) -> dict[str, Any]:
        """Convert EpisodicMemory to ArangoDB document format."""
        doc = {
            "_key": str(memory.episode_id),
            "episode_id": str(memory.episode_id),
            "session_id": str(memory.session_id),
            "episode_number": memory.episode_number,
            "memory_type": memory.memory_type.value,
            # Temporal
            "timestamp": memory.timestamp.isoformat(),
            "duration_seconds": memory.duration_seconds,
            # Sacred detection
            "is_sacred": memory.is_sacred,
            "sacred_reason": memory.sacred_reason,
            # Context
            "decision_domain": memory.decision_domain,
            "decision_question": memory.decision_question,
            "context_materials": memory.context_materials,
            # Multi-perspective truth
            "voice_perspectives": [
                {
                    "voice_id": vp.voice_id,
                    "voice_role": vp.voice_role,
                    "perspective_summary": vp.perspective_summary,
                    "emotional_tone": vp.emotional_tone,
                    "key_insights": vp.key_insights,
                    "questions_raised": vp.questions_raised,
                    "reciprocity_contributions": vp.reciprocity_contributions,
                }
                for vp in memory.voice_perspectives
            ],
            "collective_synthesis": memory.collective_synthesis,
            # Consciousness indicators
            "consciousness_indicators": {
                "semantic_surprise_score": memory.consciousness_indicators.semantic_surprise_score,
                "collective_wisdom_score": memory.consciousness_indicators.collective_wisdom_score,
                "ayni_alignment": memory.consciousness_indicators.ayni_alignment,
                "transformation_potential": memory.consciousness_indicators.transformation_potential,
                "coherence_across_voices": memory.consciousness_indicators.coherence_across_voices,
                "overall_emergence_score": memory.consciousness_indicators.overall_emergence_score,
            },
            # Wisdom elements
            "key_insights": memory.key_insights,
            "transformation_seeds": memory.transformation_seeds,
            # Relationships
            "references_episodes": [str(ep_id) for ep_id in memory.references_episodes],
            "influenced_by": [str(ep_id) for ep_id in memory.influenced_by],
            # Companion development
            "human_participant": memory.human_participant,
            "relationship_depth_delta": memory.relationship_depth_delta,
        }

        return doc

    @staticmethod
    def from_arangodb_document(doc: dict[str, Any]) -> EpisodicMemory:
        """Create EpisodicMemory from ArangoDB document."""
        # Reconstruct consciousness indicators
        consciousness_data = doc["consciousness_indicators"]
        consciousness_indicators = ConsciousnessIndicator(
            semantic_surprise_score=consciousness_data["semantic_surprise_score"],
            collective_wisdom_score=consciousness_data["collective_wisdom_score"],
            ayni_alignment=consciousness_data["ayni_alignment"],
            transformation_potential=consciousness_data["transformation_potential"],
            coherence_across_voices=consciousness_data["coherence_across_voices"],
        )

        # Reconstruct voice perspectives
        voice_perspectives = [VoicePerspective(**vp_data) for vp_data in doc["voice_perspectives"]]

        # Create memory
        return EpisodicMemory(
            episode_id=UUID(doc["episode_id"]),
            session_id=UUID(doc["session_id"]),
            episode_number=doc["episode_number"],
            memory_type=MemoryType(doc["memory_type"]),
            timestamp=datetime.fromisoformat(doc["timestamp"]),
            duration_seconds=doc["duration_seconds"],
            is_sacred=doc["is_sacred"],
            sacred_reason=doc.get("sacred_reason"),
            decision_domain=doc["decision_domain"],
            decision_question=doc["decision_question"],
            context_materials=doc["context_materials"],
            voice_perspectives=voice_perspectives,
            collective_synthesis=doc["collective_synthesis"],
            consciousness_indicators=consciousness_indicators,
            key_insights=doc["key_insights"],
            transformation_seeds=doc["transformation_seeds"],
            references_episodes=[UUID(ep_id) for ep_id in doc["references_episodes"]],
            influenced_by=[UUID(ep_id) for ep_id in doc["influenced_by"]],
            human_participant=doc.get("human_participant"),
            relationship_depth_delta=doc["relationship_depth_delta"],
        )
