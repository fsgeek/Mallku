#!/usr/bin/env python3
"""
Test script for Memory Anchor Service.

This script tests the core Memory Anchor Service functionality
to ensure it works correctly with the database.
"""

import asyncio
import logging
import sys
import pytest_asyncio
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from mallku.services.memory_anchor_service import (
        CursorUpdate,
        MemoryAnchorService,
        ProviderInfo,
    )
    print("✓ Successfully imported Memory Anchor Service")
except ImportError as e:
    print(f"✗ Failed to import service: {e}")
    sys.exit(1)
 
@pytest_asyncio.fixture
async def service():
    """Fixture to initialize MemoryAnchorService."""
    service = MemoryAnchorService()
    await service.initialize()
    return service

async def test_service_initialization():
    """Test service initialization."""
    print("\n1. Testing service initialization...")

    try:
        service = MemoryAnchorService()
        await service.initialize()
        print("   ✓ Service initialized successfully")

        # Check that we have a current anchor
        if service.current_anchor_id:
            print(f"   ✓ Current anchor ID: {service.current_anchor_id}")
        else:
            print("   ✓ No existing anchors, ready for first anchor")

        return service
    except Exception as e:
        print(f"   ✗ Service initialization failed: {e}")
        return None

async def test_provider_registration(service):
    """Test provider registration."""
    print("\n2. Testing provider registration...")

    try:
        provider_info = ProviderInfo(
            provider_id="test_provider",
            provider_type="filesystem",
            cursor_types=["temporal", "spatial"],
            metadata={"test": True}
        )

        result = await service.register_provider(provider_info)
        print(f"   ✓ Provider registered: {result['provider_id']}")
        print(f"   ✓ Current anchor: {result['current_anchor_id']}")

        return True
    except Exception as e:
        print(f"   ✗ Provider registration failed: {e}")
        return False

async def test_cursor_update(service):
    """Test cursor updates."""
    print("\n3. Testing cursor updates...")

    try:
        # Test temporal cursor update
        cursor_update = CursorUpdate(
            provider_id="test_provider",
            cursor_type="temporal",
            cursor_value="2024-01-15T10:30:00Z",
            metadata={"source": "test"}
        )

        response = await service.update_cursor(cursor_update)
        print(f"   ✓ Temporal cursor updated, anchor: {response.anchor_id}")

        # Test spatial cursor update
        cursor_update = CursorUpdate(
            provider_id="test_provider",
            cursor_type="spatial",
            cursor_value={"latitude": 49.2827, "longitude": -123.1207},
            metadata={"accuracy": "high"}
        )

        response = await service.update_cursor(cursor_update)
        print(f"   ✓ Spatial cursor updated, anchor: {response.anchor_id}")
        print(f"   ✓ Cursors now: {len(response.cursors)} types")

        return True
    except Exception as e:
        print(f"   ✗ Cursor update failed: {e}")
        return False

async def test_anchor_retrieval(service):
    """Test anchor retrieval."""
    print("\n4. Testing anchor retrieval...")

    try:
        # Get current anchor
        current = await service.get_current_anchor()
        print(f"   ✓ Retrieved current anchor: {current.anchor_id}")
        print(f"   ✓ Timestamp: {current.timestamp}")
        print(f"   ✓ Cursor types: {list(current.cursors.keys())}")

        # Get anchor by ID
        specific = await service.get_anchor_by_id(current.anchor_id)
        print(f"   ✓ Retrieved by ID matches: {specific.anchor_id == current.anchor_id}")

        return True
    except Exception as e:
        print(f"   ✗ Anchor retrieval failed: {e}")
        return False

async def test_anchor_lineage(service):
    """Test anchor lineage tracking."""
    print("\n5. Testing anchor lineage...")

    try:
        current_anchor = await service.get_current_anchor()

        # Get lineage
        lineage = await service.get_anchor_lineage(current_anchor.anchor_id, depth=5)
        print(f"   ✓ Retrieved lineage with {len(lineage)} anchors")

        for i, anchor in enumerate(lineage):
            print(f"   ✓ Anchor {i+1}: {anchor.anchor_id} at {anchor.timestamp}")

        return True
    except Exception as e:
        print(f"   ✗ Anchor lineage failed: {e}")
        return False

async def test_cleanup(service):
    """Clean up test service."""
    print("\n6. Cleaning up...")

    try:
        await service.shutdown()
        print("   ✓ Service shutdown successfully")
        return True
    except Exception as e:
        print(f"   ✗ Service cleanup failed: {e}")
        return False

async def main():
    """Run all tests."""
    print("Memory Anchor Service Test")
    print("=" * 40)

    # Set up logging to see what's happening
    logging.basicConfig(level=logging.INFO)

    tests = [
        test_service_initialization,
        lambda s: test_provider_registration(s),
        lambda s: test_cursor_update(s),
        lambda s: test_anchor_retrieval(s),
        lambda s: test_anchor_lineage(s),
        lambda s: test_cleanup(s)
    ]

    passed = 0
    total = len(tests)
    service = None

    for i, test in enumerate(tests):
        try:
            if i == 0:  # First test returns service
                service = await test()
                if service:
                    passed += 1
            else:
                if service and await test(service):
                    passed += 1
        except Exception as e:
            print(f"   ✗ Test failed with exception: {e}")

    print(f"\n{'=' * 40}")
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Memory Anchor Service is working.")
        return 0
    else:
        print("❌ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
