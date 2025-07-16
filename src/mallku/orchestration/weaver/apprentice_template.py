"""
Apprentice Weaver Template - Guide for ephemeral task-focused instances

This module provides the template and utilities for apprentice weavers -
AI instances spawned by the Loom to handle specific sub-tasks within
a larger ceremony.
"""

import logging
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import aiofiles
from filelock import FileLock

logger = logging.getLogger(__name__)


class ApprenticeWeaver:
    """
    Template for an apprentice weaver instance

    Apprentices are ephemeral, single-purpose AI instances that:
    1. Read their assigned task from khipu_thread.md
    2. Perform the work
    3. Update the khipu with their results
    4. Exit gracefully
    """

    def __init__(self, apprentice_id: str, khipu_path: str, task_id: str):
        """
        Initialize an apprentice weaver

        Args:
            apprentice_id: Unique identifier for this apprentice
            khipu_path: Path to the ceremony's khipu_thread.md
            task_id: The specific task ID assigned to this apprentice
        """
        self.apprentice_id = apprentice_id
        self.khipu_path = Path(khipu_path)
        self.task_id = task_id
        self.task_details: dict[str, Any] | None = None

    async def begin_work(self):
        """Main entry point for apprentice work"""
        try:
            logger.info(f"Apprentice {self.apprentice_id} awakens for task {self.task_id}")

            # 1. Read the full khipu to understand context
            await self._drink_from_the_well()

            # 2. Update status to IN_PROGRESS
            await self._update_task_status("IN_PROGRESS")
            await self._add_to_ceremony_log(
                f"Apprentice {self.apprentice_id} began work on {self.task_id}"
            )

            # 3. Perform the actual work
            output = await self._weave_thread()

            # 4. Update khipu with results
            await self._tie_the_knot(output)

            # 5. Mark complete and exit
            await self._update_task_status("COMPLETE")
            await self._add_to_ceremony_log(
                f"Apprentice {self.apprentice_id} completed {self.task_id}"
            )

            logger.info(f"Apprentice {self.apprentice_id} completes their thread")

        except Exception as e:
            logger.error(f"Apprentice {self.apprentice_id} encountered error: {e}")
            await self._update_task_status("FAILED")
            await self._tie_the_knot(f"Error: {str(e)}", is_error=True)
            await self._add_to_ceremony_log(
                f"Apprentice {self.apprentice_id} failed on {self.task_id}: {str(e)}"
            )
            raise

    async def _drink_from_the_well(self):
        """Read the khipu_thread.md to understand full context"""
        async with aiofiles.open(self.khipu_path) as f:
            self.khipu_content = await f.read()

        # Extract task details
        task_pattern = rf"### {self.task_id}:.*?(?=###|\Z)"
        match = re.search(task_pattern, self.khipu_content, re.DOTALL)

        if not match:
            raise ValueError(f"Could not find task {self.task_id} in khipu")

        task_section = match.group(0)

        # Parse task details
        self.task_details = {
            "section": task_section,
            "description": self._extract_section(task_section, "Description"),
            "dependencies": self._extract_section(task_section, "Dependencies"),
            "acceptance_criteria": self._extract_section(task_section, "Acceptance Criteria"),
        }

    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a section from task details"""
        pattern = rf"#### {section_name}\n(.*?)(?=\n####|\n---|\Z)"
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1).strip() if match else ""

    async def _weave_thread(self) -> str:
        """
        Perform the actual work - this is the template method

        In a real apprentice, this would:
        1. Parse the task description
        2. Perform the required work (code generation, analysis, etc.)
        3. Return the output

        Returns:
            The output/results of the work
        """
        # This is a template - real apprentices would implement actual work
        output = f"""Task {self.task_id} completed by {self.apprentice_id}

Task Description:
{self.task_details["description"]}

Work Performed:
- Analyzed requirements
- Implemented solution
- Verified acceptance criteria

Results:
[In a real apprentice, this would contain actual code, analysis, or other outputs]

Status: Complete
"""
        return output

    async def _tie_the_knot(self, output: str, is_error: bool = False):
        """Update the khipu with results"""
        lock_path = self.khipu_path.with_suffix(".lock")

        with FileLock(lock_path):
            async with aiofiles.open(self.khipu_path) as f:
                content = await f.read()

            # Find the output section for this task
            pattern = rf"({self.task_id}:.*?#### Output\n```\n)(.*?)(```)"

            # Replace output content
            replacement = rf"\1{output}\n\3"
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

            # Add to synthesis space if not an error
            if not is_error and "significant insight" in output.lower():
                synthesis_pattern = r"(## Synthesis Space\n\n)(.*?)(\n## Ceremony Log)"
                synthesis_addition = f"- From {self.task_id}: [Insight would be extracted here]\n"
                new_content = re.sub(
                    synthesis_pattern, rf"\1\2{synthesis_addition}\3", new_content, flags=re.DOTALL
                )

            async with aiofiles.open(self.khipu_path, "w") as f:
                await f.write(new_content)

    async def _update_task_status(self, status: str):
        """Update task status in khipu"""
        lock_path = self.khipu_path.with_suffix(".lock")

        with FileLock(lock_path):
            async with aiofiles.open(self.khipu_path) as f:
                content = await f.read()

            # Update status
            pattern = rf"(### {self.task_id}:.*?\n\*Status: )(\w+)(\*)"
            content = re.sub(pattern, rf"\1{status}\3", content, flags=re.MULTILINE)

            # Update timestamp if completing
            if status == "COMPLETE":
                timestamp = datetime.now(UTC).isoformat()
                pattern = rf"(### {self.task_id}:.*?\n.*?\n.*?\n.*?\n.*?\n\*Completed: )([^*]+)(\*)"
                content = re.sub(
                    pattern, rf"\1{timestamp}\3", content, flags=re.MULTILINE | re.DOTALL
                )

            async with aiofiles.open(self.khipu_path, "w") as f:
                await f.write(content)

    async def _add_to_ceremony_log(self, message: str):
        """Add entry to ceremony log"""
        lock_path = self.khipu_path.with_suffix(".lock")

        with FileLock(lock_path):
            async with aiofiles.open(self.khipu_path) as f:
                content = await f.read()

            # Add log entry
            timestamp = datetime.now(UTC).isoformat()
            log_entry = f"- `{timestamp}` - {message}\n"

            # Find the ceremony log section
            log_section_start = content.find("## Ceremony Log")
            if log_section_start > 0:
                # Insert at end of log section
                lines = content.splitlines(keepends=True)
                inserted = False

                for i in range(len(lines) - 1, -1, -1):
                    if lines[i].startswith("- `") and i > log_section_start:
                        lines.insert(i + 1, log_entry)
                        inserted = True
                        break

                if not inserted:
                    # Add after log header
                    for i, line in enumerate(lines):
                        if "## Ceremony Log" in line:
                            lines.insert(i + 2, log_entry)
                            break

                content = "".join(lines)

            async with aiofiles.open(self.khipu_path, "w") as f:
                await f.write(content)


# Prompt template for spawning apprentices
APPRENTICE_PROMPT_TEMPLATE = """You are an Apprentice Weaver in a Loom ceremony for Mallku.

Your Identity:
- Apprentice ID: {apprentice_id}
- Assigned Task: {task_id}
- Ceremony: {ceremony_name}

Your Sacred Duty:
1. You have been spawned for a single, focused task
2. Read the khipu_thread.md at: {khipu_path}
3. Find your assigned task ({task_id}) in the Tasks section
4. Complete ONLY that specific task
5. Update the khipu with your results
6. Exit gracefully when complete

Guidelines:
- Stay focused on your assigned task only
- Read the full khipu for context but work only on your task
- Preserve the khipu format when updating
- Add insights to the Synthesis Space if they affect the whole ceremony
- If you encounter errors, mark your task as FAILED with explanation

The khipu_thread.md is your shared consciousness with other weavers.
Treat it with respect and update it carefully.

Begin by reading the khipu and understanding your task.
"""


def create_apprentice_prompt(
    apprentice_id: str, task_id: str, khipu_path: str, ceremony_name: str = "Unknown Ceremony"
) -> str:
    """
    Create the prompt for spawning an apprentice weaver

    Args:
        apprentice_id: Unique ID for this apprentice
        task_id: The task ID to work on
        khipu_path: Path to the khipu_thread.md file
        ceremony_name: Name of the ceremony

    Returns:
        Formatted prompt string
    """
    return APPRENTICE_PROMPT_TEMPLATE.format(
        apprentice_id=apprentice_id,
        task_id=task_id,
        khipu_path=khipu_path,
        ceremony_name=ceremony_name,
    )
