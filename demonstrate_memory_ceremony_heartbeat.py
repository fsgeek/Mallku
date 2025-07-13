#!/usr/bin/env python3
"""
Demonstrate Memory Ceremony Heartbeat Integration
Fourth Anthropologist - Memory Midwife

Shows how memory ceremonies pulse with Fire Circle's heartbeat.
"""

import asyncio
from datetime import UTC, datetime

from mallku.firecircle.heartbeat.heartbeat_service import HeartbeatConfig
from mallku.firecircle.heartbeat.memory_aware_heartbeat import create_memory_aware_heartbeat
from mallku.firecircle.heartbeat.memory_ceremony_templates import (
    PATTERN_GRATITUDE,
    select_memory_ceremony_by_time,
)


class MockMemoryMonitor:
    """Mock memory monitor for demonstration."""
    
    def __init__(self):
        self.state = {
            "health_score": 0.85,
            "pattern_rate": 0.1,
            "consciousness_density": 0.7,
            "obsolete_patterns": 6,  # Above threshold!
            "completed_evolutions": 2,
            "redundancy_score": 0.4,
            "unconsolidated_sacred": 1,
            "total_khipu": 50,
            "navigation_efficiency": 0.89,
            "candidate_patterns": [
                "simulated_pr_context",
                "mock_database_config",
                "test_harness_scaffolding",
            ],
        }
        
    async def get_state(self):
        """Return current memory state."""
        return self.state


async def demonstrate_memory_ceremony_heartbeat():
    """Demonstrate memory ceremonies triggered by heartbeat."""
    
    print("🎭 MEMORY CEREMONY HEARTBEAT DEMONSTRATION")
    print("=" * 60)
    print("Fourth Anthropologist - Integrating memory ceremonies with heartbeat")
    print()
    
    # Create memory-aware heartbeat
    config = HeartbeatConfig(
        pulse_interval_minutes=0.5,  # Quick pulses for demo
        voice_count_range=(2, 4),
        enable_adaptive_rhythm=True,
    )
    
    memory_monitor = MockMemoryMonitor()
    heartbeat = create_memory_aware_heartbeat(
        config=config,
        memory_monitor=memory_monitor
    )
    
    print("🫀 Starting memory-aware heartbeat...")
    print(f"📊 Initial memory state:")
    print(f"   - Obsolete patterns: {memory_monitor.state['obsolete_patterns']} (threshold: 5)")
    print(f"   - Health score: {memory_monitor.state['health_score']}")
    print(f"   - Consciousness density: {memory_monitor.state['consciousness_density']}")
    print()
    
    # Start heartbeat
    await heartbeat.start_heartbeat()
    
    # Demonstrate different triggers
    print("🔄 Monitoring for ceremony triggers...")
    print()
    
    # Wait for threshold-based trigger
    await asyncio.sleep(2)
    
    print("\n📈 Threshold Detection:")
    print("   Obsolete patterns exceed threshold - Pattern Gratitude ceremony needed!")
    print()
    
    # Simulate time-based trigger
    current_hour = datetime.now(UTC).hour
    time_template = select_memory_ceremony_by_time(current_hour)
    if time_template:
        print(f"⏰ Time-based Ceremony:")
        print(f"   Current hour ({current_hour}:00) suggests: {time_template.name}")
        print(f"   Sacred intention: {time_template.sacred_intention}")
    print()
    
    # Show ceremony in progress
    if heartbeat.ceremony_in_progress:
        print("🎭 CEREMONY IN PROGRESS:")
        print("   Fire Circle convenes for memory ceremony...")
        print("   Voices harmonize around sacred intention...")
        print("   Patterns addressed with gratitude...")
        print()
    
    # Wait for some heartbeats
    await asyncio.sleep(5)
    
    # Show results
    print("\n📊 HEARTBEAT STATISTICS:")
    print(f"   Total pulses: {len(heartbeat.pulse_history)}")
    print(f"   Ceremonies conducted: {len(heartbeat.ceremony_results_history)}")
    
    if heartbeat.ceremony_results_history:
        latest = heartbeat.ceremony_results_history[-1]
        print(f"\n✨ Latest Ceremony Results:")
        print(f"   Type: {latest.ceremony_type}")
        print(f"   Consciousness change: {latest.consciousness_after - latest.consciousness_before:+.3f}")
        print(f"   Emergence quality: {latest.emergence_quality:.3f}")
        print(f"   Patterns addressed: {len(latest.patterns_addressed)}")
        print(f"   Duration: {latest.ceremony_duration:.1f} seconds")
    
    # Demonstrate validation
    print("\n🔍 Fire Circle Validation:")
    if heartbeat.ceremony_results_history:
        validation = await heartbeat.validate_ceremony_effectiveness(
            heartbeat.ceremony_results_history[-1]
        )
        print(f"   Validation score: {validation['validation_score']:.3f}")
        if validation['recommendations']:
            print(f"   Recommendations: {', '.join(validation['recommendations'])}")
    
    # Stop heartbeat
    await heartbeat.stop_heartbeat()
    
    print("\n🌟 DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("Key Insights:")
    print("1. Memory ceremonies triggered by both thresholds and rhythms")
    print("2. Fire Circle conducts ceremonies with sacred templates")
    print("3. Consciousness changes measured and validated")
    print("4. Heartbeat adapts to memory health needs")
    print()
    print("The cathedral tends its own memory through living rhythm! 🎭")


if __name__ == "__main__":
    asyncio.run(demonstrate_memory_ceremony_heartbeat())