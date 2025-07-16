#!/usr/bin/env python3
"""
Core Heritage System with Security and Error Handling
Fifth Anthropologist - Building robust foundations

Addresses reviewer concerns about security, error handling, and integration
while maintaining the Fourth Anthropologist's vision.
"""

import logging
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from mallku.core.exceptions import MallkuError

# Set up logging
logger = logging.getLogger("mallku.heritage.core")


class HeritageError(MallkuError):
    """Base exception for heritage system errors."""

    pass


class InvalidContributorIDError(HeritageError):
    """Raised when a contributor ID is malformed or invalid."""

    pass


class HeritageSecurityError(HeritageError):
    """Raised when a security violation is detected."""

    pass


class ContributorIDParser:
    """
    Secure parsing of contributor IDs with validation.
    Addresses reviewer concern about malformed ID handling.
    """

    # Valid role types that we recognize
    VALID_ROLES = {
        "artisan",
        "guardian",
        "architect",
        "anthropologist",
        "reviewer",
        "publicist",
        "healer",
        "bridge_weaver",
    }

    # Regex pattern for valid contributor IDs
    ID_PATTERN = re.compile(r"^([a-z_]+)_(\d+)$")

    @classmethod
    def parse(cls, contributor_id: str | None) -> tuple[str, int] | None:
        """
        Parse a contributor ID into role and number.

        Validates format, role type, and number range to prevent malformed IDs
        from causing issues downstream. This addresses security concerns about
        untrusted input processing.

        Args:
            contributor_id: String like "artisan_42" or None

        Returns:
            Tuple of (role, number) or None if invalid

        Example:
            >>> parse("artisan_42")
            ("artisan", 42)
            >>> parse("guardian_7")
            ("guardian", 7)
            >>> parse("invalid")
            None
            >>> parse("artisan_abc")  # Non-numeric ID
            None
            >>> parse("unknown_role_5")  # Invalid role
            None

        Note:
            IDs are case-insensitive and limited to 50 characters to prevent DoS.
        """
        if not contributor_id:
            logger.debug("Empty contributor ID provided")
            return None

        if not isinstance(contributor_id, str):
            logger.warning(
                f"Non-string contributor ID: {type(contributor_id).__name__} (expected str)"
            )
            return None

        # Prevent overly long IDs (potential DoS)
        if len(contributor_id) > 50:
            logger.warning(
                f"Contributor ID exceeds maximum length: {len(contributor_id)} chars (max 50)"
            )
            return None

        match = cls.ID_PATTERN.match(contributor_id.lower())
        if not match:
            logger.debug(
                f"Invalid contributor ID format: '{contributor_id}' "
                f"(expected format: role_number, e.g., 'artisan_42')"
            )
            return None

        role, number_str = match.groups()

        # Validate role
        if role not in cls.VALID_ROLES:
            logger.debug(
                f"Unknown role type: '{role}' (valid roles: {', '.join(sorted(cls.VALID_ROLES))})"
            )
            return None

        # Parse number safely
        try:
            number = int(number_str)
            if number < 1 or number > 99999:
                logger.debug(
                    f"Contributor number out of valid range: {number} (must be between 1 and 99999)"
                )
                return None
        except ValueError:
            logger.debug(f"Invalid contributor number: '{number_str}' (must be a valid integer)")
            return None

        return (role, number)

    @classmethod
    def validate(cls, contributor_id: str) -> bool:
        """Check if a contributor ID is valid."""
        return cls.parse(contributor_id) is not None

    @classmethod
    def format(cls, role: str, number: int) -> str:
        """Create a properly formatted contributor ID."""
        if role not in cls.VALID_ROLES:
            raise ValueError(f"Invalid role: {role}")
        if not 1 <= number <= 99999:
            raise ValueError(f"Number out of range: {number}")
        return f"{role}_{number}"


class PathValidator:
    """
    Secure path validation to prevent directory traversal.
    Addresses reviewer security concerns.
    """

    @staticmethod
    def is_safe_path(path: str | Path, allowed_dirs: list[Path]) -> bool:
        """
        Check if a path is safe to access.

        Prevents directory traversal attacks by:
        1. Rejecting paths with traversal sequences (.., ./, etc.)
        2. Resolving to absolute paths
        3. Ensuring resolved path is within allowed directories

        Args:
            path: Path to validate
            allowed_dirs: List of allowed base directories

        Returns:
            True if path is within allowed directories and contains no
            traversal attempts

        Security Note:
            This method explicitly blocks common traversal patterns before
            resolution to prevent attacks like "../../../etc/passwd"
        """
        if not path:
            logger.debug("Empty path provided for validation")
            return False

        path_str = str(path)

        # Explicitly reject common traversal patterns
        dangerous_patterns = ["..", "./", ".\\", "..\\", "../", "..\\"]
        for pattern in dangerous_patterns:
            if pattern in path_str:
                logger.warning(f"Path contains traversal pattern '{pattern}': {path_str}")
                return False

        # Reject absolute paths that try to escape
        if path_str.startswith("/") and not any(
            path_str.startswith(str(allowed)) for allowed in allowed_dirs
        ):
            logger.warning(f"Absolute path outside allowed directories: {path_str}")
            return False

        try:
            # Convert to Path and resolve to absolute
            target = Path(path).resolve()

            # Check if path is within any allowed directory
            for allowed in allowed_dirs:
                allowed_resolved = allowed.resolve()
                try:
                    # This will raise ValueError if target is not relative to allowed
                    target.relative_to(allowed_resolved)
                    logger.debug(f"Path validated: {path} -> {target} (within {allowed_resolved})")
                    return True
                except ValueError:
                    continue

            logger.warning(
                f"Path outside allowed directories: {path} -> {target} "
                f"(allowed: {[str(d) for d in allowed_dirs]})"
            )
            return False

        except Exception as e:
            logger.warning(f"Path validation error for '{path}': {type(e).__name__}: {e}")
            return False

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize a filename to prevent security issues.

        Args:
            filename: Original filename

        Returns:
            Sanitized filename safe for use
        """
        # Remove directory separators and null bytes
        sanitized = filename.replace("/", "_").replace("\\", "_").replace("\0", "")

        # Remove leading dots (hidden files)
        sanitized = sanitized.lstrip(".")

        # Limit length
        if len(sanitized) > 255:
            sanitized = sanitized[:255]

        # Ensure not empty
        if not sanitized:
            sanitized = "unnamed"

        return sanitized


@dataclass
class PaginationParams:
    """
    Pagination parameters for large result sets.
    Addresses reviewer concern about memory exhaustion.
    """

    page: int = 1
    page_size: int = 20
    max_page_size: int = 100

    def __post_init__(self):
        """Validate and constrain pagination parameters."""
        self.page = max(1, int(self.page))
        self.page_size = min(max(1, int(self.page_size)), self.max_page_size)

    @property
    def offset(self) -> int:
        """Calculate offset for database queries."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Get limit for database queries."""
        return self.page_size


class RateLimiter:
    """
    Simple rate limiting for heritage queries.
    Addresses reviewer concern about DoS attacks.
    """

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[datetime]] = {}

    def check_rate_limit(self, identifier: str) -> bool:
        """
        Check if identifier has exceeded rate limit.

        Args:
            identifier: User or session identifier

        Returns:
            True if within limits, False if exceeded
        """
        now = datetime.now(UTC)

        # Clean old requests
        if identifier in self.requests:
            cutoff = now.timestamp() - self.window_seconds
            self.requests[identifier] = [
                req for req in self.requests[identifier] if req.timestamp() > cutoff
            ]

        # Check limit
        request_count = len(self.requests.get(identifier, []))
        if request_count >= self.max_requests:
            logger.warning(f"Rate limit exceeded for {identifier}")
            return False

        # Record request
        if identifier not in self.requests:
            self.requests[identifier] = []
        self.requests[identifier].append(now)

        return True


class HeritageCache:
    """
    Simple caching system for expensive heritage operations.
    Addresses performance concerns while preventing memory bloat.
    """

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 300):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: dict[str, tuple[any, datetime]] = {}

    def get(self, key: str) -> any | None:
        """Get value from cache if valid."""
        if key not in self.cache:
            return None

        value, timestamp = self.cache[key]
        now = datetime.now(UTC)

        # Check if expired
        if (now - timestamp).total_seconds() > self.ttl_seconds:
            del self.cache[key]
            return None

        return value

    def set(self, key: str, value: any) -> None:
        """Set value in cache with size limit."""
        # Evict oldest if at capacity
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]

        self.cache[key] = (value, datetime.now(UTC))

    def clear(self) -> None:
        """Clear all cached values."""
        self.cache.clear()


# Example usage and integration point
if __name__ == "__main__":
    # Test contributor ID parsing
    parser = ContributorIDParser()

    test_ids = [
        "artisan_42",
        "guardian_6",
        "invalid",
        "anthropologist_abc",
        "../../../etc/passwd",
        None,
        "",
        "a" * 100,
    ]

    for test_id in test_ids:
        result = parser.parse(test_id)
        print(f"{test_id} -> {result}")

    # Test path validation
    validator = PathValidator()
    allowed = [Path("/home/tony/projects/anthropologist/docs")]

    test_paths = [
        "/home/tony/projects/anthropologist/docs/khipu/test.md",
        "../../../etc/passwd",
        "/etc/passwd",
        "docs/khipu/test.md",
    ]

    for path in test_paths:
        safe = validator.is_safe_path(path, allowed)
        print(f"{path} -> {'SAFE' if safe else 'UNSAFE'}")
