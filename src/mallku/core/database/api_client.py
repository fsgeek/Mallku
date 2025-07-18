"""
Secure API Gateway Client for Database Operations
================================================

56th Guardian - [Name to be discovered]
First sacred duty: Implement the bridge between security and function

This module provides a secure client that communicates with the database
through the API gateway, maintaining the sacred security boundaries while
restoring functionality.

Security through structure, not discipline.
"""

import logging
import os
from typing import Any
from urllib.parse import urljoin

import aiohttp

logger = logging.getLogger(__name__)


class SecureAPIClient:
    """
    Client for secure database operations through API gateway.

    ALL database operations MUST go through this client.
    Direct ArangoDB connections are FORBIDDEN.
    """

    def __init__(self, api_url: str | None = None):
        """
        Initialize secure API client.

        Args:
            api_url: Base URL for API gateway (default: http://localhost:8080)
        """
        self.api_url = api_url or os.getenv("MALLKU_API_URL", "http://localhost:8080")
        self.timeout = aiohttp.ClientTimeout(total=30)
        self._session: aiohttp.ClientSession | None = None
        logger.info(f"Initialized secure API client pointing to {self.api_url}")

    async def __aenter__(self):
        """Async context manager entry."""
        self._session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._session:
            await self._session.close()

    async def _request(
        self, method: str, endpoint: str, json_data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """
        Execute API request.

        Args:
            method: HTTP method
            endpoint: API endpoint
            json_data: JSON body data
            params: Query parameters

        Returns:
            Response data

        Raises:
            Exception: If request fails
        """
        if not self._session:
            # Create session if not in context manager
            self._session = aiohttp.ClientSession(timeout=self.timeout)

        url = urljoin(self.api_url, endpoint)

        try:
            async with self._session.request(
                method, url, json=json_data, params=params
            ) as response:
                if response.status >= 400:
                    error_text = await response.text()
                    raise Exception(f"API error {response.status}: {error_text}")

                return await response.json()

        except aiohttp.ClientError as e:
            logger.error(f"API client error: {e}")
            raise Exception(f"Failed to connect to API gateway: {e}")

    async def health_check(self) -> bool:
        """
        Check if API gateway is healthy.

        Returns:
            True if healthy, False otherwise
        """
        try:
            result = await self._request("GET", "/health")
            return result.get("status") == "healthy"
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def list_collections(self) -> list[str]:
        """
        List available collections.

        Returns:
            List of collection names
        """
        result = await self._request("GET", "/api/v1/collections")
        return result.get("collections", [])

    async def create_collection(self, name: str) -> bool:
        """
        Create a new collection.

        Args:
            name: Collection name

        Returns:
            True if created successfully
        """
        # This endpoint needs to be added to the API gateway
        try:
            await self._request("POST", "/api/v1/collections", json_data={"name": name})
            return True
        except Exception as e:
            logger.error(f"Failed to create collection {name}: {e}")
            return False

    async def has_collection(self, name: str) -> bool:
        """
        Check if collection exists.

        Args:
            name: Collection name

        Returns:
            True if exists
        """
        collections = await self.list_collections()
        return name in collections

    async def insert_document(self, collection: str, document: dict) -> dict[str, str]:
        """
        Insert document into collection.

        Args:
            collection: Collection name
            document: Document data

        Returns:
            Document metadata (_key, _id)
        """
        return await self._request(
            "POST", f"/api/v1/collections/{collection}/documents", json_data=document
        )

    async def query_documents(
        self, collection: str, filter_dict: dict | None = None, limit: int = 10
    ) -> list[dict]:
        """
        Query documents from collection.

        Args:
            collection: Collection name
            filter_dict: Query filter (not yet implemented in API)
            limit: Maximum results

        Returns:
            List of documents
        """
        # Current API only supports basic listing
        # TODO: Add query support to API gateway
        result = await self._request(
            "GET", f"/api/v1/collections/{collection}/documents", params={"limit": limit}
        )
        return result.get("documents", [])

    async def close(self):
        """Close the client session."""
        if self._session and not self._session.closed:
            await self._session.close()


class SecureDatabaseProxy:
    """
    Proxy that mimics ArangoDB database interface using API gateway.

    This allows existing code to work with minimal changes while
    maintaining security architecture.
    """

    def __init__(self, api_client: SecureAPIClient):
        """Initialize proxy with API client."""
        self.api_client = api_client
        self._collections_cache = {}

    async def has_collection(self, name: str) -> bool:
        """Check if collection exists."""
        return await self.api_client.has_collection(name)

    async def create_collection(self, name: str) -> "SecureCollectionProxy":
        """Create collection and return proxy."""
        await self.api_client.create_collection(name)
        return self.collection(name)

    def collection(self, name: str) -> "SecureCollectionProxy":
        """Get collection proxy."""
        if name not in self._collections_cache:
            self._collections_cache[name] = SecureCollectionProxy(self.api_client, name)
        return self._collections_cache[name]

    async def collections(self) -> list[dict[str, str]]:
        """List collections in format similar to ArangoDB."""
        names = await self.api_client.list_collections()
        return [{"name": name} for name in names]


class SecureCollectionProxy:
    """
    Proxy that mimics ArangoDB collection interface using API gateway.
    """

    def __init__(self, api_client: SecureAPIClient, name: str):
        """Initialize collection proxy."""
        self.api_client = api_client
        self.name = name

    async def insert(self, document: dict) -> dict[str, str]:
        """Insert document into collection."""
        return await self.api_client.insert_document(self.name, document)

    async def all(self, limit: int = 10) -> list[dict]:
        """Get all documents (with limit)."""
        return await self.api_client.query_documents(self.name, limit=limit)

    def add_persistent_index(self, fields: list[str], unique: bool = False):
        """
        Add persistent index (stub for compatibility).

        Note: Index creation should be handled by migration scripts,
        not runtime code. This is here for compatibility only.
        """
        logger.info(
            f"Index creation requested for {self.name} on fields {fields} - "
            "this should be handled by migration scripts"
        )
