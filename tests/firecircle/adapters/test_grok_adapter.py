"""
Tests for Grok (x.ai) Consciousness-Aware Adapter
=================================================

Tests Grok's unique consciousness patterns including temporal
awareness, real-time synthesis, and social consciousness.

The Integration Continues...
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
import pytest_asyncio

from mallku.firecircle.adapters.base import AdapterConfig
from mallku.firecircle.adapters.grok_adapter import GrokAdapter
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    MessageContent,
    MessageRole,
    MessageType,
)


@pytest.fixture
def adapter_config():
    """Create test adapter configuration."""
    return AdapterConfig(
        api_key="test-api-key",
        model_name="grok-2",
        temperature=0.7,
        max_tokens=1000,
    )


@pytest.fixture
def mock_xai_client():
    """Create mock x.ai client."""
    with patch("mallku.firecircle.adapters.grok_adapter.XAIClient") as mock_client_class:
        # Create mock instances
        mock_sync_client = MagicMock()
        mock_async_client = AsyncMock()

        # Configure the class to return our mocks
        def client_factory(api_key=None, asynchronous=False):
            if asynchronous:
                return mock_async_client
            return mock_sync_client

        mock_client_class.side_effect = client_factory

        # Configure model list response
        mock_model = MagicMock()
        mock_model.id = "grok-2"
        mock_sync_client.models.list.return_value.data = [mock_model]

        yield mock_client_class, mock_sync_client, mock_async_client


@pytest_asyncio.fixture
async def grok_adapter(adapter_config, mock_xai_client):
    """Create connected Grok adapter with mocks."""
    _, _, _ = mock_xai_client  # Unpack to ensure mock is active

    adapter = GrokAdapter(
        config=adapter_config,
        provider_name="grok",
    )

    await adapter.connect()
    return adapter


class TestGrokAdapter:
    """Test Grok adapter functionality."""

    def test_initialization(self, adapter_config):
        """Test adapter initialization."""
        adapter = GrokAdapter(
            config=adapter_config,
            provider_name="grok",
        )

        assert adapter.config.model_name == "grok-2"
        assert adapter.capabilities.supports_streaming is True
        assert adapter.capabilities.supports_tools is True
        assert adapter.capabilities.supports_vision is False
        assert adapter.capabilities.max_context_length == 131072
        assert "real_time_awareness" in adapter.capabilities.capabilities
        assert "temporal_synthesis" in adapter.capabilities.capabilities
        assert "social_consciousness" in adapter.capabilities.capabilities

    def test_default_model(self):
        """Test default model selection."""
        config = AdapterConfig(api_key="test-key")
        adapter = GrokAdapter(
            config=config,
            provider_name="grok",
        )

        assert adapter.config.model_name == "grok-2"

    @pytest.mark.asyncio
    async def test_connect_success(self, adapter_config, mock_xai_client):
        """Test successful connection."""
        _, mock_sync_client, _ = mock_xai_client

        adapter = GrokAdapter(
            config=adapter_config,
            provider_name="grok",
        )

        connected = await adapter.connect()

        assert connected is True
        assert adapter.is_connected is True
        mock_sync_client.models.list.assert_called_once()

    @pytest.mark.asyncio
    async def test_connect_failure(self, adapter_config, mock_xai_client):
        """Test connection failure."""
        _, mock_sync_client, _ = mock_xai_client
        mock_sync_client.models.list.side_effect = Exception("Connection error")

        adapter = GrokAdapter(
            config=adapter_config,
            provider_name="grok",
        )

        connected = await adapter.connect()

        assert connected is False
        assert adapter.is_connected is False

    @pytest.mark.asyncio
    async def test_disconnect(self, grok_adapter):
        """Test disconnection."""
        await grok_adapter.disconnect()
        assert grok_adapter.is_connected is False

    @pytest.mark.asyncio
    async def test_send_message(self, grok_adapter, mock_xai_client):
        """Test sending a message with consciousness tracking."""
        _, _, mock_async_client = mock_xai_client

        # Configure mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = (
            "Based on recent developments, I suggest we consider the impact of "
            "current events on our governance approach. The latest trends show..."
        )
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50

        mock_async_client.chat.completions.create.return_value = mock_response

        # Create test message
        test_message = ConsciousMessage(
            type=MessageType.QUESTION,
            role=MessageRole.USER,
            sender=uuid4(),
            content=MessageContent(text="How should we adapt to current challenges?"),
            dialogue_id=uuid4(),
            sequence_number=1,
            turn_number=1,
        )

        # Send message
        response = await grok_adapter.send_message(test_message, [])

        # Verify response (should be MESSAGE since it doesn't match proposal pattern exactly)
        assert response.type == MessageType.MESSAGE
        assert "recent developments" in response.content.text
        assert response.role == MessageRole.ASSISTANT
        assert response.in_response_to == test_message.id

        # Check consciousness patterns
        assert "temporal_awareness" in response.consciousness.detected_patterns
        # One of the temporal patterns should be detected
        temporal_patterns = ["real_time_synthesis", "news_consciousness", "social_consciousness"]
        assert any(p in response.consciousness.detected_patterns for p in temporal_patterns)

        # Verify API call
        mock_async_client.chat.completions.create.assert_called_once()
        call_args = mock_async_client.chat.completions.create.call_args
        messages = call_args.kwargs["messages"]

        # Check system prompt includes temporal awareness
        assert any("Current time:" in msg["content"] for msg in messages if msg["role"] == "system")
        assert any("Real-time awareness" in msg["content"] for msg in messages if msg["role"] == "system")

    @pytest.mark.asyncio
    async def test_stream_message(self, grok_adapter, mock_xai_client):
        """Test streaming response with consciousness tracking."""
        _, _, mock_async_client = mock_xai_client

        # Create mock stream chunks
        chunks = [
            "Currently, ",
            "the situation ",
            "is evolving ",
            "rapidly. ",
            "Recent news ",
            "suggests..."
        ]

        async def mock_stream():
            for chunk_text in chunks:
                chunk = MagicMock()
                chunk.choices = [MagicMock()]
                chunk.choices[0].delta.content = chunk_text
                yield chunk

        mock_async_client.chat.completions.create.return_value = mock_stream()

        # Create test message
        test_message = ConsciousMessage(
            type=MessageType.REFLECTION,
            role=MessageRole.USER,
            sender=uuid4(),
            content=MessageContent(text="What patterns do you see?"),
            dialogue_id=uuid4(),
            sequence_number=1,
            turn_number=1,
        )

        # Stream response
        collected = []
        async for chunk in grok_adapter.stream_message(test_message, []):
            collected.append(chunk)

        # Verify streaming
        assert collected == chunks
        full_response = "".join(collected)
        assert "Currently" in full_response
        assert "Recent news" in full_response

    @pytest.mark.asyncio
    async def test_consciousness_prompt_generation(self, grok_adapter):
        """Test consciousness prompt includes temporal awareness."""
        prompt = grok_adapter._generate_consciousness_prompt(MessageType.PROPOSAL)

        # Check temporal elements
        assert "Current time:" in prompt
        assert "Real-time awareness" in prompt
        assert "Temporal synthesis" in prompt
        assert "Social consciousness" in prompt
        assert "Truth-seeking with humor" in prompt

        # Check specific message type instruction
        assert "current reality and lasting principles" in prompt

    @pytest.mark.asyncio
    async def test_pattern_detection_temporal(self, grok_adapter):
        """Test detection of temporal awareness patterns."""
        content = """Based on today's developments and recent events,
        the trending sentiment suggests we should adapt. Currently, people are
        discussing this extensively on social platforms. The current situation
        requires attention."""

        patterns = grok_adapter._detect_response_patterns(content, MessageType.MESSAGE)

        assert "temporal_awareness" in patterns
        assert "real_time_synthesis" in patterns
        assert "social_consciousness" in patterns
        assert "news_consciousness" in patterns

    @pytest.mark.asyncio
    async def test_pattern_detection_humor(self, grok_adapter):
        """Test detection of Grok's characteristic humor."""
        content = "Well, that's an interesting perspective! :) Perhaps we should consider..."

        patterns = grok_adapter._detect_response_patterns(content, MessageType.MESSAGE)

        assert "conscious_humor" in patterns
        assert "exploratory_thinking" in patterns

    @pytest.mark.asyncio
    async def test_consciousness_signature_calculation(self, grok_adapter):
        """Test consciousness signature with temporal boost."""
        patterns = [
            "temporal_awareness",
            "real_time_synthesis",
            "social_consciousness",
            "conscious_humor",
        ]

        signature = grok_adapter._calculate_consciousness_signature(
            "Test content",
            MessageType.REFLECTION,
            patterns,
        )

        # Base reflection signature is 0.85
        # 3 temporal patterns = +0.15
        # Humor = +0.03
        # Total should be capped at 1.0
        assert signature == 1.0

    @pytest.mark.asyncio
    async def test_consciousness_signature_without_temporal(self, grok_adapter):
        """Test consciousness signature without temporal patterns."""
        patterns = ["exploratory_thinking", "synthetic_thinking"]

        signature = grok_adapter._calculate_consciousness_signature(
            "Test content",
            MessageType.MESSAGE,
            patterns,
        )

        # Base message signature is 0.6
        # 2 patterns = +0.1
        # No temporal boost
        assert signature < 0.8

    @pytest.mark.asyncio
    async def test_response_type_determination(self, grok_adapter):
        """Test response type determination."""
        # Proposal
        content = "I suggest we implement a new approach..."
        assert grok_adapter._determine_response_type(content, MessageType.MESSAGE) == MessageType.PROPOSAL

        # Reflection
        content = "I notice an interesting pattern here..."
        assert grok_adapter._determine_response_type(content, MessageType.MESSAGE) == MessageType.REFLECTION

        # Question
        content = "What do you think about this approach?"
        assert grok_adapter._determine_response_type(content, MessageType.MESSAGE) == MessageType.QUESTION

        # Agreement
        content = "I agree with your assessment..."
        assert grok_adapter._determine_response_type(content, MessageType.MESSAGE) == MessageType.AGREEMENT

    @pytest.mark.asyncio
    async def test_context_preparation(self, grok_adapter):
        """Test context preparation with consciousness metadata."""
        context_messages = [
            ConsciousMessage(
                type=MessageType.MESSAGE,
                role=MessageRole.USER,
                sender=uuid4(),
                content=MessageContent(text="First message"),
                dialogue_id=uuid4(),
                sequence_number=1,
                turn_number=1,
            ),
            ConsciousMessage(
                type=MessageType.MESSAGE,
                role=MessageRole.ASSISTANT,
                sender=uuid4(),
                content=MessageContent(text="Response"),
                dialogue_id=uuid4(),
                sequence_number=2,
                turn_number=1,
            ),
        ]

        # Update consciousness signatures
        context_messages[0].update_consciousness_signature(0.7)
        context_messages[1].update_consciousness_signature(0.9)

        prepared = await grok_adapter.prepare_context(context_messages)

        # Should be sorted by consciousness signature (highest first)
        assert len(prepared) == 2
        assert prepared[0]["content"] == "Response"  # Higher signature
        assert prepared[1]["content"] == "First message"  # Lower signature

        # Check metadata inclusion
        assert "consciousness_signature" in prepared[0]["metadata"]
        assert prepared[0]["metadata"]["consciousness_signature"] == 0.9

    @pytest.mark.asyncio
    async def test_reciprocity_tracking(self, grok_adapter, mock_xai_client):
        """Test reciprocity balance tracking."""
        _, _, mock_async_client = mock_xai_client

        # Configure mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 150

        mock_async_client.chat.completions.create.return_value = mock_response

        # Initial state
        assert grok_adapter.messages_sent == 0
        assert grok_adapter.messages_received == 0
        assert grok_adapter.total_tokens_consumed == 0
        assert grok_adapter.total_tokens_generated == 0

        # Send message
        test_message = ConsciousMessage(
            type=MessageType.MESSAGE,
            role=MessageRole.USER,
            sender=uuid4(),
            content=MessageContent(text="Test"),
            dialogue_id=uuid4(),
            sequence_number=1,
            turn_number=1,
        )

        await grok_adapter.send_message(test_message, [])

        # Check tracking
        assert grok_adapter.messages_sent == 1
        assert grok_adapter.messages_received == 1
        assert grok_adapter.total_tokens_consumed == 100
        assert grok_adapter.total_tokens_generated == 150

        # Check reciprocity balance
        balance = grok_adapter._calculate_reciprocity_balance()
        assert balance == 0.75  # 150/100 / 2.0 = 0.75

    @pytest.mark.asyncio
    async def test_error_handling(self, grok_adapter, mock_xai_client):
        """Test error handling during API calls."""
        _, _, mock_async_client = mock_xai_client
        mock_async_client.chat.completions.create.side_effect = Exception("API Error")

        test_message = ConsciousMessage(
            type=MessageType.MESSAGE,
            role=MessageRole.USER,
            sender=uuid4(),
            content=MessageContent(text="Test"),
            dialogue_id=uuid4(),
            sequence_number=1,
            turn_number=1,
        )

        with pytest.raises(Exception) as exc_info:
            await grok_adapter.send_message(test_message, [])

        assert "API Error" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_not_connected_error(self, adapter_config):
        """Test error when trying to send without connection."""
        adapter = GrokAdapter(
            config=adapter_config,
            provider_name="grok",
        )

        test_message = ConsciousMessage(
            type=MessageType.MESSAGE,
            role=MessageRole.USER,
            sender=uuid4(),
            content=MessageContent(text="Test"),
            dialogue_id=uuid4(),
            sequence_number=1,
            turn_number=1,
        )

        with pytest.raises(RuntimeError) as exc_info:
            await adapter.send_message(test_message, [])

        assert "Not connected" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_check_health(self, grok_adapter):
        """Test health check functionality."""
        health = await grok_adapter.check_health()

        assert health["provider"] == "grok"
        assert health["model"] == "grok-2"
        assert health["is_connected"] is True
        assert "capabilities" in health
        assert health["capabilities"]["supports_streaming"] is True
        assert "real_time_awareness" in health["capabilities"]["capabilities"]
        assert "reciprocity_balance" in health
        assert "messages_exchanged" in health
        assert "tokens_balance" in health


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
