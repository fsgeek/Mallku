"""
Tests for Ceremony Replay System

These tests ensure the replay engine correctly handles failed ceremonies
and provides recovery capabilities.

Created by: 69th Guardian
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import yaml

from mallku.orchestration.loom.ceremony_replay import (
    CeremonyReplayEngine,
    ReplayMode,
    ReplayResult,
)
from mallku.orchestration.loom.khipu_parser import CeremonyStatus, TaskStatus


@pytest.fixture
def temp_ceremonies_dir(tmp_path):
    """Create temporary ceremonies directory"""
    ceremonies_dir = tmp_path / "ceremonies"
    ceremonies_dir.mkdir()
    return ceremonies_dir


@pytest.fixture
def sample_failed_khipu(temp_ceremonies_dir):
    """Create a sample failed ceremony khipu"""
    content = """---
ceremony_id: test-ceremony-001
master_weaver: test-guardian
initiated: 2025-08-09T10:00:00Z
status: FAILED
completion_time: 2025-08-09T10:30:00Z
template: Bug Healing Ceremony
template_version: 1.0.0
sacred_purpose: healing
---

# Loom Ceremony: Test Ceremony

## Sacred Intention
Test ceremony for replay

## Shared Knowledge
### Key Artifacts
- test.py

## Task Manifest
Total Tasks: 3
Completed: 1
Failed: 2

| ID | Task | Status | Assignee | Priority |
|----|------|--------|----------|----------|
| T001 | First task | COMPLETE | app-001 | HIGH |
| T002 | Second task | FAILED | app-002 | HIGH |
| T003 | Third task | FAILED | - | MEDIUM |

## Tasks

### T001: First task
*Status: COMPLETE*
*Priority: HIGH*
*Assigned to: app-001*
*Started: 2025-08-09T10:05:00Z*
*Completed: 2025-08-09T10:10:00Z*

#### Description
First task description

#### Output
```
Task completed successfully
```

---

### T002: Second task
*Status: FAILED*
*Priority: HIGH*
*Assigned to: app-002*
*Started: 2025-08-09T10:10:00Z*
*Completed: 2025-08-09T10:20:00Z*

#### Description
Second task description

#### Output
```
Error: timeout exceeded
```

---

### T003: Third task
*Status: FAILED*
*Priority: MEDIUM*
*Assigned to: unassigned*
*Started: -*
*Completed: -*

#### Description
Third task description

#### Output
```
[Waiting for apprentice]
```

---

## Synthesis Space
### Emerging Patterns
- Timeout issues

## Ceremony Log
- 2025-08-09T10:00:00Z - Ceremony initiated
"""

    khipu_path = temp_ceremonies_dir / "2025-08-09_10-00-00_test-ceremony-001.md"
    khipu_path.write_text(content)
    return khipu_path


@pytest.fixture
async def replay_engine(temp_ceremonies_dir):
    """Create replay engine with temp directory"""
    return CeremonyReplayEngine(ceremonies_dir=temp_ceremonies_dir)


@pytest.mark.asyncio
async def test_analyze_ceremony(replay_engine, sample_failed_khipu):
    """Test ceremony analysis"""
    context = await replay_engine.analyze_ceremony("test-ceremony-001")

    assert context is not None
    assert context.original_ceremony_id == "test-ceremony-001"
    assert context.original_status == CeremonyStatus.FAILED
    assert len(context.failed_tasks) == 2
    assert len(context.completed_tasks) == 1
    assert context.mode == ReplayMode.RESUME
    assert context.tasks_to_replay == ["T002", "T003"]
    assert "timeout" in context.replay_reason.lower()


@pytest.mark.asyncio
async def test_analyze_nonexistent_ceremony(replay_engine):
    """Test analyzing non-existent ceremony"""
    context = await replay_engine.analyze_ceremony("nonexistent-ceremony")
    assert context is None


@pytest.mark.asyncio
async def test_create_replay_khipu(replay_engine, sample_failed_khipu):
    """Test replay khipu creation"""
    context = await replay_engine.analyze_ceremony("test-ceremony-001")

    replay_path = await replay_engine._create_replay_khipu(context, debug_level=0)

    assert replay_path.exists()
    assert "replay_test-ceremony-001" in replay_path.name

    # Verify content
    content = replay_path.read_text()
    assert "---" in content

    # Parse YAML header
    parts = content.split("---", 2)
    header = yaml.safe_load(parts[1])

    assert header["ceremony_id"] == context.replay_ceremony_id
    assert header["master_weaver"] == "replay-engine"
    assert header["status"] == "PREPARING"
    assert header["x-replay-original"] == "test-ceremony-001"
    assert header["x-replay-mode"] == "RESUME"
    assert header["sacred_purpose"] == "healing"


@pytest.mark.asyncio
async def test_replay_modes(replay_engine, sample_failed_khipu):
    """Test different replay modes"""
    # Test RESUME mode (default for failed)
    context = await replay_engine.analyze_ceremony("test-ceremony-001")
    assert context.mode == ReplayMode.RESUME
    assert context.tasks_to_replay == ["T002", "T003"]

    # Test RESTART mode
    context.mode = ReplayMode.RESTART
    context.tasks_to_replay = ["T001", "T002", "T003"]

    # Test SELECTIVE mode
    context.mode = ReplayMode.SELECTIVE
    context.tasks_to_replay = ["T002"]

    # Test DEBUG mode
    context.mode = ReplayMode.DEBUG
    assert context.mode == ReplayMode.DEBUG


@pytest.mark.asyncio
async def test_suggest_replay_strategy(replay_engine, sample_failed_khipu):
    """Test replay strategy suggestions"""
    strategy = await replay_engine.suggest_replay_strategy("test-ceremony-001")

    assert strategy["ceremony_id"] == "test-ceremony-001"
    assert strategy["current_status"] == "FAILED"
    assert strategy["suggested_mode"] == "RESUME"
    assert len(strategy["tasks_to_replay"]) == 2
    assert strategy["expected_success_rate"] == 0.8  # Timeout failures
    assert len(strategy["recommendations"]) > 0
    assert any("timeout" in rec.lower() for rec in strategy["recommendations"])


@pytest.mark.asyncio
async def test_replay_ceremony_mock(replay_engine, sample_failed_khipu):
    """Test replay ceremony with mocked Loom"""
    context = await replay_engine.analyze_ceremony("test-ceremony-001")

    # Simple test that verifies the replay khipu is created and basic flow works
    with patch("mallku.orchestration.loom.ceremony_replay.TheLoom") as MockLoom:
        mock_loom = AsyncMock()
        MockLoom.return_value = mock_loom

        # Create a simple session that will report tasks as complete
        mock_session = MagicMock()
        mock_session.status = CeremonyStatus.COMPLETE
        mock_session.tasks = {}

        # Add tasks that will be tracked
        for task_id in ["T002", "T003"]:
            mock_task = MagicMock()
            mock_task.status = TaskStatus.COMPLETE
            mock_session.tasks[task_id] = mock_task

        mock_loom._load_ceremony_session = AsyncMock(return_value=mock_session)
        mock_loom._update_session_from_khipu = AsyncMock()
        mock_loom.start = AsyncMock()
        mock_loom.stop = AsyncMock()

        result = await replay_engine.replay_ceremony(context)

        # Basic assertions - the full logic would need actual Loom integration
        assert result.replay_ceremony_id == context.replay_ceremony_id
        assert len(result.replayed_tasks) == 2
        # For this simple mock, tasks start as COMPLETE so no newly_completed
        assert result.duration > 0


@pytest.mark.asyncio
async def test_replay_with_custom_tasks(replay_engine, sample_failed_khipu):
    """Test selective task replay"""
    context = await replay_engine.analyze_ceremony("test-ceremony-001")

    with patch("mallku.orchestration.loom.ceremony_replay.TheLoom") as MockLoom:
        mock_loom = AsyncMock()
        MockLoom.return_value = mock_loom

        mock_session = MagicMock()
        mock_session.status = CeremonyStatus.COMPLETE
        mock_session.tasks = {
            "T002": MagicMock(status=TaskStatus.COMPLETE),
        }
        mock_loom._load_ceremony_session = AsyncMock(return_value=mock_session)
        mock_loom._update_session_from_khipu = AsyncMock()
        mock_loom.start = AsyncMock()
        mock_loom.stop = AsyncMock()

        # Replay only T002
        result = await replay_engine.replay_ceremony(context, custom_tasks=["T002"], debug_level=1)

        assert result.success is True
        assert result.replayed_tasks == ["T002"]
        assert context.mode == ReplayMode.SELECTIVE


@pytest.mark.asyncio
async def test_replay_history(replay_engine, sample_failed_khipu):
    """Test replay history tracking"""
    context = await replay_engine.analyze_ceremony("test-ceremony-001")

    # Initially no history
    history = await replay_engine.get_replay_history("test-ceremony-001")
    assert len(history) == 0

    # Add to history (happens during replay)
    replay_engine.replay_history["test-ceremony-001"] = [context]

    # Check history
    history = await replay_engine.get_replay_history("test-ceremony-001")
    assert len(history) == 1
    assert history[0] == context


@pytest.mark.asyncio
async def test_extract_insights(replay_engine, sample_failed_khipu):
    """Test insight extraction"""
    context = await replay_engine.analyze_ceremony("test-ceremony-001")

    # Mock session with mixed results
    mock_session = MagicMock()
    mock_session.tasks = {
        "T002": MagicMock(name="Second task", status=TaskStatus.COMPLETE),
        "T003": MagicMock(name="Third task", status=TaskStatus.FAILED),
    }

    insights = await replay_engine._extract_replay_insights(
        context, mock_session, ["T002"], ["T003"]
    )

    assert len(insights) > 0
    assert any("50.0%" in insight for insight in insights)  # Recovery rate
    assert any("Resume mode" in insight for insight in insights)


@pytest.mark.asyncio
async def test_convenience_functions():
    """Test convenience replay functions"""
    with patch("mallku.orchestration.loom.ceremony_replay.CeremonyReplayEngine") as MockEngine:
        mock_engine = AsyncMock()
        MockEngine.return_value = mock_engine

        mock_context = MagicMock()
        mock_engine.analyze_ceremony = AsyncMock(return_value=mock_context)
        mock_engine.replay_ceremony = AsyncMock(
            return_value=ReplayResult(
                success=True,
                replay_ceremony_id="replay-001",
                replayed_tasks=["T001"],
                newly_completed=["T001"],
                still_failed=[],
                insights=["Test insight"],
                duration=60.0,
            )
        )

        # Test replay_failed_ceremony
        from mallku.orchestration.loom.ceremony_replay import replay_failed_ceremony

        result = await replay_failed_ceremony("test-001")
        assert result.success is True
        mock_engine.analyze_ceremony.assert_called_once_with("test-001")

        # Test debug_ceremony
        from mallku.orchestration.loom.ceremony_replay import debug_ceremony

        result = await debug_ceremony("test-001", ["T001"])
        assert result.success is True
        assert mock_context.mode == ReplayMode.DEBUG
