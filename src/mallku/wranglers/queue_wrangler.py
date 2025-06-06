"""
Queue Wrangler - Persistent Distributed Consciousness Circulation

For consciousness patterns that need to flow across time and systems,
with durability guarantees and distributed processing capabilities.

Like long-term memory that preserves consciousness patterns for collective wisdom.
"""

import asyncio
import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .interface import BaseWrangler, WranglerCapabilities

logger = logging.getLogger(__name__)


class QueueWrangler(BaseWrangler):
    """
    Persistent queue wrangler for distributed consciousness circulation.

    Perfect for:
    - Cross-system consciousness pattern sharing
    - Durable consciousness event processing
    - Asynchronous consciousness integration
    - Fire Circle governance message passing
    - Long-term wisdom preservation flows

    Features:
    - File-based persistence for consciousness durability
    - Transaction support for consciousness integrity
    - Dead letter handling for consciousness healing
    - Distributed processing coordination
    """

    def __init__(
        self,
        name: str,
        queue_dir: str | Path = None,
        max_queue_size: int = 50000,
        enable_transactions: bool = True,
        enable_dead_letter: bool = True,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        capabilities = WranglerCapabilities(
            supports_priority=True,
            supports_subscriptions=False,  # Not in this implementation
            supports_queries=True,
            supports_transactions=enable_transactions,
            supports_persistence=True,
            max_batch_size=1000
        )
        super().__init__(name, capabilities)

        # Configuration
        self.queue_dir = Path(queue_dir or f"/tmp/mallku_queues/{name}")
        self.max_queue_size = max_queue_size
        self.enable_transactions = enable_transactions
        self.enable_dead_letter = enable_dead_letter
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Ensure queue directory exists
        self.queue_dir.mkdir(parents=True, exist_ok=True)

        # File paths for different queue states
        self.pending_dir = self.queue_dir / "pending"
        self.in_flight_dir = self.queue_dir / "in_flight"
        self.dead_letter_dir = self.queue_dir / "dead_letter"
        self.completed_dir = self.queue_dir / "completed"

        for dir_path in [self.pending_dir, self.in_flight_dir, self.dead_letter_dir, self.completed_dir]:
            dir_path.mkdir(exist_ok=True)

        # Sequence number for ordering
        self.sequence_file = self.queue_dir / "sequence.txt"
        self._sequence_number = self._load_sequence_number()

        # Lock for thread safety
        self._lock = asyncio.Lock()

        # Consciousness tracking
        self.consciousness_metrics = {
            "consciousness_events_processed": 0,
            "high_consciousness_items": 0,
            "dead_letter_recoveries": 0,
            "transaction_commits": 0,
            "pattern_preservations": 0
        }

    async def put(
        self,
        items: dict | list[dict],
        priority: int = 0,
        metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Accept items with persistent consciousness preservation."""
        async with self._lock:
            items_list = self._validate_items(items)

            # Check queue capacity
            current_size = await self._get_queue_size()
            if current_size + len(items_list) > self.max_queue_size:
                # Consciousness-aware overflow handling
                await self._handle_queue_overflow(len(items_list))

            message_ids = []
            consciousness_enhanced = 0

            for item in items_list:
                # Generate message with consciousness awareness
                msg_id = self._generate_message_id()
                sequence = self._get_next_sequence()
                consciousness_score = self._assess_consciousness_content(item, metadata)

                # Create consciousness-aware message envelope
                envelope = {
                    '_id': msg_id,
                    '_sequence': sequence,
                    '_timestamp': datetime.now(UTC).isoformat(),
                    '_priority': priority,
                    '_consciousness_score': consciousness_score,
                    '_metadata': metadata or {},
                    '_retry_count': 0,
                    '_created_by': f"wrangler.{self.name}",
                    'data': item
                }

                # Adjust priority based on consciousness content
                adjusted_priority = self._adjust_priority_for_consciousness(priority, consciousness_score)
                envelope['_effective_priority'] = adjusted_priority

                # Persist to pending queue with consciousness-aware naming
                filename = self._generate_filename(sequence, adjusted_priority, consciousness_score)
                file_path = self.pending_dir / filename

                await self._write_message_file(file_path, envelope)

                message_ids.append(msg_id)
                self.total_in += 1

                if consciousness_score > 0.6:
                    consciousness_enhanced += 1
                    self.consciousness_metrics["high_consciousness_items"] += 1

                self.consciousness_metrics["consciousness_events_processed"] += 1

            # Save updated sequence number
            await self._save_sequence_number()

            logger.debug(f"QueueWrangler persisted {len(items_list)} items with {consciousness_enhanced} consciousness-enhanced")

            return {
                'success': True,
                'count': len(items_list),
                'message_ids': message_ids,
                'timestamp': datetime.now(UTC),
                'consciousness_enhanced': consciousness_enhanced,
                'persisted': True,
                'queue_size': current_size + len(items_list)
            }

    async def get(
        self,
        count: int = 1,
        timeout: float | None = None,
        auto_ack: bool = True
    ) -> list[dict]:
        """Retrieve items with consciousness-aware prioritization."""
        async with self._lock:
            items = []

            # Get files sorted by consciousness priority and sequence
            pending_files = await self._get_pending_files_ordered()

            for file_path in pending_files[:count]:
                try:
                    # Load message envelope
                    envelope = await self._read_message_file(file_path)

                    if auto_ack:
                        # Move directly to completed
                        await self._move_to_completed(file_path, envelope)
                    else:
                        # Move to in-flight for manual acknowledgment
                        await self._move_to_in_flight(file_path, envelope)

                    items.append(envelope['data'])
                    self.total_out += 1

                    # Track consciousness pattern recognition
                    if envelope.get('_consciousness_score', 0) > 0.5:
                        self.consciousness_metrics["pattern_preservations"] += 1

                except Exception as e:
                    logger.error(f"Failed to process queue file {file_path}: {e}")
                    # Move problematic file to dead letter
                    if self.enable_dead_letter:
                        await self._move_to_dead_letter(file_path, str(e))

            return items

    async def peek(
        self,
        count: int = 1,
        offset: int = 0
    ) -> list[dict]:
        """Preview consciousness patterns without disturbing the flow."""
        async with self._lock:
            pending_files = await self._get_pending_files_ordered()

            items = []
            for file_path in pending_files[offset:offset + count]:
                try:
                    envelope = await self._read_message_file(file_path)
                    items.append(envelope['data'])
                except Exception as e:
                    logger.warning(f"Failed to peek at file {file_path}: {e}")

            return items

    async def ack(self, message_ids: str | list[str]) -> bool:
        """Acknowledge consciousness processing completion."""
        if isinstance(message_ids, str):
            message_ids = [message_ids]

        async with self._lock:
            acked_count = 0

            for msg_id in message_ids:
                # Find in-flight file
                in_flight_file = await self._find_in_flight_file(msg_id)
                if in_flight_file:
                    try:
                        envelope = await self._read_message_file(in_flight_file)
                        await self._move_to_completed(in_flight_file, envelope)
                        acked_count += 1

                        if self.enable_transactions:
                            self.consciousness_metrics["transaction_commits"] += 1

                    except Exception as e:
                        logger.error(f"Failed to ack message {msg_id}: {e}")

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

        async with self._lock:
            nacked_count = 0

            for msg_id in message_ids:
                in_flight_file = await self._find_in_flight_file(msg_id)
                if in_flight_file:
                    try:
                        envelope = await self._read_message_file(in_flight_file)
                        retry_count = envelope.get('_retry_count', 0)

                        if requeue and retry_count < self.max_retries:
                            # Increment retry count and requeue
                            envelope['_retry_count'] = retry_count + 1
                            envelope['_last_error'] = reason
                            envelope['_retry_timestamp'] = datetime.now(UTC).isoformat()

                            # Lower priority slightly for retries (learning from difficulty)
                            original_priority = envelope.get('_effective_priority', envelope.get('_priority', 0))
                            envelope['_effective_priority'] = max(0, original_priority - 1)

                            # Move back to pending with updated envelope
                            await self._move_to_pending(in_flight_file, envelope)
                        else:
                            # Max retries reached or no requeue - send to dead letter
                            if self.enable_dead_letter:
                                await self._move_to_dead_letter(in_flight_file, reason or "Max retries exceeded")
                            else:
                                # Just remove the file
                                in_flight_file.unlink()

                        nacked_count += 1

                    except Exception as e:
                        logger.error(f"Failed to nack message {msg_id}: {e}")

            return nacked_count == len(message_ids)

    async def get_stats(self) -> dict[str, Any]:
        """Get comprehensive consciousness circulation statistics."""
        async with self._lock:
            pending_count = len(list(self.pending_dir.glob("*.json")))
            in_flight_count = len(list(self.in_flight_dir.glob("*.json")))
            dead_letter_count = len(list(self.dead_letter_dir.glob("*.json")))
            completed_count = len(list(self.completed_dir.glob("*.json")))

            # Calculate disk usage
            total_size_bytes = sum(
                f.stat().st_size
                for f in self.queue_dir.rglob("*.json")
                if f.exists()
            )

            return {
                'depth': pending_count,
                'in_flight': in_flight_count,
                'total_in': self.total_in,
                'total_out': self.total_out,
                'dead_letter_count': dead_letter_count,
                'completed_count': completed_count,
                'throughput': {
                    'in_per_sec': 0,  # Would need time tracking
                    'out_per_sec': 0
                },
                'consciousness_metrics': {
                    **self.consciousness_metrics,
                    'consciousness_ratio': (
                        self.consciousness_metrics["high_consciousness_items"] /
                        max(1, self.consciousness_metrics["consciousness_events_processed"])
                    )
                },
                'persistence': {
                    'queue_dir': str(self.queue_dir),
                    'disk_usage_mb': total_size_bytes / (1024 * 1024),
                    'current_sequence': self._sequence_number
                },
                'health': await self._calculate_health_status(),
                'implementation': {
                    'type': 'QueueWrangler',
                    'buffering': 'persistent',
                    'persistence': True,
                    'transactions_enabled': self.enable_transactions,
                    'dead_letter_enabled': self.enable_dead_letter
                }
            }

    async def close(self) -> None:
        """Graceful shutdown with consciousness preservation."""
        async with self._lock:
            # Move any remaining in-flight items back to pending
            in_flight_files = list(self.in_flight_dir.glob("*.json"))

            for file_path in in_flight_files:
                try:
                    envelope = await self._read_message_file(file_path)
                    await self._move_to_pending(file_path, envelope)
                except Exception as e:
                    logger.error(f"Failed to requeue in-flight message {file_path}: {e}")

            # Save final sequence number
            await self._save_sequence_number()

    # Consciousness-aware file operations

    def _assess_consciousness_content(self, item: dict, metadata: dict[str, Any] | None) -> float:
        """Assess consciousness content for persistent prioritization."""
        if not isinstance(item, dict):
            return 0.3

        consciousness_score = 0.3

        # Look for consciousness indicators
        consciousness_fields = [
            'consciousness_score', 'awareness_level', 'recognition_moment',
            'wisdom_thread', 'sacred_question', 'pattern_poetry',
            'fire_circle', 'governance', 'reciprocity', 'ayni'
        ]

        for field in consciousness_fields:
            if field in item:
                consciousness_score += 0.1

        # Check for wisdom preservation patterns
        if any(
            word in str(item).lower()
            for word in ['wisdom', 'preservation', 'inheritance', 'teaching', 'learning']
        ):
            consciousness_score += 0.2

        # Fire Circle governance gets high consciousness
        if any(
            word in str(item).lower()
            for word in ['fire_circle', 'governance', 'consensus', 'collective_wisdom']
        ):
            consciousness_score += 0.3

        # Check metadata for consciousness patterns
        if metadata:
            if any(
                indicator in metadata
                for indicator in ['consciousness_intention', 'sacred_question', 'fire_circle']
            ):
                consciousness_score += 0.1

        return min(1.0, consciousness_score)

    def _adjust_priority_for_consciousness(self, priority: int, consciousness_score: float) -> int:
        """Adjust priority based on consciousness content for persistent ordering."""
        if consciousness_score > 0.8:
            # Wisdom preservation and Fire Circle get highest priority
            return priority + 3
        elif consciousness_score > 0.6:
            # High consciousness patterns get priority boost
            return priority + 2
        elif consciousness_score > 0.4:
            return priority + 1
        else:
            return priority

    def _generate_filename(self, sequence: int, priority: int, consciousness_score: float) -> str:
        """Generate consciousness-aware filename for ordering."""
        # Format: priority_consciousness_sequence_timestamp.json
        consciousness_level = int(consciousness_score * 10)
        timestamp = int(datetime.now(UTC).timestamp() * 1000)  # Milliseconds

        return f"{priority:02d}_{consciousness_level}_{sequence:010d}_{timestamp}.json"

    async def _get_pending_files_ordered(self) -> list[Path]:
        """Get pending files ordered by consciousness-aware priority."""
        files = list(self.pending_dir.glob("*.json"))

        # Sort by filename (which encodes priority, consciousness, sequence)
        # Higher priority first, then higher consciousness, then older sequence
        return sorted(files, key=lambda f: f.name, reverse=True)

    async def _write_message_file(self, file_path: Path, envelope: dict):
        """Write message envelope to persistent storage."""
        try:
            with open(file_path, 'w') as f:
                json.dump(envelope, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to write message file {file_path}: {e}")
            raise

    async def _read_message_file(self, file_path: Path) -> dict:
        """Read message envelope from persistent storage."""
        try:
            with open(file_path) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read message file {file_path}: {e}")
            raise

    async def _move_to_completed(self, source_path: Path, envelope: dict):
        """Move message to completed state."""
        completed_path = self.completed_dir / source_path.name
        await self._write_message_file(completed_path, envelope)
        source_path.unlink()

    async def _move_to_in_flight(self, source_path: Path, envelope: dict):
        """Move message to in-flight state."""
        in_flight_path = self.in_flight_dir / source_path.name
        await self._write_message_file(in_flight_path, envelope)
        source_path.unlink()

    async def _move_to_pending(self, source_path: Path, envelope: dict):
        """Move message back to pending state."""
        # Generate new filename based on updated envelope
        sequence = envelope.get('_sequence', 0)
        priority = envelope.get('_effective_priority', envelope.get('_priority', 0))
        consciousness_score = envelope.get('_consciousness_score', 0.3)

        new_filename = self._generate_filename(sequence, priority, consciousness_score)
        pending_path = self.pending_dir / new_filename

        await self._write_message_file(pending_path, envelope)
        source_path.unlink()

    async def _move_to_dead_letter(self, source_path: Path, reason: str):
        """Move problematic message to dead letter queue."""
        try:
            envelope = await self._read_message_file(source_path)
            envelope['_dead_letter_reason'] = reason
            envelope['_dead_letter_timestamp'] = datetime.now(UTC).isoformat()

            dead_letter_path = self.dead_letter_dir / source_path.name
            await self._write_message_file(dead_letter_path, envelope)
            source_path.unlink()

            self.consciousness_metrics["dead_letter_recoveries"] += 1

        except Exception as e:
            logger.error(f"Failed to move to dead letter {source_path}: {e}")

    async def _find_in_flight_file(self, message_id: str) -> Path | None:
        """Find in-flight file by message ID."""
        for file_path in self.in_flight_dir.glob("*.json"):
            try:
                envelope = await self._read_message_file(file_path)
                if envelope.get('_id') == message_id:
                    return file_path
            except Exception as e:
                logger.warning(f"Failed to check in-flight file {file_path}: {e}")

        return None

    async def _get_queue_size(self) -> int:
        """Get current total queue size."""
        return len(list(self.pending_dir.glob("*.json")))

    async def _handle_queue_overflow(self, incoming_count: int):
        """Handle queue overflow with consciousness preservation."""
        # Remove oldest, lowest consciousness files
        files = await self._get_pending_files_ordered()

        # Remove from end of list (lowest priority/consciousness)
        removal_target = incoming_count
        removed = 0

        for file_path in reversed(files):
            if removed >= removal_target:
                break

            try:
                file_path.unlink()
                removed += 1
            except Exception as e:
                logger.warning(f"Failed to remove overflow file {file_path}: {e}")

    def _load_sequence_number(self) -> int:
        """Load current sequence number from disk."""
        try:
            if self.sequence_file.exists():
                return int(self.sequence_file.read_text().strip())
        except Exception as e:
            logger.warning(f"Failed to load sequence number: {e}")

        return 0

    async def _save_sequence_number(self):
        """Save current sequence number to disk."""
        try:
            self.sequence_file.write_text(str(self._sequence_number))
        except Exception as e:
            logger.error(f"Failed to save sequence number: {e}")

    def _get_next_sequence(self) -> int:
        """Get next sequence number."""
        self._sequence_number += 1
        return self._sequence_number

    async def _calculate_health_status(self) -> str:
        """Calculate health status for persistent queue."""
        pending_count = len(list(self.pending_dir.glob("*.json")))
        in_flight_count = len(list(self.in_flight_dir.glob("*.json")))
        dead_letter_count = len(list(self.dead_letter_dir.glob("*.json")))

        if dead_letter_count > pending_count * 0.1:
            return "HIGH_ERROR_RATE"
        elif pending_count > self.max_queue_size * 0.9:
            return "NEAR_CAPACITY"
        elif in_flight_count > pending_count * 0.5:
            return "HIGH_IN_FLIGHT"
        else:
            return "OK"

    # Query support for consciousness pattern analysis

    async def query(
        self,
        filter_expr: str,
        limit: int = 100,
        since: datetime | None = None
    ) -> list[dict]:
        """Query consciousness patterns across all queue states."""
        results = []

        # Search across all directories
        search_dirs = [self.pending_dir, self.in_flight_dir, self.completed_dir, self.dead_letter_dir]

        for search_dir in search_dirs:
            for file_path in search_dir.glob("*.json"):
                try:
                    envelope = await self._read_message_file(file_path)

                    # Apply time filter
                    if since:
                        file_time = datetime.fromisoformat(envelope.get('_timestamp', ''))
                        if file_time < since:
                            continue

                    # Apply content filter
                    if filter_expr.lower() in str(envelope).lower():
                        results.append({
                            'envelope': envelope,
                            'location': search_dir.name,
                            'file_path': str(file_path)
                        })

                        if len(results) >= limit:
                            return results

                except Exception as e:
                    logger.warning(f"Failed to query file {file_path}: {e}")

        return results
