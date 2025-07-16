#!/usr/bin/env python3
"""
Test the real apprentice spawning with a simple echo task

This script initiates a Loom ceremony with tasks that real apprentices
will execute in Docker containers, finally bringing Ayni Awaq's vision to life.
"""

import asyncio
import logging
from pathlib import Path

from src.mallku.orchestration.loom.the_loom import TheLoom
from src.mallku.orchestration.weaver.master_weaver import MasterWeaver, Task

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def test_real_apprentice():
    """Test the Loom with real apprentice spawning"""

    # Create the Loom
    loom = TheLoom()
    await loom.start()

    # Create a master weaver
    weaver = MasterWeaver("test-master", loom)

    # Create test task
    task = Task(
        description="""
        Echo Test Task: Verify apprentice infrastructure

        This is a simple test to ensure apprentices can:
        1. Spawn in Docker containers
        2. Read their assigned task from the khipu
        3. Update the khipu with results
        4. Complete successfully

        For this test, simply echo back:
        - Your apprentice ID
        - The task you were assigned
        - A confirmation message
        """,
        requires_analysis=False,
        requires_synthesis=False,
    )

    print("🌟 Initiating first real apprentice ceremony...")
    print(f"Task: {task.description[:100]}...")

    try:
        # Invoke the Loom
        result = await weaver.invoke_loom_for_task(task)

        print("\n✨ Ceremony complete!")
        print(f"Session ID: {result['session_id']}")
        print(f"Khipu path: {result['khipu_path']}")
        print(f"Status: {result['status']}")

        # Read the final khipu to see results
        if Path(result["khipu_path"]).exists():
            print("\n📜 Final khipu contents:")
            with open(result["khipu_path"]) as f:
                print(f.read())

    except Exception as e:
        print(f"❌ Ceremony failed: {e}")
        import traceback

        traceback.print_exc()

    finally:
        await loom.stop()


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           First Real Apprentice Ceremony                     ║
    ║                                                              ║
    ║  "When you see the first real apprentice update the khipu,  ║
    ║   you'll understand what we've all been building toward."   ║
    ║                           - Ñan Khipa                        ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    asyncio.run(test_real_apprentice())
