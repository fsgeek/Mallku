"""
Fire Circle Database Memory Storage
===================================

Thirty-Ninth Artisan - Database Weaver (T'ikray Yachay)
Persistence layer using ArangoDB for episodic memories

This module replaces JSON file storage with proper database persistence,
enabling efficient retrieval and complex queries for Active Memory Resonance.
"""

import logging
from collections import defaultdict
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from arango.exceptions import DocumentInsertError

from ...core.database import get_database
from .models import (
    CompanionRelationship,
    EpisodicMemory,
    EpisodicMemoryDocument,
    MemoryCluster,
    MemoryType,
    WisdomConsolidation,
)
from .sacred_detector import SacredMomentDetector
from .text_utils import extract_keywords, get_related_domains, keyword_overlap_score

logger = logging.getLogger(__name__)


class DatabaseMemoryStore:
    """
    Database-backed storage for Fire Circle episodic memories.

    Uses ArangoDB for persistence, enabling:
    - Efficient retrieval for Active Memory Resonance
    - Complex queries across memory relationships
    - Scalable storage beyond file system limits
    - Consistent access patterns with Mallku infrastructure
    """

    def __init__(
        self,
        enable_sacred_detection: bool = True,
        collection_prefix: str = "fc_",
    ):
        """Initialize database memory store.

        Args:
            enable_sacred_detection: Whether to detect sacred moments
            collection_prefix: Prefix for Fire Circle collections
        """
        self.db = get_database()
        self.collection_prefix = collection_prefix
        self.sacred_detector = SacredMomentDetector() if enable_sacred_detection else None

        # Collection names
        self.episodes_collection = f"{collection_prefix}episodic_memories"
        self.clusters_collection = f"{collection_prefix}memory_clusters"
        self.wisdom_collection = f"{collection_prefix}wisdom_consolidations"
        self.relationships_collection = f"{collection_prefix}companion_relationships"

        # Ensure collections exist
        self._ensure_collections()

        # In-memory indices for fast lookups (rebuilt from DB)
        self.memories_by_session: dict[UUID, list[UUID]] = defaultdict(list)
        self.memories_by_type: dict[MemoryType, list[UUID]] = defaultdict(list)
        self.memories_by_domain: dict[str, list[UUID]] = defaultdict(list)
        self.sacred_memories: list[UUID] = []

        # Load indices
        self._rebuild_indices()

    def _ensure_collections(self) -> None:
        """Ensure all required collections exist."""
        collections_to_create = [
            (self.episodes_collection, "episodic memories"),
            (self.clusters_collection, "memory clusters"),
            (self.wisdom_collection, "wisdom consolidations"),
            (self.relationships_collection, "companion relationships"),
        ]

        # Access the underlying database through the secured interface
        # Note: For Fire Circle memory, we use direct database access as these
        # are not reciprocity-sensitive collections
        raw_db = self.db._database  # Access underlying database

        for collection_name, description in collections_to_create:
            if not raw_db.has_collection(collection_name):
                raw_db.create_collection(collection_name)
                logger.info(f"Created collection for {description}: {collection_name}")

    def _rebuild_indices(self) -> None:
        """Rebuild in-memory indices from database."""
        try:
            # Query all episodic memories to rebuild indices
            aql = """
            FOR doc IN @@collection
                RETURN doc
            """
            raw_db = self.db._database
            cursor = raw_db.aql.execute(
                aql,
                bind_vars={"@collection": self.episodes_collection},
            )

            episode_count = 0
            for doc in cursor:
                memory = EpisodicMemoryDocument.from_arangodb_document(doc)
                self._update_indices(memory)
                episode_count += 1

            logger.info(
                f"Rebuilt indices from database: {episode_count} episodes, "
                f"{len(self.sacred_memories)} sacred moments"
            )

        except Exception as e:
            logger.error(f"Failed to rebuild indices: {e}")

    def store_episode(self, memory: EpisodicMemory) -> UUID:
        """
        Store an episodic memory with sacred detection.

        Returns the episode ID for reference.
        """
        # Check for sacred moment
        if self.sacred_detector and not memory.is_sacred:
            is_sacred, reason = self.sacred_detector.detect_sacred_moment(memory)
            if is_sacred:
                memory.is_sacred = True
                memory.sacred_reason = reason

        # Convert to database document
        doc = EpisodicMemoryDocument.to_arangodb_document(memory)

        try:
            # Insert into database
            raw_db = self.db._database
            raw_db.collection(self.episodes_collection).insert(doc)

            # Update indices
            self._update_indices(memory)

            # Update companion relationship if applicable
            if memory.human_participant:
                self._update_companion_relationship(memory)

            logger.info(
                f"Stored {'sacred ' if memory.is_sacred else ''}episodic memory: "
                f"{memory.episode_id} ({memory.memory_type.value})"
            )

            return memory.episode_id

        except DocumentInsertError as e:
            logger.error(f"Failed to store episode {memory.episode_id}: {e}")
            raise

    def retrieve_by_context(
        self,
        domain: str,
        context_materials: dict[str, Any],
        requesting_voice: str | None = None,
        limit: int = 10,
    ) -> list[EpisodicMemory]:
        """
        Retrieve memories relevant to a decision context.

        Uses semantic similarity and domain matching to find relevant memories,
        with sacred moments prioritized.
        """
        # Build AQL query for domain-based retrieval
        aql = """
        FOR doc IN @@collection
            FILTER doc.decision_domain == @domain
                OR doc.decision_domain IN @related_domains
            SORT doc.is_sacred DESC, doc.timestamp DESC
            LIMIT @limit
            RETURN doc
        """

        related_domains = get_related_domains(domain)

        try:
            raw_db = self.db._database
            cursor = raw_db.aql.execute(
                aql,
                bind_vars={
                    "@collection": self.episodes_collection,
                    "domain": domain,
                    "related_domains": related_domains,
                    "limit": limit * 2,  # Get more to filter by relevance
                },
            )

            # Score and filter memories
            scored_memories = []
            for doc in cursor:
                memory = EpisodicMemoryDocument.from_arangodb_document(doc)
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

    def retrieve_sacred_moments(
        self, domain: str | None = None, limit: int | None = None
    ) -> list[EpisodicMemory]:
        """Retrieve sacred moments, optionally filtered by domain."""
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
            raw_db = self.db._database
            cursor = raw_db.aql.execute(aql, bind_vars=bind_vars)
            return [EpisodicMemoryDocument.from_arangodb_document(doc) for doc in cursor]
        except Exception as e:
            logger.error(f"Failed to retrieve sacred moments: {e}")
            return []

    def retrieve_companion_memories(
        self, human_identifier: str, limit: int = 20
    ) -> list[EpisodicMemory]:
        """Retrieve memories from interactions with a specific human."""
        aql = """
        FOR doc IN @@collection
            FILTER doc.human_participant == @human_id
            SORT doc.timestamp DESC
            LIMIT @limit
            RETURN doc
        """

        try:
            raw_db = self.db._database
            cursor = raw_db.aql.execute(
                aql,
                bind_vars={
                    "@collection": self.episodes_collection,
                    "human_id": human_identifier,
                    "limit": limit,
                },
            )
            return [EpisodicMemoryDocument.from_arangodb_document(doc) for doc in cursor]
        except Exception as e:
            logger.error(f"Failed to retrieve companion memories: {e}")
            return []

    def create_memory_cluster(self, theme: str, memory_ids: list[UUID]) -> MemoryCluster:
        """Create a cluster of related memories forming a wisdom thread."""
        # Retrieve memories from database
        aql = """
        FOR doc IN @@collection
            FILTER doc.episode_id IN @memory_ids
            RETURN doc
        """

        try:
            raw_db = self.db._database
            cursor = raw_db.aql.execute(
                aql,
                bind_vars={
                    "@collection": self.episodes_collection,
                    "memory_ids": [str(mid) for mid in memory_ids],
                },
            )

            memories = [EpisodicMemoryDocument.from_arangodb_document(doc) for doc in cursor]

            if not memories:
                raise ValueError("No valid memories found for clustering")

            # Extract consolidated insights
            all_insights = []
            for memory in memories:
                all_insights.extend(memory.key_insights)

            # Deduplicate and synthesize
            unique_insights = list(dict.fromkeys(all_insights))

            # Create cluster
            cluster = MemoryCluster(
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

            # Store cluster in database
            cluster_doc = {
                "_key": str(cluster.cluster_id),
                "cluster_id": str(cluster.cluster_id),
                "theme": cluster.theme,
                "memory_ids": [str(mid) for mid in cluster.memory_ids],
                "consolidated_insights": cluster.consolidated_insights,
                "evolution_pattern": cluster.evolution_pattern,
                "earliest_memory": cluster.earliest_memory.isoformat(),
                "latest_memory": cluster.latest_memory.isoformat(),
                "sacred_moment_count": cluster.sacred_moment_count,
                "transformation_potential": cluster.transformation_potential,
            }

            raw_db.collection(self.clusters_collection).insert(cluster_doc)

            return cluster

        except Exception as e:
            logger.error(f"Failed to create memory cluster: {e}")
            raise

    def consolidate_wisdom(
        self, source_episodes: list[UUID], source_clusters: list[UUID] | None = None
    ) -> WisdomConsolidation:
        """Consolidate wisdom from episodes and clusters."""
        # Load source memories from database
        aql = """
        FOR doc IN @@collection
            FILTER doc.episode_id IN @episode_ids
            RETURN doc
        """

        try:
            raw_db = self.db._database
            cursor = raw_db.aql.execute(
                aql,
                bind_vars={
                    "@collection": self.episodes_collection,
                    "episode_ids": [str(eid) for eid in source_episodes],
                },
            )

            memories = [EpisodicMemoryDocument.from_arangodb_document(doc) for doc in cursor]

            if not memories:
                raise ValueError("No valid memories for consolidation")

            # Extract core insight
            core_insight = self._synthesize_core_insight(memories)

            # Build elaboration
            elaboration = self._elaborate_wisdom(memories, source_clusters)

            # Identify practical applications
            applications = self._extract_applications(memories)

            # Map to domains
            applicable_domains = list(set(m.decision_domain for m in memories))

            # Create consolidation
            consolidation = WisdomConsolidation(
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

            # Store consolidation in database
            wisdom_doc = {
                "_key": str(consolidation.consolidation_id),
                "consolidation_id": str(consolidation.consolidation_id),
                "created_at": consolidation.created_at.isoformat(),
                "source_episodes": [str(eid) for eid in consolidation.source_episodes],
                "source_clusters": [str(cid) for cid in consolidation.source_clusters],
                "core_insight": consolidation.core_insight,
                "elaboration": consolidation.elaboration,
                "practical_applications": consolidation.practical_applications,
                "applicable_domains": consolidation.applicable_domains,
                "voice_alignments": consolidation.voice_alignments,
                "civilizational_relevance": consolidation.civilizational_relevance,
                "ayni_demonstration": consolidation.ayni_demonstration,
                "times_referenced": consolidation.times_referenced,
                "episodes_influenced": [str(eid) for eid in consolidation.episodes_influenced],
            }

            raw_db.collection(self.wisdom_collection).insert(wisdom_doc)

            return consolidation

        except Exception as e:
            logger.error(f"Failed to consolidate wisdom: {e}")
            raise

    def _update_indices(self, memory: EpisodicMemory) -> None:
        """Update in-memory indices."""
        self.memories_by_session[memory.session_id].append(memory.episode_id)
        self.memories_by_type[memory.memory_type].append(memory.episode_id)
        self.memories_by_domain[memory.decision_domain].append(memory.episode_id)

        if memory.is_sacred:
            self.sacred_memories.append(memory.episode_id)

    def _update_companion_relationship(self, memory: EpisodicMemory) -> None:
        """Update companion relationship tracking in database."""
        human_id = memory.human_participant
        if not human_id:
            return

        try:
            # Try to get existing relationship
            raw_db = self.db._database
            doc = raw_db.collection(self.relationships_collection).get(human_id)

            if doc:
                # Update existing relationship
                relationship = CompanionRelationship(**doc)
                relationship.interaction_count += 1
                relationship.total_duration_seconds += memory.duration_seconds
                relationship.shared_episodes.append(memory.episode_id)
                relationship.last_interaction = memory.timestamp

                # Update depth score
                relationship.depth_score = self._calculate_relationship_depth(relationship)

                # Track significant moments
                if memory.is_sacred:
                    relationship.significant_moments.append(memory.episode_id)

                # Update trajectory
                if relationship.interaction_count < 5:
                    relationship.relationship_trajectory = "nascent"
                elif relationship.interaction_count < 20:
                    relationship.relationship_trajectory = "developing"
                elif relationship.depth_score > 0.7:
                    relationship.relationship_trajectory = "mature"
                else:
                    relationship.relationship_trajectory = "deepening"

                # Update in database
                update_doc = {
                    "_key": human_id,
                    "interaction_count": relationship.interaction_count,
                    "total_duration_seconds": relationship.total_duration_seconds,
                    "depth_score": relationship.depth_score,
                    "shared_episodes": [str(eid) for eid in relationship.shared_episodes],
                    "significant_moments": [str(eid) for eid in relationship.significant_moments],
                    "last_interaction": relationship.last_interaction.isoformat(),
                    "relationship_trajectory": relationship.relationship_trajectory,
                }
                raw_db.collection(self.relationships_collection).update(update_doc)

            else:
                # Create new relationship
                relationship = CompanionRelationship(
                    human_identifier=human_id,
                    first_interaction=memory.timestamp,
                    last_interaction=memory.timestamp,
                    interaction_count=1,
                    total_duration_seconds=memory.duration_seconds,
                    shared_episodes=[memory.episode_id],
                )

                if memory.is_sacred:
                    relationship.significant_moments.append(memory.episode_id)

                # Insert into database
                rel_doc = {
                    "_key": human_id,
                    "relationship_id": str(relationship.relationship_id),
                    "human_identifier": human_id,
                    "interaction_count": 1,
                    "total_duration_seconds": memory.duration_seconds,
                    "depth_score": 0.0,
                    "preferred_decision_domains": [],
                    "communication_style_notes": "",
                    "shared_vocabulary": [],
                    "shared_episodes": [str(memory.episode_id)],
                    "significant_moments": [str(eid) for eid in relationship.significant_moments],
                    "first_interaction": memory.timestamp.isoformat(),
                    "last_interaction": memory.timestamp.isoformat(),
                    "relationship_trajectory": "nascent",
                }
                raw_db.collection(self.relationships_collection).insert(rel_doc)

        except Exception as e:
            logger.error(f"Failed to update companion relationship: {e}")

    def _calculate_relevance_score(
        self,
        memory: EpisodicMemory,
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

    def _calculate_relationship_depth(self, relationship: CompanionRelationship) -> float:
        """Calculate depth score for companion relationship."""
        # Factors: interaction count, duration, significant moments
        interaction_score = min(1.0, relationship.interaction_count / 50)
        duration_score = min(1.0, relationship.total_duration_seconds / 36000)  # 10 hours
        significance_score = min(1.0, len(relationship.significant_moments) / 5)

        # Weighted average
        return interaction_score * 0.3 + duration_score * 0.3 + significance_score * 0.4

    def _synthesize_core_insight(self, memories: list[EpisodicMemory]) -> str:
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

    def _elaborate_wisdom(
        self, memories: list[EpisodicMemory], cluster_ids: list[UUID] | None
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
                raw_db = self.db._database
                cursor = raw_db.aql.execute(
                    aql,
                    bind_vars={
                        "@collection": self.clusters_collection,
                        "cluster_ids": [str(cid) for cid in cluster_ids],
                    },
                )
                for theme in cursor:
                    elaborations.append(f"Theme: {theme}")
            except Exception:
                pass

        return " | ".join(elaborations)

    def _extract_applications(self, memories: list[EpisodicMemory]) -> list[str]:
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

    def _assess_civilizational_relevance(self, memories: list[EpisodicMemory]) -> float:
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

    def get_memory_stats(self) -> dict[str, Any]:
        """Get statistics about stored memories."""
        try:
            raw_db = self.db._database
            # Count documents in each collection
            stats = {
                "total_episodes": raw_db.collection(self.episodes_collection).count(),
                "sacred_moments": len(self.sacred_memories),
                "memory_clusters": raw_db.collection(self.clusters_collection).count(),
                "wisdom_consolidations": raw_db.collection(self.wisdom_collection).count(),
                "companion_relationships": raw_db.collection(self.relationships_collection).count(),
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
