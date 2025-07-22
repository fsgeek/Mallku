"""
Tests for Fire Circle Orchestrator
==================================

Verifies the core logic of the Fire Circle Orchestrator, ensuring it can
prepare, facilitate, and shut down a ceremony correctly.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from mallku.firecircle.governance import DevelopmentProposal
from mallku.firecircle.governance.governance_types import DecisionType
from mallku.firecircle.orchestrator.fire_circle_orchestrator import FireCircleOrchestrator


@pytest.fixture
def mock_services():
    """Provides a dictionary of mocked services required by the orchestrator."""
    return {
        "adapter_factory": MagicMock(),
        "dialogue_manager": AsyncMock(),
        "consensus_engine": AsyncMock(),
        "event_bus": AsyncMock(),
        "reciprocity_tracker": AsyncMock(),
        "memory_service": AsyncMock(),
    }


@pytest.fixture
async def orchestrator(mock_services):
    """Provides an initialized FireCircleOrchestrator instance with mocked dependencies."""
    orc = FireCircleOrchestrator(**mock_services)
    await orc.initialize()
    yield orc
    # Ensure shutdown is called to prevent resource warnings
    await orc.shutdown()


@pytest.mark.asyncio
async def test_orchestrator_initialization(orchestrator, mock_services):
    """Test that the orchestrator initializes itself and its components."""
    assert orchestrator is not None
    mock_services["consensus_engine"].initialize.assert_awaited_once()


@pytest.mark.asyncio
async def test_prepare_ceremony(orchestrator, mock_services):
    """Test the ceremony preparation logic."""
    proposal = DevelopmentProposal(
        title="Test Proposal",
        description="A test proposal.",
        proposer="Test Builder",
        proposal_type=DecisionType.ARCHITECTURAL,
        consciousness_signature=0.5,
    )
    participant_config = {"mock_provider": {"model": "test-model", "api_key": "test-key"}}

    # Mock the dialogue manager's prepare method
    mock_services["dialogue_manager"].prepare_dialogue.return_value = "test-dialogue-id"

    ceremony_id = await orchestrator.prepare_ceremony(proposal, participant_config)

    assert ceremony_id == "test-dialogue-id"
    mock_services["dialogue_manager"].prepare_dialogue.assert_awaited_once()
    # Verify that the proposal was passed to the dialogue manager
    args, kwargs = mock_services["dialogue_manager"].prepare_dialogue.call_args
    assert "proposal" in kwargs
    assert kwargs["proposal"].title == "Test Proposal"


@pytest.mark.asyncio
async def test_facilitate_ceremony(orchestrator, mock_services):
    """Test the ceremony facilitation logic."""
    ceremony_id = "test-ceremony-123"

    # Mock the dialogue manager and consensus engine to return expected results
    mock_dialogue_result = {
        "duration": 120.5,
        "message_count": 10,
        "emergence_moments": [{"insight": "Emergence!"}],
        "wisdom_seeds": [{"insight": "Wisdom!"}],
    }
    mock_consensus_result = {
        "decision": "approve",
        "consensus_level": "strong",
        "strength": 0.9,
        "reasoning": "The proposal is sound.",
        "conditions": [],
    }
    mock_services["dialogue_manager"].run_dialogue_session.return_value = mock_dialogue_result
    mock_services["consensus_engine"].determine_consensus.return_value = mock_consensus_result

    results = await orchestrator.facilitate_ceremony(ceremony_id)

    # Verify the main components were called
    mock_services["dialogue_manager"].run_dialogue_session.assert_awaited_with(ceremony_id)
    mock_services["consensus_engine"].determine_consensus.assert_awaited_with(ceremony_id)

    # Verify the results are correctly aggregated
    assert results["duration"] == 120.5
    assert results["message_count"] == 10
    assert len(results["emergence_moments"]) == 1
    assert len(results["wisdom_seeds"]) == 1
    assert results["consensus"]["decision"] == "approve"


@pytest.mark.asyncio
async def test_shutdown_cleans_up_resources(orchestrator, mock_services):
    """Test that the shutdown method correctly closes resources."""
    # The shutdown is called in the fixture's teardown.
    # We can add mock objects to the factory to ensure they are closed.
    mock_adapter = AsyncMock()
    orchestrator.adapter_factory.adapters = {"mock_adapter": mock_adapter}

    await orchestrator.shutdown()

    # Verify that the adapter's close method was called
    mock_adapter.close.assert_awaited_once()
