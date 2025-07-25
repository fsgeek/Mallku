#!/usr/bin/env python3
"""
Database Provisioning Diagnostic Tool
=====================================

48th Artisan - Archaeological Database Restoration

This tool diagnoses the database provisioning chain in Mallku,
helping understand why database provisioning might not be
triggering on new systems.

It traces through:
1. Configuration discovery and loading
2. Connection establishment
3. Database creation if needed
4. Collection provisioning
5. Security layer initialization

Reveals where the chain breaks and how to restore it.
"""

import logging
import os
import sys
import traceback
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Configure logging to see all details
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

# Silence noisy libraries
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'=' * 60}")
    print(f"🔍 {title}")
    print(f"{'=' * 60}")


def check_environment():
    """Check environment variables and system state."""
    print_section("Environment Check")

    # Check for CI environment
    ci_vars = ["CI", "GITHUB_ACTIONS", "JENKINS", "GITLAB_CI"]
    ci_detected = any(os.getenv(var) for var in ci_vars)
    print(f"CI Environment: {'YES' if ci_detected else 'NO'}")

    # Check database-related env vars
    db_vars = {
        "ARANGODB_HOST": os.getenv("ARANGODB_HOST", "not set"),
        "ARANGODB_PORT": os.getenv("ARANGODB_PORT", "not set"),
        "ARANGODB_DATABASE": os.getenv("ARANGODB_DATABASE", "not set"),
        "ARANGODB_NO_AUTH": os.getenv("ARANGODB_NO_AUTH", "not set"),
        "CI_DATABASE_AVAILABLE": os.getenv("CI_DATABASE_AVAILABLE", "not set"),
        "MALLKU_SKIP_DATABASE": os.getenv("MALLKU_SKIP_DATABASE", "not set"),
        "MALLKU_ENV": os.getenv("MALLKU_ENV", "not set"),
    }

    print("\nDatabase Environment Variables:")
    for var, value in db_vars.items():
        print(f"  {var}: {value}")

    # Check for config files
    print("\nConfiguration Files:")
    config_paths = [
        Path.cwd() / ".secrets" / "db-config.ini",
        Path.cwd() / "config" / "mallku_db_config.ini",
        PROJECT_ROOT / ".secrets" / "db-config.ini",
        PROJECT_ROOT / "config" / "mallku_db_config.ini",
    ]

    for path in config_paths:
        exists = path.exists()
        print(f"  {path}: {'EXISTS' if exists else 'NOT FOUND'}")
        if exists:
            print(f"    Size: {path.stat().st_size} bytes")


def test_legacy_database():
    """Test the legacy MallkuDBConfig path."""
    print_section("Testing Legacy Database (MallkuDBConfig)")

    try:
        from mallku.core.database import MallkuDBConfig

        print("✓ Successfully imported MallkuDBConfig")

        # Try to create instance
        print("\nCreating MallkuDBConfig instance...")
        db_config = MallkuDBConfig()
        print("✓ Created instance")
        print(f"  Config file: {db_config.config_file}")
        print(f"  Config loaded: {'YES' if db_config.config else 'NO'}")

        if db_config.config and "database" in db_config.config:
            print("\nDatabase configuration:")
            for key, value in db_config.config["database"].items():
                # Mask passwords
                if "password" in key.lower() or "passwd" in key.lower():
                    value = "***" if value else "(empty)"
                print(f"  {key}: {value}")

        # Try to connect
        print("\nAttempting database connection...")
        connected = db_config.connect(timeout=10)

        if connected:
            print("✅ Successfully connected to database!")

            # Test database operations
            db = db_config.get_database()
            print(f"\nDatabase name: {db.name}")
            print(f"Database properties: {db.properties()}")

            # Check collections
            print("\nExisting collections:")
            collections = db.collections()
            for col in collections:
                if not col["name"].startswith("_"):  # Skip system collections
                    print(f"  - {col['name']} ({col.get('count', 0)} documents)")

            # Test collection creation
            test_collection_name = "_artisan_test_collection"
            if db.has_collection(test_collection_name):
                db.delete_collection(test_collection_name)

            print(f"\nTesting collection creation: {test_collection_name}")
            db.create_collection(test_collection_name)
            print("✓ Collection created")

            # Clean up
            db.delete_collection(test_collection_name)
            print("✓ Collection deleted")

        else:
            print("❌ Failed to connect to database")
            print("  This is the issue - database connection not establishing")

    except Exception as e:
        print(f"❌ Error in legacy database test: {e}")
        print("\nTraceback:")
        traceback.print_exc()
        return False

    return connected


def test_secured_database():
    """Test the secured database interface."""
    print_section("Testing Secured Database Interface")

    try:
        from mallku.core.database import get_database

        print("✓ Successfully imported get_database")

        # Get secured interface
        print("\nGetting secured database interface...")
        secured_db = get_database()
        print("✓ Got secured interface")
        print(f"  Type: {type(secured_db).__name__}")
        print(f"  Skip database: {secured_db._skip_database}")

        # Initialize
        print("\nInitializing secured interface...")
        import asyncio

        async def init_secured():
            await secured_db.initialize()
            print("✓ Initialized secured interface")

            # Check metrics
            metrics = secured_db.get_security_metrics()
            print("\nSecurity metrics:")
            for key, value in metrics.items():
                if key != "recent_violations":  # Skip potentially long list
                    print(f"  {key}: {value}")

            # Check collections
            collections = secured_db.collections()
            print(f"\nCollections available: {len(collections)}")
            for col in collections[:5]:  # First 5 only
                print(f"  - {col}")

            return True

        # Run async initialization
        success = asyncio.run(init_secured())
        return success

    except Exception as e:
        print(f"❌ Error in secured database test: {e}")
        print("\nTraceback:")
        traceback.print_exc()
        return False


def test_import_chain():
    """Test the import chain that causes cascade failures."""
    print_section("Testing Import Chain (Issue #139 Root Cause)")

    print("Testing how import failures cascade...")

    # First test clean imports
    print("\n1. Testing clean imports of core modules:")
    core_modules = [
        "mallku.core.database",
        "mallku.core.security.registry",
        "mallku.core.security.secured_model",
        "mallku.firecircle.service.service",
    ]

    for module in core_modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except Exception as e:
            print(f"  ❌ {module}: {e}")

    # Test problematic imports
    print("\n2. Testing imports that use outdated APIs:")
    problem_modules = [
        "mallku.governance.fire_circle_bridge",
        "mallku.governance.consciousness_transport",
        "mallku.orchestration.event_bus",
    ]

    for module in problem_modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except Exception as e:
            print(f"  ❌ {module}: {type(e).__name__}: {e}")
            # This reveals the real error, not "No module named 'mallku'"


def diagnose_provisioning_flow():
    """Run complete diagnosis of database provisioning."""
    print("\n" + "=" * 60)
    print("🏛️  DATABASE PROVISIONING DIAGNOSTICS")
    print("=" * 60)
    print("48th Artisan - Restoring Database Flow")

    # Check environment
    check_environment()

    # Test legacy database
    legacy_works = test_legacy_database()

    # Test secured database
    secured_works = test_secured_database()

    # Test import chain
    test_import_chain()

    # Summary and recommendations
    print_section("Diagnosis Summary")

    if legacy_works and secured_works:
        print("✅ Database provisioning chain is working!")
        print("\nThe system can:")
        print("  - Connect to ArangoDB")
        print("  - Create databases if needed")
        print("  - Provision collections")
        print("  - Initialize security layer")

    elif legacy_works and not secured_works:
        print("⚠️  Legacy database works but secured interface has issues")
        print("\nPossible causes:")
        print("  - Security registry initialization failing")
        print("  - Collection policies not loading")
        print("  - Async initialization not completing")

    elif not legacy_works:
        print("❌ Database connection not establishing")
        print("\nRecommendations:")
        print("  1. Check if ArangoDB is running:")
        print("     - Default URL: http://localhost:8529")
        print("     - Run: docker ps | grep arango")
        print("  2. Check configuration:")
        print("     - Create .secrets/db-config.ini if missing")
        print("     - Verify connection parameters")
        print("  3. For local development:")
        print("     - docker run -p 8529:8529 -e ARANGO_NO_AUTH=1 arangodb:3.12")

    print("\nImport Chain Issues:")
    print("  - Outdated APIs in governance/orchestration modules")
    print("  - These cause 'No module named mallku' errors in CI")
    print("  - Need migration from MallkuDBConfig to get_database()")


if __name__ == "__main__":
    diagnose_provisioning_flow()
