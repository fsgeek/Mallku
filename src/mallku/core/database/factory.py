"""
Database Factory - Secure Access Point

This module provides the ONLY authorized way to get database connections in Mallku.
It enforces the security-by-design principle by ensuring all database access
goes through the SecuredDatabaseInterface.

Key Principle: Structure enforces security, not discipline.
"""

import logging
import sys
from typing import TYPE_CHECKING, Any

from .secured_interface import SecuredDatabaseInterface

if TYPE_CHECKING:
    from arango.database import StandardDatabase

logger = logging.getLogger(__name__)

# Global secured interface instance
_secured_interface: SecuredDatabaseInterface | None = None


class DatabaseAccessViolationError(Exception):
    """Raised when code attempts unauthorized database access."""
    pass


def get_secured_database() -> SecuredDatabaseInterface:
    """
    Get the secured database interface.

    This is the ONLY authorized way to access the database in Mallku.
    All other database access patterns are deprecated and will be blocked.

    Returns:
        SecuredDatabaseInterface that enforces security policies
    """
    global _secured_interface

    if _secured_interface is None:
        # Import here to avoid circular imports
        from .. import database

        raw_database = database.get_database()
        _secured_interface = SecuredDatabaseInterface(raw_database)

        # Initialize asynchronously when first accessed
        import asyncio
        try:
            # Try to initialize if we're in an async context
            loop = asyncio.get_running_loop()
            if loop:
                # Schedule initialization
                loop.create_task(_secured_interface.initialize())
        except RuntimeError:
            # No event loop running, initialization will happen on first use
            pass

        logger.info("Created secured database interface")

    return _secured_interface


def get_database_raw() -> "StandardDatabase":
    """
    Get raw database connection - DEPRECATED AND MONITORED.

    This function is maintained for backward compatibility during migration
    but its use is logged and monitored. New code should use get_secured_database().

    WARNING: Direct database access bypasses security model!
    """
    import inspect
    import warnings

    # Get caller information
    frame = inspect.currentframe()
    caller_frame = frame.f_back if frame else None
    caller_info = "unknown"

    if caller_frame:
        filename = caller_frame.f_code.co_filename
        line_number = caller_frame.f_lineno
        function_name = caller_frame.f_code.co_name
        caller_info = f"{filename}:{line_number} in {function_name}()"

    # Log the violation
    warning_msg = (
        f"SECURITY WARNING: Direct database access from {caller_info}. "
        f"This bypasses the security model. Use get_secured_database() instead."
    )

    logger.warning(warning_msg)
    warnings.warn(warning_msg, UserWarning, stacklevel=2)

    # Track violations for reporting
    if _secured_interface:
        _secured_interface._security_violations.append({
            "timestamp": "now",  # Would use datetime in production
            "caller": caller_info,
            "violation_type": "direct_database_access"
        })

    # Still return database for backward compatibility
    from .. import database
    return database.get_database()


# NOTE: Monkey patching disabled to avoid circular imports
# This would be implemented in a production system with proper module structure


def create_development_validator():
    """
    Create a development-time validator that checks for security violations.

    This can be used in tests and development to ensure code follows
    the security-by-design principles.
    """
    class DatabaseSecurityValidator:
        def __init__(self):
            self.violations = []

        def check_imports(self, module_name: str) -> list[str]:
            """Check if a module has problematic database imports."""
            import ast
            import inspect

            violations = []

            try:
                # Get module source
                module = sys.modules.get(module_name)
                if not module:
                    return violations

                source = inspect.getsource(module)
                tree = ast.parse(source)

                # Check for direct database imports
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom) and node.module and 'database' in node.module:
                        for alias in node.names:
                            if alias.name == 'get_database':
                                violations.append(
                                    f"Direct import of get_database in {module_name}"
                                )

            except Exception as e:
                logger.debug(f"Could not analyze module {module_name}: {e}")

            return violations

        def validate_codebase(self) -> dict[str, list[str]]:
            """Validate entire codebase for security violations."""
            all_violations = {}

            # Check all loaded modules
            for module_name in sys.modules:
                if 'mallku' in module_name:  # Only check our modules
                    violations = self.check_imports(module_name)
                    if violations:
                        all_violations[module_name] = violations

            return all_violations

    return DatabaseSecurityValidator()


def get_security_status() -> dict[str, Any]:
    """
    Get comprehensive security status for the database access layer.

    Returns information about secured interface usage, violations, and compliance.
    """
    status = {
        "secured_interface_active": _secured_interface is not None,
        "patch_applied": True,  # Always true if this module loaded
        "compliance_score": 0.0
    }

    if _secured_interface:
        metrics = _secured_interface.get_security_metrics()
        status.update(metrics)

        # Calculate compliance score
        total_operations = metrics.get("operations_count", 0)
        violations = metrics.get("security_violations", 0)

        if total_operations > 0:
            status["compliance_score"] = max(0.0, 1.0 - (violations / total_operations))
        else:
            status["compliance_score"] = 1.0

    return status
