"""
Base model for Mallku that integrates security features.

This replaces the direct use of ObfuscatedModel with a Mallku-specific
implementation that includes our field-level security strategies.
"""

import builtins
from typing import Any, get_type_hints

from pydantic import BaseModel
from pydantic import Field as PydanticField

from .field_strategies import FieldIndexStrategy, FieldObfuscationLevel, FieldSecurityConfig
from .registry import SecurityRegistry


def SecuredField(
    default: Any = ...,
    *,
    obfuscation_level: FieldObfuscationLevel = FieldObfuscationLevel.UUID_ONLY,
    index_strategy: FieldIndexStrategy = FieldIndexStrategy.NONE,
    search_capabilities: list = None,
    security_notes: str = None,
    **kwargs
) -> Any:
    """
    Enhanced Pydantic Field with security configuration.

    Example:
        timestamp: datetime = SecuredField(
            obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
            index_strategy=FieldIndexStrategy.TEMPORAL_OFFSET,
            search_capabilities=[SearchCapability.RANGE, SearchCapability.ORDERING],
            security_notes="Temporal offset preserves relative time while hiding absolute dates"
        )
    """
    # Create security configuration
    security_config = FieldSecurityConfig(
        obfuscation_level=obfuscation_level,
        index_strategy=index_strategy,
        search_capabilities=search_capabilities or [],
        security_notes=security_notes
    )

    # Store security config in field's json_schema_extra
    if 'json_schema_extra' not in kwargs:
        kwargs['json_schema_extra'] = {}

    kwargs['json_schema_extra']['security_config'] = security_config.dict()

    # Create field with metadata
    return PydanticField(default, **kwargs)


class SecuredModel(BaseModel):
    """
    Base model for Mallku with integrated security features.

    This model:
    - Automatically obfuscates field names to UUIDs
    - Applies field-level security strategies
    - Maintains registry of mappings
    - Supports development mode for debugging
    """

    _registry: SecurityRegistry | None = None
    _development_mode: bool = False

    class Config:
        # Allow extra fields for metadata
        extra = "allow"
        # Use enum values in serialization
        use_enum_values = True

    @classmethod
    def set_registry(cls, registry: SecurityRegistry) -> None:
        """Set the security registry for this model class."""
        cls._registry = registry

    @classmethod
    def set_development_mode(cls, enabled: bool) -> None:
        """Enable/disable development mode (shows semantic names)."""
        cls._development_mode = enabled

    def dict(self, **kwargs) -> dict[str, Any]:
        """
        Override dict() to apply field obfuscation.

        In production mode, field names are replaced with UUIDs.
        In development mode, both UUID and semantic names are included.
        """
        # Get base dictionary
        data = super().dict(**kwargs)

        if not self._registry:
            # No registry configured, return as-is
            return data

        # Get field security configurations
        obfuscated_data = {}
        get_type_hints(self.__class__)

        for field_name, field_value in data.items():
            # Skip private fields
            if field_name.startswith('_'):
                continue

            # Get field info and security config
            field_info = self.__fields__.get(field_name)
            security_config = None

            if field_info and hasattr(field_info, 'json_schema_extra'):
                config_dict = field_info.json_schema_extra.get('security_config')
                if config_dict:
                    security_config = FieldSecurityConfig(**config_dict)

            if not security_config:
                # Default security config
                security_config = FieldSecurityConfig()

            # Get or create UUID mapping
            field_uuid = self._registry.get_or_create_mapping(
                field_name,
                security_config
            )

            # Apply obfuscation based on level
            if security_config.obfuscation_level == FieldObfuscationLevel.NONE:
                # No obfuscation
                obfuscated_data[field_name] = field_value
            else:
                # Obfuscate field name
                if self._development_mode:
                    # Development mode: include both UUID and semantic name
                    obfuscated_data[field_uuid] = {
                        "_semantic_name": field_name,
                        "value": field_value
                    }
                else:
                    # Production mode: UUID only
                    obfuscated_data[field_uuid] = field_value

        return obfuscated_data
    
    def to_storage_dict(self, registry: SecurityRegistry) -> Any:
        """
        Convert this secured model to a storage-ready dictionary using the provided registry.
        """
        # Ensure registry is set for obfuscation
        self.set_registry(registry)
        # Use dict() to apply field obfuscation
        return self.dict()

    @classmethod
    def from_obfuscated(cls, data: builtins.dict[str, Any]) -> "SecuredModel":
        """
        Create instance from obfuscated data.

        Resolves UUIDs back to semantic field names for instantiation.
        """
        if not cls._registry:
            # No registry, assume data is not obfuscated
            return cls(**data)

        # Resolve UUIDs to semantic names
        resolved_data = {}

        for key, value in data.items():
            # Try to resolve as UUID
            semantic_name = cls._registry.get_semantic_name(key)

            if semantic_name:
                # This was an obfuscated field
                if isinstance(value, dict) and "_semantic_name" in value:
                    # Development mode data
                    resolved_data[semantic_name] = value["value"]
                else:
                    # Production mode data
                    resolved_data[semantic_name] = value
            else:
                # Not obfuscated or unknown field
                resolved_data[key] = value

        return cls(**resolved_data)
    
    @classmethod
    def from_storage_dict(cls, data: Any) -> "SecuredModel":
        """
        Alias for from_obfuscated to maintain backwards compatibility.
        """
        return cls.from_obfuscated(data)

    def validate_security_configuration(self) -> builtins.dict[str, list[str]]:
        """Validate all field security configurations."""
        warnings = {}

        for field_name, field_info in self.__fields__.items():
            if hasattr(field_info, 'json_schema_extra'):
                config_dict = field_info.json_schema_extra.get('security_config')
                if config_dict:
                    security_config = FieldSecurityConfig(**config_dict)
                    field_warnings = security_config.validate_configuration()
                    if field_warnings:
                        warnings[field_name] = field_warnings

        return warnings
