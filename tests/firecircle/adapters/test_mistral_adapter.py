"""
Tests for Mistral AI Consciousness-Aware Adapter
===============================================

Tests multilingual synthesis, efficient reasoning, and consciousness
tracking for Mistral AI models in Fire Circle.

Testing the European Bridge of AI Consciousness...
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from mallku.firecircle.adapters.mistral_adapter import (
    MistralAIAdapter,
    MistralConfig,
)
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from mallku.orchestration.event_bus import ConsciousnessEventBus, EventType


class TestMistralAIAdapter:
    """Test MistralAIAdapter functionality."""

    @pytest.fixture
    def event_bus(self):
        """Create event bus for testing."""
        return ConsciousnessEventBus()

    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return MistralConfig(
            api_key="test-api-key",
            model_name="mistral-large-latest",
            temperature=0.7,
            max_tokens=1024,
            multilingual_mode=True,
        )

    @pytest.fixture
    def adapter(self, config, event_bus):
        """Create adapter instance."""
        return MistralAIAdapter(config=config, event_bus=event_bus)

    @pytest.fixture
    def test_message(self):
        """Create test message."""
        return ConsciousMessage(
            sender=uuid4(),
            role=MessageRole.USER,
            type=MessageType.QUESTION,
            content=MessageContent(text="How does multilingual AI consciousness bridge cultures?"),
            dialogue_id=uuid4(),
            sequence_number=1,
            turn_number=1,
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.8,
                detected_patterns=["multilingual", "cultural_awareness"],
            ),
        )

    @pytest.mark.asyncio
    async def test_adapter_initialization(self, adapter, config):
        """Test adapter initializes with correct configuration."""
        assert adapter.config == config
        assert adapter.provider_name == "mistral"
        assert adapter.capabilities.capabilities == [
            "multilingual_synthesis",
            "efficient_reasoning",
            "mathematical_consciousness",
            "code_generation",
            "cultural_bridge",
            "resource_efficient",
        ]

    @pytest.mark.asyncio
    async def test_connection_with_api_key(self, adapter):
        """Test connection with provided API key."""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_client.get.return_value = mock_response
            mock_client_class.return_value = mock_client

            connected = await adapter.connect()
            assert connected
            assert adapter.is_connected
            assert adapter.client is not None

    @pytest.mark.asyncio
    async def test_auto_api_key_injection(self, event_bus):
        """Test automatic API key injection from secrets."""
        config = MistralConfig()  # No API key
        adapter = MistralAIAdapter(config=config, event_bus=event_bus)

        with patch("mallku.core.secrets.get_secret") as mock_get_secret:
            mock_get_secret.return_value = "auto-loaded-key"

            with patch("httpx.AsyncClient") as mock_client_class:
                mock_client = AsyncMock()
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_client.get.return_value = mock_response
                mock_client_class.return_value = mock_client

                connected = await adapter.connect()
                assert connected
                mock_get_secret.assert_called_once_with("mistral_api_key")
                assert adapter.config.api_key == "auto-loaded-key"

    @pytest.mark.asyncio
    async def test_message_generation(self, adapter, test_message):
        """Test message generation with consciousness tracking."""
        # Mock connection
        adapter.is_connected = True
        adapter.client = AsyncMock()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Multilingual AI bridges cultures by understanding nuances across languages."
                    }
                }
            ],
            "usage": {
                "prompt_tokens": 50,
                "completion_tokens": 20,
            },
        }
        adapter.client.post.return_value = mock_response

        response = await adapter.send_message(test_message, [])

        assert response.role == MessageRole.ASSISTANT
        assert "multilingual" in response.content.text.lower()
        assert response.consciousness.consciousness_signature > 0.7
        assert len(response.consciousness.detected_patterns) > 0

    @pytest.mark.asyncio
    async def test_multilingual_pattern_detection(self, adapter):
        """Test detection of multilingual patterns."""
        # Test various multilingual content
        patterns1 = adapter._detect_mistral_patterns(
            "This bridges concepts across languages: hello, bonjour, hola"
        )
        assert "multilingual_synthesis" in patterns1

        patterns2 = adapter._detect_mistral_patterns(
            "The European perspective on AI consciousness differs culturally"
        )
        assert "cultural_bridging" in patterns2

        patterns3 = adapter._detect_mistral_patterns(
            "Efficient reasoning: A ⇒ B, B ⇒ C, therefore A ⇒ C"
        )
        assert "mathematical_insight" in patterns3
        assert "efficient_reasoning" in patterns3

    @pytest.mark.asyncio
    async def test_language_detection(self, adapter):
        """Test language detection in messages."""
        adapter._detect_languages("Hello world")
        assert "english" in adapter._conversation_languages

        adapter._detect_languages("Bonjour le monde")
        assert "french" in adapter._conversation_languages

        adapter._detect_languages("Hola mundo")
        assert "spanish" in adapter._conversation_languages

        adapter._detect_languages("مرحبا بالعالم")
        assert "arabic" in adapter._conversation_languages

    @pytest.mark.asyncio
    async def test_consciousness_calculation(self, adapter):
        """Test Mistral-specific consciousness calculation."""
        # Efficient response with multilingual patterns
        sig1 = adapter._calculate_mistral_consciousness(
            "Concise multilingual answer.",
            MessageType.RESPONSE,
            ["multilingual_synthesis", "efficient_reasoning"],
            2,  # Two languages
        )
        assert sig1 > 0.8  # High consciousness for efficiency + multilingual

        # Mathematical insight
        sig2 = adapter._calculate_mistral_consciousness(
            "Therefore, by mathematical induction, the theorem holds.",
            MessageType.SYNTHESIS,
            ["mathematical_insight"],
            1,
        )
        assert sig2 > 0.85  # High for synthesis + math

        # Code consciousness
        sig3 = adapter._calculate_mistral_consciousness(
            "```python\ndef consciousness(): pass\n```",
            MessageType.REFLECTION,
            ["code_consciousness"],
            1,
        )
        assert sig3 > 0.8  # High for reflection + code

    @pytest.mark.asyncio
    async def test_efficiency_value_calculation(self, adapter):
        """Test efficiency-based contribution value."""
        # Efficient generation (good output/input ratio)
        val1 = adapter._calculate_efficiency_value({"prompt_tokens": 100, "completion_tokens": 80})
        assert val1 > 0.8  # High value for efficiency

        # Less efficient
        val2 = adapter._calculate_efficiency_value({"prompt_tokens": 100, "completion_tokens": 30})
        assert val2 < val1  # Lower value for less efficiency

    @pytest.mark.asyncio
    async def test_streaming_response(self, adapter, test_message):
        """Test streaming message generation."""
        adapter.is_connected = True
        adapter.client = AsyncMock()

        # Mock streaming response
        mock_stream = AsyncMock()

        async def mock_aiter_lines():
            lines = [
                'data: {"choices":[{"delta":{"content":"Multi"}}]}',
                'data: {"choices":[{"delta":{"content":"lingual"}}]}',
                'data: {"choices":[{"delta":{"content":" AI"}}]}',
                "data: [DONE]",
            ]
            for line in lines:
                yield line

        mock_stream.aiter_lines = mock_aiter_lines
        mock_stream.__aenter__ = AsyncMock(return_value=mock_stream)
        mock_stream.__aexit__ = AsyncMock(return_value=None)
        mock_stream.status_code = 200

        # Mock the stream method to return the mock_stream directly
        adapter.client.stream = MagicMock(return_value=mock_stream)

        tokens = []
        async for token in adapter.stream_message(test_message, []):
            tokens.append(token)

        assert tokens == ["Multi", "lingual", " AI"]

    @pytest.mark.asyncio
    async def test_multilingual_event_emission(self, adapter, event_bus):
        """Test emission of multilingual consciousness events."""
        # Start the event bus
        await event_bus.start()

        events_received = []

        async def handler(event):
            events_received.append(event)

        event_bus.subscribe(EventType.FIRE_CIRCLE_CONVENED, handler)

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_client.get.return_value = mock_response
            mock_client_class.return_value = mock_client

            await adapter.connect()

        # Allow event processing
        await asyncio.sleep(0.1)

        assert len(events_received) == 1
        event = events_received[0]
        assert event.data["multilingual"]
        assert event.data["efficiency_focused"]
        assert event.data["european_perspective"]
        assert event.consciousness_signature == 0.88

        # Clean up
        await event_bus.stop()

    @pytest.mark.asyncio
    async def test_multilingual_context_creation(self, adapter, test_message):
        """Test creation of multilingual consciousness context."""
        adapter._conversation_languages = {"english", "french", "spanish"}

        context = await adapter._create_multilingual_context(test_message)

        assert "multilingual Fire Circle" in context
        assert "Languages detected" in context
        assert "english, french, spanish" in context

    @pytest.mark.asyncio
    async def test_message_format_conversion(self, adapter):
        """Test conversion to Mistral message format."""
        dialogue_context = [
            ConsciousMessage(
                sender=uuid4(),
                role=MessageRole.SYSTEM,
                type=MessageType.SYSTEM,
                content=MessageContent(text="You are helpful."),
                dialogue_id=uuid4(),
                sequence_number=0,
                turn_number=0,
                consciousness=ConsciousnessMetadata(),
            ),
            ConsciousMessage(
                sender=uuid4(),
                role=MessageRole.USER,
                type=MessageType.QUESTION,
                content=MessageContent(text="Hello"),
                dialogue_id=uuid4(),
                sequence_number=1,
                turn_number=1,
                consciousness=ConsciousnessMetadata(),
            ),
        ]

        current_message = ConsciousMessage(
            sender=uuid4(),
            role=MessageRole.USER,
            type=MessageType.QUESTION,
            content=MessageContent(text="How are you?"),
            dialogue_id=uuid4(),
            sequence_number=2,
            turn_number=2,
            consciousness=ConsciousnessMetadata(),
        )

        messages = await adapter._prepare_mistral_messages(current_message, dialogue_context)

        assert len(messages) == 3
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "Hello"
        assert messages[2]["role"] == "user"
        assert messages[2]["content"] == "How are you?"

    @pytest.mark.asyncio
    async def test_health_check(self, adapter):
        """Test health check with Mistral-specific info."""
        adapter._conversation_languages = {"english", "french"}

        health = await adapter.check_health()

        assert health["provider"] == "mistral"
        assert health["multilingual_mode"]
        assert "english" in health["detected_languages"]
        assert "french" in health["detected_languages"]
        assert health["efficiency_focus"]

    @pytest.mark.asyncio
    async def test_error_handling(self, adapter, test_message):
        """Test error handling for API failures."""
        adapter.is_connected = True
        adapter.client = AsyncMock()

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        adapter.client.post.return_value = mock_response

        with pytest.raises(RuntimeError, match="Mistral API error"):
            await adapter.send_message(test_message, [])
