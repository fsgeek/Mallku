"""
MCP Integration for Spawning Apprentice Weavers

This module provides the real implementation for spawning AI instances
using Docker MCP and Claude Code's capabilities.
"""

import logging
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ApprenticeSpawner:
    """
    Manages the spawning of apprentice weaver instances using MCP

    This class bridges the gap between the Loom's orchestration needs
    and the actual infrastructure for creating new AI instances.
    """

    def __init__(self, docker_image: str = "mallku-apprentice:latest"):
        """
        Initialize the apprentice spawner

        Args:
            docker_image: Docker image to use for apprentices
        """
        self.docker_image = docker_image
        self.active_apprentices: dict[str, dict[str, Any]] = {}

    async def spawn_apprentice_container(
        self, apprentice_id: str, task_id: str, khipu_path: str, ceremony_name: str
    ) -> dict[str, Any]:
        """
        Spawn an apprentice weaver in a Docker container

        This method creates a containerized environment for an apprentice
        with access to the khipu_thread.md and necessary context.

        Args:
            apprentice_id: Unique ID for this apprentice
            task_id: The task to be performed
            khipu_path: Path to the ceremony's khipu_thread.md
            ceremony_name: Name of the ceremony

        Returns:
            Dict with container info and status
        """
        try:
            # Create a working directory for the apprentice
            work_dir = Path(f"/tmp/mallku/apprentices/{apprentice_id}")
            work_dir.mkdir(parents=True, exist_ok=True)

            # Copy the khipu to the work directory
            khipu_dest = work_dir / "khipu_thread.md"
            khipu_src = Path(khipu_path)
            if khipu_src.exists():
                khipu_dest.write_text(khipu_src.read_text())
            else:
                # Create a minimal khipu if the source doesn't exist
                khipu_dest.write_text(
                    f"# Minimal khipu for {task_id}\n\n### {task_id}: Task\n*Status: PENDING*\n\n#### Output\n```\n[Waiting for apprentice]\n```\n"
                )

            # Create the apprentice script
            apprentice_script = work_dir / "apprentice_work.py"
            script_content = self._create_apprentice_script(
                apprentice_id, task_id, str(khipu_dest), ceremony_name
            )
            apprentice_script.write_text(script_content)

            # Create Docker compose configuration
            compose_config = {
                "services": {
                    f"apprentice-{apprentice_id}": {
                        "image": self.docker_image,
                        "container_name": f"mallku-apprentice-{apprentice_id}",
                        "volumes": [
                            f"{work_dir}:/workspace",
                            # Mount .secrets for API access
                            f"{Path.cwd() / '.secrets'}:/app/.secrets:ro",
                            # Mount source code for imports
                            f"{Path.cwd() / 'src'}:/app/src:ro",
                        ],
                        "environment": {
                            "APPRENTICE_ID": apprentice_id,
                            "TASK_ID": task_id,
                            "CEREMONY_NAME": ceremony_name,
                            "PYTHONPATH": "/app:/workspace",
                        },
                        "command": ["python3", "/workspace/apprentice_work.py"],
                        # Remove network reference - use default network
                    }
                },
            }

            # Write compose file
            compose_path = work_dir / "docker-compose.yml"
            with open(compose_path, "w") as f:
                import yaml

                yaml.dump(compose_config, f)

            # Deploy using Docker
            # For now, we'll use subprocess to run docker-compose
            # In production, this would use the MCP Docker tools
            import subprocess

            # Sanitize project name for Docker (only alphanumeric and underscores)
            project_name = f"apprentice{apprentice_id.replace('-', '').replace('_', '')}"

            proc = subprocess.run(
                [
                    "docker-compose",
                    "-f",
                    str(compose_path),
                    "-p",
                    project_name,
                    "up",
                    "-d",
                ],
                capture_output=True,
                text=True,
                cwd=str(work_dir),
            )

            if proc.returncode != 0:
                raise Exception(f"Docker compose failed: {proc.stderr}")

            # Track the apprentice
            self.active_apprentices[apprentice_id] = {
                "container_name": f"mallku-apprentice-{apprentice_id}",
                "task_id": task_id,
                "started_at": datetime.now(UTC).isoformat(),
                "work_dir": str(work_dir),
                "khipu_path": khipu_path,  # Store original path for updates
                "status": "running",
            }

            return {
                "apprentice_id": apprentice_id,
                "status": "spawned",
                "container_name": f"mallku-apprentice-{apprentice_id}",
                "work_dir": str(work_dir),
                "message": "Apprentice container spawned successfully",
            }

        except Exception as e:
            logger.error(f"Error spawning apprentice container: {e}")
            return {
                "apprentice_id": apprentice_id,
                "status": "failed",
                "error": str(e),
                "message": f"Failed to spawn apprentice: {str(e)}",
            }

    def _create_apprentice_script(
        self, apprentice_id: str, task_id: str, khipu_path: str, ceremony_name: str
    ) -> str:
        """
        Create the Python script that the apprentice will run

        Now using the intelligent apprentice with AI reasoning capabilities.
        """
        # First try the intelligent apprentice script
        intelligent_apprentice_path = (
            Path(__file__).parent.parent.parent.parent.parent
            / "docker/apprentice-weaver/intelligent_apprentice.py"
        )
        if intelligent_apprentice_path.exists():
            return intelligent_apprentice_path.read_text()

        # Fallback to simple apprentice
        simple_apprentice_path = (
            Path(__file__).parent.parent.parent.parent.parent
            / "docker/apprentice-weaver/simple_apprentice.py"
        )
        if simple_apprentice_path.exists():
            return simple_apprentice_path.read_text()

        # Fallback to inline script
        return """#!/usr/bin/env python3
import os
import sys
print(f"Apprentice {os.environ.get('APPRENTICE_ID')} starting...")
print(f"Task: {os.environ.get('TASK_ID')}")
# Simple apprentice would update khipu here
"""

    async def get_apprentice_logs(self, apprentice_id: str) -> str:
        """
        Retrieve logs from an apprentice container

        Args:
            apprentice_id: The apprentice to get logs from

        Returns:
            Log content as string
        """
        if apprentice_id not in self.active_apprentices:
            return f"No active apprentice found with ID: {apprentice_id}"

        container_name = self.active_apprentices[apprentice_id]["container_name"]

        try:
            import subprocess

            proc = subprocess.run(
                ["docker", "logs", container_name], capture_output=True, text=True
            )

            if proc.returncode == 0:
                return proc.stdout
            else:
                return f"Error getting logs: {proc.stderr}"

        except Exception as e:
            logger.error(f"Error getting apprentice logs: {e}")
            return f"Error retrieving logs: {str(e)}"

    async def cleanup_apprentice(self, apprentice_id: str) -> bool:
        """
        Clean up an apprentice container and working directory

        Args:
            apprentice_id: The apprentice to clean up

        Returns:
            True if cleanup successful
        """
        if apprentice_id not in self.active_apprentices:
            return False

        apprentice_info = self.active_apprentices[apprentice_id]

        try:
            # Stop and remove container
            # In real implementation, would use MCP to stop/remove container

            # Clean up working directory
            import shutil

            work_dir = Path(apprentice_info["work_dir"])
            if work_dir.exists():
                shutil.rmtree(work_dir)

            # Remove from tracking
            del self.active_apprentices[apprentice_id]

            return True

        except Exception as e:
            logger.error(f"Error cleaning up apprentice: {e}")
            return False


# Enhanced spawn_apprentice_weaver function that uses real MCP
async def spawn_apprentice_weaver_mcp(
    prompt: str,
    context_path: str | None = None,
    model: str = "claude-3-opus-20240229",
    timeout: int = 1800,
    use_docker: bool = True,
) -> dict[str, Any]:
    """
    Enhanced version of spawn_apprentice_weaver that uses real MCP infrastructure

    This function can spawn apprentices either as Docker containers or
    as new Claude Code instances, depending on configuration.

    Args:
        prompt: The task description for the apprentice
        context_path: Path to khipu_thread.md or other context
        model: AI model to use
        timeout: Timeout in seconds
        use_docker: Whether to use Docker containers

    Returns:
        Dict with apprentice information and status
    """
    apprentice_id = f"apprentice-{uuid.uuid4().hex[:8]}"

    if use_docker and context_path:
        # Extract task_id from prompt if possible
        task_id = "unknown"
        if "task:" in prompt.lower():
            # Simple extraction, could be improved
            task_id = prompt.split("task:")[-1].split()[0]

        spawner = ApprenticeSpawner()
        result = await spawner.spawn_apprentice_container(
            apprentice_id=apprentice_id,
            task_id=task_id,
            khipu_path=context_path,
            ceremony_name="Loom Ceremony",
        )

        return result

    else:
        # Fallback to simulation mode or future Claude Code MCP integration
        raise NotImplementedError


# Integration with the Loom
class MCPLoomIntegration:
    """
    Integrates the Loom with MCP capabilities for real apprentice spawning
    """

    def __init__(self):
        self.spawner = ApprenticeSpawner()

    async def spawn_for_task(
        self, task_id: str, task_description: str, khipu_path: str, ceremony_id: str
    ) -> dict[str, Any]:
        """
        Spawn an apprentice for a specific Loom task

        Args:
            task_id: The task ID from the Loom
            task_description: Full task description
            khipu_path: Path to the ceremony's khipu_thread.md
            ceremony_id: The ceremony this task belongs to

        Returns:
            Spawn result dictionary
        """
        # Sanitize ceremony_id for Docker project names (only alphanumeric and underscores)
        sanitized_ceremony = ceremony_id.replace("-", "").replace("_", "")[:8]
        apprentice_id = f"apprentice{sanitized_ceremony}{task_id.lower()}"

        # Create a focused prompt for the apprentice

        # Spawn using Docker MCP
        result = await self.spawner.spawn_apprentice_container(
            apprentice_id=apprentice_id,
            task_id=task_id,
            khipu_path=khipu_path,
            ceremony_name=f"Ceremony {ceremony_id}",
        )

        # If spawning succeeded, check for completed work and copy results back
        if result["status"] == "spawned":
            # Give the apprentice some time to complete
            import asyncio

            await asyncio.sleep(5)

            # Check if the container finished and copy results
            await self._check_and_copy_results(apprentice_id, result["work_dir"], khipu_path)

        return result

    async def _check_and_copy_results(
        self, apprentice_id: str, work_dir: str, original_khipu_path: str
    ):
        """Check if apprentice completed work and copy results back"""
        try:
            import subprocess

            # Check if container is still running
            proc = subprocess.run(
                ["docker", "ps", "-q", "-f", f"name=mallku-apprentice-{apprentice_id}"],
                capture_output=True,
                text=True,
            )

            if not proc.stdout.strip():
                # Container finished, copy results back
                workspace_khipu = Path(work_dir) / "khipu_thread.md"
                if workspace_khipu.exists():
                    original_khipu = Path(original_khipu_path)
                    if original_khipu.exists():
                        # Copy the updated khipu back
                        original_khipu.write_text(workspace_khipu.read_text())
                        logger.info(
                            f"Copied apprentice {apprentice_id} results back to original khipu"
                        )

        except Exception as e:
            logger.error(f"Error checking apprentice results: {e}")
