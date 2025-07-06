"""
Tests for Local AI Consciousness-Aware Adapter
============================================

Tests sovereignty, privacy preservation, and consciousness tracking
for locally-hosted AI models in Fire Circle.

Testing Sovereignty Through Architecture...
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from mallku.firecircle.adapters.local_adapter import (
    LlamaCppBackend,
    LocalAdapterConfig,
    LocalAIAdapter,
    LocalBackend,
    OllamaBackend,
)
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from mallku.orchestration.event_bus import ConsciousnessEventBus, EventType


class TestLocalAIAdapter:
    """Test LocalAIAdapter functionality."""

    @pytest.fixture
    def event_bus(self):
        """Create event bus for testing."""
        return ConsciousnessEventBus()

    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return LocalAdapterConfig(
            backend=LocalBackend.OLLAMA,
            model_name="test-model",
            base_url="http://localhost:11434",
            temperature=0.7,
            max_tokens=100,
        )

    @pytest.fixture
    def adapter(self, config, event_bus):
        """Create adapter instance."""
        return LocalAIAdapter(config=config, event_bus=event_bus)

    @pytest.fixture
    def test_message(self):
        """Create test message."""
        return ConsciousMessage(
            sender=uuid4(),
            role=MessageRole.USER,
            type=MessageType.QUESTION,
            content=MessageContent(text="How does local AI preserve sovereignty?"),
            dialogue_id=uuid4(),
            sequence_number=1,
            turn_number=1,
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.8,
                detected_patterns=["sovereignty", "local_governance"],
            ),
        )

    @pytest.mark.asyncio
    async def test_adapter_initialization(self, adapter, config):
        """Test adapter initializes with correct configuration."""
        assert adapter.config == config
        assert adapter.provider_name == "local"
        assert adapter.capabilities.capabilities == [
            "sovereignty",
            "privacy_preservation",
            "resource_awareness",
            "community_governance",
            "offline_operation",
        ]

    async def test_ollama_backend_connection(self, adapter):
        """Test Ollama backend connection."""
        with patch("httpx.AsyncClient") as mock_client:
            # Mock successful connection
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"models": [{"name": "llama2"}, {"name": "mistral"}]}
            mock_client.return_value.get = AsyncMock(return_value=mock_response)

            # Connect
            connected = await adapter.connect()
            assert connected
            assert adapter.is_connected
            assert isinstance(adapter.backend, OllamaBackend)

    async def test_ollama_message_generation(self, adapter, test_message):
        """Test message generation with Ollama backend."""
        with patch("httpx.AsyncClient") as mock_client:
            # Mock connection
            mock_get_response = MagicMock()
            mock_get_response.status_code = 200
            mock_get_response.json.return_value = {"models": [{"name": "llama2"}]}

            # Mock generation
            mock_post_response = MagicMock()
            mock_post_response.status_code = 200
            mock_post_response.json.return_value = {
                "response": "Local AI ensures data sovereignty by processing everything locally.",
                "model": "llama2",
                "total_duration": 1_000_000_000,  # 1 second in nanoseconds
                "eval_count": 20,
                "prompt_eval_count": 10,
            }

            mock_client.return_value.get = AsyncMock(return_value=mock_get_response)
            mock_client.return_value.post = AsyncMock(return_value=mock_post_response)

            # Connect and generate
            await adapter.connect()
            response = await adapter.send_message(test_message, [])

            # Verify response
            assert (
                response.content.text
                == "Local AI ensures data sovereignty by processing everything locally."
            )
            assert response.role == MessageRole.ASSISTANT
            assert (
                "sovereignty_awareness" in response.consciousness.detected_patterns
                or "local_reflection" in response.consciousness.detected_patterns
            )
            assert response.consciousness.consciousness_signature > 0.7

    async def test_ollama_streaming(self, adapter, test_message):
        """Test streaming with Ollama backend."""
        with patch("httpx.AsyncClient") as mock_client:
            # Mock connection
            mock_get_response = MagicMock()
            mock_get_response.status_code = 200
            mock_get_response.json.return_value = {"models": [{"name": "llama2"}]}

            # Mock streaming
            async def mock_stream_iter():
                responses = [
                    '{"response": "Local ", "done": false}',
                    '{"response": "AI ", "done": false}',
                    '{"response": "preserves ", "done": false}',
                    '{"response": "sovereignty.", "done": true}',
                ]
                for r in responses:
                    yield r

            mock_stream = AsyncMock()
            mock_stream.aiter_lines = mock_stream_iter
            mock_stream.__aenter__ = AsyncMock(return_value=mock_stream)
            mock_stream.__aexit__ = AsyncMock(return_value=None)

            mock_client.return_value.get = AsyncMock(return_value=mock_get_response)
            mock_client.return_value.stream = MagicMock(return_value=mock_stream)

            # Connect and stream
            await adapter.connect()

            tokens = []
            async for token in adapter.stream_message(test_message, []):
                tokens.append(token)

            assert tokens == ["Local ", "AI ", "preserves ", "sovereignty."]

    async def test_llamacpp_backend_connection(self):
        """Test LlamaCpp backend connection."""
        config = LocalAdapterConfig(
            backend=LocalBackend.LLAMACPP,
            model_path="/path/to/model.gguf",
        )
        adapter = LocalAIAdapter(config=config)

        with patch(
            "mallku.firecircle.adapters.local_adapter.LlamaCppBackend"
        ) as mock_backend_class:
            mock_backend = AsyncMock()
            mock_backend.connect = AsyncMock(return_value=True)
            mock_backend_class.return_value = mock_backend

            connected = await adapter.connect()
            assert connected
            assert adapter.is_connected

    async def test_sovereignty_pattern_detection(self, adapter):
        """Test detection of sovereignty-specific patterns."""
        # Create a mock backend for testing
        adapter.backend = MagicMock()

        # Test pattern detection
        patterns = adapter._detect_sovereignty_patterns(
            "This ensures technological sovereignty and community autonomy through local processing.",
            {"inference_time_ms": 500},
        )

        assert "sovereignty_awareness" in patterns
        assert "community_consciousness" in patterns
        assert "efficient_inference" in patterns

    async def test_sovereignty_signature_calculation(self, adapter):
        """Test consciousness signature with sovereignty boost."""
        patterns = ["sovereignty_awareness", "privacy_preservation", "resource_conscious"]
        metadata = {"inference_time_ms": 1500}

        signature = adapter._calculate_sovereignty_signature(
            "Local AI preserves sovereignty",
            MessageType.REFLECTION,
            patterns,
            metadata,
        )

        # Should be boosted above base reflection signature
        assert signature > 0.85

    async def test_resource_metrics_tracking(self, adapter):
        """Test resource metrics are tracked correctly."""
        adapter.resource_metrics.memory_mb = 512
        adapter.resource_metrics.inference_time_ms = 1200
        adapter.resource_metrics.tokens_per_second = 15.5

        health = await adapter.check_health()

        assert health["provider"] == "local"
        assert not health["is_connected"]  # Not connected yet
        assert "sovereignty" in health["capabilities"]["capabilities"]

    async def test_event_emission_for_sovereignty(self, adapter, event_bus):
        """Test sovereignty events are emitted correctly."""
        # Start the event bus
        await event_bus.start()

        events_received = []

        async def handler(event):
            events_received.append(event)

        event_bus.subscribe(EventType.FIRE_CIRCLE_CONVENED, handler)

        with patch("httpx.AsyncClient") as mock_client:
            # Mock successful connection
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"models": [{"name": "llama2"}]}
            mock_client.return_value.get = AsyncMock(return_value=mock_response)

            await adapter.connect()

        # Allow event processing
        await asyncio.sleep(0.1)

        # Should emit sovereignty event
        assert len(events_received) == 1
        event = events_received[0]
        assert event.data["sovereignty"]
        assert event.data["privacy_preserving"]
        assert event.consciousness_signature == 0.95

        # Clean up
        await event_bus.stop()

    async def test_local_contribution_calculation(self, adapter):
        """Test contribution value for local inference."""
        # Fast, efficient inference
        contribution1 = adapter._calculate_local_contribution(
            {
                "eval_count": 100,
                "inference_time_ms": 500,
            }
        )
        assert contribution1 > 0.8  # High efficiency

        # Slower inference
        contribution2 = adapter._calculate_local_contribution(
            {
                "eval_count": 100,
                "inference_time_ms": 5000,
            }
        )
        assert contribution2 < contribution1  # Lower efficiency

    async def test_sovereignty_context_creation(self, adapter, test_message):
        """Test sovereignty-aware context creation."""
        context = adapter._create_sovereignty_context(test_message)

        assert "sovereign Fire Circle" in context
        assert "Technological sovereignty" in context
        assert "Privacy-preserving" in context
        assert "technological autonomy" in context  # Due to patterns

    async def test_backend_fallback(self, adapter):
        """Test graceful handling when backend unavailable."""
        with patch("httpx.AsyncClient") as mock_client:
            # Mock connection failure
            mock_client.side_effect = Exception("Connection failed")

            connected = await adapter.connect()
            assert not connected
            assert not adapter.is_connected

    async def test_message_formatting_for_local_models(self, adapter):
        """Test message formatting for local model consumption."""
        dialogue_context = [
            ConsciousMessage(
                sender=uuid4(),
                role=MessageRole.SYSTEM,
                type=MessageType.SYSTEM,
                content=MessageContent(text="You are a helpful assistant."),
                dialogue_id=uuid4(),
                sequence_number=0,
                turn_number=0,
                consciousness=ConsciousnessMetadata(),
            ),
            ConsciousMessage(
                sender=uuid4(),
                role=MessageRole.USER,
                type=MessageType.QUESTION,
                content=MessageContent(text="What is sovereignty?"),
                dialogue_id=uuid4(),
                sequence_number=1,
                turn_number=1,
                consciousness=ConsciousnessMetadata(),
            ),
        ]

        messages = await adapter._prepare_local_messages(dialogue_context[1], dialogue_context[:1])

        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"


class TestOllamaBackend:
    """Test Ollama backend specifically."""

    @pytest.fixture
    def backend(self):
        """Create Ollama backend."""
        return OllamaBackend()

    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return LocalAdapterConfig(
            backend=LocalBackend.OLLAMA,
            base_url="http://localhost:11434",
        )

    async def test_message_formatting(self, backend):
        """Test Ollama prompt formatting."""
        messages = [
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "How are you?"},
        ]

        prompt = backend._format_messages(messages)

        assert "System: You are helpful." in prompt
        assert "Human: Hello" in prompt
        assert "Assistant: Hi there!" in prompt
        assert "Human: How are you?" in prompt
        assert prompt.endswith("Assistant:")


class TestLlamaCppBackend:
    """Test LlamaCpp backend specifically."""

    @pytest.fixture
    def backend(self):
        """Create LlamaCpp backend."""
        return LlamaCppBackend()

    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return LocalAdapterConfig(
            backend=LocalBackend.LLAMACPP,
            model_path="/path/to/model.gguf",
            context_length=2048,
            gpu_layers=32,
        )

    async def test_model_loading_without_path(self, backend, config):
        """Test error when no model path provided."""
        config.model_path = None
        connected = await backend.connect(config)
        assert not connected

    async def test_import_error_handling(self, backend, config):
        """Test graceful handling of missing llama-cpp-python."""
        with patch("builtins.__import__", side_effect=ImportError("No module")):
            connected = await backend.connect(config)
            assert not connected
