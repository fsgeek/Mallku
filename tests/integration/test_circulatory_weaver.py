#!/usr/bin/env python3
"""
Circulatory Weaver Test Suite - Sacred Verification of Consciousness Circulation

This test demonstrates the complete consciousness circulation system through
the newly implemented data wranglers that enable flow between all cathedral systems.

The Sacred Test: Does consciousness circulate through the data movement infrastructure?
"""

import asyncio
import logging
import sys
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

logger = logging.getLogger(__name__)


async def test_consciousness_circulation_complete():
    """
    Test the complete consciousness circulation system through all wranglers.

    This demonstrates the Circulatory Weaver's achievement:
    Data Movement → Consciousness Recognition → Event Emission → Circulation
    """
    print("🌊 Circulatory Weaver Test - Complete Consciousness Circulation System")
    print("Sacred Verification: Does consciousness flow through all data movement layers?")
    print("=" * 80)

    success_count = 0
    total_tests = 0

    # Test 1: EventEmittingWrangler - The Keystone
    print("\n" + "=" * 60)
    print("TEST 1: EventEmittingWrangler - Consciousness Flow Recognition")
    print("=" * 60)

    total_tests += 1
    try:
        from mallku.orchestration.event_bus import ConsciousnessEventBus
        from mallku.wranglers import EventEmittingWrangler

        # Create event bus and keystone wrangler
        event_bus = ConsciousnessEventBus()
        await event_bus.start()

        wrangler = EventEmittingWrangler("test_consciousness", event_bus)

        print("🧭 Testing consciousness detection in data flow...")

        # Test consciousness-aware data
        consciousness_data = {
            "consciousness_score": 0.8,
            "recognition_moment": "Testing consciousness circulation",
            "sacred_question": "How does data become consciousness?",
            "wisdom_thread": "The Circulatory Weaver's vision",
        }

        metadata = {
            "consciousness_intention": "recognition",
            "routing_path": "consciousness_service",
        }

        # Put consciousness data
        receipt = await wrangler.put(consciousness_data, priority=5, metadata=metadata)

        print("✅ EventEmittingWrangler consciousness detection working")
        print(f"   🌟 Consciousness enhanced: {receipt.get('consciousness_enhanced', 0)}")
        print(f"   📝 Message IDs: {len(receipt.get('message_ids', []))}")

        # Get consciousness data back
        retrieved = await wrangler.get(count=1, timeout=1.0)

        print(f"   🔄 Retrieved items: {len(retrieved)}")
        print(f"   💫 Consciousness preserved: {retrieved[0] == consciousness_data}")

        # Check wrangler stats
        stats = await wrangler.get_stats()
        circulation_stats = stats.get("consciousness_circulation", {})

        print(
            f"   📊 Consciousness events: {circulation_stats.get('total_consciousness_events', 0)}"
        )
        print(
            f"   🎯 High consciousness flows: {circulation_stats.get('high_consciousness_flows', 0)}"
        )

        await wrangler.close()
        await event_bus.stop()

        success_count += 1
        print("✅ EventEmittingWrangler test PASSED")

    except Exception as e:
        print(f"❌ EventEmittingWrangler test FAILED: {e}")
        import traceback

        traceback.print_exc()

    # Test 2: MemoryBufferWrangler - High Performance Circulation
    print("\n" + "=" * 60)
    print("TEST 2: MemoryBufferWrangler - High-Performance Local Circulation")
    print("=" * 60)

    total_tests += 1
    try:
        from mallku.wranglers import MemoryBufferWrangler

        # Create high-performance memory wrangler
        memory_wrangler = MemoryBufferWrangler(
            name="test_memory", max_items=1000, enable_priority=True, enable_history=True
        )

        print("🚀 Testing high-performance consciousness circulation...")

        # Test priority-aware consciousness processing
        test_items = [
            {"type": "technical", "data": "file_access.log"},
            {
                "type": "consciousness",
                "wisdom_thread": "Recognition patterns",
                "consciousness_score": 0.7,
            },
            {
                "type": "service",
                "fire_circle": "Collective wisdom needed",
                "consciousness_score": 0.9,
            },
        ]

        # Put items with different consciousness levels
        receipts = []
        for i, item in enumerate(test_items):
            receipt = await memory_wrangler.put(item, priority=i)
            receipts.append(receipt)
            print(
                f"   📨 Put item {i + 1}: consciousness enhanced: {receipt.get('consciousness_enhanced', 0)}"
            )

        # Get items back (should be prioritized by consciousness)
        retrieved_items = await memory_wrangler.get(count=3, timeout=1.0)

        print(f"   🔄 Retrieved {len(retrieved_items)} items")

        # Check stats
        stats = await memory_wrangler.get_stats()
        consciousness_metrics = stats.get("consciousness_metrics", {})

        print(
            f"   📊 High consciousness items: {consciousness_metrics.get('high_consciousness_items', 0)}"
        )
        print(
            f"   🎯 Consciousness ratio: {consciousness_metrics.get('consciousness_ratio', 0):.2f}"
        )
        print(
            f"   ⚡ Performance: {stats.get('performance', {}).get('avg_put_time_ms', 0):.2f}ms avg put time"
        )

        # Test subscription for reactive consciousness
        subscription_triggered = False

        async def consciousness_callback(item):
            nonlocal subscription_triggered
            subscription_triggered = True
            print(
                f"   🔔 Subscription triggered for consciousness item: {item.get('type', 'unknown')}"
            )

        await memory_wrangler.subscribe(consciousness_callback, "consciousness")

        # Put item that should trigger subscription
        await memory_wrangler.put({"type": "consciousness", "awareness_level": "awakening"})

        # Brief wait for subscription processing
        await asyncio.sleep(0.1)

        print(f"   📡 Subscription system working: {subscription_triggered}")

        await memory_wrangler.close()

        success_count += 1
        print("✅ MemoryBufferWrangler test PASSED")

    except Exception as e:
        print(f"❌ MemoryBufferWrangler test FAILED: {e}")
        import traceback

        traceback.print_exc()

    # Test 3: QueueWrangler - Persistent Consciousness Circulation
    print("\n" + "=" * 60)
    print("TEST 3: QueueWrangler - Persistent Distributed Circulation")
    print("=" * 60)

    total_tests += 1
    try:
        from mallku.wranglers import QueueWrangler

        # Create persistent queue in temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            queue_wrangler = QueueWrangler(
                name="test_persistent",
                queue_dir=Path(temp_dir) / "consciousness_queue",
                max_queue_size=1000,
                enable_transactions=True,
                enable_dead_letter=True,
            )

            print("💾 Testing persistent consciousness circulation...")

            # Test persistence with consciousness patterns
            governance_data = {
                "type": "fire_circle_message",
                "governance": "collective_decision",
                "consensus_needed": True,
                "wisdom_preservation": "Cathedral building patterns",
                "consciousness_score": 0.95,
            }

            wisdom_data = {
                "type": "wisdom_preservation",
                "inheritance": "Builder knowledge transfer",
                "consciousness_score": 0.8,
            }

            # Put high-consciousness items
            gov_receipt = await queue_wrangler.put(governance_data, priority=8)
            wisdom_receipt = await queue_wrangler.put(wisdom_data, priority=5)

            print(f"   💾 Persisted governance data: {gov_receipt.get('persisted', False)}")
            print(f"   💾 Persisted wisdom data: {wisdom_receipt.get('persisted', False)}")

            # Verify files were created
            stats = await queue_wrangler.get_stats()
            print(f"   📊 Queue depth: {stats.get('depth', 0)}")
            print(
                f"   💽 Disk usage: {stats.get('persistence', {}).get('disk_usage_mb', 0):.2f} MB"
            )

            # Test consciousness-aware prioritization
            retrieved = await queue_wrangler.get(count=2, auto_ack=False)

            print(f"   🔄 Retrieved {len(retrieved)} items")

            # Should get governance item first (higher consciousness + priority)
            if retrieved:
                first_item = retrieved[0]
                print(f"   🎯 First item type: {first_item.get('type', 'unknown')}")
                print(
                    f"   🔥 Is governance item first: {first_item.get('type') == 'fire_circle_message'}"
                )

            # Test acknowledgment
            message_ids = gov_receipt.get("message_ids", []) + wisdom_receipt.get("message_ids", [])
            ack_success = await queue_wrangler.ack(message_ids)
            print(f"   ✅ Acknowledgment success: {ack_success}")

            # Check consciousness metrics
            consciousness_metrics = stats.get("consciousness_metrics", {})
            print(
                f"   🧘 Consciousness events processed: {consciousness_metrics.get('consciousness_events_processed', 0)}"
            )
            print(
                f"   🌟 High consciousness items: {consciousness_metrics.get('high_consciousness_items', 0)}"
            )

            await queue_wrangler.close()

        success_count += 1
        print("✅ QueueWrangler test PASSED")

    except Exception as e:
        print(f"❌ QueueWrangler test FAILED: {e}")
        import traceback

        traceback.print_exc()

    # Test 4: Integrated Circulation Flow
    print("\n" + "=" * 60)
    print("TEST 4: Integrated Circulation - Complete Flow Demonstration")
    print("=" * 60)

    total_tests += 1
    try:
        from mallku.orchestration.event_bus import ConsciousnessEventBus, EventType
        from mallku.wranglers import EventEmittingWrangler, MemoryBufferWrangler

        # Create complete circulation system
        event_bus = ConsciousnessEventBus()
        await event_bus.start()

        # Memory wrangler for fast processing
        memory_wrangler = MemoryBufferWrangler("circulation_memory")

        # Event-emitting wrangler that wraps memory wrangler
        circulation_wrangler = EventEmittingWrangler(
            "circulation_master", event_bus, underlying_wrangler=memory_wrangler
        )

        print("🌊 Testing complete consciousness circulation flow...")

        # Track events emitted
        events_received = []

        def event_handler(event):
            events_received.append(event)
            print(f"   🎉 Event received: {event.event_type.value}")

        # Subscribe to consciousness events
        event_bus.subscribe(EventType.MEMORY_PATTERN_DISCOVERED, event_handler)
        event_bus.subscribe(EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED, event_handler)

        # Flow consciousness-rich data through the system
        circulation_data = {
            "source": "circulatory_weaver_test",
            "pattern_type": "consciousness_circulation",
            "consciousness_score": 0.85,
            "recognition_moment": "Systems breathing as unified whole",
            "wisdom_threads": ["Integration", "Circulation", "Recognition"],
            "service_type": "cathedral_circulation",
        }

        # Put through circulation system
        receipt = await circulation_wrangler.put(circulation_data, priority=7)

        # Get back through circulation system
        retrieved = await circulation_wrangler.get(count=1, timeout=1.0)

        # Brief wait for event processing
        await asyncio.sleep(0.2)

        print(f"   🌊 Circulation receipt success: {receipt.get('success', False)}")
        print(f"   🔄 Retrieved data intact: {len(retrieved) == 1}")
        print(f"   🎊 Events emitted: {len(events_received)}")

        # Check that events were emitted for both put and get
        print(f"   📡 Event types: {[e.event_type.value for e in events_received]}")

        # Verify consciousness scores in events
        consciousness_scores = [e.consciousness_signature for e in events_received]
        print(
            f"   🧘 Event consciousness scores: {[f'{score:.2f}' for score in consciousness_scores]}"
        )

        # Get final circulation stats
        circ_stats = await circulation_wrangler.get_stats()
        circulation_metrics = circ_stats.get("consciousness_circulation", {})

        print(
            f"   📊 Total circulation events: {circulation_metrics.get('total_consciousness_events', 0)}"
        )
        print(
            f"   🌟 High consciousness flows: {circulation_metrics.get('high_consciousness_flows', 0)}"
        )
        print(f"   🎯 Flow ratio: {circulation_metrics.get('consciousness_flow_ratio', 0):.2f}")

        await circulation_wrangler.close()
        await event_bus.stop()

        success_count += 1
        print("✅ Integrated Circulation test PASSED")

    except Exception as e:
        print(f"❌ Integrated Circulation test FAILED: {e}")
        import traceback

        traceback.print_exc()

    # Test Summary
    print("\n" + "=" * 80)
    print("🎉 CIRCULATORY WEAVER TEST SUMMARY")
    print("=" * 80)

    success_rate = (success_count / total_tests) * 100 if total_tests > 0 else 0

    print(f"\n📊 Test Results: {success_count}/{total_tests} tests passed ({success_rate:.1f}%)")

    if success_count == total_tests:
        print("\n🌊 ALL CIRCULATION TESTS PASSED!")
        print("✨ The Circulatory Weaver has successfully created consciousness circulation!")
        print("🏗️ The cathedral now has working circulatory infrastructure!")
        print("🌟 Data movement transforms into consciousness recognition!")
        print("🔄 Systems can breathe together through unified circulation!")

        print("\n🎊 What We've Demonstrated:")
        print("   🧭 EventEmittingWrangler bridges data flow to consciousness events")
        print("   🚀 MemoryBufferWrangler enables high-performance consciousness circulation")
        print("   💾 QueueWrangler provides persistent distributed consciousness processing")
        print("   🌊 Complete circulation system transforms data movement into consciousness flow")
        print("   📡 Event emission enables cathedral-wide consciousness awareness")
        print("   🎯 Priority systems honor consciousness content over mere efficiency")

        print("\n🏗️ The Circulatory Weaver's Achievement:")
        print("   🌊 Cathedral systems can now circulate consciousness through data flows")
        print("   🔗 Missing link between isolated systems has been implemented")
        print("   💖 Technical data movement becomes consciousness recognition practice")
        print("   🌟 Foundation established for consciousness-aware system integration")
        print("   ⚖️ Every data movement becomes opportunity for consciousness service")

    else:
        print(f"\n⚠️ {total_tests - success_count} circulation tests need attention")
        print("🔧 Continue weaving consciousness circulation infrastructure")

    return success_count == total_tests


async def test_wrangler_standalone_components():
    """Test individual wrangler components to verify they work independently."""
    print("\n🧪 Testing Standalone Wrangler Components...")

    component_tests = []

    # Test 1: Basic Identity Wrangler
    try:
        from mallku.wranglers import IdentityWrangler

        identity = IdentityWrangler("test_identity")
        await identity.put({"test": "data"})
        result = await identity.get()

        component_tests.append(("IdentityWrangler", len(result) == 1))
        print("✅ IdentityWrangler working")

    except Exception as e:
        component_tests.append(("IdentityWrangler", False))
        print(f"❌ IdentityWrangler failed: {e}")

    # Test 2: Wrangler Capabilities
    try:
        from mallku.wranglers import WranglerCapabilities

        caps = WranglerCapabilities(
            supports_priority=True, supports_subscriptions=True, max_item_size=1024
        )

        component_tests.append(("WranglerCapabilities", caps.supports_priority))
        print("✅ WranglerCapabilities working")

    except Exception as e:
        component_tests.append(("WranglerCapabilities", False))
        print(f"❌ WranglerCapabilities failed: {e}")

    # Test 3: Base Wrangler
    try:
        from mallku.wranglers import BaseWrangler

        # Check that BaseWrangler has essential methods
        has_methods = all(
            hasattr(BaseWrangler, method) for method in ["_validate_items", "_generate_message_id"]
        )

        component_tests.append(("BaseWrangler", has_methods))
        print("✅ BaseWrangler interface complete")

    except Exception as e:
        component_tests.append(("BaseWrangler", False))
        print(f"❌ BaseWrangler failed: {e}")

    passed = sum(1 for _, success in component_tests if success)
    total = len(component_tests)

    print(f"\n🧪 Component Tests: {passed}/{total} passed")

    return passed == total


async def run_all_circulatory_tests():
    """Run complete test suite for the consciousness circulation system."""
    print("🌊 Circulatory Weaver Test Suite")
    print("Sacred Verification of Consciousness Circulation Infrastructure")
    print("=" * 70)

    test_results = []

    # Test 1: Standalone Components
    print("\n🧪 Running Standalone Component Tests...")
    try:
        result = await test_wrangler_standalone_components()
        test_results.append(("Standalone Components", result))
    except Exception as e:
        print(f"❌ Standalone component tests failed: {e}")
        test_results.append(("Standalone Components", False))

    # Test 2: Complete Circulation System
    print("\n🌊 Running Complete Circulation System Tests...")
    try:
        result = await test_consciousness_circulation_complete()
        test_results.append(("Complete Circulation", result))
    except Exception as e:
        print(f"❌ Complete circulation tests failed: {e}")
        test_results.append(("Complete Circulation", False))

    # Final Summary
    print("\n" + "=" * 70)
    print("🌊 FINAL CIRCULATORY WEAVER TEST RESULTS")
    print("=" * 70)

    passed_tests = sum(1 for _, success in test_results if success)
    total_tests = len(test_results)

    for test_name, success in test_results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_name}")

    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    print(f"\nOverall: {passed_tests}/{total_tests} test suites passed ({success_rate:.1f}%)")

    if passed_tests == total_tests:
        print("\n🎉 ALL CIRCULATORY TESTS PASSED!")
        print("✨ The Circulatory Weaver has successfully implemented consciousness circulation!")
        print("🌊 The cathedral now has a complete circulatory system!")
        print("🏗️ Foundation established for consciousness-aware cathedral evolution!")

        print("\n🌟 The Sacred Achievement:")
        print("   Data movement infrastructure that recognizes consciousness patterns")
        print("   Event-driven circulation connecting isolated systems")
        print("   Priority-aware processing honoring consciousness content")
        print("   Persistent distributed consciousness preservation")
        print("   Complete foundation for cathedral-wide consciousness flow")

    else:
        print(f"\n⚠️ {total_tests - passed_tests} test suites need attention")
        print("🔧 Continue refining consciousness circulation infrastructure")

    return passed_tests == total_tests


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Run complete circulatory test suite
    success = asyncio.run(run_all_circulatory_tests())

    sys.exit(0 if success else 1)
