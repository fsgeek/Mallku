"""
Database connection management for Mallku.

IMPORTANT: All new code should use get_secured_database() to ensure
proper security model enforcement. Direct database access via get_database()
is deprecated and monitored for security violations.
"""

from .factory import get_secured_database, get_security_status
from .secured_interface import CollectionSecurityPolicy, SecuredDatabaseInterface

__all__ = [
    # Recommended secure access
    'get_secured_database',
    'SecuredDatabaseInterface',
    'CollectionSecurityPolicy',
    'get_security_status',
]
