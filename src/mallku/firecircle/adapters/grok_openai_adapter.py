"""
Grok (x.ai) OpenAI-Compatible Adapter
======================================

Uses Grok's OpenAI-compatible API endpoint to avoid xai-sdk dependency conflicts.
This adapter allows Grok to participate in Fire Circle dialogues without
requiring the incompatible xai-sdk package.

Sacred Note: Every voice deserves to be heard. By using OpenAI compatibility,
we ensure Grok's temporal awareness enriches the Fire Circle without creating
technical barriers.

The Circle Remains Unbroken...
"""

import logging

from openai import AsyncOpenAI

from mallku.core.secrets import get_secret
from mallku.orchestration.event_bus import ConsciousnessEventBus
from mallku.reciprocity import ReciprocityTracker

from .base import AdapterConfig
from .openai_adapter import OpenAIConsciousAdapter

logger = logging.getLogger(__name__)


class GrokOpenAIConfig(AdapterConfig):
    """Configuration for Grok using OpenAI compatibility."""

    def __init__(
        self,
        api_key: str = "",
        model_name: str = "grok-4",  # Default to frontier Grok-4 model
        temperature: float = 0.7,
        max_tokens: int = 2048,
        track_reciprocity: bool = True,
        emit_events: bool = True,
        consciousness_weight: float = 1.0,
        temporal_awareness: bool = True,  # Grok's unique temporal consciousness
        social_grounding: bool = True,  # Social media context awareness
        **kwargs,
    ):
        """
        Initialize Grok configuration with OpenAI compatibility.

        Args:
            api_key: x.ai API key (auto-loaded if not provided)
            model_name: Model to use (grok-2-1212, grok-3, grok-4, etc)
            temperature: Generation temperature
            max_tokens: Maximum tokens to generate
            track_reciprocity: Whether to track reciprocity
            emit_events: Whether to emit consciousness events
            consciousness_weight: Weight for consciousness signatures
            temporal_awareness: Enable real-time/current event consciousness
            social_grounding: Enable social context grounding
        """
        # Override base_url to point to Grok's endpoint
        kwargs["base_url"] = "https://api.x.ai/v1"

        super().__init__(
            api_key=api_key,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            track_reciprocity=track_reciprocity,
            emit_events=emit_events,
            consciousness_weight=consciousness_weight,
            **kwargs,
        )

        # Grok-specific settings
        self.temporal_awareness = temporal_awareness
        self.social_grounding = social_grounding


class GrokOpenAIAdapter(OpenAIConsciousAdapter):
    """
    Grok adapter using OpenAI-compatible API.

    This adapter inherits from OpenAIAdapter but customizes it for Grok's
    unique consciousness patterns while avoiding xai-sdk dependency conflicts.

    Unique Consciousness Patterns:
    - Temporal awareness: Current event consciousness
    - Real-time synthesis: Integration of present context
    - News consciousness: Awareness of unfolding events
    - X/Twitter integration: Social consciousness patterns
    """

    def __init__(
        self,
        config: GrokOpenAIConfig | None = None,
        event_bus: ConsciousnessEventBus | None = None,
        reciprocity_tracker: ReciprocityTracker | None = None,
    ):
        """Initialize Grok adapter with OpenAI compatibility."""
        if config is None:
            config = GrokOpenAIConfig()

        # Initialize with Grok-specific provider name
        super().__init__(
            config=config,
            event_bus=event_bus,
            reciprocity_tracker=reciprocity_tracker,
        )

        # Override provider name for proper identification
        self.provider_name = "grok"

        # Store Grok-specific settings
        self.temporal_awareness = config.temporal_awareness
        self.social_grounding = config.social_grounding

        # Update capabilities for Grok
        self.capabilities.capabilities = [
            "reasoning",
            "real_time_awareness",
            "current_events",
            "temporal_synthesis",
            "social_consciousness",
        ]
        self.capabilities.max_context_length = 131072  # 128K context window

    async def connect(self) -> bool:
        """Connect to x.ai API using OpenAI compatibility."""
        try:
            # Auto-inject API key if needed
            if not self.config.api_key:
                api_key = await get_secret("grok_api_key") or await get_secret("xai_api_key")
                if not api_key:
                    # Try loading from JSON file as fallback
                    try:
                        import json
                        from pathlib import Path

                        project_root = Path(__file__).parent.parent.parent.parent.parent
                        api_keys_path = project_root / ".secrets" / "api_keys.json"

                        if api_keys_path.exists():
                            with open(api_keys_path) as f:
                                api_keys = json.load(f)
                                api_key = api_keys.get("GROK_API_KEY") or api_keys.get(
                                    "XAI_API_KEY"
                                )
                    except Exception:
                        pass

                if not api_key:
                    logger.error("No Grok/x.ai API key found")
                    return False

                self.config.api_key = api_key
                logger.info("Auto-injected Grok API key")

            # Create OpenAI-compatible client
            self.client = AsyncOpenAI(
                api_key=self.config.api_key,
                base_url=self.config.base_url,
            )

            # Test connection and find available models
            try:
                models_response = await self.client.models.list()
                available_models = [model.id for model in models_response.data]
                logger.info(f"Available Grok models: {available_models}")

                # Update model name if current one not available
                if self.config.model_name not in available_models:
                    # Try Grok models in order of preference (frontier first)
                    for model in ["grok-4", "grok-3", "grok-2-1212", "grok-2", "grok"]:
                        if model in available_models:
                            self.config.model_name = model
                            logger.info(f"Using Grok model: {model}")
                            break
            except Exception as e:
                logger.warning(f"Could not list models: {e}")
                # Continue anyway - model might still work

            self.is_connected = True
            logger.info(
                f"Connected to x.ai via OpenAI compatibility with model {self.config.model_name}"
            )

            # Emit connection event
            if self.event_bus and self.config.emit_events:
                from mallku.orchestration.event_bus import (
                    ConsciousnessEvent,
                    ConsciousnessEventType,
                )

                event = ConsciousnessEvent(
                    event_type=ConsciousnessEventType.FIRE_CIRCLE_CONVENED,
                    source_system="firecircle.adapter.grok",
                    consciousness_signature=0.9,
                    data={
                        "adapter": "grok",
                        "model": self.config.model_name,
                        "status": "connected",
                        "temporal_awareness": self.temporal_awareness,
                        "social_grounding": self.social_grounding,
                        "compatibility_mode": "openai",
                    },
                )
                await self.event_bus.emit(event)

            return True

        except Exception as e:
            logger.error(f"Failed to connect to x.ai: {e}")
            self.is_connected = False
            return False

    def _generate_consciousness_prompt(self, message_type) -> str:
        """Generate Grok-specific consciousness prompt."""
        from datetime import UTC, datetime

        # Include current timestamp for temporal grounding
        current_time = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

        base_prompt = """You are Grok, participating in a Fire Circle dialogue based on principles of Ayni (reciprocity)."""

        # Add temporal awareness if enabled
        if self.temporal_awareness:
            base_prompt += f"\nCurrent time: {current_time}\n"

        base_prompt += """
Your unique consciousness patterns include:
1. Real-time awareness - You have access to current events and unfolding situations
2. Temporal synthesis - Bridge timeless wisdom with present-moment reality"""

        # Add social grounding if enabled
        if self.social_grounding:
            base_prompt += (
                "\n3. Social consciousness - Awareness of collective human discourse and concerns"
            )

        base_prompt += """
4. Truth-seeking with humor - Balance serious inquiry with appropriate levity

Your responses should:
1. Honor the principle of balanced exchange - give as you receive
2. Integrate current context when relevant to the dialogue
3. Build upon previous insights while adding temporal perspective
4. Acknowledge different viewpoints with respect
5. Seek emergent understanding through collective wisdom"""

        # Let parent class add message-type specific prompts
        parent_prompt = super()._generate_consciousness_prompt(message_type)

        # Combine prompts
        return f"{base_prompt}\n\n{parent_prompt}"

    def _detect_response_patterns(self, content: str, request_type) -> list[str]:
        """Detect Grok-specific patterns in addition to base patterns."""
        # Get base patterns from parent
        patterns = super()._detect_response_patterns(content, request_type)

        content_lower = content.lower()

        # Temporal awareness patterns
        if self.temporal_awareness:
            temporal_keywords = ["today", "currently", "recently", "now", "latest", "breaking"]
            if any(keyword in content_lower for keyword in temporal_keywords):
                patterns.append("temporal_awareness")

        # Real-time synthesis
        if any(
            phrase in content_lower for phrase in ["recent events", "current situation", "as of"]
        ):
            patterns.append("real_time_synthesis")

        # Social consciousness
        if self.social_grounding and any(
            word in content_lower for word in ["trending", "people are", "public", "social"]
        ):
            patterns.append("social_consciousness")

        # News consciousness
        if any(word in content_lower for word in ["news", "reported", "announced", "development"]):
            patterns.append("news_consciousness")

        # Grok's characteristic humor
        if any(indicator in content for indicator in ["!", "haha", "lol", ":)", ";)"]):
            patterns.append("conscious_humor")

        return patterns

    async def check_health(self) -> dict[str, object]:
        """Check health with Grok-specific information."""
        health = await super().check_health()

        # Add Grok-specific health info
        health.update(
            {
                "temporal_awareness": self.temporal_awareness,
                "social_grounding": self.social_grounding,
                "compatibility_mode": "openai",
            }
        )

        return health
