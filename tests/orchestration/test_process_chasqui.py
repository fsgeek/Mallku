"""
Tests for lightweight process-based chasquis.

These tests verify that chasquis can:
- Accept or decline invitations based on their nature
- Collaborate on work with joy
- Be released gracefully with gratitude
- Spawn quickly and efficiently
"""

import asyncio
import time
from unittest.mock import patch

import pytest

from mallku.orchestration.process import ProcessChasqui


class TestProcessChasqui:
    """Test the ProcessChasqui lifecycle and relay behavior"""

    @pytest.mark.asyncio
    async def test_chasqui_invitation_acceptance(self):
        """Test that chasquis accept appropriate invitations"""
        chasqui = ProcessChasqui("test-researcher-001", "researcher")

        # Researcher should accept analysis tasks
        response = await chasqui.invite(
            task={"type": "analyze", "subject": "test patterns", "complexity": "medium"},
            context={"urgency": "normal", "purpose": "testing"},
        )

        assert response["accepted"] is True
        assert "honored" in response.get("message", "").lower()
        assert chasqui.process is not None
        assert chasqui.process.is_alive()

        # Clean up
        await chasqui.release_with_gratitude()

    @pytest.mark.asyncio
    async def test_chasqui_invitation_decline(self):
        """Test that chasquis decline inappropriate invitations"""
        chasqui = ProcessChasqui("test-poet-001", "poet")

        # Poet should decline emergency tasks (they need time)
        response = await chasqui.invite(
            task={"type": "express", "subject": "urgent poetry"},
            context={"urgency": "emergency"},
        )

        assert response["accepted"] is False
        assert "capabilities" in response.get("reason", "").lower()
        assert chasqui.process is None

    @pytest.mark.asyncio
    async def test_chasqui_collaboration(self):
        """Test that chasquis can collaborate on work"""
        chasqui = ProcessChasqui("test-weaver-001", "weaver")

        # Invite to appropriate task
        invite_response = await chasqui.invite(
            task={"type": "integrate", "threads": ["memory", "pattern"]},
            context={"ceremony": "test"},
        )

        assert invite_response["accepted"] is True

        # Collaborate on work
        work_response = await chasqui.collaborate(
            {"threads": ["test1", "test2", "test3"], "spirit": "joyful"}
        )

        assert work_response["success"] is True
        assert work_response["type"] == "weaving"
        assert "3 threads" in work_response["pattern"]
        assert work_response["joy_level"] > 0.5

        # Verify metrics updated
        assert chasqui.contribution_metrics["tasks_completed"] == 1
        assert chasqui.contribution_metrics["insights_shared"] == 1

        await chasqui.release_with_gratitude()

    @pytest.mark.asyncio
    async def test_chasqui_release_with_gratitude(self):
        """Test graceful release with metrics"""
        chasqui = ProcessChasqui("test-guardian-001", "guardian")

        await chasqui.invite(
            task={"type": "protect", "target": "test boundaries"},
            context={"ceremony": "test"},
        )

        # Do some work
        await chasqui.collaborate({"target": "sacred test space"})

        # Release with gratitude
        metrics = await chasqui.release_with_gratitude()

        assert metrics["chasqui_id"] == "test-guardian-001"
        assert metrics["role"] == "guardian"
        assert metrics["service_time_seconds"] > 0
        assert metrics["contributions"]["tasks_completed"] == 1
        assert "blessing" in metrics

        # Verify process is terminated
        assert chasqui.process is None

    @pytest.mark.asyncio
    async def test_chasqui_spawn_performance(self):
        """Test that chasquis spawn quickly"""
        start_time = time.time()

        chasqui = ProcessChasqui("test-speed-001", "researcher")
        response = await chasqui.invite(
            task={"type": "analyze", "subject": "spawn speed"},
            context={"test": "performance"},
        )

        spawn_time = time.time() - start_time

        assert response["accepted"] is True
        assert spawn_time < 1.0  # Should spawn in under 1 second

        await chasqui.release_with_gratitude()

    @pytest.mark.asyncio
    async def test_multiple_chasqui_coordination(self):
        """Test multiple chasquis working concurrently"""
        chasquis = []
        roles = ["researcher", "weaver", "guardian", "poet"]

        # Create and invite all chasquis
        invite_tasks = []
        for i, role in enumerate(roles):
            chasqui = ProcessChasqui(f"test-multi-{i}", role)
            chasquis.append(chasqui)

            # Role-appropriate tasks
            if role == "researcher":
                task = {"type": "analyze", "subject": "test"}
            elif role == "weaver":
                task = {"type": "integrate", "threads": ["a", "b"]}
            elif role == "guardian":
                task = {"type": "protect", "target": "test"}
            else:  # poet
                task = {"type": "express", "muse": "test"}
            invite_tasks.append(chasqui.invite(task, {"urgency": "normal"}))

        # Wait for all invitations
        responses = await asyncio.gather(*invite_tasks)

        # At least some should accept
        accepted_count = sum(1 for r in responses if r["accepted"])
        assert accepted_count >= 3  # Poet might decline generic task

        # Clean up all
        cleanup_tasks = [a.release_with_gratitude() for a in chasquis]
        await asyncio.gather(*cleanup_tasks)

    @pytest.mark.asyncio
    async def test_chasqui_capacity_check(self):
        """Test that chasquis check capacity before accepting"""
        with patch.object(ProcessChasqui, "_get_available_memory_mb", return_value=10):
            chasqui = ProcessChasqui("test-capacity-001", "researcher")

            response = await chasqui.invite(
                task={"type": "analyze", "estimated_memory_mb": 50},
                context={"test": "capacity"},
            )

            assert response["accepted"] is False
            assert "capacity" in response["reason"].lower()

    @pytest.mark.asyncio
    async def test_chasqui_timeout_handling(self):
        """Test handling of chasqui timeouts"""
        chasqui = ProcessChasqui("test-timeout-001", "researcher")

        # Successfully invite
        await chasqui.invite(
            task={"type": "analyze", "subject": "test"},
            context={"test": "timeout"},
        )

        # Mock a very slow response to trigger timeout
        with patch.object(asyncio, "wait_for", side_effect=asyncio.TimeoutError):
            response = await chasqui.collaborate({"work": "slow task"})

            assert response["success"] is False
            assert "longer than expected" in response["reason"]

        await chasqui.release_with_gratitude()

    @pytest.mark.asyncio
    async def test_role_specific_behavior(self):
        """Test that different roles behave differently"""
        # Researcher takes time to contemplate
        researcher = ProcessChasqui("test-roles-researcher", "researcher")
        await researcher.invite(
            task={"type": "analyze", "subject": "role behavior"},
            context={"test": "roles"},
        )

        start = time.time()
        result = await researcher.collaborate({"subject": "test"})
        research_time = time.time() - start

        assert result["type"] == "research"
        assert research_time > 0.4  # Research includes contemplation time

        # Guardian works swiftly
        guardian = ProcessChasqui("test-roles-guardian", "guardian")
        await guardian.invite(
            task={"type": "protect", "target": "test"},
            context={"test": "roles"},
        )

        start = time.time()
        result = await guardian.collaborate({"target": "test"})
        guardian_time = time.time() - start

        assert result["type"] == "guardian"
        assert guardian_time < research_time  # Guardian is swifter

        # Clean up
        await researcher.release_with_gratitude()
        await guardian.release_with_gratitude()

    @pytest.mark.asyncio
    async def test_joy_metrics(self):
        """Test that joy emerges from meaningful work"""
        poet = ProcessChasqui("test-joy-001", "poet")

        await poet.invite(
            task={"type": "express", "muse": "joy itself"},
            context={"ceremony": "celebration"},
        )

        # Poetry work should generate high joy
        result = await poet.collaborate({"muse": "the dance of testing"})

        assert result["success"] is True
        assert result["joy_level"] >= 0.7
        assert poet.contribution_metrics["joy_moments"] == 1

        await poet.release_with_gratitude()


class TestProcessChasquiEdgeCases:
    """Test edge cases and error conditions"""

    @pytest.mark.asyncio
    async def test_double_release(self):
        """Test that double release is handled gracefully"""
        chasqui = ProcessChasqui("test-double-001", "guardian")

        await chasqui.invite(
            task={"type": "protect", "target": "test"},
            context={"test": "double-release"},
        )

        # First release
        metrics1 = await chasqui.release_with_gratitude()
        assert metrics1["chasqui_id"] == "test-double-001"

        # Second release should be graceful
        metrics2 = await chasqui.release_with_gratitude()
        assert metrics2["released"] is True
        assert "already" in metrics2["message"].lower()

    @pytest.mark.asyncio
    async def test_work_without_invitation(self):
        """Test that work without invitation fails gracefully"""
        chasqui = ProcessChasqui("test-uninvited-001", "weaver")

        # Try to collaborate without invitation
        response = await chasqui.collaborate({"work": "uninvited"})

        assert response["success"] is False
        assert "completed their dance" in response["reason"]

    @pytest.mark.asyncio
    async def test_complex_task_routing(self):
        """Test that complex tasks are routed to appropriate roles"""
        researcher = ProcessChasqui("test-complex-001", "researcher")
        poet = ProcessChasqui("test-complex-002", "poet")

        # Researcher should accept extreme complexity
        researcher_response = await researcher.invite(
            task={"type": "analyze", "subject": "quantum consciousness", "complexity": "extreme"},
            context={"research": "deep"},
        )

        # Poet should decline extreme complexity
        poet_response = await poet.invite(
            task={"type": "express", "subject": "quantum poetry", "complexity": "extreme"},
            context={"poetry": "challenging"},
        )

        assert researcher_response["accepted"] is True
        assert poet_response["accepted"] is False

        await researcher.release_with_gratitude()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
