"""
Security module for Mallku - handling data obfuscation, encryption, and index strategies.

This module implements the balance between security and utility, allowing field-level
configuration of how data is protected while maintaining queryability.
"""

from .field_strategies import (
    FieldIndexStrategy,
    FieldObfuscationLevel,
    FieldSecurityConfig,
    SearchCapability,
)
from .registry import SecurityRegistry
from .secured_model import SecuredField, SecuredModel
from .temporal import TemporalEncoder, TemporalOffsetConfig
from .transformers import (
    BlindIndexTransformer,
    BucketedTransformer,
    DeterministicTransformer,
    IdentityTransformer,
    TemporalOffsetTransformer,
    TransformerRegistry,
)

__all__ = [
    # Field strategies
    "FieldIndexStrategy",
    "FieldObfuscationLevel",
    "FieldSecurityConfig",
    "SearchCapability",
    # Registry
    "SecurityRegistry",
    # Temporal
    "TemporalEncoder",
    "TemporalOffsetConfig",
    # Transformers
    "TransformerRegistry",
    "IdentityTransformer",
    "DeterministicTransformer",
    "BucketedTransformer",
    "BlindIndexTransformer",
    "TemporalOffsetTransformer",
    # Models
    "SecuredModel",
    "SecuredField",
]
