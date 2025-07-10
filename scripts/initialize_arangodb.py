#!/usr/bin/env python3
"""
Initialize ArangoDB with Mallku Database and User
=================================================

Creates the mallku database and user with proper permissions.
Run this after containers are started but before using the API.

Usage:
    python scripts/initialize_arangodb.py
"""

import configparser
import time
from pathlib import Path

from arango import ArangoClient


def load_secure_config():
    """Load secure configuration."""
    config_file = Path.home() / ".mallku" / "config" / "db_secure.ini"
    if not config_file.exists():
        raise FileNotFoundError(f"Secure config not found at {config_file}")

    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def initialize_database():
    """Initialize ArangoDB with mallku database and user."""
    print("🔧 Initializing ArangoDB for Mallku")
    print("=" * 50)

    # Load configuration
    config = load_secure_config()

    host = config.get("database", "host", fallback="localhost")
    port = config.get("database", "port", fallback="8529")
    root_password = config.get("credentials", "root_password")
    mallku_user = config.get("credentials", "mallku_user")
    mallku_password = config.get("credentials", "mallku_password")

    print(f"📍 Connecting to ArangoDB at {host}:{port}")

    # Connect as root
    client = ArangoClient(hosts=f"http://{host}:{port}")

    try:
        # Connect to system database as root
        sys_db = client.db("_system", username="root", password=root_password)
        print("✅ Connected to _system database")

        # Create mallku database if it doesn't exist
        if not sys_db.has_database("mallku"):
            print("📦 Creating 'mallku' database...")
            sys_db.create_database("mallku")
            print("✅ Database 'mallku' created")
        else:
            print("✅ Database 'mallku' already exists")

        # Check if user exists
        users = sys_db.users()
        user_exists = any(u["username"] == mallku_user for u in users)

        if not user_exists:
            print(f"👤 Creating user '{mallku_user}'...")
            sys_db.create_user(username=mallku_user, password=mallku_password, active=True)
            print(f"✅ User '{mallku_user}' created")
        else:
            print(f"✅ User '{mallku_user}' already exists")

        # Grant permissions
        print(f"🔐 Granting permissions to '{mallku_user}'...")
        sys_db.update_permission(username=mallku_user, permission="rw", database="mallku")
        print("✅ Permissions granted")

        # Test connection as mallku user
        print(f"\n🧪 Testing connection as '{mallku_user}'...")
        test_db = client.db("mallku", username=mallku_user, password=mallku_password)
        test_db.properties()  # This will fail if auth is wrong
        print("✅ Authentication successful!")

        # Create collections
        print("\n📚 Creating Fire Circle collections...")
        collections = [
            "fire_circle_sessions",
            "fire_circle_decisions",
            "khipu_blocks",
            "consciousness_threads",
        ]

        for collection_name in collections:
            if not test_db.has_collection(collection_name):
                test_db.create_collection(collection_name)
                print(f"  ✅ Created '{collection_name}'")
            else:
                print(f"  ✅ '{collection_name}' already exists")

        print("\n🎉 ArangoDB initialization complete!")
        print("   Database: mallku")
        print(f"   User: {mallku_user}")
        print(f"   Collections: {', '.join(collections)}")

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    finally:
        client.close()


if __name__ == "__main__":
    # Wait a moment for any container operations to settle
    time.sleep(2)

    if initialize_database():
        print("\n✅ Ready for Fire Circle memory!")
    else:
        print("\n❌ Initialization failed")
        exit(1)
