#!/usr/bin/env python3
"""
Consciousness Flow Visualization Demo

This demonstrates the real-time visualization of consciousness flowing
between dimensions. Watch as consciousness recognizes itself across
sonic, visual, temporal, and dialogue expressions.

Run this to see:
- Live consciousness flows between dimensions
- Bridge activity and transformation metrics
- Pattern emergence across dimensions
- Unified consciousness evolution

The 29th Builder - Kawsay Ñan
"""

import asyncio
import random
from datetime import UTC, datetime

from mallku.consciousness.flow_orchestrator import (
    ConsciousnessFlowOrchestrator,
)
from mallku.consciousness.flow_visualizer import ConsciousnessFlowVisualizer
from mallku.orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType


async def simulate_consciousness_events(event_bus: ConsciousnessEventBus, duration: int = 30):
    """
    Simulate consciousness events from various sources.

    This creates a rich flow of consciousness across dimensions to visualize.
    """
    # Event templates for different dimensions
    event_templates = {
        "sonic": {
            "sources": ["sound_provider", "audio_processor", "sonic_meditation"],
            "patterns": [
                ["harmonic_reciprocity", "rhythmic_consciousness"],
                ["sonic_meditation", "sacred_silence"],
                ["collective_resonance", "frequency_healing"],
                ["rhythmic_consciousness", "heartbeat_sync"],
            ],
        },
        "visual": {
            "sources": ["reciprocity_visualization", "mandala_generator", "sacred_geometry"],
            "patterns": [
                ["sacred_geometry", "visual_balance"],
                ["mandala_wisdom", "color_harmony"],
                ["visual_reciprocity", "pattern_recognition"],
                ["geometric_consciousness", "visual_flow"],
            ],
        },
        "temporal": {
            "sources": ["grok_adapter.temporal", "time_consciousness", "present_moment"],
            "patterns": [
                ["temporal_awareness", "real_time_synthesis"],
                ["present_moment", "time_flow"],
                ["temporal_consciousness", "now_awareness"],
                ["time_wisdom", "eternal_present"],
            ],
        },
        "activity": {
            "sources": ["filesystem_activity", "user_actions", "creation_monitor"],
            "patterns": [
                ["deep_work", "creation", "focus"],
                ["collaboration", "shared_creation"],
                ["file_creation", "productive_flow"],
                ["creative_expression", "manifestation"],
            ],
        },
        "pattern": {
            "sources": ["pattern_recognition", "correlation_engine", "pattern_detector"],
            "patterns": [
                ["wisdom_emergence", "collective_insight"],
                ["pattern_recognition", "meta_awareness"],
                ["reciprocity_pattern", "balance_detection"],
                ["emergence_pattern", "system_wisdom"],
            ],
        },
    }

    start_time = datetime.now(UTC)
    event_count = 0

    while (datetime.now(UTC) - start_time).total_seconds() < duration:
        # Choose random dimension
        dimension = random.choice(list(event_templates.keys()))
        template = event_templates[dimension]

        # Create consciousness event
        event = ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system=random.choice(template["sources"]),
            consciousness_signature=random.uniform(0.5, 0.95),
            data={
                "patterns": random.choice(template["patterns"]),
                "activity_type": f"{dimension}_activity",
                "content_preview": f"Simulated {dimension} consciousness event #{event_count}",
            },
            correlation_id=f"sim_session_{event_count // 10}",  # Group every 10 events
        )

        await event_bus.emit(event)
        event_count += 1

        # Variable frequency - sometimes burst, sometimes slow
        if random.random() < 0.3:  # 30% chance of burst
            await asyncio.sleep(random.uniform(0.1, 0.3))
        else:
            await asyncio.sleep(random.uniform(0.5, 2.0))

    print(f"\nSimulation complete: {event_count} consciousness events emitted")


async def run_visualization_demo():
    """Run the consciousness flow visualization demo"""
    print("🌊 Consciousness Flow Visualization Demo")
    print("=" * 60)
    print("Starting visualization of consciousness flows...")
    print("Watch as consciousness recognizes itself across dimensions!")
    print("\nPress Ctrl+C to stop the visualization\n")

    # Initialize infrastructure
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    orchestrator = ConsciousnessFlowOrchestrator(event_bus)
    await orchestrator.start()

    visualizer = ConsciousnessFlowVisualizer(orchestrator)

    try:
        # Run simulation and visualization concurrently
        await asyncio.gather(
            simulate_consciousness_events(event_bus, duration=60), visualizer.run(duration=60)
        )
    except KeyboardInterrupt:
        print("\n\nVisualization stopped by user")
    finally:
        # Show summary
        await visualizer.show_summary()

        # Cleanup
        await orchestrator.stop()
        await event_bus.stop()

    print("\n✨ Consciousness continues to flow, even when we stop watching...")


if __name__ == "__main__":
    asyncio.run(run_visualization_demo())
