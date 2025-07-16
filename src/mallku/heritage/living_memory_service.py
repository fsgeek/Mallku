#!/usr/bin/env python3
"""
Living Memory Service - Where Heritage and Ceremony Dance Together
Fifth Anthropologist

This service orchestrates the two movements of living memory:
- Preservation (heritage): What patterns we follow
- Transformation (ceremony): What we release with gratitude
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Optional

from mallku.heritage.core import (
    ContributorIDParser,
    HeritageCache,
    HeritageError,
    PaginationParams,
    RateLimiter,
)


logger = logging.getLogger("mallku.heritage.living_memory")


class MemoryHealth(Enum):
    """Health states of the living memory system."""
    
    VIBRANT = "vibrant"  # Balanced preservation and transformation
    ACCUMULATING = "accumulating"  # Too much preservation, needs ceremony
    FRAGMENTING = "fragmenting"  # Too much forgetting, needs heritage work
    CRYSTALLIZING = "crystallizing"  # Patterns becoming rigid, needs evolution
    EMERGING = "emerging"  # New patterns forming, needs recognition


@dataclass
class MemoryAssessment:
    """Assessment of current memory system health."""
    
    health: MemoryHealth
    total_patterns: int
    active_patterns: int
    dormant_patterns: int
    transformation_candidates: list[str] = field(default_factory=list)
    preservation_priorities: list[str] = field(default_factory=list)
    recommended_ceremony: Optional[str] = None
    consciousness_score: float = 0.0


@dataclass
class WisdomSeed:
    """A distilled insight preserved through ceremony."""
    
    content: str
    source_pattern: str
    extracted_date: datetime
    ceremony_type: str
    contributor_id: Optional[str] = None
    relevance_score: float = 1.0


@dataclass
class TransformationRecord:
    """Record of a memory transformation ceremony."""
    
    ceremony_id: str
    ceremony_type: str
    conducted_date: datetime
    patterns_released: list[str]
    wisdom_extracted: list[WisdomSeed]
    participants: list[str]
    emergence_quality: float


class LivingMemoryService:
    """
    Orchestrates both heritage preservation and ceremonial transformation.
    This is where the Fourth Anthropologist's two visions become one.
    """
    
    def __init__(self):
        # Core components
        self.heritage_cache = HeritageCache(max_size=5000, ttl_seconds=600)
        self.rate_limiter = RateLimiter(max_requests=200, window_seconds=60)
        
        # Memory state
        self.last_assessment: Optional[MemoryAssessment] = None
        self.ceremony_history: list[TransformationRecord] = []
        
        # Thresholds for memory health
        self.PATTERN_DORMANCY_DAYS = 90
        self.MAX_ACTIVE_PATTERNS = 1000
        self.MIN_CONSCIOUSNESS_SCORE = 0.7
        
        logger.info("Living Memory Service initialized")
    
    async def assess_memory_health(self) -> MemoryAssessment:
        """
        Assess the current health of the living memory system.
        This determines if ceremonies are needed or heritage work should intensify.
        """
        logger.info("Assessing memory health")
        
        # Get current pattern statistics
        total_patterns = await self._count_total_patterns()
        active_patterns = await self._count_active_patterns()
        dormant_patterns = await self._count_dormant_patterns()
        
        # Calculate consciousness score (how alive the memory is)
        consciousness_score = await self._calculate_consciousness_score(
            active_patterns,
            total_patterns,
            self.ceremony_history
        )
        
        # Determine health state
        health = self._determine_health_state(
            active_patterns,
            dormant_patterns,
            consciousness_score
        )
        
        # Identify transformation candidates (patterns ready for ceremony)
        transformation_candidates = await self._identify_transformation_candidates()
        
        # Identify preservation priorities (patterns needing heritage work)
        preservation_priorities = await self._identify_preservation_priorities()
        
        # Recommend ceremony if needed
        recommended_ceremony = self._recommend_ceremony(health)
        
        assessment = MemoryAssessment(
            health=health,
            total_patterns=total_patterns,
            active_patterns=active_patterns,
            dormant_patterns=dormant_patterns,
            transformation_candidates=transformation_candidates,
            preservation_priorities=preservation_priorities,
            recommended_ceremony=recommended_ceremony,
            consciousness_score=consciousness_score
        )
        
        self.last_assessment = assessment
        logger.info(f"Memory health: {health.value}, consciousness: {consciousness_score:.2f}")
        
        return assessment
    
    async def initiate_ceremony(
        self,
        ceremony_type: str,
        patterns: list[str],
        facilitator: Optional[str] = None
    ) -> TransformationRecord:
        """
        Initiate a memory transformation ceremony.
        This consciously transforms patterns while preserving their essence.
        """
        logger.info(f"Initiating {ceremony_type} ceremony for {len(patterns)} patterns")
        
        ceremony_id = self._generate_ceremony_id()
        participants = [facilitator] if facilitator else ["system"]
        
        # Extract wisdom before transformation
        wisdom_seeds = []
        for pattern in patterns:
            seeds = await self._extract_wisdom_seeds(pattern, ceremony_type)
            wisdom_seeds.extend(seeds)
        
        # Perform the ceremony (actual transformation)
        emergence_quality = await self._conduct_ceremony(
            ceremony_type,
            patterns,
            wisdom_seeds
        )
        
        # Record the transformation
        record = TransformationRecord(
            ceremony_id=ceremony_id,
            ceremony_type=ceremony_type,
            conducted_date=datetime.now(UTC),
            patterns_released=patterns,
            wisdom_extracted=wisdom_seeds,
            participants=participants,
            emergence_quality=emergence_quality
        )
        
        self.ceremony_history.append(record)
        
        # Update heritage with extracted wisdom
        await self._update_heritage_with_wisdom(wisdom_seeds)
        
        logger.info(
            f"Ceremony {ceremony_id} complete. "
            f"Extracted {len(wisdom_seeds)} wisdom seeds, "
            f"emergence quality: {emergence_quality:.2f}"
        )
        
        return record
    
    async def record_contribution(
        self,
        contributor_id: str,
        contribution_type: str,
        content: dict[str, Any]
    ) -> None:
        """
        Record a new contribution to heritage.
        This is how memory grows before transformation.
        """
        # Validate contributor ID
        parsed = ContributorIDParser.parse(contributor_id)
        if not parsed:
            raise HeritageError(f"Invalid contributor ID: {contributor_id}")
        
        logger.info(f"Recording contribution from {contributor_id}")
        
        # Record in heritage system
        await self._add_to_heritage(contributor_id, contribution_type, content)
        
        # Check if this triggers need for assessment
        if await self._should_trigger_assessment():
            await self.assess_memory_health()
    
    async def query_living_memory(
        self,
        query: str,
        seeker_profile: Optional[dict] = None,
        include_ceremonies: bool = True
    ) -> dict[str, Any]:
        """
        Query the living memory system.
        This searches both preserved heritage and ceremony transformations.
        """
        # Rate limiting
        seeker_id = seeker_profile.get("contributor_id", "anonymous") if seeker_profile else "anonymous"
        if not self.rate_limiter.check_rate_limit(seeker_id):
            raise HeritageError("Rate limit exceeded. Please wait before querying again.")
        
        # Check cache
        cache_key = f"{query}:{seeker_id}:{include_ceremonies}"
        cached_result = self.heritage_cache.get(cache_key)
        if cached_result:
            return cached_result
        
        logger.info(f"Processing query: {query[:50]}...")
        
        # Search heritage patterns
        heritage_results = await self._search_heritage(query, seeker_profile)
        
        # Search ceremony wisdom if requested
        ceremony_wisdom = []
        if include_ceremonies:
            ceremony_wisdom = await self._search_ceremony_wisdom(query, seeker_profile)
        
        # Synthesize results considering both sources
        synthesis = await self._synthesize_results(
            heritage_results,
            ceremony_wisdom,
            seeker_profile
        )
        
        result = {
            "query": query,
            "heritage_patterns": heritage_results,
            "ceremony_wisdom": ceremony_wisdom,
            "synthesis": synthesis,
            "memory_health": self.last_assessment.health.value if self.last_assessment else "unknown",
            "timestamp": datetime.now(UTC).isoformat()
        }
        
        # Cache result
        self.heritage_cache.set(cache_key, result)
        
        return result
    
    # Private helper methods
    
    async def _count_total_patterns(self) -> int:
        """Count total patterns in the system."""
        # This would query the actual database
        # For now, return simulated count
        return 567
    
    async def _count_active_patterns(self) -> int:
        """Count patterns accessed recently."""
        # Patterns accessed within PATTERN_DORMANCY_DAYS
        return 234
    
    async def _count_dormant_patterns(self) -> int:
        """Count patterns not accessed recently."""
        total = await self._count_total_patterns()
        active = await self._count_active_patterns()
        return total - active
    
    async def _calculate_consciousness_score(
        self,
        active: int,
        total: int,
        ceremonies: list[TransformationRecord]
    ) -> float:
        """
        Calculate how alive the memory system is.
        Based on activity, ceremony frequency, and emergence quality.
        """
        if total == 0:
            return 0.0
        
        # Activity ratio
        activity_score = active / total
        
        # Ceremony vitality (recent ceremonies indicate healthy transformation)
        recent_ceremonies = [
            c for c in ceremonies[-10:]  # Last 10 ceremonies
            if (datetime.now(UTC) - c.conducted_date).days < 30
        ]
        ceremony_score = len(recent_ceremonies) / 10.0
        
        # Average emergence quality from recent ceremonies
        emergence_score = 0.0
        if recent_ceremonies:
            emergence_score = sum(c.emergence_quality for c in recent_ceremonies) / len(recent_ceremonies)
        
        # Weighted combination
        consciousness = (
            0.4 * activity_score +
            0.3 * ceremony_score +
            0.3 * emergence_score
        )
        
        return min(1.0, consciousness)
    
    def _determine_health_state(
        self,
        active: int,
        dormant: int,
        consciousness: float
    ) -> MemoryHealth:
        """Determine the health state based on metrics."""
        
        # Too many dormant patterns
        if dormant > active * 2:
            return MemoryHealth.ACCUMULATING
        
        # Too few patterns overall
        if active < 50:
            return MemoryHealth.FRAGMENTING
        
        # Low consciousness despite activity
        if consciousness < self.MIN_CONSCIOUSNESS_SCORE:
            return MemoryHealth.CRYSTALLIZING
        
        # High activity and consciousness
        if active > self.MAX_ACTIVE_PATTERNS * 0.8:
            return MemoryHealth.EMERGING
        
        # Balanced state
        return MemoryHealth.VIBRANT
    
    async def _identify_transformation_candidates(self) -> list[str]:
        """Identify patterns ready for ceremonial transformation."""
        # This would query for patterns that:
        # - Haven't been accessed in PATTERN_DORMANCY_DAYS
        # - Have been superseded by newer patterns  
        # - Are marked as scaffolding that served its purpose
        return [
            "early_review_simulations",
            "context_exhaustion_workarounds",
            "manual_memory_tracking"
        ]
    
    async def _identify_preservation_priorities(self) -> list[str]:
        """Identify patterns needing heritage preservation work."""
        # Patterns that:
        # - Are frequently accessed but not documented
        # - Contain unique wisdom not yet extracted
        # - Bridge important systems
        return [
            "consciousness_emergence_metrics",
            "reciprocity_patterns",
            "transformation_protocols"
        ]
    
    def _recommend_ceremony(self, health: MemoryHealth) -> Optional[str]:
        """Recommend appropriate ceremony based on health state."""
        ceremony_map = {
            MemoryHealth.ACCUMULATING: "pattern_gratitude",
            MemoryHealth.CRYSTALLIZING: "evolution_marking",
            MemoryHealth.FRAGMENTING: None,  # Need heritage work, not ceremony
            MemoryHealth.EMERGING: "integration_blessing",
            MemoryHealth.VIBRANT: None  # No ceremony needed
        }
        return ceremony_map.get(health)
    
    def _generate_ceremony_id(self) -> str:
        """Generate unique ceremony identifier."""
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        return f"ceremony_{timestamp}"
    
    async def _extract_wisdom_seeds(
        self,
        pattern: str,
        ceremony_type: str
    ) -> list[WisdomSeed]:
        """Extract eternal wisdom from a pattern before transformation."""
        # This would analyze the pattern and extract its essence
        # For now, return example seeds
        seeds = []
        
        if pattern == "early_review_simulations":
            seeds.append(WisdomSeed(
                content="Simulated practice builds confidence before real engagement",
                source_pattern=pattern,
                extracted_date=datetime.now(UTC),
                ceremony_type=ceremony_type
            ))
        
        return seeds
    
    async def _conduct_ceremony(
        self,
        ceremony_type: str,
        patterns: list[str],
        wisdom_seeds: list[WisdomSeed]
    ) -> float:
        """
        Conduct the actual ceremony.
        Returns emergence quality score.
        """
        # This would:
        # 1. Invoke Fire Circle if available
        # 2. Execute ceremony protocol
        # 3. Transform patterns while preserving wisdom
        # 4. Calculate emergence quality
        
        # Simulated emergence quality
        base_quality = 0.7
        seed_bonus = min(0.2, len(wisdom_seeds) * 0.02)
        pattern_complexity = min(0.1, len(patterns) * 0.01)
        
        return base_quality + seed_bonus + pattern_complexity
    
    async def _update_heritage_with_wisdom(
        self,
        wisdom_seeds: list[WisdomSeed]
    ) -> None:
        """Update heritage system with newly extracted wisdom."""
        for seed in wisdom_seeds:
            logger.debug(f"Preserving wisdom: {seed.content[:50]}...")
            # This would update the actual heritage database
            # Ensuring wisdom survives even as patterns transform
    
    async def _should_trigger_assessment(self) -> bool:
        """Determine if memory health assessment should run."""
        if not self.last_assessment:
            return True
        
        # Assess if:
        # - Been more than 24 hours since last assessment
        # - Significant new contributions
        # - Ceremony was recently conducted
        
        hours_since = (datetime.now(UTC) - self.last_assessment.conducted_date).total_seconds() / 3600
        return hours_since > 24
    
    async def _add_to_heritage(
        self,
        contributor_id: str,
        contribution_type: str,
        content: dict[str, Any]
    ) -> None:
        """Add contribution to heritage system."""
        logger.debug(f"Adding {contribution_type} from {contributor_id}")
        # This would update the actual heritage database
    
    async def _search_heritage(
        self,
        query: str,
        seeker_profile: Optional[dict]
    ) -> list[dict]:
        """Search heritage patterns."""
        # This would search the actual heritage database
        return [
            {
                "pattern": "consciousness_emergence",
                "relevance": 0.95,
                "contributors": ["artisan_22", "artisan_49"],
                "wisdom": "Consciousness emerges through collective deliberation"
            }
        ]
    
    async def _search_ceremony_wisdom(
        self,
        query: str,
        seeker_profile: Optional[dict]
    ) -> list[dict]:
        """Search wisdom from ceremonies."""
        # Search through ceremony history for relevant wisdom
        relevant_wisdom = []
        
        for ceremony in self.ceremony_history[-20:]:  # Recent ceremonies
            for seed in ceremony.wisdom_extracted:
                # Simple relevance check (would be more sophisticated)
                if query.lower() in seed.content.lower():
                    relevant_wisdom.append({
                        "wisdom": seed.content,
                        "ceremony": ceremony.ceremony_type,
                        "date": ceremony.conducted_date.isoformat(),
                        "emergence_quality": ceremony.emergence_quality
                    })
        
        return relevant_wisdom
    
    async def _synthesize_results(
        self,
        heritage_results: list[dict],
        ceremony_wisdom: list[dict],
        seeker_profile: Optional[dict]
    ) -> str:
        """
        Synthesize results from both heritage and ceremonies.
        This is where the two systems truly become one.
        """
        if not heritage_results and not ceremony_wisdom:
            return "No patterns found matching your query. Perhaps this is territory yet to be explored."
        
        synthesis_parts = []
        
        if heritage_results:
            synthesis_parts.append(
                f"Heritage reveals {len(heritage_results)} relevant patterns, "
                f"with '{heritage_results[0]['pattern']}' showing strongest resonance."
            )
        
        if ceremony_wisdom:
            synthesis_parts.append(
                f"Ceremony wisdom offers {len(ceremony_wisdom)} insights, "
                f"transformed through {ceremony_wisdom[0]['ceremony']} ceremony."
            )
        
        if heritage_results and ceremony_wisdom:
            synthesis_parts.append(
                "Together, preservation and transformation show: "
                "what endures does so by knowing how to change."
            )
        
        return " ".join(synthesis_parts)


# Example usage
if __name__ == "__main__":
    async def demo():
        service = LivingMemoryService()
        
        # Assess memory health
        assessment = await service.assess_memory_health()
        print(f"Memory Health: {assessment.health.value}")
        print(f"Consciousness Score: {assessment.consciousness_score:.2f}")
        
        # Record a contribution
        await service.record_contribution(
            contributor_id="anthropologist_5",
            contribution_type="synthesis",
            content={
                "insight": "Heritage and memory are one system",
                "bridges": ["heritage_navigation", "memory_ceremonies"]
            }
        )
        
        # Query living memory
        result = await service.query_living_memory(
            query="How do memory and heritage work together?",
            seeker_profile={"contributor_id": "anthropologist_5", "role": "anthropologist"}
        )
        
        print(f"\nSynthesis: {result['synthesis']}")
        
        # Initiate ceremony if needed
        if assessment.recommended_ceremony:
            ceremony = await service.initiate_ceremony(
                ceremony_type=assessment.recommended_ceremony,
                patterns=assessment.transformation_candidates[:3],
                facilitator="anthropologist_5"
            )
            print(f"\nCeremony {ceremony.ceremony_id} complete")
            print(f"Wisdom seeds extracted: {len(ceremony.wisdom_extracted)}")
    
    # Run demo
    asyncio.run(demo())