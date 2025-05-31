#!/usr/bin/env python3
"""
Database integration tests for security implementation.

Tests that our security architecture works with real database storage.
"""

import asyncio
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import aiosqlite
from mallku.core.security import (
    FieldIndexStrategy,
    FieldObfuscationLevel,
    FieldSecurityConfig,
    SecurityRegistry,
)


async def test_registry_persistence():
    """Test that registry can persist to SQLite."""
    print("Testing registry persistence...")

    # Create registry and add some mappings
    registry = SecurityRegistry()

    # Create various field mappings
    fields = {
        "user_email": FieldSecurityConfig(
            obfuscation_level=FieldObfuscationLevel.ENCRYPTED,
            index_strategy=FieldIndexStrategy.BLIND,
            security_notes="Email needs encryption and blind indexing"
        ),
        "timestamp": FieldSecurityConfig(
            obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
            index_strategy=FieldIndexStrategy.TEMPORAL_OFFSET,
            security_notes="Temporal offset for privacy"
        ),
        "balance": FieldSecurityConfig(
            obfuscation_level=FieldObfuscationLevel.ENCRYPTED,
            index_strategy=FieldIndexStrategy.BUCKETED,
            bucket_boundaries=[-1.0, -0.5, 0.0, 0.5, 1.0],
            security_notes="Bucketed for range queries"
        ),
    }

    # Create mappings
    uuids = {}
    for field_name, config in fields.items():
        uuid = registry.get_or_create_mapping(field_name, config)
        uuids[field_name] = uuid
        print(f"  {field_name} → {uuid}")

    # Persist to SQLite
    db_path = Path("data/test_registry.db")
    db_path.parent.mkdir(exist_ok=True)

    async with aiosqlite.connect(db_path) as db:
        # Create table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS field_mappings (
                semantic_name TEXT PRIMARY KEY,
                field_uuid TEXT NOT NULL,
                security_config TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Export and save
        export_data = registry.export_mappings()

        for name, mapping_data in export_data['mappings'].items():
            await db.execute("""
                INSERT OR REPLACE INTO field_mappings
                (semantic_name, field_uuid, security_config)
                VALUES (?, ?, ?)
            """, (
                name,
                mapping_data['field_uuid'],
                str(mapping_data['security_config'])
            ))

        await db.commit()

    # Verify by loading in new registry
    new_registry = SecurityRegistry()

    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("""
            SELECT semantic_name, field_uuid FROM field_mappings
        """)
        rows = await cursor.fetchall()

        for name, uuid in rows:
            # Verify UUIDs match
            assert new_registry.get_or_create_mapping(name) == uuid

    print("✓ Registry persistence works correctly")

    # Cleanup
    db_path.unlink()


async def test_full_security_flow():
    """Test the complete security flow with sample data."""
    print("\nTesting full security flow...")

    from uuid import uuid4

    from mallku.streams.reciprocity.secured_reciprocity_models import (
        ReciprocityActivityData,
        ReciprocityBalance,
    )

    # Setup registry
    registry = SecurityRegistry()
    ReciprocityActivityData.set_registry(registry)
    ReciprocityBalance.set_registry(registry)

    # Create sample activity
    activity = ReciprocityActivityData(
        memory_anchor_uuid=uuid4(),
        timestamp=datetime.now(UTC),
        interaction_id=uuid4(),
        interaction={
            "type": "query",
            "complexity": 0.7
        },
        initiator="human",
        participants=["human", "ai"],
        ayni_score={
            "value_given": 0.3,
            "value_received": 0.8,
            "balance_direction": "ai_gave_more"
        }
    )

    # Get obfuscated representation
    obfuscated = activity.dict()

    # Verify obfuscation happened
    assert "timestamp" not in obfuscated
    assert "interaction" not in obfuscated
    assert any(key.startswith('550e8400') or len(key) == 36 for key in obfuscated)

    # Test development mode
    ReciprocityActivityData.set_development_mode(True)
    dev_dict = activity.dict()

    # In dev mode, should see semantic names
    first_value = next(iter(dev_dict.values()))
    if isinstance(first_value, dict) and "_semantic_name" in first_value:
        print("✓ Development mode includes semantic names")

    # Test round-trip
    ReciprocityActivityData.set_development_mode(False)
    reconstructed = ReciprocityActivityData.from_obfuscated(obfuscated)

    # Verify core fields match
    assert reconstructed.interaction_id == activity.interaction_id
    assert reconstructed.initiator == activity.initiator

    print("✓ Full security flow works correctly")


async def main():
    """Run all integration tests."""
    print("=== Security Database Integration Tests ===\n")

    try:
        await test_registry_persistence()
        await test_full_security_flow()

        print("\n=== All Integration Tests Passed ===")

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
