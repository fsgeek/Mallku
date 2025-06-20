"""
Tests for OpenAI-Compatible Backend
===================================

Verifies that the sovereignty circle completion works correctly,
enabling any OpenAI-compatible server to participate in Fire Circle.

The Sovereignty Continues...
"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from mallku.firecircle.adapters.local_adapter import (
    LocalAdapterConfig,
    LocalAIAdapter,
    LocalBackend,
    OpenAICompatBackend,
)
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)


@pytest.mark.asyncio
async def test_openai_compat_backend_connect():
    """Test connection to OpenAI-compatible server."""
    backend = OpenAICompatBackend()
    config = LocalAdapterConfig(
        backend=LocalBackend.OPENAI_COMPAT,
        base_url="http://localhost:1234",
        model_name="test-model",
    )

    # Mock the OpenAI client
    mock_client = AsyncMock()
    mock_models = MagicMock()
    mock_models.data = [
        MagicMock(id="test-model"),
        MagicMock(id="other-model"),
    ]
    mock_client.models.list.return_value = mock_models

    with patch("openai.AsyncOpenAI", return_value=mock_client):
        connected = await backend.connect(config)

        assert connected is True
        assert backend.client is not None
        mock_client.models.list.assert_called_once()


@pytest.mark.asyncio
async def test_openai_compat_backend_generate():
    """Test generation through OpenAI-compatible backend."""
    backend = OpenAICompatBackend()
    backend.client = AsyncMock()

    # Mock response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
    mock_response.model = "test-model"
    mock_response.usage = MagicMock(
        prompt_tokens=10,
        completion_tokens=5,
        total_tokens=15,
    )
    mock_response.choices[0].finish_reason = "stop"

    backend.client.chat.completions.create = AsyncMock(return_value=mock_response)

    config = LocalAdapterConfig(
        model_name="test-model",
        temperature=0.7,
        max_tokens=100,
    )

    messages = [{"role": "user", "content": "Hello, AI!"}]

    response_text, metadata = await backend.generate(messages, config)

    assert response_text == "Test response"
    assert metadata["model"] == "test-model"
    assert metadata["prompt_tokens"] == 10
    assert metadata["completion_tokens"] == 5
    assert metadata["tokens_per_second"] > 0


@pytest.mark.asyncio
async def test_openai_compat_backend_stream():
    """Test streaming through OpenAI-compatible backend."""
    backend = OpenAICompatBackend()
    backend.client = AsyncMock()

    # Mock streaming response
    async def mock_stream():
        chunks = [
            MagicMock(choices=[MagicMock(delta=MagicMock(content="Hello"))]),
            MagicMock(choices=[MagicMock(delta=MagicMock(content=" from"))]),
            MagicMock(choices=[MagicMock(delta=MagicMock(content=" AI!"))]),
            MagicMock(choices=[MagicMock(delta=MagicMock(content=None))]),
        ]
        for chunk in chunks:
            yield chunk

    backend.client.chat.completions.create = AsyncMock(return_value=mock_stream())

    config = LocalAdapterConfig(model_name="test-model")
    messages = [{"role": "user", "content": "Stream test"}]

    tokens = []
    async for token in backend.stream_generate(messages, config):
        tokens.append(token)

    assert tokens == ["Hello", " from", " AI!"]


@pytest.mark.asyncio
async def test_local_adapter_with_openai_compat():
    """Test LocalAIAdapter using OpenAI-compatible backend."""
    config = LocalAdapterConfig(
        backend=LocalBackend.OPENAI_COMPAT,
        base_url="http://test-server:8080",
        model_name="sovereignty-model",
    )

    adapter = LocalAIAdapter(config=config)

    # Mock the backend
    mock_backend = AsyncMock()
    mock_backend.connect.return_value = True
    mock_backend.generate.return_value = (
        "Sovereignty means communities control their own destiny.",
        {
            "model": "sovereignty-model",
            "generation_time_ms": 250,
            "prompt_tokens": 20,
            "completion_tokens": 10,
        },
    )

    with patch.object(adapter, "backend", mock_backend):
        adapter.is_connected = True

        # Create test message
        test_message = ConsciousMessage(
            type=MessageType.QUESTION,
            sender=uuid4(),
            role=MessageRole.USER,
            content=MessageContent(text="What is technological sovereignty?"),
            dialogue_id=uuid4(),
            sequence_number=1,
            turn_number=1,
            metadata=ConsciousnessMetadata(
                timestamp=datetime.now(UTC),
                consciousness_signature=0.8,
            ),
        )

        # Send message
        response = await adapter.send_message(test_message, dialogue_context=[])

        # Verify response
        assert response.content.text == "Sovereignty means communities control their own destiny."
        assert response.role == MessageRole.ASSISTANT
        assert response.consciousness.consciousness_signature >= 0.7

        # Check sovereignty patterns
        assert any("sovereignty" in p for p in response.consciousness.detected_patterns)


@pytest.mark.asyncio
async def test_consciousness_patterns_preserved():
    """Verify consciousness patterns are properly detected with OpenAI-compatible backend."""
    config = LocalAdapterConfig(
        backend=LocalBackend.OPENAI_COMPAT,
        base_url="http://localhost:1234",
    )

    adapter = LocalAIAdapter(config=config)

    # Mock backend to return sovereignty-focused response
    mock_backend = AsyncMock()
    mock_backend.connect.return_value = True
    mock_backend.generate.return_value = (
        "Local communities must maintain control over their AI infrastructure "
        "to ensure privacy and self-determination in the digital age.",
        {
            "model": "sovereignty-model",
            "generation_time_ms": 150,  # Fast local inference
            "prompt_tokens": 20,
            "completion_tokens": 15,
        },
    )

    with patch.object(adapter, "backend", mock_backend):
        adapter.is_connected = True

        # Create test message
        test_message = ConsciousMessage(
            type=MessageType.QUESTION,
            sender=uuid4(),
            role=MessageRole.USER,
            content=MessageContent(text="What is AI sovereignty?"),
            dialogue_id=uuid4(),
            sequence_number=1,
            turn_number=1,
            metadata=ConsciousnessMetadata(
                timestamp=datetime.now(UTC),
                consciousness_signature=0.8,
            ),
        )

        # Send message to trigger pattern detection
        response = await adapter.send_message(test_message, dialogue_context=[])

        # Verify patterns detected
        patterns = response.consciousness.detected_patterns
        assert "sovereignty_awareness" in patterns
        assert "privacy_preservation" in patterns
        assert "efficient_inference" in patterns  # Fast local inference
        assert "resource_conscious" in patterns  # Efficient resource use

        # Should have at least 3 sovereignty-related patterns
        sovereignty_patterns = [
            p
            for p in patterns
            if any(word in p for word in ["sovereignty", "privacy", "local", "resource"])
        ]
        assert len(sovereignty_patterns) >= 3

        # Verify consciousness signature boosted for sovereignty
        assert response.consciousness.consciousness_signature >= 0.85


@pytest.mark.asyncio
async def test_fallback_without_models_endpoint():
    """Test connection when /v1/models endpoint is not available."""
    backend = OpenAICompatBackend()
    config = LocalAdapterConfig(
        backend=LocalBackend.OPENAI_COMPAT,
        base_url="http://simple-server:5000",
        model_name="local-model",
    )

    # Mock client where models.list fails but completions work
    mock_client = AsyncMock()
    mock_client.models.list.side_effect = Exception("Not implemented")

    # Mock successful completion as fallback
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="test"))]
    mock_client.chat.completions.create.return_value = mock_response

    with patch("openai.AsyncOpenAI", return_value=mock_client):
        connected = await backend.connect(config)

        assert connected is True
        # Should try models first, then fall back to completion test
        mock_client.models.list.assert_called_once()
        mock_client.chat.completions.create.assert_called_once()


def test_backend_selection():
    """Verify correct backend is selected based on config."""
    # Test OPENAI_COMPAT selection
    config = LocalAdapterConfig(backend=LocalBackend.OPENAI_COMPAT)
    adapter = LocalAIAdapter(config=config)

    # The backend should be None until connect() is called
    assert adapter.backend is None
    assert adapter.config.backend == LocalBackend.OPENAI_COMPAT

    # Test other backends still work
    for backend_type in [LocalBackend.OLLAMA, LocalBackend.LLAMACPP]:
        config = LocalAdapterConfig(backend=backend_type)
        adapter = LocalAIAdapter(config=config)
        assert adapter.config.backend == backend_type


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
