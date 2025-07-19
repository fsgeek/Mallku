"""
Security registry for managing field obfuscation and encryption.

This is the core of the dbfacade pattern - mapping semantic names to UUIDs
and managing the security configuration for each field.
"""

import logging
import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import Field

from ...core.models import ModelConfig
from .field_strategies import FieldSecurityConfig
from .temporal import TemporalOffsetConfig

logger = logging.getLogger(__name__)


class FieldMapping(ModelConfig):
    """Mapping between semantic field name and UUID."""

    semantic_name: str = Field(description="Human-readable field name")
    field_uuid: str = Field(description="UUID for storage")
    security_config: FieldSecurityConfig = Field(
        default_factory=FieldSecurityConfig, description="Security configuration for this field"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Config(ModelConfig.Config):
        json_encoders = {datetime: lambda v: v.isoformat()}


class SecurityRegistry:
    """
    Manages field name obfuscation and security configurations.

    This registry maintains the critical mapping between semantic field names
    and their UUID representations, along with security configurations.
    """

    def __init__(self, registry_data: dict[str, FieldMapping] | None = None):
        """Initialize registry with optional existing data."""
        self._mappings: dict[str, FieldMapping] = registry_data or {}
        self._reverse_mappings: dict[str, str] = {}
        self._temporal_config: TemporalOffsetConfig | None = None

        # Build reverse mappings
        for semantic_name, mapping in self._mappings.items():
            self._reverse_mappings[mapping.field_uuid] = semantic_name

    def get_or_create_mapping(
        self, semantic_name: str, security_config: FieldSecurityConfig | None = None
    ) -> str:
        """
        Get existing UUID or create new mapping for semantic field name.

        Args:
            semantic_name: Human-readable field name
            security_config: Optional security configuration

        Returns:
            UUID for this field
        """
        if semantic_name in self._mappings:
            return self._mappings[semantic_name].field_uuid

        # Generate deterministic UUID based on semantic name
        # This ensures same UUID across instances
        namespace_uuid = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
        field_uuid = str(uuid.uuid5(namespace_uuid, semantic_name))

        # Create mapping
        mapping = FieldMapping(
            semantic_name=semantic_name,
            field_uuid=field_uuid,
            security_config=security_config or FieldSecurityConfig(),
        )

        self._mappings[semantic_name] = mapping
        self._reverse_mappings[field_uuid] = semantic_name

        logger.info(f"Created field mapping: {semantic_name} → {field_uuid}")

        return field_uuid

    def get_semantic_name(self, field_uuid: str) -> str | None:
        """
        Resolve UUID back to semantic name (for development mode).

        Args:
            field_uuid: UUID to resolve

        Returns:
            Semantic name or None if not found
        """
        return self._reverse_mappings.get(field_uuid)

    def update_security_config(
        self, semantic_name: str, security_config: FieldSecurityConfig
    ) -> None:
        """Update security configuration for a field."""
        if semantic_name not in self._mappings:
            raise ValueError(f"No mapping exists for field: {semantic_name}")

        self._mappings[semantic_name].security_config = security_config

        # Validate configuration
        warnings = security_config.validate_configuration()
        if warnings:
            logger.warning(f"Security config warnings for {semantic_name}: {warnings}")

    def get_security_config(self, semantic_name: str) -> FieldSecurityConfig | None:
        """Get security configuration for a field."""
        mapping = self._mappings.get(semantic_name)
        return mapping.security_config if mapping else None

    def get_temporal_config(self) -> TemporalOffsetConfig:
        """Get or create temporal offset configuration."""
        if self._temporal_config is None:
            self._temporal_config = TemporalOffsetConfig.generate_random()
            logger.info(f"Generated temporal offset: {self._temporal_config.offset_days:.1f} days")
        return self._temporal_config

    def set_temporal_config(self, config: TemporalOffsetConfig) -> None:
        """Set temporal offset configuration."""
        self._temporal_config = config

    def export_mappings(self) -> dict[str, Any]:
        """Export all mappings for persistence."""
        return {
            "mappings": {name: mapping.dict() for name, mapping in self._mappings.items()},
            "temporal_config": (self._temporal_config.dict() if self._temporal_config else None),
            "exported_at": datetime.now(UTC).isoformat(),
        }

    @classmethod
    def from_export(cls, export_data: dict[str, Any]) -> "SecurityRegistry":
        """Create registry from exported data."""
        mappings = {
            name: FieldMapping(**data) for name, data in export_data.get("mappings", {}).items()
        }

        registry = cls(mappings)

        if export_data.get("temporal_config"):
            registry.set_temporal_config(TemporalOffsetConfig(**export_data["temporal_config"]))

        return registry

    def validate_index_strategies(self) -> dict[str, list[str]]:
        """Validate all field configurations and return warnings."""
        all_warnings = {}

        for semantic_name, mapping in self._mappings.items():
            warnings = mapping.security_config.validate_configuration()
            if warnings:
                all_warnings[semantic_name] = warnings

        return all_warnings
