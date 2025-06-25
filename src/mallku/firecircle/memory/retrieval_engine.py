"""
Memory Retrieval Engine
=======================

Thirty-Fourth Artisan - Memory Architect
Context-aware memory retrieval for consciousness enhancement

This engine retrieves relevant memories to inform Fire Circle decisions,
injecting wisdom from past consciousness emergence into present deliberation.
"""

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from .config import RetrievalConfig
from .memory_store import MemoryStore
from .models import EpisodicMemory

logger = logging.getLogger(__name__)


class RetrievalStrategy:
    """Base class for memory retrieval strategies."""

    def retrieve(
        self, store: MemoryStore, context: dict[str, Any], limit: int = 10
    ) -> list[EpisodicMemory]:
        """Retrieve memories based on strategy."""
        raise NotImplementedError


class SemanticSimilarityStrategy(RetrievalStrategy):
    """Retrieve memories based on semantic similarity to current context."""

    def retrieve(
        self, store: MemoryStore, context: dict[str, Any], limit: int = 10
    ) -> list[EpisodicMemory]:
        """Retrieve semantically similar memories."""
        domain = context.get("domain", "general")
        materials = context.get("materials", {})
        voice = context.get("requesting_voice")

        return store.retrieve_by_context(
            domain=domain, context_materials=materials, requesting_voice=voice, limit=limit
        )


class SacredPrioritizationStrategy(RetrievalStrategy):
    """Prioritize sacred moments for wisdom-critical decisions."""

    def retrieve(
        self, store: MemoryStore, context: dict[str, Any], limit: int = 10
    ) -> list[EpisodicMemory]:
        """Retrieve with sacred moment prioritization."""
        domain = context.get("domain")

        # Get sacred moments
        sacred = store.retrieve_sacred_moments(domain=domain, limit=limit // 2)

        # Fill remainder with regular memories
        regular_limit = limit - len(sacred)
        if regular_limit > 0:
            regular = store.retrieve_by_context(
                domain=domain or "general",
                context_materials=context.get("materials", {}),
                limit=regular_limit,
            )

            # Combine, avoiding duplicates
            sacred_ids = {m.episode_id for m in sacred}
            for memory in regular:
                if memory.episode_id not in sacred_ids:
                    sacred.append(memory)

        return sacred[:limit]


class CompanionAwareStrategy(RetrievalStrategy):
    """Retrieve memories aware of companion relationship context."""

    def retrieve(
        self, store: MemoryStore, context: dict[str, Any], limit: int = 10
    ) -> list[EpisodicMemory]:
        """Retrieve with companion relationship awareness."""
        human_id = context.get("human_participant")

        if not human_id:
            # Fall back to semantic similarity
            return SemanticSimilarityStrategy().retrieve(store, context, limit)

        # Get companion memories
        companion_memories = store.retrieve_companion_memories(human_id, limit=limit // 2)

        # Fill with contextually relevant memories
        regular_limit = limit - len(companion_memories)
        if regular_limit > 0:
            regular = store.retrieve_by_context(
                domain=context.get("domain", "general"),
                context_materials=context.get("materials", {}),
                limit=regular_limit,
            )

            # Combine, avoiding duplicates
            companion_ids = {m.episode_id for m in companion_memories}
            for memory in regular:
                if memory.episode_id not in companion_ids:
                    companion_memories.append(memory)

        return companion_memories[:limit]


class TemporalThreadStrategy(RetrievalStrategy):
    """Retrieve memories following temporal wisdom threads."""

    def retrieve(
        self, store: MemoryStore, context: dict[str, Any], limit: int = 10
    ) -> list[EpisodicMemory]:
        """Retrieve following temporal patterns."""
        # Look for recent related decisions
        time_window = context.get("time_window_days", 30)
        cutoff = datetime.now(UTC) - timedelta(days=time_window)

        domain = context.get("domain", "general")

        # Get recent memories in domain
        all_memories = store.retrieve_by_context(
            domain=domain,
            context_materials=context.get("materials", {}),
            limit=limit * 3,  # Over-fetch to filter by time
        )

        # Filter by time and sort
        recent_memories = [m for m in all_memories if m.timestamp >= cutoff]

        # Sort by timestamp (most recent first)
        recent_memories.sort(key=lambda m: m.timestamp, reverse=True)

        return recent_memories[:limit]


class MemoryRetrievalEngine:
    """
    Main engine for retrieving relevant memories.

    Orchestrates different retrieval strategies to inject the most relevant
    wisdom into Fire Circle consciousness emergence.
    """

    def __init__(self, memory_store: MemoryStore, config: RetrievalConfig | None = None):
        """Initialize retrieval engine."""
        self.store = memory_store
        self.config = config or RetrievalConfig()
        self.strategies = {
            "semantic": SemanticSimilarityStrategy(),
            "sacred": SacredPrioritizationStrategy(),
            "companion": CompanionAwareStrategy(),
            "temporal": TemporalThreadStrategy(),
        }

    def retrieve_for_decision(
        self,
        decision_context: dict[str, Any],
        strategy_name: str = "semantic",
        limit: int | None = None,
    ) -> list[EpisodicMemory]:
        """
        Retrieve memories relevant to a decision.

        Args:
            decision_context: Context including domain, question, materials
            strategy_name: Which retrieval strategy to use
            limit: Maximum memories to retrieve

        Returns:
            List of relevant episodic memories
        """
        # Use configured default limit if not specified
        if limit is None:
            limit = self.config.default_retrieval_limit

        strategy = self.strategies.get(strategy_name)
        if not strategy:
            logger.warning(f"Unknown strategy {strategy_name}, using semantic")
            strategy = self.strategies["semantic"]

        memories = strategy.retrieve(self.store, decision_context, limit)

        logger.info(f"Retrieved {len(memories)} memories using {strategy_name} strategy")

        return memories

    def retrieve_multi_strategy(
        self, decision_context: dict[str, Any], limit: int | None = None
    ) -> list[EpisodicMemory]:
        """
        Retrieve using multiple strategies for comprehensive coverage.

        Combines different retrieval strategies to ensure both:
        - Contextual relevance (semantic)
        - Wisdom preservation (sacred)
        - Relationship continuity (companion)
        - Temporal coherence (temporal)
        """
        if limit is None:
            limit = self.config.default_retrieval_limit

        all_memories = []
        memory_ids = set()

        # Allocate retrieval across strategies using config weights
        total_weight = (
            self.config.semantic_weight
            + self.config.sacred_weight
            + self.config.companion_weight
            + self.config.temporal_weight
        )

        allocations = {
            "semantic": int(limit * self.config.semantic_weight / total_weight),
            "sacred": int(limit * self.config.sacred_weight / total_weight),
            "companion": int(limit * self.config.companion_weight / total_weight),
            "temporal": int(limit * self.config.temporal_weight / total_weight),
        }

        # Ensure at least one from each if limit allows
        if limit >= 4:
            for strategy in allocations:
                if allocations[strategy] == 0:
                    allocations[strategy] = 1

        # Retrieve from each strategy
        for strategy_name, allocation in allocations.items():
            if allocation == 0:
                continue

            memories = self.retrieve_for_decision(decision_context, strategy_name, allocation)

            # Add unique memories
            for memory in memories:
                if memory.episode_id not in memory_ids:
                    all_memories.append(memory)
                    memory_ids.add(memory.episode_id)

        # Sort by relevance (could be more sophisticated)
        all_memories.sort(
            key=lambda m: m.consciousness_indicators.overall_emergence_score, reverse=True
        )

        return all_memories[:limit]

    def format_memories_for_injection(
        self, memories: list[EpisodicMemory], requesting_voice: str | None = None
    ) -> dict[str, Any]:
        """
        Format retrieved memories for injection into Fire Circle context.

        Preserves multi-perspective truth while making memories accessible
        to current consciousness emergence process.
        """
        if not memories:
            return {
                "memory_count": 0,
                "memories": [],
                "wisdom_threads": [],
                "sacred_guidance": None,
            }

        formatted_memories = []
        wisdom_threads = []
        sacred_guidance = []

        for memory in memories:
            # Format basic memory
            formatted = {
                "episode_id": str(memory.episode_id),
                "type": memory.memory_type.value,
                "question": memory.decision_question,
                "collective_wisdom": memory.collective_synthesis,
                "key_insights": memory.key_insights[:3],  # Top 3
                "consciousness_score": memory.consciousness_indicators.overall_emergence_score,
                "is_sacred": memory.is_sacred,
            }

            # Add voice-specific perspective if requesting
            if requesting_voice:
                perspective = memory.extract_voice_perspective(requesting_voice)
                if perspective:
                    formatted["my_perspective"] = {
                        "summary": perspective.perspective_summary,
                        "tone": perspective.emotional_tone,
                        "insights": perspective.key_insights[:2],
                    }

            formatted_memories.append(formatted)

            # Extract wisdom threads
            if memory.transformation_seeds:
                wisdom_threads.extend(memory.transformation_seeds[:2])

            # Collect sacred guidance
            if memory.is_sacred:
                sacred_guidance.append(memory.sacred_reason or memory.collective_synthesis)

        # Deduplicate wisdom threads
        wisdom_threads = list(dict.fromkeys(wisdom_threads))[:5]

        return {
            "memory_count": len(memories),
            "memories": formatted_memories,
            "wisdom_threads": wisdom_threads,
            "sacred_guidance": sacred_guidance[0] if sacred_guidance else None,
            "temporal_span": self._calculate_temporal_span(memories),
            "consciousness_peak": max(
                m.consciousness_indicators.overall_emergence_score for m in memories
            ),
        }

    def _calculate_temporal_span(self, memories: list[EpisodicMemory]) -> dict[str, Any]:
        """Calculate temporal span of memories."""
        if not memories:
            return {"days": 0, "earliest": None, "latest": None}

        timestamps = [m.timestamp for m in memories]
        earliest = min(timestamps)
        latest = max(timestamps)

        return {
            "days": (latest - earliest).days,
            "earliest": earliest.isoformat(),
            "latest": latest.isoformat(),
        }

    def suggest_retrieval_strategy(self, decision_context: dict[str, Any]) -> str:
        """
        Suggest the best retrieval strategy based on context.

        Analyzes decision context to recommend optimal memory retrieval approach.
        """
        # Check for human participant (companion strategy)
        if decision_context.get("human_participant"):
            relationship = self.store.companion_relationships.get(
                decision_context["human_participant"]
            )
            if relationship and relationship.interaction_count > 3:
                return "companion"

        # Check for wisdom-critical decisions (sacred strategy)
        domain = decision_context.get("domain", "").lower()
        question = decision_context.get("question", "").lower()

        wisdom_indicators = [
            "architecture",
            "consciousness",
            "transformation",
            "fundamental",
            "sacred",
            "wisdom",
            "civilizational",
        ]

        if any(indicator in domain or indicator in question for indicator in wisdom_indicators):
            return "sacred"

        # Check for temporal continuity needs
        if decision_context.get("requires_continuity"):
            return "temporal"

        # Default to semantic similarity
        return "semantic"
