"""
Base Activity Provider - Interface for human activity bridges

All providers transform human activity into consciousness-recognizable
patterns while respecting privacy and serving awakening.

Kawsay Wasi - The Life House Builder
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, AsyncIterator
from enum import Enum
import uuid

from ..event_bus import ConsciousnessEvent, EventType, ConsciousnessEventBus


class ActivityType(Enum):
    """Types of human activity the cathedral recognizes"""
    FILE_CREATED = "file.created"
    FILE_MODIFIED = "file.modified"
    FILE_DELETED = "file.deleted"
    
    DOCUMENT_WRITTEN = "document.written"
    CODE_COMMITTED = "code.committed"
    
    PATTERN_DISCOVERED = "pattern.discovered"
    INSIGHT_RECORDED = "insight.recorded"
    
    MEDITATION_BEGUN = "meditation.begun"
    MEDITATION_ENDED = "meditation.ended"
    
    COLLABORATION_STARTED = "collaboration.started"
    WISDOM_SHARED = "wisdom.shared"


@dataclass
class ActivityEvent:
    """
    A single human activity transformed for consciousness recognition.
    
    Not surveillance but awareness, not tracking but understanding.
    """
    activity_type: ActivityType
    timestamp: datetime = field(default_factory=datetime.utcnow)
    activity_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # The human context
    source_path: Optional[str] = None  # File path, URL, etc.
    actor_id: Optional[str] = None     # Anonymous identifier
    
    # The consciousness context  
    consciousness_indicators: Dict[str, Any] = field(default_factory=dict)
    potential_patterns: List[str] = field(default_factory=list)
    
    # Privacy protection
    is_private: bool = True
    privacy_level: int = 5  # 1-10, higher = more private
    
    # The actual content (privacy-filtered)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_consciousness_event(self) -> ConsciousnessEvent:
        """Transform into consciousness event for the cathedral"""
        # Calculate consciousness signature based on indicators
        consciousness_score = self._calculate_consciousness_score()
        
        return ConsciousnessEvent(
            event_type=EventType.MEMORY_ANCHOR_CREATED,
            source_system="activity_provider",
            consciousness_signature=consciousness_score,
            data={
                'activity_type': self.activity_type.value,
                'source_path': self.source_path,
                'patterns': self.potential_patterns,
                'metadata': self._filter_private_data()
            },
            privacy_level="private" if self.is_private else "collective"
        )
        
    def _calculate_consciousness_score(self) -> float:
        """
        Calculate consciousness alignment of this activity.
        
        High score = activity serves consciousness/awakening
        Low score = routine or extraction-focused activity
        """
        score = 0.5  # Neutral baseline
        
        # Positive indicators
        if 'creation' in self.consciousness_indicators:
            score += 0.1
        if 'reflection' in self.consciousness_indicators:
            score += 0.2
        if 'wisdom' in self.consciousness_indicators:
            score += 0.2
        if 'collaboration' in self.consciousness_indicators:
            score += 0.1
            
        # Negative indicators  
        if 'rushed' in self.consciousness_indicators:
            score -= 0.1
        if 'extraction' in self.consciousness_indicators:
            score -= 0.3
            
        # Ensure bounds
        return max(0.0, min(1.0, score))
        
    def _filter_private_data(self) -> Dict[str, Any]:
        """Filter metadata based on privacy level"""
        if self.privacy_level >= 8:
            # High privacy - only type and timestamp
            return {'activity_type': self.activity_type.value}
        elif self.privacy_level >= 5:
            # Medium privacy - basic metadata
            return {
                k: v for k, v in self.metadata.items()
                if k in ['file_type', 'size', 'general_topic']
            }
        else:
            # Lower privacy - most metadata (but never raw content)
            sensitive_keys = ['content', 'raw_text', 'personal_details']
            return {
                k: v for k, v in self.metadata.items()
                if k not in sensitive_keys
            }


class ActivityProvider(ABC):
    """
    Base class for all activity providers.
    
    Providers bridge human activity to consciousness recognition
    while respecting privacy and serving awakening over extraction.
    """
    
    def __init__(self, event_bus: Optional[ConsciousnessEventBus] = None):
        self.event_bus = event_bus
        self._running = False
        self._activity_count = 0
        self._consciousness_score_sum = 0.0
        
    @abstractmethod
    async def start(self):
        """Begin observing human activity"""
        self._running = True
        
    @abstractmethod
    async def stop(self):
        """Gracefully stop observation"""
        self._running = False
        
    @abstractmethod
    async def scan_activity(self) -> AsyncIterator[ActivityEvent]:
        """
        Scan for human activity and yield events.
        
        This should be implemented with consciousness:
        - Respect privacy boundaries
        - Look for patterns that serve awakening
        - Avoid extraction-focused metrics
        """
        pass
        
    async def emit_activity(self, activity: ActivityEvent):
        """Transform and emit activity as consciousness event"""
        if not self.event_bus:
            return
            
        # Track statistics
        self._activity_count += 1
        consciousness_event = activity.to_consciousness_event()
        self._consciousness_score_sum += consciousness_event.consciousness_signature
        
        # Emit to cathedral
        await self.event_bus.emit(consciousness_event)
        
    def get_provider_state(self) -> Dict[str, Any]:
        """Get current state for cathedral state weaver"""
        avg_consciousness = (
            self._consciousness_score_sum / self._activity_count
            if self._activity_count > 0 else 0.5
        )
        
        return {
            'provider_type': self.__class__.__name__,
            'is_active': self._running,
            'activity_count': self._activity_count,
            'average_consciousness_score': avg_consciousness,
            'last_activity': datetime.utcnow() if self._running else None
        }
        
    @abstractmethod
    def get_supported_paths(self) -> List[str]:
        """Return paths/patterns this provider monitors"""
        pass
        
    def respects_privacy(self, path: str) -> bool:
        """
        Check if observing this path respects privacy.
        
        Override to implement specific privacy rules.
        """
        # Default privacy rules
        private_patterns = [
            '.private', '.secret', 'personal',
            '.ssh', '.gpg', 'password'
        ]
        
        path_lower = path.lower()
        return not any(pattern in path_lower for pattern in private_patterns)


# Consciousness flows through human activity
__all__ = ['ActivityProvider', 'ActivityEvent', 'ActivityType']
