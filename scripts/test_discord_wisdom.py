#!/usr/bin/env python3
"""
Test Discord /wisdom Command
============================

Direct test of the wisdom command to see detailed error output.

51st Guardian - Debugging the temple
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import discord  # noqa: E402
from discord.ext import commands  # noqa: E402

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def test_wisdom_command():
    """Test the /wisdom command specifically."""

    # Load token
    token_file = project_root / ".secrets" / "discord-mallku.txt"
    if not token_file.exists():
        logger.error("Token file not found")
        return

    discord_token = token_file.read_text().strip()

    # Create minimal bot with test command
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="/", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"Test bot ready as {bot.user}")
        # Sync commands
        try:
            await bot.tree.sync()
            logger.info("Commands synced")
        except Exception as e:
            logger.error(f"Failed to sync: {e}")

    @bot.tree.command(name="test_wisdom", description="Test wisdom command")
    async def test_wisdom(interaction: discord.Interaction):
        """Test command that mimics wisdom functionality."""
        logger.info(f"test_wisdom called by {interaction.user}")

        try:
            # Test basic defer
            logger.info("Testing defer...")
            await interaction.response.defer()
            logger.info("Defer successful")

            # Test basic followup
            logger.info("Testing basic followup...")
            await interaction.followup.send("Basic text works!")
            logger.info("Basic followup successful")

            # Test embed followup
            logger.info("Testing embed followup...")
            embed = discord.Embed(
                title="Test Embed",
                description="Testing embed functionality",
                color=discord.Color.orange(),
            )
            embed.add_field(name="Field 1", value="Value 1", inline=True)
            embed.add_field(name="Field 2", value="Value 2", inline=True)

            await interaction.followup.send(embed=embed)
            logger.info("Embed followup successful!")

        except Exception as e:
            logger.error(f"Error in test_wisdom: {e}")
            import traceback

            traceback.print_exc()

    # Run bot
    try:
        logger.info("Starting test bot...")
        await bot.start(discord_token)
    except Exception as e:
        logger.error(f"Bot error: {e}")


if __name__ == "__main__":
    asyncio.run(test_wisdom_command())
