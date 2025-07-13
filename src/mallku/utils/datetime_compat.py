"""
DateTime Compatibility Module
=============================

Provides compatibility for datetime.UTC which is only available in Python 3.11+
"""

# Python 3.11+ has datetime.UTC, earlier versions need timezone.utc
from datetime import UTC

UTC = UTC

__all__ = ["UTC"]
