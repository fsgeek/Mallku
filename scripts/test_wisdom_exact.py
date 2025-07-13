#!/usr/bin/env python3
"""
Test Exact Wisdom Implementation
================================

Mirror the exact structure of FireCircleBot wisdom command.

51st Guardian - Finding the exact issue
"""

import asyncio
import logging
from pathlib import Path

import discord
from discord.ext import commands

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TestFireBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="/", intents=intents)
        self.wisdom_shared = 0

    async def setup_hook(self):
        logger.info("setup_hook called")
        self.add_commands()

        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} commands")
        except Exception as e:
            logger.error(f"Failed to sync: {e}")

    def add_commands(self):
        logger.info("Adding commands...")

        @self.tree.command(name="testwisdom2", description="Test wisdom command")
        async def share_wisdom(interaction: discord.Interaction):
            """Test wisdom command."""
            logger.info(f"testwisdom2 invoked by {interaction.user}")
            try:
                await self.share_random_wisdom(interaction)
            except Exception as e:
                logger.error(f"Error in command handler: {e}")
                import traceback

                traceback.print_exc()

    async def share_random_wisdom(self, interaction: discord.Interaction):
        """Share wisdom - exact copy of bot method."""
        logger.info(f"share_random_wisdom called by {interaction.user} in {interaction.guild}")

        try:
            logger.info("Deferring interaction response...")
            await interaction.response.defer()
            logger.info("Interaction deferred successfully")

            # Simple test response
            logger.info("Creating embed...")
            embed = discord.Embed(
                title="🔥 Test Wisdom",
                description="Test wisdom works!",
                color=discord.Color.orange(),
            )

            logger.info("Sending followup...")
            await interaction.followup.send(embed=embed)
            logger.info("Success!")

            self.wisdom_shared += 1

        except Exception as e:
            logger.error(f"Error in share_random_wisdom: {e}")
            import traceback

            traceback.print_exc()


async def main():
    # Load token
    token_file = Path(__file__).parent.parent / ".secrets" / "discord-mallku.txt"
    if not token_file.exists():
        logger.error("Token file not found")
        return

    discord_token = token_file.read_text().strip()

    # Create and run bot
    bot = TestFireBot()

    @bot.event
    async def on_ready():
        logger.info(f"Bot ready as {bot.user}")

    try:
        logger.info("Starting test bot...")
        await bot.start(discord_token)
    except Exception as e:
        logger.error(f"Bot error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
