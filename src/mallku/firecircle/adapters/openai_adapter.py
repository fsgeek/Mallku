"""
OpenAI Consciousness-Aware Adapter
=================================

Adapter for OpenAI models (GPT-4, etc.) with full consciousness
integration. Tracks patterns, reciprocity, and consciousness
signatures for all interactions.

The Integration Continues...
"""

import logging
from collections.abc import AsyncIterator

try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    AsyncOpenAI = None

from ..protocol.conscious_message import (
    ConsciousMessage,
    MessageContent,
    MessageRole,
    MessageType,
)
from .base import ConsciousModelAdapter, ModelCapabilities

logger = logging.getLogger(__name__)


class OpenAIConsciousAdapter(ConsciousModelAdapter):
    """
    OpenAI adapter with consciousness awareness.

    Integrates GPT models with Mallku's consciousness infrastructure,
    enabling pattern detection and reciprocity tracking for all
    OpenAI interactions.
    """

    def __init__(self, *args, **kwargs):
        """Initialize OpenAI adapter."""
        super().__init__(*args, **kwargs)

        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library not available. Install with: pip install openai")

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

    async def connect(self) -> bool:
        """Connect to OpenAI API."""
        try:
            self.client = AsyncOpenAI(api_key=self.config.api_key)

            # Test connection
            await self.client.models.retrieve(self.config.model_name)

            self.is_connected = True
            logger.info(f"Connected to OpenAI with model {self.config.model_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to OpenAI: {e}")
            self.is_connected = False
            return False

    async def disconnect(self) -> None:
        """Disconnect from OpenAI."""
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

            # Create conscious response
            response_message = ConsciousMessage(
                type=self._determine_response_type(response_content, message.type),
                role=MessageRole.ASSISTANT,
                sender=self.adapter_id,
                content=MessageContent(text=response_content),
                dialogue_id=message.dialogue_id,
                sequence_number=message.sequence_number + 1,
                turn_number=message.turn_number,
                in_response_to=message.id,
            )

            # Update consciousness metadata
            response_message.consciousness.correlation_id = message.consciousness.correlation_id
            response_message.consciousness.detected_patterns = patterns

            # Calculate consciousness signature
            signature = self._calculate_consciousness_signature(
                response_content,
                response_message.type,
                patterns,
            )
            response_message.update_consciousness_signature(signature)

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
            self._detect_response_patterns(full_content, message.type)

            # Create response for tracking
            response_message = ConsciousMessage(
                type=self._determine_response_type(full_content, message.type),
                role=MessageRole.ASSISTANT,
                sender=self.adapter_id,
                content=MessageContent(text=full_content),
                dialogue_id=message.dialogue_id,
                sequence_number=message.sequence_number + 1,
                turn_number=message.turn_number,
                in_response_to=message.id,
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
