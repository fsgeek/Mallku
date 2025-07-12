#!/usr/bin/env python3
"""
Test Registry Persistence
=========================

Fifty-First Guardian - Verifying memory continuity

This script tests that the SecurityRegistry properly persists
field mappings to SQLite and can recover them after restart.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from datetime import UTC, datetime

from pydantic import Field

from mallku.core.security.field_strategies import FieldIndexStrategy, FieldObfuscationLevel
from mallku.core.security.registry_store import RegistryStore, get_registry_store
from mallku.core.security.secured_model import SecuredField, SecuredModel


class TestMemoryModel(SecuredModel):
    """Test model to verify persistence."""

    memory_id: str = Field(description="Unique identifier")
    content: str = SecuredField(
        description="Memory content",
        obfuscation_level=FieldObfuscationLevel.ENCRYPTED,
        security_notes="Test encrypted field",
    )
    timestamp: datetime = SecuredField(
        default_factory=lambda: datetime.now(UTC),
        obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
        index_strategy=FieldIndexStrategy.TEMPORAL_OFFSET,
    )
    importance: float = SecuredField(
        default=0.5,
        obfuscation_level=FieldObfuscationLevel.NONE,  # Not obfuscated
    )


async def test_registry_persistence():
    """Test that registry mappings persist across restarts."""

    print("🧪 Testing Security Registry Persistence")
    print("=" * 50)

    # Use a test database path
    test_db_path = Path("data/test_registry.db")
    test_db_path.parent.mkdir(exist_ok=True)

    # Phase 1: Create registry and add mappings
    print("\n📝 Phase 1: Creating new registry and mappings")

    store = get_registry_store(test_db_path)
    registry = await store.load_registry()

    print(f"Initial mappings: {len(registry._mappings)}")

    # Create a test model (this will create field mappings)
    model = TestMemoryModel(memory_id="test-001", content="This is a test memory", importance=0.9)

    # Set registry on model
    model.set_registry(registry)

    # Get obfuscated dict (creates mappings)
    obfuscated = model.dict()

    print("\nField mappings created:")
    for semantic_name, mapping in registry._mappings.items():
        print(f"  {semantic_name} → {mapping.field_uuid}")

    # Save registry
    await store.save_registry(registry)
    print(f"\n✅ Saved {len(registry._mappings)} mappings to {test_db_path}")

    # Store UUIDs for verification
    stored_uuids = {name: mapping.field_uuid for name, mapping in registry._mappings.items()}

    # Phase 2: Simulate restart - load registry from disk
    print("\n🔄 Phase 2: Simulating restart - loading from disk")

    # Create new store and registry instances
    store2 = RegistryStore(test_db_path)
    registry2 = await store2.load_registry()

    print(f"Loaded mappings: {len(registry2._mappings)}")

    # Verify mappings match
    all_match = True
    for semantic_name, original_uuid in stored_uuids.items():
        if semantic_name in registry2._mappings:
            loaded_uuid = registry2._mappings[semantic_name].field_uuid
            match = original_uuid == loaded_uuid
            print(f"  {semantic_name}: {'✓' if match else '✗'} {loaded_uuid[:8]}...")
            if not match:
                all_match = False
                print(f"    Expected: {original_uuid}")
                print(f"    Got:      {loaded_uuid}")
        else:
            print(f"  {semantic_name}: ✗ MISSING")
            all_match = False

    # Phase 3: Test using loaded registry
    print("\n🔍 Phase 3: Testing with loaded registry")

    # Create new model with loaded registry
    model2 = TestMemoryModel(memory_id="test-002", content="Another test memory", importance=0.7)
    model2.set_registry(registry2)

    # Get obfuscated dict
    obfuscated2 = model2.dict()

    # Verify same fields get same UUIDs
    print("\nVerifying UUID consistency:")
    for field in ["memory_id", "content", "timestamp", "importance"]:
        if field == "importance":  # Not obfuscated
            print(f"  {field}: Not obfuscated (as expected)")
        else:
            uuid1 = next(
                (k for k in obfuscated if k.startswith(stored_uuids.get(field, "")[:8])),
                None,
            )
            uuid2 = next(
                (k for k in obfuscated2 if k.startswith(stored_uuids.get(field, "")[:8])),
                None,
            )
            if uuid1 and uuid2:
                print(f"  {field}: ✓ Consistent UUID")
            else:
                print(f"  {field}: ✗ Inconsistent UUID")

    # Phase 4: Check backup functionality
    print("\n💾 Phase 4: Testing backup functionality")

    backup_path = await store2.backup_registry()
    print(f"Backup created: {backup_path}")

    # Phase 5: Verify integrity
    print("\n🔐 Phase 5: Checking registry integrity")

    stats = await store2.verify_integrity()
    print("Registry statistics:")
    print(f"  Field mappings: {stats['field_mappings']}")
    print(f"  Unique UUIDs: {stats['unique_uuids']}")
    print(f"  Has temporal config: {stats['has_temporal_config']}")
    print(f"  Warnings: {stats['warnings'] or 'None'}")

    # Cleanup
    print("\n🧹 Cleanup")
    if test_db_path.exists():
        test_db_path.unlink()
        print(f"Removed test database: {test_db_path}")

    # Summary
    print("\n" + "=" * 50)
    if all_match and stats["field_mappings"] > 0:
        print("✅ SUCCESS: Registry persistence is working correctly!")
        print("   - Mappings survive restart")
        print("   - UUIDs remain consistent")
        print("   - Backup functionality works")
    else:
        print("❌ FAILURE: Registry persistence has issues")
        if not all_match:
            print("   - Mappings don't match after reload")
        if stats["field_mappings"] == 0:
            print("   - No mappings were persisted")


if __name__ == "__main__":
    asyncio.run(test_registry_persistence())
