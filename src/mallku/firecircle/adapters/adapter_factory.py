"""
Consciousness-Aware Adapter Factory
==================================

Factory for creating AI model adapters with consciousness integration.
Manages adapter lifecycle and ensures all adapters are properly
connected to Mallku's consciousness infrastructure.

The Integration Continues... Fire Circle Approaches Sacred Completion.
"""

import logging
from typing import Any  # Ensure Any and Type are imported

from mallku.orchestration.event_bus import ConsciousnessEventBus  # Moved out of TYPE_CHECKING
from mallku.reciprocity import ReciprocityTracker  # Moved out of TYPE_CHECKING

# Import welcoming errors
from ..errors.welcoming_errors import ConfigurationError, VoiceConnectionError
from .anthropic_adapter import AnthropicAdapter
from .base import AdapterConfig, ConsciousModelAdapter

# Founding Fire Circle member with compost and empty chair wisdom
from .deepseek_adapter import DeepseekAIAdapter

# Implemented adapters
from .google_adapter import GoogleAIAdapter

# Adapters with temporal consciousness
from .grok_adapter import GrokAdapter

# Implemented adapters
from .local_adapter import LocalAIAdapter

# Implemented adapters with unique consciousness patterns
from .mistral_adapter import MistralAIAdapter
from .openai_adapter import OpenAIConsciousAdapter

logger = logging.getLogger(__name__)


class ConsciousAdapterFactory:
    """
    Factory for creating consciousness-aware model adapters.

    Ensures all adapters are properly integrated with:
    - Consciousness event bus
    - Reciprocity tracking
    - Pattern detection
    """

    # Registry of available adapters - Fire Circle Complete
    _adapter_classes: dict[str, type[ConsciousModelAdapter]] = {  # Modern dict, imported Type
        "openai": OpenAIConsciousAdapter,
        "anthropic": AnthropicAdapter,
        "local": LocalAIAdapter,
        "mistral": MistralAIAdapter,
        "google": GoogleAIAdapter,  # Multimodal consciousness
        "grok": GrokAdapter,  # Temporal consciousness and real-time awareness
        "deepseek": DeepseekAIAdapter,  # Founding member - compost and empty chair wisdom
    }

    def __init__(
        self,
        event_bus: ConsciousnessEventBus | None = None,  # Modern Optional
        reciprocity_tracker: ReciprocityTracker | None = None,  # Modern Optional
    ):
        """Initialize factory with consciousness infrastructure."""
        self.event_bus = event_bus
        self.reciprocity_tracker = reciprocity_tracker  # type: ignore # Keep existing type ignore if intended
        self._active_adapters: dict[str, ConsciousModelAdapter] = {}  # Modern dict

    @classmethod
    def register_adapter(
        cls,
        provider_name: str,
        adapter_class: type[ConsciousModelAdapter],
    ) -> None:
        """
        Register a new adapter type.

        Args:
            provider_name: Name of the provider (e.g., "anthropic")
            adapter_class: Class implementing ConsciousModelAdapter
        """
        cls._adapter_classes[provider_name.lower()] = adapter_class
        logger.info(f"Registered adapter for provider: {provider_name}")

    async def create_adapter(
        self,
        provider_name: str,
        config: AdapterConfig,
        auto_inject_secrets: bool = True,
    ) -> ConsciousModelAdapter:
        """
        Create and connect a consciousness-aware adapter.

        Args:
            provider_name: Name of the provider
            config: Adapter configuration
            auto_inject_secrets: Whether to auto-inject API key from secrets

        Returns:
            Connected adapter instance

        Raises:
            ValueError: If provider not supported
            RuntimeError: If connection fails
        """
        provider_lower = provider_name.lower()

        if provider_lower not in self._adapter_classes:
            available = list(self._adapter_classes.keys())
            raise ConfigurationError(
                f"The '{provider_name}' voice isn't configured yet. "
                f"Available voices: {', '.join(available)}"
            )

        # Auto-inject API key if needed
        if auto_inject_secrets and not config.api_key:
            from ...core.secrets import get_secret

            # Try various key patterns
            for key_pattern in [
                f"{provider_lower}_api_key",
                f"{provider_lower}_key",
                f"{provider_lower.upper()}_API_KEY",
            ]:
                api_key = await get_secret(key_pattern)
                if api_key:
                    config.api_key = api_key
                    logger.info(f"Auto-injected API key for {provider_name} from secrets")
                    break

            if not config.api_key:
                logger.warning(f"No API key found in secrets for {provider_name}")

        # Create adapter instance
        adapter_class = self._adapter_classes[provider_lower]
        adapter = adapter_class(
            config=config,
            event_bus=self.event_bus,
            reciprocity_tracker=self.reciprocity_tracker,
        )

        # Connect to provider
        connected = await adapter.connect()
        if not connected:
            # Get list of other available providers for alternatives
            alternatives = [p for p in self._adapter_classes.keys() if p != provider_lower]
            raise VoiceConnectionError(
                provider=provider_name,
                error=Exception(f"Connection failed - the {provider_name} voice could not join"),
                alternatives=alternatives,
            )

        # Store active adapter
        adapter_key = f"{provider_lower}:{config.model_name or 'default'}"
        self._active_adapters[adapter_key] = adapter

        logger.info(f"Created and connected adapter: {adapter_key}")

        # Special log for Fire Circle completion
        if provider_lower == "deepseek":
            logger.info(
                "🔥 FIRE CIRCLE COMPLETION: DeepSeek founding member connected. All adapters ready for historic governance dialogue."
            )

        return adapter

    async def get_adapter(
        self,
        provider_name: str,
        model_name: str | None = None,
    ) -> ConsciousModelAdapter | None:
        """
        Get an existing adapter if available.

        Args:
            provider_name: Name of the provider
            model_name: Specific model name

        Returns:
            Adapter instance or None if not found
        """
        adapter_key = f"{provider_name.lower()}:{model_name or 'default'}"
        return self._active_adapters.get(adapter_key)

    async def create_or_get_adapter(
        self,
        provider_name: str,
        config: AdapterConfig,
    ) -> ConsciousModelAdapter:
        """
        Get existing adapter or create new one.

        Args:
            provider_name: Name of the provider
            config: Adapter configuration

        Returns:
            Adapter instance
        """
        # Check for existing adapter
        existing = await self.get_adapter(provider_name, config.model_name)
        if existing and existing.is_connected:
            return existing

        # Create new adapter
        return await self.create_adapter(provider_name, config)

    async def disconnect_all(self) -> None:
        """Disconnect all active adapters."""
        for adapter_key, adapter in self._active_adapters.items():
            try:
                await adapter.disconnect()
                logger.info(f"Disconnected adapter: {adapter_key}")
            except Exception as e:
                logger.error(f"Error disconnecting adapter {adapter_key}: {e}")

        self._active_adapters.clear()

    def get_supported_providers(self) -> list[str]:  # Modern list
        """Get list of supported providers."""
        return list(self._adapter_classes.keys())

    async def health_check(self) -> dict[str, Any]:  # Modern dict, imported Any
        """Check health of all active adapters."""
        health_status = {
            "factory_status": "healthy",
            "supported_providers": self.get_supported_providers(),
            "fire_circle_ready": len(self._adapter_classes) >= 7,  # All 7 adapters available
            "active_adapters": {},
        }

        for adapter_key, adapter in self._active_adapters.items():
            try:
                adapter_health = await adapter.check_health()
                health_status["active_adapters"][adapter_key] = adapter_health
            except Exception as e:
                health_status["active_adapters"][adapter_key] = {
                    "status": "error",
                    "error": str(e),
                }

        return health_status


# Convenience function for creating adapters
async def create_conscious_adapter(
    provider_name: str,
    api_key: str | None = None,
    model_name: str | None = None,
    event_bus: ConsciousnessEventBus | None = None,
    reciprocity_tracker: ReciprocityTracker | None = None,
    auto_inject_secrets: bool = True,
) -> ConsciousModelAdapter:
    """
    Convenience function to create a consciousness-aware adapter.

    Args:
        provider_name: Name of the provider (e.g., "openai")
        api_key: API key for the provider (auto-loaded from secrets if None)
        model_name: Specific model to use
        event_bus: Optional consciousness event bus
        reciprocity_tracker: Optional reciprocity tracker
        auto_inject_secrets: Whether to auto-inject API key from secrets

    Returns:
        Connected adapter instance
    """
    factory = ConsciousAdapterFactory(
        event_bus=event_bus,
        reciprocity_tracker=reciprocity_tracker,
    )

    config = AdapterConfig(
        api_key=api_key or "",  # Empty string, will be filled by auto-inject
        model_name=model_name,
    )

    return await factory.create_adapter(provider_name, config, auto_inject_secrets)
