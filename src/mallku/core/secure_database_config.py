"""
Secure Database Configuration for Mallku
========================================

Integrates secure credential management with existing Mallku infrastructure.
Based on Indaleko patterns but adapted for Mallku's architecture.

This replaces hardcoded test credentials with secure, auto-generated ones
that require no memorization but provide real security.
"""

import configparser
import json
import logging
import os
from pathlib import Path
from typing import Optional

from mallku.core.database import MallkuDBConfig


class SecureMallkuDBConfig(MallkuDBConfig):
    """
    Secure database configuration that uses proper credentials.

    Extends MallkuDBConfig to load credentials from secure storage
    instead of using hardcoded test passwords.
    """

    SECURE_CONFIG_DIR = Path.home() / ".mallku" / "config"
    SECURE_CONFIG_FILE = SECURE_CONFIG_DIR / "db_secure.ini"

    def __init__(self, config_file: str | None = None):
        """Initialize with secure configuration."""
        # Don't call parent __init__ yet - we need to set up secure config first
        self.secure_config_file = self.SECURE_CONFIG_FILE
        self.secure_config = None

        # Load secure configuration if it exists
        if self._load_secure_config():
            # Override the config_file to prevent default creation
            config_file = str(self.secure_config_file)

        # Now initialize parent with proper config
        super().__init__(config_file)

    def _load_secure_config(self) -> bool:
        """Load secure configuration if it exists."""
        if not self.secure_config_file.exists():
            logging.warning(
                f"No secure config found at {self.secure_config_file}. "
                "Run 'python scripts/setup_secure_database.py --setup' to create one."
            )
            return False

        try:
            self.secure_config = configparser.ConfigParser()
            self.secure_config.read(self.secure_config_file)
            return True
        except Exception as e:
            logging.error(f"Failed to load secure config: {e}")
            return False

    def _load_config(self) -> None:
        """Override to load from secure configuration."""
        if self.secure_config:
            # Use secure configuration
            self.config = configparser.ConfigParser()

            # Map secure config to expected format
            self.config["database"] = {
                "host": self.secure_config.get("database", "host", fallback="localhost"),
                "port": self.secure_config.get("database", "port", fallback="8529"),
                "database": self.secure_config.get("database", "database", fallback="mallku"),
                "user_name": self.secure_config.get("credentials", "mallku_user"),
                "user_password": self.secure_config.get("credentials", "mallku_password"),
                "admin_user": "root",
                "admin_passwd": self.secure_config.get("credentials", "root_password"),
                "ssl": self.secure_config.get("database", "ssl", fallback="false"),
            }

            logging.info("Loaded secure database configuration")
        else:
            # Fall back to parent's default behavior
            super()._load_config()
            logging.warning("Using default test credentials - not secure!")

    def get_connection_string(self) -> str:
        """Get ArangoDB connection string with credentials."""
        db_config = self.config["database"]
        protocol = "https" if db_config.get("ssl", "false").lower() == "true" else "http"
        return f"{protocol}://{db_config['host']}:{db_config['port']}"

    def get_docker_config(self) -> dict[str, str] | None:
        """Get Docker configuration if available."""
        docker_config_file = self.SECURE_CONFIG_DIR / "docker_secure.json"
        if not docker_config_file.exists():
            return None

        try:
            with open(docker_config_file) as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load Docker config: {e}")
            return None

    def get_api_credentials(self) -> tuple[str, str]:
        """Get API credentials for external access."""
        if self.secure_config and "credentials" in self.secure_config:
            return (
                self.secure_config["credentials"]["mallku_user"],
                self.secure_config["credentials"]["mallku_password"],
            )
        else:
            # Fall back to defaults from parent
            return (self.config["database"]["user_name"], self.config["database"]["user_password"])

    @classmethod
    def ensure_secure_config(cls) -> bool:
        """
        Ensure secure configuration exists.

        Returns True if config exists or was created, False on error.
        """
        config_file = cls.SECURE_CONFIG_FILE

        if config_file.exists():
            return True

        print("🔐 No secure configuration found.")
        print("Please run: python scripts/setup_secure_database.py --setup")
        print("This will generate secure credentials automatically.")

        return False

    @classmethod
    def from_environment(cls) -> Optional["SecureMallkuDBConfig"]:
        """
        Create config from environment variables if available.

        Useful for CI/CD and containerized environments.
        """
        required_vars = [
            "MALLKU_DB_HOST",
            "MALLKU_DB_PORT",
            "MALLKU_DB_NAME",
            "MALLKU_DB_USER",
            "MALLKU_DB_PASSWORD",
        ]

        # Check if all required vars are present
        if not all(os.getenv(var) for var in required_vars):
            return None

        # Create temporary config
        config = cls(config_file=":memory:")
        config.config = configparser.ConfigParser()
        config.config["database"] = {
            "host": os.getenv("MALLKU_DB_HOST", "localhost"),
            "port": os.getenv("MALLKU_DB_PORT", "8529"),
            "database": os.getenv("MALLKU_DB_NAME", "mallku"),
            "user_name": os.getenv("MALLKU_DB_USER"),
            "user_password": os.getenv("MALLKU_DB_PASSWORD"),
            "admin_user": os.getenv("MALLKU_DB_ADMIN_USER", "root"),
            "admin_passwd": os.getenv("MALLKU_DB_ADMIN_PASSWORD", ""),
            "ssl": os.getenv("MALLKU_DB_SSL", "false"),
        }

        return config


def get_secure_db_config() -> SecureMallkuDBConfig:
    """
    Get secure database configuration.

    Tries in order:
    1. Environment variables (for CI/CD)
    2. Secure config file
    3. Falls back to default with warning
    """
    # Try environment first
    config = SecureMallkuDBConfig.from_environment()
    if config:
        logging.info("Using database config from environment variables")
        return config

    # Try secure config file
    config = SecureMallkuDBConfig()
    if config.secure_config:
        logging.info("Using secure database configuration")
        return config

    # Warn about insecure fallback
    logging.warning(
        "No secure configuration found. Using test credentials. "
        "Run 'python scripts/setup_secure_database.py --setup' for security."
    )
    return config
