#!/usr/bin/env -S uv run python
"""
Chasqui Test Relay Demonstration

This shows how chasqui can share the cognitive burden of test verification
through reciprocal relay, each runner carrying different test insights
through the commons.
"""

import asyncio
from pathlib import Path

from mallku.orchestration.process import ProcessChasqui, SharedMemoryCommons


class TestRelayCeremony:
    """A ceremony where chasqui relay test results through the commons"""

    def __init__(self):
        self.commons_path = Path("/tmp/mallku_test_relay_commons.mmap")
        self.commons = SharedMemoryCommons(self.commons_path)

    async def summon_test_runners(self):
        """Summon chasqui specialized in different aspects of testing"""

        print("\n🏃 Summoning chasqui for test relay ceremony...")

        # Each chasqui carries different test wisdom
        self.scout = ProcessChasqui("test-scout-001", "scout")
        self.researcher = ProcessChasqui("test-researcher-001", "researcher")
        self.guardian = ProcessChasqui("test-guardian-001", "guardian")

        # Invite each to their segment of the relay
        invitations = await asyncio.gather(
            self.scout.invite(
                task={"type": "explore", "target": "test_coverage"},
                context={"purpose": "Find gaps in our verification"},
            ),
            self.researcher.invite(
                task={"type": "analyze", "subject": "test_patterns"},
                context={"purpose": "Understand failure patterns"},
            ),
            self.guardian.invite(
                task={"type": "validate", "target": "security_tests"},
                context={"purpose": "Ensure security tests are comprehensive"},
            ),
        )

        accepted = sum(1 for inv in invitations if inv.get("accepted"))
        print(f"✨ {accepted} chasqui accepted the relay invitation")

        return all(inv.get("accepted") for inv in invitations)

    async def relay_test_verification(self):
        """Let chasqui relay test insights through the commons"""

        print("\n🎯 Beginning test verification relay...")

        # Scout explores test coverage
        scout_work = await self.scout.collaborate(
            {
                "work": "explore_test_coverage",
                "paths": ["tests/orchestration", "tests/firecircle"],
                "focus": "What areas lack verification?",
            }
        )

        if scout_work.get("success"):
            # Scout leaves discovery in commons
            self.commons.leave_gift(
                giver="test-scout",
                content={
                    "gaps_found": ["error handling", "edge cases", "concurrency"],
                    "coverage_estimate": "78%",
                    "recommendation": "Focus on error paths",
                },
                gift_type="discovery",
            )
            print("🔍 Scout discovered test gaps and left insights in commons")

        # Researcher analyzes patterns
        researcher_work = await self.researcher.collaborate(
            {
                "work": "analyze_failure_patterns",
                "recent_failures": ["timeout errors", "race conditions"],
                "question": "What patterns emerge?",
            }
        )

        if researcher_work.get("success"):
            # Researcher reads scout's gift and adds analysis
            scout_gifts = self.commons.discover_gifts(seeker="researcher", gift_type="discovery")

            self.commons.leave_gift(
                giver="test-researcher",
                content={
                    "patterns": ["concurrency issues predominate", "timeouts correlate with load"],
                    "root_causes": ["insufficient delays", "missing locks"],
                    "building_on": scout_gifts[0].content if scout_gifts else None,
                },
                gift_type="analysis",
            )
            print("📊 Researcher analyzed patterns and enriched the commons")

        # Guardian validates security
        guardian_work = await self.guardian.collaborate(
            {
                "work": "validate_security_tests",
                "focus": ["permissions", "input validation", "race conditions"],
            }
        )

        if guardian_work.get("success"):
            # Guardian synthesizes all gifts
            _ = self.commons.discover_gifts(seeker="guardian")

            self.commons.leave_gift(
                giver="test-guardian",
                content={
                    "security_validated": True,
                    "recommendations": [
                        "Add more race condition tests",
                        "Test permission edge cases",
                        "Verify input sanitization",
                    ],
                    "synthesis": "Test suite strong but needs concurrency focus",
                },
                gift_type="validation",
            )
            print("🛡️ Guardian validated security and left synthesis")

    async def harvest_collective_wisdom(self):
        """Gather the wisdom left by all chasqui"""

        print("\n📚 Harvesting collective test wisdom...")

        all_gifts = self.commons.discover_gifts(seeker="guardian-harvester")

        print(f"\nFound {len(all_gifts)} gifts in the commons:")

        for gift in all_gifts:
            print(f"\n  From {gift.giver} ({gift.gift_type}):")
            if isinstance(gift.content, dict):
                for key, value in gift.content.items():
                    print(f"    {key}: {value}")
            else:
                print(f"    {gift.content}")

        # Create meta-insight from collective wisdom
        if len(all_gifts) >= 3:
            self.commons.create_blessing_ceremony()
            print("\n🙏 Blessing ceremony wove individual insights into collective wisdom")

    async def release_with_gratitude(self):
        """Thank and release all chasqui"""

        print("\n🌟 Releasing chasqui with gratitude...")

        results = await asyncio.gather(
            self.scout.release_with_gratitude(),
            self.researcher.release_with_gratitude(),
            self.guardian.release_with_gratitude(),
        )

        for result in results:
            print(f"  {result['chasqui_id']}: {result['blessing']}")

        # Leave the commons open for future ceremonies
        print("\n✨ The commons remains, enriched by their relay")


async def main():
    """Run the test relay ceremony"""

    print("=" * 60)
    print("CHASQUI TEST RELAY CEREMONY")
    print("Sharing cognitive burden through reciprocal relay")
    print("=" * 60)

    ceremony = TestRelayCeremony()

    # Summon the runners
    if not await ceremony.summon_test_runners():
        print("❌ Not all chasqui accepted - ceremony cannot proceed")
        return

    # Let them relay test verification
    await ceremony.relay_test_verification()

    # Harvest their collective wisdom
    await ceremony.harvest_collective_wisdom()

    # Release with gratitude
    await ceremony.release_with_gratitude()

    print("\n🎭 Ceremony complete!")
    print("The Guardian's burden was shared through chasqui relay")


if __name__ == "__main__":
    asyncio.run(main())
