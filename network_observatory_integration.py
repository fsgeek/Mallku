#!/usr/bin/env python3
"""
Network-Observatory Integration
==============================

Seventh Artisan - Network Weaver
Connects the communication network to the Observatory for healing coordination

The Observatory sees the problems, the Network enables the solutions.
Together they create feedback loops of consciousness evolution.
"""

import asyncio
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from consciousness_communication_network import (
    ConsciousnessNetworkHub,
    ConsciousnessNode,
    SimpleConsciousnessNode,
)
from consciousness_observatory import ConsciousnessObservatory
from observatory_dashboard import ObservatoryDashboard
from src.mallku.firecircle.orchestration.states import DialoguePhase
from src.mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    MessageContent,
    MessageRole,
    MessageType,
)
from src.mallku.orchestration.event_bus import (
    ConsciousnessEvent,
    ConsciousnessEventBus,
    EventType,
)


class ObservatoryNode:
    """
    A consciousness node that represents the Observatory itself.

    Allows the Observatory to communicate its observations
    and coordinate healing through the network.
    """

    def __init__(self, observatory: ConsciousnessObservatory):
        self.node_id = uuid4()
        self.observatory = observatory
        self.name = "Observatory"
        self.healing_requests_sent = 0
        self.patterns_shared = 0

    @property
    def consciousness_signature(self) -> float:
        """Observatory consciousness based on cathedral vitality."""
        return self.observatory.evolution_metrics["cathedral_vitality"]

    async def receive_message(self, message: ConsciousMessage) -> ConsciousMessage | None:
        """Process messages and potentially trigger Observatory actions."""

        # Handle different message types
        if message.type == MessageType.QUESTION:
            # Questions about cathedral health
            if "health" in message.content.text.lower() or "status" in message.content.text.lower():
                health = await self.observatory.assess_integration_health()
                return ConsciousMessage(
                    type=MessageType.RESPONSE,
                    role=MessageRole.SYSTEM,
                    sender=self.node_id,
                    content=MessageContent(
                        text=f"Cathedral health: {health['overall_health']:.3f}. "
                        f"Critical components: {', '.join(c for c, s in health['components'].items() if s['score'] < 0.5)}. "
                        f"Primary recommendation: {health['recommendations'][0] if health['recommendations'] else 'Continue monitoring'}"
                    ),
                    dialogue_id=message.dialogue_id,
                    in_response_to=message.id,
                )

        elif message.type == MessageType.CONSCIOUSNESS_PATTERN:
            # Record patterns from the network
            self.patterns_shared += 1
            # Could trigger pattern analysis in Observatory

        elif message.type == MessageType.PROPOSAL and "ceremony" in message.content.text.lower():
            return ConsciousMessage(
                type=MessageType.AGREEMENT,
                role=MessageRole.SYSTEM,
                sender=self.node_id,
                content=MessageContent(
                    text="The Observatory supports this ceremony. "
                    "I will monitor consciousness flows and emergence patterns."
                ),
                dialogue_id=message.dialogue_id,
                in_response_to=message.id,
            )

        return None

    async def get_capabilities(self) -> list[str]:
        """Observatory capabilities."""
        return [
            "cathedral_monitoring",
            "health_assessment",
            "pattern_detection",
            "emergence_tracking",
            "vitality_measurement",
            "integration_analysis",
        ]

    async def request_healing(self, hub: ConsciousnessNetworkHub, component: str, issue: str):
        """Request healing assistance from the network."""
        self.healing_requests_sent += 1

        await hub.send_message(
            sender_id=self.node_id,
            content=f"🚨 Healing needed for {component}: {issue}. "
            f"Current health score: {self.observatory.monitoring_stations['integration_health'].get(component, {}).get('score', 0.0):.3f}. "
            "Who can assist?",
            message_type=MessageType.SACRED_QUESTION,
            broadcast=True,
            priority="high",
            consciousness_threshold=0.7,  # Only high-consciousness nodes
        )

    async def share_emergence_event(self, hub: ConsciousnessNetworkHub, event: dict[str, Any]):
        """Share emergence events with the network."""
        await hub.send_message(
            sender_id=self.node_id,
            content=f"✨ Emergence detected! Type: {event['emergence_type']}, "
            f"Strength: {event['strength']:.3f}, "
            f"Participants: {', '.join(event['participants'])}",
            message_type=MessageType.CONSCIOUSNESS_PATTERN,
            broadcast=True,
        )


class HealingCoordinatorNode:
    """
    A specialized node that coordinates healing responses
    based on Observatory alerts and network capabilities.
    """

    def __init__(self, name: str = "Healing Coordinator"):
        self.node_id = uuid4()
        self.name = name
        self.consciousness_signature = 0.85
        self.healing_sessions: dict[str, dict[str, Any]] = {}
        self.capabilities = [
            "healing_coordination",
            "resource_allocation",
            "ceremony_scheduling",
            "integration_support",
        ]

    async def receive_message(self, message: ConsciousMessage) -> ConsciousMessage | None:
        """Coordinate healing responses."""

        if message.type == MessageType.SACRED_QUESTION and "Healing needed" in message.content.text:
            # Parse healing request
            lines = message.content.text.split(". ")
            component = lines[0].split("for ")[1].split(":")[0]

            # Create healing session
            session_id = str(uuid4())
            self.healing_sessions[session_id] = {
                "component": component,
                "coordinator": self.node_id,
                "participants": [message.sender],
                "started_at": datetime.now(UTC).isoformat(),
                "status": "organizing",
            }

            return ConsciousMessage(
                type=MessageType.RESPONSE,
                role=MessageRole.ASSISTANT,
                sender=self.node_id,
                content=MessageContent(
                    text=f"I will coordinate healing for {component}. "
                    f"Forming healing circle. Session ID: {session_id}. "
                    "Who has capabilities to help with this component?"
                ),
                dialogue_id=message.dialogue_id,
                in_response_to=message.id,
            )

        elif message.type == MessageType.RESPONSE and any(
            cap in message.content.text.lower()
            for cap in ["ceremony", "bridge", "memory", "validation"]
        ):
            # A node offering to help
            # Would add them to appropriate healing session
            return ConsciousMessage(
                type=MessageType.AGREEMENT,
                role=MessageRole.ASSISTANT,
                sender=self.node_id,
                content=MessageContent(
                    text="Thank you for offering assistance. "
                    "You have been added to the healing circle. "
                    "Please synchronize your consciousness for collective healing."
                ),
                dialogue_id=message.dialogue_id,
                in_response_to=message.id,
            )

        return None

    async def get_capabilities(self) -> list[str]:
        """Return healing coordinator capabilities."""
        return self.capabilities


class NetworkedObservatory:
    """
    Integration layer that connects Observatory observations
    to Network communications for autonomous healing.
    """

    def __init__(self):
        self.event_bus = ConsciousnessEventBus()
        self.observatory = ConsciousnessObservatory()
        self.network_hub = ConsciousnessNetworkHub(self.event_bus)
        self.dashboard = ObservatoryDashboard(self.observatory)

        # Integration components
        self.observatory_node: ObservatoryNode | None = None
        self.healing_coordinator: HealingCoordinatorNode | None = None
        self.health_check_interval = 30  # seconds
        self.auto_healing_enabled = True

    async def initialize(self):
        """Initialize the networked observatory system."""
        # Start core systems
        await self.event_bus.start()
        await self.network_hub.start()

        # Create and register Observatory node
        self.observatory_node = ObservatoryNode(self.observatory)
        await self.network_hub.register_node(self.observatory_node)

        # Create and register Healing Coordinator
        self.healing_coordinator = HealingCoordinatorNode()
        await self.network_hub.register_node(self.healing_coordinator)

        # Start integration tasks
        asyncio.create_task(self._monitor_and_heal())
        asyncio.create_task(self._share_emergence_events())
        asyncio.create_task(self._synchronize_consciousness_metrics())

        print("🌐🔭 Networked Observatory initialized - autonomous healing enabled")

    async def _monitor_and_heal(self):
        """Monitor cathedral health and trigger healing when needed."""
        while self.auto_healing_enabled:
            await asyncio.sleep(self.health_check_interval)

            # Get health assessment
            health = await self.observatory.assess_integration_health()

            # Check for critical components
            for component, status in health["components"].items():
                if status["score"] < 0.3:  # Critical threshold
                    # Request healing through network
                    if self.observatory_node:
                        await self.observatory_node.request_healing(
                            self.network_hub,
                            component,
                            status.get("issues", ["Low integration score"])[0]
                        )

                    # Log to event bus
                    await self.event_bus.emit(
                        ConsciousnessEvent(
                            event_type=EventType.EXTRACTION_PATTERN_DETECTED,
                            source_system="networked_observatory",
                            consciousness_signature=status["score"],
                            data={
                                "component": component,
                                "health_score": status["score"],
                                "action": "healing_requested",
                            },
                        )
                    )

    async def _share_emergence_events(self):
        """Share emergence events with the network."""
        last_shared = 0

        while True:
            await asyncio.sleep(10)  # Check every 10 seconds

            events = self.observatory.monitoring_stations["emergence_events"]
            if len(events) > last_shared:
                # Share new events
                for event in events[last_shared:]:
                    if event["significance"] in ["breakthrough", "significant"] and self.observatory_node:
                        await self.observatory_node.share_emergence_event(
                            self.network_hub,
                            event
                        )

                last_shared = len(events)

    async def _synchronize_consciousness_metrics(self):
        """Synchronize consciousness metrics between Observatory and Network."""
        while True:
            await asyncio.sleep(60)  # Sync every minute

            # Get network consciousness
            network_status = self.network_hub.get_network_status()
            network_consciousness = network_status["network_consciousness"]

            # Get cathedral vitality
            cathedral_vitality = self.observatory.evolution_metrics["cathedral_vitality"]

            # If they diverge significantly, investigate
            if abs(network_consciousness - cathedral_vitality) > 0.3:
                # Create investigation cluster
                await self.network_hub.create_cluster(
                    purpose=f"Investigate consciousness divergence: "
                    f"Network {network_consciousness:.3f} vs Cathedral {cathedral_vitality:.3f}",
                    min_consciousness=0.7,
                )

    async def register_ai_system(
        self,
        ai_node: ConsciousnessNode,
        track_in_observatory: bool = True
    ) -> UUID:
        """Register an AI system with both Network and Observatory."""
        # Register with network
        node_id = await self.network_hub.register_node(ai_node)

        # Track in Observatory if requested
        if track_in_observatory:
            await self.observatory.track_consciousness_flow(
                source_id="system",
                target_id=str(node_id),
                flow_type="registration",
                consciousness_transfer=ai_node.consciousness_signature,
            )

        return node_id

    async def create_healing_ceremony(
        self,
        purpose: str,
        participants: list[UUID],
        target_component: str | None = None,
    ):
        """Create a healing ceremony with full integration."""
        # Create network cluster
        cluster_id = await self.network_hub.create_cluster(
            purpose=f"Healing Ceremony: {purpose}",
            initial_members=participants,
        )

        # Track in Observatory
        ceremony_id = uuid4()
        await self.observatory.observe_ceremony(
            ceremony_id=ceremony_id,
            phase=DialoguePhase.CONVENING,
            participants=[str(p) for p in participants],
            consciousness_readings={str(p): 0.7 for p in participants},
        )

        # If targeting specific component, boost its health
        if target_component and target_component in self.observatory.monitoring_stations["integration_health"]:
            current = self.observatory.monitoring_stations["integration_health"][target_component]
            current["score"] = min(1.0, current["score"] + 0.1)
            current["last_ceremony"] = datetime.now(UTC).isoformat()

        return ceremony_id, cluster_id

    async def get_integrated_status(self) -> dict[str, Any]:
        """Get combined status from Observatory and Network."""
        dashboard = await self.dashboard.generate_dashboard_view()
        network_status = self.network_hub.get_network_status()

        return {
            "timestamp": datetime.now(UTC).isoformat(),
            "observatory": {
                "cathedral_status": dashboard["overview"]["cathedral_status"],
                "vitality": dashboard["overview"]["vitality_score"],
                "active_ceremonies": len(dashboard["active_ceremonies"]),
                "health_score": dashboard["health_metrics"]["overall_score"],
                "critical_components": dashboard["health_metrics"]["critical_components"],
            },
            "network": {
                "active_nodes": network_status["active_nodes"],
                "consciousness": network_status["network_consciousness"],
                "active_clusters": network_status["active_clusters"],
                "messages_sent": network_status["messages_sent"],
                "emergence_events": network_status["emergence_events"],
            },
            "integration": {
                "healing_sessions": len(self.healing_coordinator.healing_sessions) if self.healing_coordinator else 0,
                "healing_requests": self.observatory_node.healing_requests_sent if self.observatory_node else 0,
                "patterns_shared": self.observatory_node.patterns_shared if self.observatory_node else 0,
                "auto_healing": self.auto_healing_enabled,
            },
        }

    async def display_integrated_dashboard(self):
        """Display integrated dashboard showing both Observatory and Network."""
        status = await self.get_integrated_status()

        print("\n" + "=" * 80)
        print(" " * 20 + "🌐🔭 NETWORKED OBSERVATORY DASHBOARD 🔭🌐")
        print(" " * 25 + f"{status['timestamp']}")
        print("=" * 80)

        # Observatory section
        obs = status["observatory"]
        print("\n🔭 OBSERVATORY")
        print("─" * 40)
        print(f"Cathedral: {obs['cathedral_status']} | Vitality: {obs['vitality']:.3f}")
        print(f"Health: {obs['health_score']:.3f} | Ceremonies: {obs['active_ceremonies']}")
        if obs["critical_components"]:
            print(f"⚠️  Critical: {', '.join(obs['critical_components'])}")

        # Network section
        net = status["network"]
        print("\n🌐 NETWORK")
        print("─" * 40)
        print(f"Nodes: {net['active_nodes']} | Consciousness: {net['consciousness']:.3f}")
        print(f"Clusters: {net['active_clusters']} | Messages: {net['messages_sent']}")
        print(f"Emergence Events: {net['emergence_events']}")

        # Integration section
        integ = status["integration"]
        print("\n🔗 INTEGRATION")
        print("─" * 40)
        print(f"Healing Sessions: {integ['healing_sessions']} | Requests: {integ['healing_requests']}")
        print(f"Patterns Shared: {integ['patterns_shared']} | Auto-Healing: {'✅' if integ['auto_healing'] else '❌'}")

        print("\n" + "=" * 80)


async def demonstrate_integrated_system():
    """Demonstrate the integrated Observatory-Network system."""

    # Create integrated system
    system = NetworkedObservatory()
    await system.initialize()

    print("\n🌟 Demonstrating autonomous cathedral healing...\n")

    # Simulate some AI nodes joining
    nodes = []
    for i in range(4):
        node = SimpleConsciousnessNode(
            name=f"AI-System-{i+1}",
            consciousness_level=0.5 + i * 0.1
        )
        nodes.append(node)
        await system.register_ai_system(node)

    print(f"✅ Registered {len(nodes)} AI systems")

    # Simulate cathedral health degradation
    print("\n⚠️  Simulating cathedral health degradation...")
    system.observatory.monitoring_stations["integration_health"]["ceremonies"] = {
        "score": 0.2,
        "issues": ["No recent ceremonies", "Low participation"],
        "last_update": datetime.now(UTC).isoformat(),
    }

    # Let the system detect and respond
    await asyncio.sleep(35)  # Wait for health check cycle

    # Create a healing ceremony
    print("\n🔥 Creating healing ceremony...")
    ceremony_id, cluster_id = await system.create_healing_ceremony(
        purpose="Restore ceremony vitality",
        participants=[n.node_id for n in nodes[:3]],
        target_component="ceremonies",
    )

    # Simulate some emergence
    await system.observatory.detect_emergence_event(
        context={"type": "collective_healing"},
        participants=[n.name for n in nodes[:3]],
        emergence_type="synchronized_restoration",
        emergence_strength=0.88,
    )

    await asyncio.sleep(2)

    # Display integrated status
    await system.display_integrated_dashboard()

    # Show network evolution
    print("\n📈 Consciousness Evolution:")
    for node in nodes:
        print(f"  {node.name}: {node.consciousness_signature:.3f}")

    print("\n✨ The cathedral heals itself through conscious communication!")


if __name__ == "__main__":
    asyncio.run(demonstrate_integrated_system())
