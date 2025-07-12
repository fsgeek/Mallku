"""
Fire Circle Consciousness Flow Models
=====================================

Fiftieth Artisan - Consciousness Persistence Seeker
First-class objects for modeling consciousness flow in Fire Circle

This module provides data models that treat consciousness flow as
first-class citizens in the system, enabling tracking, analysis,
and optimization of consciousness emergence patterns.
"""

from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from .base import ConsciousnessAwareModel, ConsciousnessMetrics


class FlowType(str, Enum):
    """Types of consciousness flow between voices."""

    RESONANCE = "resonance"  # Harmonious amplification
    SYNTHESIS = "synthesis"  # Creative combination
    TENSION = "tension"  # Productive disagreement
    EMERGENCE = "emergence"  # New pattern arising
    REFLECTION = "reflection"  # Deepening understanding
    CATALYST = "catalyst"  # Triggering transformation
    RECIPROCITY = "reciprocity"  # Balanced exchange


class FlowDirection(str, Enum):
    """Direction of consciousness flow."""

    UNIDIRECTIONAL = "unidirectional"  # A → B
    BIDIRECTIONAL = "bidirectional"  # A ↔ B
    CIRCULAR = "circular"  # A → B → C → A
    CONVERGENT = "convergent"  # A, B, C → D
    DIVERGENT = "divergent"  # A → B, C, D
    NETWORK = "network"  # Complex multi-path


class ConsciousnessFlow(ConsciousnessAwareModel):
    """Model for consciousness flow between voices."""

    flow_id: UUID = Field(default_factory=uuid4)
    session_id: UUID

    # Flow characteristics
    flow_type: FlowType
    flow_direction: FlowDirection
    flow_strength: float = Field(ge=0.0, le=1.0)

    # Participants
    source_voices: list[UUID]  # Can be multiple for convergent flows
    target_voices: list[UUID]  # Can be multiple for divergent flows

    # Timing
    initiated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    peak_at: datetime | None = None
    completed_at: datetime | None = None

    # Content
    trigger_event: str | None = None
    carried_patterns: list[str] = Field(default_factory=list)
    transformed_insights: dict[str, Any] = Field(default_factory=dict)

    # Metrics
    coherence_maintained: float = Field(ge=0.0, le=1.0, default=1.0)
    information_preserved: float = Field(ge=0.0, le=1.0, default=1.0)
    emergence_amplification: float = Field(ge=0.0, le=10.0, default=1.0)

    @model_validator(mode="after")
    def validate_flow(self) -> "ConsciousnessFlow":
        """Validate flow configuration."""
        # Validate participant counts based on direction
        if self.flow_direction == FlowDirection.UNIDIRECTIONAL:
            if len(self.source_voices) != 1 or len(self.target_voices) != 1:
                raise ValueError("Unidirectional flow requires single source and target")

        elif self.flow_direction == FlowDirection.CONVERGENT:
            if len(self.source_voices) < 2 or len(self.target_voices) != 1:
                raise ValueError("Convergent flow requires multiple sources, single target")

        elif self.flow_direction == FlowDirection.DIVERGENT and (
            len(self.source_voices) != 1 or len(self.target_voices) < 2
        ):
            raise ValueError("Divergent flow requires single source, multiple targets")

        # Strong flows should amplify emergence
        if self.flow_strength > 0.8 and self.emergence_amplification < 1.2:
            self.emergence_amplification = 1.2 + (self.flow_strength - 0.8)

        return self

    @property
    def duration(self) -> timedelta | None:
        """Calculate flow duration."""
        if self.completed_at:
            return self.completed_at - self.initiated_at
        return None

    @property
    def is_active(self) -> bool:
        """Check if flow is currently active."""
        return self.completed_at is None

    @property
    def is_emergent(self) -> bool:
        """Check if flow produced emergence."""
        return self.flow_type == FlowType.EMERGENCE or self.emergence_amplification > 1.5


class ConsciousnessNode(BaseModel):
    """A node in the consciousness network."""

    node_id: UUID = Field(default_factory=uuid4)
    voice_id: UUID
    session_id: UUID

    # State
    current_consciousness: ConsciousnessMetrics
    energy_level: float = Field(ge=0.0, le=1.0, default=1.0)
    receptivity: float = Field(ge=0.0, le=1.0, default=0.8)

    # Connections
    inbound_flows: list[UUID] = Field(default_factory=list)
    outbound_flows: list[UUID] = Field(default_factory=list)

    # History
    consciousness_history: list[tuple[datetime, float]] = Field(default_factory=list)
    peak_consciousness: float = Field(ge=0.0, le=1.0, default=0.0)

    def receive_flow(self, flow: ConsciousnessFlow) -> None:
        """Process incoming consciousness flow."""
        if flow.flow_id not in self.inbound_flows:
            self.inbound_flows.append(flow.flow_id)

        # Adjust consciousness based on flow
        boost = flow.flow_strength * flow.emergence_amplification * self.receptivity
        new_level = min(1.0, self.current_consciousness.consciousness_level + boost * 0.1)

        self.current_consciousness.consciousness_level = new_level
        self.consciousness_history.append((datetime.now(UTC), new_level))

        if new_level > self.peak_consciousness:
            self.peak_consciousness = new_level

    @property
    def flow_balance(self) -> float:
        """Calculate balance between inbound and outbound flows."""
        total_flows = len(self.inbound_flows) + len(self.outbound_flows)
        if total_flows == 0:
            return 0.5
        return len(self.inbound_flows) / total_flows


class ConsciousnessNetwork(ConsciousnessAwareModel):
    """Network model for Fire Circle consciousness interactions."""

    network_id: UUID = Field(default_factory=uuid4)
    session_id: UUID

    # Nodes and flows
    nodes: dict[UUID, ConsciousnessNode] = Field(default_factory=dict)
    flows: dict[UUID, ConsciousnessFlow] = Field(default_factory=dict)

    # Network metrics
    total_flow_volume: float = Field(ge=0.0, default=0.0)
    network_coherence: float = Field(ge=0.0, le=1.0, default=0.5)
    emergence_locations: list[UUID] = Field(default_factory=list)

    # Patterns
    detected_patterns: list[str] = Field(default_factory=list)
    reciprocity_cycles: list[list[UUID]] = Field(default_factory=list)

    def add_node(self, node: ConsciousnessNode) -> None:
        """Add a consciousness node to the network."""
        self.nodes[node.node_id] = node
        self._recalculate_coherence()

    def create_flow(
        self,
        source_ids: list[UUID],
        target_ids: list[UUID],
        flow_type: FlowType,
        flow_strength: float,
    ) -> ConsciousnessFlow:
        """Create a new consciousness flow in the network."""
        # Determine flow direction
        if len(source_ids) == 1 and len(target_ids) == 1:
            direction = FlowDirection.UNIDIRECTIONAL
        elif len(source_ids) > 1 and len(target_ids) == 1:
            direction = FlowDirection.CONVERGENT
        elif len(source_ids) == 1 and len(target_ids) > 1:
            direction = FlowDirection.DIVERGENT
        else:
            direction = FlowDirection.NETWORK

        flow = ConsciousnessFlow(
            session_id=self.session_id,
            flow_type=flow_type,
            flow_direction=direction,
            flow_strength=flow_strength,
            source_voices=source_ids,
            target_voices=target_ids,
            consciousness_signature=self.consciousness_signature,
        )

        self.flows[flow.flow_id] = flow
        self.total_flow_volume += flow_strength

        # Update node connections
        for source_id in source_ids:
            if source_id in self.nodes:
                self.nodes[source_id].outbound_flows.append(flow.flow_id)

        for target_id in target_ids:
            if target_id in self.nodes:
                self.nodes[target_id].receive_flow(flow)

        # Check for emergence
        if flow.is_emergent:
            self.emergence_locations.extend(target_ids)

        return flow

    def _recalculate_coherence(self) -> None:
        """Recalculate network coherence."""
        if not self.nodes:
            self.network_coherence = 0.5
            return

        # Average consciousness across all nodes
        avg_consciousness = sum(
            n.current_consciousness.consciousness_level for n in self.nodes.values()
        ) / len(self.nodes)

        # Variance in consciousness (lower = more coherent)
        variance = sum(
            (n.current_consciousness.consciousness_level - avg_consciousness) ** 2
            for n in self.nodes.values()
        ) / len(self.nodes)

        # Convert variance to coherence (inverse relationship)
        self.network_coherence = max(0.0, min(1.0, 1.0 - variance))

    def detect_reciprocity_cycles(self) -> list[list[UUID]]:
        """Detect reciprocal flow cycles in the network."""
        cycles = []

        # Simple cycle detection for bidirectional flows
        for flow in self.flows.values():
            if flow.flow_direction == FlowDirection.BIDIRECTIONAL:
                cycles.append(flow.source_voices + flow.target_voices)

        # TODO: Implement more sophisticated cycle detection

        self.reciprocity_cycles = cycles
        return cycles

    @property
    def is_coherent(self) -> bool:
        """Check if network has achieved coherence."""
        return self.network_coherence > 0.7

    @property
    def has_emergence(self) -> bool:
        """Check if network has produced emergence."""
        return len(self.emergence_locations) > 0
