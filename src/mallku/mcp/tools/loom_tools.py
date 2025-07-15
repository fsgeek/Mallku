"""
MCP Tools for the Weaver and Loom System

These tools enable AI instances to invoke the Loom for large task orchestration,
spawn apprentice weavers, and monitor ceremony progress.
"""

import logging
import re
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ...orchestration.loom import TaskStatus, TheLoom

logger = logging.getLogger(__name__)

# Global Loom instance (initialized on first use)
_loom_instance: TheLoom | None = None


def _get_loom() -> TheLoom:
    """Get or create the global Loom instance"""
    global _loom_instance
    if _loom_instance is None:
        _loom_instance = TheLoom()
        # Start the loom in the background
        import asyncio

        asyncio.create_task(_loom_instance.start())
    return _loom_instance


async def invoke_loom(
    ceremony_name: str,
    sacred_intention: str,
    tasks: list[dict[str, Any]],
    master_weaver: str | None = None,
) -> dict[str, Any]:
    """
    Invoke the Loom for large task orchestration

    This is the primary entry point for AI instances that recognize a task
    is too large for their context window. The Loom will orchestrate the
    decomposed tasks across multiple apprentice instances.

    Args:
        ceremony_name: A descriptive name for this ceremony
        sacred_intention: The overall goal and context (2-3 paragraphs)
        tasks: List of task definitions, each containing:
            - id: Unique task ID (e.g., "T001")
            - name: Short task name
            - description: Detailed description of what needs to be done
            - priority: HIGH, MEDIUM, or LOW (optional, defaults to MEDIUM)
            - dependencies: List of task IDs this depends on (optional)
        master_weaver: Identifier of invoking instance (auto-detected if not provided)

    Returns:
        Dict containing:
            - ceremony_id: Unique identifier for this ceremony
            - khipu_path: Path to the khipu_thread.md file
            - status: Initial status (always "IN_PROGRESS")
            - message: Human-readable status message

    Example:
        result = await invoke_loom(
            ceremony_name="Build Authentication System",
            sacred_intention="Create a secure, reciprocal authentication system...",
            tasks=[
                {
                    "id": "T001",
                    "name": "Design auth schema",
                    "description": "Design the database schema for user authentication...",
                    "priority": "HIGH"
                },
                {
                    "id": "T002",
                    "name": "Implement auth endpoints",
                    "description": "Create REST API endpoints for login, logout...",
                    "dependencies": ["T001"]
                }
            ]
        )
    """
    try:
        # Auto-detect master weaver if not provided
        if master_weaver is None:
            master_weaver = f"ai-instance-{uuid.uuid4().hex[:8]}"

        # Validate tasks
        task_ids = set()
        for task in tasks:
            if "id" not in task or "name" not in task or "description" not in task:
                raise ValueError(f"Task missing required fields: {task}")
            if task["id"] in task_ids:
                raise ValueError(f"Duplicate task ID: {task['id']}")
            task_ids.add(task["id"])

            # Validate dependencies reference existing tasks
            for dep in task.get("dependencies", []):
                if dep not in task_ids:
                    raise ValueError(f"Task {task['id']} depends on unknown task: {dep}")

        # Get or create Loom instance
        loom = _get_loom()

        # Initiate the ceremony
        session = await loom.initiate_ceremony(
            ceremony_name=ceremony_name,
            master_weaver=master_weaver,
            sacred_intention=sacred_intention,
            tasks=tasks,
        )

        logger.info(f"Loom ceremony initiated: {session.ceremony_id}")

        return {
            "ceremony_id": session.ceremony_id,
            "khipu_path": str(session.khipu_path),
            "status": session.status.value,
            "message": f"Ceremony '{ceremony_name}' initiated with {len(tasks)} tasks",
            "monitor_hint": f"Use check_loom_status('{session.ceremony_id}') to monitor progress",
        }

    except Exception as e:
        logger.error(f"Error invoking Loom: {e}")
        return {"error": str(e), "status": "FAILED", "message": f"Failed to invoke Loom: {str(e)}"}


async def check_loom_status(ceremony_id: str) -> dict[str, Any]:
    """
    Check the status of an active Loom ceremony

    Args:
        ceremony_id: The ceremony ID returned by invoke_loom

    Returns:
        Dict containing:
            - ceremony_id: The ceremony ID
            - status: Current ceremony status
            - tasks_total: Total number of tasks
            - tasks_complete: Number of completed tasks
            - tasks_failed: Number of failed tasks
            - active_apprentices: Number of currently active apprentices
            - khipu_path: Path to the khipu_thread.md file

    Example:
        status = await check_loom_status("abc123...")
        print(f"Progress: {status['tasks_complete']}/{status['tasks_total']}")
    """
    try:
        loom = _get_loom()

        if ceremony_id not in loom.active_sessions:
            # Try to find completed ceremony by checking khipu files
            ceremonies_dir = Path("fire_circle_decisions/loom_ceremonies")
            for khipu_file in ceremonies_dir.glob("*.md"):
                # Quick check if this might be our ceremony
                content = khipu_file.read_text()
                if f"ceremony_id: {ceremony_id}" in content:
                    return {
                        "ceremony_id": ceremony_id,
                        "status": "COMPLETE",
                        "message": "Ceremony completed, see khipu_path for results",
                        "khipu_path": str(khipu_file),
                    }

            return {
                "ceremony_id": ceremony_id,
                "status": "NOT_FOUND",
                "message": "Ceremony not found in active or completed ceremonies",
            }

        session = loom.active_sessions[ceremony_id]

        # Count task statuses
        tasks_complete = sum(1 for t in session.tasks.values() if t.status == TaskStatus.COMPLETE)
        tasks_failed = sum(1 for t in session.tasks.values() if t.status == TaskStatus.FAILED)
        tasks_in_progress = sum(
            1 for t in session.tasks.values() if t.status == TaskStatus.IN_PROGRESS
        )

        return {
            "ceremony_id": ceremony_id,
            "status": session.status.value,
            "tasks_total": len(session.tasks),
            "tasks_complete": tasks_complete,
            "tasks_failed": tasks_failed,
            "tasks_in_progress": tasks_in_progress,
            "active_apprentices": len(session.active_apprentices),
            "khipu_path": str(session.khipu_path),
            "initiated_at": session.initiated_at.isoformat(),
            "completion_time": session.completion_time.isoformat()
            if session.completion_time
            else None,
        }

    except Exception as e:
        logger.error(f"Error checking Loom status: {e}")
        return {"error": str(e), "status": "ERROR", "message": f"Failed to check status: {str(e)}"}


async def spawn_apprentice_weaver(
    prompt: str,
    context_path: str | None = None,
    model: str = "claude-3-opus-20240229",
    timeout: int = 1800,
) -> dict[str, Any]:
    """
    Spawn a new AI instance with specific context

    This is a lower-level tool used by the Loom to spawn apprentice weavers.
    It can also be used directly for simpler orchestration needs.

    Args:
        prompt: The prompt/instructions for the apprentice
        context_path: Optional path to a context file (e.g., khipu_thread.md)
        model: The model to use (defaults to Claude 3 Opus)
        timeout: Timeout in seconds (defaults to 30 minutes)

    Returns:
        Dict containing:
            - apprentice_id: Unique identifier for this apprentice
            - status: Spawn status
            - start_time: When the apprentice was spawned
            - output_path: Where the apprentice's output will be saved

    Note:
        This is currently a placeholder implementation. The actual spawning
        mechanism will depend on the available MCP infrastructure for creating
        new AI instances programmatically.
    """
    apprentice_id = f"apprentice-{uuid.uuid4().hex[:8]}"

    try:
        # Create output directory for apprentice
        output_dir = Path(
            f"fire_circle_decisions/apprentice_outputs/{datetime.now(UTC).strftime('%Y-%m-%d')}"
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{apprentice_id}.md"

        # Prepare the full prompt with context
        full_prompt = f"""You are an Apprentice Weaver in a Loom ceremony.

Your ID: {apprentice_id}
Your single task: {prompt}
"""

        if context_path:
            try:
                context_content = Path(context_path).read_text()
                full_prompt += f"\n\nContext from {context_path}:\n{context_content}"
            except Exception as e:
                logger.warning(f"Could not read context file: {e}")

        # TODO: Actual implementation would spawn a new Claude instance here
        # For now, we simulate the spawning
        logger.info(f"Would spawn apprentice {apprentice_id} with prompt length {len(full_prompt)}")

        # Save the prompt for debugging
        prompt_path = output_dir / f"{apprentice_id}_prompt.txt"
        prompt_path.write_text(full_prompt)

        # Simulate successful spawn
        return {
            "apprentice_id": apprentice_id,
            "status": "SPAWNED",
            "start_time": datetime.now(UTC).isoformat(),
            "output_path": str(output_path),
            "prompt_path": str(prompt_path),
            "message": "Apprentice spawned (simulation mode)",
            "note": "Actual Claude instance spawning not yet implemented",
        }

    except Exception as e:
        logger.error(f"Error spawning apprentice: {e}")
        return {
            "apprentice_id": apprentice_id,
            "status": "FAILED",
            "error": str(e),
            "message": f"Failed to spawn apprentice: {str(e)}",
        }


# Additional utility functions that might be useful


async def list_active_ceremonies() -> dict[str, Any]:
    """
    List all active Loom ceremonies

    Returns:
        Dict containing list of active ceremonies with basic info
    """
    try:
        loom = _get_loom()

        ceremonies = []
        for ceremony_id, session in loom.active_sessions.items():
            ceremonies.append(
                {
                    "ceremony_id": ceremony_id,
                    "status": session.status.value,
                    "tasks_total": len(session.tasks),
                    "initiated_at": session.initiated_at.isoformat(),
                    "khipu_path": str(session.khipu_path),
                }
            )

        return {"active_ceremonies": ceremonies, "count": len(ceremonies)}

    except Exception as e:
        logger.error(f"Error listing ceremonies: {e}")
        return {"error": str(e), "active_ceremonies": [], "count": 0}


async def read_khipu_thread(khipu_path: str) -> dict[str, Any]:
    """
    Read and parse a khipu_thread.md file

    Args:
        khipu_path: Path to the khipu_thread.md file

    Returns:
        Dict containing parsed khipu content and metadata
    """
    try:
        path = Path(khipu_path)
        if not path.exists():
            return {"error": "File not found", "path": khipu_path}

        content = path.read_text()

        # Extract key information
        # This is a simplified parser - could be expanded
        ceremony_id_match = re.search(r"ceremony_id: (.+)", content)
        status_match = re.search(r"status: (\w+)", content)

        return {
            "path": khipu_path,
            "ceremony_id": ceremony_id_match.group(1) if ceremony_id_match else None,
            "status": status_match.group(1) if status_match else None,
            "content": content,
            "size": len(content),
            "modified": datetime.fromtimestamp(path.stat().st_mtime, tz=UTC).isoformat(),
        }

    except Exception as e:
        logger.error(f"Error reading khipu: {e}")
        return {"error": str(e), "path": khipu_path}
