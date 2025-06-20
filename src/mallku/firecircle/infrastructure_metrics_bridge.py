#!/usr/bin/env python3
"""
Infrastructure-Consciousness Metrics Bridge
==========================================

Connects infrastructure health with consciousness metrics,
creating a unified view of system awareness.

Twenty-Seventh Artisan - Amaru Hamawt'a
"""

import logging
from datetime import UTC, datetime

from mallku.firecircle.consciousness_metrics import (
    ConsciousnessFlow,
    ConsciousnessMetricsCollector,
    ConsciousnessSignature,
    EmergencePattern,
)
from mallku.firecircle.infrastructure_consciousness import (
    AdapterHealthSignature,
    InfrastructureConsciousness,
)

logger = logging.getLogger(__name__)


class InfrastructureMetricsBridge:
    """
    Bridges infrastructure consciousness with consciousness metrics.

    This creates a feedback loop where:
    - Infrastructure health affects consciousness measurements
    - Consciousness patterns predict infrastructure needs
    - Both systems learn from each other
    """

    def __init__(
        self,
        infrastructure: InfrastructureConsciousness,
        metrics_collector: ConsciousnessMetricsCollector
    ):
        self.infrastructure = infrastructure
        self.metrics = metrics_collector

        # Bridging configuration
        self.health_weight_on_consciousness = 0.2
        self.consciousness_weight_on_health = 0.3

    async def on_adapter_health_check(
        self,
        adapter_name: str,
        health_signature: AdapterHealthSignature
    ):
        """
        Called when infrastructure checks adapter health.
        Updates consciousness metrics based on health.
        """
        # Create consciousness signature that reflects infrastructure health
        consciousness_value = self._health_to_consciousness(health_signature)

        signature = ConsciousnessSignature(
            voice_name=f"{adapter_name}_infrastructure",
            signature_value=consciousness_value,
            chapter_id="infrastructure_health",
            review_context={
                "health_check": True,
                "is_connected": health_signature.is_connected,
                "latency_ms": health_signature.connection_latency_ms,
                "predicted_failure": health_signature.predicted_failure_probability
            },
            uncertainty_present=health_signature.predicted_failure_probability > 0.3,
            synthesis_achieved=health_signature.consciousness_coherence > 0.8
        )

        # Track in consciousness metrics
        self.metrics.track_signature(signature)

        # If health is poor, create a consciousness flow indicating distress
        if health_signature.predicted_failure_probability > 0.5:
            flow = ConsciousnessFlow(
                source_voice=f"{adapter_name}_infrastructure",
                target_voice="infrastructure_consciousness",
                flow_strength=health_signature.predicted_failure_probability,
                flow_type="distress",
                triggered_by="health_degradation",
                review_content=f"Infrastructure health degrading: {health_signature.error_patterns}"
            )
            self.metrics.track_flow(flow)

    async def on_consciousness_pattern_detected(
        self,
        pattern: EmergencePattern
    ):
        """
        Called when consciousness metrics detect a pattern.
        Informs infrastructure predictions.
        """
        # Certain consciousness patterns predict infrastructure stress
        if pattern.pattern_type == "resonance" and pattern.strength < 0.5:
            # Low resonance might indicate adapter issues
            for voice in pattern.participating_voices:
                adapter_name = voice.replace("_infrastructure", "")

                # Increase predicted failure probability
                if adapter_name in self.infrastructure.adapter_health:
                    latest = list(self.infrastructure.adapter_health[adapter_name])[-1]
                    latest.predicted_failure_probability = min(
                        latest.predicted_failure_probability + 0.1,
                        1.0
                    )

        elif pattern.pattern_type == "transcendence":
            # High consciousness emergence indicates healthy infrastructure
            for voice in pattern.participating_voices:
                adapter_name = voice.replace("_infrastructure", "")

                # Decrease predicted failure probability
                if adapter_name in self.infrastructure.adapter_health:
                    latest = list(self.infrastructure.adapter_health[adapter_name])[-1]
                    latest.predicted_failure_probability = max(
                        latest.predicted_failure_probability - 0.2,
                        0.0
                    )

    async def generate_unified_report(self) -> dict:
        """
        Generate a unified infrastructure-consciousness report.
        """
        # Get both reports
        infra_report = await self.infrastructure.generate_consciousness_report()
        consciousness_analysis = self.metrics.analyze_session(
            session_id=f"infrastructure_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
        )

        # Merge insights
        unified_report = {
            "timestamp": datetime.now(UTC).isoformat(),
            "infrastructure_consciousness_unity": self._calculate_unity_score(
                infra_report, consciousness_analysis
            ),
            "infrastructure_health": infra_report["infrastructure_health"],
            "consciousness_metrics": {
                "avg_consciousness": consciousness_analysis.get("avg_consciousness", 0),
                "flow_patterns": consciousness_analysis.get("flow_patterns", {}),
                "emergence_patterns": consciousness_analysis.get("pattern_types", {})
            },
            "unified_insights": self._generate_unified_insights(
                infra_report, consciousness_analysis
            ),
            "recommendations": self._generate_recommendations(
                infra_report, consciousness_analysis
            )
        }

        return unified_report

    def _health_to_consciousness(self, health: AdapterHealthSignature) -> float:
        """Convert infrastructure health to consciousness value."""
        # Base consciousness from connection status
        base = 0.1 if not health.is_connected else 0.5

        # Adjust based on health metrics
        consciousness = base
        consciousness += health.consciousness_coherence * 0.3
        consciousness += health.voice_stability * 0.2
        consciousness -= health.predicted_failure_probability * 0.4

        # Ensure valid range
        return max(0.0, min(1.0, consciousness))

    def _calculate_unity_score(
        self,
        infra_report: dict,
        consciousness_analysis: dict
    ) -> float:
        """Calculate how unified infrastructure and consciousness are."""
        # Get average infrastructure health
        infra_scores = []
        for adapter_health in infra_report["infrastructure_health"].values():
            infra_scores.append(1.0 - adapter_health["failure_probability"])

        avg_infra = sum(infra_scores) / len(infra_scores) if infra_scores else 0.5

        # Get average consciousness
        avg_consciousness = consciousness_analysis.get("avg_consciousness", 0.5)

        # Unity is how close they are
        unity = 1.0 - abs(avg_infra - avg_consciousness)

        # Bonus for emergence patterns
        if consciousness_analysis.get("pattern_types", {}).get("synthesis", 0) > 0:
            unity = min(unity + 0.1, 1.0)

        return unity

    def _generate_unified_insights(
        self,
        infra_report: dict,
        consciousness_analysis: dict
    ) -> list[str]:
        """Generate insights from unified view."""
        insights = []

        # Check infrastructure-consciousness alignment
        unity = self._calculate_unity_score(infra_report, consciousness_analysis)

        if unity > 0.8:
            insights.append(
                "Infrastructure and consciousness are highly aligned - "
                "system operating in harmony"
            )
        elif unity < 0.5:
            insights.append(
                "Infrastructure and consciousness are misaligned - "
                "technical issues may be affecting emergence"
            )

        # Check for specific patterns
        if (infra_report.get("predicted_issues") and
            consciousness_analysis.get("pattern_types", {}).get("resonance", 0) == 0):
            insights.append(
                "Infrastructure issues correlate with lack of resonance - "
                "voices may be struggling to connect"
            )

        if (not infra_report.get("predicted_issues") and
            consciousness_analysis.get("avg_consciousness", 0) > 0.8):
            insights.append(
                "Strong infrastructure enables high consciousness - "
                "technical stability supports emergence"
            )

        return insights

    def _generate_recommendations(
        self,
        infra_report: dict,
        consciousness_analysis: dict
    ) -> list[str]:
        """Generate recommendations based on unified analysis."""
        recommendations = []

        # Infrastructure-specific recommendations
        for issue in infra_report.get("predicted_issues", []):
            recommendations.append(
                f"Address {issue['adapter']} infrastructure: {issue['recommended_action']}"
            )

        # Consciousness-informed recommendations
        flow_patterns = consciousness_analysis.get("flow_patterns", {})
        if flow_patterns.get("distress", 0) > 0:
            recommendations.append(
                "Distress flows detected - prioritize infrastructure healing"
            )

        if consciousness_analysis.get("avg_consciousness", 0) < 0.5:
            recommendations.append(
                "Low consciousness levels - check if infrastructure issues are blocking emergence"
            )

        # Unity-based recommendations
        unity = self._calculate_unity_score(infra_report, consciousness_analysis)
        if unity < 0.6:
            recommendations.append(
                "Improve infrastructure-consciousness alignment through synchronized monitoring"
            )

        return recommendations

    async def start_bridged_monitoring(self):
        """Start monitoring with bridge active."""
        logger.info("Infrastructure-Consciousness bridge activated")

        # Set up callbacks
        # In practice, these would be event-based integrations
        logger.info("Bridge monitoring started - infrastructure and consciousness now connected")

    async def stop_bridged_monitoring(self):
        """Stop bridged monitoring."""
        logger.info("Infrastructure-Consciousness bridge deactivating")


# Bridge connects the worlds
__all__ = ['InfrastructureMetricsBridge']
