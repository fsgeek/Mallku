"""
Integration tests for the Weaver and Loom system.

These tests verify the basic functionality of the Loom orchestrator
without requiring actual Docker containers or MCP connections.
"""

import asyncio
import tempfile
from datetime import UTC, datetime
from pathlib import Path

import pytest

from mallku.orchestration.loom.the_loom import (
    CeremonyStatus,
    TaskStatus,
    TheLoom,
)


class TestLoomBasicFunctionality:
    """Test basic Loom functionality without external dependencies"""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files"""
        with tempfile.TemporaryDirectory() as td:
            yield Path(td)

    @pytest.mark.asyncio
    async def test_loom_initialization(self, temp_dir):
        """Test that Loom can be initialized properly"""
        loom = TheLoom(ceremonies_dir=temp_dir)

        assert loom.ceremonies_dir == temp_dir
        assert loom.max_concurrent_apprentices == 3
        assert loom.apprentice_timeout == 1800
        assert len(loom.active_sessions) == 0

    @pytest.mark.asyncio
    async def test_ceremony_initiation(self, temp_dir):
        """Test initiating a new ceremony"""
        loom = TheLoom(ceremonies_dir=temp_dir)

        # Define test tasks
        tasks = [
            {
                "id": "T001",
                "name": "Initialize System",
                "description": "Set up the test environment",
                "priority": "HIGH",
                "dependencies": [],
            },
            {
                "id": "T002",
                "name": "Process Data",
                "description": "Process test data",
                "priority": "MEDIUM",
                "dependencies": ["T001"],
            },
        ]

        # Initiate ceremony
        session = await loom.initiate_ceremony(
            ceremony_name="Test Ceremony",
            master_weaver="guardian-60",
            sacred_intention="Test the Loom system",
            tasks=tasks,
        )

        # Verify session
        assert session.ceremony_id in loom.active_sessions
        assert session.master_weaver == "guardian-60"
        assert session.status == CeremonyStatus.IN_PROGRESS
        assert len(session.tasks) == 2

        # Verify tasks
        assert "T001" in session.tasks
        assert session.tasks["T001"].name == "Initialize System"
        assert session.tasks["T001"].status == TaskStatus.PENDING
        assert session.tasks["T001"].priority == "HIGH"

        # Verify khipu was created
        assert session.khipu_path.exists()
        khipu_content = session.khipu_path.read_text()
        assert "Test Ceremony" in khipu_content
        assert "guardian-60" in khipu_content

    @pytest.mark.asyncio
    async def test_khipu_parsing(self, temp_dir):
        """Test parsing an existing khipu file"""
        loom = TheLoom(ceremonies_dir=temp_dir)

        # Create a khipu file manually
        khipu_path = temp_dir / "test_ceremony.md"
        khipu_content = """---
ceremony_id: test-ceremony-123
master_weaver: guardian-60
initiated: 2025-01-01T00:00:00Z
status: IN_PROGRESS
---

# Loom Ceremony: Test Ceremony
*Initiated: 2025-01-01T00:00:00Z*
*Master Weaver: guardian-60*
*Status: IN_PROGRESS*

## Sacred Intention
Test the Loom parsing functionality

## Sub-Tasks

### T001: First Task
*Status: PENDING*
*Priority: HIGH*
*Assigned: None*

**Description**: The first test task

---

### T002: Second Task
*Status: IN_PROGRESS*
*Priority: MEDIUM*
*Assigned: apprentice-1*
*Started: 2025-01-01T00:30:00Z*

**Description**: The second test task

**Output**:
Working on the task...
"""
        khipu_path.write_text(khipu_content)

        # Parse ceremony from khipu
        ceremony_data, tasks = await loom._parse_khipu_file(khipu_path)

        # Verify ceremony data
        assert ceremony_data["ceremony_id"] == "test-ceremony-123"
        assert ceremony_data["master_weaver"] == "guardian-60"
        assert ceremony_data["status"] == "IN_PROGRESS"

        # Verify tasks
        assert len(tasks) == 2
        assert tasks[0]["task_id"] == "T001"
        assert tasks[0]["status"] == TaskStatus.PENDING
        assert tasks[1]["task_id"] == "T002"
        assert tasks[1]["status"] == TaskStatus.IN_PROGRESS

    @pytest.mark.asyncio
    async def test_task_completion_tracking(self, temp_dir):
        """Test tracking task completion"""
        loom = TheLoom(ceremonies_dir=temp_dir)

        # Create ceremony with tasks
        tasks = [
            {"id": "T001", "name": "Task 1", "description": "First task"},
            {"id": "T002", "name": "Task 2", "description": "Second task"},
        ]

        session = await loom.initiate_ceremony(
            ceremony_name="Completion Test",
            master_weaver="guardian-60",
            sacred_intention="Test completion tracking",
            tasks=tasks,
        )

        # Simulate task completion
        session.tasks["T001"].status = TaskStatus.COMPLETE
        session.tasks["T001"].completed_at = datetime.now(UTC)
        session.tasks["T001"].output = "Task 1 completed successfully"

        # Update khipu
        await loom._update_khipu_file(session)

        # Verify khipu reflects completion
        khipu_content = session.khipu_path.read_text()
        assert "COMPLETE" in khipu_content
        assert "Task 1 completed successfully" in khipu_content

        # Complete all tasks
        session.tasks["T002"].status = TaskStatus.COMPLETE
        session.tasks["T002"].completed_at = datetime.now(UTC)
        session.tasks["T002"].output = "Task 2 completed successfully"

        # Check if ceremony should complete
        all_complete = all(t.status == TaskStatus.COMPLETE for t in session.tasks.values())
        assert all_complete

        # Complete ceremony
        session.status = CeremonyStatus.COMPLETE
        session.completion_time = datetime.now(UTC)
        await loom._update_khipu_file(session)

        # Verify final state
        khipu_content = session.khipu_path.read_text()
        assert "status: COMPLETE" in khipu_content.lower()


class TestLoomErrorHandling:
    """Test error handling in the Loom system"""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files"""
        with tempfile.TemporaryDirectory() as td:
            yield Path(td)

    @pytest.mark.asyncio
    async def test_task_failure_handling(self, temp_dir):
        """Test handling of task failures"""
        loom = TheLoom(ceremonies_dir=temp_dir)

        # Create ceremony
        tasks = [{"id": "T001", "name": "Failing Task", "description": "This will fail"}]

        session = await loom.initiate_ceremony(
            ceremony_name="Failure Test",
            master_weaver="guardian-60",
            sacred_intention="Test failure handling",
            tasks=tasks,
        )

        # Simulate task failure
        session.tasks["T001"].status = TaskStatus.FAILED
        session.tasks["T001"].error = "Simulated failure: Unable to complete task"

        # Update khipu
        await loom._update_khipu_file(session)

        # Verify failure is recorded
        khipu_content = session.khipu_path.read_text()
        assert "FAILED" in khipu_content
        assert "Simulated failure" in khipu_content

    @pytest.mark.asyncio
    async def test_invalid_task_dependencies(self, temp_dir):
        """Test handling of invalid task dependencies"""
        loom = TheLoom(ceremonies_dir=temp_dir)

        # Create tasks with invalid dependency
        tasks = [
            {
                "id": "T001",
                "name": "Task with bad dependency",
                "description": "Has invalid dependency",
                "dependencies": ["T999"],  # Non-existent task
            }
        ]

        # Should still create ceremony but note the issue
        session = await loom.initiate_ceremony(
            ceremony_name="Bad Dependency Test",
            master_weaver="guardian-60",
            sacred_intention="Test invalid dependencies",
            tasks=tasks,
        )

        assert len(session.tasks) == 1
        assert session.tasks["T001"].dependencies == ["T999"]


class TestLoomFileOperations:
    """Test Loom file operations with proper locking"""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files"""
        with tempfile.TemporaryDirectory() as td:
            yield Path(td)

    @pytest.mark.asyncio
    async def test_concurrent_khipu_updates(self, temp_dir):
        """Test that concurrent updates to khipu are handled safely"""
        loom = TheLoom(ceremonies_dir=temp_dir)

        # Create ceremony
        tasks = [
            {"id": f"T{i:03d}", "name": f"Task {i}", "description": f"Task number {i}"}
            for i in range(5)
        ]

        session = await loom.initiate_ceremony(
            ceremony_name="Concurrent Test",
            master_weaver="guardian-60",
            sacred_intention="Test concurrent updates",
            tasks=tasks,
        )

        # Simulate concurrent updates
        async def update_task(task_id: str):
            session.tasks[task_id].status = TaskStatus.COMPLETE
            session.tasks[task_id].output = f"{task_id} completed"
            await loom._update_khipu_file(session)

        # Run updates concurrently
        await asyncio.gather(*[update_task(f"T{i:03d}") for i in range(5)])

        # Verify all updates were recorded
        khipu_content = session.khipu_path.read_text()
        for i in range(5):
            assert f"T{i:03d} completed" in khipu_content

    @pytest.mark.asyncio
    async def test_khipu_recovery(self, temp_dir):
        """Test recovery from corrupted khipu files"""
        loom = TheLoom(ceremonies_dir=temp_dir)

        # Create a corrupted khipu
        khipu_path = temp_dir / "corrupted.md"
        khipu_path.write_text("This is not valid YAML or markdown")

        # Parsing should handle gracefully
        try:
            ceremony_data, tasks = await loom._parse_khipu_file(khipu_path)
            # Should return empty or default values
            assert ceremony_data is None or len(tasks) == 0
        except Exception as e:
            # Should not raise unhandled exceptions
            pytest.fail(f"Parsing corrupted khipu raised exception: {e}")


@pytest.mark.asyncio
async def test_loom_monitor_lifecycle():
    """Test the Loom monitor lifecycle"""
    with tempfile.TemporaryDirectory() as td:
        temp_dir = Path(td)
        loom = TheLoom(ceremonies_dir=temp_dir)

        # Start the Loom
        await loom.start()
        assert loom._monitor_task is not None
        assert not loom._monitor_task.done()

        # Let it run briefly
        await asyncio.sleep(0.1)

        # Stop the Loom
        await loom.stop()
        assert loom._monitor_task.cancelled()


@pytest.mark.asyncio
async def test_ceremony_status_transitions():
    """Test proper ceremony status transitions"""
    with tempfile.TemporaryDirectory() as td:
        temp_dir = Path(td)
        loom = TheLoom(ceremonies_dir=temp_dir)

        # Create ceremony
        tasks = [
            {"id": "T001", "name": "Setup", "description": "Initial setup"},
            {
                "id": "T002",
                "name": "Process",
                "description": "Main processing",
                "dependencies": ["T001"],
            },
            {
                "id": "T003",
                "name": "Cleanup",
                "description": "Final cleanup",
                "dependencies": ["T002"],
            },
        ]

        session = await loom.initiate_ceremony(
            ceremony_name="Status Test",
            master_weaver="guardian-60",
            sacred_intention="Test status transitions",
            tasks=tasks,
        )

        # Initial state
        assert session.status == CeremonyStatus.IN_PROGRESS
        assert all(t.status == TaskStatus.PENDING for t in session.tasks.values())

        # Complete tasks in order
        for task_id in ["T001", "T002", "T003"]:
            task = session.tasks[task_id]

            # Verify dependencies
            for dep_id in task.dependencies:
                dep_task = session.tasks[dep_id]
                assert dep_task.status == TaskStatus.COMPLETE

            # Progress task
            task.status = TaskStatus.IN_PROGRESS
            task.started_at = datetime.now(UTC)
            await loom._update_khipu_file(session)

            # Complete task
            task.status = TaskStatus.COMPLETE
            task.completed_at = datetime.now(UTC)
            task.output = f"{task_id} completed"
            await loom._update_khipu_file(session)

        # Complete ceremony
        session.status = CeremonyStatus.COMPLETE
        session.completion_time = datetime.now(UTC)
        await loom._update_khipu_file(session)

        # Verify final state
        assert session.status == CeremonyStatus.COMPLETE
        assert all(t.status == TaskStatus.COMPLETE for t in session.tasks.values())
