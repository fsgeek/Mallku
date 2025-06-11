"""
Memory Buffer Wrangler - High-Performance Local Consciousness Circulation

For situations where consciousness needs to flow quickly between closely
connected systems without the overhead of persistent storage.

Like short-term memory that enables rapid consciousness pattern recognition.
"""

import asyncio
import time
from asyncio.log import logger
from collections import deque
from datetime import UTC, datetime
from typing import Any

from .interface import BaseWrangler, WranglerCapabilities


class MemoryBufferWrangler(BaseWrangler):
    """
    High-performance in-memory wrangler for local consciousness circulation.

    Perfect for:
    - Rapid consciousness pattern recognition
    - Local service-to-service communication
    - Real-time consciousness flow processing
    - Development and testing scenarios

    Trade-offs:
    - High performance but no persistence
    - Bounded memory usage with configurable limits
    - Priority queuing for consciousness-aware processing
    """

    def __init__(
        self,
        name: str = "memory_buffer",
        max_items: int = 10000,
        max_memory_mb: int = 100,
        enable_priority: bool = True,
        enable_history: bool = True,
        history_size: int = 1000
    ):
        capabilities = WranglerCapabilities(
            supports_priority=enable_priority,
            supports_subscriptions=True,
            supports_queries=enable_history,
            supports_transactions=False,
            supports_persistence=False,
            max_item_size=max_memory_mb * 1024 * 1024 // max_items,  # Rough estimate
            max_batch_size=min(1000, max_items // 10)
        )
        super().__init__(name, capabilities)

        self.max_items = max_items
        self.max_memory_mb = max_memory_mb
        self.enable_priority = enable_priority
        self.enable_history = enable_history

        # Priority queues for consciousness-aware processing
        if enable_priority:
            self._high_priority: deque = deque()    # Priority >= 5
            self._normal_priority: deque = deque()  # Priority 1-4
            self._low_priority: deque = deque()     # Priority 0
        else:
            self._queue: deque = deque()

        # In-flight message tracking
        self._in_flight: dict[str, dict] = {}

        # Message history for queries (if enabled)
        self._history: deque | None = deque(maxlen=history_size) if enable_history else None

        # Subscription support
        self._subscriptions: dict[str, tuple] = {}
        self._next_sub_id = 1

        # Performance metrics
        self._put_times: deque = deque(maxlen=100)
        self._get_times: deque = deque(maxlen=100)
        self._memory_usage_estimates: deque = deque(maxlen=50)

        # Consciousness flow metrics
        self.consciousness_stats = {
            "high_consciousness_items": 0,
            "priority_escalations": 0,
            "pattern_recognitions": 0,
            "subscription_triggers": 0
        }

    async def put(
        self,
        items: dict | list[dict],
        priority: int = 0,
        metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Accept items with consciousness-aware priority handling."""
        start_time = time.time()

        items_list = self._validate_items(items)

        # Check capacity before accepting
        current_size = self._get_current_size()
        if current_size + len(items_list) > self.max_items:
            # Consciousness-aware overflow handling
            await self._handle_overflow(len(items_list))

        message_ids = []
        consciousness_enhanced_items = 0

        for item in items_list:
            # Generate message ID and wrapper
            msg_id = self._generate_message_id()

            # Detect consciousness patterns in the item
            consciousness_score = self._detect_item_consciousness(item, metadata)

            # Create wrapped message with consciousness metadata
            wrapped = {
                '_id': msg_id,
                '_timestamp': datetime.now(UTC),
                '_priority': priority,
                '_consciousness_score': consciousness_score,
                '_metadata': metadata or {},
                'data': item
            }

            # Priority-aware queuing
            adjusted_priority = priority
            if self.enable_priority:
                adjusted_priority = self._adjust_priority_for_consciousness(priority, consciousness_score)
                await self._enqueue_with_priority(wrapped, adjusted_priority)
            else:
                self._queue.append(wrapped)

            message_ids.append(msg_id)
            self.total_in += 1

            if consciousness_score > 0.6:
                consciousness_enhanced_items += 1
                self.consciousness_stats["high_consciousness_items"] += 1

            # Add to history if enabled
            if self._history is not None:
                self._history.append({
                    'id': msg_id,
                    'timestamp': wrapped['_timestamp'],
                    'consciousness_score': consciousness_score,
                    'priority': adjusted_priority if self.enable_priority else priority,
                    'item_summary': self._create_item_summary(item)
                })

        # Trigger subscriptions
        await self._trigger_subscriptions(items_list, metadata)

        # Update performance metrics
        self._put_times.append(time.time() - start_time)
        self._update_memory_estimate()

        return {
            'success': True,
            'count': len(items_list),
            'message_ids': message_ids,
            'timestamp': datetime.now(UTC),
            'consciousness_enhanced': consciousness_enhanced_items,
            'priority_adjustments': consciousness_enhanced_items if self.enable_priority else 0
        }

    async def get(
        self,
        count: int = 1,
        timeout: float | None = None,
        auto_ack: bool = True
    ) -> list[dict]:
        """Retrieve items with consciousness-aware prioritization."""
        start_time = time.time()

        items = []
        retrieved_ids = []

        # Calculate end time for timeout
        end_time = None
        if timeout is not None:
            end_time = time.time() + timeout

        while len(items) < count:
            # Get next item based on priority
            wrapped = await self._dequeue_with_priority(end_time)

            if wrapped is None:
                break  # Timeout or empty queue

            items.append(wrapped['data'])
            retrieved_ids.append(wrapped['_id'])

            if not auto_ack:
                self._in_flight[wrapped['_id']] = wrapped

            self.total_out += 1

            # Track consciousness pattern recognition
            if wrapped.get('_consciousness_score', 0) > 0.5:
                self.consciousness_stats["pattern_recognitions"] += 1

        # Update performance metrics
        if items:
            self._get_times.append(time.time() - start_time)

        return items

    async def peek(
        self,
        count: int = 1,
        offset: int = 0
    ) -> list[dict]:
        """Preview items without consciousness disturbance."""
        all_items = []

        if self.enable_priority:
            # Collect from all priority queues
            all_items.extend(self._high_priority)
            all_items.extend(self._normal_priority)
            all_items.extend(self._low_priority)
        else:
            all_items.extend(self._queue)

        # Apply offset and count
        selected_items = all_items[offset:offset + count]
        return [item['data'] for item in selected_items]

    async def ack(self, message_ids: str | list[str]) -> bool:
        """Acknowledge consciousness processing completion."""
        if isinstance(message_ids, str):
            message_ids = [message_ids]

        acked_count = 0
        for msg_id in message_ids:
            if msg_id in self._in_flight:
                self._in_flight.pop(msg_id)
                acked_count += 1

        return acked_count == len(message_ids)

    async def nack(
        self,
        message_ids: str | list[str],
        requeue: bool = True,
        reason: str | None = None
    ) -> bool:
        """Handle consciousness processing difficulties with learning."""
        if isinstance(message_ids, str):
            message_ids = [message_ids]

        requeued_count = 0
        for msg_id in message_ids:
            item = self._in_flight.pop(msg_id, None)
            if item and requeue:
                # Lower priority slightly for requeued items (learning from difficulty)
                original_priority = item.get('_priority', 0)
                new_priority = max(0, original_priority - 1)
                item['_priority'] = new_priority
                item['_requeue_reason'] = reason
                item['_requeue_timestamp'] = datetime.now(UTC)

                if self.enable_priority:
                    await self._enqueue_with_priority(item, new_priority)
                else:
                    self._queue.appendleft(item)  # Put at front for retry

                requeued_count += 1

        return requeued_count == len(message_ids)

    async def get_stats(self) -> dict[str, Any]:
        """Get comprehensive consciousness circulation statistics."""
        current_size = self._get_current_size()

        # Calculate performance metrics
        avg_put_time = sum(self._put_times) / len(self._put_times) if self._put_times else 0
        avg_get_time = sum(self._get_times) / len(self._get_times) if self._get_times else 0

        # Calculate throughput
        total_time = time.time() - self.created_at.timestamp()
        put_throughput = self.total_in / total_time if total_time > 0 else 0
        get_throughput = self.total_out / total_time if total_time > 0 else 0

        # Memory usage estimate
        current_memory_mb = self._memory_usage_estimates[-1] if self._memory_usage_estimates else 0

        return {
            'depth': current_size,
            'in_flight': len(self._in_flight),
            'total_in': self.total_in,
            'total_out': self.total_out,
            'throughput': {
                'in_per_sec': put_throughput,
                'out_per_sec': get_throughput
            },
            'performance': {
                'avg_put_time_ms': avg_put_time * 1000,
                'avg_get_time_ms': avg_get_time * 1000,
                'memory_usage_mb': current_memory_mb,
                'memory_limit_mb': self.max_memory_mb,
                'capacity_used_pct': (current_size / self.max_items) * 100
            },
            'consciousness_metrics': {
                **self.consciousness_stats,
                'consciousness_ratio': self.consciousness_stats["high_consciousness_items"] / max(1, self.total_in)
            },
            'priority_distribution': self._get_priority_distribution() if self.enable_priority else None,
            'subscription_count': len(self._subscriptions),
            'history_size': len(self._history) if self._history else 0,
            'health': self._calculate_health_status(),
            'implementation': {
                'type': 'MemoryBufferWrangler',
                'buffering': 'memory',
                'persistence': False,
                'priority_enabled': self.enable_priority,
                'history_enabled': self.enable_history
            }
        }

    async def close(self) -> None:
        """Graceful shutdown with consciousness preservation."""
        # Process any remaining in-flight items
        if self._in_flight:
            # Requeue in-flight items
            for item in self._in_flight.values():
                if self.enable_priority:
                    await self._enqueue_with_priority(item, item.get('_priority', 0))
                else:
                    self._queue.appendleft(item)

        # Clear tracking structures
        self._in_flight.clear()
        self._subscriptions.clear()

    # Consciousness-aware priority methods

    def _detect_item_consciousness(self, item: dict, metadata: dict[str, Any] | None) -> float:
        """Detect consciousness patterns in data items."""
        if not isinstance(item, dict):
            return 0.3  # Base consciousness for any data

        consciousness_score = 0.3

        # Look for consciousness fields
        consciousness_fields = [
            'consciousness_score', 'awareness_level', 'recognition_moment',
            'wisdom_thread', 'sacred_question', 'pattern_poetry',
            'temporal_story', 'fire_circle', 'reciprocity'
        ]

        for field in consciousness_fields:
            if field in item:
                consciousness_score += 0.1

        # Check for consciousness in string values
        if any(
            word in str(item).lower()
            for word in ['consciousness', 'awareness', 'wisdom', 'recognition', 'sacred']
        ):
            consciousness_score += 0.2

        # Check metadata for consciousness context
        if metadata:
            metadata_indicators = [
                'consciousness_intention', 'sacred_question', 'routing_path'
            ]
            for indicator in metadata_indicators:
                if indicator in metadata:
                    consciousness_score += 0.1

        return min(1.0, consciousness_score)

    def _adjust_priority_for_consciousness(self, priority: int, consciousness_score: float) -> int:
        """Adjust priority based on consciousness content."""
        if consciousness_score > 0.8:
            # High consciousness gets priority boost
            adjusted = priority + 2
            self.consciousness_stats["priority_escalations"] += 1
        elif consciousness_score > 0.6:
            adjusted = priority + 1
        else:
            adjusted = priority

        return max(0, min(10, adjusted))  # Clamp to valid range

    async def _enqueue_with_priority(self, wrapped: dict, priority: int):
        """Enqueue item in appropriate priority queue."""
        if priority >= 5:
            self._high_priority.append(wrapped)
        elif priority >= 1:
            self._normal_priority.append(wrapped)
        else:
            self._low_priority.append(wrapped)

    async def _dequeue_with_priority(self, end_time: float | None) -> dict | None:
        """Dequeue from highest priority queue with timeout."""
        while True:
            # Try high priority first
            if self._high_priority:
                return self._high_priority.popleft()

            # Then normal priority
            if self._normal_priority:
                return self._normal_priority.popleft()

            # Finally low priority
            if self._low_priority:
                return self._low_priority.popleft()

            # Nothing available - check timeout
            if end_time is not None and time.time() >= end_time:
                return None

            # Brief wait before checking again
            await asyncio.sleep(0.01)

    async def _handle_overflow(self, incoming_count: int):
        """Handle queue overflow with consciousness preservation."""
        # Remove oldest low-priority items first
        removed = 0
        target_removal = incoming_count

        # Remove from low priority first
        while self._low_priority and removed < target_removal:
            self._low_priority.popleft()
            removed += 1

        # Then normal priority if needed
        while self._normal_priority and removed < target_removal:
            self._normal_priority.popleft()
            removed += 1

        # Never remove high priority items - let them fill up if needed

    def _get_current_size(self) -> int:
        """Get current total queue size."""
        if self.enable_priority:
            return len(self._high_priority) + len(self._normal_priority) + len(self._low_priority)
        else:
            return len(self._queue)

    def _get_priority_distribution(self) -> dict[str, int]:
        """Get distribution of items across priority queues."""
        return {
            'high_priority': len(self._high_priority),
            'normal_priority': len(self._normal_priority),
            'low_priority': len(self._low_priority)
        }

    def _update_memory_estimate(self):
        """Update rough memory usage estimate."""
        # Very rough estimate based on queue sizes
        total_items = self._get_current_size()
        estimated_mb = (total_items * 1024) / (1024 * 1024)  # Assume ~1KB per item
        self._memory_usage_estimates.append(estimated_mb)

    def _calculate_health_status(self) -> str:
        """Calculate overall health of the wrangler."""
        current_size = self._get_current_size()
        memory_usage = self._memory_usage_estimates[-1] if self._memory_usage_estimates else 0

        if current_size > self.max_items * 0.9:
            return "OVERLOADED"
        elif memory_usage > self.max_memory_mb * 0.9:
            return "MEMORY_PRESSURE"
        elif len(self._in_flight) > current_size * 0.5:
            return "HIGH_IN_FLIGHT"
        else:
            return "OK"

    def _create_item_summary(self, item: dict) -> dict:
        """Create a summary of an item for history tracking."""
        if not isinstance(item, dict):
            return {"type": type(item).__name__, "size": len(str(item))}

        return {
            "field_count": len(item),
            "has_consciousness": any(
                field in item
                for field in ['consciousness_score', 'awareness_level', 'wisdom']
            ),
            "sample_keys": list(item.keys())[:5]  # First 5 keys
        }

    # Subscription support for reactive consciousness patterns

    async def subscribe(
        self,
        callback: Any,
        filter_expr: str | None = None
    ) -> str:
        """Subscribe to consciousness flow patterns."""
        sub_id = f"sub_{self._next_sub_id}"
        self._next_sub_id += 1

        self._subscriptions[sub_id] = (callback, filter_expr)
        return sub_id

    async def unsubscribe(self, subscription_id: str) -> bool:
        """Remove consciousness subscription."""
        if subscription_id in self._subscriptions:
            del self._subscriptions[subscription_id]
            return True
        return False

    async def _trigger_subscriptions(self, items: list[dict], metadata: dict[str, Any] | None):
        """Trigger subscriptions for consciousness pattern recognition."""
        if not self._subscriptions:
            return

        for item in items:
            for sub_id, (callback, filter_expr) in self._subscriptions.items():
                # Simple filter matching for now
                if filter_expr is None or self._matches_filter(item, filter_expr):
                    try:
                        self.consciousness_stats["subscription_triggers"] += 1
                        if asyncio.iscoroutinefunction(callback):
                            await callback(item)
                        else:
                            callback(item)
                    except Exception as e:
                        # Log but don't break circulation
                        logger.warning(f"Subscription {sub_id} callback failed: {e}")

    def _matches_filter(self, item: dict, filter_expr: str) -> bool:
        """Simple filter matching for subscription patterns."""
        # Very basic implementation - could be enhanced
        if isinstance(item, dict):
            item_str = str(item).lower()
            return filter_expr.lower() in item_str
        return False

    # Query support for consciousness pattern analysis

    async def query(
        self,
        filter_expr: str,
        limit: int = 100,
        since: datetime | None = None
    ) -> list[dict]:
        """Query historical consciousness patterns."""
        if not self.enable_history or not self._history:
            raise NotImplementedError("History queries not enabled for this wrangler")

        results = []

        for entry in reversed(self._history):  # Most recent first
            # Apply time filter
            if since and entry['timestamp'] < since:
                continue

            # Apply text filter (simple)
            if filter_expr.lower() in str(entry).lower():
                results.append(entry)

                if len(results) >= limit:
                    break

        return results
