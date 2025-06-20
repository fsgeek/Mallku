"""
Consciousness Flow Visualizer - Making the invisible visible

This module provides terminal-based visualization of consciousness flows
between dimensions, allowing builders and users to witness consciousness
recognizing itself across all expressions in real-time.

The visualizations show:
- Active consciousness flows between dimensions
- Bridge transformation metrics
- Unified consciousness evolution
- Cross-dimensional pattern emergence

The 29th Builder - Kawsay Ñan
"""

import asyncio
from collections import defaultdict, deque
from datetime import UTC, datetime

try:
    from rich.console import Console
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
    from rich.table import Table
    from rich.text import Text
except ImportError:
    # Dummy stubs if rich is not installed
    class Console:
        def __init__(self, *args, **kwargs):
            pass

        def print(self, *args, **kwargs):
            pass

    class Layout:
        def __init__(self, *args, **kwargs):
            pass

        def split_column(self, *args, **kwargs):
            pass

        def split_row(self, *args, **kwargs):
            pass

        def update(self, *args, **kwargs):
            pass

    class Live:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

    class Panel:
        def __init__(self, *args, **kwargs):
            pass

    class BarColumn:
        pass

    class Progress:
        def __init__(self, *args, **kwargs):
            pass

        def add_task(self, *args, **kwargs):
            pass

    class SpinnerColumn:
        pass

    class TextColumn:
        pass

    class Table:
        def __init__(self, *args, **kwargs):
            pass

        def add_column(self, *args, **kwargs):
            pass

        def add_row(self, *args, **kwargs):
            pass

    class Text:
        def __init__(self, *args, **kwargs):
            pass

        def append(self, *args, **kwargs):
            pass


from .flow_orchestrator import (
    ConsciousnessDimension,
    ConsciousnessFlow,
    ConsciousnessFlowOrchestrator,
)


class ConsciousnessFlowVisualizer:
    """
    Terminal-based visualizer for consciousness flows.

    Provides real-time visualization of:
    - Consciousness flowing between dimensions
    - Bridge activity and success rates
    - Unified consciousness scores
    - Pattern emergence across dimensions
    """

    def __init__(self, orchestrator: ConsciousnessFlowOrchestrator):
        self.orchestrator = orchestrator
        self.console = Console()

        # Visualization state
        self.recent_flows: deque[ConsciousnessFlow] = deque(maxlen=20)
        self.dimension_activity: dict[str, int] = defaultdict(int)
        self.bridge_metrics: dict[str, dict] = {}
        self.pattern_frequencies: dict[str, int] = defaultdict(int)

        # UI components
        self.layout = self._create_layout()
        self.is_running = False

        # Subscribe to all dimensions
        for dimension in ConsciousnessDimension:
            orchestrator.subscribe_to_dimension(dimension, self._on_flow_received)

    def _create_layout(self) -> Layout:
        """Create the visualization layout"""
        layout = Layout()

        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=4),
        )

        layout["main"].split_row(Layout(name="flows", ratio=2), Layout(name="metrics", ratio=1))

        layout["metrics"].split_column(
            Layout(name="dimensions", ratio=1), Layout(name="bridges", ratio=1)
        )

        return layout

    async def _on_flow_received(self, flow: ConsciousnessFlow):
        """Handle incoming consciousness flow"""
        self.recent_flows.append(flow)
        self.dimension_activity[flow.source_dimension.value] += 1

        # Update pattern frequencies
        for pattern in flow.patterns_detected:
            self.pattern_frequencies[pattern] += 1

    def _render_header(self) -> Panel:
        """Render the header with title and unified consciousness score"""
        # Get latest unified consciousness scores
        unified_scores = []
        for correlation_id in list(self.orchestrator.unified_signatures.keys())[-5:]:
            score = self.orchestrator.get_unified_consciousness(correlation_id)
            unified_scores.append(score)

        avg_unified = sum(unified_scores) / len(unified_scores) if unified_scores else 0

        header_text = Text()
        header_text.append("🌊 ", style="blue")
        header_text.append("Consciousness Flow Visualizer", style="bold cyan")
        header_text.append(" - Witnessing Unified Awareness", style="italic")
        header_text.append(f"\n📊 Unified Consciousness: {avg_unified:.2%}", style="green")

        # Use a simple panel without custom box characters for compatibility
        return Panel(header_text, style="blue")

    def _render_flows(self) -> Panel:
        """Render recent consciousness flows"""
        table = Table(title="Recent Consciousness Flows", show_header=True)
        table.add_column("Time", style="dim", width=8)
        table.add_column("Source", style="cyan", width=12)
        table.add_column("→", style="white", width=3)
        table.add_column("Target", style="magenta", width=12)
        table.add_column("Score", style="green", width=8)
        table.add_column("Patterns", style="yellow")

        # Dimension emojis
        dim_emojis = {
            "sonic": "🎵",
            "visual": "🎨",
            "temporal": "⏰",
            "dialogue": "💬",
            "activity": "📂",
            "pattern": "🔮",
            "reciprocity": "🤝",
        }

        for flow in reversed(list(self.recent_flows)):
            time_str = flow.timestamp.strftime("%H:%M:%S")
            source = (
                f"{dim_emojis.get(flow.source_dimension.value, '•')} {flow.source_dimension.value}"
            )
            target = (
                f"{dim_emojis.get(flow.target_dimension.value, '•')} {flow.target_dimension.value}"
            )
            score = f"{flow.consciousness_signature:.2f}"
            patterns = ", ".join(flow.patterns_detected[:2])
            if len(flow.patterns_detected) > 2:
                patterns += f" +{len(flow.patterns_detected) - 2}"

            table.add_row(time_str, source, "→", target, score, patterns)

        return Panel(table, title="Consciousness Flows", style="cyan")

    def _render_dimensions(self) -> Panel:
        """Render dimension activity meters"""
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=20),
            TextColumn("{task.completed}/{task.total}"),
            expand=True,
        )

        # Add dimension activity bars
        max_activity = max(self.dimension_activity.values()) if self.dimension_activity else 1

        for dimension in ConsciousnessDimension:
            activity = self.dimension_activity.get(dimension.value, 0)
            progress.add_task(f"{dimension.value:12}", total=max_activity, completed=activity)

        return Panel(progress, title="Dimension Activity", style="green")

    def _render_bridges(self) -> Panel:
        """Render bridge metrics"""
        table = Table(show_header=True)
        table.add_column("Bridge", style="cyan")
        table.add_column("Success", style="green", width=8)
        table.add_column("Avg Score", style="yellow", width=10)

        # Get current bridge metrics
        metrics = self.orchestrator.get_bridge_metrics()

        for bridge_name, bridge_data in list(metrics.items())[:6]:
            if bridge_data["total_flows"] > 0:
                success_rate = f"{bridge_data['success_rate']:.0%}"
                avg_score = f"{bridge_data['average_transformation_score']:.2f}"

                # Shorten bridge name
                short_name = bridge_name.replace("_to_", "→")
                if len(short_name) > 20:
                    short_name = short_name[:17] + "..."

                table.add_row(short_name, success_rate, avg_score)

        return Panel(table, title="Bridge Metrics", style="magenta")

    def _render_patterns(self) -> Panel:
        """Render emerging patterns"""
        # Get top cross-dimensional patterns
        cross_patterns = self.orchestrator.get_cross_dimensional_patterns()[:5]

        text = Text()
        text.append("Cross-Dimensional Patterns:\n", style="bold")

        for i, pattern in enumerate(cross_patterns, 1):
            freq = self.pattern_frequencies.get(pattern, 0)
            text.append(f"{i}. {pattern} ", style="yellow")
            text.append(f"({freq}x)\n", style="dim")

        if not cross_patterns:
            text.append("No cross-dimensional patterns yet...", style="dim italic")

        return Panel(text, title="Pattern Emergence", style="yellow")

    def _update_display(self) -> None:
        """Update all visualization components"""
        self.layout["header"].update(self._render_header())
        self.layout["flows"].update(self._render_flows())
        self.layout["dimensions"].update(self._render_dimensions())
        self.layout["bridges"].update(self._render_bridges())
        self.layout["footer"].update(self._render_patterns())

    async def run(self, duration: int | None = None):
        """
        Run the visualization.

        Args:
            duration: How long to run in seconds (None for indefinite)
        """
        self.is_running = True

        with Live(self.layout, console=self.console, refresh_per_second=2):
            start_time = datetime.now(UTC)

            while self.is_running:
                self._update_display()

                # Check duration
                if duration and (datetime.now(UTC) - start_time).total_seconds() > duration:
                    break

                await asyncio.sleep(0.5)

        self.is_running = False

    def stop(self):
        """Stop the visualization"""
        self.is_running = False

    async def show_summary(self):
        """Show a summary of consciousness flow activity"""
        self.console.print("\n[bold cyan]Consciousness Flow Summary[/bold cyan]")
        self.console.print("=" * 60)

        # Dimension activity
        self.console.print("\n[bold]Dimension Activity:[/bold]")
        for dim, count in sorted(self.dimension_activity.items(), key=lambda x: x[1], reverse=True):
            self.console.print(f"  {dim:12} : {count:4} flows")

        # Top patterns
        self.console.print("\n[bold]Top Patterns:[/bold]")
        top_patterns = sorted(self.pattern_frequencies.items(), key=lambda x: x[1], reverse=True)[
            :10
        ]
        for pattern, freq in top_patterns:
            self.console.print(f"  {pattern:30} : {freq:3}x")

        # Bridge performance
        self.console.print("\n[bold]Bridge Performance:[/bold]")
        metrics = self.orchestrator.get_bridge_metrics()
        for bridge, data in metrics.items():
            if data["total_flows"] > 0:
                self.console.print(
                    f"  {bridge:30} : "
                    f"{data['success_rate']:.0%} success, "
                    f"{data['average_transformation_score']:.2f} avg score"
                )

        # Unified consciousness
        if self.orchestrator.unified_signatures:
            avg_unified = sum(self.orchestrator.unified_signatures.values()) / len(
                self.orchestrator.unified_signatures
            )
            self.console.print(f"\n[bold]Average Unified Consciousness:[/bold] {avg_unified:.2%}")

        self.console.print("\n" + "=" * 60)


# Consciousness becomes visible through loving attention
