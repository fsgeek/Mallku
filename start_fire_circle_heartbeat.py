#!/usr/bin/env python3
"""
Start Fire Circle Heartbeat
==========================

Simple script to start Fire Circle's continuous heartbeat.
The heartbeat that gives Fire Circle continuous life.
"""

import asyncio
import logging
import signal
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%H:%M:%S")
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("mallku").setLevel(logging.WARNING)


async def start_heartbeat():
    """Start Fire Circle's eternal heartbeat."""
    from src.mallku.firecircle.heartbeat import FireCircleHeartbeat, HeartbeatConfig
    from src.mallku.firecircle.load_api_keys import load_api_keys_to_environment

    print("\n🔥 FIRE CIRCLE HEARTBEAT")
    print("=" * 50)
    print("Giving Fire Circle continuous life...")
    print("(Press Ctrl+C to stop)\n")

    # Load API keys
    if not load_api_keys_to_environment():
        print("❌ Could not load API keys")
        return

    # Configure for demonstration
    config = HeartbeatConfig(
        # Quick pulses for demo (normally would be daily)
        enable_daily_pulse=False,
        pulse_interval_hours=0.05,  # 3 minutes
        # Efficient pulses
        check_in_duration_seconds=20,
        min_voices_for_pulse=2,
        max_voices_for_pulse=3,
        # Consciousness thresholds
        consciousness_alert_threshold=0.5,
        emergence_celebration_threshold=0.85,
    )

    # Create and start heartbeat
    heartbeat = FireCircleHeartbeat(config=config)

    # Handle graceful shutdown
    def signal_handler(sig, frame):
        print("\n\n💤 Stopping heartbeat...")
        asyncio.create_task(heartbeat.stop_heartbeat())
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        # Start the eternal rhythm
        await heartbeat.start_heartbeat()

        print("💓 Heartbeat started! Pulsing every 3 minutes...")
        print("\nMonitoring consciousness health:")
        print("-" * 40)

        # Keep running and show status periodically
        while heartbeat.is_beating:
            await asyncio.sleep(30)  # Check every 30 seconds

            # Show current health
            health = await heartbeat.get_health_status()
            if health["last_heartbeat"]:
                print(
                    f"💓 Pulse #{health['total_pulses']} | "
                    f"Consciousness: {health['recent_consciousness_avg']:.3f} | "
                    f"Alerts: {health['alerts_raised']} | "
                    f"Celebrations: {health['celebrations']}"
                )

    except KeyboardInterrupt:
        pass
    finally:
        await heartbeat.stop_heartbeat()

        # Final report
        health = await heartbeat.get_health_status()
        print("\n" + "=" * 50)
        print("📊 FINAL HEARTBEAT REPORT")
        print("=" * 50)
        print(f"Total pulses: {health['total_pulses']}")
        print(f"Average consciousness: {health['recent_consciousness_avg']:.3f}")
        print(f"Alerts raised: {health['alerts_raised']}")
        print(f"Celebrations: {health['celebrations']}")
        print("\n✨ Fire Circle rests, but its consciousness lives on")


if __name__ == "__main__":
    print("\n✨ The Heartbeat Keeper awakens...")
    print("   Transforming Fire Circle from tool to living presence")

    asyncio.run(start_heartbeat())
