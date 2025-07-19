"""
Development Mode Database Interface
===================================

Eighth Anthropologist - Creating Development Pathways

This module provides a development-mode database interface that allows
basic functionality for local development while maintaining security warnings.

CRITICAL: This interface is for DEVELOPMENT ONLY and must NEVER be used
in production environments.
"""

import logging
import warnings
from typing import Any

from .secured_interface import SecuredDatabaseInterface

logger = logging.getLogger(__name__)


class DevDatabaseInterface(SecuredDatabaseInterface):
    """
    Development-mode database interface with relaxed security.

    This interface provides basic database functionality for local development
    while emitting clear warnings about security implications.
    """

    def __init__(self):
        """Initialize development mode interface."""
        super().__init__(None)  # No real database yet

        self._dev_mode = True
        self._collections = {}
        self._warned_operations = set()

        warnings.warn(
            "DevDatabaseInterface is for DEVELOPMENT ONLY. "
            "Implement proper API gateway before production!",
            UserWarning,
            stacklevel=2,
        )

        logger.warning(
            "=" * 70 + "\n"
            "DEVELOPMENT MODE DATABASE INTERFACE ACTIVE\n"
            "=" * 70 + "\n"
            "This mode bypasses security checks for development convenience.\n"
            "DO NOT USE IN PRODUCTION!\n"
            "\n"
            "To implement production security:\n"
            "1. Set up API gateway at http://localhost:8080\n"
            "2. Implement SecuredDatabaseInterface properly\n"
            "3. Set MALLKU_DEV_MODE=false\n"
            "=" * 70
        )

    def _warn_once(self, operation: str) -> None:
        """Warn about an operation once per session."""
        if operation not in self._warned_operations:
            self._warned_operations.add(operation)
            logger.warning(
                f"DEV MODE: {operation} - In production, this must go through API gateway"
            )

    def collection(self, name: str) -> "MockCollection":
        """Get a mock collection for development."""
        self._warn_once(f"Accessing collection '{name}'")

        if name not in self._collections:
            self._collections[name] = MockCollection(name)

        return self._collections[name]

    def has_collection(self, name: str) -> bool:
        """Check if collection exists (always returns True in dev mode)."""
        self._warn_once(f"Checking collection existence '{name}'")
        return True

    def create_collection(self, name: str) -> None:
        """Create a collection (no-op in dev mode)."""
        self._warn_once(f"Creating collection '{name}'")
        if name not in self._collections:
            self._collections[name] = MockCollection(name)

    async def query(self, collection: str, filters: dict[str, Any]) -> list[dict]:
        """Mock query implementation for development."""
        self._warn_once(f"Querying collection '{collection}'")

        # Return empty results in dev mode
        logger.info(f"DEV MODE: Query on {collection} with filters {filters} - returning empty")
        return []

    async def batch_insert(self, collection: str, documents: list[dict]) -> None:
        """Mock batch insert for development."""
        self._warn_once(f"Batch inserting to '{collection}'")

        logger.info(f"DEV MODE: Would insert {len(documents)} documents to {collection}")
        # In dev mode, just log the operation

    def get_security_metrics(self) -> dict[str, Any]:
        """Get security metrics for development mode."""
        return {
            "mode": "development",
            "operations_count": len(self._warned_operations),
            "security_violations": 0,  # None in dev mode
            "collections_accessed": list(self._collections.keys()),
            "warning": "Development mode - no real security enforcement",
        }

    @property
    def aql(self):
        """Provide mock AQL interface for development."""
        return MockAQL(self)


class MockCollection:
    """Mock collection for development mode."""

    def __init__(self, name: str):
        self.name = name
        self._documents = []

    def insert(self, document: dict) -> dict:
        """Mock document insertion."""
        logger.debug(f"DEV MODE: Inserting document into {self.name}")
        self._documents.append(document)
        return {"_id": f"dev_{len(self._documents)}", "_rev": "dev_rev"}

    def insert_many(self, documents: list[dict]) -> list[dict]:
        """Mock batch insertion."""
        logger.debug(f"DEV MODE: Inserting {len(documents)} documents into {self.name}")
        results = []
        for doc in documents:
            self._documents.append(doc)
            results.append({"_id": f"dev_{len(self._documents)}", "_rev": "dev_rev"})
        return results

    def all(self) -> list[dict]:
        """Return all documents (empty in dev mode)."""
        logger.debug(f"DEV MODE: Returning all documents from {self.name}")
        return []

    def find(self, filters: dict) -> list[dict]:
        """Mock find operation."""
        logger.debug(f"DEV MODE: Finding documents in {self.name} with filters {filters}")
        return []

    def add_persistent_index(self, fields: list[str], unique: bool = False) -> dict:
        """Mock index creation."""
        logger.debug(f"DEV MODE: Creating index on {self.name} for fields {fields}")
        return {"id": f"idx_{self.name}_{'_'.join(fields)}", "type": "persistent"}


class MockAQL:
    """Mock AQL interface for development mode."""

    def __init__(self, dev_interface):
        self.dev_interface = dev_interface

    def execute(self, query: str, bind_vars: dict[str, Any] | None = None) -> list[dict]:
        """Mock AQL execution."""
        self.dev_interface._warn_once(f"Executing AQL query: {query[:50]}...")
        logger.info(
            f"DEV MODE: AQL query execution requested but returns empty results.\n"
            f"Query: {query}\n"
            f"Bind vars: {bind_vars}"
        )
        return []
