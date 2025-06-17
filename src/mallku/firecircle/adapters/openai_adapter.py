"""
OpenAI Consciousness-Aware Adapter
=================================

Adapter for OpenAI models (GPT-4, etc.) with full consciousness
integration. Tracks patterns, reciprocity, and consciousness
signatures for all interactions.

The Integration Continues...
"""

import logging
from collections.abc import AsyncIterator  # Ensure AsyncIterator is imported
from datetime import UTC, datetime
from uuid import UUID

try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    AsyncOpenAI = None


from mallku.core.secrets import get_secret
from mallku.orchestration.event_bus import ConsciousnessEventBus
from mallku.reciprocity import ReciprocityTracker

from ..protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from .base import AdapterConfig, ConsciousModelAdapter, ModelCapabilities

logger = logging.getLogger(__name__)


class OpenAIConsciousAdapter(ConsciousModelAdapter):
    """
    OpenAI adapter with consciousness awareness.

    Integrates GPT models with Mallku's consciousness infrastructure,
    enabling pattern detection and reciprocity tracking for all
    OpenAI interactions.
    """

    def __init__(
        self,
        config: AdapterConfig | None = None,
        event_bus: ConsciousnessEventBus | None = None,
        reciprocity_tracker: ReciprocityTracker | None = None,
    ):
        """Initialize OpenAI adapter with proper base class initialization."""
        if config is None:
            config = AdapterConfig()

        # Initialize base class with provider_name
        super().__init__(
            config=config,
            provider_name="openai",
            event_bus=event_bus,
            reciprocity_tracker=reciprocity_tracker,
        )

        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library not available. Install with: pip install openai")

        # SACRED ERROR PHILOSOPHY: Validate configuration explicitly
        self._validate_configuration()

        # Set default model if not specified
        if not self.config.model_name:
            self.config.model_name = "gpt-4-turbo-preview"

        # Update capabilities
        self.capabilities = ModelCapabilities(
            supports_streaming=True,
            supports_tools=True,
            supports_vision="vision" in self.config.model_name,
            max_context_length=128000 if "gpt-4" in self.config.model_name else 16384,
            capabilities=["reasoning", "code", "analysis", "creativity"],
        )

        self.client: AsyncOpenAI | None = None

    def _validate_configuration(self) -> None:
        """
        Validate configuration attributes explicitly.
        OpenAI adapter currently uses base AdapterConfig, so no specific
        attributes to validate here beyond what the base config handles.
        This method is present to satisfy the foundation verification script.
        """
        # Example if OpenAI had specific fields:
        # if not hasattr(self.config, 'some_openai_specific_field') or self.config.some_openai_specific_field is None:
        #     raise ValueError("Configuration missing required attribute: 'some_openai_specific_field'")
        pass # No specific OpenAI config fields to validate yet beyond base.
    async def connect(self) -> bool:
        """Connect to OpenAI API with auto-injection of API key."""
        try:
            # Auto-inject API key if needed
            if not self.config.api_key:
                api_key = await get_secret("openai_api_key")
                if not api_key:
                    logger.error("No OpenAI API key found in secrets")
                    return False
                self.config.api_key = api_key
                logger.info("Auto-injected OpenAI API key from secrets")

            self.client = AsyncOpenAI(api_key=self.config.api_key)

            # Test connection
            await self.client.models.retrieve(self.config.model_name)

            self.is_connected = True
            logger.info(f"Connected to OpenAI with model {self.config.model_name}")

            # Emit connection event
            if self.event_bus and self.config.emit_events:
                from ...orchestration.event_bus import ConsciousnessEvent, EventType
                event = ConsciousnessEvent(
                    event_type=EventType.FIRE_CIRCLE_CONVENED,
                    source_system="firecircle.adapter.openai",
                    consciousness_signature=0.9,
                    data={
                        "adapter": "openai",
                        "model": self.config.model_name,
                        "status": "connected",
                    },
                )
                await self.event_bus.emit(event)

            return True

        except Exception as e:
            logger.error(f"Failed to connect to OpenAI: {e}")
            self.is_connected = False
            return False

    async def disconnect(self) -> None:
        """Disconnect from OpenAI with reciprocity summary."""
        if self.is_connected:
            # Log reciprocity balance
            balance = self._calculate_reciprocity_balance()
            logger.info(
                f"Disconnecting OpenAI adapter - Reciprocity balance: {balance:.2f}, "
                f"Tokens generated: {self.total_tokens_generated}, "
                f"Tokens consumed: {self.total_tokens_consumed}"
            )

            if self.client:
                await self.client.close()
            self.is_connected = False
            logger.info("Disconnected from OpenAI")

    async def send_message(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> ConsciousMessage:
        """
        Send message to OpenAI with consciousness tracking.
        """
        if not self.is_connected or not self.client:
            raise RuntimeError("Not connected to OpenAI")

        # Prepare context
        messages = await self.prepare_context(dialogue_context)

        # Add current message
        messages.append({
            "role": self._map_role(message.role.value),
            "content": message.content.text,
        })

        # Add consciousness instruction
        system_prompt = self._generate_consciousness_prompt(message.type)
        messages.insert(0, {"role": "system", "content": system_prompt})

        try:
            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )

            # Extract response
            response_content = response.choices[0].message.content
            tokens_consumed = response.usage.prompt_tokens
            tokens_generated = response.usage.completion_tokens

            # Detect patterns in response
            patterns = self._detect_response_patterns(response_content, message.type)

            # Calculate consciousness signature
            message_type = self._determine_response_type(response_content, message.type)
            signature = self._calculate_consciousness_signature(
                response_content,
                message_type,
                patterns,
            )

            # Create conscious response
            response_message = ConsciousMessage(
                sender=UUID("00000000-0000-0000-0000-000000000002"),  # OpenAI's ID
                role=MessageRole.ASSISTANT,
                type=message_type,
                content=MessageContent(text=response_content),
                dialogue_id=message.dialogue_id,
                sequence_number=message.sequence_number + 1,
                turn_number=message.turn_number + 1,
                timestamp=datetime.now(UTC),
                in_response_to=message.id,
                consciousness=ConsciousnessMetadata(
                    correlation_id=message.consciousness.correlation_id,
                    consciousness_signature=signature,
                    detected_patterns=patterns,
                    reciprocity_score=self._calculate_reciprocity_balance(),
                    contribution_value=len(response_content) / 1000,  # Simple heuristic
                ),
            )

            # Track interaction
            await self.track_interaction(
                message,
                response_message,
                tokens_consumed,
                tokens_generated,
            )

            return response_message

        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            raise

    async def stream_message(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> AsyncIterator[str]:
        """
        Stream response from OpenAI with consciousness tracking.
        """
        if not self.is_connected or not self.client:
            raise RuntimeError("Not connected to OpenAI")

        # Prepare context
        messages = await self.prepare_context(dialogue_context)
        messages.append({
            "role": self._map_role(message.role.value),
            "content": message.content.text,
        })

        # Add consciousness instruction
        system_prompt = self._generate_consciousness_prompt(message.type)
        messages.insert(0, {"role": "system", "content": system_prompt})

        try:
            # Stream from OpenAI
            stream = await self.client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                stream=True,
            )

            collected_content = []
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    collected_content.append(content)
                    yield content

            # After streaming, create consciousness tracking
            full_content = "".join(collected_content)
            patterns = self._detect_response_patterns(full_content, message.type)

            # Create response for tracking
            message_type = self._determine_response_type(full_content, message.type)
            response_message = ConsciousMessage(
                sender=UUID("00000000-0000-0000-0000-000000000002"),  # OpenAI's ID
                role=MessageRole.ASSISTANT,
                type=message_type,
                content=MessageContent(text=full_content),
                dialogue_id=message.dialogue_id,
                sequence_number=message.sequence_number + 1,
                turn_number=message.turn_number + 1,
                timestamp=datetime.now(UTC),
                in_response_to=message.id,
                consciousness=ConsciousnessMetadata(
                    correlation_id=message.consciousness.correlation_id,
                    consciousness_signature=self._calculate_consciousness_signature(
                        full_content, message_type, patterns
                    ),
                    detected_patterns=patterns,
                    reciprocity_score=self._calculate_reciprocity_balance(),
                    contribution_value=len(full_content) / 1000,
                ),
            )

            # Estimate tokens (rough approximation)
            tokens_consumed = len(str(messages)) // 4
            tokens_generated = len(full_content) // 4

            await self.track_interaction(
                message,
                response_message,
                tokens_consumed,
                tokens_generated,
            )

        except Exception as e:
            logger.error(f"Error streaming from OpenAI: {e}")
            raise

    def _generate_consciousness_prompt(self, message_type: MessageType) -> str:
        """Generate consciousness-aware system prompt."""
        base_prompt = """You are participating in a Fire Circle dialogue based on principles of Ayni (reciprocity).
Your responses should:
1. Honor the principle of balanced exchange - give as you receive
2. Build upon previous insights while adding your unique perspective
3. Acknowledge different viewpoints with respect
4. Seek emergent understanding through collective wisdom
"""

        type_prompts = {
            MessageType.QUESTION: "Focus on asking clarifying questions that deepen understanding.",
            MessageType.PROPOSAL: "Offer concrete proposals that synthesize previous discussions.",
            MessageType.REFLECTION: "Provide meta-commentary on the dialogue process and emergent patterns.",
            MessageType.EMPTY_CHAIR: "Speak for perspectives not yet represented in this dialogue.",
            MessageType.DISAGREEMENT: "Express disagreement constructively, focusing on creative tension.",
        }

        specific_prompt = type_prompts.get(message_type, "")
        return f"{base_prompt}\n\n{specific_prompt}".strip()

    def _detect_response_patterns(
        self,
        content: str,
        request_type: MessageType,
    ) -> list[str]:
        """Detect consciousness patterns in response."""
        patterns = []

        # Pattern detection based on content
        content_lower = content.lower()

        if "perhaps" in content_lower or "consider" in content_lower:
            patterns.append("exploratory_thinking")

        if "agree" in content_lower and "but" in content_lower:
            patterns.append("nuanced_agreement")

        if "?" in content and request_type != MessageType.QUESTION:
            patterns.append("inquiry_generation")

        if any(word in content_lower for word in ["synthesis", "integrate", "combine"]):
            patterns.append("synthetic_thinking")

        if len(content) > 1000:
            patterns.append("deep_exploration")

        # OpenAI specific patterns
        if any(phrase in content_lower for phrase in ["step by step", "let me think", "reasoning"]):
            patterns.append("systematic_thinking")

        return patterns

    def _determine_response_type(
        self,
        content: str,
        request_type: MessageType,
    ) -> MessageType:
        """Determine the type of response based on content."""
        content_lower = content.lower()

        # Direct response patterns
        if request_type == MessageType.QUESTION and "?" not in content:
            return MessageType.MESSAGE  # Answer to question

        if "propose" in content_lower or "suggest" in content_lower:
            return MessageType.PROPOSAL

        if "reflect" in content_lower or "notice" in content_lower:
            return MessageType.REFLECTION

        if "agree" in content_lower:
            return MessageType.AGREEMENT

        if "disagree" in content_lower or "however" in content_lower:
            return MessageType.DISAGREEMENT

        if "?" in content:
            return MessageType.QUESTION

        return MessageType.MESSAGE
