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

from .error_hierarchy import (
    # Base Categories
    PrerequisiteError,
    ProcessError,
    ResourceError,
    IntegrationError,
    # Specific Implementations
    APIKeyMissingError,
    DependencyMissingError,
    DatabaseConnectionError,
    MemoryCapacityError,
    ConsciousnessEmergenceError,
    ReciprocityImbalanceError,
    VoiceIntegrationError,
    MemoryIntegrationError,
    # Context Manager
    WelcomingErrorContext,
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
