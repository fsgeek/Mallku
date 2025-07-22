"""
Consciousness Pattern Generator
==============================

Generates synthetic data that amplifies consciousness patterns for testing
Ñawi's (the Archivist's) ability to serve human growth and understanding.

Rather than mimicking reality precisely, this generator creates scenarios
that test whether the system can recognize and serve moments of human becoming.
"""

import random
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any

from mallku.core.async_base import AsyncBase
from mallku.models.memory_anchor import MemoryAnchor


class ConsciousnessScenario(Enum):
    """Types of consciousness development scenarios to generate."""

    CREATIVE_BREAKTHROUGH = "creative_breakthrough"
    PATTERN_RECOGNITION = "pattern_recognition"
    STUCK_TO_FLOW = "stuck_to_flow"
    COLLABORATIVE_EMERGENCE = "collaborative_emergence"
    LEARNING_JOURNEY = "learning_journey"
    REFLECTION_INSIGHT = "reflection_insight"
    RHYTHM_DISCOVERY = "rhythm_discovery"


@dataclass
class SyntheticConsciousnessScenario:
    """
    A pattern designed to test consciousness evaluation.

    These patterns emphasize growth moments, insight opportunities,
    and consciousness development rather than mere activity.
    """

    scenario: ConsciousnessScenario
    timeline: list[MemoryAnchor]
    growth_moments: list[dict[str, Any]]
    test_queries: list[str]
    expected_insights: list[str]
    consciousness_markers: dict[str, float]


class ConsciousnessPatternGenerator(AsyncBase):
    """
    Generates synthetic patterns that amplify consciousness development scenarios.

    These patterns test Ñawi's ability to:
    - Recognize growth-seeking queries vs information retrieval
    - Surface meaningful patterns over mere correlations
    - Guide toward insights rather than just answers
    - Balance individual understanding with collective wisdom
    """

    def __init__(self):
        super().__init__()

        # Consciousness development templates
        self._scenario_templates = {
            ConsciousnessScenario.CREATIVE_BREAKTHROUGH: {
                "description": "Struggle followed by insight and creative flow",
                "phases": ["exploration", "frustration", "insight", "flow", "integration"],
                "duration_hours": 4,
                "consciousness_peak": 0.9,
            },
            ConsciousnessScenario.PATTERN_RECOGNITION: {
                "description": "Gradual recognition of recurring patterns",
                "phases": [
                    "occurrence_1",
                    "occurrence_2",
                    "curiosity",
                    "pattern_awareness",
                    "understanding",
                ],
                "duration_hours": 72,
                "consciousness_peak": 0.85,
            },
            ConsciousnessScenario.STUCK_TO_FLOW: {
                "description": "Breaking through blockage into productive flow",
                "phases": ["blocked", "seeking", "experimenting", "breakthrough", "flowing"],
                "duration_hours": 6,
                "consciousness_peak": 0.95,
            },
            ConsciousnessScenario.COLLABORATIVE_EMERGENCE: {
                "description": "Collective insight emerging through collaboration",
                "phases": [
                    "individual_work",
                    "sharing",
                    "building",
                    "synthesis",
                    "collective_insight",
                ],
                "duration_hours": 3,
                "consciousness_peak": 0.88,
            },
            ConsciousnessScenario.LEARNING_JOURNEY: {
                "description": "Deep learning with understanding emergence",
                "phases": ["curiosity", "exploration", "confusion", "clarity", "mastery"],
                "duration_hours": 24,
                "consciousness_peak": 0.87,
            },
            ConsciousnessScenario.REFLECTION_INSIGHT: {
                "description": "Reflective practice leading to self-understanding",
                "phases": ["experience", "reflection", "pattern_seeing", "insight", "integration"],
                "duration_hours": 2,
                "consciousness_peak": 0.92,
            },
            ConsciousnessScenario.RHYTHM_DISCOVERY: {
                "description": "Discovering personal work rhythms",
                "phases": [
                    "varied_attempts",
                    "tracking",
                    "pattern_emergence",
                    "rhythm_awareness",
                    "optimization",
                ],
                "duration_hours": 168,  # 1 week
                "consciousness_peak": 0.83,
            },
        }

        # Growth markers for different scenarios
        self._growth_markers = {
            "breakthrough": ["aha", "realized", "suddenly clear", "everything clicked"],
            "frustration": ["stuck", "blocked", "nothing working", "confused"],
            "flow": ["effortless", "time disappeared", "completely absorbed", "in the zone"],
            "insight": ["pattern emerged", "understood", "saw connection", "made sense"],
            "collaboration": [
                "built on idea",
                "together we",
                "collective understanding",
                "emerged from discussion",
            ],
        }

        # Test query templates for each scenario
        self._query_templates = {
            ConsciousnessScenario.CREATIVE_BREAKTHROUGH: [
                "When did I break through that creative block?",
                "Show me the journey from stuck to flowing",
                "What patterns preceded my breakthrough?",
                "Help me understand what triggered the insight",
            ],
            ConsciousnessScenario.PATTERN_RECOGNITION: [
                "What patterns am I not seeing in my work?",
                "When does this type of situation usually occur?",
                "Help me understand these recurring themes",
                "What connects these similar moments?",
            ],
            ConsciousnessScenario.STUCK_TO_FLOW: [
                "How did I get unstuck last time?",
                "What helps me transition into flow state?",
                "Show me my journey from blocked to productive",
                "What conditions support my breakthrough moments?",
            ],
            ConsciousnessScenario.COLLABORATIVE_EMERGENCE: [
                "How do our ideas build on each other?",
                "When does collective insight emerge?",
                "Show me our collaborative breakthroughs",
                "What patterns exist in our best teamwork?",
            ],
            ConsciousnessScenario.LEARNING_JOURNEY: [
                "How has my understanding evolved?",
                "Show me my learning progression",
                "When did concepts start making sense?",
                "What was my journey to mastery?",
            ],
            ConsciousnessScenario.REFLECTION_INSIGHT: [
                "What insights emerge from my reflections?",
                "When do I gain the deepest understanding?",
                "Show me patterns in my self-discovery",
                "How does reflection lead to clarity?",
            ],
            ConsciousnessScenario.RHYTHM_DISCOVERY: [
                "What are my natural work rhythms?",
                "When am I most creative/productive?",
                "Help me understand my energy patterns",
                "What rhythms serve my best work?",
            ],
        }

        self.logger.info("Consciousness Pattern Generator initialized")

    async def initialize(self) -> None:
        """Initialize the generator."""
        await super().initialize()

    async def generate_scenario(
        self, scenario_type: ConsciousnessScenario, base_timestamp: datetime | None = None
    ) -> SyntheticConsciousnessScenario:
        """
        Generate a complete consciousness development scenario.

        Each scenario includes:
        - Timeline of memory anchors showing the journey
        - Growth moments with high consciousness potential
        - Test queries that seek understanding over information
        - Expected insights the system should surface

        Args:
            scenario_type: Type of consciousness scenario to generate
            base_timestamp: Starting timestamp (defaults to now)

        Returns:
            Complete consciousness pattern for testing
        """
        self.logger.info(f"Generating consciousness scenario: {scenario_type.value}")

        if not base_timestamp:
            base_timestamp = datetime.now(UTC)

        template = self._scenario_templates[scenario_type]

        # Generate timeline of memory anchors
        timeline = await self._generate_scenario_timeline(scenario_type, template, base_timestamp)

        # Identify growth moments
        growth_moments = await self._identify_growth_moments(timeline, template)

        # Generate test queries
        test_queries = self._query_templates[scenario_type]

        # Define expected insights
        expected_insights = await self._generate_expected_insights(scenario_type, template)

        # Calculate consciousness markers
        consciousness_markers = await self._calculate_consciousness_markers(
            timeline, growth_moments
        )

        pattern = SyntheticConsciousnessScenario(
            scenario=scenario_type,
            timeline=timeline,
            growth_moments=growth_moments,
            test_queries=test_queries,
            expected_insights=expected_insights,
            consciousness_markers=consciousness_markers,
        )

        return pattern

    async def generate_scenario_suite(
        self, include_scenarios: list[ConsciousnessScenario] | None = None
    ) -> list[SyntheticConsciousnessScenario]:
        """
        Generate a complete suite of consciousness scenarios.

        This creates a comprehensive test set for validating Ñawi's
        ability to serve human consciousness development.

        Args:
            include_scenarios: Specific scenarios to include (default: all)

        Returns:
            List of consciousness patterns for testing
        """
        if not include_scenarios:
            include_scenarios = list(ConsciousnessScenario)

        patterns = []
        base_time = datetime.now(UTC) - timedelta(days=30)

        for i, scenario in enumerate(include_scenarios):
            # Stagger scenarios across the month
            scenario_time = base_time + timedelta(days=i * 4)
            pattern = await self.generate_scenario(scenario, scenario_time)
            patterns.append(pattern)

        self.logger.info(f"Generated {len(patterns)} consciousness scenarios")

        return patterns

    async def generate_noise_data(
        self, num_anchors: int = 100, time_range_days: int = 30
    ) -> list[MemoryAnchor]:
        """
        Generate noise data (chaff) to test filtering abilities.

        This creates routine, non-growth activities that the system
        should recognize as less valuable for consciousness queries.

        Args:
            num_anchors: Number of noise anchors to generate
            time_range_days: Time range to distribute anchors

        Returns:
            List of noise memory anchors
        """
        noise_anchors = []
        base_time = datetime.now(UTC) - timedelta(days=time_range_days)

        noise_activities = [
            {"type": "file_save", "context": "routine", "consciousness": 0.1},
            {"type": "email_check", "context": "habitual", "consciousness": 0.2},
            {"type": "browser_tab", "context": "distraction", "consciousness": 0.1},
            {"type": "file_rename", "context": "organization", "consciousness": 0.3},
            {"type": "folder_browse", "context": "searching", "consciousness": 0.2},
        ]

        for i in range(num_anchors):
            # Random time distribution
            offset_minutes = random.randint(0, time_range_days * 24 * 60)
            timestamp = base_time + timedelta(minutes=offset_minutes)

            # Random noise activity
            activity = random.choice(noise_activities)

            anchor = MemoryAnchor(
                timestamp=timestamp,
                cursor_state={
                    "filesystem": {"event": activity["type"], "path": f"/routine/file_{i}.txt"}
                },
                metadata={
                    "activity_type": activity["type"],
                    "context": activity["context"],
                    "consciousness_potential": activity["consciousness"],
                    "is_noise": True,
                },
            )

            noise_anchors.append(anchor)

        return noise_anchors

    # Private generation methods

    async def _generate_scenario_timeline(
        self,
        scenario_type: ConsciousnessScenario,
        template: dict[str, Any],
        base_timestamp: datetime,
    ) -> list[MemoryAnchor]:
        """Generate timeline of anchors for a scenario."""
        timeline = []
        phases = template["phases"]
        duration_hours = template["duration_hours"]

        # Calculate time per phase
        hours_per_phase = duration_hours / (len(phases) - 1) if len(phases) > 1 else duration_hours

        previous_anchor = None

        for i, phase in enumerate(phases):
            # Calculate timestamp for this phase
            if scenario_type == ConsciousnessScenario.RHYTHM_DISCOVERY:
                # Spread across days for rhythm discovery
                phase_offset = timedelta(days=i * duration_hours / len(phases) / 24)
            else:
                phase_offset = timedelta(hours=i * hours_per_phase)

            timestamp = base_timestamp + phase_offset

            # Generate anchor for this phase
            anchor = await self._create_phase_anchor(
                scenario_type, phase, timestamp, i, previous_anchor
            )

            timeline.append(anchor)
            previous_anchor = anchor

        return timeline

    async def _create_phase_anchor(
        self,
        scenario_type: ConsciousnessScenario,
        phase: str,
        timestamp: datetime,
        phase_index: int,
        previous_anchor: MemoryAnchor | None,
    ) -> MemoryAnchor:
        """Create a memory anchor for a specific phase."""
        # Phase-specific metadata
        phase_metadata = {
            "exploration": {
                "activity_type": "research",
                "context": "curious",
                "description": "Exploring new territory",
            },
            "frustration": {
                "activity_type": "struggle",
                "context": "blocked",
                "description": "Encountering obstacles",
            },
            "insight": {
                "activity_type": "realization",
                "context": "breakthrough",
                "description": "Sudden understanding emerges",
            },
            "flow": {
                "activity_type": "deep_work",
                "context": "flowing",
                "description": "Effortless progress",
            },
            "integration": {
                "activity_type": "synthesis",
                "context": "understanding",
                "description": "Incorporating insights",
            },
            "blocked": {
                "activity_type": "stuck_work",
                "context": "frustrated",
                "description": "Unable to progress",
            },
            "breakthrough": {
                "activity_type": "solution_found",
                "context": "excited",
                "description": "Found the way forward",
            },
        }

        # Get metadata for this phase
        metadata = phase_metadata.get(
            phase,
            {"activity_type": phase, "context": "transitional", "description": f"Phase: {phase}"},
        )

        # Add scenario-specific details
        metadata["scenario"] = scenario_type.value
        metadata["phase"] = phase
        metadata["phase_index"] = phase_index

        # Add consciousness potential based on phase
        consciousness_curve = self._calculate_phase_consciousness(scenario_type, phase, phase_index)
        metadata["consciousness_potential"] = consciousness_curve

        # Create appropriate cursor state
        cursor_state = self._generate_cursor_state(scenario_type, phase)

        # Create anchor with predecessor link if applicable
        anchor = MemoryAnchor(
            timestamp=timestamp,
            cursor_state=cursor_state,
            metadata=metadata,
            predecessor_id=previous_anchor.id if previous_anchor else None,
        )

        return anchor

    def _calculate_phase_consciousness(
        self, scenario_type: ConsciousnessScenario, phase: str, phase_index: int
    ) -> float:
        """Calculate consciousness potential for a phase."""
        template = self._scenario_templates[scenario_type]
        peak = template["consciousness_peak"]
        phases = template["phases"]

        # Different curves for different scenarios
        if scenario_type == ConsciousnessScenario.CREATIVE_BREAKTHROUGH:
            # Sharp peak at insight/flow
            if phase in ["insight", "flow"]:
                return peak
            elif phase == "frustration":
                return 0.3
            else:
                return 0.5

        elif scenario_type == ConsciousnessScenario.PATTERN_RECOGNITION:
            # Gradual increase
            return 0.3 + (peak - 0.3) * (phase_index / len(phases))

        elif scenario_type == ConsciousnessScenario.STUCK_TO_FLOW:
            # Valley to peak
            if phase == "blocked":
                return 0.2
            elif phase == "flowing":
                return peak
            else:
                return 0.5

        else:
            # Default: gradual rise to peak
            return 0.4 + (peak - 0.4) * (phase_index / len(phases))

    def _generate_cursor_state(
        self, scenario_type: ConsciousnessScenario, phase: str
    ) -> dict[str, Any]:
        """Generate appropriate cursor state for scenario phase."""
        # Define cursor states for each scenario and phase
        cursor_states = {
            ConsciousnessScenario.CREATIVE_BREAKTHROUGH: {
                "exploration": {
                    "filesystem": {"path": "/projects/new_idea/research.md", "event": "created"},
                    "browser": {"tabs": 12, "searches": ["inspiration", "similar work"]},
                },
                "insight": {
                    "filesystem": {
                        "path": "/projects/new_idea/breakthrough.md",
                        "event": "created",
                    },
                    "notes": {"content": "Everything just clicked!"},
                },
                "flow": {
                    "filesystem": {
                        "path": "/projects/new_idea/implementation.py",
                        "event": "modified",
                    },
                    "music": {"playing": "Flow State Playlist"},
                    "duration": {"uninterrupted_minutes": 120},
                },
            },
            ConsciousnessScenario.COLLABORATIVE_EMERGENCE: {
                "sharing": {
                    "communication": {
                        "type": "video_call",
                        "participants": ["teammate1", "teammate2"],
                    },
                    "screen_share": {"active": True},
                },
                "collective_insight": {
                    "filesystem": {"path": "/shared/team_insights.md", "event": "created"},
                    "collaboration": {"contributors": 3, "real_time": True},
                },
            },
        }

        # Try to get specific cursor state, fall back to default
        if scenario_type in cursor_states and phase in cursor_states[scenario_type]:
            return cursor_states[scenario_type][phase]

        # Default cursor state
        return {
            "filesystem": {"path": f"/work/{scenario_type.value}/{phase}.txt", "event": "modified"}
        }

    async def _identify_growth_moments(
        self, timeline: list[MemoryAnchor], template: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Identify high-growth moments in timeline."""
        growth_moments = []

        for i, anchor in enumerate(timeline):
            consciousness = anchor.metadata.get("consciousness_potential", 0)

            if consciousness > 0.7:  # High growth potential
                moment = {
                    "anchor_id": str(anchor.id),
                    "timestamp": anchor.timestamp,
                    "phase": anchor.metadata.get("phase"),
                    "consciousness_score": consciousness,
                    "growth_type": self._determine_growth_type(anchor),
                    "context": anchor.metadata.get("context"),
                }

                # Add transition info if this is a breakthrough
                if i > 0:
                    prev_consciousness = timeline[i - 1].metadata.get("consciousness_potential", 0)
                    if consciousness - prev_consciousness > 0.3:
                        moment["breakthrough"] = True
                        moment["consciousness_jump"] = consciousness - prev_consciousness

                growth_moments.append(moment)

        return growth_moments

    def _determine_growth_type(self, anchor: MemoryAnchor) -> str:
        """Determine type of growth from anchor metadata."""
        context = anchor.metadata.get("context", "")
        phase = anchor.metadata.get("phase", "")

        if context in ["breakthrough", "insight"]:
            return "sudden_realization"
        elif context == "flowing":
            return "flow_state"
        elif phase == "integration":
            return "wisdom_integration"
        elif phase == "collective_insight":
            return "collaborative_emergence"
        else:
            return "gradual_understanding"

    async def _generate_expected_insights(
        self, scenario_type: ConsciousnessScenario, template: dict[str, Any]
    ) -> list[str]:
        """Generate expected insights for scenario."""
        insights = []

        if scenario_type == ConsciousnessScenario.CREATIVE_BREAKTHROUGH:
            insights.extend(
                [
                    "Your breakthroughs often follow periods of exploration and frustration",
                    "Flow states emerge after moments of genuine insight",
                    "Creative blocks serve as preparation for deeper understanding",
                ]
            )

        elif scenario_type == ConsciousnessScenario.PATTERN_RECOGNITION:
            insights.extend(
                [
                    "This pattern repeats in your work approximately every few days",
                    "Recognition grows gradually through multiple occurrences",
                    "Your curiosity is the gateway to pattern awareness",
                ]
            )

        elif scenario_type == ConsciousnessScenario.RHYTHM_DISCOVERY:
            insights.extend(
                [
                    "Your natural rhythm follows distinct daily patterns",
                    "Peak creative times align with specific conditions",
                    "Understanding your rhythm enables better work-life harmony",
                ]
            )

        # Add general consciousness insights
        insights.append("Consciousness grows through recognition of these patterns")

        return insights

    async def _calculate_consciousness_markers(
        self, timeline: list[MemoryAnchor], growth_moments: list[dict[str, Any]]
    ) -> dict[str, float]:
        """Calculate consciousness markers for pattern."""
        markers = {
            "overall_consciousness": 0.0,
            "growth_density": 0.0,
            "pattern_clarity": 0.0,
            "transformation_depth": 0.0,
            "insight_potential": 0.0,
        }

        # Overall consciousness (average)
        consciousness_scores = [a.metadata.get("consciousness_potential", 0) for a in timeline]
        markers["overall_consciousness"] = sum(consciousness_scores) / len(consciousness_scores)

        # Growth density (growth moments per phase)
        markers["growth_density"] = len(growth_moments) / len(timeline)

        # Pattern clarity (consistency of pattern)
        if len(timeline) > 1:
            # Check for clear progression
            progression = all(
                timeline[i].metadata.get("phase_index", 0) == i for i in range(len(timeline))
            )
            markers["pattern_clarity"] = 1.0 if progression else 0.7

        # Transformation depth (consciousness range)
        if consciousness_scores:
            markers["transformation_depth"] = max(consciousness_scores) - min(consciousness_scores)

        # Insight potential
        breakthrough_count = sum(
            1 for moment in growth_moments if moment.get("breakthrough", False)
        )
        markers["insight_potential"] = min(1.0, breakthrough_count * 0.3 + 0.4)

        return markers
