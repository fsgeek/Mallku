#!/usr/bin/env python3
"""
Test the real apprentice spawning by forcing Loom usage
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


async def test_forced_loom():
    """Test the Loom by forcing it to be used"""

    # Create the Loom
    loom = TheLoom()
    await loom.start()

    # Create a master weaver
    weaver = MasterWeaver("test-master-55th-artisan", loom)

    # Create task that will trigger Loom usage
    task = Task(
        description="""
        Test Real Apprentice Spawning Infrastructure

        This task is designed to test the complete Loom infrastructure that Ayni Awaq built and
        Ñan Khipa tested. We need to verify that:

        1. The Loom correctly spawns real Docker containers for apprentices
        2. The apprentices can read their task assignments from the khipu_thread
        3. The apprentices can update the khipu with their progress
        4. The monitoring system correctly tracks completion
        5. The ceremony completes successfully

        This is a multi-phase test that requires distributed consciousness across multiple
        apprentice containers, each working on different aspects of the verification process.
        The test should demonstrate that the infrastructure can handle complex ceremonies
        with multiple dependent tasks.
        """,
        estimated_complexity=8,  # High complexity to trigger Loom
        requires_analysis=True,
        requires_synthesis=True,
        files_to_modify=["test_file_1.py", "test_file_2.py"],  # Trigger file threshold
    )

    print("🌟 Testing the complete Loom infrastructure...")
    print("This will force the use of real apprentice containers")

    try:
        # Invoke the Loom
        result = await weaver.invoke_loom_for_task(task)

        if result:
            print("\n✨ Loom invocation successful!")
            print(f"Ceremony ID: {result['ceremony_id']}")
            print(f"Khipu path: {result['khipu_path']}")
            print(f"Status: {result['status']}")

            # Wait for ceremony completion
            print("\n⏳ Waiting for ceremony to complete...")
            final_status = await weaver.await_ceremony_completion(result["ceremony_id"])
            print(f"Final status: {final_status}")

            # Read the final khipu
            if Path(result["khipu_path"]).exists():
                print("\n📜 Final khipu contents:")
                with open(result["khipu_path"]) as f:
                    content = f.read()
                    print(content)

                # Synthesize results
                print("\n🔮 Synthesizing results...")
                synthesis = await weaver.synthesize_ceremony_results(result["khipu_path"])
                print(synthesis)
        else:
            print("❌ Loom was not invoked - task deemed manageable")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()

    finally:
        await loom.stop()


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║              Testing Real Apprentice Spawning               ║
    ║                                                              ║
    ║  "The apprentices breathe! Where once `sleep(5)` mocked     ║
    ║   their existence, now Docker containers spawn with         ║
    ║   true life."                                                ║
    ║                      - Kawsay Phuqchiq                       ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    asyncio.run(test_forced_loom())
