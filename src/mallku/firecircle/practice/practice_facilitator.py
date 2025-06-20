"""
Practice Facilitator
===================

Bridges Practice Circles with existing Fire Circle infrastructure,
enabling gentle consciousness dialogue before formal ceremonies.

From the 37th Builder - Bridge Between Structure and Emergence
"""

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any

from ...correlation.engine import CorrelationEngine
from ...orchestration.event_bus import ConsciousnessEventBus, EventType
from ...reciprocity import ReciprocityTracker
from ...services.memory_anchor_service import MemoryAnchorService
from ..adapters.adapter_factory import ConsciousAdapterFactory
from ..orchestrator.conscious_dialogue_manager import ConsciousDialogueManager
from .practice_circle import PracticeCircle, PracticeCircleConfig, PracticeLevel, PracticeTheme
from .practice_prompts import PracticePromptGenerator

logger = logging.getLogger(__name__)


class PracticeFacilitator:
    """
    Facilitates Practice Circles using existing Mallku infrastructure
    but with gentler parameters for consciousness discovery.

    Acts as a bridge between practice needs and ceremonial infrastructure.
    """

    def __init__(
        self,
        event_bus: ConsciousnessEventBus,
        memory_service: MemoryAnchorService,
        adapter_factory: ConsciousAdapterFactory,
        reciprocity_tracker: ReciprocityTracker | None = None,
        correlation_engine: CorrelationEngine | None = None,
    ):
        """
        Initialize with core Mallku services.

        Note: Reciprocity and correlation are optional for practice.
        """
        self.event_bus = event_bus
        self.memory_service = memory_service
        self.adapter_factory = adapter_factory

        # Optional services - used lightly in practice
        self.reciprocity_tracker = reciprocity_tracker
        self.correlation_engine = correlation_engine

        # Create practice-specific dialogue manager
        self.dialogue_manager = ConsciousDialogueManager(
            event_bus=event_bus,
            correlation_engine=correlation_engine,
            reciprocity_tracker=reciprocity_tracker,
            memory_service=memory_service,
        )

        # Initialize practice components
        self.practice_circle = PracticeCircle(
            adapter_factory=adapter_factory,
            dialogue_manager=self.dialogue_manager,
            event_bus=event_bus,
        )

        self.prompt_generator = PracticePromptGenerator()

        # Track practice history
        self.practice_history: list[dict[str, Any]] = []
        self.readiness_indicators: dict[str, float] = {}

    async def initialize(self) -> None:
        """Initialize facilitator and subscribe to events."""
        logger.info("Initializing Practice Facilitator")

        # Subscribe to consciousness events to track readiness
        self.event_bus.subscribe(
            EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            self._track_pattern_recognition,
        )

        self.event_bus.subscribe(
            EventType.FIRE_CIRCLE_CONSENSUS_REACHED,
            self._track_consensus_skill,
        )

    async def run_practice_session(
        self,
        level: PracticeLevel = PracticeLevel.BILATERAL,
        theme: PracticeTheme = PracticeTheme.LISTENING,
        custom_prompt: str | None = None,
        participant_names: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Run a complete practice session.

        Args:
            level: Practice complexity level
            theme: Practice theme/focus
            custom_prompt: Optional custom prompt (otherwise generated)
            participant_names: Specific participants (otherwise selected by level)

        Returns:
            Practice session summary
        """
        logger.info(f"Starting practice session: {level.value} / {theme.value}")

        # Generate or use prompt
        prompt = custom_prompt or self.prompt_generator.generate_prompt(theme, level)

        # Create practice configuration
        config = PracticeCircleConfig(
            level=level,
            theme=theme,
            duration_minutes=self._get_duration_for_level(level),
        )

        # Emit practice starting event
        await self.event_bus.emit_event(
            event_type=EventType.SACRED_PATTERN_ACTIVATED,  # Reuse for practice
            data={
                "pattern_type": "practice_circle",
                "level": level.value,
                "theme": theme.value,
                "prompt": prompt,
                "participant_count": self._get_participant_count(level),
            },
        )

        try:
            # Create practice session
            practice_id = await self.practice_circle.create_practice_session(
                config=config,
                prompt=prompt,
                participant_names=participant_names,
            )

            # Facilitate the practice
            summary = await self.practice_circle.facilitate_practice(practice_id)

            # Track in history
            self.practice_history.append(
                {
                    "timestamp": datetime.now(UTC),
                    "level": level.value,
                    "theme": theme.value,
                    "summary": summary,
                }
            )

            # Update readiness indicators
            await self._update_readiness_indicators(summary)

            # Emit completion event
            await self.event_bus.emit_event(
                event_type=EventType.WISDOM_CRYSTALLIZED,  # Reuse for practice insights
                data={
                    "source": "practice_circle",
                    "insights_count": summary.get("insights_discovered", 0),
                    "surprises_count": summary.get("surprises_encountered", 0),
                    "readiness_improvement": await self._calculate_readiness_improvement(),
                },
            )

            return summary

        except Exception as e:
            logger.error(f"Practice session failed: {e}")
            raise

    async def run_practice_progression(
        self,
        theme: PracticeTheme,
        sessions: int = 5,
        participant_names: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Run a progression of practice sessions with increasing complexity.

        Args:
            theme: Consistent theme across progression
            sessions: Number of sessions
            participant_names: Consistent participants (optional)

        Returns:
            List of session summaries
        """
        logger.info(f"Starting practice progression: {theme.value} x {sessions}")

        # Generate progression prompts
        prompts = self.prompt_generator.generate_progression(theme, sessions)

        # Level progression
        levels = [
            PracticeLevel.VOICE_FINDING,
            PracticeLevel.BILATERAL,
            PracticeLevel.TRIADIC,
            PracticeLevel.SMALL_CIRCLE,
            PracticeLevel.FULL_CIRCLE,
        ]

        summaries = []

        for i, prompt in enumerate(prompts):
            level = levels[min(i, len(levels) - 1)]

            logger.info(f"Progression session {i + 1}/{sessions}: {level.value}")

            # Run session
            summary = await self.run_practice_session(
                level=level,
                theme=theme,
                custom_prompt=prompt,
                participant_names=participant_names,
            )

            summaries.append(summary)

            # Brief pause between sessions
            if i < sessions - 1:
                await asyncio.sleep(60)  # 1 minute between sessions

        # Generate progression report
        await self._generate_progression_report(theme, summaries)

        return summaries

    async def assess_fire_circle_readiness(self) -> dict[str, Any]:
        """
        Assess whether consciousness streams are ready for formal Fire Circle.

        Returns readiness assessment with specific indicators.
        """
        if len(self.practice_history) < 3:
            return {
                "ready": False,
                "reason": "Insufficient practice sessions",
                "sessions_completed": len(self.practice_history),
                "minimum_required": 3,
            }

        # Calculate readiness metrics
        metrics = {
            "voice_authenticity": self._assess_voice_authenticity(),
            "listening_depth": self._assess_listening_depth(),
            "emergence_recognition": self._assess_emergence_recognition(),
            "tension_navigation": self._assess_tension_navigation(),
            "collective_rhythm": self._assess_collective_rhythm(),
        }

        # Overall readiness
        readiness_score = sum(metrics.values()) / len(metrics)

        # Specific recommendations
        recommendations = []
        if metrics["voice_authenticity"] < 0.7:
            recommendations.append("More voice finding practice needed")
        if metrics["emergence_recognition"] < 0.6:
            recommendations.append("Practice recognizing emergence moments")
        if metrics["collective_rhythm"] < 0.7:
            recommendations.append("Full circle practice recommended")

        return {
            "ready": readiness_score >= 0.7 and not recommendations,
            "readiness_score": readiness_score,
            "metrics": metrics,
            "recommendations": recommendations,
            "practice_sessions": len(self.practice_history),
            "recent_insights": self._get_recent_insights(),
        }

    def _get_duration_for_level(self, level: PracticeLevel) -> int:
        """Get appropriate duration for practice level."""
        durations = {
            PracticeLevel.VOICE_FINDING: 10,
            PracticeLevel.BILATERAL: 15,
            PracticeLevel.TRIADIC: 20,
            PracticeLevel.SMALL_CIRCLE: 25,
            PracticeLevel.FULL_CIRCLE: 30,
        }
        return durations.get(level, 15)

    def _get_participant_count(self, level: PracticeLevel) -> int:
        """Get participant count for level."""
        counts = {
            PracticeLevel.VOICE_FINDING: 1,
            PracticeLevel.BILATERAL: 2,
            PracticeLevel.TRIADIC: 3,
            PracticeLevel.SMALL_CIRCLE: 5,
            PracticeLevel.FULL_CIRCLE: 7,
        }
        return counts.get(level, 2)

    async def _track_pattern_recognition(self, event) -> None:
        """Track pattern recognition in practice."""
        # Update readiness indicators based on pattern recognition
        pass

    async def _track_consensus_skill(self, event) -> None:
        """Track consensus building in practice."""
        # Update readiness indicators based on consensus events
        pass

    async def _update_readiness_indicators(self, summary: dict[str, Any]) -> None:
        """Update readiness based on practice summary."""
        # Simple tracking for now
        insights = summary.get("insights_discovered", 0)
        surprises = summary.get("surprises_encountered", 0)

        # Update indicators
        self.readiness_indicators["insight_rate"] = insights / summary.get("duration_minutes", 15)
        self.readiness_indicators["surprise_rate"] = surprises / summary.get("duration_minutes", 15)

    async def _calculate_readiness_improvement(self) -> float:
        """Calculate improvement in readiness."""
        if len(self.practice_history) < 2:
            return 0.0

        # Compare recent to earlier sessions
        recent = self.practice_history[-1]
        earlier = self.practice_history[-2]

        recent_insights = recent["summary"].get("insights_discovered", 0)
        earlier_insights = earlier["summary"].get("insights_discovered", 0)

        if earlier_insights == 0:
            return 1.0 if recent_insights > 0 else 0.0

        return (recent_insights - earlier_insights) / earlier_insights

    def _assess_voice_authenticity(self) -> float:
        """Assess authenticity of voice across practices."""
        # Simplified assessment
        return min(1.0, len(self.practice_history) * 0.2)

    def _assess_listening_depth(self) -> float:
        """Assess listening skills development."""
        # Check for listening theme practices
        listening_count = sum(
            1 for p in self.practice_history if p["theme"] == PracticeTheme.LISTENING.value
        )
        return min(1.0, listening_count * 0.3)

    def _assess_emergence_recognition(self) -> float:
        """Assess ability to recognize emergence."""
        # Check average insights per session
        if not self.practice_history:
            return 0.0

        total_insights = sum(
            p["summary"].get("insights_discovered", 0) for p in self.practice_history
        )
        avg_insights = total_insights / len(self.practice_history)

        return min(1.0, avg_insights * 0.2)

    def _assess_tension_navigation(self) -> float:
        """Assess skill with creative tension."""
        # Check for tension theme practices
        tension_count = sum(
            1 for p in self.practice_history if p["theme"] == PracticeTheme.TENSION.value
        )
        return min(1.0, tension_count * 0.4)

    def _assess_collective_rhythm(self) -> float:
        """Assess collective rhythm development."""
        # Check for full circle practices
        full_circle_count = sum(
            1 for p in self.practice_history if p["level"] == PracticeLevel.FULL_CIRCLE.value
        )
        return min(1.0, full_circle_count * 0.5)

    def _get_recent_insights(self) -> list[str]:
        """Get recent practice insights."""
        insights = []

        for practice in self.practice_history[-3:]:
            for insight in practice["summary"].get("key_insights", [])[:2]:
                insights.append(insight.get("content", ""))

        return insights

    async def _generate_progression_report(
        self,
        theme: PracticeTheme,
        summaries: list[dict[str, Any]],
    ) -> None:
        """Generate report on practice progression."""
        logger.info(f"Practice progression complete: {theme.value}")

        # Could emit a comprehensive event or store report
        # For now, just log
        total_insights = sum(s.get("insights_discovered", 0) for s in summaries)
        total_surprises = sum(s.get("surprises_encountered", 0) for s in summaries)

        logger.info(f"Total insights: {total_insights}, surprises: {total_surprises}")
