"""
Correlation to Memory Anchor Adapter

Transforms detected temporal correlations into persistent memory anchors,
bridging the gap between pattern detection and contextual storage.
"""

import logging
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from mallku.correlation.models import TemporalCorrelation
from mallku.models.memory_anchor import MemoryAnchor
from mallku.services.memory_anchor_service import MemoryAnchorService

logger = logging.getLogger(__name__)


class CorrelationToAnchorAdapter:
    """
    Adapter that converts temporal correlations into memory anchors.

    This component serves as the crucial bridge between correlation detection
    and persistent storage, transforming patterns into queryable context.
    """

    def __init__(
        self,
        memory_service: MemoryAnchorService,
        confidence_threshold: float = 0.7,
        batch_size: int = 10
    ):
        """
        Initialize the correlation adapter.

        Args:
            memory_service: Memory Anchor Service for persistence
            confidence_threshold: Minimum confidence to create anchors
            batch_size: Number of correlations to batch for efficiency
        """
        self.memory_service = memory_service
        self.confidence_threshold = confidence_threshold
        self.batch_size = batch_size

        # Statistics
        self.stats = {
            'correlations_processed': 0,
            'anchors_created': 0,
            'anchors_rejected_confidence': 0,
            'anchors_rejected_error': 0,
            'processing_times': [],
            'last_batch_time': None
        }

        # Batch processing
        self.pending_correlations: list[TemporalCorrelation] = []

    async def process_correlation(self, correlation: TemporalCorrelation) -> MemoryAnchor | None:
        """
        Process a single correlation and potentially create a memory anchor.

        Args:
            correlation: Detected temporal correlation

        Returns:
            Created memory anchor or None if not created
        """
        start_time = datetime.now(UTC)

        try:
            self.stats['correlations_processed'] += 1

            # Check confidence threshold
            if correlation.confidence_score < self.confidence_threshold:
                self.stats['anchors_rejected_confidence'] += 1
                logger.debug(
                    f"Correlation {correlation.correlation_id} rejected: "
                    f"confidence {correlation.confidence_score:.3f} < {self.confidence_threshold}"
                )
                return None

            # Create memory anchor from correlation
            anchor = await self._create_memory_anchor(correlation)

            if anchor:
                self.stats['anchors_created'] += 1
                logger.info(
                    f"Created memory anchor {anchor.anchor_id} from correlation "
                    f"with confidence {correlation.confidence_score:.3f}"
                )

            return anchor

        except Exception as e:
            self.stats['anchors_rejected_error'] += 1
            logger.error(f"Error processing correlation {correlation.correlation_id}: {e}")
            return None

        finally:
            processing_time = (datetime.now(UTC) - start_time).total_seconds() * 1000
            self.stats['processing_times'].append(processing_time)

            # Keep only recent processing times for performance metrics
            if len(self.stats['processing_times']) > 1000:
                self.stats['processing_times'] = self.stats['processing_times'][-500:]

    async def process_correlation_batch(self, correlations: list[TemporalCorrelation]) -> list[MemoryAnchor]:
        """
        Process a batch of correlations for improved efficiency.

        Args:
            correlations: List of correlations to process

        Returns:
            List of created memory anchors
        """
        batch_start = datetime.now(UTC)
        created_anchors = []

        logger.info(f"Processing batch of {len(correlations)} correlations")

        for correlation in correlations:
            anchor = await self.process_correlation(correlation)
            if anchor:
                created_anchors.append(anchor)

        batch_time = (datetime.now(UTC) - batch_start).total_seconds()
        self.stats['last_batch_time'] = batch_time

        logger.info(
            f"Batch processing complete: {len(created_anchors)} anchors created "
            f"from {len(correlations)} correlations in {batch_time:.2f}s"
        )

        return created_anchors

    async def _create_memory_anchor(self, correlation: TemporalCorrelation) -> MemoryAnchor | None:
        """Create a memory anchor from a temporal correlation."""

        try:
            # Extract primary event information
            primary_event = correlation.primary_event

            # Build cursors from correlated events
            cursors = self._build_cursors_from_correlation(correlation)

            # Create temporal window
            temporal_window = {
                'start_time': correlation.temporal_window_start,
                'end_time': correlation.temporal_window_end,
                'precision': correlation.temporal_precision.value,
                'gap': correlation.temporal_gap.total_seconds()
            }

            # Build correlation metadata
            correlation_metadata = {
                'pattern_type': correlation.pattern_type,
                'confidence_score': correlation.confidence_score,
                'occurrence_frequency': correlation.occurrence_frequency,
                'pattern_stability': correlation.pattern_stability,
                'confidence_factors': correlation.confidence_factors
            }

            # Create memory anchor
            anchor = MemoryAnchor(
                anchor_id=uuid4(),
                cursors=cursors,
                temporal_window=temporal_window,
                metadata={
                    'correlation_id': str(correlation.correlation_id),
                    'correlation_metadata': correlation_metadata,
                    'primary_event': {
                        'event_id': str(primary_event.event_id),
                        'timestamp': primary_event.timestamp.isoformat(),
                        'event_type': primary_event.event_type.value,
                        'stream_id': primary_event.stream_id,
                        'correlation_tags': primary_event.correlation_tags
                    },
                    'created_by': 'correlation_adapter',
                    'creation_method': 'temporal_correlation'
                },
                confidence_score=correlation.confidence_score,
                created_at=datetime.now(UTC),
                last_accessed=datetime.now(UTC)
            )

            # Store anchor using memory service
            stored_anchor = await self.memory_service.create_memory_anchor(anchor)

            return stored_anchor

        except Exception as e:
            logger.error(f"Failed to create memory anchor from correlation: {e}")
            return None

    def _build_cursors_from_correlation(self, correlation: TemporalCorrelation) -> list[dict[str, Any]]:
        """Build cursors from correlation events."""
        cursors = []

        # Add cursor for primary event
        primary_cursor = self._create_cursor_from_event(correlation.primary_event, 'primary')
        cursors.append(primary_cursor)

        # Add cursors for correlated events
        for i, event in enumerate(correlation.correlated_events):
            cursor = self._create_cursor_from_event(event, f'correlated_{i}')
            cursors.append(cursor)

        return cursors

    def _create_cursor_from_event(self, event: Any, role: str) -> dict[str, Any]:
        """Create a cursor from an event."""

        cursor = {
            'role': role,
            'event_id': str(event.event_id),
            'timestamp': event.timestamp.isoformat(),
            'event_type': event.event_type.value,
            'stream_id': event.stream_id,
            'content_summary': self._summarize_event_content(event),
            'correlation_tags': event.correlation_tags
        }

        # Add content-specific cursor information
        if hasattr(event, 'content') and event.content:
            if 'file_path' in event.content:
                cursor['file_path'] = event.content['file_path']
                cursor['cursor_type'] = 'file_reference'
            elif 'operation' in event.content:
                cursor['operation'] = event.content['operation']
                cursor['cursor_type'] = 'activity_reference'
            else:
                cursor['cursor_type'] = 'event_reference'

        return cursor

    def _summarize_event_content(self, event: Any) -> str:
        """Create a brief summary of event content for the cursor."""

        if not hasattr(event, 'content') or not event.content:
            return f"{event.event_type.value} event"

        content = event.content

        # File-related events
        if 'file_name' in content:
            operation = content.get('operation', 'unknown')
            return f"{operation} {content['file_name']}"

        # Activity events
        if 'operation' in content:
            return f"{content['operation']} operation"

        # Generic event
        return f"{event.event_type.value} event at {event.timestamp.strftime('%H:%M:%S')}"

    def get_statistics(self) -> dict[str, Any]:
        """Get adapter processing statistics."""
        stats = self.stats.copy()

        # Calculate derived metrics
        if stats['processing_times']:
            stats['avg_processing_time_ms'] = sum(stats['processing_times']) / len(stats['processing_times'])
            stats['max_processing_time_ms'] = max(stats['processing_times'])
            stats['min_processing_time_ms'] = min(stats['processing_times'])
        else:
            stats['avg_processing_time_ms'] = 0
            stats['max_processing_time_ms'] = 0
            stats['min_processing_time_ms'] = 0

        # Calculate success rate
        total_processed = stats['correlations_processed']
        if total_processed > 0:
            stats['anchor_creation_rate'] = stats['anchors_created'] / total_processed
            stats['confidence_rejection_rate'] = stats['anchors_rejected_confidence'] / total_processed
            stats['error_rate'] = stats['anchors_rejected_error'] / total_processed
        else:
            stats['anchor_creation_rate'] = 0
            stats['confidence_rejection_rate'] = 0
            stats['error_rate'] = 0

        return stats

    def reset_statistics(self) -> None:
        """Reset adapter statistics."""
        self.stats = {
            'correlations_processed': 0,
            'anchors_created': 0,
            'anchors_rejected_confidence': 0,
            'anchors_rejected_error': 0,
            'processing_times': [],
            'last_batch_time': None
        }
