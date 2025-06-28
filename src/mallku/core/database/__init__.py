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
    "get_secured_database",
    "SecuredDatabaseInterface",
    "CollectionSecurityPolicy",
    "get_security_status",
    # Legacy compatibility (deprecated, will log warnings)
    "get_database_raw",
    "get_database",
    "get_db_config",
    "MallkuDBConfig",
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
    from ..database import get_db_config as _get_db_config

    return _get_db_config()
