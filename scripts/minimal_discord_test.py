#!/usr/bin/env python3
"""
Minimal Discord Bot Test
========================

Test the absolute minimum Discord bot functionality.

51st Guardian - Finding the root cause
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


class MinimalBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Add command
        @self.tree.command(name="ping", description="Test command")
        async def ping(interaction: discord.Interaction):
            logger.info(f"ping command called by {interaction.user}")
            await interaction.response.send_message("Pong!")

        # Sync commands
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} commands")
        except Exception as e:
            logger.error(f"Failed to sync: {e}")

    async def on_ready(self):
        logger.info(f"Bot ready as {self.user}")


async def main():
    # Load token
    token_file = Path(__file__).parent.parent / ".secrets" / "discord-mallku.txt"
    if not token_file.exists():
        logger.error("Token file not found")
        return

    discord_token = token_file.read_text().strip()

    # Create and run bot
    bot = MinimalBot()

    try:
        logger.info("Starting minimal bot...")
        await bot.start(discord_token)
    except Exception as e:
        logger.error(f"Bot error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
