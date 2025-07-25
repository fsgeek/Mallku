"""
Development Mode Database Interface
===================================

This module provides an in-memory, mock implementation of the ArangoDB
database interface for local development and testing.
"""

import logging
import warnings
from typing import Any

logger = logging.getLogger(__name__)


class MockCollection:
    """A mock collection for in-memory database operations."""

    def __init__(self, name: str):
        self.name = name
        self._documents = {}

    def insert_many(self, documents: list[dict]) -> list[dict]:
        """Mock batch insertion."""
        results = []
        for doc in documents:
            key = doc.get("_key", str(len(self._documents)))
            self._documents[key] = doc
            results.append({"_id": f"{self.name}/{key}", "_key": key})
        return results

    def __getattr__(self, name: str) -> Any:
        """Mock other collection methods."""

        def mock_method(*args, **kwargs):
            logger.debug(f"MockCollection.{name} called with {args} {kwargs}")
            return None

        return mock_method


class DevDatabaseInterface:
    """
    An in-memory mock of the arango.database.StandardDatabase interface.
    """

    def __init__(self):
        self._collections = {}
        warnings.warn(
            "DevDatabaseInterface is active. Using in-memory mock database.",
            UserWarning,
            stacklevel=2,
        )

    def collection(self, name: str) -> MockCollection:
        """Get a mock collection."""
        if name not in self._collections:
            self._collections[name] = MockCollection(name)
        return self._collections[name]

    def has_collection(self, name: str) -> bool:
        """Check if a mock collection exists."""
        return name in self._collections

    def create_collection(self, name: str) -> MockCollection:
        """Create a mock collection."""
        return self.collection(name)

    def __getattr__(self, name: str) -> Any:
        """Mock other database methods."""
        raise NotImplementedError(
            f"Method '{name}' is not implemented in DevDatabaseInterface. "
            "This is an in-memory mock. To use real database functionality, "
            "ensure MALLKU_DEV_MODE is not set to 'true' and that you are "
            "connected to a running ArangoDB instance."
        )
