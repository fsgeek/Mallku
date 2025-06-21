#!/usr/bin/env python3
"""
Simple Test Runner for Consciousness Bridge
===========================================

Run tests individually to verify each component.
"""

import asyncio

from test_consciousness_bridge import (
    test_bridge_handles_consciousness_patterns,
    test_bridge_receives_health_updates,
    test_consciousness_bridge_monitors_session,
    test_consciousness_coherence_boost,
    test_healing_reconnection,
    test_healing_retry_strategy,
    test_healing_with_error_patterns,
    test_session_health_report_generation,
)


async def run_all_tests():
    """Run all tests individually."""
    tests = [
        ("Bridge monitoring", test_consciousness_bridge_monitors_session),
        ("Health update processing", test_bridge_receives_health_updates),
        ("Retry strategy healing", test_healing_retry_strategy),
        ("Reconnection healing", test_healing_reconnection),
        ("Consciousness coherence boost", test_consciousness_coherence_boost),
        ("Health report generation", test_session_health_report_generation),
        ("Consciousness pattern handling", test_bridge_handles_consciousness_patterns),
        ("Error pattern healing", test_healing_with_error_patterns),
    ]

    print("🧪 Testing Infrastructure Consciousness Bridge...")
    print("=" * 80)

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            await test_func()
            print(f"✅ {name} test passed")
            passed += 1
        except Exception as e:
            print(f"❌ {name} test failed: {e}")
            failed += 1

    print("\n" + "=" * 80)
    print(f"Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All consciousness bridge tests passed!")
        print("\nThe bridge between Infrastructure Consciousness and Fire Circle is solid.")
        print("Self-healing dialogues are now possible.")
    else:
        print(f"\n⚠️  {failed} tests failed. Please review the errors above.")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
