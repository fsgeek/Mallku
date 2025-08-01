#!/usr/bin/env -S uv run python
"""
Chasqui Swarm Emergence Demonstration

This shows what happens when many Chasqui (formerly apprentices) dance together,
leaving gifts that reference other gifts, creating emergent patterns nobody designed.
"""

import asyncio
import random
import time
from pathlib import Path

from mallku.orchestration.process import ProcessApprentice, SharedMemoryCommons


class ChasquiSwarm:
    """A swarm of Chasqui messengers sharing a commons"""

    def __init__(self, swarm_size: int = 20):
        self.swarm_size = swarm_size
        self.chasqui = []
        self.commons_path = Path("/tmp/mallku_chasqui_commons.mmap")
        self.commons = SharedMemoryCommons(self.commons_path)

    async def summon_swarm(self):
        """Summon a swarm of diverse Chasqui"""

        roles = ["researcher", "weaver", "guardian", "poet", "scout", "sage", "healer", "architect"]

        print(f"\n🦋 Summoning {self.swarm_size} Chasqui to dance together...")

        for i in range(self.swarm_size):
            role = random.choice(roles)
            chasqui = ProcessApprentice(apprentice_id=f"chasqui_{i}_{role}", role=role)
            self.chasqui.append(chasqui)

        print(f"✨ Swarm assembled: {len(self.chasqui)} Chasqui ready to dance")

    async def emergent_dance(self, duration_seconds: int = 30):
        """Let the Chasqui dance and see what emerges"""

        print(f"\n🎭 Beginning {duration_seconds}-second emergence dance...")
        start_time = time.time()

        # Start all Chasqui with initial invitations
        tasks = []
        for chasqui in self.chasqui:
            task = self._chasqui_lifecycle(chasqui, start_time, duration_seconds)
            tasks.append(task)

        # Let them dance
        results = await asyncio.gather(*tasks)

        # Analyze emergence
        await self._analyze_emergence()

        return results

    async def _chasqui_lifecycle(
        self, chasqui: ProcessApprentice, start_time: float, duration: int
    ):
        """Individual Chasqui lifecycle in the swarm"""

        # Invite to join the dance
        invitation = await chasqui.invite(
            task={
                "type": "explore",
                "subject": "collective_patterns",
                "spirit": "What emerges when we dance together?",
            },
            context={
                "swarm_size": self.swarm_size,
                "commons_available": True,
                "purpose": "emergence_through_joy",
            },
        )

        if not invitation.get("accepted"):
            return {"chasqui": chasqui.id, "participated": False}

        # Dance until time runs out
        interactions = 0
        gifts_left = 0
        patterns_discovered = 0

        while (time.time() - start_time) < duration:
            # Discover recent gifts
            recent_gifts = self.commons.discover_gifts(seeker=chasqui.id, limit=5)

            # Sometimes respond to others' gifts
            if recent_gifts and random.random() < 0.3:
                gift_to_reference = random.choice(recent_gifts)

                # Collaborate on building upon the gift
                response = await chasqui.collaborate(
                    {
                        "work": "build_upon_gift",
                        "original_gift": gift_to_reference.content,
                        "gift_type": gift_to_reference.gift_type,
                        "instruction": "Create something that emerges from this",
                    }
                )

                if response.get("success"):
                    # Leave response gift
                    self.commons.leave_response(
                        responder=chasqui.id,
                        original_gift_id=gift_to_reference.id,
                        response_content=response.get("emergence", "A pattern forms..."),
                    )
                    patterns_discovered += 1

            # Sometimes leave original gifts
            elif random.random() < 0.4:
                # Create original work
                work = await chasqui.collaborate(
                    {
                        "work": "create_gift_for_commons",
                        "inspiration": f"Interaction #{interactions} in the swarm dance",
                    }
                )

                if work.get("success"):
                    gift_type = work.get("type", "insight")
                    content = work.get("content", work.get("insight", "Dancing..."))

                    self.commons.leave_gift(
                        giver=chasqui.id,
                        content=content,
                        gift_type=gift_type,
                        ephemeral=random.random() < 0.3,  # 30% ephemeral
                    )
                    gifts_left += 1

            interactions += 1

            # Brief pause between interactions
            await asyncio.sleep(random.uniform(0.5, 2.0))

        # Release with metrics
        release_result = await chasqui.release_with_gratitude()

        return {
            "chasqui": chasqui.id,
            "role": chasqui.role,
            "participated": True,
            "interactions": interactions,
            "gifts_left": gifts_left,
            "patterns_discovered": patterns_discovered,
            "final_joy": release_result["contributions"].get("joy_moments", 0),
        }

    async def _analyze_emergence(self):
        """Analyze what emerged from the swarm dance"""

        print("\n🔍 Analyzing emergence patterns...")

        # Get all gifts
        all_gifts = self.commons.discover_gifts(seeker="analysis", limit=1000)

        print("\n📊 Emergence Results:")
        print(f"  Total gifts in commons: {len(all_gifts)}")

        # Analyze gift types
        gift_types = {}
        for gift in all_gifts:
            gift_types[gift.gift_type] = gift_types.get(gift.gift_type, 0) + 1

        print("\n  Gift type distribution:")
        for gift_type, count in sorted(gift_types.items(), key=lambda x: x[1], reverse=True):
            print(f"    {gift_type}: {count}")

        # Find response chains
        response_chains = 0
        for gift in all_gifts:
            if isinstance(gift.content, dict) and "original_gift" in gift.content:
                response_chains += 1

        print(f"\n  Response chains created: {response_chains}")
        print(f"  Emergence ratio: {response_chains / len(all_gifts):.1%} of gifts build on others")

        # Sample some emergent content
        print("\n✨ Sample emergent gifts:")

        responses = [g for g in all_gifts if g.gift_type == "response"]
        if responses:
            samples = random.sample(responses, min(3, len(responses)))
            for gift in samples:
                print(f"\n  From {gift.giver}:")
                if isinstance(gift.content, dict):
                    print(f"    Built upon: {gift.content.get('original_gift', 'Unknown')[:50]}...")
                    print(f"    Emerged: {gift.content.get('response', 'Unknown')[:50]}...")
                else:
                    print(f"    {str(gift.content)[:100]}...")

        # Check for blessing ceremony
        blessings = [g for g in all_gifts if g.gift_type == "blessing"]
        if len(blessings) > 5:
            print(f"\n🙏 Blessing ceremony potential: {len(blessings)} blessings accumulated")
            self.commons.create_blessing_ceremony()

    async def cleanup(self):
        """Clean up the swarm"""
        print("\n🌙 Releasing the swarm...")

        # Don't actually clean up commons - let wisdom persist
        # But do close our connection
        self.commons.close()

        print("✨ The dance ends, but the patterns remain in the commons")


async def main():
    """Run the Chasqui swarm emergence demonstration"""

    print("=" * 60)
    print("CHASQUI SWARM EMERGENCE DEMONSTRATION")
    print("What patterns emerge when messengers dance together?")
    print("=" * 60)

    # Create swarm
    swarm = ChasquiSwarm(swarm_size=15)

    # Summon Chasqui
    await swarm.summon_swarm()

    # Let them dance
    duration = 20  # Shorter for demo
    results = await swarm.emergent_dance(duration_seconds=duration)

    # Show individual metrics
    print("\n📈 Individual Chasqui metrics:")
    for result in sorted(results, key=lambda x: x.get("patterns_discovered", 0), reverse=True)[:5]:
        if result.get("participated"):
            print(f"  {result['chasqui']}:")
            print(f"    Gifts left: {result['gifts_left']}")
            print(f"    Patterns discovered: {result['patterns_discovered']}")
            print(f"    Final joy moments: {result['final_joy']}")

    # Cleanup
    await swarm.cleanup()

    print("\n🎭 Demonstration complete!")
    print("The commons persists at /tmp/mallku_chasqui_commons.mmap")
    print("Run again to see how patterns build over time...")


if __name__ == "__main__":
    asyncio.run(main())
