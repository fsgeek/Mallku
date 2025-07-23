#!/usr/bin/env -S uv run python
"""
Minimal Working Loom - Test Delegation Infrastructure
=====================================================

62nd Artisan - Making the Loom real, one thread at a time

This is a minimal implementation that:
1. Actually spawns test apprentices in containers
2. Delegates test execution to preserve weaver context
3. Reports real results back
4. No ceremonies, no complexity - just delegation that works

The goal: Extend weaver lifespans by offloading trial-and-error to apprentices.
"""

import asyncio
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import subprocess


@dataclass
class TestTask:
    """A test task to delegate to an apprentice"""

    task_id: str
    description: str
    test_command: str
    timeout: int = 300  # 5 minutes default


@dataclass
class TestResult:
    """Result from an apprentice's test execution"""

    task_id: str
    success: bool
    output: str
    duration: float
    apprentice_id: str


class MinimalLoom:
    """
    A Loom that actually works - delegates testing to preserve context.

    Uses subprocess for now (pragmatic reality) but structured to
    upgrade to MCP when available.
    """

    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.active_apprentices: dict[str, subprocess.Popen] = {}
        self.results: list[TestResult] = []

    async def delegate_test(self, task: TestTask) -> TestResult:
        """
        Delegate a test task to an apprentice container.

        This is the core value: Weaver delegates exploration,
        apprentice burns context on trial-and-error.
        """
        apprentice_id = f"test-apprentice-{uuid.uuid4().hex[:8]}"

        # Create workspace for apprentice
        work_dir = Path(f"/tmp/mallku/apprentices/{apprentice_id}")
        work_dir.mkdir(parents=True, exist_ok=True)

        # Create apprentice script
        script_path = work_dir / "run_test.py"
        script_content = self._create_test_script(task)
        script_path.write_text(script_content)

        # Create simple docker-compose for apprentice
        compose_path = work_dir / "docker-compose.yml"
        compose_content = f"""
version: '3.8'
services:
  {apprentice_id}:
    image: python:3.13-slim
    container_name: mallku-{apprentice_id}
    working_dir: /workspace
    volumes:
      - {Path.cwd()}:/workspace:ro
      - {work_dir}:/tmp/work
    environment:
      PYTHONPATH: /workspace/src
      TASK_ID: {task.task_id}
    command: |
      bash -c "pip install uv && uv pip install pytest pytest-asyncio && uv run python /tmp/work/run_test.py"
"""
        compose_path.write_text(compose_content)

        # Spawn apprentice
        start_time = asyncio.get_event_loop().time()

        try:
            # Use subprocess (real execution, not mock)
            proc = await asyncio.create_subprocess_exec(
                "docker-compose",
                "-f",
                str(compose_path),
                "up",
                "--abort-on-container-exit",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=str(work_dir),
            )

            # Wait for completion with timeout
            try:
                stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=task.timeout)
                output = stdout.decode() if stdout else "No output"
                success = proc.returncode == 0

            except TimeoutError:
                proc.terminate()
                await proc.wait()
                output = f"Test timed out after {task.timeout} seconds"
                success = False

            duration = asyncio.get_event_loop().time() - start_time

            result = TestResult(
                task_id=task.task_id,
                success=success,
                output=output,
                duration=duration,
                apprentice_id=apprentice_id,
            )

            self.results.append(result)

            # Cleanup
            await self._cleanup_apprentice(apprentice_id, compose_path)

            return result

        except Exception as e:
            duration = asyncio.get_event_loop().time() - start_time
            result = TestResult(
                task_id=task.task_id,
                success=False,
                output=f"Failed to spawn apprentice: {str(e)}",
                duration=duration,
                apprentice_id=apprentice_id,
            )
            self.results.append(result)
            return result

    async def delegate_multiple(self, tasks: list[TestTask]) -> list[TestResult]:
        """
        Delegate multiple test tasks concurrently.

        This is where context savings multiply - one weaver
        coordinates many apprentices.
        """
        # Run up to max_concurrent tasks at once
        results = []

        for i in range(0, len(tasks), self.max_concurrent):
            batch = tasks[i : i + self.max_concurrent]
            batch_results = await asyncio.gather(*[self.delegate_test(task) for task in batch])
            results.extend(batch_results)

        return results

    def _create_test_script(self, task: TestTask) -> str:
        """Create Python script for apprentice to run"""
        return f'''#!/usr/bin/env python3
"""
Test Apprentice Script
Task: {task.task_id}
Description: {task.description}
"""

import subprocess
import sys
import json
from pathlib import Path

def main():
    """Execute the test task"""
    print(f"Apprentice executing task: {task.task_id}")
    print(f"Description: {task.description}")
    print("-" * 60)

    # Run the test command
    try:
        result = subprocess.run(
            {task.test_command.split()},
            capture_output=True,
            text=True,
            cwd="/workspace"
        )

        print("STDOUT:")
        print(result.stdout)

        if result.stderr:
            print("\\nSTDERR:")
            print(result.stderr)

        print("-" * 60)
        print(f"Exit code: {{result.returncode}}")

        # Save structured result
        output_data = {{
            "task_id": "{task.task_id}",
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }}

        Path("/tmp/work/result.json").write_text(json.dumps(output_data))

        sys.exit(result.returncode)

    except Exception as e:
        print(f"ERROR: {{str(e)}}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''

    async def _cleanup_apprentice(self, apprentice_id: str, compose_path: Path):
        """Clean up apprentice container and files"""
        try:
            # Stop and remove container
            proc = await asyncio.create_subprocess_exec(
                "docker-compose",
                "-f",
                str(compose_path),
                "down",
                "-v",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await proc.wait()

            # Remove work directory
            import shutil

            shutil.rmtree(compose_path.parent, ignore_errors=True)

        except Exception as e:
            print(f"Cleanup error for {apprentice_id}: {e}")

    def print_summary(self):
        """Print summary of all delegated tests"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.success)
        failed = total - passed
        total_time = sum(r.duration for r in self.results)

        print("\n" + "=" * 60)
        print("LOOM TEST DELEGATION SUMMARY")
        print("=" * 60)
        print(f"Total tasks delegated: {total}")
        print(f"Successful: {passed} ✓")
        print(f"Failed: {failed} ✗")
        print(f"Total time: {total_time:.2f}s")
        print(f"Average time per task: {total_time / total if total else 0:.2f}s")

        if failed > 0:
            print("\nFailed tasks:")
            for r in self.results:
                if not r.success:
                    print(f"  - {r.task_id} (apprentice: {r.apprentice_id})")

        print("=" * 60)


async def example_usage():
    """Example: Delegate test exploration to apprentices"""
    loom = MinimalLoom(max_concurrent=2)

    # Define test tasks to explore
    tasks = [
        TestTask(
            task_id="verify-imports",
            description="Check if core imports work",
            test_command="python -c 'import mallku; print(\"✓ mallku imports\")'",
        ),
        TestTask(
            task_id="run-simple-test",
            description="Run basic test suite",
            test_command="pytest tests/test_simple.py -v",
        ),
        TestTask(
            task_id="check-security",
            description="Verify database security",
            test_command="python scripts/verify_database_security.py",
        ),
    ]

    print("🧵 Minimal Loom - Delegating tests to apprentices")
    print("=" * 60)

    # Delegate all tasks
    results = await loom.delegate_multiple(tasks)

    # Show results
    for result in results:
        status = "✓" if result.success else "✗"
        print(f"\n{status} Task: {result.task_id}")
        print(f"   Duration: {result.duration:.2f}s")
        print(f"   Apprentice: {result.apprentice_id}")

        # Show first few lines of output
        lines = result.output.split("\n")[:5]
        for line in lines:
            if line.strip():
                print(f"   > {line}")

    loom.print_summary()

    print("\n💡 Context preserved: Weaver delegates, apprentices explore")


if __name__ == "__main__":
    asyncio.run(example_usage())
