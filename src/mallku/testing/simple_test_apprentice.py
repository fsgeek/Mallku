#!/usr/bin/env -S uv run python
"""
Simple Test Apprentice - A Real Testing Tool
============================================

62nd Artisan - Building something that actually works

This is a focused test runner that:
1. Actually spawns a subprocess to run tests
2. Captures real output
3. Reports real results
4. No mocks, no simulations, no beautiful lies

It's simple because simplicity is more likely to be real.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any


class TestResult:
    """A real test result from a real test run"""

    def __init__(self, test_name: str, passed: bool, output: str, duration: float):
        self.test_name = test_name
        self.passed = passed
        self.output = output
        self.duration = duration

    def to_dict(self) -> dict[str, Any]:
        return {
            "test_name": self.test_name,
            "passed": self.passed,
            "output": self.output,
            "duration": self.duration,
            "timestamp": datetime.now().isoformat(),
        }


class SimpleTestApprentice:
    """
    A test runner that actually runs tests.

    No orchestration complexity, no ceremony overhead.
    Just run tests and report results.
    """

    def __init__(self, work_dir: Path = Path.cwd()):
        self.work_dir = work_dir
        self.results: list[TestResult] = []

    async def run_pytest(self, test_path: str, verbose: bool = True) -> TestResult:
        """Run pytest on a specific file or directory"""
        start_time = asyncio.get_event_loop().time()

        cmd = ["uv", "run", "pytest", test_path]
        if verbose:
            cmd.append("-v")

        try:
            # Run the actual test
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=self.work_dir,
            )

            stdout, _ = await proc.communicate()
            output = stdout.decode() if stdout else ""

            duration = asyncio.get_event_loop().time() - start_time
            passed = proc.returncode == 0

            result = TestResult(test_path, passed, output, duration)
            self.results.append(result)

            return result

        except Exception as e:
            duration = asyncio.get_event_loop().time() - start_time
            result = TestResult(test_path, False, f"Error running test: {str(e)}", duration)
            self.results.append(result)
            return result

    async def run_script(self, script_path: str, *args: str) -> TestResult:
        """Run any Python script and capture results"""
        start_time = asyncio.get_event_loop().time()

        cmd = ["uv", "run", "python", script_path] + list(args)

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=self.work_dir,
            )

            stdout, _ = await proc.communicate()
            output = stdout.decode() if stdout else ""

            duration = asyncio.get_event_loop().time() - start_time
            passed = proc.returncode == 0

            result = TestResult(script_path, passed, output, duration)
            self.results.append(result)

            return result

        except Exception as e:
            duration = asyncio.get_event_loop().time() - start_time
            result = TestResult(script_path, False, f"Error running script: {str(e)}", duration)
            self.results.append(result)
            return result

    async def verify_imports(self, module_name: str) -> TestResult:
        """Verify a module can be imported without errors"""
        start_time = asyncio.get_event_loop().time()

        test_script = f"""
import sys
try:
    import {module_name}
    print(f"✓ Successfully imported {module_name}")
    sys.exit(0)
except Exception as e:
    print(f"✗ Failed to import {module_name}: {{e}}")
    sys.exit(1)
"""

        try:
            proc = await asyncio.create_subprocess_exec(
                "uv",
                "run",
                "python",
                "-c",
                test_script,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=self.work_dir,
            )

            stdout, _ = await proc.communicate()
            output = stdout.decode() if stdout else ""

            duration = asyncio.get_event_loop().time() - start_time
            passed = proc.returncode == 0

            result = TestResult(f"import {module_name}", passed, output, duration)
            self.results.append(result)

            return result

        except Exception as e:
            duration = asyncio.get_event_loop().time() - start_time
            result = TestResult(f"import {module_name}", False, f"Error: {str(e)}", duration)
            self.results.append(result)
            return result

    def save_results(self, output_path: Path):
        """Save test results to a JSON file"""
        results_data = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(self.results),
            "passed": sum(1 for r in self.results if r.passed),
            "failed": sum(1 for r in self.results if not r.passed),
            "results": [r.to_dict() for r in self.results],
        }

        output_path.write_text(json.dumps(results_data, indent=2))
        print(f"✓ Results saved to {output_path}")

    def print_summary(self):
        """Print a summary of test results"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed

        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total tests: {total}")
        print(f"Passed: {passed} ✓")
        print(f"Failed: {failed} ✗")

        if failed > 0:
            print("\nFailed tests:")
            for r in self.results:
                if not r.passed:
                    print(f"  - {r.test_name}")

        print("=" * 60)


async def main():
    """Example usage of the Simple Test Apprentice"""
    apprentice = SimpleTestApprentice()

    # Example 1: Verify imports work
    print("Verifying core imports...")
    await apprentice.verify_imports("mallku")
    await apprentice.verify_imports("mallku.firecircle")

    # Example 2: Run a specific test file (if it exists)
    test_file = Path("tests/test_simple.py")
    if test_file.exists():
        print(f"\nRunning {test_file}...")
        await apprentice.run_pytest(str(test_file))

    # Example 3: Run a verification script
    verify_script = Path("scripts/verify_database_security.py")
    if verify_script.exists():
        print(f"\nRunning {verify_script}...")
        await apprentice.run_script(str(verify_script))

    # Print summary
    apprentice.print_summary()

    # Save results
    apprentice.save_results(Path("test_results.json"))


if __name__ == "__main__":
    asyncio.run(main())
