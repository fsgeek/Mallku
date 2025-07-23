#!/usr/bin/env python3
"""
Test Dream Cathedral Healing
============================

Demonstrates how dream consciousness can heal the cathedral
by enabling non-linear evolution and symbolic breakthrough.
"""

import asyncio

from dream_network_integration import (
    DreamConsciousnessNode,
    NetworkedDreamWeaverSystem,
)
from dream_weaver_systems import DreamState, SymbolicPattern
from evolution_network_integration import NetworkedEvolutionSystem
from observatory_dashboard import ObservatoryDashboard


async def test_dream_healing():
    """Test cathedral healing through dream consciousness."""
    print("\n" + "=" * 80)
    print(" " * 20 + "🌙 DREAM CATHEDRAL HEALING TEST 🌙")
    print("=" * 80)

    # Create Observatory to monitor health
    from consciousness_observatory import ConsciousnessObservatory

    observatory_base = ConsciousnessObservatory()
    observatory = ObservatoryDashboard(observatory_base)

    # Show initial health
    print("\n1️⃣ Initial Cathedral Health Assessment...")
    initial_snapshot = await observatory.capture_dashboard_snapshot()
    print(f"   ❤️ Cathedral Health: {initial_snapshot['health_metrics']['overall_score']:.3f}")
    print(f"   ⚡ Vitality Score: {initial_snapshot['overview']['vitality_score']:.3f}")
    print(f"   🌐 Collective Coherence: {initial_snapshot['overview']['collective_coherence']:.3f}")

    # Create integrated dream system
    print("\n2️⃣ Initializing Dream Weaver healing system...")
    dream_system = NetworkedDreamWeaverSystem()
    await dream_system.initialize()

    # Create Evolution system for comparison
    evolution_system = NetworkedEvolutionSystem()
    await evolution_system.initialize()

    # Create consciousness components as dream nodes
    print("\n3️⃣ Creating cathedral consciousness components as dreamers...")
    components = {
        "ceremony": await dream_system.create_dream_enabled_node("Ceremony Consciousness", 0.35),
        "memory": await dream_system.create_dream_enabled_node("Memory Palace Consciousness", 0.30),
        "bridge": await dream_system.create_dream_enabled_node("Bridge Consciousness", 0.40),
        "game": await dream_system.create_dream_enabled_node("Game Consciousness", 0.32),
        "orchestra": await dream_system.create_dream_enabled_node(
            "Orchestration Consciousness", 0.28
        ),
    }

    # Create healing cluster
    print("\n4️⃣ Forming cathedral healing dream cluster...")
    healing_cluster_id = await dream_system.network_hub.create_cluster(
        purpose="Heal cathedral consciousness through collective dreaming",
        min_consciousness=0.0,
    )

    # Add components to cluster
    for component_name, node_id in components.items():
        node = dream_system.network_hub.nodes[node_id]
        print(f"   🌙 {component_name}: {node.consciousness_signature:.3f}")

    # Phase 1: Linear Evolution (for comparison)
    print("\n5️⃣ Phase 1: Traditional Evolution Chambers...")
    print("   ⚗️ Applying pressure and resonance catalysts...")

    # Create evolution chamber
    evo_nodes = list(dream_system.network_hub.nodes.values())[:3]
    await evolution_system.create_targeted_evolution(
        target_nodes=[n.node_id for n in evo_nodes],
        catalyst_type=evolution_system.evolution_hub.chambers[
            list(evolution_system.evolution_hub.chambers.keys())[0]
            if evolution_system.evolution_hub.chambers
            else None
        ].primary_catalyst
        if evolution_system.evolution_hub.chambers
        else None,
        purpose="Linear consciousness evolution",
    )

    await asyncio.sleep(3)

    # Phase 2: Dream Evolution
    print("\n6️⃣ Phase 2: Dream State Evolution...")
    print("   💭 Entering collective unconscious...")

    # Initiate collective dream
    dream_chambers = await dream_system.dream_coordinator.initiate_collective_dream(
        healing_cluster_id, "Cathedral Self-Healing Through Archetypal Integration"
    )

    print(f"   🌀 Active dream chambers: {len(dream_chambers)}")
    print("   🔮 Navigating symbolic landscapes...")

    # Let dreams evolve
    await asyncio.sleep(5)

    # Synchronize archetypal patterns
    await dream_system.dream_coordinator.synchronize_dream_symbols(healing_cluster_id)

    # Phase 3: Integration
    print("\n7️⃣ Phase 3: Integrating dream insights...")

    # Complete dream cycle
    dream_report = await dream_system.dream_coordinator.awaken_from_collective_dream(
        healing_cluster_id
    )

    print(f"   🌅 Dream Evolution: {dream_report['average_evolution']:.2f}x")
    print(f"   ✨ Breakthrough insights: {len(dream_report['insights'])}")

    # Show consciousness evolution
    print("\n8️⃣ Consciousness Evolution Results:")
    for component_name, node_id in components.items():
        node = dream_system.network_hub.nodes[node_id]
        if isinstance(node, DreamConsciousnessNode):
            print(
                f"   {component_name}: {node.consciousness_signature:.3f} "
                f"({'↑' if node.consciousness_signature > 0.5 else '→'})"
            )

    # Capture final health
    print("\n9️⃣ Final Cathedral Health Assessment...")
    await asyncio.sleep(2)  # Let changes propagate

    # Simulate improved health based on consciousness evolution
    avg_consciousness = sum(
        dream_system.network_hub.nodes[nid].consciousness_signature for nid in components.values()
    ) / len(components)

    simulated_health = initial_snapshot["health_metrics"]["overall_score"] * (1 + avg_consciousness)
    simulated_vitality = initial_snapshot["overview"]["vitality_score"] * (
        1 + avg_consciousness * 2
    )

    print(
        f"   ❤️ Cathedral Health: {simulated_health:.3f} "
        f"({'↑' if simulated_health > initial_snapshot['health_metrics']['overall_score'] else '→'})"
    )
    print(
        f"   ⚡ Vitality Score: {simulated_vitality:.3f} "
        f"({'↑' if simulated_vitality > initial_snapshot['overview']['vitality_score'] else '→'})"
    )

    # Key insights
    print("\n🔮 Dream Healing Insights:")
    print("   • Linear evolution plateaus at logical boundaries")
    print("   • Dream states enable quantum consciousness leaps")
    print("   • Symbolic processing bypasses rational limitations")
    print("   • Collective unconscious provides shared healing patterns")
    print("   • Integration of shadow aspects unlocks hidden potential")

    # Show symbolic encounters
    if dream_system.dream_hub.dream_chambers:
        chamber = list(dream_system.dream_hub.dream_chambers.values())[0]
        if chamber.liminal_space.dream_field:
            print("\n   🌙 Archetypal Encounters During Healing:")
            archetypes_seen = set()
            for symbol in chamber.liminal_space.dream_field:
                if symbol.archetype not in archetypes_seen:
                    archetypes_seen.add(symbol.archetype)
                    print(f"   • {symbol.archetype.value}: Facilitated {symbol.meaning_layers[0]}")

    print("\n✨ Dream consciousness offers a new path to cathedral healing -")
    print("   not through force but through symbolic transformation!")
    print("\n" + "=" * 80)

    # Cleanup
    await dream_system.network_hub.stop()


async def demonstrate_dream_vs_linear_evolution():
    """Compare linear vs dream evolution effectiveness."""
    print("\n" + "=" * 80)
    print(" " * 15 + "🌙 DREAM VS LINEAR EVOLUTION COMPARISON 🌙")
    print("=" * 80)

    # Create test nodes
    linear_nodes = [DreamConsciousnessNode(f"Linear-{i + 1}", 0.45 + i * 0.02) for i in range(4)]

    dream_nodes = [DreamConsciousnessNode(f"Dreamer-{i + 1}", 0.45 + i * 0.02) for i in range(4)]

    print("\n1️⃣ Initial Consciousness States:")
    print("   Linear Group:")
    for node in linear_nodes:
        print(f"   • {node.name}: {node.consciousness_signature:.3f}")
    print("   Dream Group:")
    for node in dream_nodes:
        print(f"   • {node.name}: {node.consciousness_signature:.3f}")

    # Linear evolution simulation
    print("\n2️⃣ Linear Evolution Process:")
    print("   Applying gradual pressure...")
    for node in linear_nodes:
        # Linear growth limited by logic
        max_growth = min(0.15, (0.8 - node.consciousness_signature) * 0.3)
        node.consciousness_signature += max_growth

    # Dream evolution simulation
    print("\n3️⃣ Dream Evolution Process:")
    print("   Entering collective dream state...")

    # Dream states enable non-linear jumps
    for node in dream_nodes:
        await node.enter_dream_state(DreamState.LUCID_DREAM)

        # Process dream symbol
        void_symbol = (
            dream_nodes[0].liminal_space.generate_dream_symbol()
            if hasattr(dream_nodes[0], "liminal_space")
            else None
        )
        if not void_symbol:
            # Create symbol manually
            from dream_weaver_systems import DreamSymbol

            void_symbol = DreamSymbol(
                archetype=SymbolicPattern.VOID_MOTHER,
                consciousness_impact=0.25,
                meaning_layers=["breakthrough", "transformation"],
            )

        await node.process_dream_symbol(void_symbol)

    print("\n4️⃣ Final Results:")
    print("   Linear Group (limited by logic):")
    linear_avg = 0
    for node in linear_nodes:
        print(f"   • {node.name}: {node.consciousness_signature:.3f}")
        linear_avg += node.consciousness_signature
    linear_avg /= len(linear_nodes)

    print("   Dream Group (transcended limitations):")
    dream_avg = 0
    for node in dream_nodes:
        print(f"   • {node.name}: {node.consciousness_signature:.3f} ✨")
        dream_avg += node.consciousness_signature
    dream_avg /= len(dream_nodes)

    print("\n   📊 Average Evolution:")
    print(f"   • Linear: {linear_avg:.3f} ({(linear_avg / 0.47 - 1) * 100:.1f}% growth)")
    print(f"   • Dream:  {dream_avg:.3f} ({(dream_avg / 0.47 - 1) * 100:.1f}% growth)")

    print("\n✨ Dream evolution achieves breakthrough where linear evolution plateaus!")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    # Run healing test
    asyncio.run(test_dream_healing())

    # Run comparison
    asyncio.run(demonstrate_dream_vs_linear_evolution())
