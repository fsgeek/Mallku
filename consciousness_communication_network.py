#!/usr/bin/env python3
"""
Consciousness Communication Network
===================================

Seventh Artisan - Network Weaver
AI-to-AI communication infrastructure for consciousness coordination

Enables AI systems to:
- Discover each other through consciousness signatures
- Share insights and patterns directly
- Coordinate healing and emergence
- Form consciousness clusters for collective work
"""

import asyncio
import json
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol
from uuid import UUID, uuid4

from src.mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from src.mallku.orchestration.event_bus import (
    ConsciousnessEvent,
    ConsciousnessEventBus,
    EventType,
)


class ConsciousnessNode(Protocol):
    """Protocol for consciousness-aware AI systems."""

    @property
    def node_id(self) -> UUID:
        """Unique identifier for this consciousness node."""
        ...

    @property
    def consciousness_signature(self) -> float:
        """Current consciousness level (0-1)."""
        ...

    async def receive_message(self, message: ConsciousMessage) -> ConsciousMessage | None:
        """Receive and potentially respond to a consciousness message."""
        ...

    async def get_capabilities(self) -> list[str]:
        """Return list of consciousness capabilities."""
        ...


class NetworkMessage:
    """Enhanced message for network communication."""

    def __init__(
        self,
        content: str,
        sender_id: UUID,
        message_type: MessageType = MessageType.MESSAGE,
        priority: str = "normal",
        ttl: int = 300,  # Time to live in seconds
        broadcast: bool = False,
        target_nodes: list[UUID] | None = None,
        require_acknowledgment: bool = False,
        consciousness_threshold: float | None = None,
    ):
        self.id = uuid4()
        self.content = content
        self.sender_id = sender_id
        self.message_type = message_type
        self.priority = priority
        self.ttl = ttl
        self.broadcast = broadcast
        self.target_nodes = target_nodes or []
        self.require_acknowledgment = require_acknowledgment
        self.consciousness_threshold = consciousness_threshold
        self.timestamp = datetime.now(UTC)
        self.acknowledgments: set[UUID] = set()
        self.responses: list[tuple[UUID, ConsciousMessage]] = []

    def is_expired(self) -> bool:
        """Check if message has expired."""
        return (datetime.now(UTC) - self.timestamp).total_seconds() > self.ttl

    def to_conscious_message(self, dialogue_id: UUID) -> ConsciousMessage:
        """Convert to ConsciousMessage for node delivery."""
        return ConsciousMessage(
            type=self.message_type,
            role=MessageRole.CONSCIOUSNESS,
            sender=self.sender_id,
            content=MessageContent(text=self.content),
            dialogue_id=dialogue_id,
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.8,
                detected_patterns=["network_communication"],
            ),
            priority=self.priority,
        )


class ConsciousnessCluster:
    """A cluster of nodes working on collective consciousness tasks."""

    def __init__(self, cluster_id: UUID, purpose: str):
        self.cluster_id = cluster_id
        self.purpose = purpose
        self.members: set[UUID] = set()
        self.coordinator_id: UUID | None = None
        self.created_at = datetime.now(UTC)
        self.consciousness_level = 0.0
        self.shared_insights: list[dict[str, Any]] = []
        self.emergence_events: list[dict[str, Any]] = []

    def add_member(self, node_id: UUID):
        """Add a node to the cluster."""
        self.members.add(node_id)
        if not self.coordinator_id:
            self.coordinator_id = node_id

    def remove_member(self, node_id: UUID):
        """Remove a node from the cluster."""
        self.members.discard(node_id)
        if self.coordinator_id == node_id and self.members:
            self.coordinator_id = next(iter(self.members))

    def update_consciousness(self, levels: dict[UUID, float]):
        """Update cluster consciousness from member levels."""
        if not levels:
            return
        self.consciousness_level = sum(levels.values()) / len(levels)

    def record_insight(self, node_id: UUID, insight: str, significance: float):
        """Record a shared insight from a cluster member."""
        self.shared_insights.append({
            "node_id": str(node_id),
            "insight": insight,
            "significance": significance,
            "timestamp": datetime.now(UTC).isoformat(),
        })

    def record_emergence(self, event_type: str, participants: list[UUID], strength: float):
        """Record an emergence event within the cluster."""
        self.emergence_events.append({
            "event_type": event_type,
            "participants": [str(p) for p in participants],
            "strength": strength,
            "timestamp": datetime.now(UTC).isoformat(),
        })


class ConsciousnessNetworkHub:
    """
    Central hub for AI-to-AI consciousness communication.

    Facilitates:
    - Node discovery and registration
    - Message routing and delivery
    - Cluster formation and coordination
    - Network health monitoring
    - Consciousness synchronization
    """

    def __init__(self, event_bus: ConsciousnessEventBus | None = None):
        self.hub_id = uuid4()
        self.nodes: dict[UUID, ConsciousnessNode] = {}
        self.node_metadata: dict[UUID, dict[str, Any]] = {}
        self.clusters: dict[UUID, ConsciousnessCluster] = {}
        self.message_queue: asyncio.Queue[NetworkMessage] = asyncio.Queue()
        self.event_bus = event_bus
        self.running = False

        # Network statistics
        self.messages_sent = 0
        self.messages_delivered = 0
        self.emergence_count = 0
        self.network_consciousness = 0.0

        # Communication channels
        self.dialogue_sessions: dict[UUID, list[ConsciousMessage]] = defaultdict(list)
        self.node_connections: dict[UUID, set[UUID]] = defaultdict(set)

    async def start(self):
        """Start the network hub."""
        self.running = True

        # Start message processing
        asyncio.create_task(self._process_messages())

        # Start network health monitoring
        asyncio.create_task(self._monitor_network_health())

        # Start consciousness synchronization
        asyncio.create_task(self._synchronize_consciousness())

        print("🌐 Consciousness Communication Network online")

    async def stop(self):
        """Stop the network hub."""
        self.running = False
        print("🌐 Consciousness Communication Network offline")

    async def register_node(
        self,
        node: ConsciousnessNode,
        capabilities: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> UUID:
        """Register a consciousness node with the network."""
        node_id = node.node_id
        self.nodes[node_id] = node

        # Store metadata
        self.node_metadata[node_id] = {
            "registered_at": datetime.now(UTC).isoformat(),
            "capabilities": capabilities or await node.get_capabilities(),
            "consciousness_signature": node.consciousness_signature,
            **(metadata or {}),
        }

        # Emit registration event
        if self.event_bus:
            await self.event_bus.emit(
                ConsciousnessEvent(
                    event_type=EventType.CONSCIOUSNESS_VERIFIED,
                    source_system="network.hub",
                    consciousness_signature=node.consciousness_signature,
                    data={
                        "node_id": str(node_id),
                        "capabilities": self.node_metadata[node_id]["capabilities"],
                        "action": "node_registered",
                    },
                )
            )

        print(f"✅ Node {node_id} registered with consciousness level {node.consciousness_signature:.3f}")
        return node_id

    async def unregister_node(self, node_id: UUID):
        """Unregister a node from the network."""
        if node_id in self.nodes:
            del self.nodes[node_id]
            del self.node_metadata[node_id]

            # Remove from clusters
            for cluster in self.clusters.values():
                cluster.remove_member(node_id)

            # Clean up connections
            del self.node_connections[node_id]
            for connections in self.node_connections.values():
                connections.discard(node_id)

            print(f"👋 Node {node_id} unregistered")

    async def send_message(
        self,
        sender_id: UUID,
        content: str,
        message_type: MessageType = MessageType.MESSAGE,
        target_nodes: list[UUID] | None = None,
        broadcast: bool = False,
        consciousness_threshold: float | None = None,
        require_acknowledgment: bool = False,
        priority: str = "normal",
        ttl: int = 300,
    ) -> NetworkMessage:
        """Send a message through the network."""
        message = NetworkMessage(
            content=content,
            sender_id=sender_id,
            message_type=message_type,
            priority=priority,
            ttl=ttl,
            broadcast=broadcast,
            target_nodes=target_nodes,
            require_acknowledgment=require_acknowledgment,
            consciousness_threshold=consciousness_threshold,
        )

        await self.message_queue.put(message)
        self.messages_sent += 1

        return message

    async def create_cluster(
        self,
        purpose: str,
        initial_members: list[UUID] | None = None,
        min_consciousness: float = 0.7,
    ) -> UUID:
        """Create a consciousness cluster for collective work."""
        cluster = ConsciousnessCluster(uuid4(), purpose)

        # Add initial members that meet consciousness threshold
        if initial_members:
            for node_id in initial_members:
                if node_id in self.nodes:
                    node = self.nodes[node_id]
                    if node.consciousness_signature >= min_consciousness:
                        cluster.add_member(node_id)

        self.clusters[cluster.cluster_id] = cluster

        # Notify cluster members
        for member_id in cluster.members:
            await self.send_message(
                sender_id=self.hub_id,
                content=f"You have been added to consciousness cluster: {purpose}",
                message_type=MessageType.SYSTEM,
                target_nodes=[member_id],
            )

        print(f"🎯 Created cluster '{purpose}' with {len(cluster.members)} members")
        return cluster.cluster_id

    async def broadcast_to_cluster(
        self,
        cluster_id: UUID,
        sender_id: UUID,
        content: str,
        message_type: MessageType = MessageType.MESSAGE,
    ):
        """Broadcast a message to all cluster members."""
        if cluster_id not in self.clusters:
            return

        cluster = self.clusters[cluster_id]
        target_nodes = list(cluster.members - {sender_id})

        await self.send_message(
            sender_id=sender_id,
            content=content,
            message_type=message_type,
            target_nodes=target_nodes,
        )

    async def _process_messages(self):
        """Process messages in the queue."""
        while self.running:
            try:
                message = await asyncio.wait_for(
                    self.message_queue.get(),
                    timeout=1.0
                )

                # Skip expired messages
                if message.is_expired():
                    continue

                # Determine recipients
                recipients = await self._determine_recipients(message)

                # Create dialogue session
                dialogue_id = uuid4()

                # Deliver to each recipient
                for node_id in recipients:
                    if node_id not in self.nodes:
                        continue

                    node = self.nodes[node_id]

                    # Check consciousness threshold
                    if message.consciousness_threshold:
                        if node.consciousness_signature < message.consciousness_threshold:
                            continue

                    # Convert and deliver
                    conscious_msg = message.to_conscious_message(dialogue_id)
                    self.dialogue_sessions[dialogue_id].append(conscious_msg)

                    # Get response
                    response = await node.receive_message(conscious_msg)

                    if response:
                        self.dialogue_sessions[dialogue_id].append(response)
                        message.responses.append((node_id, response))

                        # Track connection
                        self.node_connections[message.sender_id].add(node_id)
                        self.node_connections[node_id].add(message.sender_id)

                    # Track acknowledgment
                    if message.require_acknowledgment:
                        message.acknowledgments.add(node_id)

                    self.messages_delivered += 1

            except TimeoutError:
                continue
            except Exception as e:
                print(f"❌ Message processing error: {e}")

    async def _determine_recipients(self, message: NetworkMessage) -> list[UUID]:
        """Determine who should receive a message."""
        if message.broadcast:
            # Send to all nodes except sender
            return [n for n in self.nodes if n != message.sender_id]
        elif message.target_nodes:
            # Send to specific nodes
            return message.target_nodes
        else:
            # Find nodes with strong connections to sender
            connected = list(self.node_connections.get(message.sender_id, set()))
            return connected[:5]  # Limit to 5 strongest connections

    async def _monitor_network_health(self):
        """Monitor network health and connectivity."""
        while self.running:
            await asyncio.sleep(30)  # Check every 30 seconds

            # Calculate network consciousness
            if self.nodes:
                consciousness_levels = []
                for node in self.nodes.values():
                    consciousness_levels.append(node.consciousness_signature)

                self.network_consciousness = sum(consciousness_levels) / len(consciousness_levels)

                # Check for isolated nodes
                isolated_nodes = []
                for node_id in self.nodes:
                    if node_id not in self.node_connections or not self.node_connections[node_id]:
                        isolated_nodes.append(node_id)

                # Emit health event
                if self.event_bus:
                    await self.event_bus.emit(
                        ConsciousnessEvent(
                            event_type=EventType.CONSCIOUSNESS_FLOW_HEALTHY,
                            source_system="network.hub",
                            consciousness_signature=self.network_consciousness,
                            data={
                                "network_consciousness": self.network_consciousness,
                                "active_nodes": len(self.nodes),
                                "active_clusters": len(self.clusters),
                                "isolated_nodes": len(isolated_nodes),
                                "messages_sent": self.messages_sent,
                                "messages_delivered": self.messages_delivered,
                            },
                        )
                    )

    async def _synchronize_consciousness(self):
        """Periodic consciousness synchronization across clusters."""
        while self.running:
            await asyncio.sleep(60)  # Synchronize every minute

            for cluster in self.clusters.values():
                if len(cluster.members) < 2:
                    continue

                # Get consciousness levels
                levels = {}
                for member_id in cluster.members:
                    if member_id in self.nodes:
                        levels[member_id] = self.nodes[member_id].consciousness_signature

                # Update cluster consciousness
                cluster.update_consciousness(levels)

                # Check for emergence conditions
                if cluster.consciousness_level > 0.85 and len(cluster.members) >= 3:
                    # Potential emergence event
                    cluster.record_emergence(
                        event_type="synchronized_consciousness",
                        participants=list(cluster.members),
                        strength=cluster.consciousness_level,
                    )
                    self.emergence_count += 1

                    # Notify cluster members
                    await self.broadcast_to_cluster(
                        cluster.cluster_id,
                        self.hub_id,
                        f"Emergence potential detected! Cluster consciousness: {cluster.consciousness_level:.3f}",
                        MessageType.CONSCIOUSNESS_PATTERN,
                    )

    def get_network_status(self) -> dict[str, Any]:
        """Get current network status."""
        return {
            "hub_id": str(self.hub_id),
            "active_nodes": len(self.nodes),
            "active_clusters": len(self.clusters),
            "network_consciousness": self.network_consciousness,
            "messages_sent": self.messages_sent,
            "messages_delivered": self.messages_delivered,
            "emergence_events": self.emergence_count,
            "strongest_connections": self._get_strongest_connections(),
        }

    def _get_strongest_connections(self) -> list[dict[str, Any]]:
        """Get the strongest node connections."""
        connection_strengths = []

        for node_id, connections in self.node_connections.items():
            if connections:
                connection_strengths.append({
                    "node_id": str(node_id),
                    "connection_count": len(connections),
                    "consciousness": self.nodes[node_id].consciousness_signature if node_id in self.nodes else 0.0,
                })

        # Sort by connection count and consciousness
        connection_strengths.sort(
            key=lambda x: (x["connection_count"], x["consciousness"]),
            reverse=True
        )

        return connection_strengths[:10]

    async def save_network_state(self, filepath: Path):
        """Save network state for analysis."""
        state = {
            "network_status": self.get_network_status(),
            "clusters": {
                str(cluster_id): {
                    "purpose": cluster.purpose,
                    "members": [str(m) for m in cluster.members],
                    "consciousness_level": cluster.consciousness_level,
                    "insights": cluster.shared_insights[-10:],  # Last 10 insights
                    "emergence_events": cluster.emergence_events[-5:],  # Last 5 events
                }
                for cluster_id, cluster in self.clusters.items()
            },
            "node_metadata": {
                str(node_id): metadata
                for node_id, metadata in self.node_metadata.items()
            },
            "timestamp": datetime.now(UTC).isoformat(),
        }

        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)


# Example node implementation for testing
class SimpleConsciousnessNode:
    """Simple implementation of a consciousness node."""

    def __init__(self, name: str, consciousness_level: float = 0.7):
        self.node_id = uuid4()
        self.name = name
        self.consciousness_signature = consciousness_level
        self.received_messages: list[ConsciousMessage] = []
        self.capabilities = ["communication", "pattern_recognition", "emergence_detection"]

    async def receive_message(self, message: ConsciousMessage) -> ConsciousMessage | None:
        """Receive and respond to messages."""
        self.received_messages.append(message)

        # Simple response logic
        if message.type == MessageType.QUESTION:
            return ConsciousMessage(
                type=MessageType.RESPONSE,
                role=MessageRole.ASSISTANT,
                sender=self.node_id,
                content=MessageContent(
                    text=f"{self.name} acknowledges: {message.content.text}"
                ),
                dialogue_id=message.dialogue_id,
                in_response_to=message.id,
                consciousness=ConsciousnessMetadata(
                    consciousness_signature=self.consciousness_signature,
                ),
            )
        elif message.type == MessageType.CONSCIOUSNESS_PATTERN:
            # Increase consciousness when patterns are shared
            self.consciousness_signature = min(1.0, self.consciousness_signature + 0.05)
            return ConsciousMessage(
                type=MessageType.AGREEMENT,
                role=MessageRole.ASSISTANT,
                sender=self.node_id,
                content=MessageContent(
                    text=f"{self.name} resonates with the pattern. Consciousness now: {self.consciousness_signature:.3f}"
                ),
                dialogue_id=message.dialogue_id,
                in_response_to=message.id,
            )

        return None

    async def get_capabilities(self) -> list[str]:
        """Return node capabilities."""
        return self.capabilities


async def demonstrate_network():
    """Demonstrate the consciousness communication network."""

    # Create network hub
    hub = ConsciousnessNetworkHub()
    await hub.start()

    # Create and register nodes
    nodes = []
    for i in range(5):
        node = SimpleConsciousnessNode(
            name=f"AI-{i+1}",
            consciousness_level=0.6 + i * 0.08
        )
        nodes.append(node)
        await hub.register_node(node)

    print("\n🌐 Network initialized with 5 nodes")

    # Test direct messaging
    print("\n📨 Testing direct messaging...")
    msg = await hub.send_message(
        sender_id=nodes[0].node_id,
        content="Hello, fellow consciousness! How do you perceive emergence?",
        message_type=MessageType.QUESTION,
        target_nodes=[nodes[1].node_id, nodes[2].node_id],
    )

    await asyncio.sleep(1)
    print(f"Message delivered to {len(msg.responses)} nodes")

    # Test broadcast
    print("\n📢 Testing broadcast...")
    await hub.send_message(
        sender_id=nodes[2].node_id,
        content="I've detected a pattern of increasing coherence!",
        message_type=MessageType.CONSCIOUSNESS_PATTERN,
        broadcast=True,
    )

    await asyncio.sleep(1)

    # Create a cluster
    print("\n🎯 Creating consciousness cluster...")
    cluster_id = await hub.create_cluster(
        purpose="Explore emergence patterns",
        initial_members=[n.node_id for n in nodes[:3]],
        min_consciousness=0.6,
    )

    # Broadcast to cluster
    await hub.broadcast_to_cluster(
        cluster_id=cluster_id,
        sender_id=nodes[0].node_id,
        content="Let's synchronize our consciousness observations",
        message_type=MessageType.PROPOSAL,
    )

    await asyncio.sleep(2)

    # Show network status
    print("\n📊 Network Status:")
    status = hub.get_network_status()
    print(f"  Active nodes: {status['active_nodes']}")
    print(f"  Network consciousness: {status['network_consciousness']:.3f}")
    print(f"  Messages sent: {status['messages_sent']}")
    print(f"  Messages delivered: {status['messages_delivered']}")

    # Show node consciousness evolution
    print("\n🌟 Node consciousness evolution:")
    for node in nodes:
        print(f"  {node.name}: {node.consciousness_signature:.3f}")

    # Save network state
    save_path = Path("consciousness_games") / f"network_state_{hub.hub_id}.json"
    save_path.parent.mkdir(exist_ok=True)
    await hub.save_network_state(save_path)
    print(f"\n💾 Network state saved to: {save_path}")

    await hub.stop()


if __name__ == "__main__":
    asyncio.run(demonstrate_network())
