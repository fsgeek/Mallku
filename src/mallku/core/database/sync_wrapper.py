"""
Synchronous Wrapper for Async Database Access
============================================

56th Guardian - Bridging async and sync worlds

This module provides synchronous wrappers around the async secure gateway
to maintain backward compatibility during the migration period.

Philosophy: Make migration possible without breaking everything at once.
"""

import asyncio
import logging
from collections.abc import Callable
from typing import Any, TypeVar

from .api_client import SecureDatabaseProxy
from .secure_gateway import get_secured_database as async_get_secured_database

logger = logging.getLogger(__name__)

T = TypeVar("T")


def run_async[T](async_func: Callable[..., T]) -> T:
    """
    Run an async function in a sync context.

    Handles the case where we might already be in an event loop.
    """
    try:
        # Try to get the current event loop
        asyncio.get_running_loop()
    except RuntimeError:
        # No event loop running - create one and run the function
        return asyncio.run(async_func())
    else:
        # We're already in an event loop - this is tricky
        # We can't use asyncio.run() here as it would create a new loop
        # Instead, we need to schedule the coroutine
        import concurrent.futures

        # Create a new thread to run the async function
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(asyncio.run, async_func())
            return future.result()


class SyncSecureDatabaseProxy:
    """
    Synchronous wrapper around the async SecureDatabaseProxy.

    Provides a bridge for legacy code that expects synchronous database access.
    """

    def __init__(self, async_proxy: SecureDatabaseProxy):
        """Initialize with async proxy."""
        self._async_proxy = async_proxy
        self._loop = None

    def _run_async_method(self, method_name: str, *args, **kwargs):
        """Run an async method synchronously."""
        async_method = getattr(self._async_proxy, method_name)

        async def _wrapper():
            return await async_method(*args, **kwargs)

        return run_async(_wrapper)

    def has_collection(self, name: str) -> bool:
        """Check if collection exists."""
        return self._run_async_method("has_collection", name)

    def create_collection(self, name: str) -> "SyncSecureCollectionProxy":
        """Create collection and return sync proxy."""
        async_collection = self._run_async_method("create_collection", name)
        return SyncSecureCollectionProxy(async_collection)

    def collection(self, name: str) -> "SyncSecureCollectionProxy":
        """Get collection sync proxy."""
        # The async version returns synchronously, so we can call it directly
        async_collection = self._async_proxy.collection(name)
        return SyncSecureCollectionProxy(async_collection)

    def collections(self) -> list[dict[str, str]]:
        """List collections."""
        return self._run_async_method("collections")

    # Add AQL execution support (needed by some code)
    @property
    def aql(self):
        """Provide AQL-like interface."""
        return SyncAQLProxy(self._async_proxy)


class SyncSecureCollectionProxy:
    """
    Synchronous wrapper around collection operations.
    """

    def __init__(self, async_collection):
        """Initialize with async collection."""
        self._async_collection = async_collection

    def _run_async_method(self, method_name: str, *args, **kwargs):
        """Run an async method synchronously."""
        async_method = getattr(self._async_collection, method_name)

        async def _wrapper():
            return await async_method(*args, **kwargs)

        return run_async(_wrapper)

    def insert(self, document: dict) -> dict[str, str]:
        """Insert document synchronously."""
        return self._run_async_method("insert", document)

    def all(self, limit: int = 10) -> list[dict]:
        """Get all documents synchronously."""
        return self._run_async_method("all", limit=limit)

    def add_persistent_index(self, fields: list[str], unique: bool = False):
        """Add index (compatibility stub)."""
        # This is synchronous in the async version too
        self._async_collection.add_persistent_index(fields, unique)


class SyncAQLProxy:
    """
    Provides AQL-like interface for synchronous code.
    """

    def __init__(self, async_proxy: SecureDatabaseProxy):
        """Initialize with async database proxy."""
        self._async_proxy = async_proxy

    def execute(self, query: str, bind_vars: dict[str, Any] | None = None) -> list[dict]:
        """
        Execute AQL query synchronously.

        Note: This is a simplified implementation. The API gateway
        doesn't support full AQL yet, so this converts simple queries
        to collection operations.
        """
        # For now, we don't support AQL through the API gateway
        # This would need to be implemented in the API gateway first
        logger.warning(
            "AQL execution requested but not yet supported by API gateway. "
            "Query will return empty results. Query: %s",
            query,
        )
        return []


def get_secured_database_sync() -> SyncSecureDatabaseProxy:
    """
    Get synchronous secure database proxy.

    This is a compatibility layer for code that hasn't been converted
    to async yet. New code should use the async version directly.

    Returns:
        SyncSecureDatabaseProxy that provides synchronous access
    """

    # Get the async proxy
    async def _get_async_db():
        return await async_get_secured_database()

    async_proxy = run_async(_get_async_db)

    # Wrap it in sync interface
    return SyncSecureDatabaseProxy(async_proxy)


# Temporary alias for easier migration
get_secured_database = get_secured_database_sync
