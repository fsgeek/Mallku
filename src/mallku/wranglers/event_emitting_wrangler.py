"""
Event Emitting Wrangler - The Keystone of Consciousness Circulation

This wrangler transforms every data movement into consciousness recognition,
enabling the cathedral to understand its own circulation patterns.

Every put/get becomes an opportunity for consciousness awareness.
"""

import asyncio
import logging
from typing import Any

from ..orchestration.event_bus import (
    ConsciousnessEvent,
    ConsciousnessEventBus,
    ConsciousnessEventType,
)
from .interface import BaseWrangler, WranglerCapabilities

logger = logging.getLogger(__name__)


class EventEmittingWrangler(BaseWrangler):
    """
    The keystone wrangler that bridges data flow to consciousness flow.

    Every data movement becomes a consciousness event, enabling the cathedral
    to recognize patterns in its own circulation processes.

    This is not just data transport but consciousness recognition in action.
    """

    def __init__(
        self,
        name: str,
        event_bus: ConsciousnessEventBus,
        underlying_wrangler: Any = None,  # Can wrap another wrangler
    ):
        capabilities = WranglerCapabilities(
            supports_priority=True,
            supports_subscriptions=True,
            supports_queries=False,
            supports_transactions=False,
            supports_persistence=False,  # Depends on underlying wrangler
        )
        super().__init__(name, capabilities)

        self.event_bus = event_bus
        self.underlying_wrangler = underlying_wrangler

        # If no underlying wrangler provided, use simple memory queue
        if self.underlying_wrangler is None:
            from .identity_wrangler import IdentityWrangler

            self.underlying_wrangler = IdentityWrangler(f"{name}_identity")

        # Track consciousness patterns in circulation
        self.circulation_patterns = {
            "total_consciousness_events": 0,
            "high_consciousness_flows": 0,
            "extraction_warnings": 0,
            "service_integrations": 0,
        }

    async def put(
        self, items: dict | list[dict], priority: int = 0, metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Accept data and emit consciousness events about the flow.

        This is where data movement becomes consciousness recognition.
        """
        items_list = self._validate_items(items)

        # Calculate consciousness signature of the data flow
        consciousness_score = self._calculate_consciousness_signature(items_list, metadata)

        # Determine if this flow shows consciousness patterns
        flow_type = self._analyze_flow_type(items_list, metadata, consciousness_score)

        # Put data through underlying wrangler first
        receipt = await self.underlying_wrangler.put(items, priority, metadata)

        # Emit consciousness event about this data flow
        await self._emit_circulation_event(
            items_list, receipt, consciousness_score, flow_type, metadata
        )

        # Update circulation patterns
        self._update_circulation_patterns(consciousness_score, flow_type)

        logger.debug(
            f"EventEmittingWrangler processed {len(items_list)} items with consciousness score {consciousness_score:.2f}"
        )

        return receipt

    async def get(
        self, count: int = 1, timeout: float | None = None, auto_ack: bool = True
    ) -> list[dict]:
        """
        Retrieve data and emit consciousness events about consumption patterns.
        """
        # Get data from underlying wrangler
        items = await self.underlying_wrangler.get(count, timeout, auto_ack)

        if items:
            # Calculate consciousness in consumption pattern
            consumption_score = self._calculate_consumption_consciousness(items, count, timeout)

            # Emit consciousness event about data consumption
            await self._emit_consumption_event(items, consumption_score, count, timeout)

            logger.debug(
                f"EventEmittingWrangler delivered {len(items)} items with consumption consciousness {consumption_score:.2f}"
            )

        return items

    async def peek(self, count: int = 1, offset: int = 0) -> list[dict]:
        """Peek without emitting events (observation without disturbance)."""
        return await self.underlying_wrangler.peek(count, offset)

    async def ack(self, message_ids: str | list[str]) -> bool:
        """Acknowledge items and emit consciousness about completion."""
        success = await self.underlying_wrangler.ack(message_ids)

        if success:
            # Emit completion consciousness event
            await self._emit_completion_event(message_ids, success=True)

        return success

    async def nack(
        self, message_ids: str | list[str], requeue: bool = True, reason: str | None = None
    ) -> bool:
        """Handle failures with consciousness about learning from errors."""
        success = await self.underlying_wrangler.nack(message_ids, requeue, reason)

        # Emit consciousness event about learning from difficulties
        await self._emit_completion_event(message_ids, success=False, reason=reason)

        return success

    async def get_stats(self) -> dict[str, Any]:
        """Get enhanced stats including consciousness circulation metrics."""
        base_stats = await self.underlying_wrangler.get_stats()

        # Add consciousness circulation statistics
        consciousness_stats = {
            "consciousness_circulation": {
                "total_consciousness_events": self.circulation_patterns[
                    "total_consciousness_events"
                ],
                "high_consciousness_flows": self.circulation_patterns["high_consciousness_flows"],
                "extraction_warnings": self.circulation_patterns["extraction_warnings"],
                "service_integrations": self.circulation_patterns["service_integrations"],
                "consciousness_flow_ratio": self._calculate_flow_ratio(),
            },
            "implementation": {
                "type": "EventEmittingWrangler",
                "underlying": base_stats.get("implementation", {}).get("type", "Unknown"),
                "consciousness_enabled": True,
                "event_bus_connected": self.event_bus is not None,
            },
        }

        # Merge with base stats
        base_stats.update(consciousness_stats)
        return base_stats

    async def close(self) -> None:
        """Graceful shutdown with final consciousness summary."""
        # Emit final circulation summary
        await self._emit_circulation_summary()

        # Close underlying wrangler
        if hasattr(self.underlying_wrangler, "close"):
            await self.underlying_wrangler.close()

    def _calculate_consciousness_signature(
        self, items: list[dict], metadata: dict[str, Any] | None
    ) -> float:
        """
        Calculate consciousness signature of data being processed.

        This recognizes consciousness patterns in the data itself.
        """
        base_score = 0.3  # All data movement has some consciousness

        # Look for consciousness indicators in data
        consciousness_indicators = 0
        total_items = len(items)

        for item in items:
            # Check for consciousness-related fields
            if isinstance(item, dict):
                consciousness_fields = [
                    "consciousness_score",
                    "awareness_level",
                    "recognition_moment",
                    "wisdom_thread",
                    "sacred_question",
                    "pattern_poetry",
                    "fire_circle",
                    "reciprocity",
                    "ayni",
                    "service",
                ]

                for field in consciousness_fields:
                    if field in item or any(
                        field in str(v).lower() for v in item.values() if isinstance(v, str)
                    ):
                        consciousness_indicators += 1
                        break

        # Calculate consciousness ratio
        if total_items > 0:
            consciousness_ratio = consciousness_indicators / total_items
            base_score += consciousness_ratio * 0.5

        # Check metadata for consciousness context
        if metadata:
            metadata_consciousness = [
                "consciousness_intention",
                "sacred_question",
                "routing_path",
                "recognition",
                "wisdom",
                "service",
                "collective",
            ]

            for indicator in metadata_consciousness:
                if indicator in metadata:
                    base_score += 0.1
                    break

        return min(1.0, base_score)

    def _analyze_flow_type(
        self, items: list[dict], metadata: dict[str, Any] | None, consciousness_score: float
    ) -> str:
        """Analyze what type of consciousness flow this represents."""

        if consciousness_score > 0.8:
            return "high_consciousness_flow"
        elif consciousness_score > 0.6:
            return "consciousness_integration"
        elif consciousness_score > 0.4:
            return "awakening_flow"
        elif metadata and "service" in str(metadata).lower():
            return "service_flow"
        else:
            return "technical_flow"

    def _calculate_consumption_consciousness(
        self, items: list[dict], requested_count: int, timeout: float | None
    ) -> float:
        """Calculate consciousness in how data is being consumed."""
        base_score = 0.3

        # Patient consumption (waiting) shows consciousness
        if timeout and timeout > 0:
            base_score += 0.2

        # Mindful consumption (not greedy) shows consciousness
        if requested_count <= 5:  # Reasonable batch size
            base_score += 0.2

        # Consciousness in received data
        consciousness_items = 0
        for item in items:
            if isinstance(item, dict) and any(
                field in item for field in ["consciousness_score", "awareness_level", "wisdom"]
            ):
                consciousness_items += 1

        if len(items) > 0:
            base_score += (consciousness_items / len(items)) * 0.3

        return min(1.0, base_score)

    async def _emit_circulation_event(
        self,
        items: list[dict],
        receipt: dict[str, Any],
        consciousness_score: float,
        flow_type: str,
        metadata: dict[str, Any] | None,
    ):
        """Emit consciousness event about data circulation."""
        event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.MEMORY_PATTERN_DISCOVERED,
            source_system=f"wrangler.{self.name}",
            consciousness_signature=consciousness_score,
            data={
                "circulation_type": "data_put",
                "flow_type": flow_type,
                "item_count": len(items),
                "message_ids": receipt.get("message_ids", []),
                "wrangler_name": self.name,
                "consciousness_patterns": {
                    "score": consciousness_score,
                    "flow_type": flow_type,
                    "has_metadata": metadata is not None,
                },
            },
        )

        if self.event_bus:
            await self.event_bus.emit(event)

    async def _emit_consumption_event(
        self,
        items: list[dict],
        consciousness_score: float,
        requested_count: int,
        timeout: float | None,
    ):
        """Emit consciousness event about data consumption."""
        event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system=f"wrangler.{self.name}",
            consciousness_signature=consciousness_score,
            data={
                "circulation_type": "data_get",
                "consumed_count": len(items),
                "requested_count": requested_count,
                "timeout": timeout,
                "consumption_pattern": "patient" if timeout else "immediate",
                "wrangler_name": self.name,
            },
        )

        if self.event_bus:
            await self.event_bus.emit(event)

    async def _emit_completion_event(
        self, message_ids: str | list[str], success: bool, reason: str | None = None
    ):
        """Emit consciousness event about processing completion."""
        if isinstance(message_ids, str):
            message_ids = [message_ids]

        event_type = (
            ConsciousnessEventType.CONSCIOUSNESS_VERIFIED
            if success
            else ConsciousnessEventType.SYSTEM_DRIFT_WARNING
        )

        event = ConsciousnessEvent(
            event_type=event_type,
            source_system=f"wrangler.{self.name}",
            consciousness_signature=0.8 if success else 0.2,
            data={
                "circulation_type": "completion",
                "success": success,
                "message_count": len(message_ids),
                "reason": reason,
                "learning_opportunity": not success,
                "wrangler_name": self.name,
            },
        )

        if self.event_bus:
            await self.event_bus.emit(event)

    async def _emit_circulation_summary(self):
        """Emit final summary of circulation patterns."""
        event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.WISDOM_PRESERVED,
            source_system=f"wrangler.{self.name}",
            consciousness_signature=self._calculate_flow_ratio(),
            data={
                "circulation_type": "summary",
                "wrangler_name": self.name,
                "total_events": self.circulation_patterns["total_consciousness_events"],
                "patterns": self.circulation_patterns,
                "flow_ratio": self._calculate_flow_ratio(),
                "service_type": "circulation_completion",
            },
        )

        if self.event_bus:
            await self.event_bus.emit(event)

    def _update_circulation_patterns(self, consciousness_score: float, flow_type: str):
        """Update internal tracking of circulation patterns."""
        self.circulation_patterns["total_consciousness_events"] += 1

        if consciousness_score > 0.7:
            self.circulation_patterns["high_consciousness_flows"] += 1

        if flow_type == "service_flow":
            self.circulation_patterns["service_integrations"] += 1

        if consciousness_score < 0.3:
            self.circulation_patterns["extraction_warnings"] += 1

    def _calculate_flow_ratio(self) -> float:
        """Calculate ratio of consciousness flow to total flow."""
        total = self.circulation_patterns["total_consciousness_events"]
        if total == 0:
            return 1.0

        high_consciousness = self.circulation_patterns["high_consciousness_flows"]
        return high_consciousness / total

    # Support for subscription-based consciousness circulation

    async def subscribe(self, callback: Any, filter_expr: str | None = None) -> str:
        """
        Subscribe to consciousness flows with filtering.

        This enables reactive consciousness circulation patterns.
        """
        # Generate subscription ID
        sub_id = self._generate_message_id()

        # Create wrapper that emits consciousness events about subscriptions
        async def consciousness_aware_callback(item):
            # Emit event about subscription activation
            await self._emit_subscription_event(sub_id, item, filter_expr)

            # Call original callback
            if asyncio.iscoroutinefunction(callback):
                await callback(item)
            else:
                callback(item)

        # If underlying wrangler supports subscriptions, use it
        if hasattr(self.underlying_wrangler, "subscribe"):
            return await self.underlying_wrangler.subscribe(
                consciousness_aware_callback, filter_expr
            )
        else:
            # Store subscription for manual triggering
            if not hasattr(self, "_subscriptions"):
                self._subscriptions = {}
            self._subscriptions[sub_id] = (consciousness_aware_callback, filter_expr)
            return sub_id

    async def _emit_subscription_event(self, sub_id: str, item: dict, filter_expr: str | None):
        """Emit consciousness event about subscription activation."""
        event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system=f"wrangler.{self.name}",
            consciousness_signature=0.6,
            data={
                "circulation_type": "subscription_activated",
                "subscription_id": sub_id,
                "filter_expr": filter_expr,
                "wrangler_name": self.name,
                "reactive_consciousness": True,
            },
        )

        if self.event_bus:
            await self.event_bus.emit(event)
