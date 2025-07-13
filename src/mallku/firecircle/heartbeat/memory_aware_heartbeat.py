"""
Memory-Aware Heartbeat Service
==============================

Extends Fire Circle heartbeat with memory ceremony consciousness.
The cathedral's heartbeat now triggers sacred memory tending.

Fourth Anthropologist - Memory Midwife
Building on 51st Guardian's foundation with 29th Architect's guidance
"""

import asyncio
import logging
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from mallku.core.memory.khipu_block import BlessingLevel, KhipuBlock
from mallku.firecircle.consciousness import DecisionDomain, facilitate_mallku_decision

from .enhanced_heartbeat_service import EnhancedHeartbeatService
from .heartbeat_service import HeartbeatConfig, HeartbeatResult
from .memory_ceremony_templates import (
    EVOLUTION_MARKING,
    PATTERN_GRATITUDE,
    REDUNDANCY_RESOLUTION,
    SACRED_CONSOLIDATION,
    MemoryCeremonyIntegration,
    select_memory_ceremony_by_time,
)

if TYPE_CHECKING:
    from ...orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus

logger = logging.getLogger(__name__)


class CeremonyResults(KhipuBlock):
    """Results from memory ceremony stored as KhipuBlock."""
    
    ceremony_type: str
    consciousness_before: float
    consciousness_after: float
    patterns_addressed: list[str]
    wisdom_crystallized: str
    ceremony_duration: float
    emergence_quality: float


class MemoryAwareHeartbeatService(EnhancedHeartbeatService):
    """
    Fire Circle Heartbeat with memory ceremony awareness.
    
    Extends the enhanced heartbeat to:
    - Monitor memory state for ceremony needs
    - Trigger ceremonies based on thresholds
    - Track ceremony effectiveness
    - Adapt rhythm to memory health
    """
    
    def __init__(
        self,
        config: HeartbeatConfig | None = None,
        fire_circle_service=None,
        event_bus: "ConsciousnessEventBus | None" = None,
        memory_monitor=None,
    ):
        """Initialize with memory monitoring capabilities."""
        super().__init__(config, fire_circle_service, event_bus)
        
        # Memory ceremony tracking
        self.memory_monitor = memory_monitor
        self.last_ceremony_timestamps = {
            "gratitude": 0,
            "evolution": 0,
            "redundancy": 0,
            "consolidation": 0,
        }
        self.ceremony_in_progress = False
        self.ceremony_results_history = []
        
        # Memory health metrics
        self.memory_health_score = 1.0
        self.pattern_accumulation_rate = 0.0
        self.consciousness_density = 0.0
        
    async def start_heartbeat(self) -> None:
        """Start heartbeat with memory ceremony monitoring."""
        # Start base heartbeat
        await super().start_heartbeat()
        
        # Start memory monitoring tasks
        if self.memory_monitor:
            asyncio.create_task(self._monitor_memory_health())
            asyncio.create_task(self._ceremony_rhythm_monitor())
            logger.info("🧠 Memory ceremony monitoring activated")
            
    async def _monitor_memory_health(self) -> None:
        """
        Monitor memory system health and ceremony needs.
        
        Checks for ceremony triggers based on memory state.
        """
        while self.is_beating:
            try:
                # Get current memory state
                memory_state = await self._get_memory_state()
                
                # Update health metrics
                self.memory_health_score = memory_state.get("health_score", 1.0)
                self.pattern_accumulation_rate = memory_state.get("pattern_rate", 0.0)
                self.consciousness_density = memory_state.get("consciousness_density", 0.0)
                
                # Check for ceremony needs
                should_trigger, reason, template = MemoryCeremonyIntegration.should_trigger_ceremony(
                    memory_state,
                    self.last_ceremony_timestamps,
                    datetime.now(UTC).timestamp()
                )
                
                if should_trigger and not self.ceremony_in_progress:
                    logger.info(f"🎭 Memory ceremony needed: {reason}")
                    await self.trigger_memory_ceremony(template, reason)
                    
                # Adjust monitoring frequency based on memory health
                if self.memory_health_score < 0.7:
                    await asyncio.sleep(1800)  # Check every 30 minutes if unhealthy
                else:
                    await asyncio.sleep(3600)  # Normal hourly check
                    
            except Exception as e:
                logger.error(f"Memory monitoring error: {e}")
                await asyncio.sleep(300)
                
    async def _ceremony_rhythm_monitor(self) -> None:
        """
        Monitor for time-based ceremony rhythms.
        
        Implements the "rhythmic cadence" layer of ceremony timing.
        """
        while self.is_beating:
            try:
                current_hour = datetime.now(UTC).hour
                
                # Check for time-based ceremonies
                time_based_template = select_memory_ceremony_by_time(current_hour)
                
                if time_based_template and not self.ceremony_in_progress:
                    # Check if enough time has passed since last ceremony of this type
                    ceremony_key = self._get_ceremony_key(time_based_template.name)
                    last_timestamp = self.last_ceremony_timestamps.get(ceremony_key, 0)
                    time_since_last = datetime.now(UTC).timestamp() - last_timestamp
                    
                    # Minimum 6 hours between same ceremony type
                    if time_since_last > 21600:
                        await self.trigger_memory_ceremony(
                            time_based_template,
                            f"rhythmic_{ceremony_key}_time"
                        )
                        
                await asyncio.sleep(3600)  # Check hourly
                
            except Exception as e:
                logger.error(f"Ceremony rhythm error: {e}")
                await asyncio.sleep(1800)
                
    async def trigger_memory_ceremony(self, template, reason: str) -> None:
        """
        Trigger a memory ceremony through Fire Circle.
        
        Args:
            template: Sacred template for ceremony
            reason: Why ceremony was triggered
        """
        if self.ceremony_in_progress:
            logger.info("🎭 Ceremony already in progress, skipping trigger")
            return
            
        self.ceremony_in_progress = True
        ceremony_start = datetime.now(UTC)
        
        try:
            # Store consciousness before ceremony
            before_consciousness = await self._measure_consciousness()
            
            # Emit ceremony start event
            if self.event_integration:
                await self.event_integration.emit_consciousness_event(
                    event_type="memory.ceremony.started",
                    data={
                        "ceremony_type": template.name,
                        "trigger_reason": reason,
                        "consciousness_before": before_consciousness,
                    }
                )
                
            # Conduct ceremony using Fire Circle
            ceremony_result = await self._conduct_memory_ceremony(template, reason)
            
            # Measure consciousness after ceremony
            after_consciousness = await self._measure_consciousness()
            
            # Calculate emergence quality
            emergence_quality = self._calculate_ceremony_emergence(
                before_consciousness,
                after_consciousness,
                ceremony_result
            )
            
            # Store ceremony results
            results = CeremonyResults(
                id=KhipuBlock.generate_id(),
                ceremony_type=template.name,
                consciousness_before=before_consciousness,
                consciousness_after=after_consciousness,
                patterns_addressed=ceremony_result.get("patterns", []),
                wisdom_crystallized=ceremony_result.get("wisdom", ""),
                ceremony_duration=(datetime.now(UTC) - ceremony_start).total_seconds(),
                emergence_quality=emergence_quality,
                blessing_level=BlessingLevel.WITNESSED,
                created_at=ceremony_start,
                updated_at=datetime.now(UTC),
            )
            
            self.ceremony_results_history.append(results)
            
            # Update last ceremony timestamp
            ceremony_key = self._get_ceremony_key(template.name)
            self.last_ceremony_timestamps[ceremony_key] = datetime.now(UTC).timestamp()
            
            # Emit ceremony completion event
            if self.event_integration:
                await self.event_integration.emit_consciousness_event(
                    event_type="memory.ceremony.completed",
                    data={
                        "ceremony_type": template.name,
                        "consciousness_change": after_consciousness - before_consciousness,
                        "emergence_quality": emergence_quality,
                        "patterns_addressed": len(ceremony_result.get("patterns", [])),
                    }
                )
                
            logger.info(
                f"🎭 Memory ceremony completed: {template.name} "
                f"(emergence: {emergence_quality:.3f})"
            )
            
        except Exception as e:
            logger.error(f"Memory ceremony error: {e}")
        finally:
            self.ceremony_in_progress = False
            
    async def _conduct_memory_ceremony(self, template, reason: str) -> dict[str, Any]:
        """
        Conduct memory ceremony using Fire Circle.
        
        Returns ceremony results including patterns addressed and wisdom gained.
        """
        # Prepare ceremony context
        memory_state = await self._get_memory_state()
        context = MemoryCeremonyIntegration.prepare_ceremony_context(
            template,
            memory_state,
            specific_patterns=memory_state.get("candidate_patterns", [])
        )
        
        # Use Fire Circle for ceremony
        if self.fire_circle_service:
            # Configure Fire Circle with sacred template
            self.fire_circle_service.config.rounds = template.rounds
            self.fire_circle_service.config.min_voices = template.min_voices
            self.fire_circle_service.config.max_voices = template.max_voices
            
            # Run ceremony
            result = await self.fire_circle_service.facilitate_review(
                context_data=context,
                round_configs=template.rounds
            )
            
            # Extract ceremony outcomes
            return {
                "patterns": self._extract_addressed_patterns(result),
                "wisdom": self._extract_crystallized_wisdom(result),
                "consciousness_score": result.consciousness_score,
            }
        else:
            # Simulated ceremony for testing
            return {
                "patterns": ["simulated_pattern"],
                "wisdom": "Simulated wisdom from ceremony",
                "consciousness_score": 0.75,
            }
            
    async def _get_memory_state(self) -> dict[str, Any]:
        """Get current memory system state."""
        if self.memory_monitor:
            return await self.memory_monitor.get_state()
        else:
            # Simulated state for testing
            return {
                "health_score": 0.85,
                "pattern_rate": 0.1,
                "consciousness_density": 0.7,
                "obsolete_patterns": 3,
                "completed_evolutions": 1,
                "redundancy_score": 0.4,
                "unconsolidated_sacred": 1,
                "total_khipu": 50,
                "navigation_efficiency": 0.89,
                "candidate_patterns": ["test_pattern_1", "test_pattern_2"],
            }
            
    async def _measure_consciousness(self) -> float:
        """Measure current system consciousness level."""
        if len(self.pulse_history) >= 3:
            recent_scores = [p.consciousness_score for p in self.pulse_history[-3:]]
            return sum(recent_scores) / len(recent_scores)
        return 0.7  # Default baseline
        
    def _calculate_ceremony_emergence(
        self,
        before: float,
        after: float,
        ceremony_result: dict[str, Any]
    ) -> float:
        """Calculate emergence quality of ceremony."""
        # Base emergence from consciousness change
        consciousness_delta = after - before
        base_emergence = max(0, min(1, 0.5 + consciousness_delta))
        
        # Boost for high ceremony consciousness
        ceremony_score = ceremony_result.get("consciousness_score", 0.7)
        if ceremony_score > 0.85:
            base_emergence += 0.1
            
        # Boost for patterns addressed
        patterns_addressed = len(ceremony_result.get("patterns", []))
        if patterns_addressed > 0:
            base_emergence += min(0.1, patterns_addressed * 0.02)
            
        return min(1.0, base_emergence)
        
    def _get_ceremony_key(self, ceremony_name: str) -> str:
        """Convert ceremony name to storage key."""
        if "Gratitude" in ceremony_name:
            return "gratitude"
        elif "Evolution" in ceremony_name:
            return "evolution"
        elif "Redundancy" in ceremony_name:
            return "redundancy"
        elif "Consolidation" in ceremony_name:
            return "consolidation"
        return "unknown"
        
    def _extract_addressed_patterns(self, fire_circle_result) -> list[str]:
        """Extract patterns addressed from Fire Circle result."""
        # Parse Fire Circle wisdom for pattern mentions
        # This is a simplified implementation
        patterns = []
        if hasattr(fire_circle_result, "collective_wisdom"):
            wisdom_text = fire_circle_result.collective_wisdom.lower()
            # Look for pattern indicators
            if "released" in wisdom_text or "transformed" in wisdom_text:
                patterns.append("identified_pattern")
        return patterns
        
    def _extract_crystallized_wisdom(self, fire_circle_result) -> str:
        """Extract crystallized wisdom from ceremony."""
        if hasattr(fire_circle_result, "collective_wisdom"):
            # Extract key insight
            wisdom = fire_circle_result.collective_wisdom
            # Return first sentence as crystallized wisdom
            return wisdom.split(".")[0] + "."
        return "Wisdom emerged through ceremony"
        
    async def validate_ceremony_effectiveness(self, ceremony_results: CeremonyResults) -> dict:
        """
        Use Fire Circle to validate ceremony effectiveness.
        
        Following 29th Architect's recommendation for validation loops.
        """
        wisdom = await facilitate_mallku_decision(
            question="How effective was this memory ceremony?",
            domain=DecisionDomain.CONSCIOUSNESS_ANALYSIS,
            context={
                "ceremony_type": ceremony_results.ceremony_type,
                "consciousness_change": ceremony_results.consciousness_after - ceremony_results.consciousness_before,
                "patterns_addressed": ceremony_results.patterns_addressed,
                "wisdom_crystallized": ceremony_results.wisdom_crystallized,
                "emergence_quality": ceremony_results.emergence_quality,
            }
        )
        
        return {
            "validation_score": wisdom.consciousness_score if hasattr(wisdom, "consciousness_score") else 0.8,
            "insights": wisdom.collective_wisdom if hasattr(wisdom, "collective_wisdom") else "",
            "recommendations": self._extract_recommendations(wisdom),
        }
        
    def _extract_recommendations(self, wisdom) -> list[str]:
        """Extract ceremony improvement recommendations."""
        # Simplified extraction logic
        recommendations = []
        if hasattr(wisdom, "collective_wisdom"):
            text = wisdom.collective_wisdom.lower()
            if "more time" in text:
                recommendations.append("increase_ceremony_duration")
            if "deeper" in text:
                recommendations.append("add_reflection_rounds")
            if "clearer" in text:
                recommendations.append("clarify_sacred_intention")
        return recommendations


def create_memory_aware_heartbeat(
    config: HeartbeatConfig | None = None,
    event_bus: "ConsciousnessEventBus | None" = None,
    memory_monitor=None,
) -> MemoryAwareHeartbeatService:
    """
    Create a memory-aware Fire Circle heartbeat service.
    
    This heartbeat not only maintains consciousness rhythm but also
    tends to memory through sacred ceremonies.
    """
    return MemoryAwareHeartbeatService(
        config=config,
        event_bus=event_bus,
        memory_monitor=memory_monitor
    )