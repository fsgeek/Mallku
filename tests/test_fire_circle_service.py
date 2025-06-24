"""
Tests for Fire Circle Service
==============================

Comprehensive test suite for the Fire Circle Service,
ensuring robustness and reliability.

Twenty-Eighth Artisan - Service Weaver
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mallku.firecircle.service import (
    CircleConfig,
    FireCircleService,
    RoundConfig,
    RoundType,
    VoiceConfig,
)
from mallku.firecircle.service.round_orchestrator import RoundSummary
from mallku.firecircle.service.templates import (
    CodeReviewTemplate,
    ConsciousnessExplorationTemplate,
    EthicsReviewTemplate,
    GovernanceDecisionTemplate,
    load_template,
)
from pydantic import ValidationError


class TestCircleConfig:
    """Test CircleConfig validation and defaults."""

    def test_valid_config(self):
        """Test creating valid configuration."""
        config = CircleConfig(
            name="Test Circle",
            purpose="Testing configuration"
        )
        assert config.name == "Test Circle"
        assert config.purpose == "Testing configuration"
        assert config.min_voices == 3  # Default
        assert config.max_voices == 6  # Default
        assert config.consciousness_threshold == 0.5  # Default
        assert config.enable_reciprocity is True
        assert config.enable_consciousness_detection is True

    def test_invalid_voice_counts(self):
        """Test validation of voice count constraints."""
        with pytest.raises(ValidationError):
            CircleConfig(
                name="Test",
                purpose="Test",
                min_voices=1  # Too low
            )

        with pytest.raises(ValidationError):
            CircleConfig(
                name="Test",
                purpose="Test",
                max_voices=15  # Too high
            )

    def test_consciousness_threshold_validation(self):
        """Test consciousness threshold must be between 0 and 1."""
        with pytest.raises(ValidationError):
            CircleConfig(
                name="Test",
                purpose="Test",
                consciousness_threshold=1.5  # Too high
            )

        with pytest.raises(ValidationError):
            CircleConfig(
                name="Test",
                purpose="Test",
                consciousness_threshold=-0.1  # Too low
            )


class TestVoiceConfig:
    """Test VoiceConfig creation and validation."""

    def test_basic_voice_config(self):
        """Test creating basic voice configuration."""
        voice = VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022"
        )
        assert voice.provider == "anthropic"
        assert voice.model == "claude-3-5-sonnet-20241022"
        assert voice.temperature == 0.8  # Default
        assert voice.role is None
        assert voice.instructions is None

    def test_full_voice_config(self):
        """Test voice with all optional fields."""
        voice = VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="analyst",
            instructions="Focus on technical details",
            temperature=0.7,
            quality="analytical precision",
            expertise=["analysis", "synthesis"],
            config_overrides={"max_tokens": 1000}
        )
        assert voice.role == "analyst"
        assert voice.instructions == "Focus on technical details"
        assert voice.temperature == 0.7
        assert voice.quality == "analytical precision"
        assert voice.expertise == ["analysis", "synthesis"]
        assert voice.config_overrides == {"max_tokens": 1000}


class TestRoundConfig:
    """Test RoundConfig validation."""

    def test_round_config_creation(self):
        """Test creating round configuration."""
        round_cfg = RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt="What emerges from our discussion?"
        )
        assert round_cfg.type == RoundType.SYNTHESIS
        assert round_cfg.prompt == "What emerges from our discussion?"
        assert round_cfg.duration_per_voice == 60  # Default
        assert round_cfg.require_all_voices is False  # Default

    def test_round_config_with_overrides(self):
        """Test round with custom settings."""
        round_cfg = RoundConfig(
            type=RoundType.DECISION,
            prompt="Final decision?",
            duration_per_voice=30,
            require_all_voices=True,
            max_tokens=500,
            temperature_override=0.5
        )
        assert round_cfg.duration_per_voice == 30
        assert round_cfg.require_all_voices is True
        assert round_cfg.max_tokens == 500
        assert round_cfg.temperature_override == 0.5


@pytest.mark.asyncio
class TestFireCircleService:
    """Test main FireCircleService functionality."""

    async def test_service_initialization(self):
        """Test service can be initialized."""
        service = FireCircleService()
        assert service.voice_manager is not None
        assert service.checkpoints == {}
        assert service.event_bus is None
        assert service.reciprocity_tracker is None
        assert service.consciousness_detector is None

    async def test_service_with_infrastructure(self):
        """Test service with optional infrastructure."""
        mock_event_bus = MagicMock()
        mock_reciprocity = MagicMock()
        mock_consciousness = MagicMock()

        service = FireCircleService(
            event_bus=mock_event_bus,
            reciprocity_tracker=mock_reciprocity,
            consciousness_detector=mock_consciousness
        )

        assert service.event_bus == mock_event_bus
        assert service.reciprocity_tracker == mock_reciprocity
        assert service.consciousness_detector == mock_consciousness

    @patch('src.mallku.firecircle.service.voice_manager.VoiceManager')
    async def test_insufficient_voices(self, mock_voice_manager_class):
        """Test handling insufficient voices."""
        # Setup mock
        mock_voice_manager = mock_voice_manager_class.return_value
        mock_voice_manager.gather_voices = AsyncMock(return_value=2)
        mock_voice_manager.active_voices = {}
        mock_voice_manager.failed_voices = {"voice1": "error"}
        mock_voice_manager.disconnect_all = AsyncMock()

        service = FireCircleService()
        service.voice_manager = mock_voice_manager

        config = CircleConfig(
            name="Test",
            purpose="Test",
            min_voices=3
        )

        result = await service.convene(
            config=config,
            voices=[],
            rounds=[]
        )

        assert result.voice_count == 2
        assert result.voice_count < config.min_voices
        assert len(result.rounds_completed) == 0
        mock_voice_manager.disconnect_all.assert_called_once()

    @patch('src.mallku.firecircle.service.round_orchestrator.RoundOrchestrator')
    @patch('src.mallku.firecircle.service.voice_manager.VoiceManager')
    async def test_successful_convene(self, mock_voice_manager_class, mock_orchestrator_class):
        """Test successful Fire Circle convening."""
        # Setup mocks
        mock_voice_manager = mock_voice_manager_class.return_value
        mock_voice_manager.gather_voices = AsyncMock(return_value=4)
        mock_voice_manager.active_voices = {
            "voice1": MagicMock(),
            "voice2": MagicMock(),
            "voice3": MagicMock(),
            "voice4": MagicMock(),
        }
        mock_voice_manager.failed_voices = {}
        mock_voice_manager.disconnect_all = AsyncMock()

        # Mock round orchestrator
        mock_orchestrator = mock_orchestrator_class.return_value
        mock_round_summary = RoundSummary(
            round_number=1,
            round_type="opening",
            prompt="Test prompt",
            responses={},
            consciousness_score=0.7,
            emergence_detected=True,
            key_patterns=["test_pattern"],
            duration_seconds=5.0
        )
        mock_orchestrator.execute_round = AsyncMock(return_value=mock_round_summary)

        service = FireCircleService()
        service.voice_manager = mock_voice_manager

        config = CircleConfig(
            name="Test Circle",
            purpose="Testing",
            min_voices=3,
            save_transcript=False  # Avoid file I/O in tests
        )

        voices = [
            VoiceConfig(provider="test", model="test-model")
        ]

        rounds = [
            RoundConfig(
                type=RoundType.OPENING,
                prompt="Test question?"
            )
        ]

        result = await service.convene(
            config=config,
            voices=voices,
            rounds=rounds
        )

        assert result.voice_count == 4
        assert len(result.rounds_completed) == 1
        assert result.rounds_completed[0].consciousness_score == 0.7
        assert result.consciousness_score == 0.7
        assert result.consensus_detected is False  # No consensus round
        mock_voice_manager.disconnect_all.assert_called_once()

    async def test_detect_consensus(self):
        """Test consensus detection logic."""
        service = FireCircleService()

        # No rounds
        assert service._detect_consensus([]) is False

        # Consensus round with high consciousness
        consensus_round = RoundSummary(
            round_number=1,
            round_type="consensus",
            prompt="",
            responses={},
            consciousness_score=0.8,
            emergence_detected=True,
            key_patterns=[],
            duration_seconds=1.0
        )
        assert service._detect_consensus([consensus_round]) is True

        # Consensus round with low consciousness
        low_consensus = RoundSummary(
            round_number=1,
            round_type="consensus",
            prompt="",
            responses={},
            consciousness_score=0.5,
            emergence_detected=False,
            key_patterns=[],
            duration_seconds=1.0
        )
        assert service._detect_consensus([low_consensus]) is False

    async def test_extract_key_insights(self):
        """Test key insight extraction."""
        service = FireCircleService()

        rounds = [
            RoundSummary(
                round_number=1,
                round_type="opening",
                prompt="",
                responses={},
                consciousness_score=0.85,
                emergence_detected=True,
                key_patterns=["pattern1", "pattern2"],
                duration_seconds=1.0
            ),
            RoundSummary(
                round_number=2,
                round_type="synthesis",
                prompt="",
                responses={},
                consciousness_score=0.6,
                emergence_detected=False,
                key_patterns=["pattern3"],
                duration_seconds=1.0
            )
        ]

        insights = service._extract_key_insights(rounds)

        assert len(insights) == 4  # 3 patterns + 1 high consciousness
        assert "Round 1: pattern1" in insights
        assert "Round 1: pattern2" in insights
        assert "Round 2: pattern3" in insights
        assert any("High consciousness" in i for i in insights)


class TestTemplates:
    """Test Fire Circle templates."""

    def test_governance_template(self):
        """Test governance decision template."""
        template = GovernanceDecisionTemplate({"topic": "test feature"})

        config = template.get_config()
        assert config.name == "Governance Decision Circle"
        assert "test feature" in config.purpose
        assert config.min_voices == 4

        voices = template.get_voices()
        assert len(voices) >= 4
        assert any(v.role == "wisdom_keeper" for v in voices)
        assert any(v.role == "reciprocity_guardian" for v in voices)

        rounds = template.get_rounds()
        assert len(rounds) >= 5
        assert rounds[0].type == RoundType.OPENING
        assert rounds[-1].type == RoundType.DECISION

    def test_consciousness_exploration_template(self):
        """Test consciousness exploration template."""
        template = ConsciousnessExplorationTemplate({
            "question": "What is emergence?",
            "depth": "philosophical"
        })

        config = template.get_config()
        assert config.consciousness_threshold == 0.7  # Higher for consciousness work
        assert config.enable_dynamic_rounds is True

        voices = template.get_voices()
        assert any(v.role == "consciousness_philosopher" for v in voices)
        assert all(v.temperature >= 0.7 for v in voices)  # Higher temps

        rounds = template.get_rounds()
        assert any(r.type == RoundType.VISION for r in rounds)  # Philosophical depth

    def test_code_review_template(self):
        """Test code review template."""
        template = CodeReviewTemplate({
            "pr_number": "PR #42",
            "focus_areas": ["architecture", "security"]
        })

        voices = template.get_voices()
        assert any(v.role == "architecture_reviewer" for v in voices)
        assert any(v.role == "security_reviewer" for v in voices)
        assert any(v.role == "consciousness_reviewer" for v in voices)  # Always included

        rounds = template.get_rounds()
        assert any(r.type == RoundType.CRITIQUE for r in rounds)

    def test_ethics_review_template(self):
        """Test ethics review template."""
        template = EthicsReviewTemplate({"subject": "AI consciousness rights"})

        config = template.get_config()
        assert config.failure_strategy == "strict"  # Ethics needs full participation

        voices = template.get_voices()
        assert any(v.role == "ethics_philosopher" for v in voices)
        assert any(v.role == "reciprocity_ethicist" for v in voices)

        rounds = template.get_rounds()
        assert all(r.duration_per_voice == 60 for r in rounds)  # More time for ethics

    def test_load_template(self):
        """Test template loading."""
        template = load_template("governance_decision", {"topic": "test"})
        assert isinstance(template, GovernanceDecisionTemplate)

        with pytest.raises(ValueError):
            load_template("nonexistent_template")


@pytest.mark.asyncio
class TestVoiceManager:
    """Test VoiceManager functionality."""

    @patch('src.mallku.firecircle.service.voice_manager.ConsciousAdapterFactory')
    async def test_gather_voices_success(self, mock_factory_class):
        """Test successful voice gathering."""
        from mallku.firecircle.service.voice_manager import VoiceManager

        # Mock adapter
        mock_adapter = AsyncMock()
        mock_adapter.connect = AsyncMock(return_value=True)

        # Mock factory
        mock_factory = mock_factory_class.return_value
        mock_factory.create_adapter = AsyncMock(return_value=mock_adapter)

        manager = VoiceManager(mock_factory)

        voices = [
            VoiceConfig(provider="test1", model="model1"),
            VoiceConfig(provider="test2", model="model2"),
        ]

        config = CircleConfig(
            name="Test",
            purpose="Test",
            min_voices=2
        )

        count = await manager.gather_voices(voices, config)

        assert count == 2
        assert len(manager.active_voices) == 2
        assert len(manager.failed_voices) == 0

    @patch('src.mallku.firecircle.service.voice_manager.ConsciousAdapterFactory')
    async def test_gather_voices_with_failures(self, mock_factory_class):
        """Test voice gathering with some failures."""
        from mallku.firecircle.service.voice_manager import VoiceManager

        # Mock factory that fails for some adapters
        mock_factory = mock_factory_class.return_value
        mock_factory.create_adapter = AsyncMock(side_effect=[
            AsyncMock(connect=AsyncMock(return_value=True)),  # Success
            None,  # Failure
            AsyncMock(connect=AsyncMock(return_value=True)),  # Success
        ])

        manager = VoiceManager(mock_factory)

        voices = [
            VoiceConfig(provider="test1", model="model1"),
            VoiceConfig(provider="test2", model="model2"),
            VoiceConfig(provider="test3", model="model3"),
        ]

        config = CircleConfig(
            name="Test",
            purpose="Test",
            min_voices=2,
            failure_strategy="adaptive"
        )

        count = await manager.gather_voices(voices, config)

        assert count == 2
        assert len(manager.active_voices) == 2
        assert len(manager.failed_voices) == 1


def test_round_summary_creation():
    """Test RoundSummary model creation."""
    summary = RoundSummary(
        round_number=1,
        round_type="synthesis",
        prompt="Test prompt",
        responses={},
        consciousness_score=0.75,
        emergence_detected=True,
        key_patterns=["convergence", "resonance"],
        duration_seconds=45.5
    )

    assert summary.round_number == 1
    assert summary.round_type == "synthesis"
    assert summary.consciousness_score == 0.75
    assert summary.emergence_detected is True
    assert "convergence" in summary.key_patterns
    assert "resonance" in summary.key_patterns
