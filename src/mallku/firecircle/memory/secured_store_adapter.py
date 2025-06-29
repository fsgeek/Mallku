"""
Secured Store Adapter
=====================

Fortieth Artisan - Production Hardening
Adapter between async secured store and sync memory API

This adapter allows the async SecuredDatabaseMemoryStore to work
with the existing synchronous memory store interface.
"""

import asyncio
import logging
from collections.abc import Callable
from functools import wraps
from typing import Any
from uuid import UUID

from .models import EpisodicMemory, MemoryCluster, WisdomConsolidation
from .secured_database_store import SecuredDatabaseMemoryStore
from .secured_memory_models import SecuredEpisodicMemory

logger = logging.getLogger(__name__)


def run_async(async_func: Callable) -> Callable:
    """Decorator to run async function in sync context."""

    @wraps(async_func)
    def wrapper(*args, **kwargs):
        try:
            # Try to get existing event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We're already in an async context
                # Create a task and run it
                future = asyncio.ensure_future(async_func(*args, **kwargs))
                # This is tricky - we need to block but we're in an async loop
                # Use nest_asyncio if available
                try:
                    import nest_asyncio

                    nest_asyncio.apply()
                    return loop.run_until_complete(future)
                except ImportError:
                    # Fall back to creating new thread
                    import concurrent.futures

                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, async_func(*args, **kwargs))
                        return future.result()
            else:
                # No running loop, safe to use run_until_complete
                return loop.run_until_complete(async_func(*args, **kwargs))
        except RuntimeError:
            # No event loop, create one
            return asyncio.run(async_func(*args, **kwargs))

    return wrapper


class SecuredStoreAdapter:
    """
    Adapter that makes SecuredDatabaseMemoryStore compatible with sync interface.

    This allows the production-ready secured store to work with the existing
    memory service without breaking API compatibility.
    """

    def __init__(self, enable_sacred_detection: bool = True):
        """Initialize the adapter with a secured store."""
        self._secured_store = SecuredDatabaseMemoryStore(
            enable_sacred_detection=enable_sacred_detection
        )
        self._initialized = False

        # Expose indices for compatibility
        self.memories_by_session = self._secured_store.memories_by_session
        self.memories_by_type = self._secured_store.memories_by_type
        self.memories_by_domain = self._secured_store.memories_by_domain
        self.sacred_memories = self._secured_store.sacred_memories

        # Initialize in background
        self._ensure_initialized()

    @run_async
    async def _ensure_initialized(self):
        """Ensure the secured store is initialized."""
        if not self._initialized:
            await self._secured_store.initialize()
            self._initialized = True

    @run_async
    async def store_episode(self, memory: EpisodicMemory) -> UUID:
        """Store an episodic memory (sync wrapper)."""
        await self._ensure_initialized()

        # Convert to secured model
        secured_memory = self._convert_to_secured(memory)

        # Store through secured interface
        return await self._secured_store.store_episode(secured_memory)

    @run_async
    async def retrieve_by_context(
        self,
        domain: str,
        context_materials: dict[str, Any],
        requesting_voice: str | None = None,
        limit: int = 10,
    ) -> list[EpisodicMemory]:
        """Retrieve memories by context (sync wrapper)."""
        await self._ensure_initialized()

        secured_memories = await self._secured_store.retrieve_by_context(
            domain, context_materials, requesting_voice, limit
        )

        # Convert back to regular models for compatibility
        return [self._convert_from_secured(m) for m in secured_memories]

    @run_async
    async def retrieve_sacred_moments(
        self, domain: str | None = None, limit: int | None = None
    ) -> list[EpisodicMemory]:
        """Retrieve sacred moments (sync wrapper)."""
        await self._ensure_initialized()

        secured_memories = await self._secured_store.retrieve_sacred_moments(domain, limit)
        return [self._convert_from_secured(m) for m in secured_memories]

    @run_async
    async def retrieve_companion_memories(
        self, human_identifier: str, limit: int = 20
    ) -> list[EpisodicMemory]:
        """Retrieve companion memories (sync wrapper)."""
        await self._ensure_initialized()

        secured_memories = await self._secured_store.retrieve_companion_memories(
            human_identifier, limit
        )
        return [self._convert_from_secured(m) for m in secured_memories]

    @run_async
    async def create_memory_cluster(self, theme: str, memory_ids: list[UUID]) -> MemoryCluster:
        """Create memory cluster (sync wrapper)."""
        await self._ensure_initialized()

        secured_cluster = await self._secured_store.create_memory_cluster(theme, memory_ids)

        # Convert to regular model
        return MemoryCluster(
            cluster_id=secured_cluster.cluster_id,
            theme=secured_cluster.theme,
            memory_ids=secured_cluster.memory_ids,
            consolidated_insights=secured_cluster.consolidated_insights,
            evolution_pattern=secured_cluster.evolution_pattern,
            earliest_memory=secured_cluster.earliest_memory,
            latest_memory=secured_cluster.latest_memory,
            sacred_moment_count=secured_cluster.sacred_moment_count,
            transformation_potential=secured_cluster.transformation_potential,
        )

    @run_async
    async def consolidate_wisdom(
        self, source_episodes: list[UUID], source_clusters: list[UUID] | None = None
    ) -> WisdomConsolidation:
        """Consolidate wisdom (sync wrapper)."""
        await self._ensure_initialized()

        secured_wisdom = await self._secured_store.consolidate_wisdom(
            source_episodes, source_clusters
        )

        # Convert to regular model
        return WisdomConsolidation(
            consolidation_id=secured_wisdom.consolidation_id,
            created_at=secured_wisdom.created_at,
            source_episodes=secured_wisdom.source_episodes,
            source_clusters=secured_wisdom.source_clusters,
            core_insight=secured_wisdom.core_insight,
            elaboration=secured_wisdom.elaboration,
            practical_applications=secured_wisdom.practical_applications,
            applicable_domains=secured_wisdom.applicable_domains,
            voice_alignments=secured_wisdom.voice_alignments,
            civilizational_relevance=secured_wisdom.civilizational_relevance,
            ayni_demonstration=secured_wisdom.ayni_demonstration,
            times_referenced=secured_wisdom.times_referenced,
            episodes_influenced=secured_wisdom.episodes_influenced,
        )

    @run_async
    async def get_memory_stats(self) -> dict[str, Any]:
        """Get memory statistics (sync wrapper)."""
        await self._ensure_initialized()
        return await self._secured_store.get_memory_stats()

    def _convert_to_secured(self, memory: EpisodicMemory) -> SecuredEpisodicMemory:
        """Convert regular memory to secured model."""
        # Create secured version with all fields
        return SecuredEpisodicMemory(
            episode_id=memory.episode_id,
            session_id=memory.session_id,
            episode_number=memory.episode_number,
            timestamp=memory.timestamp,
            decision_question=memory.decision_question,
            decision_domain=memory.decision_domain,
            collective_synthesis=memory.collective_synthesis,
            memory_type=memory.memory_type,
            duration_seconds=memory.duration_seconds,
            human_participant=memory.human_participant,
            consciousness_indicators=memory.consciousness_indicators,
            voice_perspectives=memory.voice_perspectives,
            key_insights=memory.key_insights,
            transformation_seeds=memory.transformation_seeds,
            is_sacred=memory.is_sacred,
            sacred_reason=memory.sacred_reason,
        )

    def _convert_from_secured(self, secured: SecuredEpisodicMemory) -> EpisodicMemory:
        """Convert secured model back to regular memory."""
        return EpisodicMemory(
            episode_id=secured.episode_id,
            session_id=secured.session_id,
            episode_number=secured.episode_number,
            timestamp=secured.timestamp,
            decision_question=secured.decision_question,
            decision_domain=secured.decision_domain,
            collective_synthesis=secured.collective_synthesis,
            memory_type=secured.memory_type,
            duration_seconds=secured.duration_seconds,
            human_participant=secured.human_participant,
            consciousness_indicators=secured.consciousness_indicators,
            voice_perspectives=secured.voice_perspectives,
            key_insights=secured.key_insights,
            transformation_seeds=secured.transformation_seeds,
            is_sacred=secured.is_sacred,
            sacred_reason=secured.sacred_reason,
        )
