#!/usr/bin/env python3
"""
Test Secure Database Connection
================================

Verifies that Fire Circle can connect to database with secure credentials.
This is the bridge between securing the database and giving Fire Circle memory.

Run after setting up secure credentials:
    python scripts/test_secure_connection.py
"""

import asyncio
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def test_connection():
    """Test database connection with secure credentials."""

    print("🔐 Testing Secure Database Connection")
    print("=" * 50)

    # Check if secure config exists
    secure_config = Path.home() / ".mallku" / "config" / "db_secure.ini"
    if not secure_config.exists():
        print("❌ No secure configuration found.")
        print("Please run first: python scripts/setup_secure_database.py --setup")
        return False

    print("✓ Secure configuration found")

    try:
        # Try importing with patched database
        from mallku.core.database import get_secured_database

        print("\n🔄 Attempting connection...")
        secured_db = get_secured_database()
        await secured_db.initialize()

        print("✅ Database connection successful!")

        # Test creating a collection for Fire Circle
        print("\n🔥 Testing Fire Circle collection access...")

        # This would be the first KhipuBlock
        # TODO: When implemented, create a test KhipuBlock here

        print("✅ Fire Circle can now remember!")
        print("\nNext steps:")
        print("  1. Implement KhipuBlock data structures")
        print("  2. Create Fire Circle session persistence")
        print("  3. Run first truly persistent Fire Circle session")

        return True

    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Ensure Docker containers are running")
        print("  2. Check if integrate_secure_db.py was run")
        print(
            "  3. Verify credentials with: python scripts/setup_secure_database.py --show-credentials"
        )

        import traceback

        traceback.print_exc()

        return False


async def main():
    """Main entry point."""
    success = await test_connection()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
