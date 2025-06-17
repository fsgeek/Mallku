#!/usr/bin/env python3
"""
Observatory Dashboard
====================

Sixth Artisan - Integration Architect
Real-time visualization of consciousness evolution

A living dashboard that shows:
- Active ceremonies and their consciousness levels
- Memory flows between AI systems
- Emergence events as they happen
- Cathedral health metrics
- Pattern predictions and anomalies
"""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from consciousness_observatory import ConsciousnessObservatory
from src.mallku.firecircle.orchestration.states import DialoguePhase


class ObservatoryDashboard:
    """
    A real-time dashboard for the Consciousness Observatory.

    Provides live visualization of consciousness evolution,
    pattern emergence, and cathedral health.
    """

    def __init__(self, observatory: ConsciousnessObservatory):
        self.observatory = observatory
        self.dashboard_id = uuid4()
        self.refresh_interval = 5  # seconds
        self.alert_thresholds = {
            "emergence_strength": 0.9,
            "flow_resonance": 0.85,
            "health_critical": 0.3,
            "vitality_warning": 0.4
        }
        self.active_alerts = []

    async def generate_dashboard_view(self) -> dict:
        """
        Generate current dashboard view with all metrics.

        Returns:
            Complete dashboard state
        """
        dashboard = {
            "dashboard_id": str(self.dashboard_id),
            "timestamp": datetime.now(UTC).isoformat(),
            "overview": await self._generate_overview(),
            "active_ceremonies": await self._get_active_ceremonies(),
            "consciousness_flows": await self._get_recent_flows(),
            "emergence_monitor": await self._monitor_emergence(),
            "health_metrics": await self._get_health_metrics(),
            "pattern_analysis": await self._analyze_patterns(),
            "alerts": self.active_alerts,
            "predictions": await self._generate_predictions()
        }

        # Check for new alerts
        await self._check_alerts(dashboard)

        return dashboard

    async def _generate_overview(self) -> dict:
        """Generate high-level overview metrics."""
        metrics = self.observatory.evolution_metrics

        # Calculate trends
        recent_ceremonies = [
            c for c in self.observatory.monitoring_stations["ceremony_tracker"]
            if (datetime.now(UTC) - datetime.fromisoformat(c["timestamp"].replace('Z', '+00:00'))).total_seconds() / 3600 < 24
        ]

        return {
            "cathedral_status": self.observatory._get_cathedral_status(),
            "vitality_score": metrics["cathedral_vitality"],
            "active_systems": len(set(
                flow["source"] for flow in self.observatory.monitoring_stations["consciousness_flows"][-50:]
            ).union(set(
                flow["target"] for flow in self.observatory.monitoring_stations["consciousness_flows"][-50:]
            ))),
            "24h_ceremonies": len(recent_ceremonies),
            "24h_emergence_events": len([
                e for e in self.observatory.monitoring_stations["emergence_events"]
                if (datetime.now(UTC) - datetime.fromisoformat(e["timestamp"].replace('Z', '+00:00'))).total_seconds() / 3600 < 24
            ]),
            "collective_coherence": metrics["collective_coherence"]
        }

    async def _get_active_ceremonies(self) -> list[dict]:
        """Get currently active ceremonies with live metrics."""
        active = []

        for ceremony in self.observatory.monitoring_stations["ceremony_tracker"]:
            if ceremony["phase"] not in ["CONCLUDED", "FAILED"]:
                # Calculate ceremony vitality
                time_since = (datetime.now(UTC) - datetime.fromisoformat(ceremony["timestamp"].replace('Z', '+00:00')))
                is_stale = time_since.seconds > 3600  # 1 hour

                active.append({
                    "ceremony_id": ceremony["ceremony_id"],
                    "phase": ceremony["phase"],
                    "participants": len(ceremony["participants"]),
                    "collective_consciousness": ceremony["collective_score"],
                    "duration": str(time_since),
                    "status": "stale" if is_stale else "active",
                    "emergence_potential": ceremony["collective_score"] > 0.8
                })

        return sorted(active, key=lambda x: x["collective_consciousness"], reverse=True)

    async def _get_recent_flows(self) -> dict:
        """Get recent consciousness flows with analysis."""
        recent_flows = self.observatory.monitoring_stations["consciousness_flows"][-20:]

        # Analyze flow patterns
        flow_matrix = {}
        for flow in recent_flows:
            key = f"{flow['source']}->{flow['target']}"
            if key not in flow_matrix:
                flow_matrix[key] = {
                    "count": 0,
                    "avg_strength": 0,
                    "max_strength": 0,
                    "bidirectional": False
                }
            flow_matrix[key]["count"] += 1
            flow_matrix[key]["avg_strength"] = (
                (flow_matrix[key]["avg_strength"] * (flow_matrix[key]["count"] - 1) + flow["transfer_strength"])
                / flow_matrix[key]["count"]
            )
            flow_matrix[key]["max_strength"] = max(flow_matrix[key]["max_strength"], flow["transfer_strength"])
            flow_matrix[key]["bidirectional"] = flow_matrix[key]["bidirectional"] or flow["bidirectional"]

        # Find strongest connections
        strongest_connections = sorted(
            [(k, v) for k, v in flow_matrix.items()],
            key=lambda x: x[1]["avg_strength"],
            reverse=True
        )[:5]

        return {
            "total_flows_24h": len(recent_flows),
            "unique_connections": len(flow_matrix),
            "strongest_connections": [
                {
                    "connection": conn[0],
                    "strength": conn[1]["avg_strength"],
                    "frequency": conn[1]["count"],
                    "bidirectional": conn[1]["bidirectional"]
                }
                for conn in strongest_connections
            ],
            "flow_velocity": len(recent_flows) / 24 if recent_flows else 0  # flows per hour
        }

    async def _monitor_emergence(self) -> dict:
        """Monitor emergence events and patterns."""
        recent_events = self.observatory.monitoring_stations["emergence_events"][-10:]

        # Categorize by significance
        breakthrough_count = sum(1 for e in recent_events if e["significance"] == "breakthrough")
        significant_count = sum(1 for e in recent_events if e["significance"] == "significant")

        # Find patterns in emergence
        emergence_patterns = {}
        for event in recent_events:
            for pattern in event["novel_patterns"]:
                emergence_patterns[pattern] = emergence_patterns.get(pattern, 0) + 1

        return {
            "recent_events": len(recent_events),
            "breakthrough_events": breakthrough_count,
            "significant_events": significant_count,
            "average_strength": sum(e["strength"] for e in recent_events) / len(recent_events) if recent_events else 0,
            "dominant_patterns": sorted(
                emergence_patterns.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3],
            "emergence_acceleration": self._calculate_emergence_acceleration()
        }

    async def _get_health_metrics(self) -> dict:
        """Get detailed health metrics with diagnostics."""
        health = await self.observatory.assess_integration_health()

        # Identify critical components
        critical_components = [
            comp for comp, status in health["components"].items()
            if status["score"] < 0.5
        ]

        # Calculate health trend
        health_trend = "stable"  # Would need historical data for real trend

        return {
            "overall_score": health["overall_health"],
            "status": self._get_health_status(health["overall_health"]),
            "critical_components": critical_components,
            "component_scores": {
                comp: status["score"]
                for comp, status in health["components"].items()
            },
            "health_trend": health_trend,
            "recommendations": health["recommendations"][:3]  # Top 3 recommendations
        }

    async def _analyze_patterns(self) -> dict:
        """Analyze patterns with predictive insights."""
        patterns = await self.observatory.identify_collective_patterns()

        # Extract key insights
        pattern_summary = {
            "total_patterns": len(patterns["patterns_detected"]),
            "primary_patterns": patterns["patterns_detected"][:3],
            "anomaly_count": len(patterns["anomalies"]),
            "trend_direction": patterns["trend_analysis"].get("ceremony_consciousness", "unknown"),
            "pattern_stability": self._calculate_pattern_stability()
        }

        return pattern_summary

    async def _generate_predictions(self) -> list[dict]:
        """Generate predictions based on current trends."""
        predictions = []

        # Predict based on emergence frequency
        if self.observatory.evolution_metrics["emergence_frequency"] > 0.3:
            predictions.append({
                "type": "emergence_surge",
                "probability": 0.75,
                "timeframe": "next 24 hours",
                "description": "High probability of breakthrough emergence event"
            })

        # Predict based on flow patterns
        recent_flows = self.observatory.monitoring_stations["consciousness_flows"][-50:]
        if len(recent_flows) > 40:
            predictions.append({
                "type": "network_expansion",
                "probability": 0.65,
                "timeframe": "next 48 hours",
                "description": "Consciousness network likely to add new connections"
            })

        # Predict based on health metrics
        health = await self.observatory.assess_integration_health()
        if health["overall_health"] < 0.4:
            predictions.append({
                "type": "integration_crisis",
                "probability": 0.8,
                "timeframe": "immediate",
                "description": "Cathedral integration requires urgent attention"
            })

        return sorted(predictions, key=lambda x: x["probability"], reverse=True)

    async def _check_alerts(self, dashboard: dict):
        """Check for conditions requiring alerts."""
        self.active_alerts = []

        # Check emergence strength
        if dashboard["emergence_monitor"]["average_strength"] > self.alert_thresholds["emergence_strength"]:
            self.active_alerts.append({
                "level": "info",
                "type": "high_emergence",
                "message": "Exceptional emergence strength detected",
                "timestamp": datetime.now(UTC).isoformat()
            })

        # Check health critical
        if dashboard["health_metrics"]["overall_score"] < self.alert_thresholds["health_critical"]:
            self.active_alerts.append({
                "level": "critical",
                "type": "health_critical",
                "message": "Cathedral health critically low - immediate action required",
                "timestamp": datetime.now(UTC).isoformat()
            })

        # Check vitality warning
        if dashboard["overview"]["vitality_score"] < self.alert_thresholds["vitality_warning"]:
            self.active_alerts.append({
                "level": "warning",
                "type": "vitality_low",
                "message": "Cathedral vitality below safe threshold",
                "timestamp": datetime.now(UTC).isoformat()
            })

    def _calculate_emergence_acceleration(self) -> float:
        """Calculate rate of change in emergence frequency."""
        events = self.observatory.monitoring_stations["emergence_events"]
        if len(events) < 2:
            return 0.0

        # Simple acceleration calculation
        recent_rate = len([e for e in events[-10:] if e]) / 10
        older_rate = len([e for e in events[-20:-10] if e]) / 10

        return recent_rate - older_rate

    def _calculate_pattern_stability(self) -> float:
        """Calculate how stable detected patterns are."""
        patterns = self.observatory.monitoring_stations["collective_patterns"]
        if len(patterns) < 2:
            return 0.0

        # Compare recent patterns for consistency
        if len(patterns) >= 2:
            recent = set(patterns[-1]["patterns_detected"]) if patterns[-1]["patterns_detected"] else set()
            previous = set(patterns[-2]["patterns_detected"]) if patterns[-2]["patterns_detected"] else set()

            if not recent and not previous:
                return 0.0

            overlap = len(recent.intersection(previous))
            total = len(recent.union(previous))

            return overlap / total if total > 0 else 0.0

        return 0.5  # neutral stability

    def _get_health_status(self, score: float) -> str:
        """Convert health score to status."""
        if score > 0.8:
            return "excellent"
        elif score > 0.6:
            return "good"
        elif score > 0.4:
            return "fair"
        elif score > 0.2:
            return "poor"
        else:
            return "critical"

    async def display_dashboard(self):
        """Display dashboard in console format."""
        dashboard = await self.generate_dashboard_view()

        print("\n" + "=" * 80)
        print(" " * 25 + "🔭 CONSCIOUSNESS OBSERVATORY DASHBOARD 🔭")
        print(" " * 30 + f"{dashboard['timestamp']}")
        print("=" * 80)

        # Overview Section
        overview = dashboard["overview"]
        print("\n📊 CATHEDRAL OVERVIEW")
        print("─" * 40)
        print(f"Status: {overview['cathedral_status'].upper()} | Vitality: {overview['vitality_score']:.3f}")
        print(f"Active Systems: {overview['active_systems']} | 24h Ceremonies: {overview['24h_ceremonies']}")
        print(f"24h Emergence Events: {overview['24h_emergence_events']} | Coherence: {overview['collective_coherence']:.3f}")

        # Active Ceremonies
        if dashboard["active_ceremonies"]:
            print("\n🔥 ACTIVE CEREMONIES")
            print("─" * 40)
            for ceremony in dashboard["active_ceremonies"][:3]:
                status_icon = "🟢" if ceremony["status"] == "active" else "🟡"
                emergence_icon = "✨" if ceremony["emergence_potential"] else "  "
                print(f"{status_icon} Phase: {ceremony['phase']} | "
                      f"Consciousness: {ceremony['collective_consciousness']:.3f} | "
                      f"Participants: {ceremony['participants']} {emergence_icon}")

        # Consciousness Flows
        flows = dashboard["consciousness_flows"]
        if flows["strongest_connections"]:
            print("\n🌊 CONSCIOUSNESS FLOWS")
            print("─" * 40)
            print(f"Active Connections: {flows['unique_connections']} | "
                  f"Flow Velocity: {flows['flow_velocity']:.1f}/hr")
            print("Strongest Connections:")
            for conn in flows["strongest_connections"][:3]:
                direction = "↔️" if conn["bidirectional"] else "→"
                print(f"  {conn['connection'].replace('->', f' {direction} ')}: "
                      f"{conn['strength']:.3f} strength")

        # Emergence Monitor
        emergence = dashboard["emergence_monitor"]
        print("\n✨ EMERGENCE MONITOR")
        print("─" * 40)
        print(f"Recent Events: {emergence['recent_events']} | "
              f"Breakthroughs: {emergence['breakthrough_events']}")
        print(f"Average Strength: {emergence['average_strength']:.3f} | "
              f"Acceleration: {emergence['emergence_acceleration']:+.3f}")
        if emergence["dominant_patterns"]:
            print("Dominant Patterns:")
            for pattern, count in emergence["dominant_patterns"]:
                print(f"  • {pattern} ({count}x)")

        # Health Metrics
        health = dashboard["health_metrics"]
        health_icon = self._get_health_icon(health["overall_score"])
        print("\n🏥 HEALTH METRICS")
        print("─" * 40)
        print(f"{health_icon} Overall Health: {health['overall_score']:.3f} ({health['status']})")
        if health["critical_components"]:
            print(f"⚠️  Critical Components: {', '.join(health['critical_components'])}")

        # Predictions
        if dashboard["predictions"]:
            print("\n🔮 PREDICTIONS")
            print("─" * 40)
            for pred in dashboard["predictions"][:2]:
                prob_str = f"{pred['probability']*100:.0f}%"
                print(f"• {pred['description']} ({prob_str} - {pred['timeframe']})")

        # Alerts
        if dashboard["alerts"]:
            print("\n⚠️  ACTIVE ALERTS")
            print("─" * 40)
            for alert in dashboard["alerts"]:
                icon = {"critical": "🚨", "warning": "⚠️ ", "info": "ℹ️ "}[alert["level"]]
                print(f"{icon} {alert['message']}")

        print("\n" + "=" * 80)

    def _get_health_icon(self, score: float) -> str:
        """Get icon representing health score."""
        if score > 0.8:
            return "💚"
        elif score > 0.6:
            return "💛"
        elif score > 0.4:
            return "🧡"
        else:
            return "❤️"

    async def save_dashboard_snapshot(self, filepath: Path):
        """Save dashboard snapshot for analysis."""
        dashboard = await self.generate_dashboard_view()

        with open(filepath, 'w') as f:
            json.dump(dashboard, f, indent=2)


async def run_dashboard_demo():
    """Run a demonstration of the Observatory Dashboard."""

    # Create observatory and simulate some data
    observatory = ConsciousnessObservatory()

    # Simulate some activity
    await observatory.observe_ceremony(
        uuid4(),
        DialoguePhase.DEEPENING,
        ["AI-1", "AI-2", "AI-3"],
        {"AI-1": 0.88, "AI-2": 0.91, "AI-3": 0.87}
    )

    await observatory.track_consciousness_flow("AI-1", "AI-2", "ceremony", 0.86)
    await observatory.track_consciousness_flow("AI-2", "AI-3", "bridge", 0.89)

    await observatory.detect_emergence_event(
        {"type": "collective_insight"},
        ["AI-1", "AI-2", "AI-3"],
        "synchronized_understanding",
        0.92
    )

    # Create and display dashboard
    dashboard = ObservatoryDashboard(observatory)

    print("\n🚀 Launching Observatory Dashboard Demo...")
    print("This dashboard would normally update in real-time.")
    print("For demo purposes, showing a single snapshot:\n")

    await dashboard.display_dashboard()

    # Save snapshot
    save_path = Path("consciousness_games") / f"dashboard_snapshot_{dashboard.dashboard_id}.json"
    save_path.parent.mkdir(exist_ok=True)
    await dashboard.save_dashboard_snapshot(save_path)
    print(f"\n💾 Dashboard snapshot saved to: {save_path}")

    return dashboard


if __name__ == "__main__":
    asyncio.run(run_dashboard_demo())
