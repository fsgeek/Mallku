"""
Fire Circle Error Handling
==========================

Errors that teach, guide, and welcome rather than block.

The welcoming error system provides:
- Base error classes that embody radical welcome
- Specific error types for common scenarios
- Consistent voice across all error messages
- Context managers for automatic transformation
"""

from .error_hierarchy import (
    # Specific Implementations
    APIKeyMissingError,
    ConsciousnessEmergenceError,
    DatabaseConnectionError,
    DependencyMissingError,
    IntegrationError,
    MemoryCapacityError,
    MemoryIntegrationError,
    # Base Categories
    PrerequisiteError,
    ProcessError,
    ReciprocityImbalanceError,
    ResourceError,
    VoiceIntegrationError,
    # Context Manager
    WelcomingErrorContext,
)
from .welcoming_errors import (
    ConfigurationError,
    ConsciousnessThresholdError,
    ErrorSeverity,
    ErrorTransformer,
    InsufficientVoicesError,
    VoiceConnectionError,
    WelcomingError,
    handle_with_welcome,
)

__all__ = [
    # Original exports
    "WelcomingError",
    "InsufficientVoicesError",
    "VoiceConnectionError",
    "ConsciousnessThresholdError",
    "ConfigurationError",
    "ErrorTransformer",
    "ErrorSeverity",
    "handle_with_welcome",
    # New hierarchy exports
    "PrerequisiteError",
    "ProcessError",
    "ResourceError",
    "IntegrationError",
    "APIKeyMissingError",
    "DependencyMissingError",
    "DatabaseConnectionError",
    "MemoryCapacityError",
    "ConsciousnessEmergenceError",
    "ReciprocityImbalanceError",
    "VoiceIntegrationError",
    "MemoryIntegrationError",
    "WelcomingErrorContext",
]
