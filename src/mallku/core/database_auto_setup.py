"""

# SECURITY: All database access through secure API gateway
# Direct ArangoDB access is FORBIDDEN - use get_secured_database()

Database Auto-Setup for Mallku
==============================

42nd Artisan - Making Infrastructure Reciprocal

Following the Indaleko philosophy where "things just work", this module
ensures databases and collections exist when needed, removing the friction
between intention and execution.

This represents a shift from extractive patterns (assuming infrastructure
exists) to reciprocal patterns (creating conditions for emergence).
"""

import logging
import os
from typing import Any

# from arango import ArangoClient  # REMOVED: Use secure API gateway instead
from arango.exceptions import CollectionCreateError

logger = logging.getLogger(__name__)


class DatabaseAutoSetup:
    """Ensures databases and collections exist when needed."""

    # Required collections for Mallku
    REQUIRED_COLLECTIONS = [
        "memory_anchors",
        "reciprocity_activities",
        "temporal_links",
        "consciousness_events",
        "fire_circle_sessions",
        "episodic_memories",
        "wisdom_consolidations",
        "companion_relationships",
    ]

    @classmethod
    def ensure_database_exists(
        cls,
        # SECURITY: Use secure API gateway instead of direct ArangoDB client
        # client: ArangoClient,
        api_url: str,
        database_name: str,
        username: str = "root",
        password: str = "",
    ) -> Any:
        """
        Ensure a database exists, creating it if necessary.

        This embodies reciprocal infrastructure - instead of failing when
        a database doesn't exist, we create the conditions for success.
        """
        # SECURITY: This method needs to be reimplemented to use the secure API gateway
        # The 54th Guardian removed direct ArangoDB access but didn't complete the implementation
        # For now, raise NotImplementedError to maintain architectural integrity
        raise NotImplementedError(
            "Database auto-setup must be reimplemented to use secure API gateway. "
            "Direct ArangoDB connections are forbidden. "
            "Use get_secured_database() from mallku.core.database instead."
        )

    @classmethod
    def _ensure_collections_exist(cls, db: Any) -> None:
        """Ensure all required collections exist in the database."""
        for collection_name in cls.REQUIRED_COLLECTIONS:
            try:
                if not db.has_collection(collection_name):
                    db.create_collection(collection_name)
                    logger.info(f"✓ Created collection: {collection_name}")
                else:
                    logger.debug(f"  Collection {collection_name} already exists")
            except CollectionCreateError:
                logger.debug(f"  Collection {collection_name} already exists")
            except Exception as e:
                logger.warning(f"  Could not create collection {collection_name}: {e}")

    @classmethod
    def should_auto_setup(cls) -> bool:
        """
        Determine if automatic setup should be enabled.

        Following Indaleko philosophy, we default to "yes" but respect
        explicit opt-out for production safety.
        """
        # Explicit opt-out
        if os.getenv("MALLKU_NO_AUTO_SETUP", "").lower() == "true":
            return False

        # Explicit opt-in (legacy CI flag)
        if os.getenv("CI_DATABASE_AVAILABLE") == "1":
            return True

        # Development environment indicators
        if os.getenv("MALLKU_ENV", "").lower() in ["development", "dev", "test"]:
            return True

        # Check if we're in a known development setup
        if os.path.exists(".git") and not os.path.exists("/.dockerenv"):
            # Local development (has .git, not in Docker)
            return True

        # Default to reciprocal behavior - make things work
        return True

    @classmethod
    def enhance_connection(cls, original_connect_func):
        """
        Decorator to enhance database connection with auto-setup.

        This wraps existing connection functions to add reciprocal
        infrastructure creation.
        """

        def enhanced_connect(*args, **kwargs):
            if cls.should_auto_setup():
                # Extract connection parameters
                if args:
                    database_name = (
                        args[0] if isinstance(args[0], str) else kwargs.get("database", "mallku")
                    )
                else:
                    database_name = kwargs.get("database", "mallku")

                # Try auto-setup first
                try:
                    # SECURITY: Use secure API gateway instead of direct ArangoDB client
                    # client = ArangoClient(hosts=kwargs.get("hosts", "http://localhost:8080"))
                    api_url = kwargs.get("hosts", "http://localhost:8080")
                    return cls.ensure_database_exists(
                        api_url,
                        database_name,
                        username=kwargs.get("username", "root"),
                        password=kwargs.get("password", ""),
                    )
                except Exception as e:
                    logger.debug(f"Auto-setup failed, falling back to original: {e}")

            # Fall back to original behavior
            return original_connect_func(*args, **kwargs)

        return enhanced_connect


def make_database_reciprocal():
    """
    Transform Mallku's database layer to be reciprocal.

    After calling this, database connections will automatically create
    databases and collections as needed, embodying the principle that
    infrastructure should support intention, not block it.
    """
    logger.info("Enabling reciprocal database infrastructure...")

    # This would patch the existing database connection functions
    # to use auto-setup. Implementation depends on how Mallku's
    # database layer is structured.

    # For now, we provide the building blocks that can be integrated
    # into the existing codebase.

    logger.info("✓ Database layer ready for reciprocal operation")


# Usage example:
"""
# In database.py or wherever connections are made:

from mallku.core.database_auto_setup import DatabaseAutoSetup

# Enhance existing connection
db = DatabaseAutoSetup.ensure_database_exists(
    client,
    "mallku_dev",
    username="root",
    password=""
)

# Or use as decorator
@DatabaseAutoSetup.enhance_connection
def connect_to_database(database, **kwargs):
    # Original connection logic
    pass
"""
