"""
Deprecated Database Access Functions
===================================

These functions exist only to provide clear error messages when
legacy code attempts to use insecure database access patterns.

This is part of the structural barrier pattern: make violations
impossible, not just detectable.
"""

from typing import NoReturn


class DatabaseSecurityViolationError(Exception):
    """Raised when code attempts to bypass database security architecture."""

    def __init__(self):
        super().__init__(
            "\n\nDATABASE SECURITY VIOLATION\n"
            "=" * 60 + "\n"
            "Direct database access is FORBIDDEN.\n\n"
            "You must use: get_secured_database()\n\n"
            "Why this matters:\n"
            "- Direct access bypasses authentication and authorization\n"
            "- Parallel code paths lead to untested security holes\n"
            "- Architectural drift creates vulnerabilities\n\n"
            "To fix this error:\n"
            "1. Replace: from ...core.database import get_database\n"
            "   With:    from ...core.database import get_secured_database\n\n"
            "2. Replace: db = get_database()\n"
            "   With:    db = await get_secured_database()\n\n"
            "3. Update function to be async if needed\n\n"
            "See: https://github.com/fsgeek/Mallku/issues/177\n"
            "=" * 60
        )


def get_database(*args, **kwargs) -> NoReturn:
    """
    DEPRECATED: Direct database access violates security architecture.

    This function exists only to provide a clear error message.
    Use get_secured_database() instead.
    """
    raise DatabaseSecurityViolationError()


def MallkuDBConfig(*args, **kwargs) -> NoReturn:
    """
    DEPRECATED: Direct configuration violates security architecture.

    Database configuration is now handled internally by the
    secured database interface.
    """
    raise DatabaseSecurityViolationError()


# Deprecated aliases to catch all variants
get_db = get_database
get_db_connection = get_database
get_database_connection = get_database
