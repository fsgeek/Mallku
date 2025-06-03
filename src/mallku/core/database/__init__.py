"""
Database connection management for Mallku.

IMPORTANT: All new code should use get_secured_database() to ensure
proper security model enforcement. Direct database access via get_database()
is deprecated and monitored for security violations.
"""

from .factory import get_database_raw, get_secured_database, get_security_status
from .secured_interface import CollectionSecurityPolicy, SecuredDatabaseInterface

__all__ = [
    # Recommended secure access
    'get_secured_database',
    'SecuredDatabaseInterface',
    'CollectionSecurityPolicy',
    'get_security_status',
    # Legacy compatibility (deprecated, will log warnings)
    'get_database_raw',
    'get_database',
    'get_db_config',
]

# Legacy compatibility aliases
get_database = get_database_raw

# Import get_db_config dynamically to avoid circular imports
def get_db_config():
    """Get database configuration - legacy compatibility function."""
    from .. import database as legacy_db
    return legacy_db.get_db_config()
