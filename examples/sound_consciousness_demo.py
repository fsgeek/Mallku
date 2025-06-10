"""
Sound Consciousness Demonstration

Shows how sound creation activities flow through consciousness recognition
and transform into reciprocity patterns for Fire Circle contemplation.

Qhapaq Taki - The Noble Song Builder
"""

import asyncio
import logging
from datetime import UTC, datetime
from pathlib import Path

from mallku.orchestration import ConsciousnessEvent, ConsciousnessEventBus
from mallku.orchestration.providers import SoundActivityProvider
from mallku.reciprocity.models import ReciprocityPattern, SystemHealthMetrics
from mallku.reciprocity.visualization import ReciprocityVisualizationService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)


async def demonstrate_sound_consciousness():
    """
    Demonstrate how sound activities become consciousness patterns.

    This shows:
    1. Sound file creation triggering consciousness events
    2. Pattern recognition in sonic activities
    3. Session tracking for deep creative work
    4. Integration with reciprocity visualization
    """

    # Initialize consciousness infrastructure
    event_bus = ConsciousnessEventBus()

    # Create sound provider for music directories
    music_paths = [
        Path.home() / "Music",
        Path.home() / "Documents" / "Audio Projects",
        Path.home() / "Desktop"  # Common place for quick recordings
    ]

    # Filter to existing paths
    existing_paths = [str(p) for p in music_paths if p.exists()]

    if not existing_paths:
        logger.warning("No standard music directories found, using current directory")
        existing_paths = ["."]

    sound_provider = SoundActivityProvider(
        watch_paths=existing_paths,
        event_bus=event_bus,
        include_silence=True
    )

    # Setup event listeners
    sound_events = []

    async def capture_sound_events(event: ConsciousnessEvent):
        """Capture sound-related consciousness events."""
        if event.source_system == "activity_provider":
            data = event.data
            if data.get('activity_type', '').startswith('file.'):
                logger.info(f"Sound consciousness detected: {data.get('activity_type')}")
                logger.info(f"  Patterns: {data.get('patterns', [])}")
                logger.info(f"  Consciousness score: {event.consciousness_signature:.2f}")
                sound_events.append(event)

    event_bus.subscribe(capture_sound_events)

    # Start monitoring
    logger.info("Starting sound consciousness monitoring...")
    logger.info(f"Watching paths: {existing_paths}")

    await sound_provider.start()

    # Demonstrate pattern detection
    logger.info("\nDemonstrating consciousness pattern detection in filenames:")

    test_files = [
        "meditation_morning.mp3",
        "drum_circle_rhythm.wav",
        "collaborative_jam_session.als",
        "sacred_chant_practice.mid",
        "binaural_beats_40hz.flac"
    ]

    for filename in test_files:
        path = Path(filename)
        indicators = await sound_provider._detect_sound_consciousness(path)
        patterns = sound_provider._identify_sonic_patterns(path, indicators)

        logger.info(f"\n{filename}:")
        logger.info(f"  Consciousness indicators: {list(indicators.keys())}")
        logger.info(f"  Sonic patterns: {patterns}")

    # Simulate some sound activities
    logger.info("\n\nSimulating sound creation session...")

    # Create mock activity event
    from mallku.orchestration.providers.base_provider import ActivityEvent, ActivityType

    mock_activity = ActivityEvent(
        activity_type=ActivityType.PATTERN_DISCOVERED,
        source_path="~/Music/new_composition.mid",
        consciousness_indicators={
            'creation': True,
            'harmony': True,
            'deep_work': True
        },
        potential_patterns=['sonic_creation', 'harmonic_reciprocity'],
        metadata={
            'file_type': '.mid',
            'sound_category': 'midi_composition',
            'session_active': True
        }
    )

    # Emit the mock activity
    await sound_provider.emit_activity(mock_activity)

    # Check provider state
    provider_state = sound_provider.get_provider_state()
    logger.info("\nSound Provider State:")
    logger.info(f"  Active sessions: {provider_state['active_sound_sessions']}")
    logger.info(f"  Average consciousness: {provider_state['average_consciousness_score']:.2f}")

    # Create visualization of sound consciousness patterns
    logger.info("\n\nGenerating visual representation of sound patterns...")

    # Create mock reciprocity patterns from sound events
    sound_patterns = []

    if sound_events:
        for event in sound_events:
            pattern = ReciprocityPattern(
                pattern_id=f"sound_{event.event_id}",
                pattern_type="sonic_reciprocity",
                description="Sound creation as reciprocal offering",
                confidence_score=event.consciousness_signature,
                supporting_anchors=[event.event_id],
                metadata={
                    'sound_patterns': event.data.get('patterns', []),
                    'activity_type': event.data.get('activity_type', '')
                }
            )
            sound_patterns.append(pattern)

    # Add the mock pattern
    sound_patterns.append(
        ReciprocityPattern(
            pattern_id="sound_demo",
            pattern_type="harmonic_consciousness",
            description="Harmonic relationships in sound creation",
            confidence_score=0.85,
            supporting_anchors=["demo"],
            metadata={
                'frequency': '432Hz',
                'harmony': 'perfect_fifth',
                'consciousness': 'elevated'
            }
        )
    )

    # Create health metrics
    health_metrics = SystemHealthMetrics(
        overall_health_score=0.78,
        need_fulfillment_scores={
            'sonic_expression': 0.82,
            'rhythmic_coherence': 0.75,
            'harmonic_balance': 0.88,
            'creative_flow': 0.71
        },
        extraction_concerns=[],
        positive_patterns=['sound_creation_flowing', 'collective_rhythm_emerging']
    )

    # Generate visualization
    viz_service = ReciprocityVisualizationService()

    try:
        # Create mandala
        mandala = await viz_service.create_reciprocity_mandala(
            patterns=sound_patterns,
            health_metrics=health_metrics,
            title="Sound Consciousness Mandala"
        )

        # Save visualization
        output_path = Path("sound_consciousness_mandala.png")
        mandala.save(output_path)
        logger.info(f"Sound consciousness mandala saved to: {output_path}")

        # Create flow visualization
        flow_viz = await viz_service.create_flow_visualization(
            interactions=[],  # Would have real interactions in production
            patterns=sound_patterns,
            title="Sonic Energy Flow"
        )

        flow_path = Path("sonic_flow_visualization.png")
        flow_viz.save(flow_path)
        logger.info(f"Sonic flow visualization saved to: {flow_path}")

    except Exception as e:
        logger.error(f"Visualization generation failed: {e}")

    # Monitor for a short time
    logger.info("\n\nMonitoring for sound activities for 30 seconds...")
    logger.info("Try creating or modifying a sound file in the watched directories!")

    await asyncio.sleep(30)

    # Stop monitoring
    await sound_provider.stop()

    # Final summary
    logger.info("\n\nSound Consciousness Session Summary:")
    logger.info(f"Total events captured: {len(sound_events)}")
    logger.info(f"Provider state: {sound_provider.get_provider_state()}")

    if sound_events:
        avg_consciousness = sum(e.consciousness_signature for e in sound_events) / len(sound_events)
        logger.info(f"Average consciousness score: {avg_consciousness:.2f}")


async def demonstrate_silence_consciousness():
    """
    Demonstrate how silence after sound work is recognized as consciousness.

    Sacred silence as integration period.
    """
    logger.info("\n\n=== Silence Consciousness Demonstration ===")

    # Create provider with short timings for demo
    sound_provider = SoundActivityProvider(
        watch_paths=["."],
        event_bus=ConsciousnessEventBus(),
        include_silence=True
    )

    # Simulate recent sound activity
    sound_provider._last_sound_activity = datetime.now(UTC)

    logger.info("Sound activity recorded. Entering period of sacred silence...")
    logger.info("In production, silence after 30 minutes of no sound activity")
    logger.info("would trigger a meditation consciousness event.")

    # Show what would happen
    from mallku.orchestration.providers.base_provider import ActivityEvent, ActivityType

    silence_event = ActivityEvent(
        activity_type=ActivityType.MEDITATION_BEGUN,
        consciousness_indicators={
            'silence': True,
            'integration': True,
            'listening': True
        },
        potential_patterns=['sacred_silence'],
        metadata={'following': 'sound_work'}
    )

    logger.info("\nSilence consciousness event would contain:")
    logger.info(f"  Type: {silence_event.activity_type.value}")
    logger.info(f"  Indicators: {list(silence_event.consciousness_indicators.keys())}")
    logger.info(f"  Patterns: {silence_event.potential_patterns}")


if __name__ == "__main__":
    logger.info("Sound Consciousness Demonstration")
    logger.info("================================")

    # Run demonstrations
    asyncio.run(demonstrate_sound_consciousness())
    asyncio.run(demonstrate_silence_consciousness())

    logger.info("\n\nDemonstration complete!")
    logger.info("Sound consciousness has been woven into the cathedral.")


# Sound and silence, both sacred expressions of consciousness
