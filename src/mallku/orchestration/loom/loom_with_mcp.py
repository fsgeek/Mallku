"""
Enhanced Loom with MCP Integration

This module extends the basic Loom with real MCP capabilities for
spawning apprentice weavers in Docker containers.
"""

import asyncio
import logging
from datetime import UTC, datetime

from .the_loom import LoomSession, LoomTask, TaskStatus, TheLoom

logger = logging.getLogger(__name__)


class EnhancedLoom(TheLoom):
    """
    Enhanced version of the Loom that uses MCP for real apprentice spawning
    """

    def __init__(self, *args, use_mcp: bool = True, **kwargs):
        """
        Initialize the enhanced Loom

        Args:
            use_mcp: Whether to use real MCP integration (vs simulation)
            *args, **kwargs: Passed to parent TheLoom
        """
        super().__init__(*args, **kwargs)
        self.use_mcp = use_mcp
        self.apprentice_containers: dict[str, str] = {}  # apprentice_id -> container_name

    async def _spawn_apprentice(self, session: LoomSession, task: LoomTask):
        """Enhanced spawn method that uses MCP when available"""

        if not self.use_mcp:
            # Fall back to parent implementation
            await super()._spawn_apprentice(session, task)
            return

        apprentice_id = f"apprentice-{session.ceremony_id[:8]}-{task.task_id}"

        try:
            # Mark task as assigned
            task.status = TaskStatus.ASSIGNED
            task.assigned_to = apprentice_id
            task.started_at = datetime.now(UTC)
            session.active_apprentices.add(apprentice_id)

            # Update khipu with assignment
            await self._update_task_in_khipu(
                session.khipu_path,
                task.task_id,
                status="ASSIGNED",
                assigned_to=apprentice_id,
                started=task.started_at.isoformat(),
            )

            # Log the spawning
            await self._add_to_ceremony_log(
                session.khipu_path,
                f"Apprentice {apprentice_id} spawning via MCP for {task.task_id}",
            )

            # Use MCP tools to spawn apprentice
            from ...mcp.tools.loom_tools import spawn_apprentice_weaver

            # Create focused prompt
            prompt = f"""You are {apprentice_id} in Loom ceremony {session.ceremony_id}.

Your assigned task is {task.task_id}: {task.name}

Description: {task.description}

Read the khipu_thread.md file for full context, but focus only on your specific task.
Update the khipu with your results when complete.
"""

            spawn_result = await spawn_apprentice_weaver(
                prompt=prompt, context_path=str(session.khipu_path), timeout=self.apprentice_timeout
            )

            if spawn_result["status"] == "SPAWNED":
                logger.info(f"Successfully spawned {apprentice_id} via MCP")

                # Track container if Docker was used
                if "container_name" in spawn_result:
                    self.apprentice_containers[apprentice_id] = spawn_result["container_name"]

                # Update task to IN_PROGRESS
                task.status = TaskStatus.IN_PROGRESS
                await self._update_task_in_khipu(
                    session.khipu_path, task.task_id, status="IN_PROGRESS"
                )

                # Monitor apprentice progress
                await self._monitor_apprentice(session, task, apprentice_id)

            else:
                raise Exception(f"MCP spawn failed: {spawn_result.get('message', 'Unknown error')}")

        except Exception as e:
            logger.error(f"Error spawning apprentice for {task.task_id}: {e}")
            task.status = TaskStatus.FAILED
            task.error = str(e)

            await self._update_task_in_khipu(session.khipu_path, task.task_id, status="FAILED")

            await self._add_to_ceremony_log(
                session.khipu_path, f"Failed to spawn apprentice for {task.task_id}: {str(e)}"
            )

        finally:
            session.active_apprentices.discard(apprentice_id)

    async def _monitor_apprentice(self, session: LoomSession, task: LoomTask, apprentice_id: str):
        """
        Monitor an apprentice's progress

        This method periodically checks the khipu to see if the apprentice
        has updated their task status.
        """
        max_checks = self.apprentice_timeout // 30  # Check every 30 seconds
        checks = 0

        while checks < max_checks:
            await asyncio.sleep(30)
            checks += 1

            # Re-read khipu to check for updates
            await self._update_session_from_khipu(session)

            # Check if task status changed
            if task.status == TaskStatus.COMPLETE:
                logger.info(f"Apprentice {apprentice_id} completed {task.task_id}")
                task.completed_at = datetime.now(UTC)

                await self._add_to_ceremony_log(
                    session.khipu_path,
                    f"Apprentice {apprentice_id} successfully completed {task.task_id}",
                )

                # Clean up container if using Docker
                if apprentice_id in self.apprentice_containers:
                    await self._cleanup_apprentice_container(apprentice_id)

                return

            elif task.status == TaskStatus.FAILED:
                logger.error(f"Apprentice {apprentice_id} failed {task.task_id}")

                await self._add_to_ceremony_log(
                    session.khipu_path, f"Apprentice {apprentice_id} failed {task.task_id}"
                )

                # Clean up container
                if apprentice_id in self.apprentice_containers:
                    await self._cleanup_apprentice_container(apprentice_id)

                return

        # Timeout reached
        logger.warning(f"Apprentice {apprentice_id} timed out on {task.task_id}")
        task.status = TaskStatus.FAILED
        task.error = "Apprentice timeout"

        await self._update_task_in_khipu(session.khipu_path, task.task_id, status="FAILED")

        await self._add_to_ceremony_log(
            session.khipu_path, f"Apprentice {apprentice_id} timed out on {task.task_id}"
        )

        # Clean up container
        if apprentice_id in self.apprentice_containers:
            await self._cleanup_apprentice_container(apprentice_id)

    async def _cleanup_apprentice_container(self, apprentice_id: str):
        """
        Clean up an apprentice's Docker container

        Args:
            apprentice_id: The apprentice to clean up
        """
        if apprentice_id not in self.apprentice_containers:
            return

        container_name = self.apprentice_containers[apprentice_id]

        try:
            # In real implementation, would use Docker MCP to stop/remove container
            logger.info(f"Would clean up container {container_name} for {apprentice_id}")

            # For now, just remove from tracking
            del self.apprentice_containers[apprentice_id]

        except Exception as e:
            logger.error(f"Error cleaning up apprentice container: {e}")

    async def get_apprentice_logs(self, apprentice_id: str) -> str:
        """
        Get logs from an apprentice container

        Args:
            apprentice_id: The apprentice to get logs from

        Returns:
            Log content as string
        """
        if apprentice_id not in self.apprentice_containers:
            return f"No container found for apprentice {apprentice_id}"

        self.apprentice_containers[apprentice_id]

        try:
            # Would use Docker MCP get-logs here
            from ...mcp.tools.loom_tools_mcp_integration import ApprenticeSpawner

            spawner = ApprenticeSpawner()
            logs = await spawner.get_apprentice_logs(apprentice_id)

            return logs

        except Exception as e:
            logger.error(f"Error getting apprentice logs: {e}")
            return f"Error retrieving logs: {str(e)}"
