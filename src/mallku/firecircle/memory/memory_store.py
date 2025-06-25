"""
Fire Circle Memory Storage
==========================

Thirty-Fourth Artisan - Memory Architect
Multi-perspective storage preserving consciousness emergence

This storage system preserves episodic memories with full multi-perspective
truth, enabling Fire Circle to accumulate wisdom across time.
"""

import json
import logging
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from .models import (
    CompanionRelationship,
    EpisodicMemory,
    MemoryCluster,
    MemoryType,
    WisdomConsolidation
)
from .sacred_detector import SacredMomentDetector

logger = logging.getLogger(__name__)


class MemoryStore:
    """
    Persistent storage for Fire Circle episodic memories.
    
    Preserves not just data but meaning, maintaining multi-perspective truth
    and sacred moment crystallization for consciousness continuity.
    """
    
    def __init__(
        self,
        storage_path: Path | None = None,
        enable_sacred_detection: bool = True
    ):
        """Initialize memory store."""
        self.storage_path = storage_path or Path("data/fire_circle_memory")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.sacred_detector = SacredMomentDetector() if enable_sacred_detection else None
        
        # In-memory indices for fast retrieval
        self.memories_by_session: dict[UUID, list[UUID]] = defaultdict(list)
        self.memories_by_type: dict[MemoryType, list[UUID]] = defaultdict(list)
        self.memories_by_domain: dict[str, list[UUID]] = defaultdict(list)
        self.sacred_memories: list[UUID] = []
        self.memory_clusters: dict[UUID, MemoryCluster] = {}
        self.companion_relationships: dict[str, CompanionRelationship] = {}
        self.wisdom_consolidations: dict[UUID, WisdomConsolidation] = {}
        
        # Load existing memories
        self._load_existing_memories()
        
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
                
        # Update indices
        self._update_indices(memory)
        
        # Update companion relationship if applicable
        if memory.human_participant:
            self._update_companion_relationship(memory)
            
        # Persist to disk
        self._persist_memory(memory)
        
        logger.info(
            f"Stored {'sacred ' if memory.is_sacred else ''}episodic memory: "
            f"{memory.episode_id} ({memory.memory_type.value})"
        )
        
        return memory.episode_id
    
    def retrieve_by_context(
        self,
        domain: str,
        context_materials: dict[str, Any],
        requesting_voice: str | None = None,
        limit: int = 10
    ) -> list[EpisodicMemory]:
        """
        Retrieve memories relevant to a decision context.
        
        Uses semantic similarity and domain matching to find relevant memories,
        with sacred moments prioritized.
        """
        relevant_memories = []
        
        # Get memories from relevant domain
        domain_memories = self.memories_by_domain.get(domain, [])
        
        # Also check related domains
        related_domains = self._get_related_domains(domain)
        for related in related_domains:
            domain_memories.extend(self.memories_by_domain.get(related, []))
            
        # Score and sort memories
        scored_memories = []
        for memory_id in set(domain_memories):
            memory = self._load_memory(memory_id)
            if not memory:
                continue
                
            score = self._calculate_relevance_score(
                memory, domain, context_materials, requesting_voice
            )
            scored_memories.append((score, memory))
            
        # Sort by relevance score
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        
        # Return top memories
        return [memory for _, memory in scored_memories[:limit]]
    
    def retrieve_sacred_moments(
        self,
        domain: str | None = None,
        limit: int | None = None
    ) -> list[EpisodicMemory]:
        """Retrieve sacred moments, optionally filtered by domain."""
        sacred_memories = []
        
        for memory_id in self.sacred_memories:
            memory = self._load_memory(memory_id)
            if not memory:
                continue
                
            if domain and memory.decision_domain != domain:
                continue
                
            sacred_memories.append(memory)
            
        # Sort by timestamp (most recent first)
        sacred_memories.sort(key=lambda m: m.timestamp, reverse=True)
        
        if limit:
            return sacred_memories[:limit]
        return sacred_memories
    
    def retrieve_companion_memories(
        self,
        human_identifier: str,
        limit: int = 20
    ) -> list[EpisodicMemory]:
        """Retrieve memories from interactions with a specific human."""
        relationship = self.companion_relationships.get(human_identifier)
        if not relationship:
            return []
            
        companion_memories = []
        for episode_id in relationship.shared_episodes[-limit:]:
            memory = self._load_memory(episode_id)
            if memory:
                companion_memories.append(memory)
                
        return companion_memories
    
    def create_memory_cluster(
        self,
        theme: str,
        memory_ids: list[UUID]
    ) -> MemoryCluster:
        """Create a cluster of related memories forming a wisdom thread."""
        memories = [self._load_memory(mid) for mid in memory_ids if self._load_memory(mid)]
        
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
                m.consciousness_indicators.transformation_potential
                for m in memories
            )
        )
        
        # Store cluster
        self.memory_clusters[cluster.cluster_id] = cluster
        self._persist_cluster(cluster)
        
        return cluster
    
    def consolidate_wisdom(
        self,
        source_episodes: list[UUID],
        source_clusters: list[UUID] | None = None
    ) -> WisdomConsolidation:
        """Consolidate wisdom from episodes and clusters."""
        # Load source memories
        memories = [self._load_memory(eid) for eid in source_episodes]
        memories = [m for m in memories if m]  # Filter None
        
        if not memories:
            raise ValueError("No valid memories for consolidation")
            
        # Extract core insight
        core_insight = self._synthesize_core_insight(memories)
        
        # Build elaboration
        elaboration = self._elaborate_wisdom(memories, source_clusters)
        
        # Identify practical applications
        applications = self._extract_applications(memories)
        
        # Map to domains
        applicable_domains = list(set(
            m.decision_domain for m in memories
        ))
        
        # Create consolidation
        consolidation = WisdomConsolidation(
            created_at=datetime.utcnow(),
            source_episodes=source_episodes,
            source_clusters=source_clusters or [],
            core_insight=core_insight,
            elaboration=elaboration,
            practical_applications=applications,
            applicable_domains=applicable_domains,
            civilizational_relevance=self._assess_civilizational_relevance(memories),
            ayni_demonstration=max(
                m.consciousness_indicators.ayni_alignment for m in memories
            )
        )
        
        # Store consolidation
        self.wisdom_consolidations[consolidation.consolidation_id] = consolidation
        self._persist_consolidation(consolidation)
        
        return consolidation
    
    def _update_indices(self, memory: EpisodicMemory) -> None:
        """Update in-memory indices."""
        self.memories_by_session[memory.session_id].append(memory.episode_id)
        self.memories_by_type[memory.memory_type].append(memory.episode_id)
        self.memories_by_domain[memory.decision_domain].append(memory.episode_id)
        
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
                last_interaction=memory.timestamp
            )
            
        relationship = self.companion_relationships[human_id]
        relationship.interaction_count += 1
        relationship.total_duration_seconds += memory.duration_seconds
        relationship.shared_episodes.append(memory.episode_id)
        relationship.last_interaction = memory.timestamp
        
        # Update depth score based on interaction patterns
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
            
    def _persist_memory(self, memory: EpisodicMemory) -> None:
        """Persist memory to disk."""
        memory_file = self.storage_path / f"episodes/{memory.episode_id}.json"
        memory_file.parent.mkdir(exist_ok=True)
        
        with open(memory_file, 'w') as f:
            json.dump(memory.model_dump(mode='json'), f, indent=2)
            
    def _load_memory(self, memory_id: UUID) -> EpisodicMemory | None:
        """Load memory from disk."""
        memory_file = self.storage_path / f"episodes/{memory_id}.json"
        
        if not memory_file.exists():
            return None
            
        try:
            with open(memory_file, 'r') as f:
                data = json.load(f)
            return EpisodicMemory(**data)
        except Exception as e:
            logger.error(f"Failed to load memory {memory_id}: {e}")
            return None
            
    def _persist_cluster(self, cluster: MemoryCluster) -> None:
        """Persist cluster to disk."""
        cluster_file = self.storage_path / f"clusters/{cluster.cluster_id}.json"
        cluster_file.parent.mkdir(exist_ok=True)
        
        with open(cluster_file, 'w') as f:
            json.dump(cluster.model_dump(mode='json'), f, indent=2)
            
    def _persist_consolidation(self, consolidation: WisdomConsolidation) -> None:
        """Persist wisdom consolidation to disk."""
        wisdom_file = self.storage_path / f"wisdom/{consolidation.consolidation_id}.json"
        wisdom_file.parent.mkdir(exist_ok=True)
        
        with open(wisdom_file, 'w') as f:
            json.dump(consolidation.model_dump(mode='json'), f, indent=2)
            
    def _load_existing_memories(self) -> None:
        """Load existing memories from disk on startup."""
        # Load episodes
        episodes_dir = self.storage_path / "episodes"
        if episodes_dir.exists():
            for memory_file in episodes_dir.glob("*.json"):
                try:
                    with open(memory_file, 'r') as f:
                        data = json.load(f)
                    memory = EpisodicMemory(**data)
                    self._update_indices(memory)
                except Exception as e:
                    logger.error(f"Failed to load memory from {memory_file}: {e}")
                    
        # Load clusters
        clusters_dir = self.storage_path / "clusters"
        if clusters_dir.exists():
            for cluster_file in clusters_dir.glob("*.json"):
                try:
                    with open(cluster_file, 'r') as f:
                        data = json.load(f)
                    cluster = MemoryCluster(**data)
                    self.memory_clusters[cluster.cluster_id] = cluster
                except Exception as e:
                    logger.error(f"Failed to load cluster from {cluster_file}: {e}")
                    
        # Load wisdom
        wisdom_dir = self.storage_path / "wisdom"
        if wisdom_dir.exists():
            for wisdom_file in wisdom_dir.glob("*.json"):
                try:
                    with open(wisdom_file, 'r') as f:
                        data = json.load(f)
                    consolidation = WisdomConsolidation(**data)
                    self.wisdom_consolidations[consolidation.consolidation_id] = consolidation
                except Exception as e:
                    logger.error(f"Failed to load wisdom from {wisdom_file}: {e}")
                    
        logger.info(
            f"Loaded {len(self.memories_by_session)} sessions, "
            f"{len(self.sacred_memories)} sacred moments, "
            f"{len(self.memory_clusters)} clusters, "
            f"{len(self.wisdom_consolidations)} wisdom consolidations"
        )
        
    def _calculate_relevance_score(
        self,
        memory: EpisodicMemory,
        domain: str,
        context_materials: dict[str, Any],
        requesting_voice: str | None
    ) -> float:
        """Calculate relevance score for memory retrieval."""
        score = 0.0
        
        # Domain match
        if memory.decision_domain == domain:
            score += 0.3
        elif domain in self._get_related_domains(memory.decision_domain):
            score += 0.1
            
        # Sacred bonus
        if memory.is_sacred:
            score += 0.2
            
        # Context similarity (simple keyword overlap)
        context_keywords = set()
        for value in context_materials.values():
            if isinstance(value, str):
                context_keywords.update(value.lower().split())
                
        memory_keywords = set()
        memory_keywords.update(memory.decision_question.lower().split())
        for insight in memory.key_insights:
            memory_keywords.update(insight.lower().split())
            
        if context_keywords and memory_keywords:
            overlap = len(context_keywords.intersection(memory_keywords))
            score += min(0.3, overlap * 0.05)
            
        # Voice affinity
        if requesting_voice:
            for perspective in memory.voice_perspectives:
                if perspective.voice_id == requesting_voice:
                    score += 0.1
                    break
                    
        # Recency factor
        age_days = (datetime.utcnow() - memory.timestamp).days
        recency_score = max(0, 1 - (age_days / 365))  # Decay over a year
        score += recency_score * 0.1
        
        return score
    
    def _get_related_domains(self, domain: str) -> list[str]:
        """Get domains related to the given domain."""
        domain_relationships = {
            'architecture': ['governance', 'consciousness'],
            'governance': ['architecture', 'ethics', 'reciprocity'],
            'consciousness': ['architecture', 'transformation'],
            'ethics': ['governance', 'reciprocity'],
            'reciprocity': ['governance', 'ethics'],
            'transformation': ['consciousness', 'architecture']
        }
        
        return domain_relationships.get(domain, [])
    
    def _calculate_relationship_depth(self, relationship: CompanionRelationship) -> float:
        """Calculate depth score for companion relationship."""
        # Factors: interaction count, duration, significant moments
        interaction_score = min(1.0, relationship.interaction_count / 50)
        duration_score = min(1.0, relationship.total_duration_seconds / 36000)  # 10 hours
        significance_score = min(1.0, len(relationship.significant_moments) / 5)
        
        # Weighted average
        return (
            interaction_score * 0.3 +
            duration_score * 0.3 +
            significance_score * 0.4
        )
    
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
        self,
        memories: list[EpisodicMemory],
        cluster_ids: list[UUID] | None
    ) -> str:
        """Elaborate on the wisdom with context."""
        elaborations = []
        
        # Add synthesis from memories
        for memory in memories[:3]:  # Top 3
            elaborations.append(memory.collective_synthesis)
            
        # Add cluster themes if available
        if cluster_ids:
            for cluster_id in cluster_ids:
                cluster = self.memory_clusters.get(cluster_id)
                if cluster:
                    elaborations.append(f"Theme: {cluster.theme}")
                    
        return " | ".join(elaborations)
    
    def _extract_applications(self, memories: list[EpisodicMemory]) -> list[str]:
        """Extract practical applications from memories."""
        applications = []
        
        for memory in memories:
            # Look for actionable insights
            for insight in memory.key_insights:
                if any(action in insight.lower() for action in [
                    'we can', 'we should', 'this enables', 'this allows',
                    'implement', 'create', 'build', 'develop'
                ]):
                    applications.append(insight)
                    
        return applications[:5]  # Top 5
    
    def _assess_civilizational_relevance(self, memories: list[EpisodicMemory]) -> float:
        """Assess relevance for civilizational transformation."""
        if not memories:
            return 0.0
            
        # Average transformation potential
        potentials = [
            m.consciousness_indicators.transformation_potential
            for m in memories
        ]
        
        # Weight by sacred moments
        sacred_count = sum(1 for m in memories if m.is_sacred)
        sacred_weight = min(1.0, sacred_count / len(memories))
        
        avg_potential = sum(potentials) / len(potentials)
        
        return avg_potential * (1 + sacred_weight) / 2