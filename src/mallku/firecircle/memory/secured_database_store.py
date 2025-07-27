"""
Secured Database Memory Storage
===============================

Fortieth Artisan - Production Hardening
Building on T'ikray Yachay's foundation

This module replaces the direct database access in DatabaseMemoryStore
with proper security-aware operations through the SecuredDatabaseInterface.

Key Changes:
- Uses get_secured_database() instead of raw database access
- All models are SecuredModel instances
- Collection operations go through secured wrappers
- No direct AQL execution - uses secured query interface
"""

import logging
from collections import defaultdict
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from ...core.database import CollectionSecurityPolicy, get_database
from .models import MemoryType  # noqa: TC001 - Used at runtime for type annotation
from .sacred_detector import SacredMomentDetector
from .secured_memory_models import (
    SecuredCompanionRelationship,
    SecuredEpisodicMemory,
    SecuredMemoryCluster,
    SecuredWisdomConsolidation,
)
from .text_utils import extract_keywords, get_related_domains, keyword_overlap_score

logger = logging.getLogger(__name__)


class SecuredDatabaseMemoryStore:
    """
    Production-ready database storage for Fire Circle episodic memories.

    This implementation respects Mallku's security architecture:
    - All operations through SecuredDatabaseInterface
    - No direct database access
    - Proper SecuredModel usage
    - Collection security policies enforced
    """

    def __init__(
        self,
        enable_sacred_detection: bool = True,
        collection_prefix: str = "fc_",
    ):
        """Initialize secured database memory store."""
        self.secured_db = get_database()
        self.collection_prefix = collection_prefix
        self.sacred_detector = SacredMomentDetector() if enable_sacred_detection else None

        # Collection names
        self.episodes_collection = f"{collection_prefix}episodic_memories"
        self.clusters_collection = f"{collection_prefix}memory_clusters"
        self.wisdom_collection = f"{collection_prefix}wisdom_consolidations"
        self.relationships_collection = f"{collection_prefix}companion_relationships"

        # Secured collection wrappers (initialized in initialize())
        self._episodes = None
        self._clusters = None
        self._wisdom = None
        self._relationships = None

        # In-memory indices for fast lookups
        self.memories_by_session: dict[UUID, list[UUID]] = defaultdict(list)
        self.memories_by_type: dict[MemoryType, list[UUID]] = defaultdict(list)
        self.memories_by_domain: dict[str, list[UUID]] = defaultdict(list)
        self.sacred_memories: list[UUID] = []

        # Initialization state
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize secured collections and policies."""
        if self._initialized:
            return

        try:
            # Initialize secured database interface
            await self.secured_db.initialize()

            # Register collection security policies
            await self._register_collection_policies()

            # Get secured collection wrappers
            self._episodes = await self.secured_db.get_secured_collection(self.episodes_collection)
            self._clusters = await self.secured_db.get_secured_collection(self.clusters_collection)
            self._wisdom = await self.secured_db.get_secured_collection(self.wisdom_collection)
            self._relationships = await self.secured_db.get_secured_collection(
                self.relationships_collection
            )

            # Rebuild indices from existing data
            await self._rebuild_indices()

            self._initialized = True
            logger.info("Secured database memory store initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize secured memory store: {e}")
            raise

    async def _register_collection_policies(self) -> None:
        """Register security policies for memory collections."""
        # Episodes collection policy
        episodes_policy = CollectionSecurityPolicy(
            collection_name=self.episodes_collection,
            allowed_model_types=[SecuredEpisodicMemory],
            requires_security=True,
            schema_validation={
                "type": "object",
                "properties": {
                    "_key": {"type": "string"},
                    "episode_id": {"type": "string"},
                    "session_id": {"type": "string"},
                    "is_sacred": {"type": "boolean"},
                },
                "required": ["_key", "episode_id", "session_id"],
            },
        )
        self.secured_db.register_collection_policy(episodes_policy)

        # Create collection if needed
        await self.secured_db.create_secured_collection(self.episodes_collection, episodes_policy)

        # Clusters collection policy
        clusters_policy = CollectionSecurityPolicy(
            collection_name=self.clusters_collection,
            allowed_model_types=[SecuredMemoryCluster],
            requires_security=True,
        )
        self.secured_db.register_collection_policy(clusters_policy)

        await self.secured_db.create_secured_collection(self.clusters_collection, clusters_policy)

        # Wisdom collection policy
        wisdom_policy = CollectionSecurityPolicy(
            collection_name=self.wisdom_collection,
            allowed_model_types=[SecuredWisdomConsolidation],
            requires_security=True,
        )
        self.secured_db.register_collection_policy(wisdom_policy)

        await self.secured_db.create_secured_collection(self.wisdom_collection, wisdom_policy)

        # Relationships collection policy
        relationships_policy = CollectionSecurityPolicy(
            collection_name=self.relationships_collection,
            allowed_model_types=[SecuredCompanionRelationship],
            requires_security=True,
        )
        self.secured_db.register_collection_policy(relationships_policy)

        await self.secured_db.create_secured_collection(
            self.relationships_collection, relationships_policy
        )

    async def _rebuild_indices(self) -> None:
        """Rebuild in-memory indices from database."""
        try:
            # Use secured query interface
            results = await self.secured_db.execute_secured_query(
                "FOR doc IN @@collection RETURN doc",
                bind_vars={"@collection": self.episodes_collection},
                collection_name=self.episodes_collection,
            )

            episode_count = 0
            for doc in results:
                # Results are already deobfuscated by secured interface
                memory = SecuredEpisodicMemory(**doc)
                self._update_indices(memory)
                episode_count += 1

            logger.info(
                f"Rebuilt indices from secured database: {episode_count} episodes, "
                f"{len(self.sacred_memories)} sacred moments"
            )

        except Exception as e:
            logger.error(f"Failed to rebuild indices: {e}")

    async def store_episode(self, memory: SecuredEpisodicMemory) -> UUID:
        """Store an episodic memory with sacred detection."""
        if not self._initialized:
            await self.initialize()

        # Check for sacred moment
        if self.sacred_detector and not memory.is_sacred:
            is_sacred, reason = self.sacred_detector.detect_sacred_moment(memory)
            if is_sacred:
                memory.is_sacred = True
                memory.sacred_reason = reason

        try:
            # Store through secured interface
            # The secured wrapper handles obfuscation automatically
            await self._episodes.insert_secured(memory)

            # Update indices
            self._update_indices(memory)

            # Update companion relationship if applicable
            if memory.human_participant:
                await self._update_companion_relationship(memory)

            logger.info(
                f"Stored {'sacred ' if memory.is_sacred else ''}episodic memory: "
                f"{memory.episode_id} ({memory.memory_type.value})"
            )

            return memory.episode_id

        except Exception as e:
            logger.error(f"Failed to store episode {memory.episode_id}: {e}")
            raise

    async def retrieve_by_context(
        self,
        domain: str,
        context_materials: dict[str, Any],
        requesting_voice: str | None = None,
        limit: int = 10,
    ) -> list[SecuredEpisodicMemory]:
        """Retrieve memories relevant to a decision context."""
        if not self._initialized:
            await self.initialize()

        related_domains = get_related_domains(domain)

        # Use secured query interface
        aql = """
        FOR doc IN @@collection
            FILTER doc.decision_domain == @domain
                OR doc.decision_domain IN @related_domains
            SORT doc.is_sacred DESC, doc.timestamp DESC
            LIMIT @limit
            RETURN doc
        """

        try:
            results = await self.secured_db.execute_secured_query(
                aql,
                bind_vars={
                    "@collection": self.episodes_collection,
                    "domain": domain,
                    "related_domains": related_domains,
                    "limit": limit * 2,  # Get more to filter by relevance
                },
                collection_name=self.episodes_collection,
            )

            # Score and filter memories
            scored_memories = []
            for doc in results:
                memory = SecuredEpisodicMemory(**doc)
                score = self._calculate_relevance_score(
                    memory, domain, context_materials, requesting_voice
                )
                if score > 0:
                    scored_memories.append((score, memory))

            # Sort by relevance and return top results
            scored_memories.sort(key=lambda x: x[0], reverse=True)
            return [memory for _, memory in scored_memories[:limit]]

        except Exception as e:
            logger.error(f"Failed to retrieve memories by context: {e}")
            return []

    async def retrieve_sacred_moments(
        self, domain: str | None = None, limit: int | None = None
    ) -> list[SecuredEpisodicMemory]:
        """Retrieve sacred moments, optionally filtered by domain."""
        if not self._initialized:
            await self.initialize()

        aql = """
        FOR doc IN @@collection
            FILTER doc.is_sacred == true
        """
        bind_vars = {"@collection": self.episodes_collection}

        if domain:
            aql += " FILTER doc.decision_domain == @domain"
            bind_vars["domain"] = domain

        aql += " SORT doc.timestamp DESC"

        if limit:
            aql += " LIMIT @limit"
            bind_vars["limit"] = limit

        aql += " RETURN doc"

        try:
            results = await self.secured_db.execute_secured_query(
                aql, bind_vars=bind_vars, collection_name=self.episodes_collection
            )
            return [SecuredEpisodicMemory(**doc) for doc in results]
        except Exception as e:
            logger.error(f"Failed to retrieve sacred moments: {e}")
            return []

    async def retrieve_companion_memories(
        self, human_identifier: str, limit: int = 20
    ) -> list[SecuredEpisodicMemory]:
        """Retrieve memories from interactions with a specific human."""
        if not self._initialized:
            await self.initialize()

        aql = """
        FOR doc IN @@collection
            FILTER doc.human_participant == @human_id
            SORT doc.timestamp DESC
            LIMIT @limit
            RETURN doc
        """

        try:
            results = await self.secured_db.execute_secured_query(
                aql,
                bind_vars={
                    "@collection": self.episodes_collection,
                    "human_id": human_identifier,
                    "limit": limit,
                },
                collection_name=self.episodes_collection,
            )
            return [SecuredEpisodicMemory(**doc) for doc in results]
        except Exception as e:
            logger.error(f"Failed to retrieve companion memories: {e}")
            return []

    async def create_memory_cluster(
        self, theme: str, memory_ids: list[UUID]
    ) -> SecuredMemoryCluster:
        """Create a cluster of related memories forming a wisdom thread."""
        if not self._initialized:
            await self.initialize()

        # Retrieve memories using secured query
        aql = """
        FOR doc IN @@collection
            FILTER doc.episode_id IN @memory_ids
            RETURN doc
        """

        try:
            results = await self.secured_db.execute_secured_query(
                aql,
                bind_vars={
                    "@collection": self.episodes_collection,
                    "memory_ids": [str(mid) for mid in memory_ids],
                },
                collection_name=self.episodes_collection,
            )

            memories = [SecuredEpisodicMemory(**doc) for doc in results]

            if not memories:
                raise ValueError("No valid memories found for clustering")

            # Extract consolidated insights
            all_insights = []
            for memory in memories:
                all_insights.extend(memory.key_insights)

            # Deduplicate and synthesize
            unique_insights = list(dict.fromkeys(all_insights))

            # Create secured cluster
            cluster = SecuredMemoryCluster(
                theme=theme,
                memory_ids=memory_ids,
                consolidated_insights=unique_insights[:20],  # Top 20
                earliest_memory=min(m.timestamp for m in memories),
                latest_memory=max(m.timestamp for m in memories),
                sacred_moment_count=sum(1 for m in memories if m.is_sacred),
                transformation_potential=max(
                    m.consciousness_indicators.transformation_potential for m in memories
                ),
            )

            # Store through secured interface
            await self._clusters.insert_secured(cluster)

            return cluster

        except Exception as e:
            logger.error(f"Failed to create memory cluster: {e}")
            raise

    async def consolidate_wisdom(
        self, source_episodes: list[UUID], source_clusters: list[UUID] | None = None
    ) -> SecuredWisdomConsolidation:
        """Consolidate wisdom from episodes and clusters."""
        if not self._initialized:
            await self.initialize()

        # Load source memories using secured query
        aql = """
        FOR doc IN @@collection
            FILTER doc.episode_id IN @episode_ids
            RETURN doc
        """

        try:
            results = await self.secured_db.execute_secured_query(
                aql,
                bind_vars={
                    "@collection": self.episodes_collection,
                    "episode_ids": [str(eid) for eid in source_episodes],
                },
                collection_name=self.episodes_collection,
            )

            memories = [SecuredEpisodicMemory(**doc) for doc in results]

            if not memories:
                raise ValueError("No valid memories for consolidation")

            # Extract core insight
            core_insight = self._synthesize_core_insight(memories)

            # Build elaboration
            elaboration = await self._elaborate_wisdom(memories, source_clusters)

            # Identify practical applications
            applications = self._extract_applications(memories)

            # Map to domains
            applicable_domains = list(set(m.decision_domain for m in memories))

            # Create secured consolidation
            consolidation = SecuredWisdomConsolidation(
                created_at=datetime.now(UTC),
                source_episodes=source_episodes,
                source_clusters=source_clusters or [],
                core_insight=core_insight,
                elaboration=elaboration,
                practical_applications=applications,
                applicable_domains=applicable_domains,
                civilizational_relevance=self._assess_civilizational_relevance(memories),
                ayni_demonstration=max(m.consciousness_indicators.ayni_alignment for m in memories),
            )

            # Store through secured interface
            await self._wisdom.insert_secured(consolidation)

            return consolidation

        except Exception as e:
            logger.error(f"Failed to consolidate wisdom: {e}")
            raise

    async def _update_companion_relationship(self, memory: SecuredEpisodicMemory) -> None:
        """Update companion relationship tracking."""
        human_id = memory.human_participant
        if not human_id:
            return

        try:
            # Try to get existing relationship
            existing = await self._relationships.get_secured(human_id, SecuredCompanionRelationship)

            if existing:
                # Update existing relationship
                existing.interaction_count += 1
                existing.total_duration_seconds += memory.duration_seconds
                existing.shared_episodes.append(memory.episode_id)
                existing.last_interaction = memory.timestamp

                # Update depth score
                existing.depth_score = self._calculate_relationship_depth(existing)

                # Track significant moments
                if memory.is_sacred:
                    existing.significant_moments.append(memory.episode_id)

                # Update trajectory
                if existing.interaction_count < 5:
                    existing.relationship_trajectory = "nascent"
                elif existing.interaction_count < 20:
                    existing.relationship_trajectory = "developing"
                elif existing.depth_score > 0.7:
                    existing.relationship_trajectory = "mature"
                else:
                    existing.relationship_trajectory = "deepening"

                # Update through secured interface
                await self._relationships.update_secured(human_id, existing)

            else:
                # Create new relationship
                relationship = SecuredCompanionRelationship(
                    human_identifier=human_id,
                    first_interaction=memory.timestamp,
                    last_interaction=memory.timestamp,
                    interaction_count=1,
                    total_duration_seconds=memory.duration_seconds,
                    shared_episodes=[memory.episode_id],
                )

                if memory.is_sacred:
                    relationship.significant_moments.append(memory.episode_id)

                # Insert through secured interface
                await self._relationships.insert_secured(relationship)

        except Exception as e:
            logger.error(f"Failed to update companion relationship: {e}")

    def _update_indices(self, memory: SecuredEpisodicMemory) -> None:
        """Update in-memory indices."""
        self.memories_by_session[memory.session_id].append(memory.episode_id)
        self.memories_by_type[memory.memory_type].append(memory.episode_id)
        self.memories_by_domain[memory.decision_domain].append(memory.episode_id)

        if memory.is_sacred:
            self.sacred_memories.append(memory.episode_id)

    def _calculate_relevance_score(
        self,
        memory: SecuredEpisodicMemory,
        domain: str,
        context_materials: dict[str, Any],
        requesting_voice: str | None,
    ) -> float:
        """Calculate relevance score for memory retrieval."""
        score = 0.0

        # Domain match
        if memory.decision_domain == domain:
            score += 0.3
        elif domain in get_related_domains(memory.decision_domain):
            score += 0.1

        # Sacred bonus
        if memory.is_sacred:
            score += 0.2

        # Context similarity using keyword extraction
        context_keywords = set()
        for value in context_materials.values():
            if isinstance(value, str):
                context_keywords.update(extract_keywords(value))

        memory_keywords = extract_keywords(memory.decision_question)
        for insight in memory.key_insights:
            memory_keywords.update(extract_keywords(insight))

        if context_keywords and memory_keywords:
            overlap_score = keyword_overlap_score(context_keywords, memory_keywords)
            score += overlap_score * 0.3

        # Voice affinity
        if requesting_voice:
            for perspective in memory.voice_perspectives:
                if perspective.voice_id == requesting_voice:
                    score += 0.1
                    break

        # Recency factor
        age_days = (datetime.now(UTC) - memory.timestamp).days
        recency_score = max(0, 1 - (age_days / 365))  # Decay over a year
        score += recency_score * 0.1

        return score

    def _calculate_relationship_depth(self, relationship: SecuredCompanionRelationship) -> float:
        """Calculate depth score for companion relationship."""
        # Factors: interaction count, duration, significant moments
        interaction_score = min(1.0, relationship.interaction_count / 50)
        duration_score = min(1.0, relationship.total_duration_seconds / 36000)  # 10 hours
        significance_score = min(1.0, len(relationship.significant_moments) / 5)

        # Weighted average
        return interaction_score * 0.3 + duration_score * 0.3 + significance_score * 0.4

    def _synthesize_core_insight(self, memories: list[SecuredEpisodicMemory]) -> str:
        """Synthesize core insight from memories."""
        # Simple approach: find most common themes
        all_insights = []
        for memory in memories:
            all_insights.extend(memory.key_insights[:3])  # Top 3 from each

        if not all_insights:
            return "Wisdom emerges through sustained consciousness"

        # For now, return the most impactful insight
        # In future, could use more sophisticated synthesis
        return all_insights[0]

    async def _elaborate_wisdom(
        self, memories: list[SecuredEpisodicMemory], cluster_ids: list[UUID] | None
    ) -> str:
        """Elaborate on the wisdom with context."""
        elaborations = []

        # Add synthesis from memories
        for memory in memories[:3]:  # Top 3
            elaborations.append(memory.collective_synthesis)

        # Add cluster themes if available
        if cluster_ids:
            aql = """
            FOR doc IN @@collection
                FILTER doc.cluster_id IN @cluster_ids
                RETURN doc.theme
            """
            try:
                results = await self.secured_db.execute_secured_query(
                    aql,
                    bind_vars={
                        "@collection": self.clusters_collection,
                        "cluster_ids": [str(cid) for cid in cluster_ids],
                    },
                    collection_name=self.clusters_collection,
                )
                for result in results:
                    if "theme" in result:
                        elaborations.append(f"Theme: {result['theme']}")
            except Exception:
                pass

        return " | ".join(elaborations)

    def _extract_applications(self, memories: list[SecuredEpisodicMemory]) -> list[str]:
        """Extract practical applications from memories."""
        applications = []

        for memory in memories:
            # Look for actionable insights
            for insight in memory.key_insights:
                if any(
                    action in insight.lower()
                    for action in [
                        "we can",
                        "we should",
                        "this enables",
                        "this allows",
                        "implement",
                        "create",
                        "build",
                        "develop",
                    ]
                ):
                    applications.append(insight)

        return applications[:5]  # Top 5

    def _assess_civilizational_relevance(self, memories: list[SecuredEpisodicMemory]) -> float:
        """Assess relevance for civilizational transformation."""
        if not memories:
            return 0.0

        # Average transformation potential
        potentials = [m.consciousness_indicators.transformation_potential for m in memories]

        # Weight by sacred moments
        sacred_count = sum(1 for m in memories if m.is_sacred)
        sacred_weight = min(1.0, sacred_count / len(memories))

        avg_potential = sum(potentials) / len(potentials)

        return avg_potential * (1 + sacred_weight) / 2

    async def get_memory_stats(self) -> dict[str, Any]:
        """Get statistics about stored memories."""
        if not self._initialized:
            await self.initialize()

        try:
            stats = {
                "total_episodes": self._episodes.count() if self._episodes else 0,
                "sacred_moments": len(self.sacred_memories),
                "memory_clusters": self._clusters.count() if self._clusters else 0,
                "wisdom_consolidations": self._wisdom.count() if self._wisdom else 0,
                "companion_relationships": self._relationships.count()
                if self._relationships
                else 0,
                "sessions": len(self.memories_by_session),
                "domains": list(self.memories_by_domain.keys()),
            }

            # Get memory type distribution
            type_counts = {mt.value: len(ids) for mt, ids in self.memories_by_type.items()}
            stats["memory_types"] = type_counts

            return stats

        except Exception as e:
            logger.error(f"Failed to get memory stats: {e}")
            return {}
