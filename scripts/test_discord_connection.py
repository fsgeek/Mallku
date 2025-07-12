#!/usr/bin/env python3
"""
Test Discord Bot Connection
===========================

Minimal test to verify the Discord bot can connect and receive events.

51st Guardian - Testing the temple doors
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mallku.discord_gateway import FireCircleBot  # noqa: E402

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def test_connection():
    """Test basic Discord connection."""

    # Load token
    token_file = project_root / ".secrets" / "discord-mallku.txt"
    if not token_file.exists():
        logger.error("Token file not found")
        return

    discord_token = token_file.read_text().strip()

    # Create minimal bot
    bot = FireCircleBot()

    # Override on_ready to exit after connection
    original_on_ready = bot.on_ready

    async def test_on_ready():
        await original_on_ready()
        logger.info("✅ Successfully connected to Discord!")
        logger.info(f"Bot name: {bot.user.name}")
        logger.info(f"Bot ID: {bot.user.id}")
        logger.info(f"Connected to {len(bot.guilds)} guild(s)")

        # List guilds
        for guild in bot.guilds:
            logger.info(f"  - {guild.name} (ID: {guild.id})")

        # Close after successful connection
        await asyncio.sleep(2)
        await bot.close()

    bot.on_ready = test_on_ready

    try:
        logger.info("🔥 Testing Fire Circle Discord connection...")
        await bot.start(discord_token)
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        if "Improper token" in str(e):
            logger.error("The token appears to be invalid")
        elif "401 Unauthorized" in str(e):
            logger.error("The token was rejected by Discord")


if __name__ == "__main__":
    asyncio.run(test_connection())
