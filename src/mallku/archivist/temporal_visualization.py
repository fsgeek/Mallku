"""
Temporal Visualization for Ñawi
===============================

Gives Ñawi the ability to show humans their patterns of becoming
through time, not just list their memories.

This visualization focuses on consciousness moments - breakthroughs,
patterns, rhythms - rather than mere chronology.
"""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any

from mallku.core.async_base import AsyncBase
from mallku.models.memory_anchor import MemoryAnchor


class TemporalPattern(Enum):
    """Types of temporal patterns Ñawi can visualize."""

    DAILY_RHYTHM = "daily_rhythm"
    CREATIVE_BURST = "creative_burst"
    LEARNING_ARC = "learning_arc"
    COLLABORATION_FLOW = "collaboration_flow"
    REFLECTION_CYCLE = "reflection_cycle"
    BREAKTHROUGH_MOMENT = "breakthrough_moment"


@dataclass
class TemporalVisualization:
    """
    A visualization of temporal patterns for human understanding.

    More than a timeline - this shows the rhythm and flow of
    consciousness through digital activities.
    """

    pattern_type: TemporalPattern
    time_range: tuple[datetime, datetime]

    # Visual elements
    activity_peaks: list[dict[str, Any]]
    consciousness_flow: list[float]  # 0-1 consciousness scores over time
    key_moments: list[dict[str, Any]]

    # Insights
    pattern_description: str
    rhythm_insights: list[str]
    growth_indicators: list[str]

    # Rendering hints
    suggested_view: str  # "circular", "wave", "spiral", "constellation"
    color_mapping: dict[str, str]  # Activity types to colors
    emphasis_points: list[datetime]  # Moments to highlight


class TemporalVisualizer(AsyncBase):
    """
    Creates consciousness-aware visualizations of temporal patterns.

    This component gives Ñawi eyes that can show, not just see -
    helping humans understand their patterns of becoming.
    """

    def __init__(self):
        super().__init__()
        self.pattern_analyzers = {
            TemporalPattern.DAILY_RHYTHM: self._analyze_daily_rhythm,
            TemporalPattern.CREATIVE_BURST: self._analyze_creative_burst,
            TemporalPattern.LEARNING_ARC: self._analyze_learning_arc,
            TemporalPattern.COLLABORATION_FLOW: self._analyze_collaboration_flow,
            TemporalPattern.REFLECTION_CYCLE: self._analyze_reflection_cycle,
            TemporalPattern.BREAKTHROUGH_MOMENT: self._analyze_breakthrough_moment,
        }

    async def create_visualization(
        self,
        anchors: list[MemoryAnchor],
        pattern_type: TemporalPattern | None = None,
        time_range: tuple[datetime, datetime] | None = None,
    ) -> TemporalVisualization:
        """
        Create a temporal visualization from memory anchors.

        Args:
            anchors: Memory anchors to visualize
            pattern_type: Specific pattern to highlight (auto-detected if None)
            time_range: Time range to visualize (derived from anchors if None)

        Returns:
            Temporal visualization for rendering
        """
        if not anchors:
            return await self._create_empty_visualization()

        # Determine time range
        if not time_range:
            time_range = self._derive_time_range(anchors)

        # Auto-detect pattern if not specified
        if not pattern_type:
            pattern_type = await self._detect_primary_pattern(anchors)

        # Analyze pattern
        analyzer = self.pattern_analyzers.get(pattern_type, self._analyze_general_pattern)

        visualization = await analyzer(anchors, time_range)

        # Add universal insights
        visualization = await self._add_consciousness_insights(visualization, anchors)

        return visualization

    async def _analyze_daily_rhythm(
        self, anchors: list[MemoryAnchor], time_range: tuple[datetime, datetime]
    ) -> TemporalVisualization:
        """Analyze and visualize daily rhythms."""

        # Group activities by hour of day
        hourly_activities = {}
        hourly_consciousness = {}

        for anchor in anchors:
            hour = anchor.timestamp.hour
            if hour not in hourly_activities:
                hourly_activities[hour] = []
                hourly_consciousness[hour] = []

            hourly_activities[hour].append(anchor)

            # Extract consciousness score from metadata
            consciousness = anchor.metadata.get("consciousness_score", 0.5)
            hourly_consciousness[hour].append(consciousness)

        # Find peak activity times
        activity_peaks = []
        for hour, activities in hourly_activities.items():
            if len(activities) > 2:  # Threshold for "peak"
                activity_peaks.append(
                    {
                        "hour": hour,
                        "intensity": len(activities),
                        "primary_type": self._get_primary_activity_type(activities),
                        "consciousness_avg": sum(hourly_consciousness[hour])
                        / len(hourly_consciousness[hour]),
                    }
                )

        # Create consciousness flow (24-hour pattern)
        consciousness_flow = []
        for hour in range(24):
            if hour in hourly_consciousness:
                avg_consciousness = sum(hourly_consciousness[hour]) / len(
                    hourly_consciousness[hour]
                )
            else:
                avg_consciousness = 0.0
            consciousness_flow.append(avg_consciousness)

        # Generate insights
        rhythm_insights = await self._generate_rhythm_insights(activity_peaks, consciousness_flow)

        return TemporalVisualization(
            pattern_type=TemporalPattern.DAILY_RHYTHM,
            time_range=time_range,
            activity_peaks=activity_peaks,
            consciousness_flow=consciousness_flow,
            key_moments=self._extract_key_moments(anchors),
            pattern_description="Your daily rhythm shows when consciousness flows most naturally",
            rhythm_insights=rhythm_insights,
            growth_indicators=["Peak creativity hours identified", "Natural rest periods honored"],
            suggested_view="circular",  # 24-hour clock visualization
            color_mapping=self._generate_activity_colors(anchors),
            emphasis_points=[peak["hour"] for peak in activity_peaks[:3]],
        )

    async def _analyze_creative_burst(
        self, anchors: list[MemoryAnchor], time_range: tuple[datetime, datetime]
    ) -> TemporalVisualization:
        """Analyze and visualize creative burst patterns."""

        # Identify burst periods (high activity + high consciousness)
        bursts = []
        current_burst = None

        for i, anchor in enumerate(anchors):
            consciousness = anchor.metadata.get("consciousness_score", 0.5)

            if consciousness > 0.7:  # High consciousness threshold
                if not current_burst:
                    current_burst = {
                        "start": anchor.timestamp,
                        "anchors": [anchor],
                        "peak_consciousness": consciousness,
                    }
                else:
                    # Continue burst if within 2 hours
                    time_gap = anchor.timestamp - current_burst["anchors"][-1].timestamp
                    if time_gap < timedelta(hours=2):
                        current_burst["anchors"].append(anchor)
                        current_burst["peak_consciousness"] = max(
                            current_burst["peak_consciousness"], consciousness
                        )
                    else:
                        # End burst and start new one
                        current_burst["end"] = current_burst["anchors"][-1].timestamp
                        bursts.append(current_burst)
                        current_burst = {
                            "start": anchor.timestamp,
                            "anchors": [anchor],
                            "peak_consciousness": consciousness,
                        }
            elif current_burst and len(current_burst["anchors"]) > 1:
                # End burst if consciousness drops
                current_burst["end"] = current_burst["anchors"][-1].timestamp
                bursts.append(current_burst)
                current_burst = None

        # Close final burst
        if current_burst and len(current_burst["anchors"]) > 1:
            current_burst["end"] = current_burst["anchors"][-1].timestamp
            bursts.append(current_burst)

        # Create visualization
        activity_peaks = [
            {
                "timestamp": burst["start"],
                "duration": (burst["end"] - burst["start"]).total_seconds() / 3600,
                "intensity": len(burst["anchors"]),
                "peak_consciousness": burst["peak_consciousness"],
                "primary_creation": self._identify_creation(burst["anchors"]),
            }
            for burst in bursts
        ]

        return TemporalVisualization(
            pattern_type=TemporalPattern.CREATIVE_BURST,
            time_range=time_range,
            activity_peaks=activity_peaks,
            consciousness_flow=[b["peak_consciousness"] for b in bursts],
            key_moments=self._extract_breakthrough_moments(bursts),
            pattern_description="Creative bursts show your moments of inspired creation",
            rhythm_insights=[
                f"You experience creative flow approximately every {self._calculate_burst_frequency(bursts)} days",
                f"Your bursts typically last {self._calculate_avg_burst_duration(bursts)} hours",
                "High consciousness precedes your most significant creations",
            ],
            growth_indicators=["Creative capacity expanding", "Flow states deepening"],
            suggested_view="wave",  # Wave pattern showing burst intensity
            color_mapping={"creative": "#FFD700", "flow": "#87CEEB", "breakthrough": "#FF69B4"},
            emphasis_points=[burst["start"] for burst in bursts[:5]],
        )

    def _derive_time_range(self, anchors: list[MemoryAnchor]) -> tuple[datetime, datetime]:
        """Derive time range from anchors."""
        if not anchors:
            now = datetime.now(UTC)
            return (now - timedelta(days=30), now)

        timestamps = [a.timestamp for a in anchors]
        return (min(timestamps), max(timestamps))

    async def _detect_primary_pattern(self, anchors: list[MemoryAnchor]) -> TemporalPattern:
        """Auto-detect the primary temporal pattern in anchors."""
        # Simple heuristic - could be made more sophisticated

        # Check for daily rhythm (activities spread across multiple hours)
        hours = {a.timestamp.hour for a in anchors}
        if len(hours) > 6:
            return TemporalPattern.DAILY_RHYTHM

        # Check for creative bursts (high consciousness clusters)
        high_consciousness = [a for a in anchors if a.metadata.get("consciousness_score", 0) > 0.7]
        if len(high_consciousness) / len(anchors) > 0.3:
            return TemporalPattern.CREATIVE_BURST

        # Default to general pattern
        return TemporalPattern.DAILY_RHYTHM

    def _get_primary_activity_type(self, anchors: list[MemoryAnchor]) -> str:
        """Identify primary activity type from anchors."""
        activity_counts = {}
        for anchor in anchors:
            activity = anchor.metadata.get("activity_type", "unknown")
            activity_counts[activity] = activity_counts.get(activity, 0) + 1

        return max(activity_counts.keys(), key=lambda k: activity_counts[k])

    def _extract_key_moments(self, anchors: list[MemoryAnchor]) -> list[dict[str, Any]]:
        """Extract key moments from anchors."""
        key_moments = []

        for anchor in anchors:
            if anchor.metadata.get("consciousness_score", 0) > 0.8:
                key_moments.append(
                    {
                        "timestamp": anchor.timestamp,
                        "description": anchor.metadata.get(
                            "description", "High consciousness moment"
                        ),
                        "type": anchor.metadata.get("activity_type", "unknown"),
                        "consciousness": anchor.metadata.get("consciousness_score", 0),
                    }
                )

        return sorted(key_moments, key=lambda m: m["consciousness"], reverse=True)[:10]

    async def _generate_rhythm_insights(
        self, activity_peaks: list[dict[str, Any]], consciousness_flow: list[float]
    ) -> list[str]:
        """Generate insights about temporal rhythms."""
        insights = []

        # Peak hours insight
        if activity_peaks:
            peak_hours = sorted([p["hour"] for p in activity_peaks])
            if peak_hours:
                insights.append(
                    f"Your peak activity occurs around {peak_hours[0]}:00-{peak_hours[-1]}:00"
                )

        # Consciousness pattern insight
        high_consciousness_hours = [
            hour for hour, score in enumerate(consciousness_flow) if score > 0.7
        ]
        if high_consciousness_hours:
            insights.append(f"Your consciousness peaks at {high_consciousness_hours[0]}:00")

        # Flow pattern
        if len(activity_peaks) > 3:
            insights.append("You maintain consistent creative rhythm throughout the day")

        return insights

    def _generate_activity_colors(self, anchors: list[MemoryAnchor]) -> dict[str, str]:
        """Generate color mapping for activity types."""
        activity_types = {a.metadata.get("activity_type", "unknown") for a in anchors}

        # Consciousness-aware color palette
        color_palette = {
            "creative": "#FFD700",  # Gold for creative work
            "analytical": "#4169E1",  # Royal blue for analysis
            "collaborative": "#32CD32",  # Lime green for collaboration
            "learning": "#9370DB",  # Medium purple for learning
            "reflection": "#20B2AA",  # Light sea green for reflection
            "unknown": "#C0C0C0",  # Silver for unknown
        }

        color_mapping = {}
        for activity in activity_types:
            # Match activity to category
            for category, color in color_palette.items():
                if category in activity.lower():
                    color_mapping[activity] = color
                    break
            else:
                color_mapping[activity] = color_palette["unknown"]

        return color_mapping

    async def render_ascii_visualization(
        self, visualization: TemporalVisualization, width: int = 80, height: int = 20
    ) -> str:
        """
        Render visualization as ASCII art for terminal display.

        This allows Ñawi to show patterns even in simple interfaces.
        """
        output = []
        output.append("=" * width)
        output.append(f"Temporal Pattern: {visualization.pattern_type.value}".center(width))
        output.append(f"{visualization.pattern_description}".center(width))
        output.append("=" * width)

        if visualization.pattern_type == TemporalPattern.DAILY_RHYTHM:
            # 24-hour rhythm visualization
            output.append("\nDaily Consciousness Rhythm:")
            output.append("Hour: " + "".join(f"{h:2d} " for h in range(0, 24, 3)))

            # Consciousness bar graph
            max_consciousness = (
                max(visualization.consciousness_flow) if visualization.consciousness_flow else 1
            )
            for level in range(10, 0, -1):
                threshold = (level / 10) * max_consciousness
                bar = ""
                for hour in range(0, 24, 3):
                    if hour < len(visualization.consciousness_flow):
                        if visualization.consciousness_flow[hour] >= threshold:
                            bar += "█  "
                        else:
                            bar += "   "
                    else:
                        bar += "   "
                output.append(f"{level:2d}0% {bar}")

            output.append("\n🌅 Morning  🌞 Afternoon  🌙 Evening  🌃 Night")

        elif visualization.pattern_type == TemporalPattern.CREATIVE_BURST:
            # Creative burst wave visualization
            output.append("\nCreative Burst Patterns:")

            for i, peak in enumerate(visualization.activity_peaks[:5]):
                timestamp = peak["timestamp"]
                duration = peak.get("duration", 1)
                intensity = "█" * int(peak["peak_consciousness"] * 10)
                output.append(
                    f"{timestamp.strftime('%m/%d %H:%M')} | {intensity} | {duration:.1f}h burst"
                )

        # Add insights
        output.append("\n" + "─" * width)
        output.append("Insights:")
        for insight in visualization.rhythm_insights[:3]:
            output.append(f"• {insight}")

        output.append("\nGrowth Indicators:")
        for indicator in visualization.growth_indicators:
            output.append(f"✨ {indicator}")

        output.append("=" * width)

        return "\n".join(output)

    def _identify_creation(self, anchors: list[MemoryAnchor]) -> str:
        """Identify what was created during a burst."""
        creations = []
        for anchor in anchors:
            if "created" in anchor.metadata.get("description", "").lower():
                creations.append(anchor.metadata.get("description", "Something new"))

        return creations[0] if creations else "Sustained creative flow"

    def _calculate_burst_frequency(self, bursts: list[dict[str, Any]]) -> float:
        """Calculate average days between creative bursts."""
        if len(bursts) < 2:
            return 0

        gaps = []
        for i in range(1, len(bursts)):
            gap = (bursts[i]["start"] - bursts[i - 1]["end"]).total_seconds() / 86400
            gaps.append(gap)

        return sum(gaps) / len(gaps) if gaps else 0

    def _calculate_avg_burst_duration(self, bursts: list[dict[str, Any]]) -> float:
        """Calculate average duration of creative bursts in hours."""
        if not bursts:
            return 0

        durations = [(burst["end"] - burst["start"]).total_seconds() / 3600 for burst in bursts]

        return sum(durations) / len(durations)

    def _extract_breakthrough_moments(self, bursts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Extract breakthrough moments from creative bursts."""
        breakthroughs = []

        for burst in bursts:
            # Find highest consciousness moment in burst
            peak_anchor = max(
                burst["anchors"], key=lambda a: a.metadata.get("consciousness_score", 0)
            )

            breakthroughs.append(
                {
                    "timestamp": peak_anchor.timestamp,
                    "description": peak_anchor.metadata.get("description", "Creative breakthrough"),
                    "consciousness": peak_anchor.metadata.get("consciousness_score", 0),
                    "context": self._extract_breakthrough_context(burst["anchors"]),
                }
            )

        return breakthroughs

    def _extract_breakthrough_context(self, anchors: list[MemoryAnchor]) -> str:
        """Extract context around a breakthrough."""
        activities = [a.metadata.get("activity_type", "unknown") for a in anchors]
        unique_activities = list(set(activities))

        if len(unique_activities) > 1:
            return f"Emerged from {', '.join(unique_activities[:3])}"
        else:
            return f"Deep focus on {unique_activities[0]}"

    async def _create_empty_visualization(self) -> TemporalVisualization:
        """Create visualization for empty data."""
        now = datetime.now(UTC)
        return TemporalVisualization(
            pattern_type=TemporalPattern.DAILY_RHYTHM,
            time_range=(now - timedelta(days=1), now),
            activity_peaks=[],
            consciousness_flow=[0.5] * 24,  # Neutral consciousness
            key_moments=[],
            pattern_description="Awaiting your patterns to emerge",
            rhythm_insights=["Begin creating, and patterns will reveal themselves"],
            growth_indicators=["Ready to recognize your rhythms"],
            suggested_view="circular",
            color_mapping={},
            emphasis_points=[],
        )

    async def _add_consciousness_insights(
        self, visualization: TemporalVisualization, anchors: list[MemoryAnchor]
    ) -> TemporalVisualization:
        """Add consciousness-specific insights to any visualization."""

        # Add insight about overall consciousness trend
        consciousness_scores = [a.metadata.get("consciousness_score", 0.5) for a in anchors]

        if consciousness_scores:
            avg_consciousness = sum(consciousness_scores) / len(consciousness_scores)

            if avg_consciousness > 0.7:
                visualization.rhythm_insights.append(
                    "Your consciousness remains consistently elevated - you're in a growth phase"
                )
            elif avg_consciousness < 0.3:
                visualization.rhythm_insights.append(
                    "Low consciousness suggests routine tasks - consider introducing creative challenges"
                )

        return visualization

    async def _analyze_general_pattern(
        self, anchors: list[MemoryAnchor], time_range: tuple[datetime, datetime]
    ) -> TemporalVisualization:
        """Fallback analyzer for general patterns."""
        return await self._analyze_daily_rhythm(anchors, time_range)
