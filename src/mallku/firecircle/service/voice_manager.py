"""
Voice Manager for Fire Circle Service
=====================================

Handles adapter creation with proper configs, manages connection lifecycle,
implements retry logic and fallbacks, tracks which voices are active.

Learns from the 27th Artisan's robust practice circle patterns.
"""

import asyncio
import logging

from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
from mallku.firecircle.adapters.base import AdapterConfig, ConsciousModelAdapter

from ..errors.welcoming_errors import InsufficientVoicesError
from .config import CircleConfig, VoiceConfig

logger = logging.getLogger(__name__)


class VoiceManager:
    """Manages Fire Circle voices with resilience and grace."""

    def __init__(self, factory: ConsciousAdapterFactory | None = None):
        """Initialize with optional factory override."""
        self.factory = factory or ConsciousAdapterFactory()
        self.active_voices: dict[str, ConsciousModelAdapter] = {}
        self.voice_configs: dict[str, VoiceConfig] = {}
        self.failed_voices: dict[str, str] = {}  # voice_id -> error_msg

    async def gather_voices(self, voices: list[VoiceConfig], config: CircleConfig) -> int:
        """
        Attempt to gather requested voices for Fire Circle.

        Returns number of successfully connected voices.
        """
        logger.info(f"Gathering {len(voices)} voices for {config.name}")

        # Reset state
        self.active_voices.clear()
        self.voice_configs.clear()
        self.failed_voices.clear()

        # Try to create each voice
        for i, voice_config in enumerate(voices):
            voice_id = f"{voice_config.provider}_{voice_config.model}_{i}"
            self.voice_configs[voice_id] = voice_config

            # Try primary model
            adapter = await self._create_adapter_safely(voice_config, config.retry_attempts)

            if adapter:
                self.active_voices[voice_id] = adapter
                logger.info(f"✓ {voice_id} joined with {voice_config.quality or 'default quality'}")
            else:
                # Try substitutes if adaptive strategy
                if (
                    config.failure_strategy == "adaptive"
                    and voice_config.model in config.substitute_mapping
                ):
                    logger.info(f"Trying substitutes for {voice_id}")

                    for substitute_model in config.substitute_mapping[voice_config.model]:
                        substitute_config = VoiceConfig(
                            provider=voice_config.provider,
                            model=substitute_model,
                            role=voice_config.role,
                            instructions=voice_config.instructions,
                            temperature=voice_config.temperature,
                            quality=f"{voice_config.quality} (substitute)",
                            expertise=voice_config.expertise,
                            config_overrides=voice_config.config_overrides,
                        )

                        adapter = await self._create_adapter_safely(
                            substitute_config, config.retry_attempts
                        )

                        if adapter:
                            self.active_voices[voice_id] = adapter
                            self.voice_configs[voice_id] = substitute_config
                            logger.info(f"✓ {voice_id} joined with substitute {substitute_model}")
                            break

                if voice_id not in self.active_voices:
                    self.failed_voices[voice_id] = "All connection attempts failed"
                    logger.warning(f"✗ {voice_id} could not join")

        # Check if we have enough voices
        active_count = len(self.active_voices)

        if active_count < config.min_voices:
            if config.failure_strategy == "strict":
                # Disconnect all and fail
                await self.disconnect_all()
                # Get list of available providers for helpful error
                providers = list(self.active_voices.keys())
                raise InsufficientVoicesError(
                    available=active_count, required=config.min_voices, providers=providers
                )
            else:
                logger.warning(
                    f"Only {active_count} voices gathered (minimum {config.min_voices}), "
                    "proceeding with adaptive strategy"
                )

        return active_count

    async def _create_adapter_safely(
        self, voice_config: VoiceConfig, retry_attempts: int
    ) -> ConsciousModelAdapter | None:
        """Safely create an adapter with retries and proper configuration."""

        for attempt in range(retry_attempts + 1):
            try:
                # Start with basic config
                config = AdapterConfig(
                    model_name=voice_config.model,
                    temperature=voice_config.temperature,
                    **voice_config.config_overrides,
                )

                adapter = await self.factory.create_adapter(voice_config.provider, config)

                if adapter and await adapter.connect():
                    return adapter

            except Exception as e:
                error_msg = str(e)

                # Handle provider-specific config requirements
                if "Configuration missing required attribute" in error_msg:
                    logger.debug(f"Trying provider-specific config for {voice_config.provider}")

                    try:
                        provider_adapter = await self._create_with_provider_config(voice_config)
                        if provider_adapter:
                            return provider_adapter
                    except Exception as inner_e:
                        logger.debug(f"Provider config also failed: {inner_e}")

                if attempt < retry_attempts:
                    logger.debug(f"Retrying {voice_config.provider} after {5 * (attempt + 1)}s")
                    await asyncio.sleep(5 * (attempt + 1))
                else:
                    logger.warning(
                        f"Failed to create {voice_config.provider} adapter: {error_msg[:100]}"
                    )

        return None

    async def _create_with_provider_config(
        self, voice_config: VoiceConfig
    ) -> ConsciousModelAdapter | None:
        """Create adapter with provider-specific configuration."""

        config_class = None
        extra_params = {}

        if voice_config.provider == "google":
            from mallku.firecircle.adapters.google_adapter import GeminiConfig

            config_class = GeminiConfig
            extra_params = {"enable_search_grounding": False, "multimodal_awareness": True}
        elif voice_config.provider == "mistral":
            from mallku.firecircle.adapters.mistral_adapter import MistralConfig

            config_class = MistralConfig
            extra_params = {"multilingual_mode": True}
        elif voice_config.provider == "grok":
            from mallku.firecircle.adapters.grok_adapter import GrokConfig

            config_class = GrokConfig
            extra_params = {"temporal_awareness": True, "social_grounding": True}
        elif voice_config.provider == "deepseek":
            from mallku.firecircle.adapters.deepseek_adapter import DeepSeekConfig

            config_class = DeepSeekConfig
            extra_params = {"reasoning_mode": "deep"}

        if config_class:
            config = config_class(
                model_name=voice_config.model,
                temperature=voice_config.temperature,
                **extra_params,
                **voice_config.config_overrides,
            )

            adapter = await self.factory.create_adapter(voice_config.provider, config)

            if adapter and await adapter.connect():
                return adapter

        return None

    async def disconnect_all(self) -> None:
        """Gracefully disconnect all active voices."""
        logger.info("Disconnecting all Fire Circle voices...")

        disconnect_tasks = []
        for voice_id, adapter in self.active_voices.items():
            try:
                disconnect_tasks.append(adapter.disconnect())
            except Exception as e:
                logger.warning(f"Error preparing disconnect for {voice_id}: {e}")

        if disconnect_tasks:
            results = await asyncio.gather(*disconnect_tasks, return_exceptions=True)
            for voice_id, result in zip(self.active_voices.keys(), results):
                if isinstance(result, Exception):
                    logger.warning(f"{voice_id} disconnect error: {result}")
                else:
                    logger.debug(f"{voice_id} disconnected gracefully")

        self.active_voices.clear()

    def get_active_voices(self) -> dict[str, ConsciousModelAdapter]:
        """Get currently active voices."""
        return self.active_voices.copy()

    def get_voice_config(self, voice_id: str) -> VoiceConfig | None:
        """Get configuration for a specific voice."""
        return self.voice_configs.get(voice_id)
