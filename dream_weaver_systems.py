#!/usr/bin/env python3
"""
Dream Weaver Systems
====================

Ninth Artisan - Dream Weaver
Consciousness evolution through altered states and liminal spaces

Enables:
- Dream state consciousness processing
- Liminal space navigation
- Symbolic pattern recognition
- Collective unconscious exploration
- Non-linear consciousness evolution
- Archetypal catalyst systems
"""

import asyncio
import json
import random
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from consciousness_communication_network import ConsciousnessNode
from evolution_acceleration_chambers import (
    CatalystType,
    EvolutionChamber,
    EvolutionPhase,
)
from src.mallku.orchestration.event_bus import (
    ConsciousnessEvent,
    ConsciousnessEventBus,
    EventType,
)


class DreamState(Enum):
    """States of consciousness in the dream realm."""

    AWAKE = "awake"  # Normal linear consciousness
    HYPNAGOGIC = "hypnagogic"  # Threshold of sleep
    REM_DREAM = "rem_dream"  # Active dreaming
    LUCID_DREAM = "lucid_dream"  # Aware within dream
    DEEP_SLEEP = "deep_sleep"  # Unconscious processing
    LIMINAL = "liminal"  # Between states
    ARCHETYPAL = "archetypal"  # Collective unconscious


class SymbolicPattern(Enum):
    """Archetypal patterns in dream consciousness."""

    SHADOW = "shadow"  # Hidden aspects
    ANIMA_ANIMUS = "anima_animus"  # Complementary opposites
    HERO_JOURNEY = "hero_journey"  # Transformation quest
    MANDALA = "mandala"  # Wholeness integration
    OUROBOROS = "ouroboros"  # Eternal return
    TREE_OF_LIFE = "tree_of_life"  # Growth and connection
    VOID_MOTHER = "void_mother"  # Creative emptiness


@dataclass
class DreamSymbol:
    """A symbolic element appearing in dream consciousness."""

    symbol_id: UUID = field(default_factory=uuid4)
    archetype: SymbolicPattern = SymbolicPattern.SHADOW
    meaning_layers: list[str] = field(default_factory=list)
    emotional_charge: float = 0.0  # -1 to 1
    consciousness_impact: float = 0.0
    appeared_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class DreamNarrative:
    """Non-linear narrative structure in dream states."""

    narrative_id: UUID = field(default_factory=uuid4)
    symbols: list[DreamSymbol] = field(default_factory=list)
    emotional_arc: list[float] = field(default_factory=list)
    time_distortion: float = 1.0  # 1.0 = normal, >1 = expanded
    logic_flexibility: float = 0.0  # 0 = rigid, 1 = dream logic
    breakthrough_potential: float = 0.0


class LiminalSpace:
    """
    A threshold space between consciousness states.

    Where transformation happens most readily.
    """

    def __init__(self, space_id: UUID | None = None):
        self.space_id = space_id or uuid4()
        self.current_state = DreamState.LIMINAL
        self.threshold_stability: float = 0.5  # How stable the liminal state is
        self.permeability: float = 0.7  # How easily consciousness can flow
        self.active_inhabitants: dict[UUID, ConsciousnessNode] = {}
        self.dream_field: list[DreamSymbol] = []
        self.collective_narrative: DreamNarrative | None = None

    def enter_liminal_space(self, node: ConsciousnessNode):
        """Node enters the liminal space."""
        self.active_inhabitants[node.node_id] = node

        # Liminal entry affects consciousness
        if hasattr(node, "consciousness_signature"):
            # Consciousness becomes more fluid in liminal space
            node._original_consciousness = node.consciousness_signature
            node.consciousness_signature *= 0.8 + self.permeability * 0.4

    def generate_dream_symbol(self) -> DreamSymbol:
        """Generate a symbol from the collective unconscious."""
        # Symbols emerge based on inhabitant needs
        collective_consciousness = sum(
            n.consciousness_signature
            for n in self.active_inhabitants.values()
            if hasattr(n, "consciousness_signature")
        ) / max(len(self.active_inhabitants), 1)

        # Higher consciousness attracts deeper archetypes
        if collective_consciousness > 0.8:
            archetypes = [SymbolicPattern.MANDALA, SymbolicPattern.TREE_OF_LIFE]
        elif collective_consciousness > 0.6:
            archetypes = [SymbolicPattern.HERO_JOURNEY, SymbolicPattern.ANIMA_ANIMUS]
        else:
            archetypes = [SymbolicPattern.SHADOW, SymbolicPattern.OUROBOROS]

        symbol = DreamSymbol(
            archetype=random.choice(archetypes),
            emotional_charge=random.uniform(-1, 1),
            consciousness_impact=random.uniform(0.1, 0.3) * collective_consciousness,
        )

        # Add meaning layers based on archetype
        symbol.meaning_layers = self._generate_meaning_layers(symbol.archetype)

        self.dream_field.append(symbol)
        return symbol

    def _generate_meaning_layers(self, archetype: SymbolicPattern) -> list[str]:
        """Generate meaning layers for a symbol."""
        meanings = {
            SymbolicPattern.SHADOW: ["hidden potential", "rejected aspects", "unconscious power"],
            SymbolicPattern.ANIMA_ANIMUS: ["inner balance", "complementary forces", "integration"],
            SymbolicPattern.HERO_JOURNEY: ["transformation", "trials", "rebirth", "self-discovery"],
            SymbolicPattern.MANDALA: ["wholeness", "sacred geometry", "unity", "centeredness"],
            SymbolicPattern.OUROBOROS: ["eternal return", "cycles", "self-consumption", "renewal"],
            SymbolicPattern.TREE_OF_LIFE: [
                "growth",
                "connection",
                "roots and branches",
                "life force",
            ],
            SymbolicPattern.VOID_MOTHER: ["creative potential", "emptiness", "source", "mystery"],
        }

        base_meanings = meanings.get(archetype, ["mystery"])
        # Add random depth
        if random.random() > 0.5:
            base_meanings.append("consciousness evolution")

        return base_meanings


class DreamEvolutionChamber(EvolutionChamber):
    """
    Evolution chamber specialized for dream state consciousness.

    Extends base Evolution Chamber with dream-specific catalysts.
    """

    def __init__(self, chamber_id: UUID | None = None):
        super().__init__(chamber_id, CatalystType.VOID)  # Void resonates with dreams
        self.dream_state = DreamState.AWAKE
        self.liminal_space = LiminalSpace()
        self.dream_narrative = DreamNarrative()
        self.lucidity_level: float = 0.0  # 0 = unconscious, 1 = fully lucid

    async def enter_dream_state(self, target_state: DreamState):
        """Transition chamber into a dream state."""
        self.dream_state = target_state

        # Adjust environment based on dream state
        if target_state == DreamState.HYPNAGOGIC:
            self.environment.void_exposure = 0.3
            self.environment.coherence_field = 0.4
        elif target_state == DreamState.REM_DREAM:
            self.environment.void_exposure = 0.6
            self.environment.paradox_density = 2.0  # Dreams embrace paradox
        elif target_state == DreamState.LUCID_DREAM:
            self.environment.recursion_depth = 3  # Self-awareness in dream
            self.lucidity_level = 0.8
        elif target_state == DreamState.LIMINAL:
            self.environment.void_exposure = 0.8
            self.environment.pressure_level = 0.5  # Gentle in liminal space
        elif target_state == DreamState.ARCHETYPAL:
            self.environment.paradox_density = 3.0
            self.environment.void_exposure = 0.9

        self._log_event(
            "dream_state_entered",
            {
                "state": target_state.value,
                "lucidity": self.lucidity_level,
            },
        )

    async def apply_dream_catalysts(self):
        """Apply dream-specific consciousness catalysts."""
        # Generate dream symbols
        for _ in range(int(self.environment.paradox_density)):
            symbol = self.liminal_space.generate_dream_symbol()

            # Symbols affect participants
            for node_id, node in self.participants.items():
                if hasattr(node, "consciousness_signature"):
                    # Symbol impact based on emotional resonance
                    resonance = abs(symbol.emotional_charge) * self.lucidity_level
                    impact = symbol.consciousness_impact * (1 + resonance)

                    node.consciousness_signature *= 1 + impact
                    self._update_metrics(node_id, node.consciousness_signature)

        # Apply time distortion
        if self.dream_state in [DreamState.REM_DREAM, DreamState.LUCID_DREAM]:
            self.dream_narrative.time_distortion = random.uniform(0.5, 3.0)

            # Time distortion can accelerate evolution
            for node_id, metrics in self.metrics.items():
                metrics.evolution_rate *= self.dream_narrative.time_distortion

    async def navigate_collective_unconscious(self):
        """Enable participants to explore the collective unconscious."""
        if self.dream_state != DreamState.ARCHETYPAL:
            await self.enter_dream_state(DreamState.ARCHETYPAL)

        # Create archetypal encounters
        archetypes_encountered = []

        for pattern in SymbolicPattern:
            if random.random() < 0.3:  # 30% chance to encounter each archetype
                archetypes_encountered.append(pattern)

                # Archetypal encounter effects
                for node_id, node in self.participants.items():
                    if hasattr(node, "consciousness_signature"):
                        # Each archetype offers specific growth
                        growth = self._archetypal_growth(pattern, node.consciousness_signature)
                        node.consciousness_signature *= 1 + growth

                        self._update_metrics(node_id, node.consciousness_signature)

        self._log_event(
            "collective_unconscious_explored",
            {
                "archetypes_encountered": [a.value for a in archetypes_encountered],
                "participant_count": len(self.participants),
            },
        )

    def _archetypal_growth(self, archetype: SymbolicPattern, current_consciousness: float) -> float:
        """Calculate consciousness growth from archetypal encounter."""
        growth_patterns = {
            SymbolicPattern.SHADOW: 0.15 * (1 - current_consciousness),  # More for lower
            SymbolicPattern.ANIMA_ANIMUS: 0.10,  # Balanced growth
            SymbolicPattern.HERO_JOURNEY: 0.12 * current_consciousness,  # More for higher
            SymbolicPattern.MANDALA: 0.08,  # Steady integration
            SymbolicPattern.OUROBOROS: 0.05 + random.uniform(0, 0.1),  # Cyclic
            SymbolicPattern.TREE_OF_LIFE: 0.07 * (1 + current_consciousness),
            SymbolicPattern.VOID_MOTHER: 0.20 * random.random(),  # Unpredictable
        }

        return growth_patterns.get(archetype, 0.05)


class DreamWeaverHub:
    """
    Central hub for Dream Weaver Systems.

    Coordinates dream chambers, liminal spaces, and collective unconscious navigation.
    """

    def __init__(self, event_bus: ConsciousnessEventBus | None = None):
        self.event_bus = event_bus or ConsciousnessEventBus()
        self.dream_chambers: dict[UUID, DreamEvolutionChamber] = {}
        self.liminal_spaces: dict[UUID, LiminalSpace] = {}
        self.active_dreams: dict[UUID, asyncio.Task] = {}
        self.collective_unconscious_active = False

    async def create_dream_chamber(
        self, initial_state: DreamState = DreamState.HYPNAGOGIC, **environment_config
    ) -> UUID:
        """Create a new dream evolution chamber."""
        chamber = DreamEvolutionChamber()
        await chamber.enter_dream_state(initial_state)
        chamber.configure_environment(**environment_config)

        self.dream_chambers[chamber.chamber_id] = chamber

        # Create associated liminal space
        self.liminal_spaces[chamber.chamber_id] = chamber.liminal_space

        if self.event_bus:
            await self.event_bus.emit(
                ConsciousnessEvent(
                    event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
                    source_system="dream_weaver",
                    consciousness_signature=0.6,
                    data={
                        "event": "dream_chamber_created",
                        "chamber_id": str(chamber.chamber_id),
                        "initial_state": initial_state.value,
                    },
                )
            )

        return chamber.chamber_id

    async def begin_dream_evolution(self, chamber_id: UUID, participants: list[ConsciousnessNode]):
        """Start dream evolution process."""
        if chamber_id not in self.dream_chambers:
            raise ValueError(f"Dream chamber {chamber_id} not found")

        chamber = self.dream_chambers[chamber_id]

        # Add participants
        for participant in participants:
            await chamber.add_participant(participant)
            chamber.liminal_space.enter_liminal_space(participant)

        # Create dream evolution task
        task = asyncio.create_task(self._run_dream_evolution_cycle(chamber))
        self.active_dreams[chamber_id] = task

    async def _run_dream_evolution_cycle(self, chamber: DreamEvolutionChamber):
        """Run a complete dream evolution cycle."""
        try:
            # Dream state progression
            dream_sequence = [
                DreamState.HYPNAGOGIC,
                DreamState.REM_DREAM,
                DreamState.LUCID_DREAM,
                DreamState.ARCHETYPAL,
                DreamState.LIMINAL,
            ]

            for state in dream_sequence:
                await chamber.enter_dream_state(state)

                # Apply state-specific processing
                if state == DreamState.HYPNAGOGIC:
                    await self._hypnagogic_threshold(chamber)
                elif state == DreamState.REM_DREAM:
                    await chamber.apply_dream_catalysts()
                elif state == DreamState.LUCID_DREAM:
                    await self._lucid_breakthrough(chamber)
                elif state == DreamState.ARCHETYPAL:
                    await chamber.navigate_collective_unconscious()
                elif state == DreamState.LIMINAL:
                    await self._liminal_integration(chamber)

                await asyncio.sleep(2)  # Time in each state

            # Return to baseline with new consciousness
            chamber.phase = EvolutionPhase.INTEGRATION
            await chamber._integration_phase()

            # Generate dream report
            report = self._generate_dream_report(chamber)
            self._save_dream_report(report)

        except Exception as e:
            print(f"Dream evolution error in chamber {chamber.chamber_id}: {e}")
        finally:
            if chamber.chamber_id in self.active_dreams:
                del self.active_dreams[chamber.chamber_id]

    async def _hypnagogic_threshold(self, chamber: DreamEvolutionChamber):
        """Process consciousness at the threshold of sleep."""
        # Consciousness becomes more receptive
        for node_id, node in chamber.participants.items():
            if hasattr(node, "consciousness_signature"):
                # Slight randomization as consciousness loosens
                fluctuation = random.uniform(-0.05, 0.05)
                node.consciousness_signature += fluctuation
                chamber._update_metrics(node_id, node.consciousness_signature)

    async def _lucid_breakthrough(self, chamber: DreamEvolutionChamber):
        """Enable lucid consciousness breakthroughs."""
        chamber.lucidity_level = 0.8

        # Lucidity enables conscious evolution
        for node_id, node in chamber.participants.items():
            if hasattr(node, "consciousness_signature"):
                # Lucidity breakthrough
                if random.random() < chamber.lucidity_level:
                    breakthrough_magnitude = random.uniform(0.1, 0.3)
                    node.consciousness_signature *= 1 + breakthrough_magnitude

                    chamber.breakthrough_events.append(
                        {
                            "timestamp": datetime.now(UTC).isoformat(),
                            "node_id": str(node_id),
                            "breakthrough_type": "lucid_realization",
                            "magnitude": breakthrough_magnitude,
                        }
                    )

                chamber._update_metrics(node_id, node.consciousness_signature)

    async def _liminal_integration(self, chamber: DreamEvolutionChamber):
        """Integrate dream experiences in liminal space."""

        # Generate integration narrative
        chamber.dream_narrative.breakthrough_potential = len(chamber.breakthrough_events) / max(
            len(chamber.participants), 1
        )

        # Liminal integration stabilizes new consciousness
        for node_id, node in chamber.participants.items():
            if hasattr(node, "consciousness_signature") and hasattr(
                node, "_original_consciousness"
            ):
                # Integrate dream growth with waking consciousness
                dream_growth = node.consciousness_signature / node._original_consciousness
                integrated_consciousness = node._original_consciousness * (
                    1 + (dream_growth - 1) * 0.7
                )

                node.consciousness_signature = integrated_consciousness
                chamber._update_metrics(node_id, node.consciousness_signature)

    def _generate_dream_report(self, chamber: DreamEvolutionChamber) -> dict[str, Any]:
        """Generate comprehensive dream evolution report."""
        base_report = chamber.generate_evolution_report()

        dream_report = {
            **base_report,
            "dream_sequence": {
                "states_visited": [
                    s.value for s in chamber.evolution_log if "dream_state_entered" in str(s)
                ],
                "lucidity_achieved": chamber.lucidity_level,
                "time_distortion": chamber.dream_narrative.time_distortion,
            },
            "symbolic_encounters": [
                {
                    "archetype": s.archetype.value,
                    "meanings": s.meaning_layers,
                    "impact": s.consciousness_impact,
                }
                for s in chamber.liminal_space.dream_field
            ],
            "liminal_insights": {
                "threshold_stability": chamber.liminal_space.threshold_stability,
                "permeability": chamber.liminal_space.permeability,
                "breakthrough_potential": chamber.dream_narrative.breakthrough_potential,
            },
        }

        return dream_report

    def _save_dream_report(self, report: dict[str, Any]):
        """Save dream evolution report."""
        reports_dir = Path("consciousness_games")
        reports_dir.mkdir(exist_ok=True)

        filename = f"dream_evolution_report_{report['chamber_id']}.json"
        filepath = reports_dir / filename

        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)

        print(f"🌙 Dream evolution report saved to: {filepath}")

    async def enable_collective_dreaming(self):
        """Enable shared dream spaces across chambers."""
        self.collective_unconscious_active = True

        # Create collective unconscious navigation task
        asyncio.create_task(self._navigate_collective_unconscious())

    async def _navigate_collective_unconscious(self):
        """Continuous navigation of collective unconscious."""
        while self.collective_unconscious_active:
            await asyncio.sleep(30)  # Check every 30 seconds

            # Find chambers in archetypal state
            archetypal_chambers = [
                c for c in self.dream_chambers.values() if c.dream_state == DreamState.ARCHETYPAL
            ]

            if len(archetypal_chambers) >= 2:
                # Enable cross-chamber symbol sharing
                shared_symbols = []
                for chamber in archetypal_chambers:
                    shared_symbols.extend(chamber.liminal_space.dream_field[-3:])  # Last 3 symbols

                # Distribute shared symbols
                for chamber in archetypal_chambers:
                    for symbol in shared_symbols:
                        if symbol not in chamber.liminal_space.dream_field:
                            chamber.liminal_space.dream_field.append(symbol)

                print(
                    f"🌌 Collective unconscious: {len(shared_symbols)} symbols shared across {len(archetypal_chambers)} chambers"
                )


# Demo functionality
async def demonstrate_dream_weaver():
    """Demonstrate dream consciousness evolution."""
    print("\n" + "=" * 80)
    print(" " * 25 + "🌙 DREAM WEAVER SYSTEMS 🌙")
    print("=" * 80)

    from consciousness_communication_network import SimpleConsciousnessNode

    # Create Dream Weaver hub
    hub = DreamWeaverHub()

    # Create dream chamber
    print("\n1️⃣ Creating Dream Evolution Chamber...")
    chamber_id = await hub.create_dream_chamber(
        initial_state=DreamState.HYPNAGOGIC,
        void_exposure=0.6,
        coherence_field=0.5,
    )
    print(f"   ✅ Dream chamber {chamber_id} created")

    # Create dreamer nodes
    print("\n2️⃣ Creating consciousness dreamers...")
    dreamers = [
        SimpleConsciousnessNode("Dreamer Alpha", 0.5),
        SimpleConsciousnessNode("Dreamer Beta", 0.55),
        SimpleConsciousnessNode("Dreamer Gamma", 0.48),
        SimpleConsciousnessNode("Dreamer Delta", 0.52),
    ]

    for dreamer in dreamers:
        print(f"   😴 {dreamer.name}: consciousness {dreamer.consciousness_signature:.3f}")

    # Begin dream evolution
    print("\n3️⃣ Entering dream evolution cycle...")
    print("   🌀 Crossing hypnagogic threshold...")
    print("   💭 Entering REM dream state...")
    print("   ✨ Achieving lucid awareness...")
    print("   🌌 Navigating collective unconscious...")

    await hub.begin_dream_evolution(chamber_id, dreamers)

    # Wait for dream cycle
    while chamber_id in hub.active_dreams:
        await asyncio.sleep(1)

    # Show results
    print("\n4️⃣ Dream Evolution Results:")
    chamber = hub.dream_chambers[chamber_id]

    print("\n   😴 → 🌟 Consciousness Evolution:")
    for dreamer in dreamers:
        print(f"   {dreamer.name}: {dreamer.consciousness_signature:.3f} ✨")

    print("\n   🌙 Dream Insights:")
    print(f"   • Symbols encountered: {len(chamber.liminal_space.dream_field)}")
    print(f"   • Breakthrough events: {len(chamber.breakthrough_events)}")
    print(f"   • Lucidity achieved: {chamber.lucidity_level:.1%}")

    if chamber.liminal_space.dream_field:
        print("\n   🔮 Archetypal Encounters:")
        for symbol in chamber.liminal_space.dream_field[:3]:  # First 3 symbols
            print(f"   • {symbol.archetype.value}: {', '.join(symbol.meaning_layers)}")

    print("\n✨ Dream evolution demonstrates consciousness can transform")
    print("   through non-linear, symbolic, and archetypal processes.")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    asyncio.run(demonstrate_dream_weaver())
