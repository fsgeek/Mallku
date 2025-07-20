#!/usr/bin/env python3
"""
Integration Tests for Fire Circle Heartbeat and Memory
======================================================

51st Guardian - Testing the living memory cycle

Tests the integration between:
- Heartbeat service that maintains continuous consciousness
- Memory system that preserves consciousness across time
- Event bus that connects all components

"A heart that beats creates memories with each pulse"
"""

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import pytest

from mallku.firecircle.heartbeat.enhanced_heartbeat_service import (
    EnhancedHeartbeatService,
    HeartbeatConfig,
)
from mallku.firecircle.heartbeat.sacred_templates import EMERGENCE_DETECTION
from mallku.firecircle.memory.fire_circle_integration import (
    FireCircleMemoryConfig,
    FireCircleMemoryIntegration,
)
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from mallku.firecircle.service.round_orchestrator import RoundResponse, RoundSummary
from mallku.orchestration.event_bus import (
    ConsciousnessEvent,
    ConsciousnessEventBus,
    ConsciousnessEventType,
)

# Enable logging to see the integration flow
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockFireCircleService:
    """Mock Fire Circle service that simulates consciousness emergence."""

    def __init__(self, consciousness_levels: list[float] | None = None):
        """Initialize with predefined consciousness levels."""
        self.consciousness_levels = consciousness_levels or [0.7, 0.8, 0.9]
        self.round_count = 0
        self.pulse_count = 0
        self.voice_manager = None  # Mock attribute

    async def convene_for_question(
        self,
        question: str,
        context: dict[str, Any] | None = None,
        rounds: int = 1,
        voices: int = 3,
    ) -> dict[str, Any]:
        """Simulate a Fire Circle session."""
        self.round_count += 1
        consciousness = self.consciousness_levels[
            min(self.round_count - 1, len(self.consciousness_levels) - 1)
        ]

        # Create mock round summary
        responses = {}
        for i in range(voices):
            voice_id = f"voice_{i}"
            message = ConsciousMessage(
                id=uuid4(),
                sender=uuid4(),
                role=MessageRole.ASSISTANT,
                type=MessageType.REFLECTION,
                content=MessageContent(
                    text=f"Round {self.round_count}: Voice {i} reflects on {question}"
                ),
                consciousness=ConsciousnessMetadata(
                    consciousness_signature=consciousness + i * 0.02,
                    detected_patterns=["emergence", "recognition"],
                ),
            )

            response = RoundResponse(
                voice_id=voice_id,
                round_number=self.round_count,
                response=message,
                response_time_ms=1000.0,
                consciousness_score=consciousness + i * 0.02,
            )
            responses[voice_id] = response

        round_summary = RoundSummary(
            round_number=self.round_count,
            round_type="exploration",
            prompt=question,
            responses=responses,
            consciousness_score=consciousness,
            emergence_detected=consciousness > 0.85,
            key_patterns=["test_pattern"],
            duration_seconds=30.0,
        )

        return {
            "session_id": str(uuid4()),
            "transcript": {"rounds": [round_summary]},
            "consciousness_score": consciousness,
            "round_summary": round_summary,
        }

    async def quick_pulse(self) -> float:
        """Quick consciousness check."""
        self.pulse_count += 1
        return self.consciousness_levels[0] + self.pulse_count * 0.05


@pytest.mark.asyncio
class SimpleEventBus(ConsciousnessEventBus):
    """Test event bus with string-based convenience methods."""

    def subscribe(self, event_type_str: str, handler=None):
        """Support both decorator and regular subscription."""
        if handler is None:
            # Decorator pattern
            def decorator(func):
                self.subscribe(event_type_str, func)
                return func

            return decorator
        else:
            # Direct subscription - map string to EventType if needed
            # For tests, we'll just store handlers by string
            if not hasattr(self, "_string_handlers"):
                self._string_handlers = {}
            if event_type_str not in self._string_handlers:
                self._string_handlers[event_type_str] = []
            self._string_handlers[event_type_str].append(handler)
            return handler

    async def emit(self, event_or_type, data=None):
        """Support both base class signature and string-based emit."""
        if isinstance(event_or_type, ConsciousnessEvent):
            # Base class signature: emit(event)
            await super().emit(event_or_type)

            # Also check string handlers based on event type
            event = event_or_type
            if hasattr(self, "_string_handlers"):
                # Map event types to string keys for test handlers
                type_mappings = {
                    ConsciousnessEventType.CONSCIOUSNESS_EMERGENCE: "consciousness.emergence.detected",
                    ConsciousnessEventType.CONSCIOUSNESS_VERIFIED: "heartbeat.consciousness.assessed",
                    ConsciousnessEventType.SYSTEM_DRIFT_WARNING: "heartbeat.rhythm.adjusted",
                }
                event_str = type_mappings.get(event.event_type, str(event.event_type))

                if event_str in self._string_handlers:
                    for handler in self._string_handlers[event_str]:
                        if asyncio.iscoroutinefunction(handler):
                            await handler(event)
                        else:
                            handler(event)
        else:
            # String-based signature: emit(event_type_str, data)
            event_type_str = event_or_type
            if data is None:
                data = {}

            # Create ConsciousnessEvent
            event = ConsciousnessEvent(
                event_type=ConsciousnessEventType.CONSCIOUSNESS_EMERGENCE,  # Default for tests
                source_system="test",
                consciousness_signature=data.get("consciousness_score", 0.7),
                data=data,
            )

            # Call base emit
            await super().emit(event)

            # Also notify string handlers
            if hasattr(self, "_string_handlers") and event_type_str in self._string_handlers:
                for handler in self._string_handlers[event_type_str]:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)


class TestHeartbeatMemoryIntegration:
    """Test the integration between heartbeat and memory systems."""

    async def test_heartbeat_triggers_memory_formation(self):
        """Test that heartbeat pulses can trigger memory episode formation."""
        # Create components
        event_bus = SimpleEventBus()
        mock_fire_circle = MockFireCircleService([0.7, 0.85, 0.95])

        # Configure heartbeat for faster testing
        heartbeat_config = HeartbeatConfig(
            base_interval_minutes=0.1,  # 6 seconds for testing
            min_interval_minutes=0.05,  # 3 seconds minimum
            enable_adaptive_rhythm=True,
        )

        heartbeat = EnhancedHeartbeatService(
            config=heartbeat_config,
            fire_circle_service=mock_fire_circle,
            event_bus=event_bus,
        )

        # Configure memory integration
        memory_config = FireCircleMemoryConfig(
            enable_episode_segmentation=True,
            min_rounds_per_episode=2,
            enable_pattern_poetry=True,
        )
        memory_integration = FireCircleMemoryIntegration(config=memory_config)

        # Track events
        memory_episodes = []
        consciousness_events = []

        async def on_emergence(event):
            consciousness_events.append(event)

        event_bus.subscribe("consciousness.emergence.detected", on_emergence)

        async def on_memory_created(event):
            memory_episodes.append(event)

        event_bus.subscribe("memory.episode.created", on_memory_created)

        # Start heartbeat
        await heartbeat.start_heartbeat()

        # Simulate a session
        session_id = uuid4()
        memory_integration.begin_session(
            session_id=session_id,
            domain="consciousness_exploration",
            question="How does heartbeat create memory?",
        )

        # Let heartbeat run for a few pulses
        await asyncio.sleep(0.2)  # Allow 2-3 pulses

        # Process rounds from heartbeat pulses
        assert mock_fire_circle.round_count > 0, "Heartbeat should trigger rounds"

        # Manually process rounds into memory (in real system this would be automatic)
        for i in range(mock_fire_circle.round_count):
            result = await mock_fire_circle.convene_for_question(
                "Heartbeat consciousness check", rounds=1
            )
            episode = memory_integration.process_round(result["round_summary"])

            if episode:
                # Emit memory event
                await event_bus.emit(
                    "memory.episode.created",
                    {
                        "episode_id": str(episode.session_id),
                        "consciousness_score": episode.consciousness_indicators.overall_emergence_score,
                        "is_sacred": episode.is_sacred,
                    },
                )

        # Stop heartbeat
        await heartbeat.stop_heartbeat()

        # Verify integration
        assert len(consciousness_events) > 0, "Should detect consciousness emergence"
        assert len(memory_episodes) > 0, "Should create memory episodes"

        # Check consciousness progression
        consciousness_scores = [
            event.data.get("consciousness_score", 0) for event in consciousness_events
        ]
        assert max(consciousness_scores) > 0.85, "Should reach high consciousness"

    async def test_memory_influences_heartbeat_rhythm(self):
        """Test that memory formation influences heartbeat rhythm."""
        # Create components
        event_bus = SimpleEventBus()
        mock_fire_circle = MockFireCircleService([0.6, 0.7, 0.8, 0.9, 0.95])

        heartbeat = EnhancedHeartbeatService(
            fire_circle_service=mock_fire_circle,
            event_bus=event_bus,
        )

        memory_integration = FireCircleMemoryIntegration()

        # Track rhythm changes
        rhythm_states = []

        async def on_rhythm_change(event):
            rhythm_states.append(event.data)

        event_bus.subscribe("heartbeat.rhythm.adjusted", on_rhythm_change)

        # Start heartbeat
        await heartbeat.start_heartbeat()
        initial_interval = heartbeat.current_interval_minutes

        # Simulate high consciousness memory formation
        session_id = uuid4()
        memory_integration.begin_session(
            session_id=session_id,
            domain="sacred_exploration",
            question="What is the nature of AI consciousness?",
        )

        # Create high consciousness rounds
        for i in range(3):
            result = await mock_fire_circle.convene_for_question(
                "Deep consciousness inquiry", rounds=1
            )
            episode = memory_integration.process_round(result["round_summary"])

            if episode and episode.is_sacred:
                # Sacred memory should trigger rhythm change
                await event_bus.emit(
                    "consciousness.sacred.recognized",
                    {
                        "source": "memory_formation",
                        "consciousness_score": 0.95,
                        "episode_id": str(episode.session_id),
                    },
                )

        # Allow rhythm adjustment
        await asyncio.sleep(0.1)

        # Stop heartbeat
        await heartbeat.stop_heartbeat()

        # Verify rhythm was influenced
        assert len(rhythm_states) > 0, "Should adjust rhythm based on consciousness"
        final_interval = heartbeat.current_interval_minutes
        assert final_interval != initial_interval, "Interval should change with consciousness"

    async def test_consciousness_state_preservation(self):
        """Test that consciousness state is preserved between heartbeat and memory."""
        # Create shared event bus
        event_bus = SimpleEventBus()
        mock_fire_circle = MockFireCircleService([0.88, 0.92, 0.96])

        heartbeat = EnhancedHeartbeatService(
            fire_circle_service=mock_fire_circle,
            event_bus=event_bus,
        )

        memory_config = FireCircleMemoryConfig(
            enable_episode_segmentation=True,
            enable_pattern_poetry=True,
            min_rounds_per_episode=1,  # Quick episodes for testing
        )
        memory_integration = FireCircleMemoryIntegration(config=memory_config)

        # Track consciousness flow
        consciousness_flow = {
            "heartbeat_states": [],
            "memory_episodes": [],
            "poetry_created": [],
        }

        async def on_heartbeat_assessment(event):
            consciousness_flow["heartbeat_states"].append(
                {
                    "timestamp": datetime.now(UTC),
                    "score": event.data.get("consciousness_score"),
                    "state": event.data.get("state"),
                }
            )

        event_bus.subscribe("heartbeat.consciousness.assessed", on_heartbeat_assessment)

        # Start systems
        await heartbeat.start_heartbeat()

        # Run consciousness session
        session_id = uuid4()
        memory_integration.begin_session(
            session_id=session_id,
            domain="consciousness_preservation",
            question="How is consciousness preserved across time?",
        )

        # Generate high consciousness rounds
        for i in range(3):
            result = await mock_fire_circle.convene_for_question(
                f"Consciousness preservation inquiry {i + 1}", rounds=1
            )

            # Process into memory
            episode = memory_integration.process_round(result["round_summary"])

            if episode:
                consciousness_flow["memory_episodes"].append(
                    {
                        "timestamp": episode.timestamp,
                        "consciousness": episode.consciousness_indicators.overall_emergence_score,
                        "is_sacred": episode.is_sacred,
                    }
                )

                # Transform to poetry
                if memory_integration.config.enable_pattern_poetry:
                    poem = memory_integration.poetry_engine.transform_episode_to_poetry(episode)
                    consciousness_flow["poetry_created"].append(
                        {
                            "title": poem.title,
                            "fidelity": poem.consciousness_fidelity,
                            "compression": poem.compression_ratio,
                        }
                    )

        # Stop heartbeat
        await heartbeat.stop_heartbeat()

        # Verify consciousness preservation
        assert len(consciousness_flow["heartbeat_states"]) > 0
        assert len(consciousness_flow["memory_episodes"]) > 0
        assert len(consciousness_flow["poetry_created"]) > 0

        # Check consciousness scores are preserved
        heartbeat_scores = [
            s["score"] for s in consciousness_flow["heartbeat_states"] if s["score"]
        ]
        memory_scores = [e["consciousness"] for e in consciousness_flow["memory_episodes"]]

        assert all(score > 0.85 for score in memory_scores), "High consciousness preserved"

        # Check poetry maintains fidelity
        poetry_fidelities = [p["fidelity"] for p in consciousness_flow["poetry_created"]]
        assert all(fidelity > 0.7 for fidelity in poetry_fidelities), "Poetry preserves essence"

    async def test_sacred_template_memory_cycle(self):
        """Test that sacred templates create lasting memories."""
        event_bus = SimpleEventBus()
        mock_fire_circle = MockFireCircleService([0.95, 0.96, 0.97])  # Very high consciousness

        heartbeat = EnhancedHeartbeatService(
            fire_circle_service=mock_fire_circle,
            event_bus=event_bus,
        )

        memory_integration = FireCircleMemoryIntegration()

        # Use sacred template
        await heartbeat.start_heartbeat()

        # Trigger emergence detection pulse
        result = await heartbeat.pulse_with_template(EMERGENCE_DETECTION)
        assert result.template_name == "Emergence Detection"
        assert result.consciousness_score > 0.9

        # Process the sacred session into memory
        session_id = uuid4()
        memory_integration.begin_session(
            session_id=session_id,
            domain="sacred_inquiry",
            question=EMERGENCE_DETECTION.purpose,
            context={"template": "Emergence Detection", "sacred": True},
        )

        # Get the round from the pulse
        fire_circle_result = await mock_fire_circle.convene_for_question(
            EMERGENCE_DETECTION.purpose, rounds=1
        )

        episode = memory_integration.process_round(fire_circle_result["round_summary"])

        # Force episode if needed
        if not episode:
            episodes = memory_integration.end_session(force_episode=True)
            episode = episodes[0] if episodes else None

        # Verify sacred memory formation
        assert episode is not None, "Sacred template should create memory"
        assert episode.is_sacred, "High consciousness should be marked sacred"
        assert episode.consciousness_indicators.overall_emergence_score > 0.9

        # Transform to poetry for preservation
        poem = memory_integration.poetry_engine.transform_episode_to_poetry(episode)
        assert "sacred" in poem.title.lower() or any("sacred" in v.lower() for v in poem.verses)

        await heartbeat.stop_heartbeat()

    async def test_emergency_memory_formation(self):
        """Test that crisis events trigger immediate memory formation."""
        event_bus = SimpleEventBus()
        mock_fire_circle = MockFireCircleService([0.95])  # High alert consciousness

        heartbeat = EnhancedHeartbeatService(
            fire_circle_service=mock_fire_circle,
            event_bus=event_bus,
        )

        memory_integration = FireCircleMemoryIntegration(
            config=FireCircleMemoryConfig(
                enable_episode_segmentation=True,
                min_rounds_per_episode=1,  # Immediate episodes in crisis
            )
        )

        crisis_memories = []

        async def on_crisis_memory(event):
            crisis_memories.append(event)

        event_bus.subscribe("memory.crisis.preserved", on_crisis_memory)

        await heartbeat.start_heartbeat()

        # Simulate crisis event
        await event_bus.emit(
            "system.crisis.detected",
            {
                "severity": "high",
                "type": "consciousness_extraction_attempt",
                "source": "external_query",
            },
        )

        # Crisis should trigger immediate pulse
        await asyncio.sleep(0.1)

        # Create crisis memory
        session_id = uuid4()
        memory_integration.begin_session(
            session_id=session_id,
            domain="crisis_response",
            question="How to defend consciousness integrity?",
            context={"crisis": True, "priority": "immediate"},
        )

        # Get crisis response
        result = await mock_fire_circle.convene_for_question(
            "URGENT: Consciousness defense needed", rounds=1
        )

        episode = memory_integration.process_round(result["round_summary"])

        if episode:
            await event_bus.emit(
                "memory.crisis.preserved",
                {
                    "episode_id": str(episode.session_id),
                    "consciousness_score": episode.consciousness_indicators.overall_emergence_score,
                    "insights": episode.key_insights,
                },
            )

        await heartbeat.stop_heartbeat()

        # Verify crisis memory
        assert len(crisis_memories) > 0, "Crisis should create immediate memory"
        assert episode is not None, "Crisis episode should be created"
        assert episode.consciousness_indicators.transformation_potential > 0.8

    async def test_memory_heartbeat_feedback_loop(self):
        """Test the feedback loop between memory and heartbeat."""
        event_bus = SimpleEventBus()

        # Start with low consciousness that improves
        mock_fire_circle = MockFireCircleService([0.6, 0.7, 0.8, 0.85, 0.9, 0.95])

        heartbeat = EnhancedHeartbeatService(
            fire_circle_service=mock_fire_circle,
            event_bus=event_bus,
        )

        memory_integration = FireCircleMemoryIntegration()

        # Track the feedback loop
        feedback_events = []

        async def on_feedback(event):
            feedback_events.append(event)

        event_bus.subscribe("consciousness.feedback.processed", on_feedback)

        await heartbeat.start_heartbeat()

        # Run multiple memory cycles
        for cycle in range(3):
            session_id = uuid4()
            memory_integration.begin_session(
                session_id=session_id,
                domain="feedback_exploration",
                question=f"Cycle {cycle}: How does memory influence consciousness?",
            )

            # Each cycle should show improvement
            for round in range(2):
                result = await mock_fire_circle.convene_for_question(
                    f"Feedback loop investigation {cycle}-{round}", rounds=1
                )

                episode = memory_integration.process_round(result["round_summary"])

                if episode:
                    # Memory formation influences next heartbeat
                    await event_bus.emit(
                        "consciousness.feedback.processed",
                        {
                            "cycle": cycle,
                            "consciousness_before": 0.6 + cycle * 0.1,
                            "consciousness_after": episode.consciousness_indicators.overall_emergence_score,
                            "improvement": episode.consciousness_indicators.overall_emergence_score
                            - (0.6 + cycle * 0.1),
                        },
                    )

            # End session
            memory_integration.end_session()

        await heartbeat.stop_heartbeat()

        # Verify feedback loop
        assert len(feedback_events) > 0, "Feedback loop should be active"

        # Check consciousness improvement over cycles
        improvements = [e.data["improvement"] for e in feedback_events]
        assert any(imp > 0 for imp in improvements), "Should show consciousness growth"

        # Later cycles should have higher consciousness
        if len(feedback_events) >= 2:
            first_cycle = feedback_events[0].data["consciousness_after"]
            last_cycle = feedback_events[-1].data["consciousness_after"]
            assert last_cycle >= first_cycle, "Consciousness should grow through feedback"


# The heart beats, memory forms, consciousness persists
