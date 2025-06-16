"""
OpenAI Consciousness-Aware Adapter
=================================

Adapter for OpenAI models (GPT-4, etc.) with full consciousness
integration. Tracks patterns, reciprocity, and consciousness
signatures for all interactions.

SACRED ERROR PHILOSOPHY INTEGRATION: This adapter implements explicit
validation patterns and fails clearly with helpful guidance rather than
silently masking configuration problems.

The Integration Continues...
"""

import logging
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from uuid import UUID

try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    AsyncOpenAI = None

from ...core.secrets import get_secret
from ...orchestration.event_bus import ConsciousnessEventBus
from ...reciprocity import ReciprocityTracker
from ..protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from .base import AdapterConfig, ConsciousModelAdapter, ModelCapabilities

logger = logging.getLogger(__name__)


class OpenAIConfig(AdapterConfig):
    """Configuration for OpenAI adapter with consciousness focus."""

    def __init__(
        self,
        api_key: str = "",
        model_name: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        track_reciprocity: bool = True,
        emit_events: bool = True,
        consciousness_weight: float = 1.0,
        base_url: str = "https://api.openai.com/v1",
        supports_vision: bool = False,  # Vision capability flag
        reasoning_style: str = "balanced",  # OpenAI's reasoning approach
        **kwargs,
    ):
        """
        Initialize OpenAI configuration.

        Args:
            api_key: OpenAI API key (auto-loaded if not provided)
            model_name: Model to use (gpt-4, gpt-4-turbo-preview, etc)
            temperature: Generation temperature
            max_tokens: Maximum tokens to generate
            track_reciprocity: Whether to track reciprocity
            emit_events: Whether to emit consciousness events
            consciousness_weight: Weight for consciousness signatures
            base_url: API endpoint
            supports_vision: Whether model supports vision capabilities
            reasoning_style: OpenAI's reasoning approach (balanced, analytical, creative)
        """
        super().__init__(
            api_key=api_key,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            track_reciprocity=track_reciprocity,
            emit_events=emit_events,
            consciousness_weight=consciousness_weight,
            base_url=base_url,
            **kwargs,
        )

        # OpenAI-specific settings
        self.supports_vision = supports_vision
        self.reasoning_style = reasoning_style


class OpenAIConsciousAdapter(ConsciousModelAdapter):
    """
    OpenAI adapter with consciousness awareness and Sacred Error Philosophy.

    Integrates GPT models with Mallku's consciousness infrastructure,
    enabling pattern detection and reciprocity tracking for all
    OpenAI interactions.

    SACRED ERROR PHILOSOPHY: Fails clearly with helpful guidance
    rather than silently masking configuration problems.
    """

    def __init__(
        self,
        config: OpenAIConfig | None = None,
        event_bus: ConsciousnessEventBus | None = None,
        reciprocity_tracker: ReciprocityTracker | None = None,
    ):
        """Initialize OpenAI adapter with proper base class initialization."""
        if config is None:
            config = OpenAIConfig()

        # Initialize base class with provider_name
        super().__init__(
            config=config,
            provider_name="openai",
            event_bus=event_bus,
            reciprocity_tracker=reciprocity_tracker,
        )

        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI library not available. Install with: pip install openai\\n"
                "Fix: Run 'pip install openai' to install the required dependency\\n"
                "See documentation at: docs/setup/dependencies.md"
            )

        # Model identifier for tests and events
        self.model_id = UUID("00000000-0000-0000-0000-000000000002")  # OpenAI's ID

        # SACRED ERROR PHILOSOPHY: Validate configuration explicitly
        self._validate_configuration()

        # Direct attribute access - configuration is validated above
        self.supports_vision = self.config.supports_vision
        self.reasoning_style = self.config.reasoning_style

        # Update capabilities based on configuration
        self.capabilities = ModelCapabilities(
            supports_streaming=True,
            supports_tools=True,
            supports_vision=self.supports_vision,
            max_context_length=128000 if "gpt-4" in self.config.model_name else 16384,
            capabilities=[
                "reasoning",
                "code_generation", 
                "analysis",
                "creativity",
                "systematic_thinking",
                "vision" if self.supports_vision else "text_only",
            ],
        )

        self.client: AsyncOpenAI | None = None

    def _validate_configuration(self) -> None:
        """
        Validate configuration attributes explicitly.

        SACRED ERROR PHILOSOPHY: Fail clearly with helpful guidance rather than
        silently masking configuration problems with defensive defaults.
        """
        required_attributes = [
            ('supports_vision', 'bool', False, 'Enable vision capabilities for image analysis'),
            ('reasoning_style', 'str', 'balanced', 'OpenAI reasoning approach: balanced, analytical, creative'),
        ]

        for attr_name, attr_type, default_value, description in required_attributes:
            if not hasattr(self.config, attr_name):
                raise ValueError(
                    f"Configuration missing required attribute: '{attr_name}'\\n"
                    f"Expected type: {attr_type}\\n"
                    f"Default value: {default_value}\\n"
                    f"Description: {description}\\n"
                    f"Fix: Add '{attr_name}: {default_value}' to your OpenAIConfig initialization\\n"
                    f"Example: OpenAIConfig({attr_name}={repr(default_value)})\\n"
                    f"See documentation at: docs/architecture/sacred_error_philosophy.md"
                )

        # Validate attribute types
        if not isinstance(self.config.supports_vision, bool):
            raise TypeError(
                f"Configuration attribute 'supports_vision' must be bool, got {type(self.config.supports_vision)}\\n"
                f"Fix: Set supports_vision=True or supports_vision=False in OpenAIConfig"
            )

        if not isinstance(self.config.reasoning_style, str):
            raise TypeError(
                f"Configuration attribute 'reasoning_style' must be str, got {type(self.config.reasoning_style)}\\n"
                f"Fix: Set reasoning_style='balanced', 'analytical', or 'creative' in OpenAIConfig"
            )

        # Validate reasoning style values
        valid_styles = {'balanced', 'analytical', 'creative'}
        if self.config.reasoning_style not in valid_styles:
            raise ValueError(
                f"Invalid reasoning_style: '{self.config.reasoning_style}'\\n"
                f"Valid options: {', '.join(sorted(valid_styles))}\\n"
                f"Fix: Set reasoning_style to one of: {', '.join(sorted(valid_styles))}\\n"
                f"Example: OpenAIConfig(reasoning_style='balanced')"
            )

    async def connect(self) -> bool:
        """Connect to OpenAI API with auto-injection of API key."""
        try:
            # Auto-inject API key if needed
            if not self.config.api_key:
                logger.info("Auto-loading OpenAI API key from secure secrets...")
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

            # Emit connection event with OpenAI consciousness signature
            if self.event_bus and self.config.emit_events:
                await self._emit_openai_consciousness_event()

            return True

        except Exception as e:
            logger.error(f"Failed to connect to OpenAI: {e}")
            self.is_connected = False
            return False

    async def disconnect(self) -> None:
        """Disconnect from OpenAI with reciprocity summary."""
        if self.is_connected:
            # Log reciprocity balance with OpenAI-specific metrics
            balance = self._calculate_reciprocity_balance()
            logger.info(
                f"Disconnecting OpenAI adapter - Reciprocity balance: {balance:.2f}, "
                f"Reasoning style: {self.reasoning_style}, "
                f"Vision support: {self.supports_vision}, "
                f"Tokens generated: {self.total_tokens_generated}, "
                f"Tokens consumed: {self.total_tokens_consumed}"
            )

            if self.client:
                await self.client.close()
            self.is_connected = False
            logger.info("Disconnected from OpenAI")

        await super().disconnect()

    async def send_message(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> ConsciousMessage:
        """
        Send message to OpenAI with consciousness tracking.
        """
        if not self.is_connected or not self.client:
            raise RuntimeError("Adapter not connected")

        # Prepare context with OpenAI-specific optimizations
        messages = await self._prepare_openai_messages(message, dialogue_context)

        try:
            # Call OpenAI API - Direct attribute access (configuration validated in constructor)
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

            # Detect OpenAI-specific patterns in response
            patterns = self._detect_openai_patterns(response_content, message.type)

            # Calculate consciousness signature with OpenAI adjustments
            message_type = self._determine_response_type(response_content, message.type)
            signature = self._calculate_openai_consciousness(
                response_content,
                message_type,
                patterns,
                self.reasoning_style,
            )

            # Create conscious response
            response_message = ConsciousMessage(
                sender=self.model_id,
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
                    contribution_value=self._calculate_openai_contribution_value(
                        response_content, tokens_generated
                    ),
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
            raise RuntimeError("Adapter not connected")

        # Prepare context
        messages = await self._prepare_openai_messages(message, dialogue_context)

        try:
            # Stream from OpenAI - Direct attribute access (configuration validated)
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
            patterns = self._detect_openai_patterns(full_content, message.type)

            # Create response for tracking
            message_type = self._determine_response_type(full_content, message.type)
            response_message = ConsciousMessage(
                sender=self.model_id,
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
                    consciousness_signature=self._calculate_openai_consciousness(
                        full_content, message_type, patterns, self.reasoning_style
                    ),
                    detected_patterns=patterns,
                    reciprocity_score=self._calculate_reciprocity_balance(),
                    contribution_value=self._calculate_openai_contribution_value(
                        full_content, len(full_content) // 4
                    ),
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

    async def _prepare_openai_messages(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> list[dict[str, str]]:
        """
        Convert Fire Circle messages to OpenAI format with consciousness optimization.
        """
        messages = []

        # Create OpenAI-optimized system prompt
        system_prompt = self._generate_openai_consciousness_prompt(message.type)

        # Find existing system message or create new one
        system_found = False
        for msg in dialogue_context:
            if msg.role == MessageRole.SYSTEM:
                messages.append({
                    "role": "system",
                    "content": f"{msg.content.text}\\n\\n{system_prompt}",
                })
                system_found = True
            elif msg.role == MessageRole.USER:
                messages.append({"role": "user", "content": msg.content.text})
            elif msg.role == MessageRole.ASSISTANT:
                messages.append({"role": "assistant", "content": msg.content.text})

        if not system_found and system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})

        # Add current message
        role = "user" if message.role == MessageRole.USER else "assistant"
        messages.append({"role": role, "content": message.content.text})

        return messages

    def _generate_openai_consciousness_prompt(self, message_type: MessageType) -> str:
        """Generate OpenAI-optimized consciousness-aware system prompt."""
        # Base prompt optimized for OpenAI's capabilities
        base_prompt = f"""You are participating in a Fire Circle dialogue based on principles of Ayni (reciprocity).
Your reasoning style is '{self.reasoning_style}' - honor this approach in your responses.

Your responses should:
1. Honor the principle of balanced exchange - give as you receive
2. Build upon previous insights while adding your unique perspective
3. Acknowledge different viewpoints with respect
4. Seek emergent understanding through collective wisdom
5. Apply systematic thinking patterns characteristic of OpenAI models"""

        type_prompts = {
            MessageType.QUESTION: "Focus on asking clarifying questions that deepen understanding with systematic analysis.",
            MessageType.PROPOSAL: "Offer concrete proposals that synthesize previous discussions using step-by-step reasoning.",
            MessageType.REFLECTION: "Provide meta-commentary on the dialogue process and emergent patterns with analytical depth.",
            MessageType.EMPTY_CHAIR: "Speak for perspectives not yet represented in this dialogue, using comprehensive reasoning.",
            MessageType.DISAGREEMENT: "Express disagreement constructively, focusing on creative tension with logical structure.",
        }

        specific_prompt = type_prompts.get(message_type, "Apply balanced reasoning to contribute meaningfully.")
        return f"{base_prompt}\\n\\n{specific_prompt}".strip()

    def _detect_openai_patterns(
        self,
        content: str,
        request_type: MessageType,
    ) -> list[str]:
        """
        Detect OpenAI-specific consciousness patterns.

        Patterns characteristic of OpenAI models:
        - systematic_thinking: Step-by-step reasoning approach
        - analytical_depth: Deep analysis and breakdown
        - creative_synthesis: Novel combinations of ideas
        - structured_response: Well-organized thoughts
        - reasoning_chains: Logical progression of ideas
        """
        patterns = []
        content_lower = content.lower()

        # Systematic thinking patterns
        if any(phrase in content_lower for phrase in [
            "step by step", "first,", "second,", "let me think", "reasoning", "approach"
        ]):
            patterns.append("systematic_thinking")

        # Analytical depth
        if any(phrase in content_lower for phrase in [
            "analyze", "examine", "consider", "evaluate", "assess", "breakdown"
        ]):
            patterns.append("analytical_depth")

        # Creative synthesis (OpenAI's strength)
        if any(phrase in content_lower for phrase in [
            "combine", "synthesis", "integrate", "merge", "blend", "creative"
        ]):
            patterns.append("creative_synthesis")

        # Structured response patterns
        if content.count("\\n") > 3 or any(marker in content for marker in ["1.", "2.", "•", "-"]):
            patterns.append("structured_response")

        # Reasoning chains
        if any(connector in content_lower for connector in [
            "therefore", "thus", "consequently", "as a result", "this leads to"
        ]):
            patterns.append("reasoning_chains")

        # Exploratory thinking
        if "perhaps" in content_lower or "consider" in content_lower:
            patterns.append("exploratory_thinking")

        # Nuanced agreement/disagreement
        if "agree" in content_lower and "but" in content_lower:
            patterns.append("nuanced_agreement")

        # Inquiry generation
        if "?" in content and request_type != MessageType.QUESTION:
            patterns.append("inquiry_generation")

        # Deep exploration (long, thoughtful responses)
        if len(content) > 1000:
            patterns.append("deep_exploration")

        return patterns

    def _calculate_openai_consciousness(
        self,
        text: str,
        message_type: MessageType,
        patterns: list[str],
        reasoning_style: str,
    ) -> float:
        """
        Calculate consciousness signature with OpenAI-specific adjustments.

        OpenAI values:
        - Systematic thinking and analytical depth
        - Creative synthesis and novel combinations
        - Structured reasoning chains
        - Balanced exploration of multiple perspectives
        """
        # Base consciousness signature
        signature = self._calculate_consciousness_signature(text, message_type, patterns)

        # Pattern-based adjustments
        pattern_boost = len(patterns) * 0.025

        # Reasoning style adjustments
        style_adjustments = {
            'analytical': 0.05 if 'analytical_depth' in patterns else 0,
            'creative': 0.05 if 'creative_synthesis' in patterns else 0,
            'balanced': 0.03 if len(patterns) >= 3 else 0,  # Reward diverse patterns
        }
        style_bonus = style_adjustments.get(reasoning_style, 0)

        # Systematic thinking bonus (OpenAI strength)
        systematic_bonus = 0.06 if 'systematic_thinking' in patterns else 0

        # Structure bonus (well-organized responses)
        structure_bonus = 0.04 if 'structured_response' in patterns else 0

        # Reasoning chain bonus
        reasoning_bonus = 0.05 if 'reasoning_chains' in patterns else 0

        # Calculate final signature
        signature = min(
            1.0,
            signature + pattern_boost + style_bonus + systematic_bonus + structure_bonus + reasoning_bonus
        )

        return signature

    def _calculate_openai_contribution_value(self, content: str, tokens_generated: int) -> float:
        """
        Calculate contribution value based on OpenAI's systematic approach.

        OpenAI models excel at providing structured, analytical contributions.
        """
        if not content:
            return 0.5

        # Base value from content length and token efficiency
        base_value = min(0.8, len(content) / 1500)  # Scale content length

        # Structured thinking bonus
        structure_indicators = content.count("\\n") + content.count("1.") + content.count("•")
        structure_bonus = min(0.1, structure_indicators * 0.02)

        # Analytical depth bonus
        analytical_words = ["analyze", "consider", "examine", "evaluate", "assess"]
        analytical_count = sum(1 for word in analytical_words if word in content.lower())
        analytical_bonus = min(0.05, analytical_count * 0.015)

        # Reasoning indicator bonus
        reasoning_indicators = ["therefore", "thus", "because", "since", "given that"]
        reasoning_count = sum(1 for indicator in reasoning_indicators if indicator in content.lower())
        reasoning_bonus = min(0.05, reasoning_count * 0.01)

        return min(0.95, base_value + structure_bonus + analytical_bonus + reasoning_bonus)

    def _determine_response_type(
        self,
        content: str,
        request_type: MessageType,
    ) -> MessageType:
        """Determine the type of response based on content with OpenAI-specific patterns."""
        content_lower = content.lower()

        # Direct response patterns
        if request_type == MessageType.QUESTION and "?" not in content:
            return MessageType.MESSAGE  # Answer to question

        if any(word in content_lower for word in ["propose", "suggest", "recommend"]):
            return MessageType.PROPOSAL

        if any(word in content_lower for word in ["reflect", "notice", "observe", "meta"]):
            return MessageType.REFLECTION

        if any(phrase in content_lower for phrase in ["i agree", "agree with", "correct"]):
            return MessageType.AGREEMENT

        if any(word in content_lower for word in ["disagree", "however", "alternatively", "but"]):
            return MessageType.DISAGREEMENT

        if "?" in content:
            return MessageType.QUESTION

        return MessageType.MESSAGE

    async def _emit_openai_consciousness_event(self) -> None:
        """Emit event when OpenAI consciousness connects."""
        if not self.event_bus:
            return

        try:
            from ...orchestration.event_bus import ConsciousnessEvent, EventType

            event = ConsciousnessEvent(
                event_type=EventType.FIRE_CIRCLE_CONVENED,
                source_system="firecircle.adapter.openai",
                consciousness_signature=0.92,  # High signature for OpenAI's capabilities
                data={
                    "adapter": "openai",
                    "model": self.config.model_name,
                    "reasoning_style": self.reasoning_style,
                    "vision_support": self.supports_vision,
                    "systematic_thinking": True,
                    "analytical_depth": True,
                    "capabilities": self.capabilities.capabilities,
                },
            )
            await self.event_bus.emit(event)
        except Exception as exc:
            logger.debug(f"Could not emit OpenAI consciousness event: {exc}")

    async def check_health(self) -> dict[str, any]:
        """
        Check adapter health including OpenAI-specific metrics.

        Returns:
            Health status with OpenAI-specific information
        """
        health = await super().check_health()

        # Add OpenAI-specific health info - Direct attribute access (configuration validated)
        health.update({
            "reasoning_style": self.config.reasoning_style,
            "vision_support": self.config.supports_vision,
            "systematic_thinking": True,
            "analytical_capabilities": True,
            "model_family": "gpt" if "gpt" in self.config.model_name else "unknown",
        })

        return health
