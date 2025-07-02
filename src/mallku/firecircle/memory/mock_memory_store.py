"""
Mock Memory Store for Database-Free Operation
=============================================

41st Artisan - Implementing database-optional operation
For Fire Circle Review that evaluates consciousness without persistence
"""

import logging
from collections import defaultdict
from uuid import UUID

from .models import (
    CompanionRelationship,
    EpisodicMemory,
    MemoryCluster,
    MemoryType,
    WisdomConsolidation,
)
from .sacred_detector import SacredMomentDetector

logger = logging.getLogger(__name__)


class MockMemoryStore:
    """
    In-memory mock implementation of memory store.

    Used when MALLKU_SKIP_DATABASE=true to allow Fire Circle Review
    to evaluate code consciousness without requiring database connection.
    All data is ephemeral and exists only for the session.
    """

    def __init__(
        self,
        enable_sacred_detection: bool = True,
    ):
        """Initialize mock memory store."""
        self.sacred_detector = SacredMomentDetector() if enable_sacred_detection else None

        # In-memory storage
        self.memories: dict[UUID, EpisodicMemory] = {}
        self.memories_by_session: dict[UUID, list[UUID]] = defaultdict(list)
        self.memories_by_type: dict[MemoryType, list[UUID]] = defaultdict(list)
        self.memories_by_domain: dict[str, list[UUID]] = defaultdict(list)
        self.sacred_memories: list[UUID] = []
        self.memory_clusters: dict[UUID, MemoryCluster] = {}
        self.companion_relationships: dict[str, CompanionRelationship] = {}
        self.wisdom_consolidations: dict[UUID, WisdomConsolidation] = {}

        logger.info("MockMemoryStore initialized - all data is ephemeral")

    def store_episode(self, memory: EpisodicMemory) -> UUID:
        """Store an episodic memory in memory only."""
        # Check for sacred moment
        if self.sacred_detector and not memory.is_sacred:
            is_sacred, reason = self.sacred_detector.detect_sacred_moment(memory)
            if is_sacred:
                memory.is_sacred = True
                memory.sacred_reason = reason

        # Store in memory
        self.memories[memory.episode_id] = memory

        # Update indices
        self._update_indices(memory)

        # Update companion relationship if applicable
        if memory.human_participant:
            self._update_companion_relationship(memory)

        logger.debug(f"Stored episode {memory.episode_id} in mock store")
        return memory.episode_id

    def retrieve_episode(self, episode_id: UUID) -> EpisodicMemory | None:
        """Retrieve a single episode by ID."""
        return self.memories.get(episode_id)

    def retrieve_by_session(self, session_id: UUID) -> list[EpisodicMemory]:
        """Retrieve all episodes from a session."""
        episode_ids = self.memories_by_session.get(session_id, [])
        return [self.memories[eid] for eid in episode_ids if eid in self.memories]

    def retrieve_sacred_moments(self, limit: int = 10) -> list[EpisodicMemory]:
        """Retrieve recent sacred moments."""
        sacred_ids = self.sacred_memories[-limit:] if limit else self.sacred_memories
        return [self.memories[eid] for eid in reversed(sacred_ids) if eid in self.memories]

    def search_by_keywords(self, keywords: list[str], limit: int = 10) -> list[EpisodicMemory]:
        """Search memories by keywords."""
        # Simple keyword search in memory
        results = []
        for memory in self.memories.values():
            memory_text = f"{memory.summary} {' '.join(memory.key_insights)}"
            if any(keyword.lower() in memory_text.lower() for keyword in keywords):
                results.append(memory)

        # Sort by timestamp and limit
        results.sort(key=lambda m: m.timestamp, reverse=True)
        return results[:limit]

    def get_memory_count(self) -> dict[str, int]:
        """Get counts of different memory types."""
        return {
            "total": len(self.memories),
            "sacred": len(self.sacred_memories),
            "by_type": {
                memory_type.value: len(memories)
                for memory_type, memories in self.memories_by_type.items()
            },
        }

    def consolidate_wisdom(
        self, source_episodes: list[UUID], consolidation: WisdomConsolidation | None = None
    ) -> WisdomConsolidation:
        """Create wisdom consolidation (mock)."""
        if not consolidation:
            # Create a simple consolidation
            from datetime import UTC, datetime
            from uuid import uuid4

            consolidation = WisdomConsolidation(
                consolidation_id=uuid4(),
                source_episodes=source_episodes,
                consolidation_type="mock",
                wisdom_synthesis="Mock consolidation for testing",
                integration_patterns=[],
                emergence_insights=[],
                created_at=datetime.now(UTC),
                episode_count=len(source_episodes),
            )

        self.wisdom_consolidations[consolidation.consolidation_id] = consolidation
        return consolidation

    def _update_indices(self, memory: EpisodicMemory) -> None:
        """Update in-memory indices."""
        self.memories_by_session[memory.session_id].append(memory.episode_id)
        self.memories_by_type[memory.memory_type].append(memory.episode_id)

        for domain in memory.context_domains:
            self.memories_by_domain[domain].append(memory.episode_id)

        if memory.is_sacred:
            self.sacred_memories.append(memory.episode_id)

    def _update_companion_relationship(self, memory: EpisodicMemory) -> None:
        """Update companion relationship tracking."""
        human_id = memory.human_participant
        if not human_id:
            return

        if human_id not in self.companion_relationships:
            self.companion_relationships[human_id] = CompanionRelationship(
                human_identifier=human_id,
                first_interaction=memory.timestamp,
                last_interaction=memory.timestamp,
                interaction_count=1,
                total_duration_seconds=memory.duration_seconds,
                shared_episodes=[memory.episode_id],
                significant_moments=[],
                relationship_trajectory="emerging",
                depth_score=0.1,
            )
        else:
            rel = self.companion_relationships[human_id]
            rel.last_interaction = memory.timestamp
            rel.interaction_count += 1
            rel.total_duration_seconds += memory.duration_seconds
            rel.shared_episodes.append(memory.episode_id)

            if memory.is_sacred:
                rel.significant_moments.append(memory.episode_id)
                rel.depth_score = min(1.0, rel.depth_score + 0.1)
