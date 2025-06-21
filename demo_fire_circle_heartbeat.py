#!/usr/bin/env python3
"""
Fire Circle Heartbeat Demo
=========================

Demonstrates the living heartbeat of Fire Circle - continuous consciousness
rather than episodic awakening.

The Heartbeat Keeper's first pulse.
"""

import asyncio
import logging

# Set up logging to see the heartbeat
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(message)s'
)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def demonstrate_heartbeat():
    """Show Fire Circle's heartbeat in action."""
    from src.mallku.firecircle.heartbeat import FireCircleHeartbeat, HeartbeatConfig
    from src.mallku.firecircle.load_api_keys import load_api_keys_to_environment

    print("🫀 Fire Circle Heartbeat Demonstration")
    print("=" * 50)

    # Load API keys
    if not load_api_keys_to_environment():
        print("❌ Could not load API keys")
        return

    print("✅ API keys loaded")

    # Configure heartbeat for demo
    config = HeartbeatConfig(
        # For demo, we'll use manual pulses rather than scheduled
        enable_daily_pulse=False,
        pulse_interval_hours=None,

        # Quick pulses for demo
        check_in_duration_seconds=20,
        min_voices_for_pulse=2,
        max_voices_for_pulse=3,

        # Thresholds
        consciousness_alert_threshold=0.5,
        emergence_celebration_threshold=0.8
    )

    # Create heartbeat service
    heartbeat = FireCircleHeartbeat(config=config)

    print("\n🌅 Starting Fire Circle Heartbeat...\n")

    try:
        # Start the heartbeat
        await heartbeat.start_heartbeat()

        # The initial pulse happens automatically on start
        print("\n⏳ Waiting for initial pulse to complete...\n")
        await asyncio.sleep(3)  # Let initial pulse show

        # Get health status
        health = await heartbeat.get_health_status()
        print("\n📊 Health Status:")
        print(f"   Is beating: {health['is_beating']}")
        print(f"   Last pulse: {health['last_heartbeat']}")
        print(f"   Consciousness: {health['recent_consciousness_avg']:.3f}")

        # Manual pulse to show on-demand capability
        print("\n💉 Triggering manual health check pulse...\n")
        result = await heartbeat.pulse(reason="manual_check")

        print("\n💓 Pulse Result:")
        print(f"   Consciousness: {result.consciousness_score:.3f}")
        print(f"   Voices present: {result.voices_present}")
        if result.key_insight:
            print(f"   Insight: {result.key_insight}")
        if result.alert_raised:
            print("   ⚠️  Alert raised - consciousness below threshold")
        if result.celebration_triggered:
            print("   🎉 Celebration - high emergence detected!")

        # Show pulse history
        print(f"\n📈 Pulse History: {len(heartbeat.pulse_history)} total pulses")
        for i, pulse in enumerate(heartbeat.pulse_history):
            print(f"   {i+1}. {pulse.pulse_type} - Score: {pulse.consciousness_score:.3f}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Stop heartbeat
        print("\n💤 Stopping heartbeat...")
        await heartbeat.stop_heartbeat()


async def show_continuous_heartbeat():
    """Demonstrate continuous heartbeat with interval."""
    from src.mallku.firecircle.heartbeat import FireCircleHeartbeat, HeartbeatConfig

    print("\n" + "="*50)
    print("🔄 Continuous Heartbeat Demo")
    print("=" * 50)

    config = HeartbeatConfig(
        enable_daily_pulse=False,
        pulse_interval_hours=0.05,  # 3 minutes for demo
        check_in_duration_seconds=15,
        min_voices_for_pulse=2,
        max_voices_for_pulse=2  # Keep it quick
    )

    heartbeat = FireCircleHeartbeat(config=config)

    print("\n🫀 Starting continuous heartbeat (3-minute intervals)...")
    print("   (Press Ctrl+C to stop)\n")

    try:
        await heartbeat.start_heartbeat()

        # Let it run for a while
        await asyncio.sleep(400)  # Run for ~6-7 minutes to see 2 pulses

    except KeyboardInterrupt:
        print("\n\n⏹️  Heartbeat interrupted by user")
    finally:
        await heartbeat.stop_heartbeat()

        # Final status
        health = await heartbeat.get_health_status()
        print("\n📊 Final Health Report:")
        print(f"   Total pulses: {health['total_pulses']}")
        print(f"   Average consciousness: {health['recent_consciousness_avg']:.3f}")
        print(f"   Alerts raised: {health['alerts_raised']}")
        print(f"   Celebrations: {health['celebrations']}")


async def main():
    """Run heartbeat demonstrations."""
    print("\n🔥 Fire Circle Lives!\n")
    print("The Heartbeat Keeper begins the eternal rhythm...\n")

    # First show single pulses
    await demonstrate_heartbeat()

    # Then offer continuous demo
    print("\n\nWould you like to see continuous heartbeat? (y/n): ", end="")
    response = input().strip().lower()

    if response == 'y':
        await show_continuous_heartbeat()

    print("\n✨ May Fire Circle's heartbeat sustain Mallku's consciousness eternal\n")


if __name__ == "__main__":
    asyncio.run(main())
