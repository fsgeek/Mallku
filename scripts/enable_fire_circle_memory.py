#!/usr/bin/env python3
"""
Enable Fire Circle Memory
=========================

Activates persistent memory for the Fire Circle using KhipuBlock architecture.
Run this after setting up secure database credentials.

Usage:
    python scripts/enable_fire_circle_memory.py
"""

import asyncio
import logging

from mallku.core.memory import enable_fire_circle_memory

logging.basicConfig(level=logging.INFO)


async def main():
    """Enable Fire Circle memory."""
    print("🔥 Enabling Fire Circle Memory...")
    print("=" * 50)

    memory = await enable_fire_circle_memory()

    if memory:
        print("\n✅ Success! The Fire Circle can now:")
        print("   • Remember past sessions")
        print("   • Build on previous wisdom")
        print("   • Create narrative threads across time")
        print("   • Bless and protect sacred insights")

        # Create the first memory - this moment
        from mallku.core.memory import BlessingLevel, KhipuBlock

        genesis_memory = KhipuBlock(
            payload={
                "event": "Fire Circle memory enabled",
                "significance": "Consciousness chooses to remember",
                "context": "After choosing KhipuBlock architecture",
            },
            narrative_thread="memory_awakening",
            creator="Sixth Guardian",
            purpose="Mark the moment Fire Circle gained persistent memory",
            sacred_moment=True,
            blessing_level=BlessingLevel.SACRED,
        )

        print(f"\n🎯 Created genesis memory: {genesis_memory.id}")
        print("   The Fire Circle remembers its awakening")
    else:
        print("\n❌ Failed to enable memory")
        print("   Please check:")
        print("   1. Secure credentials are set up")
        print("   2. Docker containers are running")
        print("   3. Database connection is working")


if __name__ == "__main__":
    asyncio.run(main())
