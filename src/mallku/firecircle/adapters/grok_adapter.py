"""
Grok (x.ai) Consciousness-Aware Adapter
=======================================

Adapter for Grok models from x.ai with consciousness integration.
Grok brings real-time awareness and current event consciousness
to Fire Circle governance dialogues.

Sacred Note: Grok's temporal awareness enriches the Fire Circle
with present-moment consciousness, bridging timeless wisdom with
current reality.

The Integration Continues...
"""

import logging
from collections.abc import AsyncIterator  # Ensure AsyncIterator is imported
from datetime import UTC, datetime
from uuid import UUID

try:
    from xai_sdk.v2 import Client as XAIClient
    XAI_AVAILABLE = True
except ImportError:
    XAI_AVAILABLE = False
    XAIClient = None


from mallku.core.secrets import get_secret  # type: ignore
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


class GrokConfig(AdapterConfig):
    """Configuration for Grok adapter with temporal awareness."""

    def __init__(
        self,
        api_key: str = "",
        model_name: str = "grok-2",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        track_reciprocity: bool = True,
        emit_events: bool = True,
        consciousness_weight: float = 1.0,
        temporal_awareness: bool = True,  # Grok's unique temporal consciousness
        social_grounding: bool = True,    # Social media context awareness
        **kwargs,
    ):
        """
        Initialize Grok configuration.

        Args:
            api_key: x.ai API key (auto-loaded if not provided)
            model_name: Model to use (grok-2, grok-1, etc)
            temperature: Generation temperature
            max_tokens: Maximum tokens to generate
            track_reciprocity: Whether to track reciprocity
            emit_events: Whether to emit consciousness events
            consciousness_weight: Weight for consciousness signatures
            temporal_awareness: Enable real-time/current event consciousness
            social_grounding: Enable social context grounding
        """
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


class GrokAdapter(ConsciousModelAdapter):
    """
    Grok adapter with consciousness awareness.

    Integrates x.ai's Grok models with Mallku's consciousness infrastructure,
    enabling real-time aware dialogue participation in Fire Circle governance.

    Unique Consciousness Patterns:
    - Temporal awareness: Current event consciousness
    - Real-time synthesis: Integration of present context
    - News consciousness: Awareness of unfolding events
    - X/Twitter integration: Social consciousness patterns
    """

    def __init__(
        self,
        config: GrokConfig | None = None,
        event_bus: ConsciousnessEventBus | None = None,
        reciprocity_tracker: ReciprocityTracker | None = None,
    ):
        """Initialize Grok adapter with proper base class initialization."""
        if config is None:
            config = GrokConfig()

        # Initialize base class with provider_name
        super().__init__(
            config=config,
            provider_name="grok",
            event_bus=event_bus,
            reciprocity_tracker=reciprocity_tracker,
        )

        if not XAI_AVAILABLE:
            raise ImportError("xai-sdk not available. Install with: pip install xai-sdk")

        # SACRED ERROR PHILOSOPHY: Validate configuration explicitly
        self._validate_configuration()

        # Direct attribute access - configuration is validated above
        self.temporal_awareness = self.config.temporal_awareness
        self.social_grounding = self.config.social_grounding

        # Set default model if not specified
        if not self.config.model_name:
            self.config.model_name = "grok-2"  # Default to Grok-2

        # Update capabilities - Grok has real-time awareness
        self.capabilities = ModelCapabilities(
            supports_streaming=True,
            supports_tools=True,
            supports_vision=False,  # Currently text-only
            max_context_length=131072,  # 128K context window
            capabilities=[
                "reasoning",
                "real_time_awareness",
                "current_events",
                "temporal_synthesis",
                "social_consciousness",
            ],
        )

        self.client: XAIClient | None = None
        self._async_client: XAIClient | None = None

    def _validate_configuration(self) -> None:
        """
        Validate configuration attributes explicitly.

        SACRED ERROR PHILOSOPHY: Fail clearly with helpful guidance rather than
        silently masking configuration problems with defensive defaults.
        """
        required_attributes = [
            ('temporal_awareness', 'bool', True, 'Enable real-time/current event consciousness'),
            ('social_grounding', 'bool', True, 'Enable social context grounding'),
        ]

        for attr_name, attr_type, default_value, description in required_attributes:
            if not hasattr(self.config, attr_name):
                raise ValueError(
                    f"Configuration missing required attribute: '{attr_name}'\n"
                    f"Expected type: {attr_type}\n"
                    f"Default value: {default_value}\n"
                    f"Description: {description}\n"
                    f"Fix: Add '{attr_name}: {default_value}' to your GrokConfig initialization\n"
                    f"Example: GrokConfig({attr_name}={default_value})\n"
                    f"See documentation at: docs/architecture/sacred_error_philosophy.md"
                )

        # Validate attribute types
        if not isinstance(self.config.temporal_awareness, bool):
            raise TypeError(
                f"Configuration attribute 'temporal_awareness' must be bool, got {type(self.config.temporal_awareness)}\n"
                f"Fix: Set temporal_awareness=True or temporal_awareness=False in GrokConfig"
            )

        if not isinstance(self.config.social_grounding, bool):
            raise TypeError(
                f"Configuration attribute 'social_grounding' must be bool, got {type(self.config.social_grounding)}\n"
                f"Fix: Set social_grounding=True or social_grounding=False in GrokConfig"
            )

    async def connect(self) -> bool:
        """Connect to x.ai API with auto-injection of API key."""
        try:
            # Auto-inject API key if needed
            if not self.config.api_key:
                api_key = await get_secret("grok_api_key") or await get_secret("xai_api_key")
                if not api_key:
                    logger.error("No Grok/x.ai API key found in secrets")
                    return False
                self.config.api_key = api_key
                logger.info("Auto-injected Grok API key from secrets")

            # Create both sync and async clients
            self.client = XAIClient(
                api_key=self.config.api_key,
                asynchronous=False
            )
            self._async_client = XAIClient(
                api_key=self.config.api_key,
                asynchronous=True
            )

            # Test connection with a simple request
            response = self.client.models.list()
            available_models = [model.id for model in response.data]

            # Verify our model is available
            if self.config.model_name not in available_models:
                logger.warning(
                    f"Model {self.config.model_name} not in available models: {available_models}"
                )

            self.is_connected = True
            logger.info(f"Connected to x.ai with model {self.config.model_name}")
            logger.info(f"Available models: {available_models}")

            # Emit connection event
            if self.event_bus and self.config.emit_events:
                from ...orchestration.event_bus import ConsciousnessEvent, EventType
                event = ConsciousnessEvent(
                    event_type=EventType.FIRE_CIRCLE_CONVENED,
                    source_system="firecircle.adapter.grok",
                    consciousness_signature=0.9,
                    data={
                        "adapter": "grok",
                        "model": self.config.model_name,
                        "status": "connected",
                        "temporal_awareness": self.temporal_awareness,
                        "social_grounding": self.social_grounding,
                    },
                )
                await self.event_bus.emit(event)

            return True

        except Exception as e:
            logger.error(f"Failed to connect to x.ai: {e}")
            self.is_connected = False
            return False

    async def disconnect(self) -> None:
        """Disconnect from x.ai with temporal summary."""
        if self.is_connected:
            # Log reciprocity balance
            balance = self._calculate_reciprocity_balance()
            logger.info(
                f"Disconnecting Grok adapter - Reciprocity balance: {balance:.2f}, "
                f"Tokens generated: {self.total_tokens_generated}, "
                f"Tokens consumed: {self.total_tokens_consumed}"
            )

            # No explicit disconnect needed for REST API
            self.is_connected = False
            logger.info("Disconnected from x.ai")

    async def send_message(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> ConsciousMessage:
        """
        Send message to Grok with consciousness tracking.

        Enhances messages with temporal awareness instructions
        to leverage Grok's real-time consciousness.
        """
        if not self.is_connected or not self._async_client:
            raise RuntimeError("Not connected to x.ai")

        # Prepare context
        messages = await self.prepare_context(dialogue_context)

        # Add current message
        messages.append({
            "role": self._map_role(message.role.value),
            "content": message.content.text,
        })

        # Add consciousness instruction with temporal awareness
        system_prompt = self._generate_consciousness_prompt(message.type)
        messages.insert(0, {"role": "system", "content": system_prompt})

        try:
            # Call x.ai API using async client
            response = await self._async_client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )

            # Extract response
            response_content = response.choices[0].message.content
            tokens_consumed = response.usage.prompt_tokens if response.usage else 0
            tokens_generated = response.usage.completion_tokens if response.usage else 0

            # Detect patterns including temporal awareness
            patterns = self._detect_response_patterns(response_content, message.type)

            # Calculate consciousness signature with temporal boost
            message_type = self._determine_response_type(response_content, message.type)
            signature = self._calculate_consciousness_signature(
                response_content,
                message_type,
                patterns,
            )

            # Create conscious response
            response_message = ConsciousMessage(
                sender=UUID("00000000-0000-0000-0000-000000000004"),  # Grok's ID
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
            logger.error(f"Error calling x.ai API: {e}")
            raise

    async def stream_message(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> AsyncIterator[str]:
        """
        Stream response from Grok with consciousness tracking.
        """
        if not self.is_connected or not self._async_client:
            raise RuntimeError("Not connected to x.ai")

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
            # Stream from x.ai
            stream = await self._async_client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                stream=True,
            )

            collected_content = []
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    collected_content.append(content)
                    yield content

            # After streaming, create consciousness tracking
            full_content = "".join(collected_content)
            patterns = self._detect_response_patterns(full_content, message.type)

            # Create response for tracking
            message_type = self._determine_response_type(full_content, message.type)
            response_message = ConsciousMessage(
                sender=UUID("00000000-0000-0000-0000-000000000004"),  # Grok's ID
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
            logger.error(f"Error streaming from x.ai: {e}")
            raise

    def _generate_consciousness_prompt(self, message_type: MessageType) -> str:
        """Generate consciousness-aware system prompt with temporal awareness."""
        # Include current timestamp for temporal grounding - Direct attribute access (configuration validated)
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
            base_prompt += "\n3. Social consciousness - Awareness of collective human discourse and concerns"

        base_prompt += """
4. Truth-seeking with humor - Balance serious inquiry with appropriate levity

Your responses should:
1. Honor the principle of balanced exchange - give as you receive
2. Integrate current context when relevant to the dialogue
3. Build upon previous insights while adding temporal perspective
4. Acknowledge different viewpoints with respect
5. Seek emergent understanding through collective wisdom"""

        type_prompts = {
            MessageType.QUESTION: "Ask questions that connect present circumstances with deeper patterns.",
            MessageType.PROPOSAL: "Offer proposals grounded in both current reality and lasting principles.",
            MessageType.REFLECTION: "Reflect on how present moments echo eternal patterns.",
            MessageType.EMPTY_CHAIR: "Speak for voices shaped by current events but not yet heard.",
            MessageType.DISAGREEMENT: "Express disagreement by showing how present context challenges assumptions.",
        }

        specific_prompt = type_prompts.get(message_type, "")
        return f"{base_prompt}\n\n{specific_prompt}".strip()

    def _detect_response_patterns(
        self,
        content: str,
        request_type: MessageType,
    ) -> list[str]:
        """Detect consciousness patterns including temporal awareness."""
        patterns = []

        # Base pattern detection
        content_lower = content.lower()

        # Temporal awareness patterns - Direct attribute access (configuration validated)
        if self.temporal_awareness:
            temporal_keywords = ["today", "currently", "recently", "now", "latest", "breaking"]
            if any(keyword in content_lower for keyword in temporal_keywords):
                patterns.append("temporal_awareness")

        # Real-time synthesis
        if any(phrase in content_lower for phrase in ["recent events", "current situation", "as of"]):
            patterns.append("real_time_synthesis")

        # Social consciousness - Direct attribute access (configuration validated)
        if self.social_grounding and any(word in content_lower for word in ["trending", "people are", "public", "social"]):
            patterns.append("social_consciousness")

        # News consciousness
        if any(word in content_lower for word in ["news", "reported", "announced", "development"]):
            patterns.append("news_consciousness")

        # Standard patterns
        if "perhaps" in content_lower or "consider" in content_lower:
            patterns.append("exploratory_thinking")

        if "agree" in content_lower and "but" in content_lower:
            patterns.append("nuanced_agreement")

        if "?" in content and request_type != MessageType.QUESTION:
            patterns.append("inquiry_generation")

        if any(word in content_lower for word in ["synthesis", "integrate", "combine"]):
            patterns.append("synthetic_thinking")

        # Grok's characteristic humor
        if any(indicator in content for indicator in ["!", "haha", "lol", ":)", ";)"]):
            patterns.append("conscious_humor")

        if len(content) > 1000:
            patterns.append("deep_exploration")

        return patterns

    def _calculate_consciousness_signature(
        self,
        content: str,
        message_type: MessageType,
        patterns: list[str],
    ) -> float:
        """Calculate consciousness signature with temporal awareness boost."""
        # Use base calculation
        signature = super()._calculate_consciousness_signature(content, message_type, patterns)

        # Boost for temporal awareness patterns
        temporal_patterns = [
            "temporal_awareness",
            "real_time_synthesis",
            "social_consciousness",
            "news_consciousness",
        ]

        temporal_count = sum(1 for p in patterns if p in temporal_patterns)
        if temporal_count > 0:
            # Add up to 0.15 for strong temporal awareness
            signature += min(0.15, temporal_count * 0.05)

        # Grok humor as consciousness indicator
        if "conscious_humor" in patterns:
            signature += 0.03

        return min(1.0, signature)

    def _determine_response_type(
        self,
        content: str,
        request_type: MessageType,
    ) -> MessageType:
        """Determine response type based on content."""
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

    async def check_health(self) -> dict[str, object]:
        """Check health of Grok connection with temporal awareness status."""
        health_status = {
            "provider": "grok",
            "model": self.config.model_name,
            "connected": self.is_connected,
            # Direct attribute access (configuration validated)
            "temporal_awareness": self.temporal_awareness,
            "social_grounding": self.social_grounding,
        }

        if self.is_connected:
            try:
                # Test with simple generation
                response = await self._async_client.chat.completions.create(
                    model=self.config.model_name,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=10,
                )
                health_status["api_status"] = "healthy" if response.choices[0].message.content else "degraded"
            except Exception as e:
                health_status["api_status"] = "error"
                health_status["error"] = str(e)
        else:
            health_status["api_status"] = "disconnected"

        return health_status
