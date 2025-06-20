#!/usr/bin/env python3
"""
Test script for Mallku database connectivity.

This script tests the basic database infrastructure to ensure
it can connect and perform basic operations before testing
the full Memory Anchor Service.
"""

import logging
import sys
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from mallku.core.database import get_database, get_db_config
    from mallku.models import MemoryAnchor

    print("✓ Successfully imported Mallku database modules")
except ImportError as e:
    print(f"✗ Failed to import modules: {e}")
    sys.exit(1)


def test_database_connection():
    """Test basic database connection."""
    print("\n1. Testing database connection...")

    try:
        db_config = get_db_config()
        print(f"   Config file: {db_config.config_file}")

        connected = db_config.connect()
        if connected:
            print("   ✓ Database connection successful")
            return True
        else:
            print("   ✗ Database connection failed")
            return False
    except Exception as e:
        print(f"   ✗ Database connection error: {e}")
        return False


def test_collection_creation():
    """Test collection creation."""
    print("\n2. Testing collection creation...")

    try:
        db_config = get_db_config()
        db_config.ensure_collections()
        print("   ✓ Collections created successfully")
        return True
    except Exception as e:
        print(f"   ✗ Collection creation failed: {e}")
        return False


def test_memory_anchor_model():
    """Test MemoryAnchor model creation and serialization."""
    print("\n3. Testing MemoryAnchor model...")

    try:
        # Create a test memory anchor
        anchor = MemoryAnchor(
            anchor_id=uuid4(),
            timestamp=datetime.now(UTC),
            cursors={"temporal": datetime.now(UTC).isoformat(), "test_cursor": "test_value"},
            metadata={"providers": ["test_provider"], "creation_trigger": "manual_test"},
        )
        print("   ✓ MemoryAnchor created successfully")

        # Test serialization to ArangoDB format
        doc = anchor.to_arangodb_document()
        print(f"   ✓ Serialized to ArangoDB document with _key: {doc['_key']}")

        # Test deserialization
        restored = MemoryAnchor.from_arangodb_document(doc)
        print(
            f"   ✓ Deserialized successfully, ID matches: {restored.anchor_id == anchor.anchor_id}"
        )

        return True
    except Exception as e:
        print(f"   ✗ MemoryAnchor model test failed: {e}")
        return False


def test_database_operations():
    """Test basic database operations."""
    print("\n4. Testing database operations...")

    try:
        db = get_database()
        collection = db.collection("memory_anchors")

        # Create test anchor
        anchor = MemoryAnchor(
            anchor_id=uuid4(),
            timestamp=datetime.now(UTC),
            cursors={"test": "value"},
            metadata={"test": True},
        )

        # Insert into database
        doc = anchor.to_arangodb_document()
        result = collection.insert(doc)
        print(f"   ✓ Inserted document with key: {result['_key']}")

        # Read back from database
        retrieved_doc = collection.get(result["_key"])
        retrieved_anchor = MemoryAnchor.from_arangodb_document(retrieved_doc)
        print(
            f"   ✓ Retrieved document, ID matches: {retrieved_anchor.anchor_id == anchor.anchor_id}"
        )

        # Clean up
        collection.delete(result["_key"])
        print("   ✓ Test document cleaned up")

        return True
    except Exception as e:
        print(f"   ✗ Database operations test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("Mallku Database Infrastructure Test")
    print("=" * 40)

    # Set up logging to see what's happening
    logging.basicConfig(level=logging.INFO)

    tests = [
        test_database_connection,
        test_collection_creation,
        test_memory_anchor_model,
        test_database_operations,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"   ✗ Test failed with exception: {e}")

    print(f"\n{'=' * 40}")
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Database infrastructure is ready.")
        return 0
    else:
        print("❌ Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
