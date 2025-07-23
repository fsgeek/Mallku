"""
Database Factory
================

This module provides the factory function for creating database connections.
It is the single source of truth for database access in Mallku.
"""

import logging
import os

from arango import ArangoClient

from .dev_interface import DevDatabaseInterface
from .secured_arango_interface import SecuredArangoDatabase

logger = logging.getLogger(__name__)


def get_database():
    """
    Factory function for the database interface.

    Returns a SecuredArangoDatabase in production, and a DevDatabaseInterface
    if the MALLKU_DEV_MODE environment variable is set to "true".
    """
    if os.getenv("MALLKU_DEV_MODE", "").lower() == "true":
        logger.critical("=" * 80)
        logger.critical("WARNING: Using in-memory DevDatabaseInterface.")
        logger.critical("This provides a non-persistent, mock database for development.")
        logger.critical("NO DATA WILL BE SAVED.")
        logger.critical("To connect to a real database, ensure MALLKU_DEV_MODE is not 'true'.")
        logger.critical("=" * 80)
        return DevDatabaseInterface()
    else:
        # Configure ArangoDB client
        client = ArangoClient(hosts=os.getenv("ARANGO_HOST", "http://localhost:8529"))
        db = client.db(
            os.getenv("ARANGO_DB", "mallku"),
            username=os.getenv("ARANGO_USER", "root"),
            password=os.getenv("ARANGO_ROOT_PASSWORD", "open-dev-db-password"),
        )
        return SecuredArangoDatabase(db)
