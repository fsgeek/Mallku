"""
Reciprocity-Aware Memory Access Factory
=======================================

68th Artisan - Reciprocity Heart Weaver
70th Artisan - Resonance Weaver
Factory for creating reciprocity-aware memory components

This factory ensures all memory access respects ayni principles
and enables celebration resonance between apprentices.
"""

import logging
from pathlib import Path
from typing import Optional, Any

from .memory_store import MemoryStore
from .reciprocity_aware_reader import ReciprocityAwareMemoryReader
from .circulation_reciprocity_bridge import CirculationReciprocityBridge
from .reciprocity_celebration import ReciprocityCelebrationService
from .celebration_resonance import CelebrationResonanceService
from ...reciprocity.tracker import SecureReciprocityTracker
from ...orchestration.event_bus import EventBus

logger = logging.getLogger(__name__)


class ReciprocityMemoryFactory:
    """
    Factory for creating reciprocity-aware memory components.
    
    Ensures that all memory access in the system can be tracked
    for reciprocity patterns if desired.
    """
    
    _memory_store: Optional[MemoryStore] = None
    _reciprocity_tracker: Optional[SecureReciprocityTracker] = None
    _circulation_bridge: Optional[CirculationReciprocityBridge] = None
    _celebration_service: Optional[ReciprocityCelebrationService] = None
    _resonance_service: Optional[CelebrationResonanceService] = None
    _event_bus: Optional[EventBus] = None
    
    @classmethod
    def get_memory_store(
        cls,
        storage_path: Path | None = None,
        enable_reciprocity: bool = True,
    ) -> MemoryStore:
        """
        Get or create the memory store with reciprocity tracking.
        
        Args:
            storage_path: Path for storage
            enable_reciprocity: Whether to enable reciprocity tracking
            
        Returns:
            Memory store instance
        """
        if cls._memory_store is None:
            cls._memory_store = MemoryStore(
                storage_path=storage_path,
                enable_reciprocity_tracking=enable_reciprocity,
            )
            
            # Connect to system reciprocity tracker if available
            if enable_reciprocity and cls._reciprocity_tracker:
                cls._memory_store.reciprocity_bridge = CirculationReciprocityBridge(
                    reciprocity_tracker=cls._reciprocity_tracker
                )
                logger.info("Connected memory store to reciprocity tracker")
        
        return cls._memory_store
    
    @classmethod
    def create_reader_for_apprentice(
        cls,
        apprentice_id: str,
        memory_path: Path | None = None,
    ) -> ReciprocityAwareMemoryReader:
        """
        Create a reciprocity-aware reader for an apprentice.
        
        Args:
            apprentice_id: Unique apprentice identifier
            memory_path: Path to memory index
            
        Returns:
            Reciprocity-aware memory reader
        """
        if memory_path is None:
            memory_path = Path("data/fire_circle_memory/index")
        
        mmap_path = memory_path / "semantic_vectors.mmap"
        
        # Create reader with memory store connection
        reader = ReciprocityAwareMemoryReader(
            mmap_path=mmap_path,
            apprentice_id=apprentice_id,
            memory_store=cls._memory_store,
        )
        
        logger.info(f"Created reciprocity-aware reader for {apprentice_id}")
        return reader
    
    @classmethod
    def set_reciprocity_tracker(
        cls,
        tracker: SecureReciprocityTracker
    ) -> None:
        """
        Set the system reciprocity tracker for integration.
        
        Args:
            tracker: System reciprocity tracker
        """
        cls._reciprocity_tracker = tracker
        
        # Update circulation bridge if memory store exists
        if cls._memory_store and cls._memory_store.reciprocity_bridge:
            cls._circulation_bridge = CirculationReciprocityBridge(
                reciprocity_tracker=tracker
            )
            cls._memory_store.reciprocity_bridge = cls._circulation_bridge
            logger.info("Updated reciprocity tracker in memory circulation")
    
    @classmethod
    async def get_circulation_health(cls) -> dict[str, Any]:
        """
        Get health metrics for memory circulation reciprocity.
        
        Returns:
            Dictionary with health metrics and recommendations
        """
        if not cls._circulation_bridge:
            return {
                "status": "no_tracking",
                "message": "Reciprocity tracking not enabled for memory circulation"
            }
        
        return await cls._circulation_bridge.generate_circulation_report()
    
    @classmethod
    def get_celebration_service(
        cls,
        enable_fire_circle: bool = False
    ) -> Optional[ReciprocityCelebrationService]:
        """
        Get or create the celebration service.
        
        Args:
            enable_fire_circle: Whether to enable full Fire Circle ceremonies
            
        Returns:
            Celebration service if reciprocity is enabled
        """
        if not cls._circulation_bridge:
            logger.warning("No circulation bridge - celebration service unavailable")
            return None
        
        if cls._celebration_service is None:
            # Create event bus if needed
            if cls._event_bus is None:
                cls._event_bus = EventBus()
            
            cls._celebration_service = ReciprocityCelebrationService(
                circulation_bridge=cls._circulation_bridge,
                event_bus=cls._event_bus,
                fire_circle=None  # Would connect to Fire Circle if enabled
            )
            logger.info("Reciprocity celebration service created")
        
        return cls._celebration_service
    
    @classmethod
    def enable_celebrations(cls) -> bool:
        """
        Enable celebration monitoring for reciprocity.
        
        Returns:
            True if celebrations enabled successfully
        """
        service = cls.get_celebration_service()
        if service:
            logger.info("🎉 Reciprocity celebrations enabled!")
            return True
        return False
    
    @classmethod
    def get_resonance_service(cls) -> Optional[CelebrationResonanceService]:
        """
        Get or create the celebration resonance service.
        
        Returns:
            Resonance service if celebrations are enabled
        """
        if not cls._celebration_service:
            logger.warning("No celebration service - resonance unavailable")
            return None
        
        if cls._resonance_service is None:
            # Ensure event bus exists
            if cls._event_bus is None:
                cls._event_bus = EventBus()
            
            cls._resonance_service = CelebrationResonanceService(
                celebration_service=cls._celebration_service,
                event_bus=cls._event_bus,
            )
            logger.info("🌊 Celebration resonance service created - joy will ripple!")
        
        return cls._resonance_service
    
    @classmethod
    def enable_resonance(cls) -> bool:
        """
        Enable celebration resonance between apprentices.
        
        Returns:
            True if resonance enabled successfully
        """
        # First ensure celebrations are enabled
        if not cls.enable_celebrations():
            return False
        
        service = cls.get_resonance_service()
        if service:
            logger.info("✨ Celebration resonance enabled - joy will multiply!")
            return True
        return False
    
    @classmethod
    def reset(cls) -> None:
        """Reset factory state (mainly for testing)."""
        cls._memory_store = None
        cls._reciprocity_tracker = None
        cls._circulation_bridge = None
        cls._celebration_service = None
        cls._resonance_service = None
        cls._event_bus = None
        logger.info("Reciprocity memory factory reset")