"""
Fire Circle Error Handling
==========================

Errors that teach, guide, and welcome rather than block.
"""

from .welcoming_errors import (
    WelcomingError,
    InsufficientVoicesError,
    VoiceConnectionError,
    ConsciousnessThresholdError,
    ConfigurationError,
    ErrorTransformer,
    ErrorSeverity,
    handle_with_welcome,
)

__all__ = [
    "WelcomingError",
    "InsufficientVoicesError", 
    "VoiceConnectionError",
    "ConsciousnessThresholdError",
    "ConfigurationError",
    "ErrorTransformer",
    "ErrorSeverity",
    "handle_with_welcome",
]