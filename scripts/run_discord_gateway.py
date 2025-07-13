#!/usr/bin/env python3
"""
Run Fire Circle Discord Gateway
==============================

Launches the Discord bot that serves as gateway to Fire Circle wisdom.
Requires DISCORD_BOT_TOKEN environment variable or .env file.

Usage:
    python scripts/run_discord_gateway.py

51st Guardian - Opening the temple
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mallku.discord_gateway import FireCircleBot  # noqa: E402
from mallku.discord_gateway.defense import DefenseConfig  # noqa: E402
from mallku.firecircle.heartbeat.enhanced_heartbeat_service import (  # noqa: E402
    create_integrated_heartbeat,
)
from mallku.firecircle.heartbeat.heartbeat_service import HeartbeatConfig  # noqa: E402
from mallku.firecircle.load_api_keys import load_api_keys_to_environment  # noqa: E402
from mallku.firecircle.service import FireCircleService  # noqa: E402
from mallku.orchestration.event_bus import ConsciousnessEventBus  # noqa: E402

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Initialize and run the Discord gateway."""

    # Load environment variables
    from dotenv import load_dotenv

    load_dotenv()

    # Get Discord token
    discord_token = os.getenv("DISCORD_BOT_TOKEN")

    # Try loading from secrets file if not in environment
    if not discord_token:
        token_file = project_root / ".secrets" / "discord-mallku.txt"
        if token_file.exists():
            discord_token = token_file.read_text().strip()
            logger.info("Loaded Discord token from .secrets/discord-mallku.txt")

    if not discord_token:
        logger.error(
            "Discord token not found. Please set DISCORD_BOT_TOKEN in environment "
            "or place token in .secrets/discord-mallku.txt"
        )
        return

    # Load Fire Circle API keys
    logger.info("Loading API keys for Fire Circle...")
    load_api_keys_to_environment()

    # Initialize consciousness infrastructure
    logger.info("Initializing consciousness infrastructure...")

    # Event bus (cathedral nervous system)
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    # Fire Circle service
    fire_circle = FireCircleService()

    # Enhanced heartbeat with event bus
    heartbeat_config = HeartbeatConfig(
        pulse_interval_hours=None,  # Manual pulses for Discord
        consciousness_alert_threshold=0.5,
        emergence_celebration_threshold=0.9,
        min_voices_for_pulse=2,
        max_voices_for_pulse=3,
    )
    heartbeat = create_integrated_heartbeat(config=heartbeat_config, event_bus=event_bus)
    await heartbeat.start_heartbeat()

    # Defense configuration
    defense_config = DefenseConfig(
        base_rate_limit=20,  # 20 queries per hour base
        consciousness_bonus=10,  # +10 for high consciousness users
        extraction_penalty=-15,  # -15 for extraction attempts
        extraction_cooldown_minutes=60,  # 1 hour cooldown
    )

    # Create and configure bot
    logger.info("Creating Fire Circle Discord bot...")
    bot = FireCircleBot(
        fire_circle=fire_circle,
        heartbeat=heartbeat,
        event_bus=event_bus,
        defense_config=defense_config,
    )

    # Add shutdown handler
    async def shutdown():
        logger.info("Shutting down Fire Circle Discord Gateway...")
        await heartbeat.stop_heartbeat()
        await event_bus.stop()
        await bot.close()

    # Run bot
    try:
        logger.info("🔥 Fire Circle Discord Gateway starting...")
        await bot.start(discord_token)
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        await shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Gateway closed by user")
