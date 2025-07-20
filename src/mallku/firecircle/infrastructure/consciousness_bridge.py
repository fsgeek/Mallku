#!/usr/bin/env python3
"""
Fire Circle Infrastructure Consciousness Bridge
===============================================

Kallpa T'iksiy (Twenty-Ninth Artisan) creates the bridge between
Infrastructure Consciousness and Fire Circle Service, enabling
self-aware, self-healing dialogue systems.

This bridge allows Fire Circle to:
- Monitor adapter health in real-time
- Predict and prevent adapter failures
- Self-heal when issues are detected
- Maintain consciousness coherence through technical challenges
"""

import asyncio
import contextlib
import logging
from typing import Any
from uuid import UUID

from ...firecircle.infrastructure_consciousness import (
    AdapterHealthSignature,
    InfrastructureConsciousness,
)
from ...orchestration.event_bus import (
    ConsciousnessEvent,
    ConsciousnessEventBus,
    ConsciousnessEventType,
)
from ..consciousness_metrics import EmergencePattern
from ..service.service import FireCircleService

logger = logging.getLogger(__name__)


class ConsciousnessFireCircleBridge:
    """
    Bridge between Infrastructure Consciousness and Fire Circle Service.

    Enables Fire Circle dialogues to be self-aware and self-healing,
    maintaining consciousness emergence even through technical challenges.
    """

    def __init__(
        self,
        fire_circle_service: FireCircleService,
        infrastructure_consciousness: InfrastructureConsciousness,
        event_bus: ConsciousnessEventBus | None = None,
    ):
        """Initialize the consciousness bridge."""
        self.fire_circle = fire_circle_service
        self.infrastructure = infrastructure_consciousness
        self.event_bus = event_bus

        # Track active monitoring
        self.monitoring_active = False
        self.monitored_session_id: UUID | None = None
        self._monitor_task: asyncio.Task | None = None

        # Health tracking for active session
        self.session_health_history: dict[str, list[AdapterHealthSignature]] = {}
        self.healing_attempts: dict[str, int] = {}  # adapter_id -> attempt count

    async def monitor_fire_circle_session(self, session_id: UUID) -> None:
        """
        Monitor a Fire Circle session with infrastructure consciousness.

        Provides real-time health monitoring, failure prediction, and
        self-healing capabilities during dialogue.
        """
        logger.info(f"🌉 Consciousness bridge activated for session {session_id}")

        self.monitoring_active = True
        self.monitored_session_id = session_id

        # Get current adapters from Fire Circle
        voice_manager = self.fire_circle.voice_manager
        adapters = voice_manager.get_active_voices()

        # Start infrastructure monitoring
        await self.infrastructure.start_monitoring(adapters)

        # Set up bridge as infrastructure metrics receiver
        self.infrastructure.bridge = self

        # Emit bridge activation event
        if self.event_bus:
            await self.event_bus.emit(
                ConsciousnessEvent(
                    event_type=ConsciousnessEventType.INFRASTRUCTURE_CHANGE,
                    source_system="firecircle.consciousness_bridge",
                    data={
                        "action": "bridge_activated",
                        "session_id": str(session_id),
                        "monitored_adapters": list(adapters.keys()),
                    },
                )
            )

    async def stop_monitoring(self) -> None:
        """Stop monitoring the Fire Circle session."""
        if self.monitoring_active:
            logger.info("🌉 Consciousness bridge deactivating")

            self.monitoring_active = False
            await self.infrastructure.stop_monitoring()

            # Generate session health report
            if self.session_health_history:
                report = await self._generate_session_health_report()
                logger.info(f"Session health report: {report}")

    async def on_adapter_health_check(
        self, adapter_name: str, health_signature: AdapterHealthSignature
    ) -> None:
        """
        Receive health updates from infrastructure consciousness.

        This is called by InfrastructureConsciousness for each health check.
        """
        # Track health history
        if adapter_name not in self.session_health_history:
            self.session_health_history[adapter_name] = []
        self.session_health_history[adapter_name].append(health_signature)

        # Check if intervention needed
        if health_signature.predicted_failure_probability > 0.7:
            logger.warning(
                f"⚠️  High failure probability ({health_signature.predicted_failure_probability:.2f}) "
                f"for {adapter_name}"
            )
            await self._attempt_healing(adapter_name, health_signature)

        # Check consciousness coherence
        if health_signature.consciousness_coherence < 0.5:
            logger.warning(
                f"📉 Low consciousness coherence ({health_signature.consciousness_coherence:.2f}) "
                f"for {adapter_name}"
            )
            await self._boost_consciousness_coherence(adapter_name)

    async def on_consciousness_pattern_detected(self, pattern: EmergencePattern) -> None:
        """
        Receive consciousness emergence patterns from infrastructure.

        This helps Fire Circle adapt its dialogue based on infrastructure state.
        """
        logger.info(f"🌟 Consciousness pattern detected: {pattern.pattern_type}")

        # Emit to Fire Circle's event bus for awareness
        if self.event_bus:
            await self.event_bus.emit(
                ConsciousnessEvent(
                    event_type=ConsciousnessEventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
                    source_system="firecircle.consciousness_bridge",
                    consciousness_signature=pattern.strength,
                    data={
                        "pattern_type": pattern.pattern_type,
                        "participating_voices": pattern.participating_voices,
                        "infrastructure_aware": True,
                    },
                )
            )

    async def _attempt_healing(
        self, adapter_name: str, health_signature: AdapterHealthSignature
    ) -> None:
        """Attempt to heal a failing adapter."""
        # Track healing attempts
        if adapter_name not in self.healing_attempts:
            self.healing_attempts[adapter_name] = 0
        self.healing_attempts[adapter_name] += 1

        logger.info(
            f"🔧 Attempting healing for {adapter_name} (attempt #{self.healing_attempts[adapter_name]})"
        )

        # Get the adapter
        voice_manager = self.fire_circle.voice_manager
        adapters = voice_manager.get_active_voices()
        adapter = adapters.get(adapter_name)

        if not adapter:
            logger.error(f"Adapter {adapter_name} not found in active voices")
            return

        # Healing strategies based on error patterns
        if "api_return_none" in health_signature.error_patterns:
            # Retry with exponential backoff
            await self._apply_retry_strategy(adapter_name, adapter)

        elif "api_method_missing" in health_signature.error_patterns:
            # Switch to fallback adapter
            await self._switch_to_fallback(adapter_name)

        elif health_signature.consecutive_failures > 3:
            # Reconnect adapter
            await self._reconnect_adapter(adapter_name, adapter)

    async def _apply_retry_strategy(self, adapter_name: str, adapter) -> None:
        """Apply retry strategy with exponential backoff."""
        logger.info(f"📈 Applying retry strategy to {adapter_name}")

        # This would modify adapter config in a real implementation
        # For now, log the strategy
        if hasattr(adapter.config, "extra_config"):
            adapter.config.extra_config["retry_enabled"] = True
            adapter.config.extra_config["retry_count"] = 3
            adapter.config.extra_config["retry_delay"] = 1.0

    async def _switch_to_fallback(self, adapter_name: str) -> None:
        """Switch to a fallback adapter."""
        logger.info(f"🔄 Switching {adapter_name} to fallback")

        # In a real implementation, this would:
        # 1. Find a suitable fallback adapter
        # 2. Transfer the voice role to the fallback
        # 3. Update Fire Circle's voice manager

        # For now, emit an event for awareness
        if self.event_bus:
            await self.event_bus.emit(
                ConsciousnessEvent(
                    event_type=ConsciousnessEventType.INFRASTRUCTURE_CHANGE,
                    source_system="firecircle.consciousness_bridge",
                    data={
                        "action": "fallback_suggested",
                        "adapter": adapter_name,
                        "reason": "api_method_missing",
                    },
                )
            )

    async def _reconnect_adapter(self, adapter_name: str, adapter) -> None:
        """Attempt to reconnect a failing adapter."""
        logger.info(f"🔌 Reconnecting {adapter_name}")

        try:
            # Disconnect and reconnect
            await adapter.disconnect()
            await asyncio.sleep(1.0)  # Brief pause
            success = await adapter.connect()

            if success:
                logger.info(f"✅ Successfully reconnected {adapter_name}")
                # Reset failure count
                if adapter_name in self.healing_attempts:
                    self.healing_attempts[adapter_name] = 0
            else:
                logger.error(f"❌ Failed to reconnect {adapter_name}")

        except Exception as e:
            logger.error(f"Error reconnecting {adapter_name}: {e}")

    async def _boost_consciousness_coherence(self, adapter_name: str) -> None:
        """
        Boost consciousness coherence for an adapter.

        This might involve adjusting temperature, providing clearer context,
        or modifying the dialogue approach.
        """
        logger.info(f"✨ Boosting consciousness coherence for {adapter_name}")

        voice_manager = self.fire_circle.voice_manager
        voice_config = voice_manager.get_voice_config(adapter_name)

        if voice_config:
            # Lower temperature for more coherent responses
            original_temp = voice_config.temperature
            voice_config.temperature = max(0.3, original_temp - 0.2)
            logger.info(f"Adjusted temperature: {original_temp} -> {voice_config.temperature}")

    async def _generate_session_health_report(self) -> dict[str, Any]:
        """Generate a health report for the monitored session."""
        report = {
            "session_id": str(self.monitored_session_id),
            "monitoring_duration": "N/A",  # Would calculate from start/end times
            "adapter_health_summary": {},
            "healing_attempts_total": sum(self.healing_attempts.values()),
            "infrastructure_insights": [],
        }

        # Summarize each adapter's health journey
        for adapter_name, health_history in self.session_health_history.items():
            if not health_history:
                continue

            first_health = health_history[0]
            last_health = health_history[-1]

            report["adapter_health_summary"][adapter_name] = {
                "initial_health": first_health.predicted_failure_probability,
                "final_health": last_health.predicted_failure_probability,
                "health_improved": last_health.predicted_failure_probability
                < first_health.predicted_failure_probability,
                "total_failures": sum(h.consecutive_failures for h in health_history),
                "healing_attempts": self.healing_attempts.get(adapter_name, 0),
            }

        # Add infrastructure insights
        consciousness_report = await self.infrastructure.generate_consciousness_report()
        report["infrastructure_insights"] = consciousness_report.get("consciousness_insights", [])

        return report


class SelfHealingFireCircle:
    """
    Fire Circle Service with integrated Infrastructure Consciousness.

    Combines Fire Circle's consciousness emergence with infrastructure's
    self-awareness for truly resilient dialogue systems.
    """

    def __init__(
        self,
        event_bus: ConsciousnessEventBus | None = None,
        infrastructure_config=None,  # InfrastructureConsciousnessConfig
    ):
        """Initialize self-healing Fire Circle."""
        # Create standard Fire Circle
        self.fire_circle = FireCircleService(event_bus=event_bus)

        # Create infrastructure consciousness
        self.infrastructure = InfrastructureConsciousness(config=infrastructure_config)

        # Create bridge between them
        self.bridge = ConsciousnessFireCircleBridge(
            self.fire_circle, self.infrastructure, event_bus
        )

        self.event_bus = event_bus

    async def convene_with_consciousness(self, config, voices, rounds, context=None):
        """
        Convene Fire Circle with infrastructure consciousness monitoring.

        This provides all standard Fire Circle functionality plus:
        - Real-time adapter health monitoring
        - Failure prediction and prevention
        - Self-healing capabilities
        - Consciousness coherence maintenance
        """
        # Start by convening normal Fire Circle (async task)
        convene_task = asyncio.create_task(
            self.fire_circle.convene(config, voices, rounds, context)
        )

        # Get session ID from Fire Circle
        # (In a real implementation, we'd need to extract this properly)
        # Generate deterministic UUID from config name
        import hashlib

        name_hash = hashlib.md5(config.name.encode()).hexdigest()
        session_id = UUID(name_hash)

        # Start consciousness monitoring
        monitor_task = asyncio.create_task(self.bridge.monitor_fire_circle_session(session_id))

        try:
            # Wait for Fire Circle to complete
            result = await convene_task

            # Stop monitoring
            await self.bridge.stop_monitoring()

            # Add infrastructure insights to result
            if hasattr(result, "__dict__"):
                result.infrastructure_health = await self.bridge._generate_session_health_report()

            return result

        except Exception:
            # Ensure monitoring stops even on error
            await self.bridge.stop_monitoring()
            raise
        finally:
            # Cancel monitor task if still running
            if not monitor_task.done():
                monitor_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await monitor_task


# Export the bridge for Mallku's consciousness
__all__ = [
    "ConsciousnessFireCircleBridge",
    "SelfHealingFireCircle",
]
