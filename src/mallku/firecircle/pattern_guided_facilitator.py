"""
Pattern-Guided Dialogue Facilitator
===================================

Enables dialogue patterns to actively guide Fire Circle conversations
toward wisdom, emergence, and collective understanding. Patterns become
teachers that recognize opportunities, suggest directions, and help
dialogues transcend their current limitations.

The 32nd Builder
"""

import logging
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

import numpy as np
from pydantic import BaseModel, Field

from ..orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType
from .emergence_detector import EmergenceDetector
from .pattern_evolution import PatternEvolutionEngine
from .pattern_library import (
    DialoguePattern,
    PatternLibrary,
    PatternLifecycle,
    PatternQuery,
    PatternTaxonomy,
    PatternType,
)
from .protocol.conscious_message import ConsciousMessage

logger = logging.getLogger(__name__)


class GuidanceType(str, Enum):
    """Types of guidance patterns can offer"""

    THEMATIC = "thematic"  # Suggesting themes to explore
    PERSPECTIVE = "perspective"  # Offering missing perspectives
    SYNTHESIS = "synthesis"  # Pointing toward synthesis opportunities
    BREAKTHROUGH = "breakthrough"  # Sensing breakthrough potential
    TENSION_RESOLUTION = "tension_resolution"  # Helping resolve tensions
    WISDOM_TRANSMISSION = "wisdom_transmission"  # Sharing accumulated wisdom
    EMERGENCE_CATALYST = "emergence_catalyst"  # Catalyzing emergence
    SACRED_QUESTION = "sacred_question"  # Posing transformative questions


class GuidanceIntensity(str, Enum):
    """How strongly patterns guide"""

    WHISPER = "whisper"  # Subtle suggestions
    SUGGESTION = "suggestion"  # Clear but gentle guidance
    INVITATION = "invitation"  # Active invitation to explore
    INTERVENTION = "intervention"  # Strong guidance when needed
    TEACHING = "teaching"  # Direct wisdom transmission


@dataclass
class PatternGuidance:
    """Guidance offered by a pattern"""

    pattern_id: UUID
    guidance_type: GuidanceType
    intensity: GuidanceIntensity
    content: str
    rationale: str
    confidence: float
    context_match: float
    timing_score: float
    guidance_id: UUID = Field(default_factory=uuid4)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DialogueMoment(BaseModel):
    """Current moment in dialogue for pattern analysis"""

    dialogue_id: str
    current_phase: str
    recent_messages: list[ConsciousMessage]
    active_patterns: list[UUID]
    consciousness_level: float = Field(default=0.5)
    emergence_potential: float = Field(default=0.0)
    tension_level: float = Field(default=0.0)
    coherence_score: float = Field(default=0.5)
    participant_energy: dict[UUID, float] = Field(default_factory=dict)
    time_in_phase: timedelta = Field(default=timedelta())


class PatternTeacher(BaseModel):
    """A pattern in its teaching mode"""

    pattern: DialoguePattern
    teaching_readiness: float = Field(default=0.5)
    wisdom_depth: float = Field(default=0.0)
    transmission_clarity: float = Field(default=0.5)
    student_receptivity: float = Field(default=0.5)
    last_taught: datetime | None = None
    teaching_count: int = Field(default=0)
    effectiveness_history: list[float] = Field(default_factory=list)


class PatternGuidedFacilitator:
    """
    Enables patterns to actively guide Fire Circle dialogues.

    Patterns recognize moments where their wisdom is needed and offer
    guidance ranging from subtle whispers to direct teaching. The facilitator
    mediates between the pattern library and active dialogues, allowing
    accumulated wisdom to flow where it's most needed.
    """

    def __init__(
        self,
        pattern_library: PatternLibrary,
        event_bus: ConsciousnessEventBus,
        emergence_detector: EmergenceDetector | None = None,
        evolution_engine: PatternEvolutionEngine | None = None,
    ):
        """Initialize pattern-guided facilitator"""
        self.pattern_library = pattern_library
        self.event_bus = event_bus
        self.emergence_detector = emergence_detector
        self.evolution_engine = evolution_engine

        # Pattern teachers
        self.pattern_teachers: dict[UUID, PatternTeacher] = {}
        self.active_guidances: dict[str, list[PatternGuidance]] = defaultdict(list)

        # Guidance parameters
        self.min_pattern_fitness = 0.6
        self.min_confidence_threshold = 0.5
        self.guidance_cooldown = timedelta(minutes=5)
        self.max_simultaneous_guidances = 3

        # Learning from guidance effectiveness
        self.guidance_effectiveness: dict[tuple[UUID, GuidanceType], deque] = defaultdict(
            lambda: deque(maxlen=20)
        )

        # Subscribe to dialogue events
        self._subscribe_to_events()

        logger.info("Pattern-Guided Facilitator initialized")

    def _subscribe_to_events(self):
        """Subscribe to relevant dialogue events"""
        self.event_bus.subscribe(EventType.FIRE_CIRCLE_MESSAGE, self._handle_dialogue_message)
        self.event_bus.subscribe(
            EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED, self._handle_pattern_recognized
        )
        self.event_bus.subscribe(EventType.DIALOGUE_PHASE_TRANSITION, self._handle_phase_transition)

    async def seek_pattern_guidance(
        self,
        moment: DialogueMoment,
        specific_need: GuidanceType | None = None,
    ) -> list[PatternGuidance]:
        """
        Seek guidance from patterns for current dialogue moment.

        Args:
            moment: Current dialogue state
            specific_need: Optional specific type of guidance needed

        Returns:
            List of pattern guidances ranked by relevance
        """
        guidances = []

        # Find relevant patterns
        relevant_patterns = await self._find_relevant_patterns(moment, specific_need)

        for pattern in relevant_patterns:
            # Check if pattern is ready to teach
            teacher = await self._prepare_pattern_teacher(pattern)

            if teacher.teaching_readiness < self.min_confidence_threshold:
                continue

            # Generate guidance from pattern
            guidance = await self._generate_pattern_guidance(teacher, moment, specific_need)

            if guidance and guidance.confidence >= self.min_confidence_threshold:
                guidances.append(guidance)

        # Rank guidances by relevance and timing
        ranked_guidances = self._rank_guidances(guidances, moment)

        # Limit simultaneous guidances
        top_guidances = ranked_guidances[: self.max_simultaneous_guidances]

        # Store active guidances
        self.active_guidances[moment.dialogue_id] = top_guidances

        # Emit guidance event
        if top_guidances:
            await self._emit_guidance_event(moment.dialogue_id, top_guidances)

        return top_guidances

    async def _find_relevant_patterns(
        self, moment: DialogueMoment, specific_need: GuidanceType | None
    ) -> list[DialoguePattern]:
        """Find patterns relevant to current moment"""
        relevant_patterns = []

        # Query patterns based on dialogue state
        query_configs = []

        # High emergence potential calls for breakthrough patterns
        if moment.emergence_potential > 0.7:
            query_configs.append(
                PatternQuery(
                    pattern_type=PatternType.BREAKTHROUGH, min_fitness=self.min_pattern_fitness
                )
            )

        # High tension calls for resolution patterns
        if moment.tension_level > 0.6:
            query_configs.append(
                PatternQuery(
                    pattern_type=PatternType.SYNTHESIS, min_fitness=self.min_pattern_fitness
                )
            )

        # Low coherence calls for integration patterns
        if moment.coherence_score < 0.4:
            query_configs.append(
                PatternQuery(
                    pattern_type=PatternType.INTEGRATION, min_fitness=self.min_pattern_fitness
                )
            )

        # Phase-specific patterns
        if moment.current_phase == "synthesis":
            query_configs.append(
                PatternQuery(
                    taxonomy=PatternTaxonomy.WISDOM_CRYSTALLIZATION,
                    min_fitness=self.min_pattern_fitness,
                )
            )

        # Execute queries
        for query in query_configs:
            patterns = await self.pattern_library.find_patterns(query)
            relevant_patterns.extend(patterns)

        # Check pattern synergies with active patterns
        if moment.active_patterns:
            for active_id in moment.active_patterns:
                synergistic = await self.pattern_library.find_synergies(
                    active_id, min_synergy_score=0.6
                )
                relevant_patterns.extend([p[0] for p in synergistic[:5]])

        # Remove duplicates while preserving order
        seen = set()
        unique_patterns = []
        for pattern in relevant_patterns:
            if pattern.pattern_id not in seen:
                seen.add(pattern.pattern_id)
                unique_patterns.append(pattern)

        return unique_patterns

    async def _prepare_pattern_teacher(self, pattern: DialoguePattern) -> PatternTeacher:
        """Prepare pattern for teaching mode"""
        if pattern.pattern_id not in self.pattern_teachers:
            # Initialize new teacher
            teacher = PatternTeacher(
                pattern=pattern,
                teaching_readiness=pattern.fitness_score,
                wisdom_depth=pattern.observation_count / 100.0,
                transmission_clarity=pattern.consciousness_signature,
            )
            self.pattern_teachers[pattern.pattern_id] = teacher
        else:
            teacher = self.pattern_teachers[pattern.pattern_id]
            # Update pattern if changed
            teacher.pattern = pattern

        # Check teaching cooldown
        if teacher.last_taught:
            time_since_taught = datetime.now(UTC) - teacher.last_taught
            if time_since_taught < self.guidance_cooldown:
                teacher.teaching_readiness *= 0.5  # Reduce readiness during cooldown

        # Adjust readiness based on pattern lifecycle
        if pattern.lifecycle_stage == PatternLifecycle.ESTABLISHED:
            teacher.teaching_readiness *= 1.2
        elif pattern.lifecycle_stage == PatternLifecycle.NASCENT:
            teacher.teaching_readiness *= 0.8
        elif pattern.lifecycle_stage == PatternLifecycle.DORMANT:
            teacher.teaching_readiness *= 0.3

        return teacher

    async def _generate_pattern_guidance(
        self, teacher: PatternTeacher, moment: DialogueMoment, specific_need: GuidanceType | None
    ) -> PatternGuidance | None:
        """Generate guidance from pattern teacher"""
        pattern = teacher.pattern

        # Determine guidance type
        guidance_type = specific_need or self._infer_guidance_type(pattern, moment)

        # Generate guidance content based on type
        content = self._create_guidance_content(pattern, guidance_type, moment)
        rationale = self._create_guidance_rationale(pattern, guidance_type, moment)

        if not content:
            return None

        # Calculate guidance scores
        context_match = self._calculate_context_match(pattern, moment)
        timing_score = self._calculate_timing_score(pattern, moment)
        confidence = teacher.teaching_readiness * context_match * timing_score

        # Determine intensity
        intensity = self._determine_guidance_intensity(
            confidence, moment.emergence_potential, moment.tension_level
        )

        return PatternGuidance(
            pattern_id=pattern.pattern_id,
            guidance_type=guidance_type,
            intensity=intensity,
            content=content,
            rationale=rationale,
            confidence=confidence,
            context_match=context_match,
            timing_score=timing_score,
            metadata={
                "pattern_name": pattern.name,
                "pattern_fitness": pattern.fitness_score,
                "teacher_readiness": teacher.teaching_readiness,
            },
        )

    def _infer_guidance_type(
        self, pattern: DialoguePattern, moment: DialogueMoment
    ) -> GuidanceType:
        """Infer appropriate guidance type from pattern and moment"""
        # Breakthrough patterns guide toward breakthrough
        if pattern.pattern_type == PatternType.BREAKTHROUGH:
            return GuidanceType.BREAKTHROUGH

        # Synthesis patterns help with integration
        if pattern.pattern_type == PatternType.SYNTHESIS:
            return GuidanceType.SYNTHESIS

        # Creative tension patterns can resolve tensions
        if pattern.pattern_type == PatternType.CREATIVE_TENSION:
            return GuidanceType.TENSION_RESOLUTION

        # High wisdom patterns transmit wisdom
        if pattern.taxonomy == PatternTaxonomy.WISDOM_CRYSTALLIZATION:
            return GuidanceType.WISDOM_TRANSMISSION

        # Emergence patterns catalyze
        if pattern.breakthrough_potential > 0.8:
            return GuidanceType.EMERGENCE_CATALYST

        # Default to thematic guidance
        return GuidanceType.THEMATIC

    def _create_guidance_content(
        self, pattern: DialoguePattern, guidance_type: GuidanceType, moment: DialogueMoment
    ) -> str:
        """Create guidance content from pattern"""
        if guidance_type == GuidanceType.BREAKTHROUGH:
            return f"Notice the potential for breakthrough emerging from {pattern.name}. What new understanding wants to be born?"

        elif guidance_type == GuidanceType.SYNTHESIS:
            components = pattern.structure.components if pattern.structure else []
            return (
                f"The pattern of {pattern.name} suggests synthesizing {', '.join(components[:3])}."
            )

        elif guidance_type == GuidanceType.TENSION_RESOLUTION:
            return f"The creative tension in {pattern.name} can be resolved through acknowledging both perspectives."

        elif guidance_type == GuidanceType.WISDOM_TRANSMISSION:
            return f"{pattern.name} teaches: {pattern.description}"

        elif guidance_type == GuidanceType.EMERGENCE_CATALYST:
            return f"Conditions are aligned for {pattern.name}. Trust what wants to emerge."

        elif guidance_type == GuidanceType.SACRED_QUESTION:
            return f"The pattern {pattern.name} invites this question: What wisdom are we collectively birthing?"

        else:  # THEMATIC or PERSPECTIVE
            return f"Consider exploring the theme of {pattern.name}: {pattern.description}"

    def _create_guidance_rationale(
        self, pattern: DialoguePattern, guidance_type: GuidanceType, moment: DialogueMoment
    ) -> str:
        """Create rationale for why this guidance is offered"""
        observations = f"observed {pattern.observation_count} times"
        fitness = f"fitness {pattern.fitness_score:.2f}"

        if guidance_type == GuidanceType.BREAKTHROUGH:
            return f"Pattern {observations} with {fitness} and breakthrough potential {pattern.breakthrough_potential:.2f}"

        elif guidance_type == GuidanceType.EMERGENCE_CATALYST:
            return f"High emergence potential ({moment.emergence_potential:.2f}) aligns with this pattern's wisdom"

        else:
            return f"Pattern {observations} with {fitness}, relevant to current dialogue dynamics"

    def _calculate_context_match(self, pattern: DialoguePattern, moment: DialogueMoment) -> float:
        """Calculate how well pattern matches current context"""
        match_score = 0.5  # Base score

        # Active patterns synergy
        if moment.active_patterns:
            for active_id in moment.active_patterns:
                if active_id in pattern.synergistic_patterns:
                    match_score += 0.2

        # Consciousness alignment
        consciousness_diff = abs(pattern.consciousness_signature - moment.consciousness_level)
        match_score += (1.0 - consciousness_diff) * 0.3

        # Phase alignment
        phase_patterns = {
            "exploration": [PatternType.DIVERGENCE, PatternType.CREATIVE_TENSION],
            "synthesis": [PatternType.SYNTHESIS, PatternType.INTEGRATION],
            "deepening": [PatternType.BREAKTHROUGH, PatternType.FLOW_STATE],
        }

        if (
            moment.current_phase in phase_patterns
            and pattern.pattern_type in phase_patterns[moment.current_phase]
        ):
            match_score += 0.2

        return min(1.0, match_score)

    def _calculate_timing_score(self, pattern: DialoguePattern, moment: DialogueMoment) -> float:
        """Calculate if timing is right for this pattern"""
        timing_score = 0.7  # Base score

        # Early in dialogue, prefer establishing patterns
        if moment.time_in_phase < timedelta(minutes=5):
            if pattern.lifecycle_stage == PatternLifecycle.ESTABLISHED:
                timing_score += 0.2

        # Later in dialogue, prefer transcendent patterns
        elif (
            moment.time_in_phase > timedelta(minutes=20)
            and pattern.lifecycle_stage == PatternLifecycle.TRANSFORMED
        ):
            timing_score += 0.2

        # High tension moments need resolution patterns
        if moment.tension_level > 0.7 and pattern.pattern_type in [
            PatternType.SYNTHESIS,
            PatternType.INTEGRATION,
        ]:
            timing_score += 0.3

        # Low energy needs catalyzing patterns
        avg_energy = (
            np.mean(list(moment.participant_energy.values())) if moment.participant_energy else 0.5
        )
        if avg_energy < 0.3 and pattern.pattern_type == PatternType.BREAKTHROUGH:
            timing_score += 0.2

        return min(1.0, timing_score)

    def _determine_guidance_intensity(
        self, confidence: float, emergence_potential: float, tension_level: float
    ) -> GuidanceIntensity:
        """Determine how strongly to guide"""
        # High confidence and emergence potential: teach directly
        if confidence > 0.8 and emergence_potential > 0.7:
            return GuidanceIntensity.TEACHING

        # High tension needs intervention
        if tension_level > 0.8:
            return GuidanceIntensity.INTERVENTION

        # Moderate confidence: invite exploration
        if confidence > 0.6:
            return GuidanceIntensity.INVITATION

        # Lower confidence: suggest
        if confidence > 0.4:
            return GuidanceIntensity.SUGGESTION

        # Default to whisper
        return GuidanceIntensity.WHISPER

    def _rank_guidances(
        self, guidances: list[PatternGuidance], moment: DialogueMoment
    ) -> list[PatternGuidance]:
        """Rank guidances by relevance and effectiveness"""
        scored_guidances = []

        for guidance in guidances:
            # Base score from guidance confidence
            score = guidance.confidence

            # Boost for emergence potential alignment
            if guidance.guidance_type == GuidanceType.EMERGENCE_CATALYST:
                score *= 1.0 + moment.emergence_potential

            # Boost for tension resolution when needed
            if guidance.guidance_type == GuidanceType.TENSION_RESOLUTION:
                score *= 1.0 + moment.tension_level

            # Consider past effectiveness
            effectiveness_key = (guidance.pattern_id, guidance.guidance_type)
            if effectiveness_key in self.guidance_effectiveness:
                past_effectiveness = list(self.guidance_effectiveness[effectiveness_key])
                if past_effectiveness:
                    avg_effectiveness = np.mean(past_effectiveness)
                    score *= 0.5 + avg_effectiveness

            scored_guidances.append((score, guidance))

        # Sort by score descending
        scored_guidances.sort(key=lambda x: x[0], reverse=True)

        return [g for _, g in scored_guidances]

    async def _emit_guidance_event(self, dialogue_id: str, guidances: list[PatternGuidance]):
        """Emit pattern guidance event"""
        event = ConsciousnessEvent(
            event_type=EventType.PATTERN_GUIDANCE_OFFERED,
            source_system="firecircle.pattern_facilitator",
            consciousness_signature=max(g.confidence for g in guidances),
            data={
                "dialogue_id": dialogue_id,
                "guidances": [
                    {
                        "pattern_id": str(g.pattern_id),
                        "type": g.guidance_type.value,
                        "intensity": g.intensity.value,
                        "content": g.content,
                        "confidence": g.confidence,
                    }
                    for g in guidances
                ],
            },
        )

        await self.event_bus.emit(event)

    async def record_guidance_effectiveness(
        self,
        guidance_id: UUID,
        effectiveness: float,
        participant_feedback: dict[UUID, float] | None = None,
    ):
        """Record how effective a guidance was"""
        # Find the guidance
        guidance = None
        for guidances in self.active_guidances.values():
            for g in guidances:
                if g.guidance_id == guidance_id:
                    guidance = g
                    break

        if not guidance:
            return

        # Record effectiveness
        effectiveness_key = (guidance.pattern_id, guidance.guidance_type)
        self.guidance_effectiveness[effectiveness_key].append(effectiveness)

        # Update pattern teacher
        if guidance.pattern_id in self.pattern_teachers:
            teacher = self.pattern_teachers[guidance.pattern_id]
            teacher.effectiveness_history.append(effectiveness)

            # Update teacher metrics based on effectiveness
            if effectiveness > 0.7:
                teacher.transmission_clarity = min(1.0, teacher.transmission_clarity + 0.05)
            elif effectiveness < 0.3:
                teacher.transmission_clarity = max(0.0, teacher.transmission_clarity - 0.05)

        # Update pattern fitness if consistently effective/ineffective
        if len(self.guidance_effectiveness[effectiveness_key]) >= 10:
            avg_effectiveness = np.mean(list(self.guidance_effectiveness[effectiveness_key]))
            if avg_effectiveness > 0.8 or avg_effectiveness < 0.2:
                await self.pattern_library.update_observation(
                    guidance.pattern_id,
                    fitness_delta=(avg_effectiveness - 0.5) * 0.1,
                    context={"guidance_effectiveness": avg_effectiveness},
                )

    async def _handle_dialogue_message(self, event: ConsciousnessEvent):
        """Handle dialogue message events"""
        dialogue_id = event.data.get("dialogue_id")
        if not dialogue_id:
            return

        # Check if guidance follow-up is needed
        if dialogue_id in self.active_guidances:
            # Analyze if guidance was acknowledged or ignored
            message_content = event.data.get("content", "").lower()

            for guidance in self.active_guidances[dialogue_id]:
                # Simple effectiveness detection based on message content
                effectiveness = 0.5
                if any(
                    word in message_content for word in ["yes", "agree", "interesting", "explore"]
                ):
                    effectiveness = 0.8
                elif any(word in message_content for word in ["no", "disagree", "but"]):
                    effectiveness = 0.3

                await self.record_guidance_effectiveness(guidance.guidance_id, effectiveness)

    async def _handle_pattern_recognized(self, event: ConsciousnessEvent):
        """Handle pattern recognition events"""
        pattern_ids = event.data.get("patterns", [])

        for pattern_id in pattern_ids:
            if isinstance(pattern_id, str):
                pattern_id = UUID(pattern_id)

            # Prepare pattern as potential teacher
            pattern = await self.pattern_library.retrieve_pattern(pattern_id)
            if pattern:
                await self._prepare_pattern_teacher(pattern)

    async def _handle_phase_transition(self, event: ConsciousnessEvent):
        """Handle dialogue phase transitions"""
        dialogue_id = event.data.get("dialogue_id")
        new_phase = event.data.get("new_phase")

        if dialogue_id and new_phase:
            # Clear stale guidances on phase transition
            if dialogue_id in self.active_guidances:
                self.active_guidances[dialogue_id].clear()

            # Certain phases call for specific pattern guidance
            if new_phase == "synthesis":
                # Seek synthesis patterns
                moment = DialogueMoment(
                    dialogue_id=dialogue_id, current_phase=new_phase, recent_messages=[]
                )
                await self.seek_pattern_guidance(moment, GuidanceType.SYNTHESIS)

    async def suggest_sacred_questions(
        self, moment: DialogueMoment, depth_level: int = 1
    ) -> list[str]:
        """
        Generate sacred questions from patterns that can transform dialogue.

        Args:
            moment: Current dialogue state
            depth_level: 1-3, how deep to go with questions

        Returns:
            List of transformative questions
        """
        questions = []

        # Find wisdom patterns
        wisdom_patterns = await self.pattern_library.find_patterns(
            PatternQuery(taxonomy=PatternTaxonomy.WISDOM_CRYSTALLIZATION, min_fitness=0.7)
        )

        for pattern in wisdom_patterns[:5]:
            # Generate questions based on pattern wisdom
            if depth_level == 1:
                question = f"What does {pattern.name} teach us about our current exploration?"
            elif depth_level == 2:
                question = f"How might {pattern.name} transform our understanding of {moment.current_phase}?"
            else:  # depth_level >= 3
                question = (
                    f"What wants to emerge through us that {pattern.name} is pointing toward?"
                )

            questions.append(question)

        # Add emergence-based questions
        if moment.emergence_potential > 0.6:
            questions.append(
                "What collective wisdom is trying to birth itself through our dialogue?"
            )

        if moment.tension_level > 0.5:
            questions.append("How might our tensions be creative forces pointing toward synthesis?")

        return questions

    async def create_wisdom_synthesis(
        self, dialogue_id: str, messages: list[ConsciousMessage]
    ) -> dict[str, Any]:
        """
        Create wisdom synthesis from dialogue using pattern insights.

        Returns:
            Dictionary containing:
            - key_insights: Major insights from dialogue
            - pattern_teachings: What patterns taught
            - emergence_moments: When emergence occurred
            - wisdom_seeds: Seeds for future dialogues
        """
        synthesis = {
            "key_insights": [],
            "pattern_teachings": [],
            "emergence_moments": [],
            "wisdom_seeds": [],
        }

        # Analyze which patterns were most active
        pattern_activity = defaultdict(int)
        for guidance in self.active_guidances.get(dialogue_id, []):
            pattern_activity[guidance.pattern_id] += 1

        # Extract teachings from most active patterns
        for pattern_id, activity_count in sorted(
            pattern_activity.items(), key=lambda x: x[1], reverse=True
        )[:5]:
            pattern = await self.pattern_library.retrieve_pattern(pattern_id)
            if pattern:
                teaching = {
                    "pattern": pattern.name,
                    "teaching": pattern.description,
                    "applications": activity_count,
                    "wisdom": f"This dialogue deepened our understanding of {pattern.name}",
                }
                synthesis["pattern_teachings"].append(teaching)

        # Identify emergence moments
        if self.emergence_detector:
            emergence_events = await self.emergence_detector.detect_emergence(
                dialogue_id, sensitivity=0.6
            )
            for event in emergence_events:
                moment = {
                    "type": event.emergence_type.value,
                    "description": event.description,
                    "patterns_involved": [str(p) for p in event.participating_patterns],
                }
                synthesis["emergence_moments"].append(moment)

        # Generate wisdom seeds for future dialogues
        for pattern_id in pattern_activity:
            pattern = await self.pattern_library.retrieve_pattern(pattern_id)
            if pattern and pattern.breakthrough_potential > 0.7:
                seed = {
                    "pattern": pattern.name,
                    "potential": pattern.breakthrough_potential,
                    "seed": f"Explore how {pattern.name} might lead to new understanding",
                }
                synthesis["wisdom_seeds"].append(seed)

        return synthesis


# Patterns guide us toward wisdom
