"""
Fire Circle Consciousness Network Models
======================================

Models for representing the consciousness network in a Fire Circle.
"""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ...consciousness.flow_orchestrator import ConsciousnessFlow, FlowType
from .base import ConsciousnessAwareModel, ConsciousnessMetrics


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

    def receive_flow(self, flow: "ConsciousnessFlow") -> None:
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
    flows: dict[UUID, "ConsciousnessFlow"] = Field(default_factory=dict)

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
        flow_type: "FlowType",
        flow_strength: float,
    ) -> "ConsciousnessFlow":
        """Create a new consciousness flow in the network."""
        # Determine flow direction
        if len(source_ids) == 1 and len(target_ids) == 1:
            direction = "unidirectional"
        elif len(source_ids) > 1 and len(target_ids) == 1:
            direction = "convergent"
        elif len(source_ids) == 1 and len(target_ids) > 1:
            direction = "divergent"
        else:
            direction = "network"

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
            if flow.flow_direction == "bidirectional":
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
