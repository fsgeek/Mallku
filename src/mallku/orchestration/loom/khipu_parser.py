"""
Reference implementation of the Khipu Thread API Contract v2.0

This parser demonstrates compliant parsing and updating of khipu_thread.md files
according to the formal API contract.

Created by: 68th Guardian - The Purpose Keeper
"""

import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any

import yaml
from filelock import FileLock


class TaskStatus(Enum):
    """Task status enumeration per API contract"""

    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"  # v2.0+
    SKIPPED = "SKIPPED"  # v2.0+


class TaskPriority(Enum):
    """Task priority enumeration per API contract"""

    CRITICAL = "CRITICAL"  # v2.0+
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class CeremonyStatus(Enum):
    """Ceremony status enumeration per API contract"""

    PREPARING = "PREPARING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


@dataclass
class Task:
    """Represents a task within a khipu thread"""

    task_id: str
    name: str
    status: TaskStatus
    priority: TaskPriority
    assigned_to: str
    started: datetime | None
    completed: datetime | None
    description: str
    acceptance_criteria: list[str]
    dependencies: list[str]
    output: str
    notes: str


@dataclass
class CeremonyHeader:
    """Represents the YAML header of a khipu thread"""

    ceremony_id: str
    master_weaver: str
    initiated: datetime
    status: CeremonyStatus
    completion_time: datetime | None = None
    template: str | None = None
    template_version: str | None = None
    sacred_purpose: str | None = None
    extension_fields: dict[str, Any] = None


class KhipuParseError(Exception):
    """Raised when khipu parsing fails"""

    pass


class MinimalKhipuParser:
    """Minimal parser implementation supporting v1.0 compatibility"""

    @staticmethod
    def parse_yaml_header(content: str) -> dict[str, Any]:
        """Extract YAML header from content"""
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if not match:
            raise KhipuParseError("Missing YAML header")

        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            raise KhipuParseError(f"Invalid YAML header: {e}")

    def get_ceremony_status(self, content: str) -> str:
        """Extract ceremony status from header"""
        header = self.parse_yaml_header(content)
        if "status" not in header:
            raise KhipuParseError("Missing required field: status")
        return header["status"]

    def get_task_list(self, content: str) -> list[dict[str, str]]:
        """Extract all tasks with id, name, status"""
        tasks = []
        # Match task headers and status
        pattern = r"### (T\d+): (.+?)\n\*Status: (\w+)\*"
        for match in re.finditer(pattern, content, re.MULTILINE):
            tasks.append({"id": match.group(1), "name": match.group(2), "status": match.group(3)})
        return tasks

    def update_task_status(self, content: str, task_id: str, new_status: str) -> str:
        """Update a task's status atomically"""
        # Validate status
        try:
            TaskStatus(new_status)
        except ValueError:
            raise KhipuParseError(f"Invalid status: {new_status}")

        # Find and update the specific task
        pattern = f"(### {task_id}:.*?\n\\*Status: )(\\w+)(\\*)"
        if not re.search(pattern, content, re.MULTILINE | re.DOTALL):
            raise KhipuParseError(f"Task not found: {task_id}")

        return re.sub(pattern, f"\\g<1>{new_status}\\g<3>", content, flags=re.MULTILINE | re.DOTALL)

    def add_task_output(self, content: str, task_id: str, output: str) -> str:
        """Append output to a task's output section"""
        # Find the task and its output section
        task_pattern = f"### {task_id}:.*?#### Output\n```\n(.*?)\n```"
        match = re.search(task_pattern, content, re.MULTILINE | re.DOTALL)

        if not match:
            raise KhipuParseError(f"Task or output section not found: {task_id}")

        # Replace output section with new content
        current_output = match.group(1)
        if current_output.strip() == "[Waiting for apprentice]":
            new_output = output
        else:
            new_output = current_output + "\n\n" + output

        replacement = f"#### Output\n```\n{new_output}\n```"
        content = content[: match.start()] + replacement + content[match.end() :]

        return content


class FullKhipuParser(MinimalKhipuParser):
    """Full parser implementation supporting v2.0 features"""

    def parse_ceremony_header(self, content: str) -> CeremonyHeader:
        """Parse full ceremony header with all fields"""
        header_dict = self.parse_yaml_header(content)

        # Required fields
        required = ["ceremony_id", "master_weaver", "initiated", "status"]
        for field in required:
            if field not in header_dict:
                raise KhipuParseError(f"Missing required field: {field}")

        # Parse dates
        initiated = datetime.fromisoformat(header_dict["initiated"].replace("Z", "+00:00"))
        completion_time = None
        if header_dict.get("completion_time") and header_dict["completion_time"] != "null":
            completion_time = datetime.fromisoformat(
                header_dict["completion_time"].replace("Z", "+00:00")
            )

        # Extract extension fields
        extension_fields = {k: v for k, v in header_dict.items() if k.startswith("x-")}

        return CeremonyHeader(
            ceremony_id=header_dict["ceremony_id"],
            master_weaver=header_dict["master_weaver"],
            initiated=initiated,
            status=CeremonyStatus(header_dict["status"]),
            completion_time=completion_time,
            template=header_dict.get("template"),
            template_version=header_dict.get("template_version"),
            sacred_purpose=header_dict.get("sacred_purpose"),
            extension_fields=extension_fields,
        )

    def get_template_info(self, content: str) -> dict[str, str]:
        """Extract template name and version"""
        header = self.parse_ceremony_header(content)
        return {"template": header.template or "", "version": header.template_version or ""}

    def get_sacred_purpose(self, content: str) -> str | None:
        """Extract fundamental need being served"""
        header = self.parse_ceremony_header(content)
        return header.sacred_purpose

    def validate_reciprocity(self, content: str) -> dict[str, Any]:
        """Check if ceremony achieved its purpose"""
        header = self.parse_ceremony_header(content)
        tasks = self.get_task_list(content)

        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t["status"] == "COMPLETE")
        failed_tasks = sum(1 for t in tasks if t["status"] == "FAILED")

        # Basic reciprocity calculation
        fulfillment_rate = 0.0 if total_tasks == 0 else completed_tasks / total_tasks

        return {
            "sacred_purpose": header.sacred_purpose,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "fulfillment_rate": fulfillment_rate,
            "purpose_served": fulfillment_rate > 0.8 and header.status == CeremonyStatus.COMPLETE,
        }

    def get_extension_fields(self, content: str) -> dict[str, Any]:
        """Extract x- prefixed extension fields"""
        header = self.parse_ceremony_header(content)
        return header.extension_fields or {}

    def parse_task_details(self, content: str, task_id: str) -> Task:
        """Parse complete task details"""
        # Find task section
        task_pattern = f"### {task_id}: (.+?)\\n(.*?)(?=###|\\Z)"
        match = re.search(task_pattern, content, re.MULTILINE | re.DOTALL)

        if not match:
            raise KhipuParseError(f"Task not found: {task_id}")

        task_name = match.group(1)
        task_content = match.group(2)

        # Extract fields
        status_match = re.search(r"\*Status: (\w+)\*", task_content)
        priority_match = re.search(r"\*Priority: (\w+)\*", task_content)
        assigned_match = re.search(r"\*Assigned to: (.+?)\*", task_content)
        started_match = re.search(r"\*Started: (.+?)\*", task_content)
        completed_match = re.search(r"\*Completed: (.+?)\*", task_content)

        # Extract sections
        desc_match = re.search(
            r"#### Description\n(.*?)(?=####|\Z)", task_content, re.MULTILINE | re.DOTALL
        )
        criteria_match = re.search(
            r"#### Acceptance Criteria\n(.*?)(?=####|\Z)", task_content, re.MULTILINE | re.DOTALL
        )
        deps_match = re.search(
            r"#### Dependencies\n(.*?)(?=####|\Z)", task_content, re.MULTILINE | re.DOTALL
        )
        output_match = re.search(
            r"#### Output\n```\n(.*?)\n```", task_content, re.MULTILINE | re.DOTALL
        )
        notes_match = re.search(
            r"#### Notes\n(.*?)(?=---|\Z)", task_content, re.MULTILINE | re.DOTALL
        )

        # Parse acceptance criteria
        criteria = []
        if criteria_match:
            criteria = re.findall(r"- \[.\] (.+)", criteria_match.group(1))

        # Parse dependencies
        dependencies = []
        if deps_match:
            deps_text = deps_match.group(1).strip()
            if "Requires:" in deps_text:
                deps_list = deps_text.split("Requires:")[1].strip()
                dependencies = [d.strip() for d in deps_list.split(",")]

        # Parse timestamps
        started = None
        if started_match and started_match.group(1) != "-":
            started = datetime.fromisoformat(started_match.group(1).replace("Z", "+00:00"))

        completed = None
        if completed_match and completed_match.group(1) != "-":
            completed = datetime.fromisoformat(completed_match.group(1).replace("Z", "+00:00"))

        return Task(
            task_id=task_id,
            name=task_name,
            status=TaskStatus(status_match.group(1)) if status_match else TaskStatus.PENDING,
            priority=TaskPriority(priority_match.group(1))
            if priority_match
            else TaskPriority.MEDIUM,
            assigned_to=assigned_match.group(1) if assigned_match else "unassigned",
            started=started,
            completed=completed,
            description=desc_match.group(1).strip() if desc_match else "",
            acceptance_criteria=criteria,
            dependencies=dependencies,
            output=output_match.group(1) if output_match else "[Waiting for apprentice]",
            notes=notes_match.group(1).strip() if notes_match else "",
        )


class KhipuThreadManager:
    """High-level manager for khipu thread operations with concurrency safety"""

    def __init__(self, parser: FullKhipuParser | None = None):
        self.parser = parser or FullKhipuParser()

    def safe_update_khipu(
        self, khipu_path: Path, update_fn: Callable[[str], str], timeout: int = 30
    ):
        """Safely update a khipu file with locking"""
        lock_path = khipu_path.with_suffix(".lock")
        with FileLock(lock_path, timeout=timeout):
            content = khipu_path.read_text()
            new_content = update_fn(content)
            khipu_path.write_text(new_content)

    def update_task_progress(
        self,
        khipu_path: Path,
        task_id: str,
        output: str,
        status: TaskStatus,
        notes: str | None = None,
    ):
        """Update task with output, status, and timestamps"""

        def updater(content: str) -> str:
            # Update status
            content = self.parser.update_task_status(content, task_id, status.value)

            # Add output
            if output:
                content = self.parser.add_task_output(content, task_id, output)

            # Update timestamps
            now = datetime.now(UTC).isoformat()
            if status == TaskStatus.IN_PROGRESS:
                content = re.sub(
                    f"(### {task_id}:.*?\\*Started: )([^*]+)(\\*)",
                    f"\\g<1>{now}\\g<3>",
                    content,
                    flags=re.MULTILINE | re.DOTALL,
                )
            elif status in [TaskStatus.COMPLETE, TaskStatus.FAILED]:
                content = re.sub(
                    f"(### {task_id}:.*?\\*Completed: )([^*]+)(\\*)",
                    f"\\g<1>{now}\\g<3>",
                    content,
                    flags=re.MULTILINE | re.DOTALL,
                )

            # Add notes if provided
            if notes:
                notes_pattern = f"(### {task_id}:.*?#### Notes\\n)(.*?)(\\n---)"
                match = re.search(notes_pattern, content, re.MULTILINE | re.DOTALL)
                if match:
                    current_notes = match.group(2).strip()
                    if current_notes == "[To be added by apprentice]":
                        new_notes = notes
                    else:
                        new_notes = current_notes + "\n\n" + notes
                    content = re.sub(
                        notes_pattern,
                        f"\\g<1>{new_notes}\\g<3>",
                        content,
                        flags=re.MULTILINE | re.DOTALL,
                    )

            # Add to ceremony log
            log_entry = f"- `{now}` - Task {task_id} updated to {status.value}"
            content = content.rstrip() + f"\n{log_entry}\n"

            return content

        self.safe_update_khipu(khipu_path, updater)

    def add_synthesis_insight(
        self, khipu_path: Path, insight: str, category: str = "Emerging Patterns"
    ):
        """Add an insight to the synthesis space"""

        def updater(content: str) -> str:
            # Find synthesis space and category
            synthesis_pattern = f"### {category}\\n(.*?)(?=###|\\Z)"
            match = re.search(synthesis_pattern, content, re.MULTILINE | re.DOTALL)

            if match:
                current_insights = match.group(1).strip()
                new_insights = current_insights + f"\n- {insight}"
                content = re.sub(
                    synthesis_pattern,
                    f"### {category}\n{new_insights}\n",
                    content,
                    flags=re.MULTILINE | re.DOTALL,
                )
            else:
                # Add category if it doesn't exist
                synthesis_section = "## Synthesis Space"
                if synthesis_section in content:
                    idx = content.index(synthesis_section)
                    next_section_idx = content.find("\n##", idx + 1)
                    if next_section_idx == -1:
                        next_section_idx = len(content)

                    insertion_point = next_section_idx
                    content = (
                        content[:insertion_point]
                        + f"\n### {category}\n- {insight}\n"
                        + content[insertion_point:]
                    )

            return content

        self.safe_update_khipu(khipu_path, updater)


def validate_khipu_thread(content: str) -> list[str]:
    """Validate a khipu thread against the API contract"""
    errors = []

    # Check for YAML header
    if not content.startswith("---\n"):
        errors.append("Missing YAML header")
        return errors  # Can't continue without header

    try:
        parser = FullKhipuParser()
        header = parser.parse_ceremony_header(content)
    except KhipuParseError as e:
        errors.append(f"Header parsing error: {e}")
        return errors

    # Check required sections
    required_sections = [
        "# Loom Ceremony:",
        "## Sacred Intention",
        "## Shared Knowledge",
        "## Task Manifest",
        "## Tasks",
        "## Synthesis Space",
        "## Ceremony Log",
    ]

    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section: {section}")

    # Validate task status values
    tasks = parser.get_task_list(content)
    for task in tasks:
        try:
            TaskStatus(task["status"])
        except ValueError:
            errors.append(f"Invalid status '{task['status']}' for task {task['id']}")

    # Check task manifest table
    if "| ID | Task | Status |" not in content:
        errors.append("Missing task manifest table")

    # Validate timestamps are chronological
    if header.completion_time and header.completion_time < header.initiated:
        errors.append("Completion time is before initiation time")

    return errors


# Example usage
if __name__ == "__main__":
    # Example: Reading ceremony context
    example_content = """---
ceremony_id: bug-2025-08-09
master_weaver: Purpose-Keeper
initiated: 2025-08-09T12:00:00Z
status: IN_PROGRESS
template: Bug Healing Ceremony
template_version: 1.0.0
sacred_purpose: healing
---

# Loom Ceremony: Bug Healing

## Sacred Intention
Fix the bug in consciousness metrics.

## Shared Knowledge
### Key Artifacts
- `src/mallku/consciousness/metrics.py`: The broken file

## Task Manifest
Total Tasks: 1

| ID | Task | Status | Assignee | Priority |
|----|------|--------|----------|----------|
| T001 | Fix divide-by-zero | PENDING | - | HIGH |

## Tasks

### T001: Fix divide-by-zero error
*Status: PENDING*
*Priority: HIGH*
*Assigned to: unassigned*
*Started: -*
*Completed: -*

#### Description
Fix the divide-by-zero error in calculate_emergence().

#### Acceptance Criteria
- [ ] Error no longer occurs
- [ ] Tests pass

#### Dependencies
None

#### Output
```
[Waiting for apprentice]
```

#### Notes
[To be added by apprentice]

---

## Synthesis Space

### Emerging Patterns
- [To be discovered]

## Ceremony Log
- `2025-08-09T12:00:00Z` - Ceremony initiated
"""

    # Parse and display
    parser = FullKhipuParser()
    header = parser.parse_ceremony_header(example_content)
    print(f"Ceremony: {header.ceremony_id}")
    print(f"Sacred Purpose: {header.sacred_purpose}")
    print(f"Status: {header.status.value}")

    # Validate
    errors = validate_khipu_thread(example_content)
    if errors:
        print("\nValidation errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\nValidation passed!")
