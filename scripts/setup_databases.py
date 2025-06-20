#!/usr/bin/env python3
"""
Database setup script for Mallku.

Sets up both ArangoDB and SQLite databases needed for development.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import aiosqlite
from arango import ArangoClient
from arango.exceptions import CollectionCreateError, DatabaseCreateError


async def setup_sqlite_registry():
    """Create SQLite database for the security registry."""
    print("Setting up SQLite registry database...")

    db_path = Path("data/mallku_registry.db")
    db_path.parent.mkdir(exist_ok=True)

    async with aiosqlite.connect(db_path) as db:
        # Create registry tables
        await db.execute("""
            CREATE TABLE IF NOT EXISTS field_mappings (
                semantic_name TEXT PRIMARY KEY,
                field_uuid TEXT NOT NULL,
                security_config TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS temporal_config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                offset_seconds INTEGER NOT NULL,
                precision TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_field_uuid
            ON field_mappings(field_uuid)
        """)

        await db.commit()

    print(f"✓ SQLite registry created at {db_path}")


def setup_arangodb():
    """Create ArangoDB test database and collections."""
    print("\nSetting up ArangoDB test database...")

    # Connect to ArangoDB (default test instance)
    client = ArangoClient(hosts="http://localhost:8529")

    # Connect to _system database first
    sys_db = client.db("_system", username="root", password="")

    # Create test database
    db_name = "mallku_test"
    try:
        sys_db.create_database(db_name)
        print(f"✓ Created database: {db_name}")
    except DatabaseCreateError:
        print(f"  Database {db_name} already exists")

    # Connect to test database
    db = client.db(db_name, username="root", password="")

    # Collections to create
    collections = [
        ("memory_anchors", "document"),
        ("reciprocity_activities", "document"),
        ("reciprocity_balances", "document"),
        ("activity_relationships", "edge"),
    ]

    for coll_name, coll_type in collections:
        try:
            if coll_type == "edge":
                db.create_collection(coll_name, edge=True)
            else:
                db.create_collection(coll_name)
            print(f"✓ Created collection: {coll_name} ({coll_type})")
        except CollectionCreateError:
            print(f"  Collection {coll_name} already exists")

    # Create indexes for common queries
    # Temporal queries on reciprocity activities
    if db.has_collection("reciprocity_activities"):
        coll = db.collection("reciprocity_activities")
        try:
            coll.add_persistent_index(fields=["timestamp"])
            print("✓ Created timestamp index on reciprocity_activities")
        except Exception:
            print("  Timestamp index already exists")


async def verify_setup():
    """Verify databases are accessible."""
    print("\nVerifying database setup...")

    # Check SQLite
    db_path = Path("data/mallku_registry.db")
    if db_path.exists():
        async with aiosqlite.connect(db_path) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM field_mappings")
            count = await cursor.fetchone()
            print(f"✓ SQLite registry has {count[0]} field mappings")

    # Check ArangoDB
    try:
        client = ArangoClient(hosts="http://localhost:8529")
        db = client.db("mallku_test", username="root", password="")
        collections = db.collections()
        print(f"✓ ArangoDB has {len(collections)} collections")
    except Exception as e:
        print(f"✗ ArangoDB connection failed: {e}")


async def main():
    """Run all setup tasks."""
    print("=== Mallku Database Setup ===\n")

    # Setup SQLite
    await setup_sqlite_registry()

    # Setup ArangoDB
    try:
        setup_arangodb()
    except Exception as e:
        print(f"\n⚠️  ArangoDB setup failed: {e}")
        print("   Make sure ArangoDB is running on localhost:8529")
        print("   You can start it with: arangodb start")

    # Verify
    await verify_setup()

    print("\n=== Setup Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
