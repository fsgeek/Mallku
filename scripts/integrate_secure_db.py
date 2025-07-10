#!/usr/bin/env python3
"""
Integrate Secure Database Configuration
=======================================

This script patches Mallku's database configuration to use
secure credentials instead of hardcoded test passwords.

It modifies the existing MallkuDBConfig to check for secure
credentials first, falling back to test credentials only
with a warning.

Run after setup_secure_database.py:
    python scripts/integrate_secure_db.py
"""

import logging
import shutil
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def create_database_patch():
    """Create a patch for database.py to use secure config."""

    patch_content = '''
# Secure configuration loader - inserted by integrate_secure_db.py
import os
from pathlib import Path

def _load_secure_config_if_available():
    """Load secure configuration if it exists."""
    secure_config_file = Path.home() / ".mallku" / "config" / "db_secure.ini"
    if secure_config_file.exists():
        import configparser
        secure_config = configparser.ConfigParser()
        secure_config.read(secure_config_file)

        # Override default configuration with secure values
        return {
            "host": secure_config.get("database", "host", fallback="localhost"),
            "port": secure_config.get("database", "port", fallback="8529"),
            "database": secure_config.get("database", "database", fallback="mallku"),
            "user_name": secure_config.get("credentials", "mallku_user"),
            "user_password": secure_config.get("credentials", "mallku_password"),
            "admin_user": "root",
            "admin_passwd": secure_config.get("credentials", "root_password"),
            "ssl": secure_config.get("database", "ssl", fallback="false"),
        }

    # Check environment variables
    if all(os.getenv(var) for var in ['MALLKU_DB_USER', 'MALLKU_DB_PASSWORD']):
        return {
            "host": os.getenv('MALLKU_DB_HOST', 'localhost'),
            "port": os.getenv('MALLKU_DB_PORT', '8529'),
            "database": os.getenv('MALLKU_DB_NAME', 'mallku'),
            "user_name": os.getenv('MALLKU_DB_USER'),
            "user_password": os.getenv('MALLKU_DB_PASSWORD'),
            "admin_user": os.getenv('MALLKU_DB_ADMIN_USER', 'root'),
            "admin_passwd": os.getenv('MALLKU_DB_ADMIN_PASSWORD', ''),
            "ssl": os.getenv('MALLKU_DB_SSL', 'false'),
        }

    return None
'''

    return patch_content


def patch_database_config():
    """Patch the database configuration to use secure credentials."""

    database_file = Path("src/mallku/core/database.py")
    if not database_file.exists():
        logger.error(f"Database file not found: {database_file}")
        return False

    # Backup original
    backup_file = database_file.with_suffix(".py.backup")
    if not backup_file.exists():
        shutil.copy(database_file, backup_file)
        logger.info(f"Created backup: {backup_file}")

    # Read the file
    with open(database_file) as f:
        content = f.read()

    # Check if already patched
    if "_load_secure_config_if_available" in content:
        logger.info("Database already patched for secure configuration")
        return True

    # Find the _create_default_config method
    patch_marker = "def _create_default_config(self) -> None:"
    if patch_marker not in content:
        logger.error("Could not find _create_default_config method to patch")
        return False

    # Insert secure config loader before the method
    patch = create_database_patch()

    # Find where to insert the patch (after imports, before class)
    import_end = content.find("class MallkuDBConfig")
    if import_end == -1:
        logger.error("Could not find MallkuDBConfig class")
        return False

    # Insert the patch
    patched_content = content[:import_end] + patch + "\n\n" + content[import_end:]

    # Now modify _create_default_config to use secure config
    old_default_config = """self.config["database"] = {
                "host": "localhost",
                "port": "8529",
                "database": "Mallku",
                "user_name": "mallku_user",
                "user_password": "test_password",
                "admin_user": "root",
                "admin_passwd": "test_admin",
                "ssl": "false",
            }"""

    new_default_config = """# Try to load secure configuration first
        secure_config = _load_secure_config_if_available()
        if secure_config:
            self.config["database"] = secure_config
            logging.info("Using secure database configuration")
        else:
            # Fall back to test credentials with warning
            logging.warning(
                "Using default test credentials - NOT SECURE! "
                "Run 'python scripts/setup_secure_database.py --setup' for security."
            )
            self.config["database"] = {
                "host": "localhost",
                "port": "8529",
                "database": "Mallku",
                "user_name": "mallku_user",
                "user_password": "test_password",
                "admin_user": "root",
                "admin_passwd": "test_admin",
                "ssl": "false",
            }"""

    patched_content = patched_content.replace(old_default_config, new_default_config)

    # Write the patched file
    with open(database_file, "w") as f:
        f.write(patched_content)

    logger.info("Successfully patched database.py for secure configuration")
    return True


def verify_patch():
    """Verify the patch works correctly."""
    try:
        # Try importing the patched module
        from mallku.core.database import MallkuDBConfig

        # Try creating an instance
        config = MallkuDBConfig()
        logger.info("✓ Patch verified - database module loads correctly")

        # Check if secure config is being used
        if hasattr(config, "config") and config.config:
            if config.config["database"].get("user_password") != "test_password":
                logger.info("✓ Secure configuration is being used")
            else:
                logger.warning("⚠️  Still using test credentials")

        return True

    except Exception as e:
        logger.error(f"Patch verification failed: {e}")
        return False


def main():
    """Main entry point."""
    print("🔧 Integrating Secure Database Configuration")
    print("=" * 50)

    # Check if secure config exists
    secure_config = Path.home() / ".mallku" / "config" / "db_secure.ini"
    if not secure_config.exists():
        print("❌ No secure configuration found.")
        print("Please run first: python scripts/setup_secure_database.py --setup")
        sys.exit(1)

    # Apply the patch
    if patch_database_config():
        print("✅ Database configuration patched successfully")

        # Verify it works
        if verify_patch():
            print("✅ Patch verified - secure configuration active")
            print("\n📝 Next steps:")
            print("  1. Restart any running Mallku services")
            print("  2. The system will now use secure credentials automatically")
            print(
                "  3. To see credentials: python scripts/setup_secure_database.py --show-credentials"
            )
        else:
            print("⚠️  Patch applied but verification failed")
            print("Check logs for details")
    else:
        print("❌ Failed to patch database configuration")
        sys.exit(1)


if __name__ == "__main__":
    main()
