"""
Index transformation strategies for field-level security.

Each transformer implements a specific strategy for making data queryable
while maintaining appropriate security.
"""

import hashlib
import hmac
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from .field_strategies import FieldSecurityConfig, SearchCapability
from .temporal import TemporalEncoder


class BaseTransformer(ABC):
    """Base class for all index transformers."""

    @abstractmethod
    def transform_for_storage(self, value: Any, config: FieldSecurityConfig) -> Any:
        """Transform value for storage according to strategy."""
        pass

    @abstractmethod
    def transform_for_query(self, value: Any, config: FieldSecurityConfig) -> Any:
        """Transform query value to match stored format."""
        pass

    @abstractmethod
    def supports_capability(self, capability: SearchCapability) -> bool:
        """Check if this transformer supports a search capability."""
        pass


class IdentityTransformer(BaseTransformer):
    """No transformation - store as-is."""

    def transform_for_storage(self, value: Any, config: FieldSecurityConfig) -> Any:
        return value

    def transform_for_query(self, value: Any, config: FieldSecurityConfig) -> Any:
        return value

    def supports_capability(self, capability: SearchCapability) -> bool:
        # Identity transformation supports all capabilities
        return True


class DeterministicTransformer(BaseTransformer):
    """Deterministic transformation - same input always produces same output."""

    def __init__(self, secret_key: bytes):
        self.secret_key = secret_key

    def _hash_value(self, value: str) -> str:
        """Create deterministic hash of value."""
        return hmac.new(
            self.secret_key,
            value.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def transform_for_storage(self, value: Any, config: FieldSecurityConfig) -> str:
        # Convert to string and hash
        str_value = str(value)
        return self._hash_value(str_value)

    def transform_for_query(self, value: Any, config: FieldSecurityConfig) -> str:
        # Same transformation for queries
        str_value = str(value)
        return self._hash_value(str_value)

    def supports_capability(self, capability: SearchCapability) -> bool:
        # Only supports equality searches
        return capability == SearchCapability.EQUALITY


class BucketedTransformer(BaseTransformer):
    """Transform numeric values into buckets for range queries."""

    def _find_bucket(self, value: float, boundaries: list[float]) -> tuple[float, float]:
        """Find which bucket a value belongs to."""
        if not boundaries:
            raise ValueError("Bucket boundaries not configured")

        # Handle edge cases
        if value <= boundaries[0]:
            return (float('-inf'), boundaries[0])
        if value >= boundaries[-1]:
            return (boundaries[-1], float('inf'))

        # Find bucket
        for i in range(len(boundaries) - 1):
            if boundaries[i] < value <= boundaries[i + 1]:
                return (boundaries[i], boundaries[i + 1])

        # Shouldn't reach here
        raise ValueError(f"Could not find bucket for value {value}")

    def transform_for_storage(self, value: Any, config: FieldSecurityConfig) -> dict:
        if not isinstance(value, int | float):
            raise ValueError(f"Bucketed strategy requires numeric value, got {type(value)}")

        bucket_min, bucket_max = self._find_bucket(
            float(value),
            config.bucket_boundaries or []
        )

        return {
            "bucket_min": bucket_min,
            "bucket_max": bucket_max,
            "bucket_label": f"[{bucket_min}, {bucket_max})"
        }

    def transform_for_query(self, value: Any, config: FieldSecurityConfig) -> dict:
        # For queries, we need to handle ranges
        if isinstance(value, dict) and "min" in value and "max" in value:
            # Range query
            return {
                "query_min": value["min"],
                "query_max": value["max"]
            }
        else:
            # Single value query - find its bucket
            return self.transform_for_storage(value, config)

    def supports_capability(self, capability: SearchCapability) -> bool:
        return capability in {
            SearchCapability.RANGE,
            SearchCapability.ORDERING,
            SearchCapability.AGGREGATION
        }


class BlindIndexTransformer(BaseTransformer):
    """Create searchable blind index using keyed hash."""

    def __init__(self, index_key: bytes):
        self.index_key = index_key

    def _create_blind_index(self, value: str, field_name: str) -> str:
        """Create blind index for a value."""
        # Include field name to prevent cross-field correlation
        data = f"{field_name}:{value}".encode()
        return hmac.new(self.index_key, data, hashlib.sha256).hexdigest()[:16]

    def transform_for_storage(self, value: Any, config: FieldSecurityConfig) -> dict:
        str_value = str(value)
        # Store both encrypted value and blind index
        return {
            "encrypted_value": str_value,  # Would be encrypted in real implementation
            "blind_index": self._create_blind_index(str_value, "field")
        }

    def transform_for_query(self, value: Any, config: FieldSecurityConfig) -> str:
        # Return just the blind index for queries
        str_value = str(value)
        return self._create_blind_index(str_value, "field")

    def supports_capability(self, capability: SearchCapability) -> bool:
        return capability == SearchCapability.EQUALITY


class TemporalOffsetTransformer(BaseTransformer):
    """Transform timestamps using temporal offset."""

    def __init__(self, encoder: TemporalEncoder):
        self.encoder = encoder

    def transform_for_storage(self, value: Any, config: FieldSecurityConfig) -> float:
        if not isinstance(value, datetime):
            raise ValueError(f"Temporal transformer requires datetime, got {type(value)}")

        # Apply precision reduction if configured
        if config.temporal_precision:
            return self.encoder.encode_with_precision(value, config.temporal_precision)
        else:
            return self.encoder.encode(value)

    def transform_for_query(self, value: Any, config: FieldSecurityConfig) -> Any:
        if isinstance(value, datetime):
            # Single timestamp
            return self.transform_for_storage(value, config)
        elif isinstance(value, dict) and "start" in value and "end" in value:
            # Time range
            return {
                "start": self.transform_for_storage(value["start"], config),
                "end": self.transform_for_storage(value["end"], config)
            }
        else:
            return value

    def supports_capability(self, capability: SearchCapability) -> bool:
        return capability in {
            SearchCapability.RANGE,
            SearchCapability.ORDERING,
            SearchCapability.EQUALITY
        }


class TransformerRegistry:
    """Registry of available transformers."""

    def __init__(self, secret_key: bytes, temporal_encoder: TemporalEncoder):
        self.transformers = {
            "identity": IdentityTransformer(),
            "deterministic": DeterministicTransformer(secret_key),
            "bucketed": BucketedTransformer(),
            "blind": BlindIndexTransformer(secret_key),
            "temporal_offset": TemporalOffsetTransformer(temporal_encoder),
        }

    def get_transformer(self, strategy: str) -> BaseTransformer | None:
        """Get transformer for a strategy."""
        return self.transformers.get(strategy)

    def transform_value(
        self,
        value: Any,
        config: FieldSecurityConfig,
        for_query: bool = False
    ) -> Any:
        """Transform a value according to its field configuration."""
        transformer = self.get_transformer(config.index_strategy.value)

        if not transformer:
            # No transformation needed
            return value

        if for_query:
            return transformer.transform_for_query(value, config)
        else:
            return transformer.transform_for_storage(value, config)
