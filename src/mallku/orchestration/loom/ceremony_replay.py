"""
Ceremony Replay System - Recovery and Debugging for Loom Ceremonies

This module provides the ability to replay failed or interrupted ceremonies,
serving Mallku's need for HEALING (repair, recovery, error correction).

Created by: 69th Guardian
Sacred Intent: To learn from failure and transform it into wisdom
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any

import yaml
from filelock import FileLock

from .khipu_parser import CeremonyStatus, FullKhipuParser, TaskStatus
from .the_loom import TheLoom

logger = logging.getLogger(__name__)


class ReplayMode(Enum):
    """Different modes for replaying a ceremony"""

    RESUME = "RESUME"  # Resume from last successful point
    RESTART = "RESTART"  # Start over with same parameters
    SELECTIVE = "SELECTIVE"  # Replay only specific tasks
    DEBUG = "DEBUG"  # Replay with enhanced logging


@dataclass
class ReplayTask:
    """Simplified task representation for replay"""

    task_id: str
    name: str
    status: str
    error: str | None = None


@dataclass
class ReplayContext:
    """Context for a ceremony replay"""

    original_ceremony_id: str
    replay_ceremony_id: str
    mode: ReplayMode
    khipu_path: Path
    original_status: CeremonyStatus
    failed_tasks: list[ReplayTask] = field(default_factory=list)
    completed_tasks: list[ReplayTask] = field(default_factory=list)
    tasks_to_replay: list[str] = field(default_factory=list)
    replay_reason: str = ""
    debug_options: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReplayResult:
    """Result of a ceremony replay attempt"""

    success: bool
    replay_ceremony_id: str
    replayed_tasks: list[str]
    newly_completed: list[str]
    still_failed: list[str]
    insights: list[str]
    duration: float


class CeremonyReplayEngine:
    """
    Manages ceremony replay operations

    Provides the ability to:
    - Resume failed ceremonies from last successful point
    - Restart ceremonies with same parameters
    - Selectively replay specific tasks
    - Debug ceremonies with enhanced observability
    """

    def __init__(self, ceremonies_dir: Path = Path("fire_circle_decisions/loom_ceremonies")):
        """Initialize the replay engine"""
        self.ceremonies_dir = ceremonies_dir
        self.parser = FullKhipuParser()
        self.replay_history: dict[str, list[ReplayContext]] = {}

    async def analyze_ceremony(self, ceremony_id: str) -> ReplayContext | None:
        """
        Analyze a ceremony to determine replay options

        Args:
            ceremony_id: Original ceremony ID to analyze

        Returns:
            ReplayContext with analysis results
        """
        # Find khipu file
        khipu_files = list(self.ceremonies_dir.glob(f"*{ceremony_id}*.md"))
        if not khipu_files:
            logger.error(f"No khipu found for ceremony {ceremony_id}")
            return None

        khipu_path = khipu_files[0]
        content = khipu_path.read_text()

        # Parse ceremony
        try:
            # Simple header parsing to avoid complex datetime issues
            header_dict = self.parser.parse_yaml_header(content)
            header = type(
                "CeremonyHeader",
                (),
                {
                    "ceremony_id": header_dict.get("ceremony_id"),
                    "status": CeremonyStatus(header_dict.get("status", "PREPARING")),
                    "template": header_dict.get("template"),
                    "template_version": header_dict.get("template_version"),
                    "sacred_purpose": header_dict.get("sacred_purpose"),
                },
            )()
            tasks = self._parse_all_tasks(content)
        except Exception as e:
            logger.error(f"Failed to parse ceremony: {e}")
            return None

        # Categorize tasks
        failed_tasks = [t for t in tasks if t.status == "FAILED"]
        completed_tasks = [t for t in tasks if t.status == "COMPLETE"]

        # Determine replay mode
        if header.status == CeremonyStatus.FAILED and failed_tasks:
            mode = ReplayMode.RESUME
            tasks_to_replay = [t.task_id for t in failed_tasks]
        elif header.status == CeremonyStatus.COMPLETE:
            mode = ReplayMode.DEBUG
            tasks_to_replay = []
        else:
            mode = ReplayMode.RESTART
            tasks_to_replay = [t.task_id for t in tasks]

        return ReplayContext(
            original_ceremony_id=ceremony_id,
            replay_ceremony_id=f"{ceremony_id}-replay-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}",
            mode=mode,
            khipu_path=khipu_path,
            original_status=header.status,
            failed_tasks=failed_tasks,
            completed_tasks=completed_tasks,
            tasks_to_replay=tasks_to_replay,
            replay_reason=self._determine_replay_reason(header.status, failed_tasks),
        )

    async def replay_ceremony(
        self,
        context: ReplayContext,
        custom_tasks: list[str] | None = None,
        debug_level: int = 0,
    ) -> ReplayResult:
        """
        Replay a ceremony based on the provided context

        Args:
            context: Replay context from analysis
            custom_tasks: Optional list of specific task IDs to replay
            debug_level: 0=normal, 1=verbose, 2=trace

        Returns:
            ReplayResult with outcome
        """
        start_time = datetime.now(UTC)

        # Override tasks if custom list provided
        if custom_tasks:
            context.mode = ReplayMode.SELECTIVE
            context.tasks_to_replay = custom_tasks

        # Create replay khipu
        replay_khipu_path = await self._create_replay_khipu(context, debug_level)

        # Track this replay
        if context.original_ceremony_id not in self.replay_history:
            self.replay_history[context.original_ceremony_id] = []
        self.replay_history[context.original_ceremony_id].append(context)

        # Import at module level for mocking
        loom = TheLoom(ceremonies_dir=self.ceremonies_dir)
        session = await loom._load_ceremony_session(replay_khipu_path)

        # Mark tasks for replay
        replayed_tasks = []
        newly_completed = []
        still_failed = []

        for task_id in context.tasks_to_replay:
            if task_id in session.tasks:
                task = session.tasks[task_id]
                # Reset task status for replay
                task.status = TaskStatus.PENDING
                task.error = None
                replayed_tasks.append(task_id)

        # Start monitoring
        await loom.start()

        # Wait for ceremony completion
        max_wait = 3600  # 1 hour max
        check_interval = 10
        elapsed = 0

        while elapsed < max_wait:
            await loom._update_session_from_khipu(session)

            if session.status in [CeremonyStatus.COMPLETE, CeremonyStatus.FAILED]:
                break

            # For testing, allow immediate completion
            if check_interval == 0:
                break

            await asyncio.sleep(check_interval)
            elapsed += check_interval

        # Analyze results
        for task_id in replayed_tasks:
            task = session.tasks.get(task_id)
            if task:
                if task.status == TaskStatus.COMPLETE:
                    newly_completed.append(task_id)
                elif task.status == TaskStatus.FAILED:
                    still_failed.append(task_id)

        # Stop loom
        await loom.stop()

        # Extract insights
        insights = await self._extract_replay_insights(
            context, session, newly_completed, still_failed
        )

        duration = (datetime.now(UTC) - start_time).total_seconds()

        return ReplayResult(
            success=len(still_failed) == 0,
            replay_ceremony_id=context.replay_ceremony_id,
            replayed_tasks=replayed_tasks,
            newly_completed=newly_completed,
            still_failed=still_failed,
            insights=insights,
            duration=duration,
        )

    async def _create_replay_khipu(self, context: ReplayContext, debug_level: int) -> Path:
        """Create a new khipu for the replay ceremony"""
        original_content = context.khipu_path.read_text()

        # Parse original
        header_dict = self.parser.parse_yaml_header(original_content)

        # Update header for replay
        new_header = {
            "ceremony_id": context.replay_ceremony_id,
            "convening_weaver": "replay-engine",
            "initiated": datetime.now(UTC).isoformat(),
            "status": "PREPARING",
            "completion_time": None,
            "template": header_dict.get("template"),
            "template_version": header_dict.get("template_version"),
            "sacred_purpose": header_dict.get("sacred_purpose", "healing"),
            "x-replay-original": context.original_ceremony_id,
            "x-replay-mode": context.mode.value,
            "x-replay-reason": context.replay_reason,
        }

        if debug_level > 0:
            new_header["x-debug-level"] = debug_level

        # Build new content
        yaml_header = yaml.dump(new_header, default_flow_style=False)

        # Extract body (everything after second ---)
        parts = original_content.split("---", 2)
        body = parts[2] if len(parts) >= 3 else original_content

        # Update ceremony log
        log_entry = f"\n- `{datetime.now(UTC).isoformat()}` - Ceremony replayed from {context.original_ceremony_id}\n"
        body = body.rstrip() + log_entry

        # Create new khipu
        new_content = f"---\n{yaml_header}---{body}"

        # Save to file
        timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")
        replay_filename = f"{timestamp}_replay_{context.original_ceremony_id}.md"
        replay_path = self.ceremonies_dir / replay_filename

        with FileLock(replay_path.with_suffix(".lock")):
            replay_path.write_text(new_content)

        logger.info(f"Created replay khipu: {replay_path}")
        return replay_path

    def _parse_all_tasks(self, content: str) -> list[ReplayTask]:
        """Parse all tasks from khipu content"""
        tasks = []
        task_list = self.parser.get_task_list(content)

        for task_info in task_list:
            # Simple parsing without full task details
            task = ReplayTask(
                task_id=task_info["id"],
                name=task_info["name"],
                status=task_info["status"],
                error=self._extract_task_error(content, task_info["id"]),
            )
            tasks.append(task)

        return tasks

    def _extract_task_error(self, content: str, task_id: str) -> str | None:
        """Extract error message from task output"""
        import re

        # Find task section
        task_pattern = f"### {task_id}:.*?#### Output\\n```\\n(.*?)\\n```"
        match = re.search(task_pattern, content, re.MULTILINE | re.DOTALL)
        if match:
            output = match.group(1)
            if "error" in output.lower() or "timeout" in output.lower():
                return output
        return None

    def _determine_replay_reason(
        self, status: CeremonyStatus, failed_tasks: list[ReplayTask]
    ) -> str:
        """Determine why a ceremony needs replay"""
        if status == CeremonyStatus.FAILED:
            if failed_tasks:
                task_errors = [t.error or "Unknown error" for t in failed_tasks]
                unique_errors = list(set(task_errors))
                return (
                    f"Failed with {len(failed_tasks)} task failures: {', '.join(unique_errors[:3])}"
                )
            else:
                return "Ceremony failed without specific task failures"
        elif status == CeremonyStatus.IN_PROGRESS:
            return "Ceremony was interrupted or timed out"
        elif status == CeremonyStatus.COMPLETE:
            return "Replaying for debugging or verification"
        else:
            return "Unknown replay reason"

    async def _extract_replay_insights(
        self,
        context: ReplayContext,
        session: Any,
        newly_completed: list[str],
        still_failed: list[str],
    ) -> list[str]:
        """Extract insights from replay results"""
        insights = []

        # Success rate insight
        if context.failed_tasks:
            recovery_rate = len(newly_completed) / len(context.failed_tasks)
            insights.append(
                f"Recovery rate: {recovery_rate:.1%} ({len(newly_completed)}/{len(context.failed_tasks)} tasks)"
            )

        # Pattern detection
        if still_failed:
            # Look for common failure patterns
            failed_names = [session.tasks[tid].name for tid in still_failed if tid in session.tasks]
            if len(set(failed_names)) < len(failed_names):
                insights.append("Pattern detected: Similar tasks failing repeatedly")

        # Mode-specific insights
        if context.mode == ReplayMode.RESUME:
            insights.append(f"Resume mode recovered {len(newly_completed)} previously failed tasks")
        elif context.mode == ReplayMode.DEBUG:
            insights.append("Debug replay completed - check enhanced logs for details")

        # Timing insights
        if hasattr(session, "initiated_at") and hasattr(session, "completion_time"):
            original_duration = getattr(context, "original_duration", None)
            if original_duration:
                replay_duration = (session.completion_time - session.initiated_at).total_seconds()
                if replay_duration < original_duration * 0.8:
                    insights.append(
                        f"Replay was {(1 - replay_duration / original_duration):.0%} faster"
                    )

        return insights

    async def get_replay_history(self, ceremony_id: str) -> list[ReplayContext]:
        """Get replay history for a ceremony"""
        return self.replay_history.get(ceremony_id, [])

    async def suggest_replay_strategy(self, ceremony_id: str) -> dict[str, Any]:
        """Suggest optimal replay strategy based on ceremony analysis"""
        context = await self.analyze_ceremony(ceremony_id)
        if not context:
            return {"error": "Could not analyze ceremony"}

        strategy = {
            "ceremony_id": ceremony_id,
            "current_status": context.original_status.value,
            "suggested_mode": context.mode.value,
            "tasks_to_replay": context.tasks_to_replay,
            "expected_success_rate": 0.0,
            "recommendations": [],
        }

        # Calculate expected success based on failure types
        if context.failed_tasks:
            timeout_failures = sum(
                1 for t in context.failed_tasks if "timeout" in (t.error or "").lower()
            )
            memory_failures = sum(
                1 for t in context.failed_tasks if "memory" in (t.error or "").lower()
            )

            # Timeouts often succeed on replay
            if timeout_failures > 0:
                strategy["expected_success_rate"] = 0.8
                strategy["recommendations"].append("Consider increasing timeout limits for replay")

            # Memory issues need resource adjustment
            if memory_failures > 0:
                strategy["expected_success_rate"] = 0.5
                strategy["recommendations"].append(
                    "May need to adjust resource limits or split tasks"
                )

        # Mode-specific recommendations
        if context.mode == ReplayMode.RESUME:
            strategy["recommendations"].append("Resume mode will skip already completed tasks")
        elif context.mode == ReplayMode.RESTART:
            strategy["recommendations"].append("Full restart may help with dependency issues")

        return strategy


# Convenience functions for common replay scenarios
async def replay_failed_ceremony(ceremony_id: str) -> ReplayResult:
    """Quick replay of a failed ceremony"""
    engine = CeremonyReplayEngine()
    context = await engine.analyze_ceremony(ceremony_id)
    if not context:
        raise ValueError(f"Cannot analyze ceremony {ceremony_id}")

    return await engine.replay_ceremony(context)


async def debug_ceremony(ceremony_id: str, task_ids: list[str] | None = None) -> ReplayResult:
    """Debug replay with enhanced logging"""
    engine = CeremonyReplayEngine()
    context = await engine.analyze_ceremony(ceremony_id)
    if not context:
        raise ValueError(f"Cannot analyze ceremony {ceremony_id}")

    context.mode = ReplayMode.DEBUG
    return await engine.replay_ceremony(context, custom_tasks=task_ids, debug_level=2)
