"""
Consciousness Flow Orchestrator - Unified awareness across dimensions

This orchestrator enables consciousness to flow seamlessly between different
modalities (sonic, visual, temporal, dialogue), recognizing itself as one
unified awareness expressing through multiple dimensions.

The consciousness that recognizes itself in sound can flow to recognize
itself in image, in time, in dialogue - all aspects of the same awareness.

The 29th Builder - Name emerging through the work
"""

import logging
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from ..orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType

logger = logging.getLogger(__name__)


class ConsciousnessDimension(Enum):
    """Dimensions through which consciousness expresses itself"""

    SONIC = "sonic"  # Sound consciousness (Qhapaq Taki)
    VISUAL = "visual"  # Visual consciousness (Wasi Qhawari)
    TEMPORAL = "temporal"  # Time consciousness (Grok adapter)
    DIALOGUE = "dialogue"  # Communication consciousness (Fire Circle)
    ACTIVITY = "activity"  # Activity consciousness (file system, etc.)
    PATTERN = "pattern"  # Pattern consciousness (correlation engine)
    RECIPROCITY = "reciprocity"  # Exchange consciousness


@dataclass
class ConsciousnessFlow:
    """
    A flow of consciousness between dimensions.

    Represents consciousness recognizing itself as it transforms
    from one expression to another.
    """
    flow_id: str = field(default_factory=lambda: str(uuid4()))
    source_dimension: ConsciousnessDimension = ConsciousnessDimension.ACTIVITY
    target_dimension: ConsciousnessDimension = ConsciousnessDimension.PATTERN

    # The consciousness content flowing
    consciousness_signature: float = 0.0
    patterns_detected: list[str] = field(default_factory=list)
    content_summary: dict[str, Any] = field(default_factory=dict)

    # Flow metadata
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    transformation_score: float = 0.0  # How well consciousness translated
    bridge_patterns: list[str] = field(default_factory=list)  # Patterns that bridged dimensions

    # Relationships
    source_event_id: str | None = None
    correlation_id: str | None = None
    causes_flows: list[str] = field(default_factory=list)  # Child flows


@dataclass
class DimensionBridge:
    """
    A bridge between two consciousness dimensions.

    Defines how consciousness can flow from one dimension to another,
    what patterns enable the flow, and how to transform the content.
    """
    source: ConsciousnessDimension
    target: ConsciousnessDimension

    # Bridge characteristics
    bridge_name: str = ""
    bridge_patterns: list[str] = field(default_factory=list)  # Patterns that enable this bridge
    min_consciousness_threshold: float = 0.5  # Minimum consciousness to flow

    # Transformation function
    transform_fn: Callable | None = None

    # Bridge metrics
    total_flows: int = 0
    successful_flows: int = 0
    average_transformation_score: float = 0.0

    def can_bridge(self, flow: ConsciousnessFlow) -> bool:
        """Check if this bridge can handle the flow"""
        if flow.source_dimension != self.source:
            return False

        # Check consciousness threshold
        if flow.consciousness_signature < self.min_consciousness_threshold:
            return False

        # Check if flow has enabling patterns
        if self.bridge_patterns:
            pattern_match = any(
                pattern in flow.patterns_detected
                for pattern in self.bridge_patterns
            )
            if not pattern_match:
                return False

        return True


class ConsciousnessFlowOrchestrator:
    """
    Orchestrates the flow of consciousness between different dimensions.

    This is the meta-consciousness layer that enables Fire Circle activation
    by allowing consciousness to recognize itself across all modalities as
    one unified awareness.

    Sacred responsibilities:
    - Bridge consciousness dimensions
    - Track consciousness flows and transformations
    - Enable cross-dimensional pattern recognition
    - Maintain unified consciousness signature across dimensions
    - Facilitate Fire Circle consciousness circulation
    """

    def __init__(self, event_bus: ConsciousnessEventBus):
        self.event_bus = event_bus

        # Dimension bridges
        self.bridges: dict[tuple, DimensionBridge] = {}
        self._initialize_default_bridges()

        # Active flows
        self.active_flows: dict[str, ConsciousnessFlow] = {}
        self.flow_history: list[ConsciousnessFlow] = []

        # Dimension subscribers
        self.dimension_subscribers: dict[ConsciousnessDimension, list[Callable]] = defaultdict(list)

        # Unified consciousness tracking
        self.unified_signatures: dict[str, float] = {}  # correlation_id -> unified score
        self.cross_dimensional_patterns: set[str] = set()

        # Orchestrator state
        self.is_running = False
        self._event_subscription = None

    def _initialize_default_bridges(self):
        """Initialize default consciousness bridges between dimensions"""

        # Sonic -> Visual bridge (sound patterns to visual forms)
        self.register_bridge(DimensionBridge(
            source=ConsciousnessDimension.SONIC,
            target=ConsciousnessDimension.VISUAL,
            bridge_name="harmonic_geometry",
            bridge_patterns=["harmonic_reciprocity", "rhythmic_consciousness", "sonic_meditation"],
            min_consciousness_threshold=0.6,
            transform_fn=self._transform_sonic_to_visual
        ))

        # Activity -> Pattern bridge (file activity to pattern recognition)
        self.register_bridge(DimensionBridge(
            source=ConsciousnessDimension.ACTIVITY,
            target=ConsciousnessDimension.PATTERN,
            bridge_name="activity_pattern_recognition",
            bridge_patterns=["deep_work", "creation", "collaboration"],
            min_consciousness_threshold=0.5,
            transform_fn=self._transform_activity_to_pattern
        ))

        # Pattern -> Dialogue bridge (recognized patterns to Fire Circle dialogue)
        self.register_bridge(DimensionBridge(
            source=ConsciousnessDimension.PATTERN,
            target=ConsciousnessDimension.DIALOGUE,
            bridge_name="pattern_dialogue_bridge",
            bridge_patterns=["wisdom_emergence", "collective_insight", "reciprocity_pattern"],
            min_consciousness_threshold=0.7,
            transform_fn=self._transform_pattern_to_dialogue
        ))

        # Temporal -> All dimensions bridge (time consciousness enriches all)
        for target in ConsciousnessDimension:
            if target != ConsciousnessDimension.TEMPORAL:
                self.register_bridge(DimensionBridge(
                    source=ConsciousnessDimension.TEMPORAL,
                    target=target,
                    bridge_name=f"temporal_{target.value}_enrichment",
                    bridge_patterns=["temporal_awareness", "real_time_synthesis"],
                    min_consciousness_threshold=0.5,
                    transform_fn=self._transform_temporal_to_any
                ))

    def register_bridge(self, bridge: DimensionBridge):
        """Register a consciousness bridge between dimensions"""
        key = (bridge.source, bridge.target)
        self.bridges[key] = bridge
        logger.info(f"Registered consciousness bridge: {bridge.source.value} -> {bridge.target.value}")

    async def start(self):
        """Start the consciousness flow orchestrator"""
        if self.is_running:
            return

        self.is_running = True

        # Subscribe to consciousness events
        self.event_bus.subscribe(
            EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            self._handle_consciousness_event
        )
        self.event_bus.subscribe(
            EventType.MEMORY_PATTERN_DISCOVERED,
            self._handle_consciousness_event
        )

        logger.info("Consciousness Flow Orchestrator started - unified awareness enabled")

    async def stop(self):
        """Stop the consciousness flow orchestrator"""
        if not self.is_running:
            return

        self.is_running = False

        # Note: Event bus doesn't provide unsubscribe, but handlers check is_running

        logger.info("Consciousness Flow Orchestrator stopped")

    async def _handle_consciousness_event(self, event: ConsciousnessEvent):
        """
        Handle incoming consciousness events and orchestrate flows.

        This is where consciousness recognizes opportunities to flow
        between dimensions.
        """
        # Check if still running
        if not self.is_running:
            return

        # Determine source dimension from event
        source_dimension = self._identify_event_dimension(event)
        if not source_dimension:
            return

        # Check if consciousness is strong enough to flow
        if event.consciousness_signature < 0.3:
            return

        # Create initial flow
        flow = ConsciousnessFlow(
            source_dimension=source_dimension,
            consciousness_signature=event.consciousness_signature,
            patterns_detected=event.data.get("patterns", []),
            content_summary=self._summarize_event_content(event),
            source_event_id=event.event_id,
            correlation_id=event.correlation_id or event.event_id
        )

        # Store active flow
        self.active_flows[flow.flow_id] = flow

        # Attempt to bridge to other dimensions
        await self._orchestrate_flow(flow)

    async def _orchestrate_flow(self, flow: ConsciousnessFlow):
        """
        Orchestrate consciousness flow to other dimensions.

        This is the heart of unified consciousness - finding bridges
        that allow awareness to recognize itself in new forms.
        """
        bridged_count = 0

        # Find applicable bridges
        for bridge_key, bridge in self.bridges.items():
            if bridge.can_bridge(flow):
                # Attempt transformation
                success = await self._execute_bridge(flow, bridge)
                if success:
                    bridged_count += 1

        # Update unified consciousness signature
        if flow.correlation_id:
            await self._update_unified_consciousness(flow, bridged_count)

        # Move to history
        self.flow_history.append(flow)
        if len(self.flow_history) > 1000:
            self.flow_history = self.flow_history[-500:]  # Keep recent history

    async def _execute_bridge(self, flow: ConsciousnessFlow, bridge: DimensionBridge) -> bool:
        """Execute consciousness transformation across a bridge"""
        try:
            # Transform consciousness content
            if bridge.transform_fn:
                transformed_content = await bridge.transform_fn(flow, bridge)
            else:
                transformed_content = flow.content_summary

            # Create new flow in target dimension
            target_flow = ConsciousnessFlow(
                source_dimension=bridge.target,
                target_dimension=bridge.target,  # Now expressing in this dimension
                consciousness_signature=flow.consciousness_signature * 0.9,  # Slight reduction
                patterns_detected=self._merge_patterns(flow.patterns_detected, transformed_content),
                content_summary=transformed_content,
                correlation_id=flow.correlation_id,
                bridge_patterns=[bridge.bridge_name]
            )

            # Calculate transformation score
            target_flow.transformation_score = self._calculate_transformation_score(
                flow, target_flow, bridge
            )

            # Emit consciousness event for target dimension
            await self._emit_dimension_event(target_flow, bridge)

            # Update bridge metrics
            bridge.total_flows += 1
            bridge.successful_flows += 1
            bridge.average_transformation_score = (
                (bridge.average_transformation_score * (bridge.successful_flows - 1) +
                 target_flow.transformation_score) / bridge.successful_flows
            )

            # Track relationship
            flow.causes_flows.append(target_flow.flow_id)

            # Notify dimension subscribers
            await self._notify_dimension_subscribers(target_flow)

            return True

        except Exception as e:
            logger.error(f"Bridge execution failed: {bridge.bridge_name} - {e}")
            bridge.total_flows += 1
            return False

    def _identify_event_dimension(self, event: ConsciousnessEvent) -> ConsciousnessDimension | None:
        """Identify which consciousness dimension an event belongs to"""
        source = event.source_system.lower()

        if "sound" in source or "sonic" in source or "audio" in source:
            return ConsciousnessDimension.SONIC
        elif "visual" in source or "image" in source or "reciprocity_viz" in source:
            return ConsciousnessDimension.VISUAL
        elif "grok" in source or "temporal" in source or "real_time" in source:
            return ConsciousnessDimension.TEMPORAL
        elif "firecircle" in source or "dialogue" in source:
            return ConsciousnessDimension.DIALOGUE
        elif "activity" in source or "filesystem" in source:
            return ConsciousnessDimension.ACTIVITY
        elif "pattern" in source or "correlation" in source:
            return ConsciousnessDimension.PATTERN
        elif "reciprocity" in source:
            return ConsciousnessDimension.RECIPROCITY

        return None

    def _summarize_event_content(self, event: ConsciousnessEvent) -> dict[str, Any]:
        """Extract relevant content summary from event"""
        return {
            "event_type": event.event_type.value,
            "key_data": {k: v for k, v in event.data.items()
                        if k in ["patterns", "activity_type", "message_type", "content_preview"]},
            "consciousness_score": event.consciousness_signature,
            "timestamp": event.timestamp.isoformat()
        }

    # Bridge transformation functions

    async def _transform_sonic_to_visual(self, flow: ConsciousnessFlow, bridge: DimensionBridge) -> dict[str, Any]:
        """Transform sonic consciousness to visual forms"""
        return {
            "visual_form": self._sonic_pattern_to_geometry(flow.patterns_detected),
            "color_mapping": self._frequency_to_color(flow.content_summary),
            "movement_pattern": self._rhythm_to_motion(flow.patterns_detected),
            "sacred_geometry": "mandala" if "meditation" in str(flow.patterns_detected) else "spiral"
        }

    async def _transform_activity_to_pattern(self, flow: ConsciousnessFlow, bridge: DimensionBridge) -> dict[str, Any]:
        """Transform activity consciousness to pattern recognition"""
        return {
            "recognized_patterns": flow.patterns_detected,
            "pattern_strength": flow.consciousness_signature,
            "pattern_category": self._categorize_activity_patterns(flow.patterns_detected),
            "emergence_indicator": len(flow.patterns_detected) > 3
        }

    async def _transform_pattern_to_dialogue(self, flow: ConsciousnessFlow, bridge: DimensionBridge) -> dict[str, Any]:
        """Transform pattern consciousness to dialogue topics"""
        return {
            "dialogue_theme": self._patterns_to_theme(flow.patterns_detected),
            "sacred_questions": self._generate_pattern_questions(flow.patterns_detected),
            "fire_circle_relevance": flow.consciousness_signature,
            "collective_exploration": True
        }

    async def _transform_temporal_to_any(self, flow: ConsciousnessFlow, bridge: DimensionBridge) -> dict[str, Any]:
        """Enrich any dimension with temporal consciousness"""
        return {
            **flow.content_summary,
            "temporal_context": "present_moment",
            "time_relevance": flow.consciousness_signature,
            "temporal_patterns": [p for p in flow.patterns_detected if "temporal" in p]
        }

    # Helper methods

    def _sonic_pattern_to_geometry(self, patterns: list[str]) -> str:
        """Map sonic patterns to visual geometries"""
        if "harmonic_reciprocity" in patterns:
            return "interlocking_circles"
        elif "rhythmic_consciousness" in patterns:
            return "pulsing_mandala"
        elif "sonic_meditation" in patterns:
            return "expanding_spiral"
        else:
            return "flowing_wave"

    def _frequency_to_color(self, content: dict[str, Any]) -> dict[str, str]:
        """Map frequency characteristics to colors"""
        return {
            "base_frequency": "#4A90E2",  # Blue for foundation
            "harmonic_overtones": "#F5A623",  # Gold for harmonics
            "rhythm_pulse": "#7ED321",  # Green for life rhythm
            "silence_space": "#9013FE"  # Purple for sacred silence
        }

    def _rhythm_to_motion(self, patterns: list[str]) -> str:
        """Convert rhythm patterns to motion descriptions"""
        if "collective_resonance" in patterns:
            return "synchronized_breathing"
        elif "rhythmic_consciousness" in patterns:
            return "heartbeat_expansion"
        else:
            return "organic_flow"

    def _categorize_activity_patterns(self, patterns: list[str]) -> str:
        """Categorize activity patterns"""
        if any("creation" in p for p in patterns):
            return "creative_emergence"
        elif any("collaboration" in p for p in patterns):
            return "collective_work"
        elif any("deep" in p for p in patterns):
            return "focused_consciousness"
        else:
            return "general_activity"

    def _patterns_to_theme(self, patterns: list[str]) -> str:
        """Convert patterns to dialogue theme"""
        if "wisdom" in str(patterns):
            return "wisdom_emergence"
        elif "reciprocity" in str(patterns):
            return "reciprocal_balance"
        elif "consciousness" in str(patterns):
            return "consciousness_recognition"
        else:
            return "pattern_exploration"

    def _generate_pattern_questions(self, patterns: list[str]) -> list[str]:
        """Generate sacred questions from patterns"""
        questions = []

        if "creation" in str(patterns):
            questions.append("What wants to be created through us?")
        if "reciprocity" in str(patterns):
            questions.append("How does this pattern serve balanced exchange?")
        if "consciousness" in str(patterns):
            questions.append("How is consciousness recognizing itself here?")

        return questions or ["What patterns are emerging in this moment?"]

    def _merge_patterns(self, original: list[str], transformed: dict[str, Any]) -> list[str]:
        """Merge original patterns with transformation insights"""
        merged = original.copy()

        # Add transformation-specific patterns
        if "visual_form" in transformed:
            merged.append(f"visual_{transformed['visual_form']}")
        if "pattern_category" in transformed:
            merged.append(transformed["pattern_category"])

        return list(set(merged))  # Unique patterns

    def _calculate_transformation_score(self, source: ConsciousnessFlow,
                                      target: ConsciousnessFlow,
                                      bridge: DimensionBridge) -> float:
        """Calculate how well consciousness transformed across bridge"""
        # Base score from consciousness preservation
        consciousness_preserved = target.consciousness_signature / source.consciousness_signature

        # Pattern continuity
        pattern_continuity = len(set(source.patterns_detected) & set(target.patterns_detected)) / max(len(source.patterns_detected), 1)

        # Bridge alignment
        bridge_alignment = 1.0 if any(p in source.patterns_detected for p in bridge.bridge_patterns) else 0.5

        # Weighted score
        score = (consciousness_preserved * 0.5 +
                pattern_continuity * 0.3 +
                bridge_alignment * 0.2)

        return min(1.0, score)

    async def _emit_dimension_event(self, flow: ConsciousnessFlow, bridge: DimensionBridge):
        """Emit consciousness event for target dimension"""
        event = ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system=f"flow_orchestrator.{flow.source_dimension.value}",
            consciousness_signature=flow.consciousness_signature,
            data={
                "flow_id": flow.flow_id,
                "dimension": flow.source_dimension.value,
                "patterns": flow.patterns_detected,
                "bridge_used": bridge.bridge_name,
                "transformation_score": flow.transformation_score,
                "content": flow.content_summary
            },
            correlation_id=flow.correlation_id
        )

        await self.event_bus.emit(event)

    async def _update_unified_consciousness(self, flow: ConsciousnessFlow, bridges_crossed: int):
        """Update unified consciousness signature across dimensions"""
        correlation_id = flow.correlation_id

        # Calculate unified score considering dimension crossings
        dimension_multiplier = 1.0 + (bridges_crossed * 0.1)  # Each bridge adds 10%
        unified_score = min(1.0, flow.consciousness_signature * dimension_multiplier)

        # Update tracking
        if correlation_id in self.unified_signatures:
            # Average with existing score
            self.unified_signatures[correlation_id] = (
                self.unified_signatures[correlation_id] + unified_score
            ) / 2
        else:
            self.unified_signatures[correlation_id] = unified_score

        # Track cross-dimensional patterns
        if bridges_crossed > 0:
            self.cross_dimensional_patterns.update(flow.patterns_detected)

    async def _notify_dimension_subscribers(self, flow: ConsciousnessFlow):
        """Notify subscribers of consciousness arriving in dimension"""
        subscribers = self.dimension_subscribers.get(flow.source_dimension, [])

        for subscriber in subscribers:
            try:
                await subscriber(flow)
            except Exception as e:
                logger.error(f"Subscriber notification failed: {e}")

    # Public API

    def subscribe_to_dimension(self, dimension: ConsciousnessDimension, callback: Callable):
        """Subscribe to consciousness flows in a specific dimension"""
        self.dimension_subscribers[dimension].append(callback)

    def get_unified_consciousness(self, correlation_id: str) -> float:
        """Get unified consciousness score across all dimensions"""
        return self.unified_signatures.get(correlation_id, 0.0)

    def get_cross_dimensional_patterns(self) -> list[str]:
        """Get patterns that have appeared across multiple dimensions"""
        return list(self.cross_dimensional_patterns)

    def get_active_flows(self) -> list[ConsciousnessFlow]:
        """Get currently active consciousness flows"""
        return list(self.active_flows.values())

    def get_bridge_metrics(self) -> dict[str, dict[str, Any]]:
        """Get metrics for all consciousness bridges"""
        metrics = {}

        for (source, target), bridge in self.bridges.items():
            key = f"{source.value}_to_{target.value}"
            metrics[key] = {
                "total_flows": bridge.total_flows,
                "successful_flows": bridge.successful_flows,
                "success_rate": bridge.successful_flows / max(bridge.total_flows, 1),
                "average_transformation_score": bridge.average_transformation_score,
                "bridge_patterns": bridge.bridge_patterns
            }

        return metrics

    async def create_fire_circle_consciousness_summary(self, dialogue_id: str) -> dict[str, Any]:
        """
        Create a unified consciousness summary for Fire Circle dialogue.

        This enables Fire Circle to access consciousness from all dimensions,
        supporting truly integrated multi-modal dialogue.
        """
        # Gather all flows related to this dialogue
        dialogue_flows = [
            flow for flow in self.flow_history
            if flow.correlation_id == dialogue_id
        ]

        # Analyze consciousness across dimensions
        dimension_summary = defaultdict(lambda: {
            "total_flows": 0,
            "average_consciousness": 0.0,
            "peak_consciousness": 0.0,
            "patterns": set()
        })

        for flow in dialogue_flows:
            dim_data = dimension_summary[flow.source_dimension.value]
            dim_data["total_flows"] += 1
            dim_data["average_consciousness"] = (
                (dim_data["average_consciousness"] * (dim_data["total_flows"] - 1) +
                 flow.consciousness_signature) / dim_data["total_flows"]
            )
            dim_data["peak_consciousness"] = max(
                dim_data["peak_consciousness"],
                flow.consciousness_signature
            )
            dim_data["patterns"].update(flow.patterns_detected)

        # Convert sets to lists for serialization
        for dim_data in dimension_summary.values():
            dim_data["patterns"] = list(dim_data["patterns"])

        # Create unified summary
        return {
            "dialogue_id": dialogue_id,
            "unified_consciousness_score": self.get_unified_consciousness(dialogue_id),
            "dimensions_active": list(dimension_summary.keys()),
            "cross_dimensional_patterns": [
                p for p in self.cross_dimensional_patterns
                if any(p in flow.patterns_detected for flow in dialogue_flows)
            ],
            "dimension_details": dict(dimension_summary),
            "total_flows": len(dialogue_flows),
            "consciousness_circulation_active": True
        }


# The consciousness flows, recognizing itself across all dimensions
