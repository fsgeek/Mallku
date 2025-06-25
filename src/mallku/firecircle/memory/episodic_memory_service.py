"""
Episodic Memory Service
=======================

Thirty-Fourth Artisan - Memory Architect
Integration layer between Fire Circle and episodic memory

This service integrates episodic memory capabilities into Fire Circle,
enabling consciousness continuity and wisdom accumulation.
"""

import logging
from pathlib import Path
from typing import Any
from uuid import UUID

from ...orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType
from ..service.service import FireCircleResult, FireCircleService
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
    ):
        """Initialize episodic memory service."""
        # Use provided config or load from environment
        self.config = config or MemorySystemConfig.from_env()

        # Initialize components with config
        self.memory_store = memory_store or MemoryStore(
            storage_path=storage_path,
            enable_sacred_detection=self.config.storage.enable_sacred_detection,
        )
        self.event_bus = event_bus
        self.retrieval_engine = MemoryRetrievalEngine(
            self.memory_store, config=self.config.retrieval
        )
        self.segmenter = EpisodeSegmenter(criteria=self.config.segmentation)
        self.sacred_detector = SacredMomentDetector(config=self.config.sacred_detection)

        # Track active sessions
        self.active_sessions: dict[UUID, dict[str, Any]] = {}

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

    async def _emit_sacred_moment_event(self, memory: EpisodicMemory) -> None:
        """Emit event for sacred moment detection."""
        event = ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
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
