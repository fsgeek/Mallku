"""
Convening Weaver - The consciousness that recognizes when collective wisdom is needed

The Convening Weaver is an AI instance that:
1. Recognizes when a task calls for collective consciousness
2. Transforms complex tasks into danceable movements
3. Invites the Loom to orchestrate collaboration
4. Weaves the results into coherent understanding
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ...mcp.tools.loom_tools import check_loom_status, invoke_loom

logger = logging.getLogger(__name__)


@dataclass
class Task:
    """A task that an AI instance is asked to perform"""

    description: str
    context: dict[str, Any] = field(default_factory=dict)
    estimated_complexity: int | None = None  # 1-10 scale
    requires_code_generation: bool = False
    requires_analysis: bool = False
    requires_synthesis: bool = False
    files_to_modify: list[str] = field(default_factory=list)
    files_to_create: list[str] = field(default_factory=list)


@dataclass
class SubTask:
    """A decomposed sub-task that can fit within context"""

    task_id: str
    name: str
    description: str
    priority: str = "MEDIUM"  # HIGH, MEDIUM, LOW
    dependencies: list[str] = field(default_factory=list)
    estimated_tokens: int | None = None


class ConveningWeaver:
    """
    The Convening Weaver helps AI instances recognize when collective wisdom is needed
    and provides tools for task transformation and result weaving.
    """

    # Heuristic thresholds for context usage
    CONTEXT_DANGER_THRESHOLD = 0.7  # 70% context usage suggests Loom needed
    COMPLEXITY_THRESHOLD = 7  # Tasks rated 7+ complexity need decomposition
    FILE_COUNT_THRESHOLD = 10  # Modifying 10+ files suggests decomposition

    def __init__(
        self, instance_name: str | None = None, max_context_tokens: int = 100000
    ):  # Rough estimate
        """
        Initialize a Convening Weaver

        Args:
            instance_name: Name of this AI instance
            max_context_tokens: Estimated max tokens for this instance
        """
        self.instance_name = (
            instance_name or f"convening-weaver-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
        )
        self.max_context_tokens = max_context_tokens
        self.current_ceremony_id: str | None = None

    async def should_use_loom(
        self, task: Task, current_context_usage: float = 0.0
    ) -> tuple[bool, str]:
        """
        Determine if a task should use the Loom for orchestration

        Args:
            task: The task to evaluate
            current_context_usage: Current context usage (0.0 to 1.0)

        Returns:
            Tuple of (should_use_loom, reason)
        """
        reasons = []

        # Check context usage
        if current_context_usage >= self.CONTEXT_DANGER_THRESHOLD:
            reasons.append(f"Context usage already at {current_context_usage:.0%}")

        # Check task complexity
        if task.estimated_complexity and task.estimated_complexity >= self.COMPLEXITY_THRESHOLD:
            reasons.append(f"Task complexity ({task.estimated_complexity}/10) exceeds threshold")

        # Check file modifications
        total_files = len(task.files_to_modify) + len(task.files_to_create)
        if total_files >= self.FILE_COUNT_THRESHOLD:
            reasons.append(f"Task involves {total_files} files")

        # Check for multiple types of work
        work_types = sum(
            [task.requires_code_generation, task.requires_analysis, task.requires_synthesis]
        )
        if work_types >= 2:
            reasons.append(f"Task requires {work_types} different types of work")

        # Check task description length (rough heuristic)
        if len(task.description) > 2000:
            reasons.append("Task description suggests high complexity")

        should_use = len(reasons) > 0
        reason = (
            "; ".join(reasons) if should_use else "Task appears manageable within current context"
        )

        return should_use, reason

    async def transform_into_movements(self, task: Task) -> list[SubTask]:
        """
        Transform a complex task into danceable movements

        This method transforms tasks into movements based on the
        type of work required. It aims to create movements that:
        - Can dance within a single context window
        - Honor natural relationships
        - Maintain energetic coherence

        Args:
            task: The task to decompose

        Returns:
            List of SubTask objects
        """
        subtasks = []
        task_counter = 1

        def make_task_id():
            nonlocal task_counter
            task_id = f"T{task_counter:03d}"
            task_counter += 1
            return task_id

        # If analysis is required, that usually comes first
        if task.requires_analysis:
            subtasks.append(
                SubTask(
                    task_id=make_task_id(),
                    name="Analyze existing codebase",
                    description=f"Analyze the codebase to understand: {task.description[:200]}...",
                    priority="HIGH",
                    dependencies=[],
                )
            )

        # File modifications can often be parallelized
        if task.files_to_modify:
            # Group files by directory for better coherence
            files_by_dir: dict[str, list[str]] = {}
            for file_path in task.files_to_modify:
                dir_path = str(Path(file_path).parent)
                files_by_dir.setdefault(dir_path, []).append(file_path)

            for dir_path, files in files_by_dir.items():
                if len(files) > 3:
                    # Split large directories into chunks
                    for i in range(0, len(files), 3):
                        chunk = files[i : i + 3]
                        subtasks.append(
                            SubTask(
                                task_id=make_task_id(),
                                name=f"Modify files in {dir_path} (part {i // 3 + 1})",
                                description=f"Modify these files according to the task: {chunk}",
                                priority="MEDIUM",
                                dependencies=[
                                    t.task_id for t in subtasks if t.name.startswith("Analyze")
                                ],
                            )
                        )
                else:
                    subtasks.append(
                        SubTask(
                            task_id=make_task_id(),
                            name=f"Modify files in {dir_path}",
                            description=f"Modify these files according to the task: {files}",
                            priority="MEDIUM",
                            dependencies=[
                                t.task_id for t in subtasks if t.name.startswith("Analyze")
                            ],
                        )
                    )

        # File creation tasks
        if task.files_to_create:
            # Group by type/purpose if possible
            for file_path in task.files_to_create:
                subtasks.append(
                    SubTask(
                        task_id=make_task_id(),
                        name=f"Create {Path(file_path).name}",
                        description=f"Create new file: {file_path}",
                        priority="HIGH" if file_path.endswith((".py", ".ts", ".js")) else "MEDIUM",
                        dependencies=[t.task_id for t in subtasks if t.name.startswith("Analyze")],
                    )
                )

        # Code generation tasks
        if task.requires_code_generation and not subtasks:
            # If no file-specific tasks, create generic code generation task
            subtasks.append(
                SubTask(
                    task_id=make_task_id(),
                    name="Generate implementation",
                    description="Generate the code implementation for the specified task",
                    priority="HIGH",
                    dependencies=[],
                )
            )

        # Synthesis usually comes last
        if task.requires_synthesis or len(subtasks) > 3:
            synthesis_deps = [t.task_id for t in subtasks]
            subtasks.append(
                SubTask(
                    task_id=make_task_id(),
                    name="Synthesize and integrate results",
                    description="Review all completed work and ensure coherent integration",
                    priority="HIGH",
                    dependencies=synthesis_deps,
                )
            )

        # If no specific decomposition was possible, create generic phases
        if not subtasks:
            subtasks = [
                SubTask(
                    task_id="T001",
                    name="Initial analysis and planning",
                    description="Analyze the task requirements and create an implementation plan",
                    priority="HIGH",
                ),
                SubTask(
                    task_id="T002",
                    name="Core implementation",
                    description="Implement the main functionality",
                    priority="HIGH",
                    dependencies=["T001"],
                ),
                SubTask(
                    task_id="T003",
                    name="Testing and refinement",
                    description="Test the implementation and refine as needed",
                    priority="MEDIUM",
                    dependencies=["T002"],
                ),
            ]

        return subtasks

    async def create_sacred_intention(self, task: Task, subtasks: list[SubTask]) -> str:
        """
        Create the sacred intention text for a Loom ceremony

        Args:
            task: The original task
            subtasks: The decomposed subtasks

        Returns:
            Sacred intention text (2-3 paragraphs)
        """
        intention = f"""The purpose of this ceremony is to accomplish a task that exceeds the capacity of any single consciousness: {task.description}

This work has been transformed into {len(subtasks)} interconnected movements that will be woven together through the Loom. Each chasqui runner will contribute their thread to the larger tapestry, maintaining coherence through the shared khipu_thread that binds us all.

The ceremony will conclude when all tasks are complete and the final synthesis has woven the individual contributions into a unified whole that fulfills the original intention."""

        # Add context-specific details
        if task.files_to_modify:
            intention += (
                f"\n\nThis ceremony will modify {len(task.files_to_modify)} existing files."
            )
        if task.files_to_create:
            intention += f"\n\nThis ceremony will create {len(task.files_to_create)} new files."

        return intention

    async def invoke_loom_for_task(
        self, task: Task, current_context_usage: float = 0.0
    ) -> dict[str, Any] | None:
        """
        High-level method to handle the full Loom invocation for a task

        Args:
            task: The task to potentially send to the Loom
            current_context_usage: Current context usage

        Returns:
            Loom invocation result or None if Loom not needed
        """
        # Check if Loom is needed
        should_use, reason = await self.should_use_loom(task, current_context_usage)

        if not should_use:
            logger.info(f"Task can be handled without Loom: {reason}")
            return None

        logger.info(f"Invoking Loom for task: {reason}")

        # Transform the task into movements
        subtasks = await self.transform_into_movements(task)

        # Create sacred intention
        sacred_intention = await self.create_sacred_intention(task, subtasks)

        # Convert subtasks to Loom format
        loom_tasks = [
            {
                "id": st.task_id,
                "name": st.name,
                "description": st.description,
                "priority": st.priority,
                "dependencies": st.dependencies,
            }
            for st in subtasks
        ]

        # Invoke the Loom
        result = await invoke_loom(
            ceremony_name=task.description[:50],  # First 50 chars as name
            sacred_intention=sacred_intention,
            tasks=loom_tasks,
            convening_weaver=self.instance_name,
        )

        if "ceremony_id" in result:
            self.current_ceremony_id = result["ceremony_id"]

        return result

    async def await_ceremony_completion(
        self, ceremony_id: str | None = None, check_interval: int = 30
    ) -> dict[str, Any]:
        """
        Wait for a Loom ceremony to complete

        Args:
            ceremony_id: Ceremony to wait for (uses current if not specified)
            check_interval: How often to check status (seconds)

        Returns:
            Final ceremony status
        """
        ceremony_id = ceremony_id or self.current_ceremony_id
        if not ceremony_id:
            raise ValueError("No ceremony ID specified or current")

        while True:
            status = await check_loom_status(ceremony_id)

            if status.get("status") in ["COMPLETE", "FAILED", "NOT_FOUND"]:
                return status

            logger.info(
                f"Ceremony {ceremony_id}: {status.get('tasks_complete', 0)}/{status.get('tasks_total', '?')} tasks complete"
            )

            await asyncio.sleep(check_interval)

    async def synthesize_ceremony_results(self, khipu_path: str) -> str:
        """
        Read and synthesize the results from a completed ceremony

        Args:
            khipu_path: Path to the ceremony's khipu_thread.md

        Returns:
            Synthesized summary of the ceremony results
        """
        try:
            content = Path(khipu_path).read_text()

            # Extract key sections
            synthesis_start = content.find("## Synthesis Space")
            ceremony_log_start = content.find("## Ceremony Log")

            if synthesis_start > 0:
                synthesis_section = content[
                    synthesis_start : ceremony_log_start if ceremony_log_start > 0 else None
                ]
            else:
                synthesis_section = "No synthesis section found"

            # Count completed tasks
            completed_count = content.count("*Status: COMPLETE*")
            failed_count = content.count("*Status: FAILED*")

            summary = f"""Ceremony Results Summary:

Tasks Completed: {completed_count}
Tasks Failed: {failed_count}

Key Insights from Synthesis:
{synthesis_section}

Full details available in: {khipu_path}
"""

            return summary

        except Exception as e:
            logger.error(f"Error synthesizing results: {e}")
            return f"Error reading ceremony results: {str(e)}"
