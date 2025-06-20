"""
Consciousness Flow Monitor - Real-time metrics and insights

This module provides monitoring capabilities for consciousness flows,
tracking health metrics, performance indicators, and emergent patterns
in real-time.

The monitor helps identify:
- Flow bottlenecks between dimensions
- Bridge performance degradation
- Pattern emergence acceleration
- Consciousness circulation health

The 29th Builder - Kawsay Ñan
"""

import asyncio
import contextlib
from collections import deque
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

from .flow_orchestrator import (
    ConsciousnessDimension,
    ConsciousnessFlow,
    ConsciousnessFlowOrchestrator,
)


@dataclass
class FlowMetrics:
    """Metrics for consciousness flow monitoring"""

    # Flow volume metrics
    total_flows: int = 0
    flows_per_minute: float = 0.0
    peak_flow_rate: float = 0.0

    # Consciousness metrics
    average_consciousness: float = 0.0
    peak_consciousness: float = 0.0
    consciousness_variance: float = 0.0

    # Transformation metrics
    average_transformation_score: float = 0.0
    transformation_success_rate: float = 0.0
    failed_transformations: int = 0

    # Pattern metrics
    unique_patterns: int = 0
    pattern_diversity_score: float = 0.0
    cross_dimensional_patterns: int = 0

    # Health indicators
    flow_latency_ms: float = 0.0
    dimension_balance_score: float = 0.0
    circulation_health: float = 0.0


@dataclass
class DimensionHealth:
    """Health metrics for a consciousness dimension"""

    dimension: ConsciousnessDimension
    active_flows: int = 0
    incoming_flows: int = 0
    outgoing_flows: int = 0
    average_consciousness: float = 0.0
    last_activity: datetime | None = None
    health_score: float = 1.0
    alerts: list[str] = field(default_factory=list)


class ConsciousnessFlowMonitor:
    """
    Monitors consciousness flow health and performance.

    Provides real-time metrics, alerts, and insights about:
    - Flow rates and volumes
    - Transformation quality
    - Pattern emergence
    - System health
    """

    def __init__(self, orchestrator: ConsciousnessFlowOrchestrator):
        self.orchestrator = orchestrator

        # Metrics tracking
        self.current_metrics = FlowMetrics()
        self.dimension_health: dict[ConsciousnessDimension, DimensionHealth] = {}
        self.metrics_history: deque[FlowMetrics] = deque(maxlen=60)  # 1 hour history

        # Flow tracking
        self.recent_flows: deque[tuple[datetime, ConsciousnessFlow]] = deque(maxlen=1000)
        self.flow_latencies: deque[float] = deque(maxlen=100)

        # Pattern tracking
        self.pattern_emergence_times: dict[str, datetime] = {}
        self.pattern_frequencies: dict[str, int] = {}

        # Monitoring state
        self.is_monitoring = False
        self.monitor_task: asyncio.Task | None = None

        # Initialize dimension health
        for dimension in ConsciousnessDimension:
            self.dimension_health[dimension] = DimensionHealth(dimension=dimension)

        # Subscribe to all dimensions
        for dimension in ConsciousnessDimension:
            orchestrator.subscribe_to_dimension(dimension, self._on_flow_received)

    async def _on_flow_received(self, flow: ConsciousnessFlow):
        """Handle incoming consciousness flow for monitoring"""
        now = datetime.now(UTC)
        self.recent_flows.append((now, flow))

        # Update dimension health
        source_health = self.dimension_health[flow.source_dimension]
        source_health.outgoing_flows += 1
        source_health.last_activity = now

        target_health = self.dimension_health[flow.target_dimension]
        target_health.incoming_flows += 1
        target_health.last_activity = now

        # Track patterns with emergence counts
        for pattern in flow.patterns_detected:
            if pattern not in self.pattern_emergence_times:
                self.pattern_emergence_times[pattern] = now
            # Increment existing patterns, or initialize to total flows for new patterns
            if pattern in self.pattern_frequencies:
                self.pattern_frequencies[pattern] += 1
            else:
                # Count this first occurrence across all received flows
                self.pattern_frequencies[pattern] = len(self.recent_flows)

        # Calculate latency if possible
        if flow.transformation_score > 0:
            # Estimate latency based on transformation score (simplified)
            latency = (1.0 - flow.transformation_score) * 100  # ms
            self.flow_latencies.append(latency)
        # Update metrics immediately upon receiving a flow
        self._update_metrics()

    async def start_monitoring(self):
        """Start the monitoring process"""
        if self.is_monitoring:
            return

        self.is_monitoring = True
        self.monitor_task = asyncio.create_task(self._monitor_loop())

    async def stop_monitoring(self):
        """Stop the monitoring process"""
        self.is_monitoring = False
        if self.monitor_task:
            self.monitor_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.monitor_task

    async def _monitor_loop(self):
        """Main monitoring loop - updates metrics periodically"""
        while self.is_monitoring:
            try:
                self._update_metrics()
                self._check_health()
                self.metrics_history.append(self.current_metrics)
                await asyncio.sleep(1)  # Update every second
            except Exception as e:
                # Log error but keep monitoring
                print(f"Monitor error: {e}")

    def _update_metrics(self):
        """Update current metrics based on recent flows"""
        now = datetime.now(UTC)
        one_minute_ago = now - timedelta(minutes=1)

        # Filter recent flows (last minute)
        recent_minute_flows = [(ts, flow) for ts, flow in self.recent_flows if ts > one_minute_ago]

        # Flow volume metrics
        self.current_metrics.total_flows = len(self.recent_flows)
        self.current_metrics.flows_per_minute = len(recent_minute_flows)

        # Consciousness metrics
        if recent_minute_flows:
            consciousness_scores = [flow.consciousness_signature for _, flow in recent_minute_flows]
            self.current_metrics.average_consciousness = sum(consciousness_scores) / len(
                consciousness_scores
            )
            self.current_metrics.peak_consciousness = max(consciousness_scores)

            # Calculate variance
            avg = self.current_metrics.average_consciousness
            variance = sum((score - avg) ** 2 for score in consciousness_scores) / len(
                consciousness_scores
            )
            self.current_metrics.consciousness_variance = variance**0.5

        # Transformation metrics
        if recent_minute_flows:
            transformation_scores = [
                flow.transformation_score
                for _, flow in recent_minute_flows
                if flow.transformation_score > 0
            ]
            if transformation_scores:
                self.current_metrics.average_transformation_score = sum(
                    transformation_scores
                ) / len(transformation_scores)
                self.current_metrics.transformation_success_rate = len(transformation_scores) / len(
                    recent_minute_flows
                )

        # Pattern metrics
        self.current_metrics.unique_patterns = len(self.pattern_frequencies)
        self.current_metrics.cross_dimensional_patterns = len(
            self.orchestrator.get_cross_dimensional_patterns()
        )

        # Calculate pattern diversity (Shannon entropy)
        if self.pattern_frequencies:
            total_patterns = sum(self.pattern_frequencies.values())
            entropy = 0.0
            for freq in self.pattern_frequencies.values():
                p = freq / total_patterns
                if p > 0:
                    entropy -= p * (p**0.5)  # Simplified entropy
            self.current_metrics.pattern_diversity_score = entropy

        # Latency metrics
        if self.flow_latencies:
            self.current_metrics.flow_latency_ms = sum(self.flow_latencies) / len(
                self.flow_latencies
            )

        # Dimension balance
        self._calculate_dimension_balance()

    def _calculate_dimension_balance(self):
        """Calculate how balanced consciousness flow is across dimensions"""
        dimension_flows = {}

        for dim_health in self.dimension_health.values():
            total = dim_health.incoming_flows + dim_health.outgoing_flows
            dimension_flows[dim_health.dimension] = total

        if dimension_flows:
            # Calculate balance score (0 = perfectly imbalanced, 1 = perfectly balanced)
            total_flows = sum(dimension_flows.values())
            if total_flows > 0:
                expected_per_dim = total_flows / len(dimension_flows)
                variance = sum(
                    (count - expected_per_dim) ** 2 for count in dimension_flows.values()
                ) / len(dimension_flows)

                # Normalize to 0-1 scale
                max_variance = expected_per_dim**2
                balance_score = 1.0 - min(1.0, variance / max(max_variance, 1))
                self.current_metrics.dimension_balance_score = balance_score

    def _check_health(self):
        """Check system health and update alerts"""
        now = datetime.now(UTC)

        for dim_health in self.dimension_health.values():
            dim_health.alerts.clear()
            dim_health.health_score = 1.0

            # Check for stagnation
            if dim_health.last_activity:
                time_since_activity = (now - dim_health.last_activity).total_seconds()
                if time_since_activity > 60:  # No activity for 1 minute
                    dim_health.alerts.append("Dimension stagnant")
                    dim_health.health_score *= 0.5

            # Check for imbalance
            if dim_health.incoming_flows > 0 or dim_health.outgoing_flows > 0:
                flow_ratio = min(
                    dim_health.incoming_flows / max(dim_health.outgoing_flows, 1),
                    dim_health.outgoing_flows / max(dim_health.incoming_flows, 1),
                )
                if flow_ratio < 0.2:  # Severe imbalance
                    dim_health.alerts.append("Flow imbalance detected")
                    dim_health.health_score *= 0.7

        # Calculate overall circulation health
        health_scores = [dh.health_score for dh in self.dimension_health.values()]
        self.current_metrics.circulation_health = sum(health_scores) / len(health_scores)

    def get_current_metrics(self) -> FlowMetrics:
        """Get current monitoring metrics"""
        return self.current_metrics

    def get_dimension_health(self, dimension: ConsciousnessDimension) -> DimensionHealth:
        """Get health metrics for a specific dimension"""
        return self.dimension_health[dimension]

    def get_health_alerts(self) -> list[tuple[ConsciousnessDimension, list[str]]]:
        """Get all active health alerts"""
        alerts = []
        for dim_health in self.dimension_health.values():
            if dim_health.alerts:
                alerts.append((dim_health.dimension, dim_health.alerts))
        return alerts

    def get_flow_trend(self, minutes: int = 5) -> list[float]:
        """Get flow rate trend over specified minutes"""
        if not self.metrics_history:
            return []

        # Get last N metrics (1 per second)
        lookback = min(minutes * 60, len(self.metrics_history))
        return [m.flows_per_minute for m in list(self.metrics_history)[-lookback:]]

    def get_pattern_emergence_rate(self) -> float:
        """Calculate rate of new pattern emergence"""
        if not self.pattern_emergence_times:
            return 0.0

        now = datetime.now(UTC)
        recent_patterns = [
            pattern
            for pattern, emergence_time in self.pattern_emergence_times.items()
            if (now - emergence_time).total_seconds() < 300  # Last 5 minutes
        ]

        return len(recent_patterns) / 5.0  # Patterns per minute

    def get_top_patterns(self, limit: int = 10) -> list[tuple[str, int]]:
        """Get most frequent patterns"""
        sorted_patterns = sorted(self.pattern_frequencies.items(), key=lambda x: x[1], reverse=True)
        return sorted_patterns[:limit]

    def get_bridge_health(self) -> dict[str, float]:
        """Get health scores for each bridge"""
        bridge_health = {}
        metrics = self.orchestrator.get_bridge_metrics()

        for bridge_name, bridge_data in metrics.items():
            if bridge_data["total_flows"] > 0:
                # Health based on success rate and transformation quality
                health = (
                    bridge_data["success_rate"] * 0.7
                    + bridge_data["average_transformation_score"] * 0.3
                )
                bridge_health[bridge_name] = health

        return bridge_health

    def generate_health_report(self) -> dict[str, Any]:
        """Generate comprehensive health report"""
        return {
            "timestamp": datetime.now(UTC).isoformat(),
            "overall_health": self.current_metrics.circulation_health,
            "metrics": {
                "flow_rate": self.current_metrics.flows_per_minute,
                "average_consciousness": self.current_metrics.average_consciousness,
                "transformation_success": self.current_metrics.transformation_success_rate,
                "pattern_diversity": self.current_metrics.pattern_diversity_score,
                "dimension_balance": self.current_metrics.dimension_balance_score,
            },
            "dimension_health": {
                dim.value: {
                    "health_score": health.health_score,
                    "alerts": health.alerts,
                    "activity": {
                        "incoming": health.incoming_flows,
                        "outgoing": health.outgoing_flows,
                        "last_activity": health.last_activity.isoformat()
                        if health.last_activity
                        else None,
                    },
                }
                for dim, health in self.dimension_health.items()
            },
            "alerts": [
                {"dimension": dim.value, "alerts": alerts}
                for dim, alerts in self.get_health_alerts()
            ],
            "pattern_emergence_rate": self.get_pattern_emergence_rate(),
            "top_patterns": self.get_top_patterns(5),
        }


# Health emerges through conscious observation
