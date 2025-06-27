"""
Database connection and configuration management for Mallku.

This module provides database connection infrastructure adapted from proven
Indaleko patterns but simplified for Mallku's focused architecture.
"""

import configparser
import logging
import os
import time
from pathlib import Path

import requests
from arango import ArangoClient
from arango.collection import StandardCollection
from arango.database import StandardDatabase


class MallkuDBConfig:
    """
    Database configuration and connection management for Mallku.

    Provides a simplified interface based on proven Indaleko patterns,
    but focused on Mallku's specific needs for memory anchors and reciprocity tracking.
    """

    def __init__(self, config_file: str | None = None):
        """Initialize database configuration."""
        self.config_file = config_file or self._get_default_config_file()
        self.config: configparser.ConfigParser | None = None
        self.client: ArangoClient | None = None
        self._database: StandardDatabase | None = None
        self.collections: dict[str, StandardCollection] = {}

        self._load_config()

    def _get_default_config_file(self) -> str:
        """Get the default configuration file path."""
        # Look for .secrets directory (as mentioned by user)
        secrets_dir = Path.cwd() / ".secrets"
        if secrets_dir.exists():
            return str(secrets_dir / "db-config.ini")

        # Fallback to config directory
        config_dir = Path.cwd() / "config"
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / "mallku_db_config.ini")

    def _load_config(self) -> None:
        """Load configuration from file."""
        if not os.path.exists(self.config_file):
            logging.warning(f"Config file {self.config_file} not found. Using defaults.")
            self._create_default_config()
            return

        self.config = configparser.ConfigParser()
        try:
            # Handle potential BOM in config file
            self.config.read(self.config_file, encoding="utf-8-sig")
            if "database" not in self.config:
                logging.warning("No database section in config. Using defaults.")
                self._create_default_config()
        except Exception as e:
            logging.error(f"Error reading config file: {e}")
            self._create_default_config()

    def _create_default_config(self) -> None:
        """Create default configuration for test database."""
        self.config = configparser.ConfigParser()

        # Use CI environment variables if available
        if os.getenv("CI_DATABASE_AVAILABLE"):
            self.config["database"] = {
                "host": os.getenv("ARANGODB_HOST", "localhost"),
                "port": os.getenv("ARANGODB_PORT", "8529"),
                "database": os.getenv("ARANGODB_DATABASE", "test_mallku"),
                "user_name": "",  # No auth in CI
                "user_password": "",  # No auth in CI
                "admin_user": "",  # No auth in CI
                "admin_passwd": "",  # No auth in CI
                "ssl": "false",
            }
        else:
            self.config["database"] = {
                "host": "localhost",
                "port": "8529",
                "database": "Mallku",
                "user_name": "mallku_user",
                "user_password": "test_password",
                "admin_user": "root",
                "admin_passwd": "test_admin",
                "ssl": "false",
            }

        # Save the default config
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, "w") as f:
            self.config.write(f)

        logging.info(f"Created default config at {self.config_file}")

    def connect(self, timeout: int = 60) -> bool:
        """
        Connect to the ArangoDB database.

        Args:
            timeout: Maximum seconds to wait for connection

        Returns:
            True if connected successfully, False otherwise
        """
        if self._database is not None:
            return True  # Already connected

        if not self.config:
            logging.error("No configuration available")
            return False

        db_config = self.config["database"]

        # Build connection URL
        protocol = "https" if db_config.get("ssl", "false").lower() == "true" else "http"
        host = db_config["host"]
        port = db_config["port"]
        url = f"{protocol}://{host}:{port}"

        # Wait for database to be ready
        logging.debug(f"Waiting for database at {url}")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # Simple connection test - even 401 means server is responding
                response = requests.get(f"{url}/_api/version", timeout=5)
                if response.status_code in [200, 401]:
                    logging.debug("Database is responding")
                    break
            except requests.RequestException:
                pass
            time.sleep(1)
        else:
            logging.error(f"Database not ready after {timeout} seconds")
            return False

        try:
            # Create client
            self.client = ArangoClient(hosts=url)

            # Connect to database
            database_name = db_config["database"]
            username = db_config["user_name"]
            password = db_config["user_password"]

            # Handle no-auth case for CI
            if os.getenv("ARANGODB_NO_AUTH") and not username:
                self._database = self.client.db(database_name, verify=True)
            else:
                self._database = self.client.db(
                    database_name, username=username, password=password, verify=True
                )

            # Test the connection
            try:
                self._database.properties()
            except Exception as db_error:
                # In CI, database might not exist yet - create it
                if os.getenv("CI_DATABASE_AVAILABLE"):
                    logging.info(f"Database {database_name} not found, creating it...")
                    try:
                        sys_db = self.client.db("_system", verify=True)
                        if not sys_db.has_database(database_name):
                            sys_db.create_database(database_name)
                        # Reconnect to the new database
                        self._database = self.client.db(database_name, verify=True)
                        self._database.properties()
                    except Exception as create_error:
                        logging.error(f"Failed to create database: {create_error}")
                        raise db_error
                else:
                    raise db_error

            logging.info(f"Connected to database {database_name}")
            return True

        except Exception as e:
            logging.error(f"Failed to connect to database: {e}")
            self._database = None
            return False

    def get_database(self) -> StandardDatabase:
        """
        Get the connected database instance.

        Returns:
            The ArangoDB database instance

        Raises:
            ValueError: If not connected to database
        """
        if self._database is None and not self.connect():
            raise ValueError("Could not connect to database")

        return self._database

    def get_collection(self, collection_name: str) -> StandardCollection:
        """
        Get a collection from the database, creating it if it doesn't exist.

        Args:
            collection_name: Name of the collection

        Returns:
            The collection object
        """
        if collection_name in self.collections:
            return self.collections[collection_name]

        db = self.get_database()

        # Check if collection exists, create if not
        if not db.has_collection(collection_name):
            logging.info(f"Creating collection {collection_name}")
            db.create_collection(collection_name)

        collection = db.collection(collection_name)
        self.collections[collection_name] = collection
        return collection

    def ensure_collections(self) -> None:
        """Ensure all required Mallku collections exist."""
        required_collections = [
            "memory_anchors",
            "reciprocity_records",
            "activity_streams",
            "context_relationships",
        ]

        for collection_name in required_collections:
            self.get_collection(collection_name)

        logging.info("All required collections are available")

    def close(self) -> None:
        """Close database connections."""
        if self.client:
            self.client.close()
            self.client = None
            self._database = None
            self.collections.clear()
            logging.debug("Database connections closed")


# Global database instance following Indaleko singleton pattern
_db_instance: MallkuDBConfig | None = None


def get_database() -> StandardDatabase:
    """
    Get the global database instance.

    This function provides the interface expected by the Memory Anchor Service.
    Following the pattern from the user's CLAUDE.md instructions.

    Returns:
        The ArangoDB database instance
    """
    global _db_instance

    if _db_instance is None:
        _db_instance = MallkuDBConfig()
        _db_instance.connect()
        _db_instance.ensure_collections()

    return _db_instance.get_database()


def get_db_config() -> MallkuDBConfig:
    """
    Get the database configuration instance.

    Returns:
        The database configuration object
    """
    global _db_instance

    if _db_instance is None:
        _db_instance = MallkuDBConfig()

    return _db_instance
