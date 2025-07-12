"""
DateTime Compatibility Module
=============================

Provides compatibility for datetime.UTC which is only available in Python 3.11+
"""

import sys

# Python 3.11+ has datetime.UTC, earlier versions need timezone.utc
from datetime import timezone

UTC = timezone.utc

__all__ = ["UTC"]
