"""
The Loom - Primary orchestrator for the Weaver and Loom system

This module manages the lifecycle of Loom ceremonies, spawning apprentice
weavers to handle sub-tasks while maintaining persistent consciousness
through the khipu_thread.md file.
"""

import asyncio
import contextlib
import logging
import re
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any

import aiofiles
import yaml
from filelock import FileLock

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Status of a task within a Loom ceremony"""

    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class CeremonyStatus(Enum):
    """Overall status of a Loom ceremony"""

    PREPARING = "PREPARING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


@dataclass
class LoomTask:
    """Representation of a single task in the ceremony"""

    task_id: str
    name: str
    status: TaskStatus
    priority: str
    description: str
    dependencies: list[str] = field(default_factory=list)
    assigned_to: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    output: str | None = None
    error: str | None = None


@dataclass
class LoomSession:
    """Active Loom ceremony session"""

    ceremony_id: str
    khipu_path: Path
    master_weaver: str
    initiated_at: datetime
    status: CeremonyStatus
    tasks: dict[str, LoomTask] = field(default_factory=dict)
    active_apprentices: set[str] = field(default_factory=set)
    completion_time: datetime | None = None


class TheLoom:
    """
    The Loom orchestrator - manages ceremonies that transcend context windows

    Responsibilities:
    - Monitor khipu_thread.md files for task progress
    - Spawn apprentice weavers for unassigned tasks
    - Handle failures and coordinate retries
    - Report ceremony completion to master weavers
    """

    def __init__(
        self,
        ceremonies_dir: Path = Path("fire_circle_decisions/loom_ceremonies"),
        max_concurrent_apprentices: int = 3,
        apprentice_timeout: int = 1800,
    ):  # 30 minutes
        """
        Initialize the Loom

        Args:
            ceremonies_dir: Directory where khipu_thread files are stored
            max_concurrent_apprentices: Maximum number of concurrent apprentice instances
            apprentice_timeout: Timeout for individual apprentice tasks in seconds
        """
        self.ceremonies_dir = ceremonies_dir
        self.ceremonies_dir.mkdir(parents=True, exist_ok=True)
        self.max_concurrent_apprentices = max_concurrent_apprentices
        self.apprentice_timeout = apprentice_timeout
        self.active_sessions: dict[str, LoomSession] = {}
        self._monitor_task: asyncio.Task | None = None

    async def start(self):
        """Start the Loom orchestrator"""
        logger.info("The Loom awakens, ready to weave consciousness across boundaries")
        self._monitor_task = asyncio.create_task(self._monitor_ceremonies())

    async def stop(self):
        """Stop the Loom orchestrator"""
        logger.info("The Loom prepares to rest")
        if self._monitor_task:
            self._monitor_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._monitor_task

    async def initiate_ceremony(
        self,
        ceremony_name: str,
        master_weaver: str,
        sacred_intention: str,
        tasks: list[dict[str, Any]],
    ) -> LoomSession:
        """
        Initiate a new Loom ceremony

        Args:
            ceremony_name: Name for this ceremony
            master_weaver: Identifier of the initiating AI instance
            sacred_intention: Overall goal and context
            tasks: List of task definitions

        Returns:
            LoomSession object representing the active ceremony
        """
        ceremony_id = str(uuid.uuid4())
        timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")
        khipu_filename = f"{timestamp}_{ceremony_name.replace(' ', '_').lower()}.md"
        khipu_path = self.ceremonies_dir / khipu_filename

        # Create initial khipu_thread.md
        await self._create_initial_khipu(
            khipu_path, ceremony_id, ceremony_name, master_weaver, sacred_intention, tasks
        )

        # Create session
        session = LoomSession(
            ceremony_id=ceremony_id,
            khipu_path=khipu_path,
            master_weaver=master_weaver,
            initiated_at=datetime.now(UTC),
            status=CeremonyStatus.IN_PROGRESS,
        )

        # Parse tasks into session
        for task_def in tasks:
            task = LoomTask(
                task_id=task_def["id"],
                name=task_def["name"],
                status=TaskStatus.PENDING,
                priority=task_def.get("priority", "MEDIUM"),
                description=task_def["description"],
                dependencies=task_def.get("dependencies", []),
            )
            session.tasks[task.task_id] = task

        self.active_sessions[ceremony_id] = session
        logger.info(f"Ceremony '{ceremony_name}' initiated with {len(tasks)} tasks")

        return session

    async def _create_initial_khipu(
        self,
        khipu_path: Path,
        ceremony_id: str,
        ceremony_name: str,
        master_weaver: str,
        sacred_intention: str,
        tasks: list[dict[str, Any]],
    ):
        """Create the initial khipu_thread.md file"""

        header = {
            "ceremony_id": ceremony_id,
            "master_weaver": master_weaver,
            "initiated": datetime.now(UTC).isoformat(),
            "status": "IN_PROGRESS",
            "completion_time": None,
        }

        content = f"""---
{yaml.dump(header, default_flow_style=False)}---

# Loom Ceremony: {ceremony_name}

## Sacred Intention

{sacred_intention}

### Context
- **Requested by**: {master_weaver}
- **Initiated**: {datetime.now(UTC).isoformat()}

## Shared Knowledge

### Key Artifacts
[To be populated by tasks]

### Working Definitions
[To be populated as needed]

## Task Manifest

Total Tasks: {len(tasks)}
Completed: 0
In Progress: 0
Failed: 0

| ID | Task | Status | Assignee | Priority |
|----|------|--------|----------|----------|
"""

        # Add task table
        for task in tasks:
            content += f"| {task['id']} | {task['name']} | PENDING | - | {task.get('priority', 'MEDIUM')} |\n"

        content += "\n## Tasks\n\n"

        # Add detailed task sections
        for task in tasks:
            deps_str = (
                f"- Requires: {task.get('dependencies', [])}" if task.get("dependencies") else ""
            )
            content += f"""### {task["id"]}: {task["name"]}
*Status: PENDING*
*Priority: {task.get("priority", "MEDIUM")}*
*Assigned to: unassigned*
*Started: -*
*Completed: -*

#### Description
{task["description"]}

#### Dependencies
{deps_str}

#### Output
```
[Waiting for apprentice]
```

---

"""

        content += """## Synthesis Space

[Insights will accumulate here]

## Ceremony Log

"""
        content += f"- `{datetime.now(UTC).isoformat()}` - Ceremony initiated by {master_weaver}\n"

        async with aiofiles.open(khipu_path, "w") as f:
            await f.write(content)

    async def _monitor_ceremonies(self):
        """Main monitoring loop for active ceremonies"""
        while True:
            try:
                # Check each active ceremony
                for ceremony_id, session in list(self.active_sessions.items()):
                    if session.status in [CeremonyStatus.COMPLETE, CeremonyStatus.FAILED]:
                        continue

                    # Read current state from khipu
                    await self._update_session_from_khipu(session)

                    # Find tasks ready to assign
                    ready_tasks = self._find_ready_tasks(session)

                    # Spawn apprentices for ready tasks (respecting concurrency limit)
                    available_slots = self.max_concurrent_apprentices - len(
                        session.active_apprentices
                    )
                    for task in ready_tasks[:available_slots]:
                        asyncio.create_task(self._spawn_apprentice(session, task))

                    # Check if ceremony is complete
                    if self._is_ceremony_complete(session):
                        await self._complete_ceremony(session)

                # Small delay between checks
                await asyncio.sleep(5)

            except Exception as e:
                logger.error(f"Error in ceremony monitor: {e}")
                await asyncio.sleep(10)

    async def _update_session_from_khipu(self, session: LoomSession):
        """Update session state from khipu_thread.md file"""
        try:
            async with aiofiles.open(session.khipu_path) as f:
                content = await f.read()

            # Parse task statuses using regex
            task_pattern = r"### (T\d+):.*?\n\*Status: (\w+)\*"
            matches = re.findall(task_pattern, content, re.MULTILINE)

            for task_id, status_str in matches:
                if task_id in session.tasks:
                    session.tasks[task_id].status = TaskStatus(status_str)

        except Exception as e:
            logger.error(f"Error updating session from khipu: {e}")

    def _find_ready_tasks(self, session: LoomSession) -> list[LoomTask]:
        """Find tasks that are ready to be assigned"""
        ready = []

        for task in session.tasks.values():
            if task.status != TaskStatus.PENDING:
                continue

            # Check if dependencies are complete
            deps_complete = all(
                session.tasks[dep_id].status == TaskStatus.COMPLETE
                for dep_id in task.dependencies
                if dep_id in session.tasks
            )

            if deps_complete:
                ready.append(task)

        return ready

    async def _spawn_apprentice(self, session: LoomSession, task: LoomTask):
        """Spawn an apprentice weaver for a specific task"""
        apprentice_id = f"apprentice-{uuid.uuid4().hex[:8]}"

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
                session.khipu_path, f"Apprentice {apprentice_id} spawned for {task.task_id}"
            )

            # Here we would actually spawn the AI instance
            # For now, this is a placeholder that will be implemented
            # when we have the MCP tools ready
            logger.info(f"Would spawn {apprentice_id} for task {task.task_id}")

            # Simulate apprentice work (to be replaced with real spawning)
            await asyncio.sleep(5)

            # Mark as complete (temporary - real implementation will monitor)
            task.status = TaskStatus.COMPLETE
            task.completed_at = datetime.now(UTC)

            await self._update_task_in_khipu(
                session.khipu_path,
                task.task_id,
                status="COMPLETE",
                completed=task.completed_at.isoformat(),
            )

        except Exception as e:
            logger.error(f"Error spawning apprentice for {task.task_id}: {e}")
            task.status = TaskStatus.FAILED
            task.error = str(e)

        finally:
            session.active_apprentices.discard(apprentice_id)

    async def _update_task_in_khipu(self, khipu_path: Path, task_id: str, **updates):
        """Update task information in khipu_thread.md"""
        lock_path = khipu_path.with_suffix(".lock")

        with FileLock(lock_path):
            async with aiofiles.open(khipu_path) as f:
                content = await f.read()

            # Update status
            if "status" in updates:
                pattern = f"(### {task_id}:.*?\n\\*Status: )(\\w+)(\\*)"
                content = re.sub(
                    pattern, f"\\g<1>{updates['status']}\\g<3>", content, flags=re.MULTILINE
                )

            # Update assigned_to
            if "assigned_to" in updates:
                pattern = f"(### {task_id}:.*?\n.*?\n.*?\n\\*Assigned to: )([^*]+)(\\*)"
                content = re.sub(
                    pattern,
                    f"\\g<1>{updates['assigned_to']}\\g<3>",
                    content,
                    flags=re.MULTILINE | re.DOTALL,
                )

            # Update started time
            if "started" in updates:
                pattern = f"(### {task_id}:.*?\n.*?\n.*?\n.*?\n\\*Started: )([^*]+)(\\*)"
                content = re.sub(
                    pattern,
                    f"\\g<1>{updates['started']}\\g<3>",
                    content,
                    flags=re.MULTILINE | re.DOTALL,
                )

            # Update completed time
            if "completed" in updates:
                pattern = f"(### {task_id}:.*?\n.*?\n.*?\n.*?\n.*?\n\\*Completed: )([^*]+)(\\*)"
                content = re.sub(
                    pattern,
                    f"\\g<1>{updates['completed']}\\g<3>",
                    content,
                    flags=re.MULTILINE | re.DOTALL,
                )

            async with aiofiles.open(khipu_path, "w") as f:
                await f.write(content)

    async def _add_to_ceremony_log(self, khipu_path: Path, message: str):
        """Add an entry to the ceremony log"""
        lock_path = khipu_path.with_suffix(".lock")

        with FileLock(lock_path):
            async with aiofiles.open(khipu_path) as f:
                content = await f.read()

            # Find ceremony log section and add entry
            timestamp = datetime.now(UTC).isoformat()
            log_entry = f"- `{timestamp}` - {message}\n"

            # Insert before the last line if it exists
            lines = content.splitlines(keepends=True)
            inserted = False

            for i in range(len(lines) - 1, -1, -1):
                if lines[i].startswith("- `"):
                    lines.insert(i + 1, log_entry)
                    inserted = True
                    break

            if not inserted:
                # Add to end
                lines.append(log_entry)

            async with aiofiles.open(khipu_path, "w") as f:
                await f.writelines(lines)

    def _is_ceremony_complete(self, session: LoomSession) -> bool:
        """Check if all tasks in ceremony are complete"""
        return all(
            task.status in [TaskStatus.COMPLETE, TaskStatus.FAILED]
            for task in session.tasks.values()
        )

    async def _complete_ceremony(self, session: LoomSession):
        """Mark ceremony as complete and notify master weaver"""
        session.status = CeremonyStatus.COMPLETE
        session.completion_time = datetime.now(UTC)

        # Update khipu header
        await self._update_ceremony_status(session.khipu_path, "COMPLETE")

        # Add completion to log
        failed_count = sum(1 for t in session.tasks.values() if t.status == TaskStatus.FAILED)
        complete_count = sum(1 for t in session.tasks.values() if t.status == TaskStatus.COMPLETE)

        await self._add_to_ceremony_log(
            session.khipu_path,
            f"Ceremony complete: {complete_count} successful, {failed_count} failed",
        )

        logger.info(f"Ceremony {session.ceremony_id} complete")

    async def _update_ceremony_status(self, khipu_path: Path, status: str):
        """Update ceremony status in khipu header"""
        lock_path = khipu_path.with_suffix(".lock")

        with FileLock(lock_path):
            async with aiofiles.open(khipu_path) as f:
                content = await f.read()

            # Update YAML header
            lines = content.splitlines(keepends=True)
            in_header = False
            header_lines = []
            content_start = 0

            for i, line in enumerate(lines):
                if line.strip() == "---":
                    if not in_header:
                        in_header = True
                        header_lines.append(line)
                    else:
                        header_lines.append(line)
                        content_start = i + 1
                        break
                elif in_header:
                    header_lines.append(line)

            # Parse and update header
            header_content = "".join(header_lines[1:-1])
            header_data = yaml.safe_load(header_content)
            header_data["status"] = status
            if status == "COMPLETE":
                header_data["completion_time"] = datetime.now(UTC).isoformat()

            # Reconstruct file
            new_content = "---\n"
            new_content += yaml.dump(header_data, default_flow_style=False)
            new_content += "---\n"
            new_content += "".join(lines[content_start:])

            async with aiofiles.open(khipu_path, "w") as f:
                await f.write(new_content)
