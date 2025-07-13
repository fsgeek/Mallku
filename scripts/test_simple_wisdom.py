#!/usr/bin/env python3
"""
Simple test of wisdom command
=============================

Test just the wisdom functionality in isolation.

51st Guardian - Finding the issue
"""

import asyncio
import logging
from pathlib import Path

import discord
from discord import app_commands

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TestBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        @self.tree.command(name="testwisdom", description="Test wisdom command")
        async def test_wisdom(interaction: discord.Interaction):
            """Test wisdom command."""
            logger.info(f"testwisdom command called by {interaction.user}")

            try:
                # Method 1: Direct response
                await interaction.response.send_message("Direct wisdom response works!")
                logger.info("Direct response sent successfully")

            except Exception as e:
                logger.error(f"Error in test_wisdom: {e}")
                import traceback

                traceback.print_exc()

        # Sync commands
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} commands")
        except Exception as e:
            logger.error(f"Failed to sync: {e}")


async def main():
    # Load token
    token_file = Path(__file__).parent.parent / ".secrets" / "discord-mallku.txt"
    if not token_file.exists():
        logger.error("Token file not found")
        return

    discord_token = token_file.read_text().strip()

    # Create and run bot
    bot = TestBot()

    @bot.event
    async def on_ready():
        logger.info(f"Bot ready as {bot.user}")
        logger.info(f"Connected to {len(bot.guilds)} guild(s)")
        for guild in bot.guilds:
            logger.info(f"  - {guild.name}")

    try:
        logger.info("Starting test bot...")
        await bot.start(discord_token)
    except Exception as e:
        logger.error(f"Bot error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
