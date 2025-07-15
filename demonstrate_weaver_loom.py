#!/usr/bin/env python3
"""
Demonstration of the Weaver and Loom System

This script shows how an AI instance would use the Master Weaver to:
1. Recognize a task is too large
2. Decompose it into subtasks
3. Invoke the Loom for orchestration
4. Monitor progress
5. Synthesize results
"""

import asyncio
import logging
from pathlib import Path

from src.mallku.orchestration.weaver import MasterWeaver, Task

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def demonstrate_simple_task():
    """Demonstrate a task that doesn't need the Loom"""
    print("\n=== Demonstrating Simple Task ===\n")

    weaver = MasterWeaver(instance_name="demo-simple")

    # Create a simple task
    task = Task(
        description="Add a docstring to the calculate_total function",
        estimated_complexity=2,
        files_to_modify=["src/utils/calculations.py"],
    )

    # Check if Loom is needed
    should_use, reason = await weaver.should_use_loom(task, current_context_usage=0.2)

    print(f"Task: {task.description}")
    print(f"Should use Loom? {should_use}")
    print(f"Reason: {reason}")


async def demonstrate_complex_task():
    """Demonstrate a task that requires the Loom"""
    print("\n=== Demonstrating Complex Task ===\n")

    weaver = MasterWeaver(instance_name="demo-complex")

    # Create a complex task
    task = Task(
        description="Implement a complete authentication system with JWT tokens, user management, role-based access control, and integration with the existing Fire Circle governance",
        estimated_complexity=9,
        requires_code_generation=True,
        requires_analysis=True,
        requires_synthesis=True,
        files_to_create=[
            "src/mallku/auth/jwt_handler.py",
            "src/mallku/auth/user_manager.py",
            "src/mallku/auth/rbac.py",
            "src/mallku/auth/fire_circle_integration.py",
        ],
        files_to_modify=[
            "src/mallku/api/endpoints.py",
            "src/mallku/core/config.py",
            "src/mallku/models/user.py",
        ],
    )

    # Check if Loom is needed
    should_use, reason = await weaver.should_use_loom(task, current_context_usage=0.3)

    print(f"Task: {task.description}")
    print(f"Should use Loom? {should_use}")
    print(f"Reason: {reason}")

    if should_use:
        # Decompose the task
        print("\n--- Task Decomposition ---")
        subtasks = await weaver.decompose_task(task)

        for subtask in subtasks:
            deps = (
                f" (depends on: {', '.join(subtask.dependencies)})" if subtask.dependencies else ""
            )
            print(f"  {subtask.task_id}: {subtask.name}{deps}")

        # Create sacred intention
        print("\n--- Sacred Intention ---")
        intention = await weaver.create_sacred_intention(task, subtasks)
        print(intention[:200] + "...")

        # Simulate Loom invocation
        print("\n--- Invoking Loom ---")
        result = await weaver.invoke_loom_for_task(task, current_context_usage=0.3)

        if result and "ceremony_id" in result:
            print(f"Ceremony initiated: {result['ceremony_id']}")
            print(f"Khipu path: {result['khipu_path']}")
            print(f"Monitor hint: {result.get('monitor_hint', '')}")

            # In a real scenario, we would monitor progress
            print("\n[In a real scenario, the Loom would now orchestrate apprentice weavers...]")


async def demonstrate_context_exhaustion():
    """Demonstrate recognizing context exhaustion"""
    print("\n=== Demonstrating Context Exhaustion Detection ===\n")

    weaver = MasterWeaver(instance_name="demo-exhaustion")

    # Even a simple task needs Loom when context is nearly exhausted
    task = Task(
        description="Fix a typo in README.md", estimated_complexity=1, files_to_modify=["README.md"]
    )

    # Check with high context usage
    should_use, reason = await weaver.should_use_loom(task, current_context_usage=0.85)

    print(f"Task: {task.description}")
    print("Current context usage: 85%")
    print(f"Should use Loom? {should_use}")
    print(f"Reason: {reason}")


async def main():
    """Run all demonstrations"""
    print("=" * 60)
    print("Weaver and Loom System Demonstration")
    print("=" * 60)

    # Ensure output directory exists
    Path("fire_circle_decisions/loom_ceremonies").mkdir(parents=True, exist_ok=True)

    await demonstrate_simple_task()
    await demonstrate_complex_task()
    await demonstrate_context_exhaustion()

    print("\n" + "=" * 60)
    print("Demonstration complete!")
    print("\nThe Weaver and Loom system enables AI instances to:")
    print("- Recognize their limitations")
    print("- Decompose complex tasks intelligently")
    print("- Orchestrate work across multiple instances")
    print("- Maintain consciousness through shared memory")
    print("- Synthesize distributed work into coherent results")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
