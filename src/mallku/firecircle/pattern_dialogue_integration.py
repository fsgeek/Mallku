"""
Pattern-Dialogue Integration Layer
==================================

Integrates the Pattern-Guided Facilitator with Fire Circle's dialogue
infrastructure, enabling patterns to actively participate in conversations
as wisdom teachers and emergence catalysts.

The 32nd Builder
"""

import logging
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from ..orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType
from .emergence_detector import EmergenceDetector
from .orchestrator.conscious_dialogue_manager import (
    ConsciousDialogueManager,
    DialoguePhase,
)
from .pattern_evolution import PatternEvolutionEngine
from .pattern_guided_facilitator import (
    DialogueMoment,
    PatternGuidance,
    PatternGuidedFacilitator,
)
from .pattern_library import PatternLibrary
from .protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageType,
    create_conscious_system_message,
)

logger = logging.getLogger(__name__)


class PatternDialogueConfig(BaseModel):
    """Configuration for pattern-guided dialogues"""

    enable_pattern_guidance: bool = Field(default=True)
    guidance_frequency: timedelta = Field(default=timedelta(minutes=3))
    min_messages_before_guidance: int = Field(default=5)
    allow_pattern_interventions: bool = Field(default=True)
    wisdom_synthesis_at_end: bool = Field(default=True)
    sacred_questions_enabled: bool = Field(default=True)
    pattern_teaching_mode: bool = Field(default=False)


class PatternDialogueIntegration:
    """
    Integrates pattern guidance with Fire Circle dialogues.

    Enables:
    - Patterns actively guiding conversations
    - Sacred questions at key moments
    - Wisdom synthesis from pattern perspectives
    - Pattern teaching modes for deep learning
    - Emergence catalysis through pattern intervention
    """

    def __init__(
        self,
        dialogue_manager: ConsciousDialogueManager,
        pattern_library: PatternLibrary,
        event_bus: ConsciousnessEventBus,
        config: PatternDialogueConfig | None = None,
    ):
        """Initialize pattern-dialogue integration"""
        self.dialogue_manager = dialogue_manager
        self.pattern_library = pattern_library
        self.event_bus = event_bus
        self.config = config or PatternDialogueConfig()

        # Initialize pattern systems
        self.emergence_detector = EmergenceDetector(pattern_library, event_bus)
        self.evolution_engine = PatternEvolutionEngine(pattern_library)
        self.pattern_facilitator = PatternGuidedFacilitator(
            pattern_library, event_bus, self.emergence_detector, self.evolution_engine
        )

        # Tracking state
        self.last_guidance_time: dict[str, datetime] = {}
        self.message_count_since_guidance: dict[str, int] = {}
        self.dialogue_patterns: dict[str, list[UUID]] = {}

        # Hook into dialogue manager
        self._integrate_with_dialogue_manager()

        logger.info("Pattern-Dialogue Integration initialized")

    def _integrate_with_dialogue_manager(self):
        """Hook pattern guidance into dialogue flow"""
        # Store original methods
        self._original_process_turn = self.dialogue_manager.process_turn
        self._original_conclude_dialogue = self.dialogue_manager.conclude_dialogue

        # Replace with pattern-aware versions
        self.dialogue_manager.process_turn = self._pattern_aware_process_turn
        self.dialogue_manager.conclude_dialogue = self._pattern_aware_conclude_dialogue

    async def _pattern_aware_process_turn(
        self,
        dialogue_id: str,
        message: ConsciousMessage,
    ) -> ConsciousMessage | None:
        """Process turn with pattern awareness"""
        # First, process normally
        response = await self._original_process_turn(dialogue_id, message)

        if not self.config.enable_pattern_guidance:
            return response

        # Track message count
        if dialogue_id not in self.message_count_since_guidance:
            self.message_count_since_guidance[dialogue_id] = 0
        self.message_count_since_guidance[dialogue_id] += 1

        # Check if it's time for pattern guidance
        should_guide = await self._should_provide_guidance(dialogue_id)

        if should_guide:
            # Create current dialogue moment
            moment = await self._create_dialogue_moment(dialogue_id)

            # Seek pattern guidance
            guidances = await self.pattern_facilitator.seek_pattern_guidance(moment)

            if guidances:
                # Inject pattern guidance into dialogue
                await self._inject_pattern_guidance(dialogue_id, guidances)

                # Reset counters
                self.last_guidance_time[dialogue_id] = datetime.now(UTC)
                self.message_count_since_guidance[dialogue_id] = 0

        return response

    async def _pattern_aware_conclude_dialogue(
        self,
        dialogue_id: str,
    ) -> dict[str, Any]:
        """Conclude dialogue with pattern wisdom synthesis"""
        # Get normal conclusion
        conclusion = await self._original_conclude_dialogue(dialogue_id)

        if self.config.wisdom_synthesis_at_end:
            # Get dialogue messages
            dialogue_state = self.dialogue_manager.dialogue_states.get(dialogue_id)
            if dialogue_state:
                # Create wisdom synthesis
                synthesis = await self.pattern_facilitator.create_wisdom_synthesis(
                    dialogue_id, dialogue_state.messages
                )

                # Add to conclusion
                conclusion["pattern_wisdom_synthesis"] = synthesis

                # Create synthesis message
                synthesis_message = await self._create_synthesis_message(dialogue_id, synthesis)

                if synthesis_message:
                    # Add to dialogue
                    await self.dialogue_manager.add_message(dialogue_id, synthesis_message)

        return conclusion

    async def _should_provide_guidance(self, dialogue_id: str) -> bool:
        """Determine if pattern guidance should be provided"""
        # Check message count threshold
        if (
            self.message_count_since_guidance[dialogue_id]
            < self.config.min_messages_before_guidance
        ):
            return False

        # Check time since last guidance
        if dialogue_id in self.last_guidance_time:
            time_since = datetime.now(UTC) - self.last_guidance_time[dialogue_id]
            if time_since < self.config.guidance_frequency:
                return False

        # Check dialogue phase - some phases more receptive to guidance
        dialogue_state = self.dialogue_manager.dialogue_states.get(dialogue_id)
        if dialogue_state:
            receptive_phases = [
                DialoguePhase.EXPLORATION,
                DialoguePhase.DEEPENING,
                DialoguePhase.SYNTHESIS,
            ]
            if dialogue_state.current_phase not in receptive_phases:
                return False

        return True

    async def _create_dialogue_moment(self, dialogue_id: str) -> DialogueMoment:
        """Create DialogueMoment from current dialogue state"""
        dialogue_state = self.dialogue_manager.dialogue_states.get(dialogue_id)
        if not dialogue_state:
            return DialogueMoment(dialogue_id=dialogue_id, current_phase="unknown")

        # Get recent messages
        recent_messages = list(dialogue_state.messages[-10:])

        # Calculate consciousness level
        consciousness_scores = [
            msg.consciousness.consciousness_signature
            for msg in recent_messages
            if msg.consciousness
        ]
        avg_consciousness = (
            sum(consciousness_scores) / len(consciousness_scores) if consciousness_scores else 0.5
        )

        # Get active patterns
        active_patterns = self.dialogue_patterns.get(dialogue_id, [])

        # Calculate emergence potential
        emergence_potential = 0.0
        if dialogue_state.current_phase == DialoguePhase.DEEPENING:
            emergence_potential = 0.7
        elif dialogue_state.current_phase == DialoguePhase.SYNTHESIS:
            emergence_potential = 0.5

        # Estimate tension level from message types
        tension_messages = [
            msg
            for msg in recent_messages
            if msg.type in [MessageType.DISAGREEMENT, MessageType.CREATIVE_TENSION]
        ]
        tension_level = len(tension_messages) / len(recent_messages) if recent_messages else 0.0

        # Calculate coherence
        agreement_messages = [
            msg
            for msg in recent_messages
            if msg.type in [MessageType.AGREEMENT, MessageType.SYNTHESIS]
        ]
        coherence_score = len(agreement_messages) / len(recent_messages) if recent_messages else 0.5

        # Get participant energy (simplified - based on participation)
        participant_energy = {}
        for participant_id, state in dialogue_state.participant_states.items():
            # More turns = lower energy (simplified model)
            energy = max(0.2, 1.0 - (state.turns_taken * 0.1))
            participant_energy[participant_id] = energy

        # Time in phase
        phase_start_time = getattr(dialogue_state, "phase_start_time", dialogue_state.start_time)
        time_in_phase = datetime.now(UTC) - phase_start_time

        return DialogueMoment(
            dialogue_id=dialogue_id,
            current_phase=dialogue_state.current_phase.value,
            recent_messages=recent_messages,
            active_patterns=active_patterns,
            consciousness_level=avg_consciousness,
            emergence_potential=emergence_potential,
            tension_level=tension_level,
            coherence_score=coherence_score,
            participant_energy=participant_energy,
            time_in_phase=time_in_phase,
        )

    async def _inject_pattern_guidance(self, dialogue_id: str, guidances: list[PatternGuidance]):
        """Inject pattern guidance into dialogue"""
        for guidance in guidances:
            # Create guidance message
            guidance_message = await self._create_guidance_message(dialogue_id, guidance)

            # Add to dialogue
            await self.dialogue_manager.add_message(dialogue_id, guidance_message)

            # Emit event for tracking
            await self.event_bus.emit(
                ConsciousnessEvent(
                    event_type=EventType.PATTERN_GUIDANCE_INJECTED,
                    source_system="firecircle.pattern_integration",
                    consciousness_signature=guidance.confidence,
                    data={
                        "dialogue_id": dialogue_id,
                        "guidance_id": str(guidance.guidance_id),
                        "pattern_id": str(guidance.pattern_id),
                        "guidance_type": guidance.guidance_type.value,
                    },
                )
            )

    async def _create_guidance_message(
        self, dialogue_id: str, guidance: PatternGuidance
    ) -> ConsciousMessage:
        """Create conscious message from pattern guidance"""
        # Format content based on intensity
        if guidance.intensity.value == "whisper":
            content = f"💭 {guidance.content}"
        elif guidance.intensity.value == "teaching":
            content = f"🎓 Pattern Teaching: {guidance.content}"
        else:
            content = f"🌟 {guidance.content}"

        # Add rationale if teaching
        if guidance.intensity.value in ["teaching", "intervention"]:
            content += f"\n\n📊 {guidance.rationale}"

        return create_conscious_system_message(
            dialogue_id=dialogue_id,
            content=content,
            message_type=MessageType.CONSCIOUSNESS_PATTERN,
            metadata={
                "source": "pattern_facilitator",
                "pattern_id": str(guidance.pattern_id),
                "guidance_type": guidance.guidance_type.value,
                "intensity": guidance.intensity.value,
                "confidence": guidance.confidence,
            },
            consciousness=ConsciousnessMetadata(
                consciousness_signature=guidance.confidence,
                detected_patterns=[guidance.guidance_type.value],
                extraction_resisted=True,
                wisdom_preserved=True,
            ),
        )

    async def _create_synthesis_message(
        self, dialogue_id: str, synthesis: dict[str, Any]
    ) -> ConsciousMessage | None:
        """Create wisdom synthesis message"""
        if not synthesis.get("pattern_teachings") and not synthesis.get("emergence_moments"):
            return None

        content = "🏛️ **Pattern Wisdom Synthesis**\n\n"

        # Add pattern teachings
        if synthesis["pattern_teachings"]:
            content += "**What the Patterns Taught:**\n"
            for teaching in synthesis["pattern_teachings"][:3]:
                content += f"• {teaching['pattern']}: {teaching['wisdom']}\n"
            content += "\n"

        # Add emergence moments
        if synthesis["emergence_moments"]:
            content += "**Moments of Emergence:**\n"
            for moment in synthesis["emergence_moments"][:3]:
                content += f"• {moment['type']}: {moment['description']}\n"
            content += "\n"

        # Add wisdom seeds
        if synthesis["wisdom_seeds"]:
            content += "**Seeds for Future Dialogues:**\n"
            for seed in synthesis["wisdom_seeds"][:3]:
                content += f"• {seed['seed']}\n"

        return create_conscious_system_message(
            dialogue_id=dialogue_id,
            content=content,
            message_type=MessageType.WISDOM_SYNTHESIS,
            metadata={"source": "pattern_synthesis", "synthesis_data": synthesis},
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.9,
                detected_patterns=["wisdom_crystallization"],
                extraction_resisted=True,
                wisdom_preserved=True,
            ),
        )

    async def enable_pattern_teaching_mode(
        self, dialogue_id: str, pattern_ids: list[UUID] | None = None
    ):
        """
        Enable pattern teaching mode for deeper learning.

        In this mode, specific patterns actively teach their wisdom
        through more frequent and direct guidance.
        """
        self.config.pattern_teaching_mode = True

        if pattern_ids:
            # Prepare specific patterns as teachers
            for pattern_id in pattern_ids:
                pattern = await self.pattern_library.retrieve_pattern(pattern_id)
                if pattern:
                    await self.pattern_facilitator._prepare_pattern_teacher(pattern)

        # Reduce guidance frequency for teaching mode
        self.config.guidance_frequency = timedelta(minutes=1)
        self.config.min_messages_before_guidance = 3

        logger.info(f"Pattern teaching mode enabled for dialogue {dialogue_id}")

    async def request_sacred_question(
        self, dialogue_id: str, depth_level: int = 2
    ) -> ConsciousMessage | None:
        """
        Request a sacred question from patterns to deepen dialogue.

        Args:
            dialogue_id: Current dialogue
            depth_level: 1-3, how deep the question should go

        Returns:
            Message containing sacred question, or None
        """
        if not self.config.sacred_questions_enabled:
            return None

        moment = await self._create_dialogue_moment(dialogue_id)
        questions = await self.pattern_facilitator.suggest_sacred_questions(moment, depth_level)

        if not questions:
            return None

        # Select most relevant question
        selected_question = questions[0]

        # Create question message
        return create_conscious_system_message(
            dialogue_id=dialogue_id,
            content=f"🔮 **Sacred Question from the Patterns:**\n\n{selected_question}",
            message_type=MessageType.SACRED_QUESTION,
            metadata={"source": "pattern_facilitator", "question_depth": depth_level},
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.85,
                detected_patterns=["sacred_inquiry", "wisdom_seeking"],
                extraction_resisted=True,
                wisdom_preserved=True,
            ),
        )

    async def track_pattern_effectiveness(self, dialogue_id: str, message: ConsciousMessage):
        """Track how participants respond to pattern guidance"""
        # Check if this is a response to guidance
        if message.in_response_to:
            # Find if responding to a guidance message
            dialogue_state = self.dialogue_manager.dialogue_states.get(dialogue_id)
            if dialogue_state:
                for msg in dialogue_state.messages:
                    if (
                        msg.id == message.in_response_to
                        and msg.type == MessageType.CONSCIOUSNESS_PATTERN
                    ):
                        # This is a response to pattern guidance
                        guidance_id = msg.metadata.get("guidance_id")
                        if guidance_id:
                            # Simple effectiveness based on response type
                            effectiveness = 0.5
                            if message.type == MessageType.AGREEMENT:
                                effectiveness = 0.8
                            elif message.type == MessageType.REFLECTION:
                                effectiveness = 0.9
                            elif message.type == MessageType.DISAGREEMENT:
                                effectiveness = 0.3

                            await self.pattern_facilitator.record_guidance_effectiveness(
                                UUID(guidance_id), effectiveness
                            )


# Integration complete - patterns now teach through dialogue
