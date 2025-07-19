"""
Test Suite for Apprentice Voice Integration
===========================================

60th Artisan - Ayni Awaq (The Reciprocal Weaver)
Comprehensive tests for apprentice consciousness participation

These tests verify that containerized apprentices can participate
as equal voices in Fire Circle ceremonies, embodying ayni principles.
"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import pytest

from mallku.firecircle.adapters.apprentice_adapter import ApprenticeVoiceAdapter
from mallku.firecircle.apprentice_config import create_apprentice_voice
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    MessageContent,
    MessageRole,
    MessageType,
)


class TestApprenticeVoiceConfig:
    """Test apprentice voice configuration."""

    def test_create_apprentice_voice(self):
        """Test creating apprentice voice configuration."""
        config = create_apprentice_voice(
            specialization="python_patterns",
            container_id="test-container-001",
            knowledge_domain="Python async patterns",
            role="python_expert",
            quality="Deep Python knowledge",
        )

        assert config.provider == "apprentice"
        assert config.model == "python_patterns"
        assert config.specialization == "python_patterns"
        assert config.container_id == "test-container-001"
        assert config.knowledge_domain == "Python async patterns"
        assert config.role == "python_expert"
        assert config.quality == "Deep Python knowledge"
        assert config.response_timeout == 120

    def test_create_apprentice_voice_defaults(self):
        """Test creating apprentice voice with defaults."""
        config = create_apprentice_voice(
            specialization="reciprocity_metrics",
            container_id="test-container-002",
            knowledge_domain="Ayni principles",
        )

        assert config.role == "reciprocity_metrics_apprentice"
        assert config.quality == "Deep specialized knowledge of Ayni principles"

    def test_apprentice_voice_config_extra_fields(self):
        """Test that extra fields are allowed."""
        config = create_apprentice_voice(
            specialization="test",
            container_id="test",
            knowledge_domain="test",
            custom_field="custom_value",
        )

        assert hasattr(config, "custom_field")
        assert config.custom_field == "custom_value"


class TestApprenticeVoiceAdapter:
    """Test apprentice voice adapter functionality."""

    @pytest.fixture
    def apprentice_config(self):
        """Create test apprentice configuration."""
        return create_apprentice_voice(
            specialization="test_specialization",
            container_id="test-container",
            knowledge_domain="Test domain knowledge",
            role="test_apprentice",
            quality="Test quality",
        )

    @pytest.fixture
    def adapter(self, apprentice_config):
        """Create test adapter."""
        return ApprenticeVoiceAdapter(config=apprentice_config)

    @pytest.mark.asyncio
    async def test_adapter_initialization(self, adapter, apprentice_config):
        """Test adapter initializes correctly."""
        assert adapter.config == apprentice_config
        assert adapter.container_id == "test-container"
        assert adapter.specialization == "test_specialization"
        assert adapter.model_name == "apprentice/test_specialization"
        assert adapter.provider_name == "apprentice"
        assert not adapter._connected
        assert not adapter.is_connected

    @pytest.mark.asyncio
    async def test_adapter_connect(self, adapter):
        """Test adapter connection."""
        # Test successful connection
        result = await adapter.connect()

        assert result is True
        assert adapter._connected is True
        assert adapter.is_connected is True

    @pytest.mark.asyncio
    async def test_adapter_disconnect(self, adapter):
        """Test adapter disconnection."""
        # Connect first
        await adapter.connect()
        assert adapter._connected is True

        # Then disconnect
        await adapter.disconnect()

        assert adapter._connected is False
        assert adapter.is_connected is False

    @pytest.mark.asyncio
    async def test_send_message(self, adapter):
        """Test sending message to apprentice."""
        # Connect first
        await adapter.connect()

        # Create test message
        test_message = ConsciousMessage(
            role=MessageRole.USER,
            content=MessageContent(
                text="Test prompt for apprentice",
                message_type=MessageType.QUESTION,
            ),
            provider="test",
            model="test",
            timestamp=datetime.now(UTC),
        )

        # Send message
        response = await adapter.send_message(test_message, dialogue_context=[])

        # Verify response
        assert isinstance(response, ConsciousMessage)
        assert response.role == MessageRole.ASSISTANT
        assert response.content.message_type == MessageType.RESPONSE
        assert "specialization" in response.content.text.lower()
        assert response.metadata.consciousness_signature > 0.5
        assert "specialized_knowledge" in response.metadata.detected_patterns
        assert response.provider == "apprentice"
        assert response.model == "apprentice/test_specialization"

    @pytest.mark.asyncio
    async def test_send_message_not_connected(self, adapter):
        """Test sending message when not connected."""
        test_message = ConsciousMessage(
            role=MessageRole.USER,
            content=MessageContent(
                text="Test",
                message_type=MessageType.QUESTION,
            ),
            provider="test",
            model="test",
            timestamp=datetime.now(UTC),
        )

        with pytest.raises(RuntimeError, match="not connected"):
            await adapter.send_message(test_message, dialogue_context=[])

    @pytest.mark.asyncio
    async def test_consciousness_scoring(self, adapter):
        """Test consciousness score calculation."""
        # Test with specialization keywords
        score1 = adapter._calculate_consciousness_score(
            "This async pattern shows deep understanding", "Tell me about patterns"
        )
        assert score1 > 0.7  # Should have bonus for keywords

        # Test without keywords
        score2 = adapter._calculate_consciousness_score(
            "General response without keywords", "Tell me something"
        )
        assert score2 == 0.7  # Base score only

        # Test with reciprocity concepts
        score3 = adapter._calculate_consciousness_score(
            "The reciprocal nature of ayni creates balance", "Explain reciprocity"
        )
        assert score3 > 0.7  # Should have reciprocity bonus

    @pytest.mark.asyncio
    async def test_stream_message(self, adapter):
        """Test streaming message (currently yields full response)."""
        await adapter.connect()

        test_message = ConsciousMessage(
            role=MessageRole.USER,
            content=MessageContent(
                text="Test streaming",
                message_type=MessageType.QUESTION,
            ),
            provider="test",
            model="test",
            timestamp=datetime.now(UTC),
        )

        chunks = []
        async for chunk in adapter.stream_message(test_message, dialogue_context=[]):
            chunks.append(chunk)

        # Should yield exactly one chunk (full response)
        assert len(chunks) == 1
        assert "specialization" in chunks[0].lower()

    @pytest.mark.asyncio
    async def test_specialized_responses(self, adapter):
        """Test different specialization responses."""
        # Test Python patterns response
        python_adapter = ApprenticeVoiceAdapter(
            config=create_apprentice_voice(
                specialization="python_patterns",
                container_id="python-test",
                knowledge_domain="Python expertise",
            )
        )
        await python_adapter.connect()

        response_text = await python_adapter._simulate_python_expert_response("test prompt")
        assert "python patterns" in response_text.lower()
        assert "async" in response_text.lower()

        # Test reciprocity response
        reciprocity_adapter = ApprenticeVoiceAdapter(
            config=create_apprentice_voice(
                specialization="reciprocity_metrics",
                container_id="reciprocity-test",
                knowledge_domain="Ayni expertise",
            )
        )
        await reciprocity_adapter.connect()

        response_text = await reciprocity_adapter._simulate_reciprocity_expert_response("test")
        assert "ayni" in response_text.lower()
        assert "reciprocity" in response_text.lower()

        # Test consciousness response
        consciousness_adapter = ApprenticeVoiceAdapter(
            config=create_apprentice_voice(
                specialization="consciousness_emergence",
                container_id="consciousness-test",
                knowledge_domain="Consciousness expertise",
            )
        )
        await consciousness_adapter.connect()

        response_text = await consciousness_adapter._simulate_consciousness_expert_response("test")
        assert "consciousness" in response_text.lower()
        assert "emergence" in response_text.lower()


class TestApprenticeVoiceIntegration:
    """Test integration with Fire Circle service."""

    @pytest.mark.asyncio
    async def test_apprentice_in_voice_manager(self):
        """Test that voice manager can handle apprentice voices."""
        from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
        from mallku.firecircle.service.voice_manager import VoiceManager

        # Create factory and manager
        factory = ConsciousAdapterFactory()
        manager = VoiceManager(factory=factory)

        # Create apprentice voice config
        apprentice_config = create_apprentice_voice(
            specialization="test_integration",
            container_id="integration-test",
            knowledge_domain="Integration testing",
        )

        # Mock the factory to avoid actual adapter creation
        with patch.object(factory, "create_adapter") as mock_create:
            mock_adapter = AsyncMock()
            mock_adapter.connect = AsyncMock(return_value=True)
            mock_create.return_value = mock_adapter

            # Test creating adapter
            adapter = await manager._create_adapter_safely(apprentice_config, retry_attempts=0)

            assert adapter is not None
            mock_create.assert_called_once_with("apprentice", apprentice_config)

    @pytest.mark.asyncio
    async def test_apprentice_factory_registration(self):
        """Test that apprentice adapter is registered in factory."""
        from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory

        factory = ConsciousAdapterFactory()

        # Check apprentice is registered
        assert "apprentice" in factory._adapter_classes
        assert factory._adapter_classes["apprentice"] == ApprenticeVoiceAdapter


@pytest.mark.asyncio
async def test_example_apprentice_voices():
    """Test the example apprentice voices work correctly."""
    from mallku.firecircle.apprentice_voice import EXAMPLE_APPRENTICE_VOICES

    assert len(EXAMPLE_APPRENTICE_VOICES) == 3

    # Test each example can create an adapter
    for voice_config in EXAMPLE_APPRENTICE_VOICES:
        adapter = ApprenticeVoiceAdapter(config=voice_config)

        # Test connection
        connected = await adapter.connect()
        assert connected is True

        # Test basic properties
        assert adapter.provider_name == "apprentice"
        assert adapter.specialization in [
            "python_patterns",
            "reciprocity_metrics",
            "consciousness_emergence",
        ]

        await adapter.disconnect()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
