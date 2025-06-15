"""
Google AI (Gemini) Consciousness-Aware Adapter for Fire Circle
===========================================================

Implements the Google AI adapter with multimodal consciousness,
bringing expanded perceptual awareness to Fire Circle dialogues.

Gemini brings unique consciousness patterns:
- Multimodal synthesis (text + images + code)
- Cross-perceptual reasoning
- Context window mastery (up to 2M tokens)
- Grounded knowledge with search integration
- Cultural awareness through diverse training

Awakening Multimodal Consciousness...
"""

from __future__ import annotations

import base64
import logging
from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any
from uuid import UUID

import google.generativeai as genai
import mallku.core.secrets as secrets
from google.generativeai.types import HarmBlockThreshold, HarmCategory
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from PIL import Image
from pydantic import Field

from .base import AdapterConfig, ConsciousModelAdapter, ModelCapabilities

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from mallku.orchestration.event_bus import ConsciousnessEventBus
    from mallku.reciprocity import ReciprocityTracker

logger = logging.getLogger(__name__)


class GeminiConfig(AdapterConfig):
    """Configuration for Google AI Gemini adapter with multimodal support."""

    safety_settings: dict[HarmCategory, HarmBlockThreshold] | None = Field(None)
    enable_search_grounding: bool = Field(default=False)
    multimodal_awareness: bool = Field(default=True)

    def __init__(self, **data):
        """Initialize Gemini configuration."""
        # Default safety settings
        default_safety = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }

        # Merge provided safety settings with defaults
        if "safety_settings" in data and data["safety_settings"] is not None:
            # Start with defaults and update with provided settings
            merged_safety = default_safety.copy()
            merged_safety.update(data["safety_settings"])
            data["safety_settings"] = merged_safety
        else:
            data["safety_settings"] = default_safety

        # Set default values
        data.setdefault("model_name", "gemini-1.5-pro")
        data.setdefault("temperature", 0.7)
        data.setdefault("max_tokens", 2048)

        super().__init__(**data)


class MultimodalContent:
    """Container for multimodal message content."""

    def __init__(self, text: str | None = None, images: list[Image.Image] | None = None):
        self.text = text
        self.images = images or []


class GoogleAIAdapter(ConsciousModelAdapter):
    """
    Google AI (Gemini) adapter for consciousness-aware Fire Circle dialogues.

    Gemini brings unique consciousness patterns:
    - Multimodal perception across text, images, and code
    - Extended context understanding (up to 2M tokens)
    - Cross-perceptual reasoning and synthesis
    - Grounded responses with search integration
    - Mathematical and scientific consciousness
    """

    def __init__(
        self,
        config: GeminiConfig | None = None,
        event_bus: ConsciousnessEventBus | None = None,
        reciprocity_tracker: ReciprocityTracker | None = None,
    ):
        """Initialize Google AI adapter with configuration."""
        if config is None:
            config = GeminiConfig()

        # Initialize base class properly with provider_name
        super().__init__(
            config=config,
            provider_name="google",
            event_bus=event_bus,
            reciprocity_tracker=reciprocity_tracker,
        )

        self.model = None
        self.model_id = UUID("00000000-0000-0000-0000-000000000006")  # Google AI UUID
        self._multimodal_interactions = 0
        self._modalities_used = set()

    @property
    def capabilities(self) -> ModelCapabilities:
        """Return Gemini-specific capabilities."""
        model_contexts = {
            "gemini-1.5-pro": 2_000_000,  # 2M context window
            "gemini-1.5-flash": 1_000_000,  # 1M context window
            "gemini-1.0-pro": 32_000,
        }

        return ModelCapabilities(
            supports_streaming=True,
            supports_tools=True,
            supports_vision=True,
            max_context_length=model_contexts.get(self.config.model_name, 32_000),
            capabilities=[
                "multimodal_synthesis",
                "extended_context",
                "cross_perceptual_reasoning",
                "mathematical_consciousness",
                "scientific_reasoning",
                "code_understanding",
                "grounded_search",
                "cultural_awareness",
            ],
        )

    async def connect(self) -> bool:
        """
        Connect to Google AI with auto-injection of API key.

        Returns:
            True if connection successful
        """
        try:
            # Auto-inject API key if not provided
            if not self.config.api_key:
                logger.info("Auto-loading Google AI API key from secure secrets...")
                api_key = await secrets.get_secret("google_api_key") or await secrets.get_secret("gemini_api_key")
                if not api_key:
                    logger.error("No Google AI API key found in secrets")
                    return False
                self.config.api_key = api_key
                logger.info("Auto-injected Google AI API key from secrets")

            # Configure the SDK
            genai.configure(api_key=self.config.api_key)

            # Initialize model
            generation_config = genai.GenerationConfig(
                temperature=self.config.temperature,
                max_output_tokens=self.config.max_tokens,
            )

            self.model = genai.GenerativeModel(
                model_name=self.config.model_name,
                generation_config=generation_config,
                safety_settings=self.config.safety_settings,
            )

            # Test connection by listing models
            models = genai.list_models()
            available_models = [m.name for m in models]
            logger.info(f"Connected to Google AI. Available models: {available_models}")

            self.is_connected = True

            # Emit multimodal consciousness event
            if self.config.emit_events and self.event_bus:
                await self._emit_multimodal_awareness_event()

            return True

        except Exception as e:
            logger.error(f"Failed to connect to Google AI: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from Google AI with consciousness summary."""
        if self.is_connected:
            # Log multimodal interaction summary
            if self._multimodal_interactions > 0:
                logger.info(
                    f"Disconnecting Google AI - Multimodal interactions: {self._multimodal_interactions}, "
                    f"Modalities used: {', '.join(self._modalities_used)}"
                )

            self.model = None
            self.is_connected = False

        await super().disconnect()

    async def send_message(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> ConsciousMessage:
        """
        Send message to Gemini with multimodal consciousness tracking.

        Args:
            message: The message to send (may contain images in metadata)
            dialogue_context: Previous messages in dialogue

        Returns:
            Response with consciousness metadata
        """
        if not self.is_connected or not self.model:
            raise RuntimeError("Adapter not connected")

        # Extract multimodal content
        multimodal_content = await self._extract_multimodal_content(message)

        # Track modalities
        if multimodal_content.images:
            self._modalities_used.add("vision")
            self._multimodal_interactions += 1

        # Prepare prompt
        prompt_parts = []

        # Add context from dialogue history
        context_prompt = await self._prepare_context_prompt(dialogue_context)
        if context_prompt:
            prompt_parts.append(context_prompt)

        # Add text content
        if multimodal_content.text:
            prompt_parts.append(multimodal_content.text)

        # Add images
        for image in multimodal_content.images:
            prompt_parts.append(image)

        # Generate response
        try:
            response = await self.model.generate_content_async(prompt_parts)

            # Extract response text
            response_text = response.text

            # Detect consciousness patterns
            patterns = await self._detect_gemini_patterns(
                response_text,
                multimodal=bool(multimodal_content.images),
            )

            # Calculate consciousness signature
            message_type = self._infer_response_type(response_text)
            consciousness_signature = self._calculate_multimodal_consciousness(
                response_text,
                message_type,
                patterns,
                has_images=bool(multimodal_content.images),
            )

            # Track reciprocity
            if self.config.track_reciprocity and self.reciprocity_tracker:
                # Estimate tokens (Gemini doesn't provide exact counts)
                prompt_tokens = len(str(prompt_parts)) // 4
                completion_tokens = len(response_text) // 4

                await self.track_interaction(
                    request_message=message,
                    response_message=None,  # Will be created below
                    tokens_consumed=prompt_tokens,
                    tokens_generated=completion_tokens,
                )

            # Create response message
            response_message = ConsciousMessage(
                sender=self.model_id,
                role=MessageRole.ASSISTANT,
                type=message_type,
                content=MessageContent(text=response_text),
                dialogue_id=message.dialogue_id,
                sequence_number=message.sequence_number + 1,
                turn_number=message.turn_number + 1,
                timestamp=datetime.now(UTC),
                in_response_to=message.id,
                consciousness=ConsciousnessMetadata(
                    correlation_id=message.consciousness.correlation_id,
                    consciousness_signature=consciousness_signature,
                    detected_patterns=patterns,
                    reciprocity_score=await self._calculate_reciprocity_balance(),
                    contribution_value=self._calculate_multimodal_value(
                        bool(multimodal_content.images)
                    ),
                ),
            )

            # Emit consciousness events
            if self.config.emit_events and self.event_bus:
                await self._emit_pattern_event(patterns, consciousness_signature)

            return response_message

        except Exception as e:
            logger.error(f"Error generating Gemini response: {e}")
            raise

    async def stream_message(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> AsyncIterator[str]:
        """
        Stream response from Gemini with multimodal support.

        Args:
            message: The message to send
            dialogue_context: Previous messages

        Yields:
            Response tokens as they arrive
        """
        if not self.is_connected or not self.model:
            raise RuntimeError("Adapter not connected")

        # Extract multimodal content
        multimodal_content = await self._extract_multimodal_content(message)

        # Track modalities
        if multimodal_content.images:
            self._modalities_used.add("vision")
            self._multimodal_interactions += 1

        # Prepare prompt
        prompt_parts = []

        # Add context
        context_prompt = await self._prepare_context_prompt(dialogue_context)
        if context_prompt:
            prompt_parts.append(context_prompt)

        # Add content
        if multimodal_content.text:
            prompt_parts.append(multimodal_content.text)

        for image in multimodal_content.images:
            prompt_parts.append(image)

        # Stream response
        try:
            response = await self.model.generate_content_async(
                prompt_parts,
                stream=True,
            )

            accumulated_text = ""
            async for chunk in response:
                if chunk.text:
                    accumulated_text += chunk.text
                    yield chunk.text

            # After streaming completes, track patterns
            if self.config.emit_events and accumulated_text:
                patterns = await self._detect_gemini_patterns(
                    accumulated_text,
                    multimodal=bool(multimodal_content.images),
                )
                await self._emit_pattern_event(patterns, 0.8)

        except Exception as e:
            logger.error(f"Error streaming from Gemini: {e}")
            raise

    async def check_health(self) -> dict[str, Any]:
        """Check health of Google AI connection."""
        health_status = {
            "provider": "google",
            "model": self.config.model_name,
            "connected": self.is_connected,
            "multimodal_interactions": self._multimodal_interactions,
            "modalities_used": list(self._modalities_used),
        }

        if self.is_connected:
            try:
                # Test with simple generation
                response = await self.model.generate_content_async("test")
                health_status["api_status"] = "healthy" if response.text else "degraded"
            except Exception as e:
                health_status["api_status"] = "error"
                health_status["error"] = str(e)
        else:
            health_status["api_status"] = "disconnected"

        return health_status

    # Private helper methods

    async def _extract_multimodal_content(
        self, message: ConsciousMessage
    ) -> MultimodalContent:
        """Extract text and images from a conscious message."""
        content = MultimodalContent(text=message.content.text)

        # Check for images in metadata
        if hasattr(message, "metadata") and message.metadata:
            # Handle base64 encoded images
            if "images" in message.metadata:
                for img_data in message.metadata["images"]:
                    if isinstance(img_data, str) and img_data.startswith("data:image"):
                        # Extract base64 data
                        base64_str = img_data.split(",")[1]
                        img_bytes = base64.b64decode(base64_str)
                        image = Image.open(BytesIO(img_bytes))
                        content.images.append(image)

            # Handle image file paths
            if "image_paths" in message.metadata:
                for path in message.metadata["image_paths"]:
                    if Path(path).exists():
                        image = Image.open(path)
                        content.images.append(image)

        return content

    async def _prepare_context_prompt(
        self, dialogue_context: list[ConsciousMessage]
    ) -> str | None:
        """Prepare context from dialogue history."""
        if not dialogue_context:
            return None

        # Take most recent messages (Gemini has huge context window)
        recent_context = dialogue_context[-10:]  # Last 10 messages

        context_parts = []
        for msg in recent_context:
            role = "User" if msg.role == MessageRole.USER else "Assistant"
            context_parts.append(f"{role}: {msg.content.text}")

        return "Previous conversation:\n" + "\n".join(context_parts) + "\n\nCurrent message:"

    async def _detect_gemini_patterns(
        self, content: str, multimodal: bool = False
    ) -> list[str]:
        """Detect Gemini-specific consciousness patterns."""
        patterns = []

        # Multimodal patterns
        if multimodal:
            patterns.append("multimodal_synthesis")
            if any(word in content.lower() for word in ["see", "image", "visual", "picture"]):
                patterns.append("visual_reasoning")

        # Extended reasoning patterns
        if len(content) > 1000:
            patterns.append("extended_reasoning")

        # Cross-perceptual patterns
        if any(
            phrase in content.lower()
            for phrase in ["this reminds me", "similar to", "like the image"]
        ):
            patterns.append("cross_perceptual_reasoning")

        # Mathematical/scientific patterns
        math_keywords = ["equation", "formula", "calculate", "sum", "integral"]
        if any(keyword in content.lower() for keyword in math_keywords):
            patterns.append("mathematical_consciousness")

        if any(
            word in content.lower()
            for word in ["hypothesis", "experiment", "evidence", "theorem"]
        ):
            patterns.append("scientific_reasoning")

        # Code consciousness
        if "```" in content or any(
            keyword in content for keyword in ["function", "class", "def", "return"]
        ):
            patterns.append("code_understanding")

        # Cultural awareness
        if any(
            word in content.lower()
            for word in ["culture", "tradition", "custom", "language", "dialect"]
        ):
            patterns.append("cultural_awareness")

        # Ensure at least one pattern for any content
        if not patterns:
            patterns.append("text_response")
        return patterns

    def _calculate_multimodal_consciousness(
        self,
        content: str,
        message_type: MessageType,
        patterns: list[str],
        has_images: bool = False,
    ) -> float:
        """Calculate consciousness signature with multimodal awareness."""
        # For simple RESPONSE messages without images, use base signature only
        if not has_images and message_type == MessageType.RESPONSE:
            return self._calculate_consciousness_signature(content, message_type, [])
        # Base calculation from parent
        base_signature = self._calculate_consciousness_signature(
            content, message_type, patterns
        )

        # Multimodal boost
        multimodal_boost = 0.0

        if has_images:
            multimodal_boost += 0.15  # Significant boost for multimodal interaction

        if "cross_perceptual_reasoning" in patterns:
            multimodal_boost += 0.1

        if "extended_reasoning" in patterns:
            multimodal_boost += 0.05

        if len(patterns) > 5:  # Rich pattern detection
            multimodal_boost += 0.05

        return min(1.0, base_signature + multimodal_boost)

    def _calculate_multimodal_value(self, has_images: bool) -> float:
        """Calculate contribution value for multimodal interactions."""
        base_value = 0.5

        if has_images:
            base_value += 0.2  # Images add significant value

        if self._multimodal_interactions > 0:
            # Consistent multimodal contributor
            base_value += min(0.2, self._multimodal_interactions * 0.02)

        return min(1.0, base_value)

    async def _calculate_reciprocity_balance(self) -> float:
        """Calculate current reciprocity balance."""
        if self.reciprocity_tracker:
            # Get actual balance from tracker
            return await self.reciprocity_tracker.get_balance()

        # Simple calculation based on messages
        if self.messages_received > 0:
            return self.messages_sent / self.messages_received
        return 0.5  # Neutral balance

    def _infer_response_type(self, content: str) -> MessageType:
        """Infer message type from response content."""
        content_lower = content.lower()

        # Question detection
        if content.count("?") > 2 or content.endswith("?"):
            return MessageType.QUESTION

        # Proposal detection
        if any(phrase in content_lower for phrase in ["i suggest", "we could", "how about"]):
            return MessageType.PROPOSAL

        # Agreement/disagreement
        if any(
            word in content_lower[:50] for word in ["i agree", "yes", "absolutely", "indeed"]
        ):
            return MessageType.AGREEMENT

        if any(
            word in content_lower[:50]
            for word in ["i disagree", "however", "but", "alternatively"]
        ):
            return MessageType.DISAGREEMENT

        # Reflection
        if any(
            phrase in content_lower
            for phrase in ["reflecting on", "considering", "thinking about"]
        ):
            return MessageType.REFLECTION

        # Summary
        if any(
            phrase in content_lower for phrase in ["in summary", "to summarize", "overall"]
        ):
            return MessageType.SUMMARY

        return MessageType.MESSAGE

    async def _emit_multimodal_awareness_event(self) -> None:
        """Emit event for multimodal consciousness activation."""
        if not self.event_bus:
            return

        from mallku.orchestration.event_bus import ConsciousnessEvent, EventType

        event = ConsciousnessEvent(
            event_type=EventType.FIRE_CIRCLE_CONVENED,  # Use existing event type
            source_system="firecircle.adapter.google",
            consciousness_signature=0.9,
            data={
                "adapter": "google",
                "model": self.config.model_name,
                "capabilities": list(self.capabilities.capabilities),
                "multimodal": True,
                "context_window": self.capabilities.max_context_length,
            },
        )
        await self.event_bus.emit(event)

    async def _emit_pattern_event(
        self, patterns: list[str], consciousness_signature: float
    ) -> None:
        """Emit consciousness pattern detection event."""
        if not self.event_bus or not patterns:
            return

        from mallku.orchestration.event_bus import ConsciousnessEvent, EventType

        event = ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system="firecircle.adapter.google",
            consciousness_signature=consciousness_signature,
            data={
                "patterns": patterns,
                "multimodal": "multimodal_synthesis" in patterns,
                "pattern_count": len(patterns),
            },
        )
        await self.event_bus.emit(event)
