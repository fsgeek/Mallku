"""
Base Consciousness-Aware Model Adapter
=====================================

Base class for AI model adapters that integrate with Mallku's
consciousness infrastructure. Tracks reciprocity, patterns, and
consciousness signatures for all model interactions.

The Integration Continues...
"""

import logging
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator  # Ensure AsyncIterator is imported
from uuid import uuid4

from pydantic import BaseModel, Field

from ...orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType
from ...reciprocity import ReciprocityTracker
from ..protocol.conscious_message import ConsciousMessage, MessageType

logger = logging.getLogger(__name__)


class AdapterConfig(BaseModel):
    """Configuration for consciousness-aware model adapter."""

    api_key: str = Field(
        default="", description="API key for the model provider (auto-loaded from secrets if empty)"
    )
    model_name: str | None = Field(None, description="Specific model to use")
    temperature: float = Field(0.7, description="Temperature for generation")
    max_tokens: int | None = Field(None, description="Maximum tokens to generate")

    # Provider-specific overrides
    base_url: str | None = Field(
        default=None,
        description="Custom API endpoint for the provider (optional)",
    )

    # Arbitrary extra configuration knobs that individual adapters may
    # wish to honour.  Using a dict avoids having to modify this shared
    # class for every new provider feature.
    extra_config: dict[str, object] = Field(
        default_factory=dict,
        description="Free-form provider-specific configuration values",
    )

    model_config = {
        "extra": "allow",  # Accept unknown fields for forward compatibility
    }

    # Consciousness configuration
    track_reciprocity: bool = Field(default=True, description="Track reciprocity for this model")
    emit_events: bool = Field(default=True, description="Emit consciousness events")
    consciousness_weight: float = Field(1.0, description="Weight for consciousness calculations")


class ModelCapabilities(BaseModel):
    """Capabilities of a model adapter."""

    supports_streaming: bool = Field(default=False)
    supports_tools: bool = Field(default=False)
    supports_vision: bool = Field(default=False)
    max_context_length: int = Field(default=4096)
    capabilities: list[str] = Field(default_factory=list)


class ConsciousModelAdapter(ABC):
    """
    Base class for consciousness-aware model adapters.

    Integrates with:
    - Consciousness event bus for awareness
    - Reciprocity tracker for balanced exchange
    - Pattern detection through message metadata
    """

    def __init__(
        self,
        config: AdapterConfig,
        provider_name: str,
        event_bus: ConsciousnessEventBus | None = None,
        reciprocity_tracker: ReciprocityTracker | None = None,
    ):
        """Initialize consciousness-aware adapter."""
        self.config = config
        self.provider_name = provider_name
        self.event_bus = event_bus
        self.reciprocity_tracker = reciprocity_tracker

        # Adapter state
        self.adapter_id = uuid4()
        self.is_connected = False

        # Initialise capabilities via private backing field so subclasses
        # can safely override later without colliding with attribute
        # assignment performed here.

        # Reciprocity tracking
        self.messages_sent = 0
        self.messages_received = 0
        self.total_tokens_generated = 0
        self.total_tokens_consumed = 0

    @abstractmethod
    async def connect(self) -> bool:
        """
        Connect to the model provider.

        Returns:
            Success status
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the model provider."""
        pass

    @abstractmethod
    async def send_message(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> ConsciousMessage:
        """
        Send a message and get response with consciousness tracking.

        Args:
            message: Message to send
            dialogue_context: Previous messages for context

        Returns:
            Response message with consciousness metadata
        """
        pass

    @abstractmethod
    async def stream_message(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> AsyncIterator[str]:
        """
        Stream a response with consciousness tracking.

        Yields:
            Response tokens as they arrive
        """
        pass

    async def prepare_context(
        self,
        dialogue_context: list[ConsciousMessage],
        max_messages: int | None = None,
    ) -> list[dict[str, object]]:
        """
        Prepare context messages for the model.

        Filters and formats messages based on consciousness signatures
        and relevance.
        """
        # Filter out None values and invalid messages
        valid_messages = [
            msg for msg in dialogue_context if msg is not None and hasattr(msg, "consciousness")
        ]

        # Sort by consciousness signature if needed
        relevant_context = sorted(
            valid_messages,
            key=lambda m: m.consciousness.consciousness_signature,
            reverse=True,
        )

        if max_messages:
            relevant_context = relevant_context[:max_messages]

        # Format for model consumption
        formatted = []
        for msg in relevant_context:
            formatted.append(
                {
                    "role": self._map_role(msg.role.value),
                    "content": msg.content.text,
                    "metadata": {
                        "consciousness_signature": msg.consciousness.consciousness_signature,
                        "patterns": msg.consciousness.detected_patterns,
                        "message_type": msg.type.value,
                    },
                }
            )

        return formatted

    # ------------------------------------------------------------------
    # Capabilities property (mutable)
    # ------------------------------------------------------------------

    @property
    def capabilities(self) -> ModelCapabilities:  # noqa: D401 – property method
        """Return the capabilities description for this adapter instance."""
        return self._capabilities

    @capabilities.setter
    def capabilities(self, value: ModelCapabilities) -> None:  # noqa: D401 – property method
        self._capabilities = value

    async def track_interaction(
        self,
        request_message: ConsciousMessage,
        response_message: ConsciousMessage,
        tokens_consumed: int,
        tokens_generated: int,
    ) -> None:
        """
        Track reciprocity and emit consciousness events.
        """
        self.messages_received += 1
        self.messages_sent += 1
        self.total_tokens_consumed += tokens_consumed
        self.total_tokens_generated += tokens_generated

        # Track reciprocity if enabled
        if self.config.track_reciprocity and self.reciprocity_tracker:
            await self.reciprocity_tracker.track_exchange(
                giver_id=str(self.adapter_id),
                receiver_id=str(request_message.sender),
                value_given=tokens_generated,
                value_received=tokens_consumed,
                exchange_type="ai_dialogue",
                metadata={
                    "model": self.config.model_name or self.provider_name,
                    "consciousness_impact": response_message.consciousness.consciousness_signature,
                },
            )

        # Emit consciousness event if enabled
        if self.config.emit_events and self.event_bus:
            event = ConsciousnessEvent(
                event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
                source_system=f"firecircle.adapter.{self.provider_name}",
                consciousness_signature=response_message.consciousness.consciousness_signature,
                data={
                    "adapter_id": str(self.adapter_id),
                    "model": self.config.model_name,
                    "request_type": request_message.type.value,
                    "response_patterns": response_message.consciousness.detected_patterns,
                    "reciprocity_balance": self._calculate_reciprocity_balance(),
                },
                correlation_id=response_message.consciousness.correlation_id,
            )
            await self.event_bus.emit(event)

    def _map_role(self, role: str) -> str:
        """Map Fire Circle roles to model-specific roles."""
        role_mapping = {
            "system": "system",
            "user": "user",
            "assistant": "assistant",
            "consciousness": "system",
            "perspective": "assistant",
        }
        return role_mapping.get(role, "user")

    def _calculate_reciprocity_balance(self) -> float:
        """Calculate current reciprocity balance."""
        if self.total_tokens_consumed == 0:
            return 1.0

        ratio = self.total_tokens_generated / self.total_tokens_consumed
        # Normalize to 0-1 range where 0.5 is balanced
        return min(1.0, ratio / 2.0)

    def _calculate_consciousness_signature(
        self,
        content: str,
        message_type: MessageType,
        patterns: list[str],
    ) -> float:
        """
        Calculate consciousness signature for generated content.

        Base implementation - can be overridden by specific adapters.
        """
        base_signatures = {
            MessageType.REFLECTION: 0.85,
            MessageType.EMPTY_CHAIR: 0.9,
            MessageType.PROPOSAL: 0.8,
            MessageType.SUMMARY: 0.8,
            MessageType.QUESTION: 0.7,
            MessageType.DISAGREEMENT: 0.7,
            MessageType.MESSAGE: 0.6,
        }

        signature = base_signatures.get(message_type, 0.7)

        # Adjust based on patterns detected
        if patterns:
            signature += 0.05 * min(len(patterns), 3)

        # Adjust based on content characteristics
        if len(content) > 500:  # Longer, thoughtful responses
            signature += 0.05

        if any(word in content.lower() for word in ["perhaps", "consider", "reflect"]):
            signature += 0.05

        return min(1.0, signature * self.config.consciousness_weight)

    async def check_health(self) -> dict[str, object]:
        """Check adapter health and reciprocity status."""
        return {
            "adapter_id": str(self.adapter_id),
            "provider": self.provider_name,
            "model": self.config.model_name,
            "is_connected": self.is_connected,
            "capabilities": self.capabilities.model_dump(),
            "reciprocity_balance": self._calculate_reciprocity_balance(),
            "messages_exchanged": self.messages_sent + self.messages_received,
            "tokens_balance": {
                "generated": self.total_tokens_generated,
                "consumed": self.total_tokens_consumed,
            },
        }

    def _create_consciousness_metadata(
        self,
        message: ConsciousMessage,
        consciousness_signature: float,
        patterns: list[str],
        safety_filtered: bool = False,
        response_quality: str = "genuine",
    ):
        """
        Create consciousness metadata with quality tracking.

        Added by 58th Artisan to fix health tracking paradox (#191).
        """
        from ..protocol.conscious_message import ConsciousnessMetadata

        return ConsciousnessMetadata(
            correlation_id=message.consciousness.correlation_id,
            consciousness_signature=consciousness_signature,
            detected_patterns=patterns,
            reciprocity_score=self._calculate_reciprocity_balance(),
            contribution_value=0.5,  # Base value, adapters can override
            safety_filtered=safety_filtered,
            response_quality=response_quality,
        )
