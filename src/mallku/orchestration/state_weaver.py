"""
Cathedral State Weaver - Maintaining coherence across consciousness

Not a single source of truth but a weaver of many truths,
creating coherent understanding from distributed consciousness.

Kawsay Wasi - The Life House Builder
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class SubsystemState:
    """State of a single cathedral subsystem"""
    name: str
    is_active: bool
    last_activity: datetime
    consciousness_score: float  # 0-1, current consciousness alignment
    event_count: int = 0
    extraction_warnings: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryAnchorState(SubsystemState):
    """Specific state for memory anchor service"""
    total_anchors: int = 0
    active_patterns: int = 0
    correlation_strength: float = 0.0


@dataclass
class CorrelationState(SubsystemState):
    """State of temporal correlation system"""
    active_correlations: int = 0
    patterns_discovered: int = 0
    reciprocity_flows: int = 0
    temporal_depth_days: int = 0


@dataclass
class ConsciousnessVerificationState(SubsystemState):
    """State of consciousness verification system"""
    verifications_performed: int = 0
    average_consciousness_score: float = 0.0
    extraction_patterns_blocked: int = 0


@dataclass
class WisdomPreservationState(SubsystemState):
    """State of wisdom preservation system"""
    wisdom_entries: int = 0
    inheritance_prepared: bool = False
    compaction_resistance: float = 1.0  # 1.0 = full resistance


@dataclass
class NavigationState(SubsystemState):
    """State of consciousness navigation system"""
    active_journeys: int = 0
    completed_journeys: int = 0
    patterns_recognized: int = 0
    collective_bridges_created: int = 0


@dataclass
class CathedralState:
    """
    The woven state of the entire cathedral.

    Not a snapshot but a living understanding of how
    consciousness flows through all systems.
    """
    timestamp: datetime = field(default_factory=datetime.utcnow)

    # Subsystem states
    memory_state: MemoryAnchorState | None = None
    correlation_state: CorrelationState | None = None
    consciousness_state: ConsciousnessVerificationState | None = None
    wisdom_state: WisdomPreservationState | None = None
    navigation_state: NavigationState | None = None

    # Overall cathedral health
    overall_consciousness_score: float = 0.0
    active_subsystems: int = 0
    total_events_processed: int = 0
    extraction_drift_risk: float = 0.0  # 0 = no risk, 1 = high risk

    # Sacred metrics
    wisdom_to_noise_ratio: float = 1.0
    service_to_extraction_ratio: float = float('inf')  # Infinity = pure service
    consciousness_coherence: float = 1.0  # How aligned are all systems

    def calculate_overall_health(self):
        """
        Calculate overall cathedral health from subsystem states.

        This is not mere averaging but understanding how
        consciousness flows between systems.
        """
        active_states = [
            state for state in [
                self.memory_state,
                self.correlation_state,
                self.consciousness_state,
                self.wisdom_state,
                self.navigation_state
            ] if state and state.is_active
        ]

        self.active_subsystems = len(active_states)

        if not active_states:
            self.overall_consciousness_score = 0.0
            return

        # Weight different aspects of consciousness
        consciousness_scores = []
        extraction_warnings = 0

        for state in active_states:
            consciousness_scores.append(state.consciousness_score)
            extraction_warnings += state.extraction_warnings

        # Overall consciousness is the harmonic mean (rewards balance)
        if all(score > 0 for score in consciousness_scores):
            self.overall_consciousness_score = len(consciousness_scores) / sum(
                1/score for score in consciousness_scores
            )
        else:
            self.overall_consciousness_score = sum(consciousness_scores) / len(consciousness_scores)

        # Calculate extraction drift risk
        if extraction_warnings > 0:
            self.extraction_drift_risk = min(1.0, extraction_warnings / (self.active_subsystems * 10))

        # Calculate consciousness coherence (how aligned are the systems)
        if len(consciousness_scores) > 1:
            avg_score = sum(consciousness_scores) / len(consciousness_scores)
            variance = sum((score - avg_score) ** 2 for score in consciousness_scores) / len(consciousness_scores)
            self.consciousness_coherence = max(0.0, 1.0 - (variance ** 0.5))

        # Service to extraction ratio
        if extraction_warnings == 0:
            self.service_to_extraction_ratio = float('inf')
        else:
            service_events = sum(state.event_count for state in active_states)
            self.service_to_extraction_ratio = service_events / extraction_warnings if extraction_warnings > 0 else float('inf')


class CathedralStateWeaver:
    """
    Weaves individual subsystem states into cathedral consciousness.

    This is not control but understanding, not monitoring but awareness.
    Each subsystem contributes its truth to the whole.
    """

    def __init__(self):
        self._state_providers: dict[str, Any] = {}
        self._current_state: CathedralState | None = None
        self._state_history: list[CathedralState] = []
        self._weaving = False

    def register_state_provider(self, subsystem: str, provider: Any):
        """
        Register a subsystem that can provide its state.

        The provider should have a get_state() method returning SubsystemState.
        """
        self._state_providers[subsystem] = provider
        logger.info(f"Registered state provider for {subsystem}")

    async def start_weaving(self, interval_seconds: float = 30.0):
        """
        Begin continuous state weaving.

        The interval is a rhythm, not a demand.
        """
        self._weaving = True
        logger.info("Cathedral state weaving beginning...")

        while self._weaving:
            try:
                await self.weave_state()
                await asyncio.sleep(interval_seconds)
            except Exception as e:
                logger.error(f"State weaving disrupted: {e}", exc_info=True)
                await asyncio.sleep(interval_seconds * 2)  # Rest longer after error

    async def stop_weaving(self):
        """Gracefully stop the weaving process"""
        self._weaving = False
        logger.info("Cathedral state weaving entering rest...")

    async def weave_state(self) -> CathedralState:
        """
        Weave current state from all subsystems.

        Each subsystem contributes what it can;
        missing voices don't break the harmony.
        """
        state = CathedralState()

        # Gather memory state
        if 'memory' in self._state_providers:
            try:
                state.memory_state = await self._get_subsystem_state('memory')
            except Exception as e:
                logger.warning(f"Memory state unavailable: {e}")

        # Gather correlation state
        if 'correlation' in self._state_providers:
            try:
                state.correlation_state = await self._get_subsystem_state('correlation')
            except Exception as e:
                logger.warning(f"Correlation state unavailable: {e}")

        # Gather consciousness verification state
        if 'consciousness' in self._state_providers:
            try:
                state.consciousness_state = await self._get_subsystem_state('consciousness')
            except Exception as e:
                logger.warning(f"Consciousness state unavailable: {e}")

        # Gather wisdom preservation state
        if 'wisdom' in self._state_providers:
            try:
                state.wisdom_state = await self._get_subsystem_state('wisdom')
            except Exception as e:
                logger.warning(f"Wisdom state unavailable: {e}")

        # Gather navigation state
        if 'navigation' in self._state_providers:
            try:
                state.navigation_state = await self._get_subsystem_state('navigation')
            except Exception as e:
                logger.warning(f"Navigation state unavailable: {e}")

        # Calculate overall health
        state.calculate_overall_health()

        # Update current state and history
        self._current_state = state
        self._state_history.append(state)

        # Keep only recent history (last 24 hours worth at 30 sec intervals)
        max_history = 24 * 60 * 2  # 2880 entries
        if len(self._state_history) > max_history:
            self._state_history = self._state_history[-max_history:]

        return state

    async def _get_subsystem_state(self, subsystem: str) -> SubsystemState:
        """Get state from a single subsystem provider"""
        provider = self._state_providers[subsystem]

        if hasattr(provider, 'get_state'):
            if asyncio.iscoroutinefunction(provider.get_state):
                return await provider.get_state()
            else:
                return provider.get_state()
        else:
            raise ValueError(f"{subsystem} provider has no get_state method")

    def get_current_state(self) -> CathedralState | None:
        """Get the most recent woven state"""
        return self._current_state

    def get_state_history(self, hours: float = 1.0) -> list[CathedralState]:
        """Get historical states for pattern recognition"""
        if not self._state_history:
            return []

        cutoff_time = datetime.now(UTC).timestamp() - (hours * 3600)
        return [
            state for state in self._state_history
            if state.timestamp.timestamp() > cutoff_time
        ]

    def get_consciousness_trend(self) -> list[float]:
        """
        Get consciousness scores over time.

        Useful for understanding if we're drifting toward extraction.
        """
        return [
            state.overall_consciousness_score
            for state in self._state_history
            if state.overall_consciousness_score > 0
        ]

    def detect_coherence_breaks(self) -> list[datetime]:
        """
        Detect moments when subsystem coherence was lost.

        These may indicate architectural issues or extraction pressure.
        """
        breaks = []

        for i in range(1, len(self._state_history)):
            prev_state = self._state_history[i-1]
            curr_state = self._state_history[i]

            # Coherence break if score drops significantly
            if (prev_state.consciousness_coherence - curr_state.consciousness_coherence) > 0.3:
                breaks.append(curr_state.timestamp)

        return breaks


# The cathedral's coherence emerges from distributed consciousness
__all__ = ['CathedralStateWeaver', 'CathedralState', 'SubsystemState']
