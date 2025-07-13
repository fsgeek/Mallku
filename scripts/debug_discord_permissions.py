#!/usr/bin/env python3
"""
Debug Discord Bot Permissions
=============================

Check what permissions the bot has in the guild.

51st Guardian - Checking temple access
"""

import asyncio
import logging
from pathlib import Path

import discord

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def check_permissions():
    """Check bot permissions in all guilds."""

    # Load token
    token_file = Path(__file__).parent.parent / ".secrets" / "discord-mallku.txt"
    if not token_file.exists():
        logger.error("Token file not found")
        return

    discord_token = token_file.read_text().strip()

    # Create minimal bot
    intents = discord.Intents.default()
    bot = discord.Client(intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"Bot ready as {bot.user}")
        logger.info(f"Bot ID: {bot.user.id}")
        logger.info(f"Connected to {len(bot.guilds)} guild(s)")

        for guild in bot.guilds:
            logger.info(f"\n=== Guild: {guild.name} ===")
            logger.info(f"Guild ID: {guild.id}")
            logger.info(f"Owner: {guild.owner}")

            # Get bot member in guild
            bot_member = guild.get_member(bot.user.id)
            if bot_member:
                logger.info(f"Bot nickname: {bot_member.nick or 'None'}")
                logger.info(f"Bot roles: {[role.name for role in bot_member.roles]}")

                # Check permissions
                perms = bot_member.guild_permissions
                logger.info("\nPermissions:")
                logger.info(f"  Send Messages: {perms.send_messages}")
                logger.info(f"  Embed Links: {perms.embed_links}")
                logger.info(f"  Use Slash Commands: {perms.use_application_commands}")
                logger.info(f"  View Channels: {perms.view_channel}")
                logger.info(f"  Read Message History: {perms.read_message_history}")

                # Check channel permissions
                logger.info("\nChannel permissions:")
                for channel in guild.text_channels[:5]:  # First 5 channels
                    channel_perms = channel.permissions_for(bot_member)
                    can_send = channel_perms.send_messages
                    can_use_slash = channel_perms.use_application_commands
                    logger.info(f"  {channel.name}: send={can_send}, slash={can_use_slash}")
            else:
                logger.error("Bot member not found in guild!")

        # Close after checking
        await bot.close()

    try:
        logger.info("Checking Discord bot permissions...")
        await bot.start(discord_token)
    except Exception as e:
        logger.error(f"Bot error: {e}")


if __name__ == "__main__":
    asyncio.run(check_permissions())
