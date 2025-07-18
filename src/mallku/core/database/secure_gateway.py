"""
Secure Database Gateway Implementation
=====================================

56th Guardian - Completing the security vision

This module provides the secure database access that maintains compatibility
with existing code while enforcing the security architecture.

All database access goes through the API gateway - no exceptions.
"""

import logging

from .api_client import SecureAPIClient, SecureDatabaseProxy

logger = logging.getLogger(__name__)

# Global instances for singleton pattern
_api_client: SecureAPIClient | None = None
_db_proxy: SecureDatabaseProxy | None = None


async def get_secured_database() -> SecureDatabaseProxy:
    """
    Get secure database proxy that routes all operations through API gateway.

    This replaces direct ArangoDB access with secure API calls while
    maintaining a compatible interface.

    Returns:
        SecureDatabaseProxy that mimics ArangoDB database interface
    """
    global _api_client, _db_proxy

    if _api_client is None:
        _api_client = SecureAPIClient()
        logger.info("Created secure API client for database operations")

    if _db_proxy is None:
        # Verify API gateway is available
        if not await _api_client.health_check():
            raise ConnectionError(
                "Cannot connect to API gateway at " + _api_client.api_url + ". "
                "Ensure the database service is running (docker-compose up)"
            )

        _db_proxy = SecureDatabaseProxy(_api_client)
        logger.info("Created secure database proxy - all operations go through API gateway")

    return _db_proxy


async def close_secured_database():
    """Close the secure database connection."""
    global _api_client, _db_proxy

    if _api_client:
        await _api_client.close()
        _api_client = None

    _db_proxy = None
    logger.info("Closed secure database connections")


# For development mode - provides clear error messages
def get_development_database():
    """
    Development mode database access.

    In development, we still require the API gateway for security parity
    with production. This ensures security issues are caught early.

    Raises:
        NotImplementedError: Always - direct database access is forbidden
    """
    raise NotImplementedError(
        "Direct database access is forbidden by security architecture.\n"
        "Even in development, all database access must go through the API gateway.\n"
        "\n"
        "To start the secure database stack:\n"
        "  docker-compose up -d\n"
        "\n"
        "This ensures dev/test environments mirror production security.\n"
        "Security through structure, not policy."
    )
