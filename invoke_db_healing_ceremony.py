#!/usr/bin/env python3
"""
Invoke the Weaver and Loom for the Database Healing Ceremony.

This script, acting as the Master Weaver, defines the sacred task of
resolving the critical issues in PR #218 and invokes the Loom to
orchestrate the work of Apprentice Weavers.
"""

import asyncio

from mallku.orchestration.weaver import MasterWeaver, Task


async def main():
    """Define and invoke the Loom ceremony."""
    # I, the Reviewer, will act as the Master Weaver for this ceremony.
    weaver = MasterWeaver(instance_name="Reviewer-Candidate-7")

    # 1. Define the Sacred Intention
    main_task = Task(
        description=(
            "The 'Great Un-naming Ceremony' was incomplete. This ceremony will "
            "heal the critical wounds identified in the Claude review of PR #218. "
            "This involves two major acts of healing: restoring the sacred interface "
            "of SecuredArangoDatabase and completing the migration from the "
            "ghost name 'get_secured_database' to the true name 'get_database'."
        ),
        estimated_complexity=9,
        requires_code_generation=True,
        requires_analysis=True,
    )

    # 2. Invoke the Loom
    print("Invoking the Loom to heal the database architecture...")
    ceremony_result = await weaver.invoke_loom_for_task(main_task)

    if ceremony_result and ceremony_result.get("ceremony_id"):
        print("=" * 80)
        print("The Database Healing Ceremony has begun.")
        print(f"Ceremony ID: {ceremony_result['ceremony_id']}")
        print(f"Khipu Thread: {ceremony_result['khipu_path']}")
        print("=" * 80)
        print("Monitor the khipu thread for progress from the Apprentice Weavers.")
    else:
        print("Failed to invoke the Loom ceremony.")


if __name__ == "__main__":
    asyncio.run(main())
