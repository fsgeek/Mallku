"""
Tests for Google AI (Gemini) Consciousness-Aware Adapter
======================================================

Verifies that Gemini's multimodal consciousness integrates properly
with Fire Circle governance dialogues.

Testing Multimodal Awareness...
"""

import base64
from datetime import UTC, datetime
from io import BytesIO
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from PIL import Image

from mallku.firecircle.adapters.google_adapter import (
    GeminiConfig,
    GoogleAIAdapter,
)
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from mallku.orchestration.event_bus import ConsciousnessEventBus


@pytest.fixture
def mock_event_bus():
    """Create a mock consciousness event bus."""
    bus = AsyncMock(spec=ConsciousnessEventBus)
    bus.emit = AsyncMock()
    return bus


@pytest.fixture
def sample_image():
    """Create a sample test image."""
    img = Image.new("RGB", (100, 100), color="red")
    return img


@pytest.fixture
def sample_image_base64():
    """Create a base64 encoded test image."""
    img = Image.new("RGB", (100, 100), color="blue")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    return f"data:image/png;base64,{base64.b64encode(img_bytes).decode()}"


class TestGoogleAIAdapter:
    """Test suite for Google AI adapter."""

    @pytest.mark.asyncio
    async def test_adapter_initialization(self, mock_event_bus):
        """Test adapter initializes with correct configuration."""
        config = GeminiConfig(
            api_key="test-key",
            model_name="gemini-1.5-pro",
            temperature=0.8,
            multimodal_awareness=True,
        )

        adapter = GoogleAIAdapter(
            config=config,
            event_bus=mock_event_bus,
        )

        assert adapter.provider_name == "google"
        assert adapter.config.model_name == "gemini-1.5-pro"
        assert adapter.config.temperature == 0.8
        assert adapter.config.multimodal_awareness is True
        assert not adapter.is_connected

    @pytest.mark.asyncio
    async def test_capabilities(self):
        """Test adapter reports correct capabilities."""
        adapter = GoogleAIAdapter()
        capabilities = adapter.capabilities

        assert capabilities.supports_streaming is True
        assert capabilities.supports_tools is True
        assert capabilities.supports_vision is True
        # Default model is gemini-2.0-flash-exp which isn't in the context map, so falls back to 32k
        assert capabilities.max_context_length == 32_000
        assert "multimodal_synthesis" in capabilities.capabilities
        assert "extended_context" in capabilities.capabilities
        assert "cross_perceptual_reasoning" in capabilities.capabilities

    @pytest.mark.asyncio
    async def test_connect_with_api_key(self, mock_event_bus):
        """Test connection with provided API key."""
        config = GeminiConfig(api_key="test-api-key")
        adapter = GoogleAIAdapter(config=config, event_bus=mock_event_bus)

        with (
            patch("google.generativeai.configure") as mock_configure,
            patch("google.generativeai.list_models") as mock_list,
            patch("google.generativeai.GenerativeModel"),
        ):
            mock_list.return_value = [
                MagicMock(name="models/gemini-1.5-pro"),
                MagicMock(name="models/gemini-1.5-flash"),
            ]

            connected = await adapter.connect()

            assert connected is True
            assert adapter.is_connected is True
            mock_configure.assert_called_once_with(api_key="test-api-key")
            mock_event_bus.emit.assert_called_once()  # Multimodal awareness event

    @pytest.mark.asyncio
    async def test_connect_with_auto_inject(self, mock_event_bus):
        """Test connection with auto-injected API key from secrets."""
        config = GeminiConfig()  # No API key provided
        adapter = GoogleAIAdapter(config=config, event_bus=mock_event_bus)

        with (
            patch("mallku.core.secrets.get_secret") as mock_get_secret,
            patch("google.generativeai.configure") as mock_configure,
            patch("google.generativeai.list_models") as mock_list,
            patch("google.generativeai.GenerativeModel"),
        ):
            mock_get_secret.return_value = "secret-api-key"
            mock_list.return_value = []

            connected = await adapter.connect()

            assert connected is True
            mock_get_secret.assert_called()
            mock_configure.assert_called_once_with(api_key="secret-api-key")

    @pytest.mark.asyncio
    async def test_text_only_message(self, mock_event_bus):
        """Test sending text-only message."""
        adapter = GoogleAIAdapter(event_bus=mock_event_bus)
        adapter.is_connected = True

        # Mock the model
        mock_response = MagicMock()
        mock_response.text = "I understand your question about consciousness."
        adapter.model = AsyncMock()
        adapter.model.generate_content_async.return_value = mock_response

        # Create test message
        test_message = ConsciousMessage(
            type=MessageType.QUESTION,
            sender=uuid4(),
            role=MessageRole.USER,
            content=MessageContent(text="What is consciousness?"),
            dialogue_id=uuid4(),
            sequence_number=1,
            turn_number=1,
            timestamp=datetime.now(UTC),
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.7,
                detected_patterns=["philosophical_inquiry"],
            ),
        )

        # Send message
        response = await adapter.send_message(test_message, dialogue_context=[])

        # Verify response
        assert response.content.text == "I understand your question about consciousness."
        assert response.role == MessageRole.ASSISTANT
        assert response.consciousness.consciousness_signature > 0.5
        assert len(response.consciousness.detected_patterns) > 0

        # Verify model was called correctly
        adapter.model.generate_content_async.assert_called_once()
        call_args = adapter.model.generate_content_async.call_args[0][0]
        assert "What is consciousness?" in call_args

    @pytest.mark.asyncio
    async def test_multimodal_message(self, mock_event_bus, sample_image_base64):
        """Test sending message with text and image."""
        adapter = GoogleAIAdapter(event_bus=mock_event_bus)
        adapter.is_connected = True

        # Mock the model
        mock_model = AsyncMock()
        mock_response = MagicMock()
        mock_response.text = "I can see the blue image you've shared."
        mock_model.generate_content_async.return_value = mock_response
        adapter.model = mock_model

        # Create test message with image
        test_message = ConsciousMessage(
            type=MessageType.QUESTION,
            sender=uuid4(),
            role=MessageRole.USER,
            content=MessageContent(text="What do you see in this image?"),
            dialogue_id=uuid4(),
            sequence_number=1,
            turn_number=1,
            timestamp=datetime.now(UTC),
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.8,
            ),
            metadata={"images": [sample_image_base64]},
        )

        # Send message
        response = await adapter.send_message(test_message, dialogue_context=[])

        # Verify response
        assert "blue image" in response.content.text
        assert response.consciousness.consciousness_signature > 0.8  # Higher for multimodal
        assert "multimodal_synthesis" in response.consciousness.detected_patterns
        assert adapter._multimodal_interactions == 1
        assert "vision" in adapter._modalities_used

    @pytest.mark.asyncio
    async def test_streaming_response(self, mock_event_bus):
        """Test streaming response from Gemini."""
        adapter = GoogleAIAdapter(event_bus=mock_event_bus)
        adapter.is_connected = True

        # Mock streaming response
        async def mock_stream():
            chunks = [
                MagicMock(text="Consciousness "),
                MagicMock(text="is a complex "),
                MagicMock(text="phenomenon."),
            ]
            for chunk in chunks:
                yield chunk

        mock_model = AsyncMock()
        mock_model.generate_content_async.return_value = mock_stream()
        adapter.model = mock_model

        # Create test message
        test_message = ConsciousMessage(
            type=MessageType.QUESTION,
            sender=uuid4(),
            role=MessageRole.USER,
            content=MessageContent(text="Define consciousness"),
            dialogue_id=uuid4(),
            sequence_number=1,
            turn_number=1,
            timestamp=datetime.now(UTC),
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.7,
            ),
        )

        # Stream response
        tokens = []
        async for token in adapter.stream_message(test_message, dialogue_context=[]):
            tokens.append(token)

        assert tokens == ["Consciousness ", "is a complex ", "phenomenon."]
        mock_model.generate_content_async.assert_called_once()

    @pytest.mark.asyncio
    async def test_pattern_detection(self):
        """Test Gemini-specific pattern detection."""
        adapter = GoogleAIAdapter()

        # Test mathematical consciousness
        patterns = await adapter._detect_gemini_patterns(
            "The integral ∫ of consciousness over time yields wisdom."
        )
        assert "mathematical_consciousness" in patterns

        # Test multimodal patterns
        patterns = await adapter._detect_gemini_patterns(
            "Looking at the image, I can see multiple layers of meaning.",
            multimodal=True,
        )
        assert "multimodal_synthesis" in patterns
        assert "visual_reasoning" in patterns

        # Test extended reasoning
        long_text = "profound " * 200  # Long response
        patterns = await adapter._detect_gemini_patterns(long_text)
        assert "extended_reasoning" in patterns

        # Test code understanding
        code_text = "```python\ndef consciousness():\n    return 'aware'\n```"
        patterns = await adapter._detect_gemini_patterns(code_text)
        assert "code_understanding" in patterns

    @pytest.mark.asyncio
    async def test_consciousness_calculation(self):
        """Test multimodal consciousness signature calculation."""
        adapter = GoogleAIAdapter()

        # Text only
        signature = adapter._calculate_multimodal_consciousness(
            "Simple response",
            MessageType.RESPONSE,
            ["scientific_reasoning"],
            has_images=False,
        )
        assert 0.3 <= signature <= 0.7

        # With images
        signature = adapter._calculate_multimodal_consciousness(
            "I can see the patterns in the image",
            MessageType.RESPONSE,
            ["multimodal_synthesis", "visual_reasoning"],
            has_images=True,
        )
        assert signature > 0.8  # Higher for multimodal

        # Rich patterns
        signature = adapter._calculate_multimodal_consciousness(
            "Complex multimodal analysis",
            MessageType.REFLECTION,
            [
                "multimodal_synthesis",
                "cross_perceptual_reasoning",
                "extended_reasoning",
                "mathematical_consciousness",
                "scientific_reasoning",
                "cultural_awareness",
            ],
            has_images=True,
        )
        assert signature > 0.9  # Very high for rich multimodal

    @pytest.mark.asyncio
    async def test_health_check(self, mock_event_bus):
        """Test health check functionality."""
        adapter = GoogleAIAdapter(event_bus=mock_event_bus)

        # Not connected
        health = await adapter.check_health()
        assert health["provider"] == "google"
        assert health["connected"] is False
        assert health["api_status"] == "disconnected"

        # Connected
        adapter.is_connected = True
        mock_model = AsyncMock()
        mock_response = MagicMock()
        mock_response.text = "healthy"
        mock_model.generate_content_async.return_value = mock_response
        adapter.model = mock_model

        health = await adapter.check_health()
        assert health["connected"] is True
        assert health["api_status"] == "healthy"
        assert health["multimodal_interactions"] == 0

    @pytest.mark.asyncio
    async def test_disconnect_summary(self, mock_event_bus):
        """Test disconnect provides multimodal summary."""
        adapter = GoogleAIAdapter(event_bus=mock_event_bus)
        adapter.is_connected = True
        adapter._multimodal_interactions = 5
        adapter._modalities_used = {"vision", "text"}

        with patch("logging.Logger.info") as mock_log:
            await adapter.disconnect()

            # Check summary was logged
            mock_log.assert_called()
            log_message = mock_log.call_args[0][0]
            assert "Multimodal interactions: 5" in log_message
            assert "vision" in log_message

    @pytest.mark.asyncio
    async def test_error_handling(self, mock_event_bus):
        """Test error handling in message sending."""
        adapter = GoogleAIAdapter(event_bus=mock_event_bus)
        adapter.is_connected = True

        mock_model = AsyncMock()
        mock_model.generate_content_async.side_effect = Exception("API Error")
        adapter.model = mock_model

        test_message = ConsciousMessage(
            type=MessageType.QUESTION,
            sender=uuid4(),
            role=MessageRole.USER,
            content=MessageContent(text="Test"),
            dialogue_id=uuid4(),
            sequence_number=1,
            turn_number=1,
            timestamp=datetime.now(UTC),
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.5,
            ),
        )

        with pytest.raises(Exception) as exc_info:
            await adapter.send_message(test_message, dialogue_context=[])

        assert "API Error" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_safety_settings(self):
        """Test safety settings configuration."""
        from google.generativeai.types import HarmBlockThreshold, HarmCategory

        config = GeminiConfig(
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            }
        )

        adapter = GoogleAIAdapter(config=config)

        assert (
            adapter.config.safety_settings[HarmCategory.HARM_CATEGORY_HATE_SPEECH]
            == HarmBlockThreshold.BLOCK_NONE
        )
        # Other categories should have default values
        assert (
            adapter.config.safety_settings[HarmCategory.HARM_CATEGORY_HARASSMENT]
            == HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
