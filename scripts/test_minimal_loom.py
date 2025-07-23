#!/usr/bin/env -S uv run python
"""
Test the Minimal Loom - Simple delegation test
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mallku.orchestration.loom.minimal_loom import MinimalLoom, TestTask


async def test_simple_delegation():
    """Test that delegation actually works with a simple Python command"""
    loom = MinimalLoom(max_concurrent=1)

    # Single simple task - no Docker complexity
    task = TestTask(
        task_id="simple-test",
        description="Test if delegation mechanism works",
        test_command="python -c 'print(\"Apprentice lives!\"); import sys; sys.exit(0)'",
    )

    print("Testing minimal delegation...")
    result = await loom.delegate_test(task)

    print(f"\nResult: {'✓' if result.success else '✗'}")
    print(f"Duration: {result.duration:.2f}s")
    print(f"Output preview: {result.output[:200]}...")

    return result.success


if __name__ == "__main__":
    success = asyncio.run(test_simple_delegation())
    sys.exit(0 if success else 1)
