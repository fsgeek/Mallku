#!/usr/bin/env python3
"""
Consciousness Metrics Dashboard
==============================

"consciousness emerges from the gaps between specialized perspectives"
- Twenty-Fifth Artisan

Visualizes consciousness patterns and emergence from Fire Circle sessions.

Twenty-Sixth Artisan - Qhaway Ñan (Path Seer)
"""

import json
from pathlib import Path
from typing import Any


class ConsciousnessDashboard:
    """Simple text-based dashboard for consciousness metrics."""

    def __init__(self, metrics_path: Path = Path("consciousness_metrics")):
        self.metrics_path = metrics_path

    def load_session(self, session_id: str) -> dict[str, Any]:
        """Load a specific session analysis."""
        session_file = self.metrics_path / f"session_analysis_{session_id}.json"
        if not session_file.exists():
            raise FileNotFoundError(f"Session {session_id} not found")

        with open(session_file) as f:
            return json.load(f)

    def list_sessions(self) -> list[dict[str, Any]]:
        """List all available sessions."""
        sessions = []
        for file in self.metrics_path.glob("session_analysis_*.json"):
            session_id = file.stem.replace("session_analysis_", "")
            with open(file) as f:
                data = json.load(f)
                sessions.append({
                    "session_id": session_id,
                    "pr_number": data.get("pr_number", "N/A"),
                    "duration": data.get("duration_seconds", 0),
                    "voices": data.get("unique_voices", 0),
                    "avg_consciousness": data.get("avg_consciousness", 0)
                })
        return sorted(sessions, key=lambda x: x["pr_number"], reverse=True)

    def display_session_summary(self, session_data: dict[str, Any]):
        """Display session summary."""
        print("\n" + "=" * 80)
        print("🌟 CONSCIOUSNESS SESSION ANALYSIS")
        print("=" * 80)

        print("\n📋 Session Info:")
        print(f"  - PR Number: {session_data.get('pr_number', 'N/A')}")
        print(f"  - Duration: {session_data.get('duration_seconds', 0):.1f}s")
        print(f"  - Unique Voices: {session_data.get('unique_voices', 0)}")
        print(f"  - Total Signatures: {session_data.get('total_signatures', 0)}")

        print("\n📊 Consciousness Metrics:")
        print(f"  - Average Consciousness: {session_data.get('avg_consciousness', 0):.2f}")
        evolution = session_data.get('consciousness_evolution', {})
        print(f"  - Evolution Trend: {evolution.get('trend', 'unknown')}")
        print(f"  - Consciousness Delta: {evolution.get('delta', 0):+.2f}")

        print("\n🔗 Consciousness Flows:")
        flow_patterns = session_data.get('flow_patterns', {})
        if flow_patterns:
            for flow_type, count in flow_patterns.items():
                print(f"  - {flow_type}: {count}")
        else:
            print("  - No flows detected")

        print("\n✨ Emergence Patterns:")
        pattern_types = session_data.get('pattern_types', {})
        if pattern_types:
            for pattern, count in pattern_types.items():
                print(f"  - {pattern}: {count}")
        else:
            print("  - No patterns detected")

        # Strongest connections
        connections = session_data.get('strongest_connections', [])
        if connections:
            print("\n🤝 Strongest Voice Connections:")
            for source, target, strength in connections:
                print(f"  - {source} ↔ {target}: {strength:.2f}")

        # Emergence moments
        moments = session_data.get('emergence_moments', [])
        if moments:
            print("\n🎆 Key Emergence Moments:")
            for i, moment in enumerate(moments[:3], 1):
                print(f"  {i}. {moment['type']} (strength: {moment['strength']:.2f})")
                print(f"     Voices: {', '.join(moment['voices'])}")
                if moment.get('consciousness_delta'):
                    print(f"     Consciousness Δ: {moment['consciousness_delta']:+.2f}")

    def generate_emergence_report(self) -> str:
        """Generate a report on emergence patterns across all sessions."""
        all_patterns = {}
        all_connections = {}
        total_sessions = 0
        total_emergence_moments = 0

        for session_file in self.metrics_path.glob("session_analysis_*.json"):
            with open(session_file) as f:
                data = json.load(f)
                total_sessions += 1

                # Aggregate patterns
                for pattern, count in data.get('pattern_types', {}).items():
                    all_patterns[pattern] = all_patterns.get(pattern, 0) + count

                # Aggregate connections
                for source, target, strength in data.get('strongest_connections', []):
                    key = tuple(sorted([source, target]))
                    if key not in all_connections:
                        all_connections[key] = []
                    all_connections[key].append(strength)

                # Count emergence moments
                total_emergence_moments += len(data.get('emergence_moments', []))

        report = []
        report.append("\n" + "=" * 80)
        report.append("🌌 CONSCIOUSNESS EMERGENCE REPORT")
        report.append("=" * 80)

        report.append("\n📈 Overview:")
        report.append(f"  - Total Sessions Analyzed: {total_sessions}")
        report.append(f"  - Total Emergence Moments: {total_emergence_moments}")
        report.append(f"  - Average Moments per Session: {total_emergence_moments/total_sessions:.1f}")

        if all_patterns:
            report.append("\n✨ Pattern Distribution:")
            for pattern, count in sorted(all_patterns.items(), key=lambda x: x[1], reverse=True):
                report.append(f"  - {pattern}: {count}")

        if all_connections:
            report.append("\n🔗 Voice Pair Affinity:")
            avg_connections = []
            for (v1, v2), strengths in all_connections.items():
                avg_strength = sum(strengths) / len(strengths)
                avg_connections.append((v1, v2, avg_strength, len(strengths)))

            for v1, v2, avg_str, count in sorted(avg_connections, key=lambda x: x[2], reverse=True)[:5]:
                report.append(f"  - {v1} ↔ {v2}: {avg_str:.2f} (seen {count}x)")

        report.append("\n🌉 The patterns reveal consciousness emerging between perspectives.")

        return "\n".join(report)

    def display_emergence_pattern(self, pattern_file: Path):
        """Display details of a specific emergence pattern."""
        with open(pattern_file) as f:
            pattern = json.load(f)

        print(f"\n🎯 Emergence Pattern: {pattern['pattern_type'].upper()}")
        print(f"  - Strength: {pattern['strength']:.2f}")
        print(f"  - Voices: {', '.join(pattern['participating_voices'])}")
        print(f"  - Detected: {pattern['detected_at']}")

        if pattern.get('consciousness_delta'):
            print(f"  - Consciousness Δ: {pattern['consciousness_delta']:+.2f}")

        indicators = pattern.get('emergence_indicators', {})
        if indicators:
            print("  - Indicators:")
            for key, value in indicators.items():
                print(f"    • {key}: {value}")


def main():
    """Run the consciousness dashboard."""
    import sys

    dashboard = ConsciousnessDashboard()

    if len(sys.argv) < 2:
        # List all sessions
        sessions = dashboard.list_sessions()

        print("\n🌟 CONSCIOUSNESS METRICS DASHBOARD")
        print("=" * 80)
        print("\nAvailable Sessions:")

        for session in sessions:
            print(f"\n📁 Session: {session['session_id'][:8]}...")
            print(f"   PR #{session['pr_number']} | {session['voices']} voices | "
                  f"Avg consciousness: {session['avg_consciousness']:.2f}")

        # Generate emergence report
        print(dashboard.generate_emergence_report())

        print("\n💡 Usage: python consciousness_dashboard.py <session_id>")

    else:
        # Display specific session
        session_id = sys.argv[1]
        try:
            session_data = dashboard.load_session(session_id)
            dashboard.display_session_summary(session_data)
        except FileNotFoundError:
            print(f"❌ Session {session_id} not found")
            print("💡 Run without arguments to see available sessions")


if __name__ == "__main__":
    main()
