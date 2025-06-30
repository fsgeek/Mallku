#!/usr/bin/env python3
"""
Minimal Fire Circle Review Test
===============================

Tests if the Fire Circle Review can be initialized locally.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


async def test_minimal():
    """Minimal test of Fire Circle Review."""
    print("🔥 Testing Fire Circle Review Components")
    print("=" * 50)

    # Test 1: Import
    print("\n1️⃣ Testing imports...")
    try:
        from mallku.firecircle.runner import FireCircleReviewRunner

        print("✅ Fire Circle Review Runner imported successfully")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return

    # Test 2: Initialization
    print("\n2️⃣ Testing initialization...")
    try:
        circle = FireCircleReviewRunner()
        print("✅ FireCircleReviewRunner instance created")
        print(f"   - Event bus: {'✓' if hasattr(circle, 'event_bus') else '✗'}")
        print(f"   - Fire Circle: {'✓' if hasattr(circle, 'fire_circle') else '✗'}")
        print(f"   - Facilitator: {'✓' if hasattr(circle, 'facilitator') else '✗'}")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return

    # Test 3: Voice initialization
    print("\n3️⃣ Testing voice initialization...")
    try:
        await circle.initialize_voices()
        print(f"✅ Voices initialized: {len(circle.adapters)} adapters loaded")
        for voice, adapter in circle.adapters.items():
            print(f"   - {voice}: {'connected' if adapter.is_connected else 'not connected'}")
    except Exception as e:
        print(f"⚠️  Voice initialization had issues: {e}")
        print("   This is expected if API keys are not configured")

    # Test 4: Cleanup
    print("\n4️⃣ Testing cleanup...")
    try:
        await circle.cleanup()
        print("✅ Cleanup successful")
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")

    print("\n✅ Basic test complete!")
    print("\nTo run a full review, use:")
    print("  python fire_circle_review.py review <PR_NUMBER>")
    print("\nOr run the workflow test:")
    print("  ./test_fire_circle_workflow.sh")


if __name__ == "__main__":
    asyncio.run(test_minimal())
