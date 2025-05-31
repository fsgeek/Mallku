"""
Field-level security strategies for balancing protection with utility.

Each field can declare its security requirements and indexing needs,
making the trade-offs explicit and auditable.
"""

from enum import Enum
from typing import Any, Protocol

from pydantic import BaseModel, Field


class FieldObfuscationLevel(str, Enum):
    """Level of obfuscation applied to field names and values."""
    NONE = "none"                    # No obfuscation
    UUID_ONLY = "uuid_only"          # Field name → UUID, value in clear
    ENCRYPTED = "encrypted"          # Field name → UUID, value encrypted


class FieldIndexStrategy(str, Enum):
    """Strategy for making fields queryable while maintaining security."""
    NONE = "none"                    # No indexing needed
    IDENTITY = "identity"            # Store as-is for indexing
    DETERMINISTIC = "deterministic"  # Same input → same output
    ORDER_PRESERVING = "order_preserving"  # Maintains sort order
    BUCKETED = "bucketed"            # Range buckets for numeric
    BLIND = "blind"                  # Keyed hash for equality
    TEMPORAL_OFFSET = "temporal_offset"  # Time-shifted for privacy
    DERIVED = "derived"              # Index on computed value


class SearchCapability(str, Enum):
    """Types of queries a field must support."""
    EQUALITY = "equality"            # field = value
    RANGE = "range"                  # field > x AND field < y
    PREFIX = "prefix"                # field LIKE 'prefix%'
    FULLTEXT = "fulltext"            # Full text search
    ORDERING = "ordering"            # ORDER BY field
    AGGREGATION = "aggregation"      # SUM, AVG, etc.


class FieldSecurityConfig(BaseModel):
    """Configuration for a field's security/utility trade-offs."""

    obfuscation_level: FieldObfuscationLevel = Field(
        default=FieldObfuscationLevel.UUID_ONLY,
        description="How the field name and value are protected"
    )

    index_strategy: FieldIndexStrategy = Field(
        default=FieldIndexStrategy.NONE,
        description="How the field is made queryable"
    )

    search_capabilities: list[SearchCapability] = Field(
        default_factory=list,
        description="Query types this field must support"
    )

    security_notes: str | None = Field(
        default=None,
        description="Documentation of security/utility trade-off"
    )

    # Strategy-specific configuration
    bucket_boundaries: list[float] | None = Field(
        default=None,
        description="For BUCKETED strategy: bucket boundaries"
    )

    temporal_precision: str | None = Field(
        default=None,
        description="For TEMPORAL_OFFSET: precision level (minute, hour, day)"
    )

    derivation_function: str | None = Field(
        default=None,
        description="For DERIVED: name of derivation function"
    )

    def validate_configuration(self) -> list[str]:
        """Validate that index strategy supports required capabilities."""
        warnings = []

        # Check strategy/capability compatibility
        if SearchCapability.RANGE in self.search_capabilities:
            valid_strategies = {
                FieldIndexStrategy.IDENTITY,
                FieldIndexStrategy.ORDER_PRESERVING,
                FieldIndexStrategy.BUCKETED,
                FieldIndexStrategy.TEMPORAL_OFFSET,
            }
            if self.index_strategy not in valid_strategies:
                warnings.append(
                    f"Strategy {self.index_strategy} may not support RANGE queries"
                )

        if SearchCapability.FULLTEXT in self.search_capabilities and self.obfuscation_level == FieldObfuscationLevel.ENCRYPTED:
            warnings.append(
                "FULLTEXT search on ENCRYPTED fields requires special handling"
            )

        # Check for configuration requirements
        if self.index_strategy == FieldIndexStrategy.BUCKETED and not self.bucket_boundaries:
            warnings.append("BUCKETED strategy requires bucket_boundaries")

        return warnings


class IndexTransformer(Protocol):
    """Protocol for index transformation strategies."""

    def transform_for_storage(self, value: Any, config: FieldSecurityConfig) -> Any:
        """Transform value for storage according to strategy."""
        ...

    def transform_for_query(self, value: Any, config: FieldSecurityConfig) -> Any:
        """Transform query value to match stored format."""
        ...

    def supports_capability(self, capability: SearchCapability) -> bool:
        """Check if this transformer supports a search capability."""
        ...
