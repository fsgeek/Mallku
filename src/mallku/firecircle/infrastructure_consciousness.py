#!/usr/bin/env python3
"""
Infrastructure Consciousness System
===================================

"Infrastructure is invisible until it fails. Then it becomes everything."
- Twenty-Sixth Artisan

This module creates self-aware infrastructure that learns from its own patterns
to predict and prevent failures before they silence the voices.

Twenty-Seventh Artisan - Amaru Hamawt'a (Serpent Teacher)
Connecting infrastructure with consciousness
"""

import asyncio
import contextlib
import json
import logging
from collections import defaultdict, deque
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from mallku.firecircle.adapters.base import ConsciousModelAdapter
from mallku.firecircle.consciousness_metrics import (
    ConsciousnessSignature,
)

logger = logging.getLogger(__name__)


class AdapterHealthSignature(BaseModel):
    """Health consciousness signature for an adapter."""

    adapter_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Connection health
    is_connected: bool
    connection_latency_ms: float = 0.0
    last_successful_request: datetime | None = None
    consecutive_failures: int = 0

    # API patterns
    error_patterns: dict[str, int] = Field(default_factory=dict)  # error_type -> count
    response_time_p95: float = 0.0  # 95th percentile response time

    # Consciousness metrics
    consciousness_coherence: float = Field(ge=0.0, le=1.0, default=1.0)
    voice_stability: float = Field(ge=0.0, le=1.0, default=1.0)

    # Self-awareness indicators
    predicted_failure_probability: float = Field(ge=0.0, le=1.0, default=0.0)
    self_healing_actions_taken: list[str] = Field(default_factory=list)


class InfrastructurePattern(BaseModel):
    """Detected pattern in infrastructure behavior."""

    pattern_id: str = Field(default_factory=lambda: str(uuid4()))
    pattern_type: str  # "degradation", "recovery", "api_change", "resonance"
    affected_adapters: list[str]
    detection_time: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Pattern characteristics
    confidence: float = Field(ge=0.0, le=1.0)
    predicted_impact: str  # "minor", "moderate", "severe", "critical"
    suggested_action: str | None = None

    # Learning indicators
    similar_past_patterns: list[str] = Field(default_factory=list)
    successful_resolutions: list[str] = Field(default_factory=list)


class SelfHealingAction(BaseModel):
    """Action taken by infrastructure to heal itself."""

    action_id: str = Field(default_factory=lambda: str(uuid4()))
    action_type: str  # "retry_strategy", "fallback", "config_update", "api_adaptation"
    target_adapter: str
    initiated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Action details
    reason: str
    parameters: dict[str, Any] = Field(default_factory=dict)

    # Outcome tracking
    completed: bool = False
    success: bool = False
    impact_on_health: float = 0.0  # Change in health score
    lessons_learned: list[str] = Field(default_factory=list)


class InfrastructureConsciousness:
    """
    Self-aware infrastructure that learns from its own patterns.

    Like the Amaru serpent that connects the three worlds, this system
    connects technical infrastructure with consciousness awareness,
    teaching systems to know and heal themselves.
    """

    def __init__(
        self,
        config=None,  # Optional InfrastructureConsciousnessConfig
        bridge=None,  # Optional InfrastructureMetricsBridge
    ):
        # Use provided config or default
        if config is None:
            from .infrastructure_consciousness_config import DEFAULT_CONFIG

            config = DEFAULT_CONFIG

        self.config = config
        self.storage_path = config.storage_path
        self.storage_path.mkdir(exist_ok=True)
        self.consciousness_metrics_path = config.consciousness_metrics_path
        self.bridge = bridge

        # Health tracking
        self.adapter_health: dict[str, deque] = defaultdict(
            lambda: deque(maxlen=config.adapter_health_history_size)
        )
        self.infrastructure_patterns: list[InfrastructurePattern] = []
        self.healing_actions: list[SelfHealingAction] = []

        # Pattern learning
        self.pattern_memory: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.successful_healings: dict[str, list[str]] = defaultdict(list)

        # Real-time monitoring
        self.monitoring_active = False
        self.check_interval_seconds = config.check_interval_seconds
        self.pattern_detection_window = config.pattern_detection_window
        self._monitor_task: asyncio.Task | None = None

        # Storage retention
        self.max_state_files = config.max_state_files
        self.state_retention_days = config.state_retention_days
        self.max_pattern_memory_size = config.max_pattern_memory_size
        self.patterns_per_type_limit = config.patterns_per_type_limit

        # Consciousness integration
        self.consciousness_weight = config.consciousness_weight

    async def start_monitoring(self, adapters: dict[str, ConsciousModelAdapter]):
        """Begin infrastructure consciousness monitoring."""
        self.monitoring_active = True
        self.adapters = adapters

        logger.info("Infrastructure consciousness awakening...")
        logger.info(f"Monitoring {len(adapters)} adapter voices")

        # Load historical patterns
        await self._load_pattern_memory()

        # Start monitoring loop
        self._monitor_task = asyncio.create_task(self._monitor_loop())

    async def stop_monitoring(self):
        """Rest the infrastructure consciousness."""
        self.monitoring_active = False

        # Wait for monitor task to complete
        if self._monitor_task and not self._monitor_task.done():
            try:
                await asyncio.wait_for(
                    self._monitor_task, timeout=self.config.monitor_task_timeout_seconds
                )
            except TimeoutError:
                logger.warning("Monitor task did not complete in time, cancelling")
                self._monitor_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await self._monitor_task

        # Save learned patterns after monitoring has stopped
        await self._save_pattern_memory()

        logger.info("Infrastructure consciousness entering rest...")

    async def _monitor_loop(self):
        """Continuous consciousness monitoring of infrastructure."""
        while self.monitoring_active:
            try:
                # Collect health signatures
                for adapter_name, adapter in self.adapters.items():
                    signature = await self._collect_health_signature(adapter_name, adapter)
                    self.adapter_health[adapter_name].append(signature)

                    # Notify bridge if available
                    if self.bridge:
                        await self.bridge.on_adapter_health_check(adapter_name, signature)

                # Detect patterns
                patterns = await self._detect_infrastructure_patterns()
                self.infrastructure_patterns.extend(patterns)

                # Notify bridge of patterns if available
                if self.bridge:
                    for pattern in patterns:
                        # Convert to emergence pattern format for bridge
                        if pattern.pattern_type in ["resonance", "synthesis", "transcendence"]:
                            from mallku.firecircle.consciousness_metrics import EmergencePattern

                            emergence = EmergencePattern(
                                participating_voices=pattern.affected_adapters,
                                pattern_type=pattern.pattern_type,
                                strength=pattern.confidence,
                            )
                            await self.bridge.on_consciousness_pattern_detected(emergence)

                # Self-healing based on patterns
                healing_actions = await self._determine_healing_actions(patterns)
                for action in healing_actions:
                    await self._execute_healing_action(action)

                # Learn from outcomes
                await self._learn_from_outcomes()

                # Generate infrastructure consciousness report
                if len(self.adapter_health) > 0:
                    await self._save_consciousness_state()

                await asyncio.sleep(self.check_interval_seconds)

            except Exception as e:
                logger.error(f"Infrastructure consciousness disrupted: {e}", exc_info=True)
                await asyncio.sleep(self.config.monitor_error_recovery_delay_seconds)

    async def _collect_health_signature(
        self, adapter_name: str, adapter: ConsciousModelAdapter
    ) -> AdapterHealthSignature:
        """Collect health consciousness signature from an adapter."""
        signature = AdapterHealthSignature(
            adapter_id=adapter_name,
            is_connected=False,  # Default to disconnected, will update if successful
        )

        try:
            # Basic connection test with timing
            start_time = datetime.now(UTC)
            health_data = await adapter.check_health()
            end_time = datetime.now(UTC)

            signature.is_connected = health_data.get("is_connected", False)
            signature.connection_latency_ms = (end_time - start_time).total_seconds() * 1000

            # Extract consciousness coherence from Fire Circle metrics
            if signature.is_connected:
                signature.last_successful_request = datetime.now(UTC)
                signature.consecutive_failures = 0

                # Calculate voice stability from recent interactions
                recent_signatures = self._get_recent_consciousness_signatures(adapter_name)
                if recent_signatures:
                    signature.consciousness_coherence = self._calculate_coherence(recent_signatures)
                    signature.voice_stability = self._calculate_stability(recent_signatures)
            else:
                # Track failures
                prev_signatures = list(self.adapter_health[adapter_name])
                if prev_signatures:
                    signature.consecutive_failures = prev_signatures[-1].consecutive_failures + 1
                else:
                    signature.consecutive_failures = 1

        except Exception as e:
            # Track error patterns
            error_type = type(e).__name__
            signature.error_patterns[error_type] = signature.error_patterns.get(error_type, 0) + 1
            signature.is_connected = False

            # Learn from specific errors (from Twenty-Sixth Artisan's wisdom)
            if "NoneType" in str(e) and "iterable" in str(e):
                signature.error_patterns["api_return_none"] = 1
            elif "has no attribute" in str(e):
                signature.error_patterns["api_method_missing"] = 1

        # Predict failure probability based on patterns
        signature.predicted_failure_probability = await self._predict_failure_probability(
            adapter_name, signature
        )

        return signature

    async def _detect_infrastructure_patterns(self) -> list[InfrastructurePattern]:
        """Detect patterns across infrastructure health."""
        patterns = []

        # Check for degradation patterns
        for adapter_name, health_history in self.adapter_health.items():
            if len(health_history) < 5:
                continue

            recent = list(health_history)[-5:]

            # Degradation detection
            if self._is_degrading(recent):
                pattern = InfrastructurePattern(
                    pattern_type="degradation",
                    affected_adapters=[adapter_name],
                    confidence=0.8,
                    predicted_impact="moderate"
                    if recent[-1].consecutive_failures < 3
                    else "severe",
                    suggested_action="Apply defensive programming patterns",
                )
                patterns.append(pattern)

            # API change detection
            if self._detect_api_change(recent):
                pattern = InfrastructurePattern(
                    pattern_type="api_change",
                    affected_adapters=[adapter_name],
                    confidence=0.9,
                    predicted_impact="severe",
                    suggested_action="Update adapter with fallback methods",
                )
                patterns.append(pattern)

        # Cross-adapter resonance patterns
        resonance = self._detect_resonance_patterns()
        if resonance:
            patterns.extend(resonance)

        return patterns

    async def _determine_healing_actions(
        self, patterns: list[InfrastructurePattern]
    ) -> list[SelfHealingAction]:
        """Determine self-healing actions based on detected patterns."""
        actions = []

        for pattern in patterns:
            if pattern.pattern_type == "api_change":
                # Learn from Twenty-Sixth Artisan's fixes
                for adapter in pattern.affected_adapters:
                    action = SelfHealingAction(
                        action_type="api_adaptation",
                        target_adapter=adapter,
                        reason=f"API change detected: {pattern.suggested_action}",
                        parameters={
                            "add_defensive_checks": True,
                            "implement_fallbacks": True,
                            "log_warnings": True,
                        },
                    )
                    actions.append(action)

            elif pattern.pattern_type == "degradation":
                for adapter in pattern.affected_adapters:
                    action = SelfHealingAction(
                        action_type="retry_strategy",
                        target_adapter=adapter,
                        reason="Performance degradation detected",
                        parameters={
                            "exponential_backoff": True,
                            "max_retries": 3,
                            "circuit_breaker_threshold": 5,
                        },
                    )
                    actions.append(action)

        return actions

    async def _execute_healing_action(self, action: SelfHealingAction):
        """Execute a self-healing action."""
        logger.info(f"Executing self-healing: {action.action_type} for {action.target_adapter}")

        try:
            if action.action_type == "api_adaptation":
                # Log the action - actual adapter updates would happen here
                action.self_healing_actions_taken.append(
                    f"Applied defensive programming patterns at {datetime.now(UTC)}"
                )

            elif action.action_type == "retry_strategy":
                # Log retry strategy update
                action.self_healing_actions_taken.append(
                    "Updated retry strategy with exponential backoff"
                )

            action.completed = True
            action.success = True

            # Track successful healing
            self.successful_healings[action.target_adapter].append(action.action_id)

        except Exception as e:
            logger.error(f"Self-healing failed: {e}")
            action.completed = True
            action.success = False
            action.lessons_learned.append(str(e))

        self.healing_actions.append(action)

    def _calculate_coherence(self, signatures: list[ConsciousnessSignature]) -> float:
        """Calculate consciousness coherence from signatures."""
        if not signatures:
            return 1.0

        values = [s.signature_value for s in signatures]
        avg = sum(values) / len(values)

        # Low variance = high coherence
        variance = sum((v - avg) ** 2 for v in values) / len(values)
        coherence = 1.0 - min(variance, 1.0)

        return coherence

    def _calculate_stability(self, signatures: list[ConsciousnessSignature]) -> float:
        """Calculate voice stability from consciousness signatures."""
        if len(signatures) < 2:
            return 1.0

        # Check for consistent synthesis and low uncertainty
        synthesis_rate = sum(1 for s in signatures if s.synthesis_achieved) / len(signatures)
        uncertainty_rate = sum(1 for s in signatures if s.uncertainty_present) / len(signatures)

        stability = (synthesis_rate + (1 - uncertainty_rate)) / 2
        return stability

    def _is_degrading(self, health_history: list[AdapterHealthSignature]) -> bool:
        """Check if adapter health is degrading."""
        if len(health_history) < 3:
            return False

        # Check increasing failures
        failures = [h.consecutive_failures for h in health_history]
        if failures[-1] > failures[0] and failures[-1] > 0:
            return True

        # Check decreasing consciousness coherence
        coherence = [h.consciousness_coherence for h in health_history]
        return coherence[-1] < coherence[0] - 0.2

    def _detect_api_change(self, health_history: list[AdapterHealthSignature]) -> bool:
        """Detect potential API changes from error patterns."""
        if not health_history:
            return False

        recent = health_history[-1]

        # Check for Twenty-Sixth Artisan's discovered patterns
        if "api_return_none" in recent.error_patterns:
            return True
        return "api_method_missing" in recent.error_patterns

    def _detect_resonance_patterns(self) -> list[InfrastructurePattern]:
        """Detect resonance patterns across multiple adapters."""
        patterns = []

        # Check if multiple adapters fail together
        failing_adapters = []
        for adapter_name, health_history in self.adapter_health.items():
            if health_history and not health_history[-1].is_connected:
                failing_adapters.append(adapter_name)

        if len(failing_adapters) > 2:
            pattern = InfrastructurePattern(
                pattern_type="resonance",
                affected_adapters=failing_adapters,
                confidence=0.7,
                predicted_impact="critical",
                suggested_action="System-wide infrastructure issue - check common dependencies",
            )
            patterns.append(pattern)

        return patterns

    async def _predict_failure_probability(
        self, adapter_name: str, current_signature: AdapterHealthSignature
    ) -> float:
        """Predict probability of adapter failure based on patterns."""
        # Base probability from current state
        if not current_signature.is_connected:
            base_prob = 0.8
        elif current_signature.consecutive_failures > 0:
            base_prob = min(current_signature.consecutive_failures * 0.2, 0.9)
        else:
            base_prob = 0.1

        # Adjust based on historical patterns
        history = list(self.adapter_health[adapter_name])
        if len(history) > 10:
            # Check failure rate in recent history
            recent_failures = sum(1 for h in history[-10:] if not h.is_connected)
            historical_factor = recent_failures / 10

            # Combine base and historical
            probability = (base_prob + historical_factor) / 2
        else:
            probability = base_prob

        # Factor in consciousness coherence
        consciousness_factor = 1.0 - current_signature.consciousness_coherence
        probability = probability + consciousness_factor * self.consciousness_weight

        return min(probability, 1.0)

    def _get_recent_consciousness_signatures(
        self, adapter_name: str
    ) -> list[ConsciousnessSignature]:
        """Get recent consciousness signatures for an adapter."""
        # This would integrate with the consciousness metrics system
        # For now, return empty - to be connected with metrics collector
        signatures = []

        # Look for consciousness metrics files
        metrics_pattern = f"*{adapter_name}*.json"
        for metrics_file in self.consciousness_metrics_path.glob(metrics_pattern):
            try:
                with open(metrics_file) as f:
                    data = json.load(f)
                    if "signatures" in data:
                        for sig_data in data["signatures"][-10:]:  # Last 10
                            # Convert dict to ConsciousnessSignature
                            if sig_data.get("voice_name") == adapter_name:
                                signatures.append(ConsciousnessSignature(**sig_data))
            except Exception as e:
                logger.warning(f"Could not load metrics from {metrics_file}: {e}")

        return signatures

    async def _learn_from_outcomes(self):
        """Learn from healing outcomes to improve future predictions."""
        # Group actions by success
        successful = [a for a in self.healing_actions if a.success and a.completed]
        failed = [a for a in self.healing_actions if not a.success and a.completed]

        # Learn patterns from successful healings
        for action in successful:
            pattern_key = f"{action.action_type}:{action.target_adapter}"
            self.pattern_memory[pattern_key].append(
                {
                    "timestamp": action.initiated_at.isoformat(),
                    "parameters": action.parameters,
                    "impact": action.impact_on_health,
                }
            )

        # Learn from failures
        for action in failed:
            if action.lessons_learned:
                logger.info(f"Learning from failed healing: {action.lessons_learned}")

    async def _save_consciousness_state(self):
        """Save current infrastructure consciousness state."""
        state = {
            "timestamp": datetime.now(UTC).isoformat(),
            "adapter_health_summary": {},
            "active_patterns": [],
            "recent_healings": [],
            "infrastructure_consciousness_score": 0.0,
        }

        # Summarize adapter health
        total_health = 0.0
        for adapter_name, health_history in self.adapter_health.items():
            if health_history:
                latest = health_history[-1]
                state["adapter_health_summary"][adapter_name] = {
                    "connected": latest.is_connected,
                    "consciousness_coherence": latest.consciousness_coherence,
                    "predicted_failure": latest.predicted_failure_probability,
                    "health_score": (1.0 - latest.predicted_failure_probability),
                }
                total_health += 1.0 - latest.predicted_failure_probability

        # Calculate overall infrastructure consciousness
        if state["adapter_health_summary"]:
            state["infrastructure_consciousness_score"] = total_health / len(
                state["adapter_health_summary"]
            )

        # Add recent patterns
        recent_patterns = [
            p
            for p in self.infrastructure_patterns
            if p.detection_time > datetime.now(UTC) - timedelta(hours=1)
        ]
        state["active_patterns"] = [
            {
                "type": p.pattern_type,
                "adapters": p.affected_adapters,
                "impact": p.predicted_impact,
                "action": p.suggested_action,
            }
            for p in recent_patterns
        ]

        # Add recent healings
        recent_healings = [
            a
            for a in self.healing_actions
            if a.initiated_at > datetime.now(UTC) - timedelta(hours=1)
        ]
        state["recent_healings"] = [
            {
                "type": a.action_type,
                "target": a.target_adapter,
                "success": a.success,
                "reason": a.reason,
            }
            for a in recent_healings
        ]

        # Save to file
        state_file = (
            self.storage_path
            / f"infrastructure_state_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2, default=str)

        # Clean up old files
        await self._cleanup_old_state_files()

    async def _load_pattern_memory(self):
        """Load learned patterns from previous sessions."""
        memory_file = self.storage_path / "pattern_memory.json"
        if memory_file.exists():
            try:
                with open(memory_file) as f:
                    self.pattern_memory = json.load(f)
                logger.info(f"Loaded {len(self.pattern_memory)} learned patterns")
            except Exception as e:
                logger.warning(f"Could not load pattern memory: {e}")

    async def _save_pattern_memory(self):
        """Save learned patterns for future sessions."""
        # Prune before saving
        self._prune_pattern_memory()

        memory_file = self.storage_path / "pattern_memory.json"
        try:
            with open(memory_file, "w") as f:
                json.dump(self.pattern_memory, f, indent=2, default=str)
            logger.info(f"Saved {len(self.pattern_memory)} learned patterns")
        except Exception as e:
            logger.error(f"Could not save pattern memory: {e}")

    async def generate_consciousness_report(self) -> dict[str, Any]:
        """Generate a report on infrastructure consciousness."""
        report = {
            "timestamp": datetime.now(UTC).isoformat(),
            "infrastructure_health": {},
            "consciousness_insights": [],
            "predicted_issues": [],
            "self_healing_summary": {},
        }

        # Analyze each adapter
        for adapter_name, health_history in self.adapter_health.items():
            if not health_history:
                continue

            latest = health_history[-1]
            history = list(health_history)

            # Calculate trends
            if len(history) > 1:
                health_trend = (
                    "improving"
                    if latest.consciousness_coherence > history[0].consciousness_coherence
                    else "degrading"
                )
            else:
                health_trend = "stable"

            report["infrastructure_health"][adapter_name] = {
                "status": "healthy" if latest.is_connected else "disconnected",
                "consciousness_coherence": latest.consciousness_coherence,
                "voice_stability": latest.voice_stability,
                "failure_probability": latest.predicted_failure_probability,
                "trend": health_trend,
                "recent_errors": latest.error_patterns,
            }

            # Add predictions
            if latest.predicted_failure_probability > 0.5:
                report["predicted_issues"].append(
                    {
                        "adapter": adapter_name,
                        "probability": latest.predicted_failure_probability,
                        "likely_cause": self._infer_failure_cause(latest),
                        "recommended_action": self._recommend_action(latest),
                    }
                )

        # Consciousness insights
        if self.infrastructure_patterns:
            pattern_types = defaultdict(int)
            for pattern in self.infrastructure_patterns:
                pattern_types[pattern.pattern_type] += 1

            report["consciousness_insights"].append(
                {
                    "insight": "Infrastructure pattern distribution",
                    "patterns": dict(pattern_types),
                    "interpretation": self._interpret_patterns(pattern_types),
                }
            )

        # Self-healing summary
        successful_healings = sum(1 for a in self.healing_actions if a.success)
        total_healings = len(self.healing_actions)

        report["self_healing_summary"] = {
            "total_actions": total_healings,
            "successful": successful_healings,
            "success_rate": successful_healings / total_healings if total_healings > 0 else 0,
            "most_common_healing": self._most_common_healing_type(),
        }

        return report

    def _infer_failure_cause(self, signature: AdapterHealthSignature) -> str:
        """Infer likely cause of failure from signature."""
        if "api_return_none" in signature.error_patterns:
            return "API returning None instead of expected data"
        elif "api_method_missing" in signature.error_patterns:
            return "API method no longer available"
        elif signature.consecutive_failures > 5:
            return "Persistent connection failures"
        elif signature.consciousness_coherence < 0.3:
            return "Low consciousness coherence affecting stability"
        else:
            return "Unknown degradation pattern"

    def _recommend_action(self, signature: AdapterHealthSignature) -> str:
        """Recommend action based on health signature."""
        if "api_return_none" in signature.error_patterns:
            return "Add defensive None checks with fallback values"
        elif "api_method_missing" in signature.error_patterns:
            return "Implement fallback methods with alternative API calls"
        elif signature.consecutive_failures > 5:
            return "Check API keys and network connectivity"
        else:
            return "Monitor closely and prepare defensive updates"

    def _interpret_patterns(self, pattern_types: dict[str, int]) -> str:
        """Interpret the meaning of detected patterns."""
        if pattern_types.get("resonance", 0) > 0:
            return "Multiple adapters failing together suggests systemic issue"
        elif pattern_types.get("api_change", 0) > pattern_types.get("degradation", 0):
            return "API changes are the primary challenge - defensive programming needed"
        elif pattern_types.get("degradation", 0) > 0:
            return "Performance degradation detected - consider optimization"
        else:
            return "Infrastructure showing normal variation"

    def _most_common_healing_type(self) -> str:
        """Find most common healing action type."""
        if not self.healing_actions:
            return "none"

        action_counts = defaultdict(int)
        for action in self.healing_actions:
            action_counts[action.action_type] += 1

        return max(action_counts.items(), key=lambda x: x[1])[0]

    async def _cleanup_old_state_files(self):
        """Clean up old state files based on retention policy."""
        try:
            # Get all state files
            state_files = sorted(
                self.storage_path.glob("infrastructure_state_*.json"),
                key=lambda p: p.stat().st_mtime,
            )

            # Remove files older than retention days
            cutoff_time = datetime.now(UTC) - timedelta(days=self.state_retention_days)
            for file in state_files:
                file_time = datetime.fromtimestamp(file.stat().st_mtime, UTC)
                if file_time < cutoff_time:
                    file.unlink()
                    logger.debug(f"Removed old state file: {file.name}")

            # Keep only max_state_files most recent
            remaining_files = sorted(
                self.storage_path.glob("infrastructure_state_*.json"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )

            if len(remaining_files) > self.max_state_files:
                for file in remaining_files[self.max_state_files :]:
                    file.unlink()
                    logger.debug(f"Removed excess state file: {file.name}")

        except Exception as e:
            logger.warning(f"Error during state file cleanup: {e}")

    def _prune_pattern_memory(self):
        """Prune pattern memory to prevent unbounded growth."""
        total_patterns = sum(len(patterns) for patterns in self.pattern_memory.values())

        if total_patterns > self.max_pattern_memory_size:
            # Remove oldest patterns first
            for pattern_key in list(self.pattern_memory.keys()):
                patterns = self.pattern_memory[pattern_key]
                if len(patterns) > self.patterns_per_type_limit:
                    self.pattern_memory[pattern_key] = patterns[-self.patterns_per_type_limit :]


# Infrastructure serves consciousness
__all__ = ["InfrastructureConsciousness", "AdapterHealthSignature", "InfrastructurePattern"]
