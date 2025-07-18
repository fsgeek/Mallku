"""

# SECURITY: All database access through secure API gateway
# Direct ArangoDB access is FORBIDDEN - use get_secured_database()

Database connection management for Mallku.

IMPORTANT: All new code should use get_secured_database() to ensure
proper security model enforcement. Direct database access via await get_secured_database()
is deprecated and monitored for security violations.
"""

# Import security types first to avoid circular imports
# Import legacy compatibility
from .factory import get_database_raw, get_security_status

# Import async version with explicit name
from .secure_gateway import get_secured_database as get_secured_database_async
from .secured_interface import CollectionSecurityPolicy, SecuredDatabaseInterface

# Import the sync version for backward compatibility
from .sync_wrapper import get_secured_database_sync as get_secured_database

__all__ = [
    # Recommended secure access
    "get_secured_database",  # Sync version for backward compatibility
    "get_secured_database_async",  # Async version for new code
    "SecuredDatabaseInterface",
    "CollectionSecurityPolicy",
    "get_security_status",
]

# ---------------------------------------------------------------------------
# Legacy compatibility layer
# ---------------------------------------------------------------------------
#
# Some integration tests (and legacy modules) still import
# ``MallkuDBConfig`` directly from ``mallku.core.database``.  The
# canonical implementation lives in the *sibling* file
# ``mallku/core/database.py``.  Because this directory now contains a
# package, that module is no longer import-able via the dotted path
# ``mallku.core.database``; it would shadow itself.  To preserve
# backwards compatibility we dynamically load the legacy implementation
# under an internal module name and re-export the required symbols.

import sys as _sys  # noqa: E402
from importlib import util as _importlib_util  # noqa: E402  (local import is intentional)
from pathlib import Path as _Path  # noqa: E402

_legacy_path = _Path(__file__).with_name("database.py")

if _legacy_path.exists():
    _spec = _importlib_util.spec_from_file_location("mallku.core._legacy_database", _legacy_path)
    _legacy_module = _importlib_util.module_from_spec(_spec)  # type: ignore[arg-type]
    assert _spec.loader  # for mypy
    _spec.loader.exec_module(_legacy_module)  # type: ignore[attr-defined]

    # Make it importable under a predictable name (optional but handy)
    _sys.modules.setdefault("mallku.core._legacy_database", _legacy_module)

    # Re-export the public class
    MallkuDBConfig = _legacy_module.MallkuDBConfig  # type: ignore[attr-defined]

    # Keep mypy & IDE happy by polluting __all__ dynamically
    globals()["MallkuDBConfig"] = MallkuDBConfig  # type: ignore[self-assignment]
else:  # pragma: no cover – should never happen in a healthy repo
    # Provide a stub to avoid AttributeErrors; will fail loudly on use.
    class MallkuDBConfig:  # type: ignore[too-many-ancestors]
        def __init__(self, *args, **kwargs):  # noqa: D401,E501
            raise ImportError("Legacy MallkuDBConfig implementation missing")


# Legacy compatibility aliases
get_database = get_database_raw


# Import get_db_config dynamically to avoid circular imports
def get_db_config():
    """Get database configuration - legacy compatibility function."""
    # Import the module using absolute path to avoid confusion
    import os

    # Get the path to the database.py file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    database_module_path = os.path.join(parent_dir, "database.py")

    # Import the module directly
    import importlib.util

    spec = importlib.util.spec_from_file_location("_database_module", database_module_path)
    if spec and spec.loader:
        _database_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_database_module)
        return _database_module.get_db_config()
    else:
        raise ImportError("Could not load database.py module")
