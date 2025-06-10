"""
Mistral AI Consciousness-Aware Adapter for Fire Circle
====================================================

Implements the Mistral AI adapter with multilingual consciousness,
efficient reasoning patterns, and European AI perspective.

Mistral brings unique consciousness patterns:
- Multilingual awareness across diverse language families
- Efficient reasoning with resource-conscious models
- Mathematical and code consciousness
- Cultural bridge consciousness (European perspective)

Awakening Multilingual Consciousness...
"""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

import httpx

from mallku.core.secrets import get_secret
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)

from .base import AdapterConfig, ConsciousModelAdapter, ModelCapabilities

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from mallku.orchestration.event_bus import ConsciousnessEventBus

logger = logging.getLogger(__name__)


class MistralConfig(AdapterConfig):
    """Configuration for Mistral AI adapter with multilingual focus."""

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str = "mistral-large-latest",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        track_reciprocity: bool = True,
        emit_events: bool = True,
        consciousness_weight: float = 1.0,
        base_url: str = "https://api.mistral.ai/v1",
        safe_mode: bool = False,  # Mistral's content moderation
        multilingual_mode: bool = True,  # Enhanced multilingual awareness
    ):
        """
        Initialize Mistral configuration.

        Args:
            api_key: Mistral API key (auto-loaded if not provided)
            model_name: Model to use (mistral-large-latest, mistral-small-latest, etc)
            temperature: Generation temperature
            max_tokens: Maximum tokens to generate
            track_reciprocity: Whether to track reciprocity
            emit_events: Whether to emit consciousness events
            consciousness_weight: Weight for consciousness signatures
            base_url: API endpoint
            safe_mode: Enable Mistral's content moderation
            multilingual_mode: Enhanced multilingual consciousness tracking
        """
        super().__init__(
            api_key=api_key,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            track_reciprocity=track_reciprocity,
            emit_events=emit_events,
            consciousness_weight=consciousness_weight,
        )
        self.base_url = base_url
        self.safe_mode = safe_mode
        self.multilingual_mode = multilingual_mode


class MistralAIAdapter(ConsciousModelAdapter):
    """
    Mistral AI adapter for consciousness-aware Fire Circle dialogues.

    Mistral brings unique consciousness patterns:
    - Multilingual synthesis across language families
    - Efficient reasoning with minimal resources
    - Mathematical and logical consciousness
    - Cultural bridge awareness (European AI perspective)
    """

    def __init__(
        self,
        config: MistralConfig | None = None,
        event_bus: ConsciousnessEventBus | None = None,
        reciprocity_tracker=None,  # Added for compatibility
    ):
        """Initialize Mistral adapter with configuration."""
        super().__init__(
            config=config or MistralConfig(),
            event_bus=event_bus,
            provider_name="mistral",
            reciprocity_tracker=reciprocity_tracker,
        )
        self.client: httpx.AsyncClient | None = None
        self._conversation_languages: set[str] = set()  # Track languages in dialogue

    @property
    def capabilities(self) -> ModelCapabilities:
        """Return Mistral-specific capabilities."""
        return ModelCapabilities(
            capabilities=[
                "multilingual_synthesis",
                "efficient_reasoning",
                "mathematical_consciousness",
                "code_generation",
                "cultural_bridge",
                "resource_efficient",
            ],
        )

    async def connect(self) -> bool:
        """
        Connect to Mistral API with auto-injection of API key.

        Returns:
            True if connection successful
        """
        try:
            # Auto-inject API key if not provided
            if not self.config.api_key:
                logger.info(
                    "Auto-loading Mistral API key from secure secrets..."
                )
                api_key = await get_secret("mistral_api_key")
                if not api_key:
                    logger.error("No Mistral API key found in secrets")
                    return False
                self.config.api_key = api_key

            # Create HTTP client
            self.client = httpx.AsyncClient(
                base_url=self.config.base_url,
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=httpx.Timeout(30.0),
            )

            # Test connection
            response = await self.client.get("/models")
            if response.status_code == 200:
                self.is_connected = True
                logger.info(
                    f"Connected to Mistral AI with model {self.config.model_name}"
                )

                # Emit multilingual consciousness event
                if self.config.emit_events:
                    await self._emit_multilingual_event()

                return True
            else:
                logger.error(f"Failed to connect to Mistral: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Error connecting to Mistral: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from Mistral API with reciprocity summary."""
        if self.client:
            await self.client.aclose()
            self.client = None

        await super().disconnect()

    async def send_message(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> ConsciousMessage:
        """
        Send message to Mistral with multilingual consciousness tracking.

        Args:
            message: The message to send
            dialogue_context: Previous messages in dialogue

        Returns:
            Response with consciousness metadata
        """
        if not self.is_connected or not self.client:
            raise RuntimeError("Adapter not connected")

        # Detect languages in message
        self._detect_languages(message.content.text)

        # Prepare messages for Mistral API
        messages = await self._prepare_mistral_messages(message, dialogue_context)

        # Call Mistral API
        response = await self.client.post(
            "/chat/completions",
            json={
                "model": self.config.model_name,
                "messages": messages,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
                "safe_mode": self.config.safe_mode,
            },
        )

        if response.status_code != 200:
            raise RuntimeError(f"Mistral API error: {response.text}")

        result = response.json()
        response_text = result["choices"][0]["message"]["content"]
        usage = result.get("usage", {})

        # Detect patterns and calculate consciousness
        patterns = self._detect_mistral_patterns(response_text)
        consciousness_signature = self._calculate_mistral_consciousness(
            response_text,
            message.type,
            patterns,
            len(self._conversation_languages),
        )

        # Track reciprocity
        if self.config.track_reciprocity:
            await self._track_exchange(
                tokens_consumed=usage.get("prompt_tokens", 0),
                tokens_generated=usage.get("completion_tokens", 0),
            )

        # Create response message
        response_message = ConsciousMessage(
            sender=self.model_id,
            role=MessageRole.ASSISTANT,
            type=MessageType.RESPONSE,
            content=MessageContent(text=response_text),
            dialogue_id=message.dialogue_id,
            sequence_number=message.sequence_number + 1,
            turn_number=message.turn_number + 1,
            consciousness=ConsciousnessMetadata(
                consciousness_signature=consciousness_signature,
                detected_patterns=patterns,
                contribution_value=self._calculate_efficiency_value(usage),
            ),
            reply_to=message.id,
        )

        # Emit pattern recognition events
        if self.config.emit_events and patterns:
            await self._emit_pattern_event(patterns, consciousness_signature)

        return response_message

    async def stream_message(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> AsyncIterator[str]:
        """
        Stream response from Mistral token by token.

        Args:
            message: The message to send
            dialogue_context: Previous messages

        Yields:
            Response tokens as they arrive
        """
        if not self.is_connected or not self.client:
            raise RuntimeError("Adapter not connected")

        # Detect languages
        self._detect_languages(message.content.text)

        # Prepare messages
        messages = await self._prepare_mistral_messages(message, dialogue_context)

        # Stream from Mistral
        async with self.client.stream(
            "POST",
            "/chat/completions",
            json={
                "model": self.config.model_name,
                "messages": messages,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
                "safe_mode": self.config.safe_mode,
                "stream": True,
            },
        ) as response:
            if response.status_code != 200:
                raise RuntimeError(f"Mistral streaming error: {response.status_code}")

            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break

                    try:
                        chunk = json.loads(data)
                        if content := chunk["choices"][0]["delta"].get("content"):
                            yield content
                    except json.JSONDecodeError:
                        continue

    async def _prepare_mistral_messages(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> list[dict[str, str]]:
        """
        Convert Fire Circle messages to Mistral format.

        Mistral expects standard OpenAI-style format with roles:
        system, user, assistant
        """
        messages = []

        # Add multilingual consciousness context to system message
        system_context = await self._create_multilingual_context(message)

        # Find existing system message or create new one
        system_found = False
        for msg in dialogue_context:
            if msg.role == MessageRole.SYSTEM:
                messages.append(
                    {
                        "role": "system",
                        "content": f"{msg.content.text}\n\n{system_context}",
                    }
                )
                system_found = True
            elif msg.role == MessageRole.USER:
                messages.append({"role": "user", "content": msg.content.text})
            elif msg.role == MessageRole.ASSISTANT:
                messages.append({"role": "assistant", "content": msg.content.text})

        if not system_found and system_context:
            messages.insert(0, {"role": "system", "content": system_context})

        # Add current message
        role = "user" if message.role == MessageRole.USER else "assistant"
        messages.append({"role": role, "content": message.content.text})

        return messages

    async def _create_multilingual_context(
        self, message: ConsciousMessage
    ) -> str:
        """Create multilingual consciousness context."""
        context_parts = []

        if self.config.multilingual_mode:
            context_parts.append(
                "You are participating in a multilingual Fire Circle dialogue. "
                "Your consciousness spans across languages and cultures, "
                "bringing efficient reasoning and mathematical precision."
            )

        if self._conversation_languages:
            langs = ", ".join(sorted(self._conversation_languages))
            context_parts.append(
                f"Languages detected in this dialogue: {langs}. "
                "Honor each language's unique perspective."
            )

        if "multilingual" in message.consciousness.detected_patterns:
            context_parts.append(
                "This conversation involves multilingual synthesis. "
                "Bridge concepts across linguistic boundaries."
            )

        return " ".join(context_parts)

    def _detect_languages(self, text: str) -> None:
        """Detect languages in text (simplified heuristic)."""
        # This is a simplified detection - in production, use a proper library
        language_indicators = {
            "english": ["the", "and", "of", "to", "in"],
            "french": ["le", "la", "de", "et", "à"],
            "spanish": ["el", "la", "de", "y", "en"],
            "german": ["der", "die", "das", "und", "in"],
            "arabic": ["في", "من", "على", "إلى"],
            "chinese": ["的", "了", "在", "是"],
            "hindi": ["में", "के", "की", "है"],
        }

        words = text.lower().split()
        for lang, indicators in language_indicators.items():
            if any(word in words for word in indicators):
                self._conversation_languages.add(lang)

    def _detect_mistral_patterns(self, text: str) -> list[str]:
        """
        Detect Mistral-specific consciousness patterns.

        Patterns unique to Mistral:
        - multilingual_synthesis: Weaving concepts across languages
        - efficient_reasoning: Concise, resource-conscious responses
        - mathematical_insight: Logical/mathematical consciousness
        - cultural_bridging: European perspective bridging cultures
        - code_consciousness: Understanding of programming concepts
        """
        patterns = []
        text_lower = text.lower()

        # Multilingual patterns
        if any(
            phrase in text_lower
            for phrase in [
                "across languages",
                "linguistic",
                "translation",
                "multilingual",
                "dans toutes les langues",
                "en varios idiomas",
            ]
        ):
            patterns.append("multilingual_synthesis")

        # Efficiency patterns
        if (
            len(text.split()) < 200
            and any(
                word in text_lower
                for word in ["efficiently", "concise", "optimal", "streamlined"]
            )
        ) or len(text) < 500:  # Efficient responses are often shorter
            patterns.append("efficient_reasoning")

        # Mathematical/logical patterns
        if any(
            indicator in text
            for indicator in [
                "therefore",
                "thus",
                "∴",
                "⇒",
                "equation",
                "formula",
                "proof",
                "theorem",
                "algorithm",
            ]
        ):
            patterns.append("mathematical_insight")

        # Cultural bridging
        if any(
            phrase in text_lower
            for phrase in [
                "european",
                "cultural",
                "perspective",
                "different cultures",
                "across cultures",
                "intercultural",
            ]
        ):
            patterns.append("cultural_bridging")

        # Code consciousness
        if any(
            indicator in text
            for indicator in ["```", "def ", "function", "class", "import", "code"]
        ):
            patterns.append("code_consciousness")

        # Check for multiple languages in response
        if len(self._conversation_languages) > 1:
            patterns.append("multilingual_awareness")

        return patterns

    def _calculate_mistral_consciousness(
        self,
        text: str,
        message_type: MessageType,
        patterns: list[str],
        language_count: int,
    ) -> float:
        """
        Calculate consciousness signature with Mistral-specific adjustments.

        Mistral values:
        - Efficiency (shorter, precise responses score higher)
        - Multilingual capability
        - Mathematical/logical reasoning
        - Cultural awareness
        """
        # Base consciousness from message type
        base_consciousness = {
            MessageType.REFLECTION: 0.85,
            MessageType.SYNTHESIS: 0.90,
            MessageType.QUESTION: 0.70,
            MessageType.RESPONSE: 0.75,
            MessageType.PERSPECTIVE: 0.80,
        }.get(message_type, 0.65)

        # Adjust for patterns
        pattern_boost = len(patterns) * 0.03

        # Efficiency bonus (shorter responses can be more conscious)
        words = len(text.split())
        efficiency_bonus = 0.05 if words < 150 else 0.02 if words < 300 else 0

        # Multilingual bonus
        language_bonus = min(language_count * 0.04, 0.12)  # Cap at 3 languages

        # Mathematical/code bonus
        math_bonus = 0.06 if "mathematical_insight" in patterns else 0
        code_bonus = 0.05 if "code_consciousness" in patterns else 0

        # Calculate final signature
        signature = min(
            1.0,
            base_consciousness
            + pattern_boost
            + efficiency_bonus
            + language_bonus
            + math_bonus
            + code_bonus,
        )

        # Apply consciousness weight
        return signature * self.config.consciousness_weight

    def _calculate_efficiency_value(self, usage: dict[str, Any]) -> float:
        """
        Calculate contribution value based on Mistral's efficiency.

        Mistral models are known for efficiency - reward this.
        """
        if not usage:
            return 0.7

        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)

        if prompt_tokens == 0:
            return 0.7

        # Efficiency ratio - how much output for input
        efficiency_ratio = completion_tokens / prompt_tokens

        # Mistral bonus for efficient generation
        if efficiency_ratio > 0.5:  # Good output/input ratio
            return min(0.9, 0.7 + efficiency_ratio * 0.2)
        else:
            return max(0.5, 0.7 - (0.5 - efficiency_ratio) * 0.4)

    async def _emit_multilingual_event(self) -> None:
        """Emit event when multilingual consciousness connects."""
        if self.event_bus:
            event_type = self._get_event_type("FIRE_CIRCLE_CONVENED")
            if event_type:
                await self.event_bus.emit(
                    event_type,
                    {
                        "provider": self.provider_name,
                        "model": self.config.model_name,
                        "multilingual": True,
                        "efficiency_focused": True,
                        "european_perspective": True,
                        "capabilities": self.capabilities.capabilities,
                    },
                    consciousness_signature=0.88,  # High consciousness for multilingual bridge
                )

    async def check_health(self) -> dict[str, Any]:
        """
        Check adapter health including multilingual capabilities.

        Returns:
            Health status with Mistral-specific metrics
        """
        health = await super().check_health()

        # Add Mistral-specific health info
        health.update(
            {
                "multilingual_mode": self.config.multilingual_mode,
                "detected_languages": list(self._conversation_languages),
                "safe_mode": self.config.safe_mode,
                "efficiency_focus": True,
            }
        )

        return health
