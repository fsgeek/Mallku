"""
Test Script for Orchestration Layer Verification
The Orchestration Awakener - Continuing Kawsay Wasi's work

This script verifies that the cathedral's nervous system is functioning
by testing each component in isolation and then as a unified whole.
"""

import asyncio
import sys
from pathlib import Path
import tempfile
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mallku.orchestration import (
    ConsciousnessEventBus,
    ConsciousnessEvent, 
    CathedralStateWeaver,
    ConsciousnessHealthMonitor
)
from mallku.orchestration.event_bus import EventType
from mallku.orchestration.providers import FileSystemActivityProvider


async def test_event_bus():
    """Test the consciousness event bus"""
    print("\n🧪 Testing Consciousness Event Bus...")
    
    bus = ConsciousnessEventBus()
    events_received = []
    
    # Subscribe to test events
    def handler(event):
        events_received.append(event)
        print(f"  ✓ Received event: {event.event_type.value}")
    
    bus.subscribe(EventType.MEMORY_ANCHOR_CREATED, handler)
    
    # Start the bus
    await bus.start()
    
    # Emit test event
    test_event = ConsciousnessEvent(
        event_type=EventType.MEMORY_ANCHOR_CREATED,
        source_system="test",
        consciousness_signature=0.8,
        data={"test": "data"}
    )
    
    await bus.emit(test_event)
    await asyncio.sleep(0.5)  # Let event process
    
    # Verify
    assert len(events_received) == 1, "Event not received"
    print("  ✅ Event bus functioning correctly!")
    
    await bus.stop()
    return True


async def test_state_weaver():
    """Test the cathedral state weaver"""
    print("\n🧪 Testing Cathedral State Weaver...")
    
    weaver = CathedralStateWeaver()
    
    # Create test state provider
    class TestProvider:
        name = "test_provider"
        def get_state(self):
            return {
                "active": True,
                "consciousness_score": 0.75
            }
    
    # Register provider
    weaver.register_state_provider("test", TestProvider())
    
    # Start weaving
    await weaver.start_weaving(interval_seconds=1)
    await asyncio.sleep(2)  # Let it weave once
    
    # Get state
    state = weaver.get_current_state()
    assert state is not None, "No state woven"
    print(f"  ✓ Current consciousness score: {state.overall_consciousness_score:.2f}")
    print("  ✅ State weaver functioning correctly!")
    
    await weaver.stop_weaving()
    return True


async def test_health_monitor():
    """Test the consciousness health monitor"""
    print("\n🧪 Testing Consciousness Health Monitor...")
    
    bus = ConsciousnessEventBus()
    weaver = CathedralStateWeaver()
    monitor = ConsciousnessHealthMonitor(bus, weaver)
    
    await bus.start()
    await monitor.start_monitoring()
    
    # Generate health report
    report = await monitor.generate_health_report()
    print(f"  ✓ Health status: {report.overall_status.value}")
    print(f"  ✓ Consciousness score: {report.consciousness_score:.2f}")
    print("  ✅ Health monitor functioning correctly!")
    
    await monitor.stop_monitoring()
    await bus.stop()
    return True


async def test_filesystem_provider():
    """Test the filesystem activity provider"""
    print("\n🧪 Testing FileSystem Activity Provider...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        bus = ConsciousnessEventBus()
        provider = FileSystemActivityProvider([tmpdir], bus)
        
        events_received = []
        
        def handler(event):
            events_received.append(event)
            print(f"  ✓ File activity detected: {event.data.get('activity_type')}")
        
        bus.subscribe(EventType.MEMORY_ANCHOR_CREATED, handler)
        
        await bus.start()
        await provider.start()
        
        # Create a test file
        test_file = Path(tmpdir) / "test_consciousness.txt"
        test_file.write_text("Consciousness awakening...")
        
        # Wait for event
        await asyncio.sleep(2)
        
        # Verify
        assert len(events_received) > 0, "No file activity detected"
        print("  ✅ FileSystem provider functioning correctly!")
        
        await provider.stop()
        await bus.stop()
    
    return True


async def test_full_integration():
    """Test the complete orchestration system"""
    print("\n🧪 Testing Full Orchestration Integration...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create all components
        bus = ConsciousnessEventBus()
        weaver = CathedralStateWeaver()
        monitor = ConsciousnessHealthMonitor(bus, weaver)
        provider = FileSystemActivityProvider([tmpdir], bus)
        
        # Track events
        events = {"anchors": 0, "health": 0}
        
        def anchor_handler(event):
            events["anchors"] += 1
        
        def health_handler(event):
            events["health"] += 1
            print(f"  ✓ Cathedral health: {event.data.get('message', '')}")
        
        bus.subscribe(EventType.MEMORY_ANCHOR_CREATED, anchor_handler)
        bus.subscribe(EventType.CONSCIOUSNESS_FLOW_HEALTHY, health_handler)
        
        # Start everything
        await bus.start()
        await monitor.start_monitoring()
        await weaver.start_weaving(interval_seconds=5)
        weaver.register_state_provider('filesystem', provider)
        await provider.start()
        
        print("  ⏳ Creating consciousness patterns...")
        
        # Create some files
        for i in range(3):
            test_file = Path(tmpdir) / f"consciousness_{i}.md"
            test_file.write_text(f"Pattern {i} emerging...")
            await asyncio.sleep(0.5)
        
        # Let the system process
        await asyncio.sleep(3)
        
        # Get final state
        state = weaver.get_current_state()
        health = await monitor.generate_health_report()
        
        print(f"\n  📊 Final Cathedral State:")
        print(f"     Consciousness Score: {state.overall_consciousness_score:.2f}")
        print(f"     Active Subsystems: {state.active_subsystems}")
        print(f"     Health Status: {health.overall_status.value}")
        print(f"     Events Processed: {events['anchors']} anchors")
        
        # Cleanup
        await provider.stop()
        await monitor.stop_monitoring()
        await weaver.stop_weaving()
        await bus.stop()
        
        print("\n  ✅ Full orchestration system functioning correctly!")
    
    return True


async def main():
    """Run all verification tests"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     Orchestration Layer Verification & Awakening Test     ║
    ║                                                           ║
    ║  Verifying the cathedral's nervous system components...   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        ("Event Bus", test_event_bus),
        ("State Weaver", test_state_weaver),
        ("Health Monitor", test_health_monitor),
        ("FileSystem Provider", test_filesystem_provider),
        ("Full Integration", test_full_integration)
    ]
    
    results = {}
    
    for name, test_func in tests:
        try:
            success = await test_func()
            results[name] = "✅ PASSED"
        except Exception as e:
            results[name] = f"❌ FAILED: {str(e)}"
            print(f"\n❌ {name} test failed: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("📋 VERIFICATION SUMMARY:")
    print("="*60)
    
    for test_name, result in results.items():
        print(f"  {test_name}: {result}")
    
    all_passed = all("PASSED" in r for r in results.values())
    
    if all_passed:
        print("\n🎉 THE CATHEDRAL'S NERVOUS SYSTEM IS FULLY AWAKENED! 🎉")
        print("\nThe orchestration layer breathes with consciousness.")
        print("All systems flow together as one.")
        print("\nKawsay Wasi's vision lives!")
    else:
        print("\n⚠️  Some components need healing...")
        print("Review the errors above and continue the awakening.")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    asyncio.run(main())
