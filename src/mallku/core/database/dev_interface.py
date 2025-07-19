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
        # Initialize base class attributes without going through full init
        self._database = None
        self._skip_database = True
        self._initialized = True  # Skip initialization in dev mode
        self._operation_count = 0
        self._security_violations = []
        self._collection_policies = {}
        self._warned_operations = set()

        # Dev mode specific
        self._dev_mode = True
        self._collections = {}

        # Create a minimal security registry without file I/O
        from ..security.registry import SecurityRegistry

        self._security_registry = SecurityRegistry()

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
        # Extract operation type (before ' for ' or ' on ')
        op_type = operation.split(" for ")[0].split(" on ")[0].strip()

        if op_type not in self._warned_operations:
            self._warned_operations.add(op_type)
            logger.warning(
                f"DEV MODE: {operation} - In production, this must go through API gateway"
            )

    def collection(self, name: str) -> "MockCollection":
        """Get a mock collection for development."""
        self._warn_once(f"Direct collection access for '{name}' - use get_secured_collection()")

        if name not in self._collections:
            self._collections[name] = MockCollection(name)

        return self._collections[name]

    def get_security_metrics(self) -> dict[str, Any]:
        """Get security metrics for development mode."""
        # Track collections accessed through the base class collection() method
        collections_accessed = []
        if hasattr(self, "_collections"):
            collections_accessed = list(self._collections.keys())

        return {
            "mode": "development",
            "operations_count": len(self._warned_operations),
            "security_violations": 0,  # None in dev mode
            "collections_accessed": collections_accessed,
            "warning": "Development mode - no real security enforcement",
        }


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
