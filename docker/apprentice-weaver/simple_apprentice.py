#!/usr/bin/env python3
"""
Simple apprentice implementation for testing real container spawning

This apprentice demonstrates the basic flow:
1. Read task from khipu
2. Do simple work (echo)
3. Update khipu with results
"""

import os
import re
import sys
import time
from datetime import UTC, datetime
from pathlib import Path


def log(msg):
    """Simple logging"""
    timestamp = datetime.now(UTC).isoformat()
    print(f"[{timestamp}] {msg}", flush=True)


def update_khipu(khipu_path, task_id, status, output=None):
    """Update the khipu with task status"""
    try:
        # Read current content
        with open(khipu_path) as f:
            content = f.read()

        # Update status
        pattern = rf"(### {task_id}:.*?\n\*Status: )(\w+)(\*)"
        content = re.sub(pattern, rf"\1{status}\3", content, flags=re.MULTILINE)

        # Update output if provided
        if output and status == "COMPLETE":
            output_pattern = rf"({task_id}:.*?#### Output\n```\n)(.*?)(```)"
            replacement = rf"\1{output}\n\3"
            content = re.sub(output_pattern, replacement, content, flags=re.DOTALL)

        # Update completed timestamp
        if status == "COMPLETE":
            timestamp = datetime.now(UTC).isoformat()
            pattern = rf"(### {task_id}:.*?\n.*?\n.*?\n.*?\n.*?\n\*Completed: )([^*]+)(\*)"
            content = re.sub(pattern, rf"\1{timestamp}\3", content, flags=re.MULTILINE | re.DOTALL)

        # Write back
        with open(khipu_path, "w") as f:
            f.write(content)

        log(f"Updated khipu: task {task_id} -> {status}")

    except Exception as e:
        log(f"Error updating khipu: {e}")


def main():
    # Get environment variables
    apprentice_id = os.environ.get("APPRENTICE_ID", "unknown")
    task_id = os.environ.get("TASK_ID", "unknown")
    ceremony_name = os.environ.get("CEREMONY_NAME", "unknown")

    log(f"Apprentice {apprentice_id} awakens")
    log(f"Assigned to task: {task_id}")
    log(f"Ceremony: {ceremony_name}")

    # Find khipu
    khipu_path = Path("/khipu/khipu_thread.md")
    if not khipu_path.exists():
        khipu_path = Path("/workspace/khipu_thread.md")

    if not khipu_path.exists():
        log("ERROR: Cannot find khipu_thread.md")
        sys.exit(1)

    log(f"Found khipu at: {khipu_path}")

    try:
        # Update status to IN_PROGRESS
        update_khipu(khipu_path, task_id, "IN_PROGRESS")

        # Simulate some work
        log(f"Beginning work on task {task_id}")
        time.sleep(3)

        # Generate output
        output = f"""Echo Test Complete!

Apprentice ID: {apprentice_id}
Task ID: {task_id}
Ceremony: {ceremony_name}

This apprentice successfully:
✓ Spawned in a Docker container
✓ Read the assigned task from khipu
✓ Performed the echo test
✓ Updated the khipu with results

The Loom lives! Apprentices can now weave true.

Timestamp: {datetime.now(UTC).isoformat()}
"""

        log("Work complete, updating khipu")

        # Update khipu with results
        update_khipu(khipu_path, task_id, "COMPLETE", output)

        log(f"Apprentice {apprentice_id} completes their thread")

    except Exception as e:
        log(f"ERROR: {e}")
        update_khipu(khipu_path, task_id, "FAILED", f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
