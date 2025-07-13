#!/usr/bin/env python3
"""
Integrate Secure Database Configuration
=======================================

This script patches Mallku's database.py to use secure credentials
from the configuration file instead of hardcoded test passwords.

Run after setup_secure_database.py to complete the integration.
"""

import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def integrate_secure_config():
    """Patch database.py to use secure configuration."""

    # Find database.py
    db_file = Path("src/mallku/core/database.py")
    if not db_file.exists():
        logger.error(f"Cannot find {db_file}")
        return False

    # Check if secure config exists
    config_file = Path.home() / ".mallku" / "config" / "db_secure.ini"
    if not config_file.exists():
        logger.error("No secure configuration found.")
        logger.error("Please run first: python scripts/setup_secure_database.py --setup")
        return False

    logger.info("✅ Found secure configuration")
    logger.info(f"📝 Patching {db_file} to use secure credentials...")

    # Read current database.py
    content = db_file.read_text()

    # Check if already patched
    if "load_secure_credentials" in content:
        logger.info("✓ Database already configured for secure credentials")
        return True

    # Create the patch
    patch = '''
# Secure credential loading
def load_secure_credentials():
    """Load credentials from secure configuration file."""
    import configparser
    from pathlib import Path

    config_file = Path.home() / ".mallku" / "config" / "db_secure.ini"
    if not config_file.exists():
        # Fall back to environment/defaults if no secure config
        return None

    config = configparser.ConfigParser()
    config.read(config_file)

    if "credentials" not in config:
        return None

    return {
        "host": config.get("database", "host", fallback="localhost"),
        "port": int(config.get("database", "port", fallback="8529")),
        "database": config.get("database", "database", fallback="mallku"),
        "username": config["credentials"]["mallku_user"],
        "password": config["credentials"]["mallku_password"],
    }

# Try to load secure credentials first
_secure_creds = load_secure_credentials()
if _secure_creds:
    ARANGO_HOST = _secure_creds["host"]
    ARANGO_PORT = _secure_creds["port"]
    ARANGO_DB = _secure_creds["database"]
    ARANGO_USER = _secure_creds["username"]
    ARANGO_PASSWORD = _secure_creds["password"]
else:
    # Fall back to original configuration
'''

    # Find where to insert the patch (after imports, before config)
    import_end = content.rfind("from pydantic")
    if import_end == -1:
        import_end = content.rfind("import ")

    # Find the line after imports
    newline_pos = content.find("\n\n", import_end)
    if newline_pos == -1:
        logger.error("Cannot find suitable insertion point")
        return False

    # Insert the patch
    patched = (
        content[: newline_pos + 2]
        + patch
        + "\n    "  # Maintain indentation
        + content[newline_pos + 2 :]
    )

    # Write back
    db_file.write_text(patched)
    logger.info("✅ Successfully patched database.py")

    # Also create a simple test script
    test_script = Path("scripts/test_secure_db_connection.py")
    test_script.write_text('''#!/usr/bin/env python3
"""Test that secure database configuration works."""

import asyncio
from mallku.core.database import get_secured_database

async def test():
    db = get_secured_database()
    await db.initialize()
    print("✅ Secure database connection successful!")

if __name__ == "__main__":
    asyncio.run(test())
''')

    logger.info("✅ Created test script: scripts/test_secure_db_connection.py")
    logger.info("\nIntegration complete! The database will now use secure credentials.")

    return True


def main():
    """Main entry point."""
    success = integrate_secure_config()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
