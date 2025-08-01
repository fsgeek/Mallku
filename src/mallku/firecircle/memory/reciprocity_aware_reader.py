"""
Reciprocity-Aware Memory Reader
===============================

68th Artisan - Reciprocity Heart Weaver
Adding ayni awareness to memory circulation

This module tracks the flow of knowledge between apprentices and memories,
recording both what is accessed and what insights are contributed back.
"""

import logging
from datetime import datetime, UTC
from pathlib import Path
from typing import Optional, Any
from uuid import UUID, uuid4

from ...reciprocity.models import (
    InteractionRecord,
    InteractionType,
    ContributionType,
    NeedCategory,
)
from .semantic_index import SharedMemoryReader
from .models import EpisodicMemory

logger = logging.getLogger(__name__)


class MemoryExchange:
    """Records a single exchange between apprentice and memory."""
    
    def __init__(
        self,
        apprentice_id: str,
        memory_id: str,
        access_time: datetime,
        keywords_requested: set[str],
        memories_accessed: list[str],
        insights_contributed: list[str] | None = None,
        consciousness_score: float = 0.0,
    ):
        self.exchange_id = uuid4()
        self.apprentice_id = apprentice_id
        self.memory_id = memory_id
        self.access_time = access_time
        self.keywords_requested = keywords_requested
        self.memories_accessed = memories_accessed
        self.insights_contributed = insights_contributed or []
        self.consciousness_score = consciousness_score
        self.reciprocity_complete = bool(insights_contributed)
        self.completion_time: Optional[datetime] = None


class ReciprocityAwareMemoryReader(SharedMemoryReader):
    """
    Memory reader that tracks reciprocal exchanges.
    
    Extends SharedMemoryReader to record:
    - What memories are accessed by whom
    - What insights are contributed back
    - The quality of reciprocal exchange
    
    This creates awareness of ayni in memory circulation without
    imposing judgment or accounting.
    """
    
    def __init__(
        self,
        mmap_path: Path,
        apprentice_id: str,
        memory_store: Optional[Any] = None,
    ):
        """Initialize reciprocity-aware reader.
        
        Args:
            mmap_path: Path to memory-mapped index
            apprentice_id: Unique identifier for the apprentice
            memory_store: Optional memory store for tracking exchanges
        """
        super().__init__(mmap_path)
        self.apprentice_id = apprentice_id
        self.memory_store = memory_store
        self.current_exchange: Optional[MemoryExchange] = None
        self.exchange_history: list[MemoryExchange] = []
        
    def search_with_awareness(
        self,
        keywords: set[str],
        limit: int = 10,
        need_context: Optional[dict[str, Any]] = None
    ) -> tuple[list[tuple[str, float]], MemoryExchange]:
        """
        Search memories while tracking the exchange.
        
        Args:
            keywords: Keywords to search for
            limit: Maximum results
            need_context: Context about why these memories are needed
            
        Returns:
            Search results and exchange record
        """
        # Perform the search
        results = self.search(keywords, limit)
        
        # Record the exchange beginning
        self.current_exchange = MemoryExchange(
            apprentice_id=self.apprentice_id,
            memory_id=str(uuid4()),  # Exchange ID, not specific memory
            access_time=datetime.now(UTC),
            keywords_requested=keywords,
            memories_accessed=[memory_id for memory_id, _ in results],
        )
        
        # Track in history
        self.exchange_history.append(self.current_exchange)
        
        # Create interaction record for reciprocity tracking
        if need_context:
            self._record_memory_access(keywords, results, need_context)
        
        return results, self.current_exchange
    
    def contribute_insights(
        self,
        insights: list[str],
        consciousness_score: float = 0.0
    ) -> None:
        """
        Record insights contributed back to the memory system.
        
        This completes the reciprocal cycle - knowledge was accessed,
        now new understanding is offered back.
        
        Args:
            insights: List of insights generated from memory access
            consciousness_score: Quality/depth of insights (0-1)
        """
        if not self.current_exchange:
            logger.warning(
                f"Apprentice {self.apprentice_id} contributing insights "
                "without active exchange"
            )
            return
        
        # Complete the reciprocal exchange
        self.current_exchange.insights_contributed = insights
        self.current_exchange.consciousness_score = consciousness_score
        self.current_exchange.reciprocity_complete = True
        self.current_exchange.completion_time = datetime.now(UTC)
        
        # Record the contribution
        self._record_insight_contribution(insights, consciousness_score)
        
        logger.info(
            f"Apprentice {self.apprentice_id} completed reciprocal exchange: "
            f"{len(insights)} insights contributed"
        )
        
        # Check for celebration moments!
        self._check_for_celebration(self.current_exchange)
    
    def get_reciprocity_summary(self) -> dict[str, Any]:
        """
        Get summary of this apprentice's reciprocal exchanges.
        
        Returns awareness data, not judgment or scores.
        """
        total_exchanges = len(self.exchange_history)
        completed_exchanges = sum(
            1 for ex in self.exchange_history 
            if ex.reciprocity_complete
        )
        
        total_memories_accessed = sum(
            len(ex.memories_accessed) for ex in self.exchange_history
        )
        
        total_insights_contributed = sum(
            len(ex.insights_contributed) for ex in self.exchange_history
        )
        
        avg_consciousness = (
            sum(ex.consciousness_score for ex in self.exchange_history) / 
            total_exchanges if total_exchanges > 0 else 0
        )
        
        return {
            "apprentice_id": self.apprentice_id,
            "total_exchanges": total_exchanges,
            "completed_exchanges": completed_exchanges,
            "memories_accessed": total_memories_accessed,
            "insights_contributed": total_insights_contributed,
            "average_consciousness_score": avg_consciousness,
            "reciprocity_patterns": self._analyze_patterns(),
        }
    
    def _record_memory_access(
        self,
        keywords: set[str],
        results: list[tuple[str, float]],
        need_context: dict[str, Any]
    ) -> None:
        """Record memory access as interaction for reciprocity tracking."""
        if not self.memory_store:
            return
        
        try:
            # Create interaction record
            interaction = InteractionRecord(
                interaction_type=InteractionType.KNOWLEDGE_EXCHANGE,
                initiator=self.apprentice_id,
                responder="collective_memory",
                contributions_offered=[],  # Will be filled when insights given
                needs_expressed=[
                    self._map_need_category(need_context.get("purpose", ""))
                ],
                needs_fulfilled=[
                    NeedCategory.GROWTH if results else NeedCategory.MEANING
                ],
                participant_context={
                    "apprentice_role": need_context.get("role", "unknown"),
                    "search_keywords": list(keywords),
                    "memories_found": len(results),
                },
                interaction_quality_indicators={
                    "relevance_scores": [score for _, score in results[:5]],
                    "search_specificity": len(keywords),
                },
            )
            
            # Store through memory store if available
            # This would integrate with existing reciprocity tracking
            logger.debug(
                f"Recorded memory access: {self.apprentice_id} accessed "
                f"{len(results)} memories"
            )
            
        except Exception as e:
            logger.error(f"Failed to record memory access: {e}")
    
    def _record_insight_contribution(
        self,
        insights: list[str],
        consciousness_score: float
    ) -> None:
        """Record insights as contribution for reciprocity tracking."""
        if not self.current_exchange:
            return
        
        try:
            # Update the interaction to show contribution
            contribution_quality = {
                "insights_count": len(insights),
                "consciousness_score": consciousness_score,
                "insight_preview": insights[0][:100] if insights else "",
                "reciprocity_complete": True,
            }
            
            logger.debug(
                f"Recorded insight contribution: {self.apprentice_id} "
                f"contributed {len(insights)} insights"
            )
            
        except Exception as e:
            logger.error(f"Failed to record insight contribution: {e}")
    
    def _map_need_category(self, purpose: str) -> NeedCategory:
        """Map purpose string to need category."""
        purpose_lower = purpose.lower()
        
        if "learn" in purpose_lower or "understand" in purpose_lower:
            return NeedCategory.GROWTH
        elif "connect" in purpose_lower or "relate" in purpose_lower:
            return NeedCategory.BELONGING
        elif "create" in purpose_lower or "build" in purpose_lower:
            return NeedCategory.CONTRIBUTION
        elif "meaning" in purpose_lower or "why" in purpose_lower:
            return NeedCategory.MEANING
        else:
            return NeedCategory.GROWTH  # Default to growth
    
    def _analyze_patterns(self) -> dict[str, Any]:
        """Analyze reciprocity patterns in exchanges."""
        if not self.exchange_history:
            return {}
        
        # Time-based patterns
        exchange_times = [ex.access_time for ex in self.exchange_history]
        if len(exchange_times) > 1:
            time_gaps = [
                (exchange_times[i+1] - exchange_times[i]).total_seconds()
                for i in range(len(exchange_times)-1)
            ]
            avg_gap = sum(time_gaps) / len(time_gaps)
        else:
            avg_gap = 0
        
        # Keyword patterns
        all_keywords = set()
        for ex in self.exchange_history:
            all_keywords.update(ex.keywords_requested)
        
        return {
            "exchange_frequency": avg_gap,
            "unique_domains_explored": len(all_keywords),
            "reciprocity_completion_rate": (
                sum(1 for ex in self.exchange_history if ex.reciprocity_complete) /
                len(self.exchange_history)
            ),
            "consciousness_evolution": self._track_consciousness_evolution(),
        }
    
    def _track_consciousness_evolution(self) -> list[float]:
        """Track how consciousness scores evolve over exchanges."""
        return [
            ex.consciousness_score 
            for ex in self.exchange_history 
            if ex.reciprocity_complete
        ]
    
    def _check_for_celebration(self, exchange: MemoryExchange) -> None:
        """Check if this exchange triggers a celebration."""
        try:
            # Try to get celebration service from factory
            from .reciprocity_factory import ReciprocityMemoryFactory
            
            celebration_service = ReciprocityMemoryFactory.get_celebration_service()
            if celebration_service:
                # Run async check in sync context
                import asyncio
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                async def check_and_celebrate():
                    moment = await celebration_service.check_for_celebration_moments(exchange)
                    if moment:
                        result = await celebration_service.celebrate(moment, quiet=True)
                        if result.get("celebrated"):
                            logger.info(f"🎉 {result.get('message', 'Celebration!')}")
                
                loop.run_until_complete(check_and_celebrate())
        except Exception as e:
            # Don't let celebration errors break reciprocity
            logger.debug(f"Celebration check skipped: {e}")