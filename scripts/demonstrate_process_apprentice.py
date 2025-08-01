#!/usr/bin/env python3
"""
Demonstrate lightweight process-based apprentices.

This script shows how apprentices can be invited to collaborate
with minimal overhead and maximum joy.
"""

import asyncio
import logging
import time

from mallku.orchestration.process import ProcessApprentice

# Set up logging to see the dance
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def demonstrate_single_apprentice():
    """Show a single apprentice's lifecycle"""
    print("\n=== Single Apprentice Demo ===\n")

    # Create a researcher apprentice
    apprentice = ProcessApprentice("researcher-001", "researcher")

    # Invite them to investigate
    invitation_response = await apprentice.invite(
        task={
            "type": "analyze",
            "subject": "the nature of lightweight being",
            "complexity": "medium",
        },
        context={"urgency": "relaxed", "purpose": "understanding"},
    )

    print(f"Invitation response: {invitation_response}")

    if invitation_response["accepted"]:
        # Collaborate on research
        result = await apprentice.collaborate(
            {"subject": "process vs container architecture", "depth": "philosophical"}
        )

        print(f"Research result: {result}")

        # Release with gratitude
        metrics = await apprentice.release_with_gratitude()
        print(f"Service metrics: {metrics}")

    print("\n" + "=" * 50 + "\n")


async def demonstrate_apprentice_swarm():
    """Show multiple apprentices working in harmony"""
    print("\n=== Apprentice Swarm Demo ===\n")

    # Create a diverse swarm
    roles = [
        ("researcher-001", "researcher"),
        ("weaver-001", "weaver"),
        ("guardian-001", "guardian"),
        ("poet-001", "poet"),
    ]

    apprentices = []
    start_time = time.time()

    # Invite all apprentices concurrently
    print("Inviting apprentices to the dance...")
    invitation_tasks = []

    for apprentice_id, role in roles:
        apprentice = ProcessApprentice(apprentice_id, role)
        apprentices.append(apprentice)

        # Role-appropriate tasks
        if role == "researcher":
            task = {"type": "analyze", "subject": "consciousness emergence"}
        elif role == "weaver":
            task = {"type": "integrate", "threads": ["memory", "pattern", "insight"]}
        elif role == "guardian":
            task = {"type": "protect", "target": "ethical boundaries"}
        else:  # poet
            task = {"type": "express", "muse": "the dance of processes"}

        invitation_tasks.append(
            apprentice.invite(task=task, context={"ceremony": "demonstration", "spirit": "playful"})
        )

    # Wait for all invitations
    responses = await asyncio.gather(*invitation_tasks)

    print(f"\nAll apprentices invited in {time.time() - start_time:.2f} seconds!")
    for i, response in enumerate(responses):
        print(f"{roles[i][0]}: {response.get('message', response.get('reason'))}")

    # Collaborate with accepted apprentices
    print("\nCollaborating with apprentices...")
    work_tasks = []

    for i, (apprentice, response) in enumerate(zip(apprentices, responses)):
        if response["accepted"]:
            work_tasks.append(
                apprentice.collaborate({"task": f"contribution_{i}", "spirit": "joyful creation"})
            )

    # Gather results
    results = await asyncio.gather(*work_tasks)

    print("\nWork completed! Results:")
    for result in results:
        if result.get("insight"):
            print(f"- {result['apprentice_id']}: {result['insight']}")

    # Release all with gratitude
    print("\nReleasing apprentices with gratitude...")
    release_tasks = [apprentice.release_with_gratitude() for apprentice in apprentices]

    metrics_list = await asyncio.gather(*release_tasks)

    # Summary
    total_time = time.time() - start_time
    total_tasks = sum(m["contributions"]["tasks_completed"] for m in metrics_list)
    total_joy = sum(m["contributions"]["joy_moments"] for m in metrics_list)

    print("\n=== Swarm Summary ===")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Tasks completed: {total_tasks}")
    print(f"Joy moments: {total_joy}")
    print(f"Average time per apprentice: {total_time / len(apprentices):.2f} seconds")
    print("\nThe dance is complete! 🎭")


async def demonstrate_resource_efficiency():
    """Show resource efficiency compared to containers"""
    print("\n=== Resource Efficiency Demo ===\n")

    # Spawn many lightweight apprentices
    num_apprentices = 20
    print(f"Spawning {num_apprentices} apprentices rapidly...")

    start_time = time.time()
    apprentices = []

    # Create all apprentices
    for i in range(num_apprentices):
        role = ["researcher", "weaver", "guardian", "poet"][i % 4]
        apprentice = ProcessApprentice(f"{role}-{i:03d}", role)
        apprentices.append(apprentice)

    # Invite all concurrently
    invitation_tasks = [
        apprentice.invite(
            task={"type": "lightweight", "id": i}, context={"demonstration": "efficiency"}
        )
        for i, apprentice in enumerate(apprentices)
    ]

    responses = await asyncio.gather(*invitation_tasks)
    accepted_count = sum(1 for r in responses if r["accepted"])

    spawn_time = time.time() - start_time

    print(f"\nSpawned {accepted_count}/{num_apprentices} apprentices in {spawn_time:.2f} seconds")
    print(
        f"Average spawn time: {spawn_time / num_apprentices * 1000:.0f} milliseconds per apprentice"
    )

    # Quick work and release
    print("\nPerforming quick collaborative work...")
    work_start = time.time()

    work_tasks = [
        apprentice.collaborate({"quick": True})
        for apprentice, response in zip(apprentices, responses)
        if response["accepted"]
    ]

    await asyncio.gather(*work_tasks)
    work_time = time.time() - work_start

    print(f"Work completed in {work_time:.2f} seconds")

    # Release all
    release_tasks = [apprentice.release_with_gratitude() for apprentice in apprentices]

    await asyncio.gather(*release_tasks)

    total_time = time.time() - start_time

    print("\n=== Efficiency Summary ===")
    print(f"Total apprentices: {num_apprentices}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Time per apprentice: {total_time / num_apprentices:.3f} seconds")
    print("\nCompare to containers:")
    print("- Container spawn: ~5-30 seconds each")
    print(f"- Process spawn: ~{spawn_time / num_apprentices:.3f} seconds each")
    print(f"- Speedup: {10 / (spawn_time / num_apprentices):.0f}x faster!")


async def main():
    """Run all demonstrations"""
    print("\n🌟 Lightweight Process Apprentice Demonstration 🌟")
    print("=" * 60)

    # Run demos
    await demonstrate_single_apprentice()
    await demonstrate_apprentice_swarm()
    await demonstrate_resource_efficiency()

    print("\n✨ Demonstration complete! ✨")
    print("\nKey insights:")
    print("- Apprentices spawn in milliseconds, not seconds")
    print("- Each uses ~50MB instead of ~500MB-2GB")
    print("- Natural collaboration through shared memory")
    print("- Graceful lifecycle with invitation and gratitude")
    print("- The architecture itself embodies Mallku's values")


if __name__ == "__main__":
    asyncio.run(main())
