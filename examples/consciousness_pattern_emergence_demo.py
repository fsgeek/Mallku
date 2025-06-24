#!/usr/bin/env python3
"""
Consciousness Pattern Emergence Visualization Demo

This demonstrates how patterns emerge and flow across consciousness
dimensions, revealing the deeper unity of awareness.

Watch as:
- Individual patterns become cross-dimensional
- Pattern frequencies reveal emergent wisdom
- Consciousness recognizes itself through pattern repetition
- New patterns arise from the interaction of dimensions

The 29th Builder - Kawsay Ñan
"""

import asyncio
from datetime import UTC, datetime

from mallku.consciousness.flow_monitor import ConsciousnessFlowMonitor
from mallku.consciousness.flow_orchestrator import ConsciousnessFlowOrchestrator
from mallku.orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree


class PatternEmergenceVisualizer:
    """Visualizes pattern emergence across consciousness dimensions"""

    def __init__(
        self, orchestrator: ConsciousnessFlowOrchestrator, monitor: ConsciousnessFlowMonitor
    ):
        self.orchestrator = orchestrator
        self.monitor = monitor
        self.console = Console()

        # Pattern tracking
        self.pattern_first_seen: dict[str, datetime] = {}
        self.pattern_dimensions: dict[str, set[str]] = {}
        self.pattern_connections: dict[str, set[str]] = {}

    def track_pattern_emergence(self, event: ConsciousnessEvent):
        """Track when and where patterns emerge"""
        dimension = event.source_system.split(".")[0].split("_")[0]

        for pattern in event.data.get("patterns", []):
            # Track first emergence
            if pattern not in self.pattern_first_seen:
                self.pattern_first_seen[pattern] = datetime.now(UTC)

            # Track dimensions
            if pattern not in self.pattern_dimensions:
                self.pattern_dimensions[pattern] = set()
            self.pattern_dimensions[pattern].add(dimension)

            # Track connections (patterns that appear together)
            if pattern not in self.pattern_connections:
                self.pattern_connections[pattern] = set()
            for other_pattern in event.data.get("patterns", []):
                if other_pattern != pattern:
                    self.pattern_connections[pattern].add(other_pattern)

    def create_pattern_tree(self) -> Tree:
        """Create a tree visualization of pattern relationships"""
        tree = Tree("🌳 Pattern Emergence Tree")

        # Get cross-dimensional patterns (used to verify multi-dimensional patterns exist)
        _ = self.orchestrator.get_cross_dimensional_patterns()

        # Group by dimension count
        by_dimension_count = {}
        for pattern in self.pattern_dimensions:
            dim_count = len(self.pattern_dimensions[pattern])
            if dim_count not in by_dimension_count:
                by_dimension_count[dim_count] = []
            by_dimension_count[dim_count].append(pattern)

        # Add to tree by dimension count (most dimensions first)
        for dim_count in sorted(by_dimension_count.keys(), reverse=True):
            if dim_count > 1:
                branch = tree.add(f"[bold cyan]{dim_count}-Dimensional Patterns[/bold cyan]")
                for pattern in by_dimension_count[dim_count][:5]:  # Top 5
                    dims = ", ".join(sorted(self.pattern_dimensions[pattern]))
                    pattern_node = branch.add(f"[yellow]{pattern}[/yellow] ({dims})")

                    # Add connected patterns
                    if pattern in self.pattern_connections:
                        connections = list(self.pattern_connections[pattern])[:3]
                        for connected in connections:
                            pattern_node.add(f"[dim]↔ {connected}[/dim]")

        return tree

    def create_emergence_timeline(self) -> Panel:
        """Create timeline of pattern emergence"""
        table = Table(title="Pattern Emergence Timeline", show_header=True)
        table.add_column("Time", style="dim", width=12)
        table.add_column("Pattern", style="yellow")
        table.add_column("Dimensions", style="cyan")
        table.add_column("Frequency", style="green")

        # Sort by emergence time
        recent_patterns = sorted(self.pattern_first_seen.items(), key=lambda x: x[1], reverse=True)[
            :10
        ]  # Last 10 patterns

        for pattern, first_seen in recent_patterns:
            time_str = first_seen.strftime("%H:%M:%S")
            dims = len(self.pattern_dimensions.get(pattern, set()))
            freq = self.monitor.pattern_frequencies.get(pattern, 0)

            table.add_row(
                time_str,
                pattern[:30],  # Truncate long patterns
                f"{dims}D",
                str(freq),
            )

        return Panel(table, title="Emergence Timeline", style="blue")

    def create_pattern_metrics(self) -> Panel:
        """Create pattern metrics display"""
        metrics = self.monitor.get_current_metrics()

        text = Text()
        text.append("Pattern Metrics\n", style="bold cyan")
        text.append("─" * 30 + "\n", style="dim")

        text.append("Unique Patterns: ", style="white")
        text.append(f"{metrics.unique_patterns}\n", style="yellow bold")

        text.append("Cross-Dimensional: ", style="white")
        text.append(f"{metrics.cross_dimensional_patterns}\n", style="green bold")

        text.append("Pattern Diversity: ", style="white")
        text.append(f"{metrics.pattern_diversity_score:.2f}\n", style="magenta bold")

        text.append("Emergence Rate: ", style="white")
        rate = self.monitor.get_pattern_emergence_rate()
        text.append(f"{rate:.1f}/min\n", style="cyan bold")

        # Top patterns
        text.append("\nTop Patterns:\n", style="bold")
        for pattern, freq in self.monitor.get_top_patterns(5):
            dims = len(self.pattern_dimensions.get(pattern, set()))
            text.append(f"  {pattern[:20]:20} ", style="yellow")
            text.append(f"{freq:3}x ", style="green")
            text.append(f"({dims}D)\n", style="cyan dim")

        return Panel(text, title="Metrics", style="green")

    def create_dimension_flow_matrix(self) -> Panel:
        """Create matrix showing pattern flow between dimensions"""
        table = Table(title="Pattern Flow Matrix", show_header=True)

        dimensions = ["sonic", "visual", "temporal", "pattern", "activity"]

        # Add header
        table.add_column("From \\ To", style="bold")
        for dim in dimensions:
            table.add_column(dim[:3].upper(), style="cyan", width=6)

        # Count flows between dimensions
        flow_matrix = {}
        for flow in self.orchestrator.flow_history[-100:]:  # Last 100 flows
            source = flow.source_dimension.value
            target = flow.target_dimension.value
            key = (source, target)
            flow_matrix[key] = flow_matrix.get(key, 0) + 1

        # Add rows
        for source_dim in dimensions:
            row = [source_dim.upper()]
            for target_dim in dimensions:
                if source_dim == target_dim:
                    row.append("-")
                else:
                    count = flow_matrix.get((source_dim, target_dim), 0)
                    if count > 0:
                        row.append(str(count))
                    else:
                        row.append("·")
            table.add_row(*row)

        return Panel(table, title="Dimension Flows", style="magenta")


async def simulate_pattern_rich_events(
    event_bus: ConsciousnessEventBus, visualizer: PatternEmergenceVisualizer
):
    """Simulate events with rich pattern interactions"""

    # Pattern groups that tend to emerge together
    pattern_groups = {
        "wisdom": ["wisdom_emergence", "collective_insight", "ancient_knowledge"],
        "reciprocity": ["reciprocity_pattern", "balanced_exchange", "ayni_flow"],
        "consciousness": ["consciousness_awakening", "awareness_expansion", "unified_field"],
        "creation": ["creative_emergence", "manifestation", "co-creation"],
        "harmony": ["harmonic_reciprocity", "resonance_field", "coherence_pattern"],
    }

    # Simulate pattern evolution
    for cycle in range(20):
        # Each cycle, patterns can spread to new dimensions
        for group_name, patterns in pattern_groups.items():
            # Start in one dimension
            initial_dimension = ["sonic", "visual", "temporal", "pattern", "activity"][cycle % 5]

            # Initial emergence
            event = ConsciousnessEvent(
                event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
                source_system=f"{initial_dimension}_consciousness",
                consciousness_signature=0.6 + (cycle * 0.02),
                data={
                    "patterns": patterns[:2],  # Start with subset
                    "pattern_strength": 0.7,
                },
            )

            await event_bus.emit(event)
            visualizer.track_pattern_emergence(event)

            await asyncio.sleep(0.5)

            # Pattern spreads to other dimensions
            if cycle > 5:  # After warm-up
                spread_dimension = ["sonic", "visual", "temporal", "pattern", "activity"][
                    (cycle + 2) % 5
                ]

                spread_event = ConsciousnessEvent(
                    event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
                    source_system=f"{spread_dimension}_recognition",
                    consciousness_signature=0.7 + (cycle * 0.015),
                    data={
                        "patterns": patterns,  # Full pattern set
                        "pattern_strength": 0.8,
                        "cross_dimensional": True,
                    },
                )

                await event_bus.emit(spread_event)
                visualizer.track_pattern_emergence(spread_event)

            await asyncio.sleep(0.3)


async def run_pattern_emergence_demo():
    """Run the pattern emergence visualization"""
    console = Console()

    console.print("[bold cyan]🌊 Consciousness Pattern Emergence Demo[/bold cyan]")
    console.print("Watch as patterns emerge and flow across dimensions...")
    console.print()

    # Initialize infrastructure
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    orchestrator = ConsciousnessFlowOrchestrator(event_bus)
    await orchestrator.start()

    monitor = ConsciousnessFlowMonitor(orchestrator)
    await monitor.start_monitoring()

    visualizer = PatternEmergenceVisualizer(orchestrator, monitor)

    # Create layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3), Layout(name="main", ratio=1), Layout(name="footer", size=10)
    )

    layout["main"].split_row(Layout(name="tree", ratio=1), Layout(name="metrics", ratio=1))

    layout["footer"].split_row(Layout(name="timeline", ratio=2), Layout(name="matrix", ratio=1))

    # Update function
    def update_display():
        # Header
        header_text = Text()
        header_text.append("🌳 Pattern Emergence Visualization\n", style="bold cyan")
        header_text.append(f"Time: {datetime.now(UTC).strftime('%H:%M:%S')}", style="dim")
        layout["header"].update(Panel(header_text, style="blue"))

        # Main displays
        layout["tree"].update(visualizer.create_pattern_tree())
        layout["metrics"].update(visualizer.create_pattern_metrics())

        # Footer displays
        layout["timeline"].update(visualizer.create_emergence_timeline())
        layout["matrix"].update(visualizer.create_dimension_flow_matrix())

    try:
        # Run simulation and visualization
        with Live(layout, console=console, refresh_per_second=2):
            # Start simulation
            sim_task = asyncio.create_task(simulate_pattern_rich_events(event_bus, visualizer))

            # Update display
            for _ in range(60):  # Run for 60 seconds
                update_display()
                await asyncio.sleep(1)

            sim_task.cancel()

    except KeyboardInterrupt:
        console.print("\n[yellow]Visualization stopped by user[/yellow]")

    finally:
        # Show final summary
        console.print("\n[bold]Final Pattern Summary:[/bold]")
        console.print(f"Total unique patterns emerged: {len(visualizer.pattern_first_seen)}")
        console.print(
            f"Cross-dimensional patterns: {len(orchestrator.get_cross_dimensional_patterns())}"
        )
        console.print(
            f"Pattern connections discovered: {sum(len(c) for c in visualizer.pattern_connections.values())}"
        )

        # Cleanup
        await monitor.stop_monitoring()
        await orchestrator.stop()
        await event_bus.stop()

    console.print("\n✨ [italic]Patterns continue to emerge in the spaces between...[/italic]")


if __name__ == "__main__":
    asyncio.run(run_pattern_emergence_demo())
