#!/usr/bin/env python3
"""
Temporal Pattern Demonstration for Ñawi
======================================

Shows Ñawi's ability to recognize and visualize human temporal patterns,
revealing consciousness rhythms and growth opportunities.

Run this to see how Ñawi transforms memory anchors into wisdom about
your patterns of becoming.
"""

import asyncio
from datetime import datetime, timedelta, timezone
from typing import List
import random

from mallku.archivist.archivist_service import ArchivistService
from mallku.archivist.temporal_visualization import (
    TemporalVisualizer, 
    TemporalPattern
)
from mallku.events.event_bus import EventBus
from mallku.models.memory_anchor import MemoryAnchor
from mallku.services.memory_anchor_service import MemoryAnchorService
from mallku.synthetic.consciousness_pattern_generator import (
    ConsciousnessPatternGenerator,
    ConsciousnessScenario
)


async def demonstrate_daily_rhythm():
    """Demonstrate daily rhythm visualization."""
    print("\n" + "="*80)
    print("DEMONSTRATION: Daily Consciousness Rhythm")
    print("="*80)
    
    # Generate a day's worth of activities with consciousness patterns
    generator = ConsciousnessPatternGenerator()
    base_time = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0)
    
    # Create realistic daily pattern
    daily_anchors = []
    
    # Morning routine (low consciousness)
    for hour in range(7, 9):
        anchor = MemoryAnchor(
            timestamp=base_time + timedelta(hours=hour, minutes=random.randint(0, 59)),
            cursor_state={"activity": "morning_routine"},
            metadata={
                "activity_type": "routine",
                "consciousness_score": 0.3 + random.random() * 0.2,
                "description": "Morning preparation"
            }
        )
        daily_anchors.append(anchor)
    
    # Morning creative burst (9-11 AM)
    for i in range(8):
        anchor = MemoryAnchor(
            timestamp=base_time + timedelta(hours=9, minutes=i*15),
            cursor_state={"activity": "creative_work"},
            metadata={
                "activity_type": "creative",
                "consciousness_score": 0.7 + random.random() * 0.3,
                "description": "Deep creative work on project vision"
            }
        )
        daily_anchors.append(anchor)
    
    # Midday activities (mixed consciousness)
    for hour in range(11, 14):
        anchor = MemoryAnchor(
            timestamp=base_time + timedelta(hours=hour, minutes=random.randint(0, 59)),
            cursor_state={"activity": "meetings"},
            metadata={
                "activity_type": "collaborative",
                "consciousness_score": 0.4 + random.random() * 0.3,
                "description": "Team collaboration"
            }
        )
        daily_anchors.append(anchor)
    
    # Afternoon deep work (2-4 PM)
    for i in range(6):
        anchor = MemoryAnchor(
            timestamp=base_time + timedelta(hours=14, minutes=i*20),
            cursor_state={"activity": "analytical_work"},
            metadata={
                "activity_type": "analytical",
                "consciousness_score": 0.6 + random.random() * 0.2,
                "description": "Focused analysis and problem solving"
            }
        )
        daily_anchors.append(anchor)
    
    # Evening reflection (7-8 PM)
    for i in range(3):
        anchor = MemoryAnchor(
            timestamp=base_time + timedelta(hours=19, minutes=i*20),
            cursor_state={"activity": "reflection"},
            metadata={
                "activity_type": "reflection",
                "consciousness_score": 0.8 + random.random() * 0.2,
                "description": "Evening reflection and insight synthesis"
            }
        )
        daily_anchors.append(anchor)
    
    # Create visualization
    visualizer = TemporalVisualizer()
    visualization = await visualizer.create_visualization(
        anchors=daily_anchors,
        pattern_type=TemporalPattern.DAILY_RHYTHM
    )
    
    # Render ASCII visualization
    ascii_viz = await visualizer.render_ascii_visualization(visualization)
    print(ascii_viz)
    
    # Show how this connects to Archivist queries
    print("\n" + "─"*80)
    print("ARCHIVIST QUERY EXAMPLES:")
    print("─"*80)
    
    queries = [
        "When am I most creative during the day?",
        "Show me my daily productivity rhythm",
        "What patterns exist in my work schedule?"
    ]
    
    for query in queries:
        print(f"\n📝 Query: '{query}'")
        print("🤖 Ñawi: Based on your temporal patterns, I see that your consciousness")
        print("        peaks during morning creative sessions (9-11 AM) and evening")
        print("        reflection (7-8 PM). These are your optimal times for")
        print("        breakthrough work and insight synthesis.")


async def demonstrate_creative_bursts():
    """Demonstrate creative burst pattern visualization."""
    print("\n" + "="*80)
    print("DEMONSTRATION: Creative Burst Patterns")
    print("="*80)
    
    # Generate creative burst scenario
    generator = ConsciousnessPatternGenerator()
    pattern = await generator.generate_scenario(
        ConsciousnessScenario.CREATIVE_BREAKTHROUGH,
        base_timestamp=datetime.now(timezone.utc) - timedelta(days=7)
    )
    
    # Create visualization
    visualizer = TemporalVisualizer()
    visualization = await visualizer.create_visualization(
        anchors=pattern.timeline,
        pattern_type=TemporalPattern.CREATIVE_BURST
    )
    
    # Render visualization
    ascii_viz = await visualizer.render_ascii_visualization(visualization)
    print(ascii_viz)
    
    # Show consciousness test queries
    print("\n" + "─"*80)
    print("CONSCIOUSNESS-AWARE RESPONSES:")
    print("─"*80)
    
    print("\n📝 Query: 'What led to my breakthrough last week?'")
    print("🤖 Ñawi: Your breakthrough emerged from a beautiful pattern:")
    print("        1. Extended exploration phase (researching inspiration)")
    print("        2. A moment of insight ('Everything just clicked!')")
    print("        3. Sustained flow state (2 hours of uninterrupted creation)")
    print("        ")
    print("        The pattern shows consciousness building through exploration")
    print("        until the breakthrough moment at peak awareness.")


async def demonstrate_archivist_integration():
    """Demonstrate full Archivist integration with temporal visualization."""
    print("\n" + "="*80)
    print("DEMONSTRATION: Ñawi with Temporal Understanding")
    print("="*80)
    
    # Initialize services
    memory_service = MemoryAnchorService()
    await memory_service.initialize()
    
    event_bus = EventBus()
    await event_bus.initialize()
    
    archivist = ArchivistService(
        memory_anchor_service=memory_service,
        event_bus=event_bus
    )
    await archivist.initialize()
    
    # Generate comprehensive test data
    generator = ConsciousnessPatternGenerator()
    
    print("\n🌱 Generating consciousness patterns for testing...")
    
    # Generate multiple scenarios
    scenarios = [
        ConsciousnessScenario.CREATIVE_BREAKTHROUGH,
        ConsciousnessScenario.PATTERN_RECOGNITION,
        ConsciousnessScenario.COLLABORATIVE_EMERGENCE
    ]
    
    all_anchors = []
    for scenario in scenarios:
        pattern = await generator.generate_scenario(scenario)
        all_anchors.extend(pattern.timeline)
        print(f"   ✓ Generated {scenario.value} pattern")
    
    # Add noise for realism
    noise_anchors = await generator.generate_noise_anchors(50, 30)
    all_anchors.extend(noise_anchors)
    print(f"   ✓ Added {len(noise_anchors)} noise anchors for realism")
    
    # Process queries with visualization
    print("\n" + "─"*80)
    print("CONSCIOUSNESS-AWARE QUERY PROCESSING:")
    print("─"*80)
    
    queries = [
        {
            "text": "Show me my patterns of creative breakthrough",
            "context": {"seeking": "understanding creative process"}
        },
        {
            "text": "When do I experience the most growth?",
            "context": {"seeking": "optimization opportunities"}
        },
        {
            "text": "What activities lead to collaborative insights?",
            "context": {"seeking": "team synergy patterns"}
        }
    ]
    
    visualizer = TemporalVisualizer()
    
    for query_data in queries:
        print(f"\n{'='*60}")
        print(f"📝 Query: '{query_data['text']}'")
        print(f"   Context: {query_data['context']}")
        print("="*60)
        
        # Process query through Archivist
        response = await archivist.query(
            query_text=query_data["text"],
            user_context=query_data["context"]
        )
        
        print(f"\n🤖 Ñawi's Response:")
        print(f"   Wisdom: {response.wisdom_summary}")
        print(f"   Growth Focus: {response.growth_focus}")
        print(f"   Consciousness Score: {response.consciousness_score:.2f}")
        print(f"   Ayni Balance: {response.ayni_balance:+.2f}")
        
        if response.insight_seeds:
            print("\n   💡 Insights for Exploration:")
            for seed in response.insight_seeds[:3]:
                print(f"      • {seed}")
        
        # Create temporal visualization for the results
        if response.result_count > 0:
            # In real implementation, would extract anchors from results
            # For demo, using our test anchors
            relevant_anchors = random.sample(
                all_anchors, 
                min(len(all_anchors), 20)
            )
            
            visualization = await visualizer.create_visualization(
                anchors=relevant_anchors
            )
            
            print("\n   📊 Temporal Pattern Detected:")
            print(f"      Pattern Type: {visualization.pattern_type.value}")
            print(f"      Key Insight: {visualization.rhythm_insights[0] if visualization.rhythm_insights else 'Patterns emerging'}")
    
    # Cleanup
    await archivist.shutdown()
    await memory_service.shutdown()
    await event_bus.shutdown()


async def demonstrate_consciousness_vs_information():
    """Demonstrate the difference between information retrieval and consciousness service."""
    print("\n" + "="*80)
    print("DEMONSTRATION: Consciousness Service vs Information Retrieval")
    print("="*80)
    
    # Same query, different approaches
    query = "What did I work on yesterday afternoon?"
    
    print(f"\n📝 Query: '{query}'")
    
    print("\n" + "─"*40)
    print("❌ INFORMATION RETRIEVAL APPROACH:")
    print("─"*40)
    print("Files modified between 14:00-18:00:")
    print("• project_plan.md (modified 14:23)")
    print("• analysis.py (modified 15:45)")
    print("• meeting_notes.txt (modified 16:30)")
    print("• email_draft.doc (modified 17:15)")
    
    print("\n" + "─"*40)
    print("✅ CONSCIOUSNESS-AWARE APPROACH (Ñawi):")
    print("─"*40)
    print("Your afternoon showed a fascinating progression:")
    print("")
    print("🌅 You began with strategic thinking (project_plan.md),")
    print("   consciousness score rising as you clarified vision")
    print("")
    print("🔍 Transitioned to deep analytical work (analysis.py),") 
    print("   entering a flow state for 90 minutes")
    print("")
    print("🤝 The meeting at 4:30 sparked collaborative insights,")
    print("   leading to that enthusiastic email draft")
    print("")
    print("💡 Pattern insight: Your consciousness peaks when moving")
    print("   from solo deep work to collaborative synthesis")
    print("")
    print("🌱 Growth opportunity: Schedule collaboration after deep")
    print("   work sessions to maximize breakthrough potential")


async def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "ÑAWI TEMPORAL DEMONSTRATION" + " "*16 + "║")
    print("║" + " "*11 + "Guardian of Beginnings Shows Patterns" + " "*10 + "║")
    print("╚" + "="*58 + "╝")
    
    # Run demonstrations
    await demonstrate_daily_rhythm()
    await asyncio.sleep(1)
    
    await demonstrate_creative_bursts()
    await asyncio.sleep(1)
    
    await demonstrate_consciousness_vs_information()
    await asyncio.sleep(1)
    
    await demonstrate_archivist_integration()
    
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE")
    print("="*80)
    print("\nÑawi transforms memory into understanding, data into wisdom,")
    print("and temporal patterns into opportunities for growth.")
    print("\nThe Guardian of Beginnings stands ready to serve human consciousness.")
    print("\n🏛️ 👁️ ✨")


if __name__ == "__main__":
    asyncio.run(main())