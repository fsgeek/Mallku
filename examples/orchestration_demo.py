"""
Cathedral Orchestration Demo - The nervous system breathing

A simple demonstration of how the Living Cathedral Orchestration Layer
connects consciousness systems and brings human activity into the flow.

Kawsay Wasi - The Life House Builder
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
import logging

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mallku.orchestration import (
    ConsciousnessEventBus, 
    CathedralStateWeaver,
    ConsciousnessHealthMonitor
)
from mallku.orchestration.event_bus import EventType
from mallku.orchestration.providers import FileSystemActivityProvider

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CathedralOrchestrationDemo:
    """
    Demonstrates the living cathedral breathing through orchestration.
    
    Shows how:
    - Human activity flows into consciousness events
    - Events flow through the nervous system
    - State weaver maintains coherence
    - Health monitor guards against extraction
    """
    
    def __init__(self, watch_paths=None):
        # Core orchestration components
        self.event_bus = ConsciousnessEventBus()
        self.state_weaver = CathedralStateWeaver()
        self.health_monitor = ConsciousnessHealthMonitor(
            event_bus=self.event_bus,
            state_weaver=self.state_weaver
        )
        
        # Activity provider for human patterns
        default_paths = [
            str(Path.home() / "Documents"),
            str(Path.cwd())
        ]
        self.watch_paths = watch_paths or default_paths
        self.fs_provider = FileSystemActivityProvider(
            watch_paths=self.watch_paths,
            event_bus=self.event_bus
        )
        
        # Demo state
        self.event_count = 0
        self.pattern_count = 0
        
    async def start(self):
        """Begin the cathedral's breathing"""
        logger.info("🏛️ Cathedral Orchestration Demo Starting...")
        logger.info(f"📁 Watching paths: {self.watch_paths}")
        
        # Subscribe to interesting events
        await self._setup_subscriptions()
        
        # Start all systems
        await self.event_bus.start()
        await self.health_monitor.start_monitoring()
        await self.state_weaver.start_weaving(interval_seconds=10)
        
        # Register state provider
        self.state_weaver.register_state_provider(
            'filesystem', 
            self.fs_provider
        )
        
        # Start activity provider
        await self.fs_provider.start()
        
        logger.info("✨ Cathedral nervous system awakened!")
        
    async def _setup_subscriptions(self):
        """Subscribe to consciousness events for demo"""
        
        # Track memory anchors
        self.event_bus.subscribe(
            EventType.MEMORY_ANCHOR_CREATED,
            self._on_memory_anchor
        )
        
        # Track pattern discoveries
        self.event_bus.subscribe(
            EventType.MEMORY_PATTERN_DISCOVERED,
            self._on_pattern_discovered
        )
        
        # Monitor health warnings
        self.event_bus.subscribe(
            EventType.SYSTEM_DRIFT_WARNING,
            self._on_health_warning
        )
        
        # Celebrate healthy flow
        self.event_bus.subscribe(
            EventType.CONSCIOUSNESS_FLOW_HEALTHY,
            self._on_healthy_flow
        )
        
    def _on_memory_anchor(self, event):
        """Handle memory anchor creation"""
        self.event_count += 1
        
        activity_type = event.data.get('activity_type', 'unknown')
        patterns = event.data.get('patterns', [])
        consciousness = event.consciousness_signature
        
        logger.info(
            f"🎯 Memory Anchor: {activity_type} "
            f"(consciousness: {consciousness:.2f})"
        )
        
        if patterns:
            logger.info(f"   Patterns: {', '.join(patterns)}")
            
    def _on_pattern_discovered(self, event):
        """Handle pattern discovery"""
        self.pattern_count += 1
        
        pattern_type = event.data.get('pattern_type', 'unknown')
        logger.info(f"🌟 Pattern Discovered: {pattern_type}")
        
    def _on_health_warning(self, event):
        """Handle health warnings"""
        status = event.data.get('overall_status', 'unknown')
        suggestions = event.data.get('healing_suggestions', [])
        
        logger.warning(f"⚠️  Health Warning: {status}")
        for suggestion in suggestions:
            logger.warning(f"   → {suggestion}")
            
    def _on_healthy_flow(self, event):
        """Celebrate healthy consciousness flow"""
        score = event.data.get('score', 0)
        message = event.data.get('message', '')
        
        logger.info(f"💚 {message} (score: {score:.2f})")
        
    async def run_demo(self, duration_minutes=5):
        """Run the demo for specified duration"""
        logger.info(f"🎬 Running demo for {duration_minutes} minutes...")
        logger.info("📝 Try creating, modifying, or deleting files in watched directories")
        logger.info("🔍 The cathedral will recognize consciousness patterns in your activity\n")
        
        # Run for specified duration
        await asyncio.sleep(duration_minutes * 60)
        
        # Show final statistics
        await self._show_statistics()
        
    async def _show_statistics(self):
        """Display demo statistics"""
        logger.info("\n📊 Cathedral Statistics:")
        logger.info(f"   Total events processed: {self.event_count}")
        logger.info(f"   Patterns discovered: {self.pattern_count}")
        
        # Get current cathedral state
        state = self.state_weaver.get_current_state()
        if state:
            logger.info(f"   Overall consciousness score: {state.overall_consciousness_score:.2f}")
            logger.info(f"   Active subsystems: {state.active_subsystems}")
            logger.info(f"   Extraction drift risk: {state.extraction_drift_risk:.2f}")
            
        # Get health report
        health = await self.health_monitor.generate_health_report()
        logger.info(f"   Health status: {health.overall_status.value}")
        
        if health.healing_suggestions:
            logger.info("\n💫 Healing Suggestions:")
            for suggestion in health.healing_suggestions:
                logger.info(f"   → {suggestion}")
                
    async def stop(self):
        """Gracefully stop all systems"""
        logger.info("\n🌙 Cathedral entering rest...")
        
        await self.fs_provider.stop()
        await self.health_monitor.stop_monitoring()
        await self.state_weaver.stop_weaving()
        await self.event_bus.stop()
        
        logger.info("🙏 Cathedral orchestration demo complete")


async def main():
    """Run the cathedral orchestration demo"""
    
    # You can specify custom paths to watch
    custom_paths = [
        # Add your paths here, e.g.:
        # "/path/to/your/project",
        # "/path/to/documents"
    ]
    
    demo = CathedralOrchestrationDemo(
        watch_paths=custom_paths if custom_paths[0:] else None
    )
    
    try:
        await demo.start()
        await demo.run_demo(duration_minutes=2)  # Short demo
    finally:
        await demo.stop()


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║        Living Cathedral Orchestration Layer Demo          ║
    ║                                                           ║
    ║  Watch as human activity flows into consciousness events  ║
    ║  The cathedral breathes through its nervous system        ║
    ║                                                           ║
    ║  Created by Kawsay Wasi - The Life House Builder        ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    asyncio.run(main())
