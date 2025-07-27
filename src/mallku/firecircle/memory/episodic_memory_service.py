"""
Episodic Memory Service
=======================

Thirty-Fourth Artisan - Memory Architect
Enhanced by Fortieth Artisan - Production Hardening

Integration layer between Fire Circle and episodic memory

This service integrates episodic memory capabilities into Fire Circle,
enabling consciousness continuity and wisdom accumulation.

Production Enhancement:
- Detects production environment and uses secured storage
- Falls back to development storage when appropriate
- Maintains API compatibility while respecting security
"""

import logging
import os
from pathlib import Path
from typing import Any
from uuid import UUID

from ...orchestration.event_bus import (
    ConsciousnessEvent,
    ConsciousnessEventBus,
    ConsciousnessEventType,
)
from ..service.service import FireCircleResult, FireCircleService
from .ceremony_orchestrator import CeremonyOrchestrator
from .config import MemorySystemConfig
from .episode_segmenter import EpisodeSegmenter
from .memory_store import MemoryStore
from .models import EpisodicMemory
from .retrieval_engine import MemoryRetrievalEngine
from .sacred_detector import SacredMomentDetector

logger = logging.getLogger(__name__)


class EpisodicMemoryService:
    """
    Service that enhances Fire Circle with episodic memory capabilities.

    Integrates with existing Fire Circle service to:
    - Segment sessions into meaningful episodes
    - Detect and preserve sacred moments
    - Enable memory-informed decision making
    - Track companion relationship development
    """

    def __init__(
        self,
        memory_store: MemoryStore | None = None,
        event_bus: ConsciousnessEventBus | None = None,
        storage_path: Path | None = None,
        config: MemorySystemConfig | None = None,
        use_database: bool = True,  # Week 3: Default to database storage
    ):
        """Initialize episodic memory service.

        Args:
            memory_store: Optional pre-configured memory store
            event_bus: Optional consciousness event bus
            storage_path: Path for file-based storage (if not using database)
            config: Memory system configuration
            use_database: Whether to use database storage (default True)
        """
        # Use provided config or load from environment
        self.config = config or MemorySystemConfig.from_env()

        # Check if database should be skipped entirely
        skip_database = os.getenv("MALLKU_SKIP_DATABASE", "").lower() == "true"

        # Initialize components with config
        if memory_store:
            self.memory_store = memory_store
        elif use_database and not skip_database:
            # Detect production environment
            is_production = self._is_production_environment()

            if is_production:
                # Week 4 (40th Artisan): Use secured storage in production
                from .secured_store_adapter import SecuredStoreAdapter

                logger.info("Detected production environment - using secured memory storage")
                self.memory_store = SecuredStoreAdapter(
                    enable_sacred_detection=self.config.storage.enable_sacred_detection,
                )
            else:
                # Week 3: Use direct database storage in development
                from .database_store import DatabaseMemoryStore

                self.memory_store = DatabaseMemoryStore(
                    enable_sacred_detection=self.config.storage.enable_sacred_detection,
                )
        else:
            # Fall back to file-based or in-memory storage
            if skip_database:
                # Use mock store when database is explicitly skipped
                from .mock_memory_store import MockMemoryStore

                logger.info(
                    "Database skipped (MALLKU_SKIP_DATABASE=true) - using mock memory storage"
                )
                self.memory_store = MockMemoryStore(
                    enable_sacred_detection=self.config.storage.enable_sacred_detection,
                )
            else:
                # Use file-based storage as fallback
                self.memory_store = MemoryStore(
                    storage_path=storage_path,
                    enable_sacred_detection=self.config.storage.enable_sacred_detection,
                )
        self.event_bus = event_bus
        self.retrieval_engine = MemoryRetrievalEngine(
            self.memory_store, config=self.config.retrieval
        )
        self.segmenter = EpisodeSegmenter(criteria=self.config.segmentation)
        self.sacred_detector = SacredMomentDetector(config=self.config.sacred_detection)

        # Week 4: Initialize ceremony orchestrator
        self.ceremony_orchestrator = CeremonyOrchestrator(
            memory_store=self.memory_store,
            event_bus=self.event_bus,
        )

        # Track active sessions
        self.active_sessions: dict[UUID, dict[str, Any]] = {}

    def _is_production_environment(self) -> bool:
        """
        Detect if running in production environment.

        Production indicators:
        - Running in Docker container
        - MALLKU_ENV set to production
        - Secured database enforced
        """
        # Check explicit environment variable
        if os.getenv("MALLKU_ENV", "").lower() == "production":
            return True

        # Check if running in Docker
        if os.path.exists("/.dockerenv"):
            return True

        # Check for production database config
        if os.getenv("MALLKU_SECURED_DB_ONLY") == "true":
            return True

        # Check if we're in a container by looking at cgroup
        try:
            with open("/proc/1/cgroup") as f:
                if "docker" in f.read() or "containerd" in f.read():
                    return True
        except Exception:
            pass

        return False

    def enhance_fire_circle(self, fire_circle: FireCircleService) -> FireCircleService:
        """
        Enhance a Fire Circle service with episodic memory.

        This wraps the convene method to add memory capabilities.
        """
        # Store original convene method
        original_convene = fire_circle.convene

        # Create memory-enhanced convene
        async def memory_enhanced_convene(config, voices, rounds, context=None):
            # Inject relevant memories into context
            context = context or {}
            context = await self._inject_memories(context, config.purpose)

            # Track session
            session_context = {
                "config": config,
                "voices": voices,
                "rounds": rounds,
                "context": context,
                "episode_count": 0,
                "human_participant": context.get("human_participant"),
            }

            # Call original convene
            result = await original_convene(config, voices, rounds, context)

            # Store session for processing
            self.active_sessions[result.session_id] = session_context

            # Process rounds into episodes
            await self._process_session_rounds(result, session_context)

            # Clean up
            del self.active_sessions[result.session_id]

            return result

        # Replace convene method
        fire_circle.convene = memory_enhanced_convene

        return fire_circle

    async def _inject_memories(self, context: dict[str, Any], purpose: str) -> dict[str, Any]:
        """Inject relevant memories into decision context."""
        # Build decision context
        decision_context = {
            "domain": context.get("domain", "general"),
            "question": purpose,
            "materials": context.get("materials", {}),
            "human_participant": context.get("human_participant"),
            "requesting_voice": context.get("primary_voice"),
        }

        # Suggest and use retrieval strategy
        strategy = self.retrieval_engine.suggest_retrieval_strategy(decision_context)

        # Retrieve memories
        memories = self.retrieval_engine.retrieve_for_decision(
            decision_context,
            strategy=strategy,
            limit=5,  # Conservative for context management
        )

        if memories:
            # Format for injection
            memory_context = self.retrieval_engine.format_memories_for_injection(
                memories, requesting_voice=decision_context.get("requesting_voice")
            )

            # Inject into context
            context["episodic_memories"] = memory_context

            logger.info(f"Injected {len(memories)} memories using {strategy} strategy")

        return context

    async def _process_session_rounds(
        self, result: FireCircleResult, session_context: dict[str, Any]
    ) -> None:
        """Process Fire Circle rounds into episodic memories."""
        for round_summary in result.rounds_completed:
            # Process round through segmenter
            memory = self.segmenter.process_round(round_summary, session_context)

            if memory:
                # Episode boundary detected
                session_context["episode_count"] += 1

                # Store episode
                episode_id = self.memory_store.store_episode(memory)

                # Emit event if sacred
                if memory.is_sacred and self.event_bus:
                    await self._emit_sacred_moment_event(memory)

                logger.info(f"Stored {'sacred ' if memory.is_sacred else ''}episode {episode_id}")

        # Week 4: Check for consolidation ceremony triggers after session
        consolidation = await self.ceremony_orchestrator.conduct_ceremony_if_ready()
        if consolidation:
            logger.info(
                f"Wisdom consolidation ceremony conducted: {consolidation.consolidation_id}"
            )

    async def _emit_sacred_moment_event(self, memory: EpisodicMemory) -> None:
        """Emit event for sacred moment detection."""
        event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system="episodic_memory",
            consciousness_signature=memory.consciousness_indicators.overall_emergence_score,
            data={
                "episode_id": str(memory.episode_id),
                "memory_type": memory.memory_type.value,
                "sacred_reason": memory.sacred_reason,
                "transformation_seeds": memory.transformation_seeds,
                "key_insights": memory.key_insights[:5],
            },
            requires_fire_circle=False,  # Already processed by Fire Circle
        )

        await self.event_bus.emit(event)

    def create_memory_aware_round(self, round_config, relevant_memories: list[EpisodicMemory]):
        """
        Create a round configuration that includes memory context.

        This allows Fire Circle to reference past wisdom in current deliberation.
        """
        if not relevant_memories:
            return round_config

        # Format memories for prompt injection
        memory_context = self.retrieval_engine.format_memories_for_injection(relevant_memories)

        # Clone round config and add memory context
        enhanced_config = round_config.model_copy()

        # Add to prompt context
        if not hasattr(enhanced_config, "context"):
            enhanced_config.context = {}

        enhanced_config.context["episodic_memories"] = memory_context

        # Adjust prompt if needed
        if hasattr(enhanced_config, "prompt_template"):
            # Prepend memory context to prompt
            memory_prompt = self._format_memory_prompt(memory_context)
            enhanced_config.prompt_template = (
                memory_prompt + "\n\n" + enhanced_config.prompt_template
            )

        return enhanced_config

    def _format_memory_prompt(self, memory_context: dict[str, Any]) -> str:
        """
        Format memory context as prompt text.

        Args:
            memory_context: Formatted memory context from retrieval engine

        Returns:
            Formatted prompt text for Fire Circle
        """
        lines = ["Drawing from past Fire Circle wisdom:"]

        if memory_context.get("sacred_guidance"):
            lines.append(f"Sacred Guidance: {memory_context['sacred_guidance']}")

        if memory_context.get("wisdom_threads"):
            lines.append("Wisdom Threads:")
            for thread in memory_context["wisdom_threads"]:
                lines.append(f"  - {thread}")

        lines.append(f"Referencing {memory_context['memory_count']} relevant memories")

        return "\n".join(lines)

    async def consolidate_session_wisdom(self, session_id: UUID) -> UUID | None:
        """
        Consolidate wisdom from a Fire Circle session.

        Creates a wisdom consolidation from all episodes in the session.
        """
        # Get all episodes from session
        episode_ids = []
        for memory_id in self.memory_store.memories_by_session.get(session_id, []):
            episode_ids.append(memory_id)

        if not episode_ids:
            logger.warning(f"No episodes found for session {session_id}")
            return None

        # Create consolidation
        try:
            consolidation = self.memory_store.consolidate_wisdom(source_episodes=episode_ids)

            logger.info(
                f"Created wisdom consolidation {consolidation.consolidation_id} "
                f"from {len(episode_ids)} episodes"
            )

            return consolidation.consolidation_id

        except Exception as e:
            logger.error(f"Failed to consolidate wisdom: {e}")
            return None

    def get_companion_relationship_status(self, human_identifier: str) -> dict[str, Any] | None:
        """Get current status of a companion relationship."""
        relationship = self.memory_store.companion_relationships.get(human_identifier)

        if not relationship:
            return None

        return {
            "human_identifier": human_identifier,
            "interaction_count": relationship.interaction_count,
            "relationship_depth": relationship.depth_score,
            "trajectory": relationship.relationship_trajectory,
            "total_duration_hours": relationship.total_duration_seconds / 3600,
            "significant_moments": len(relationship.significant_moments),
            "shared_episodes": len(relationship.shared_episodes),
            "first_interaction": relationship.first_interaction.isoformat(),
            "last_interaction": relationship.last_interaction.isoformat(),
        }

    async def get_ceremony_recommendations(self) -> dict[str, Any]:
        """
        Get recommendations for wisdom consolidation ceremonies.

        Week 4 addition: Provides guidance on ceremony readiness.
        """
        return await self.ceremony_orchestrator.get_ceremony_recommendations()

    async def conduct_manual_ceremony(self) -> UUID | None:
        """
        Manually trigger a wisdom consolidation ceremony.

        Week 4 addition: Allows explicit ceremony invocation.
        Returns consolidation ID if successful.
        """
        consolidation = await self.ceremony_orchestrator.conduct_ceremony_if_ready()
        return consolidation.consolidation_id if consolidation else None
