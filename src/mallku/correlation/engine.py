"""
Main Correlation Engine - Orchestrator of Temporal Intelligence.

This module implements the central CorrelationEngine that coordinates all
components of temporal correlation detection: pattern recognition, confidence
scoring, adaptive learning, and memory anchor generation. It transforms
streams of events into meaningful memory anchors through sophisticated
temporal analysis.
"""

import asyncio
import logging
from collections import deque
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from ..core.database import get_database
from ..models import MemoryAnchor
from ..services.memory_anchor_service import MemoryAnchorService
from .models import (
    CorrelationFeedback,
    CorrelationWindow,
    Event,
    TemporalCorrelation,
    TemporalPrecision,
)
from .patterns import ConcurrentPattern, ContextualPattern, CyclicalPattern, SequentialPattern
from .scoring import ConfidenceScorer
from .thresholds import AdaptiveThresholds


class CorrelationEngine:
    """
    Central orchestrator for temporal correlation detection and memory anchor generation.

    The CorrelationEngine embodies the architect's vision of intelligence that watches
    the flow of human activity and recognizes meaningful patterns. It coordinates
    multiple detection algorithms, learns from experience, and generates memory
    anchors that capture the temporal relationships between disparate activities.
    """

    def __init__(
        self,
        memory_anchor_service: MemoryAnchorService | None = None,
        window_size: timedelta = timedelta(hours=2),
        window_overlap: float = 0.3
    ):
        """
        Initialize the correlation engine.

        Args:
            memory_anchor_service: Service for creating memory anchors
            window_size: Default size for correlation windows
            window_overlap: Overlap factor between adjacent windows
        """
        # Core components
        self.memory_service = memory_anchor_service
        self.confidence_scorer = ConfidenceScorer()
        self.adaptive_thresholds = AdaptiveThresholds()

        # Pattern detectors for the four correlation types
        self.pattern_detectors = {
            'sequential': SequentialPattern(),
            'concurrent': ConcurrentPattern(),
            'cyclical': CyclicalPattern(),
            'contextual': ContextualPattern()
        }

        # Sliding window configuration
        self.window_size = window_size
        self.window_overlap = window_overlap

        # Event processing
        self.event_buffer: deque[Event] = deque(maxlen=10000)  # Ring buffer for events
        self.active_windows: list[CorrelationWindow] = []
        self.processing_lock = asyncio.Lock()

        # Performance tracking
        self.correlation_stats = {
            'total_correlations_detected': 0,
            'correlations_accepted': 0,
            'correlations_rejected': 0,
            'memory_anchors_created': 0,
            'last_processing_time': None
        }

        # Learning and feedback
        self.feedback_queue: list[CorrelationFeedback] = []
        self.learning_batch_size = 50

        # Set up logging
        self.logger = logging.getLogger(__name__)

    async def initialize(self):
        """Initialize the correlation engine and its components."""
        self.logger.info("Initializing Correlation Engine...")

        # Initialize memory anchor service if not provided
        if self.memory_service is None:
            self.memory_service = MemoryAnchorService()
            await self.memory_service.initialize()

        # Load saved configuration and learning data
        performance_summary = self.adaptive_thresholds.get_performance_summary()
        self.logger.info(f"Loaded adaptive thresholds: {performance_summary}")

        self.logger.info("Correlation Engine initialized successfully")

    async def process_event_stream(self, events: list[Event]) -> list[TemporalCorrelation]:
        """
        Process a stream of events to detect temporal correlations.

        This is the main entry point for correlation detection. Events are
        added to sliding windows, patterns are detected, confidence is scored,
        and high-quality correlations are converted to memory anchors.

        Args:
            events: List of events to process

        Returns:
            List of detected correlations
        """
        async with self.processing_lock:
            start_time = datetime.now(UTC)

            # Add events to buffer
            for event in events:
                self.event_buffer.append(event)

            # Update sliding windows with new events
            await self._update_sliding_windows(events)

            # Detect correlations in all active windows
            all_correlations = []
            for window in self.active_windows:
                window_correlations = await self._process_window(window)
                all_correlations.extend(window_correlations)

            # Score and filter correlations
            accepted_correlations = []
            for correlation in all_correlations:
                # Calculate confidence score
                confidence = self.confidence_scorer.calculate_correlation_confidence(correlation)
                correlation.confidence_score = confidence

                # Apply adaptive thresholds
                if self.adaptive_thresholds.should_accept_correlation(
                    confidence,
                    correlation.occurrence_frequency,
                    correlation.pattern_type
                ):
                    accepted_correlations.append(correlation)
                    self.correlation_stats['correlations_accepted'] += 1

                    # Generate memory anchor for high-confidence correlations
                    await self._create_memory_anchor(correlation)
                else:
                    self.correlation_stats['correlations_rejected'] += 1

            # Update statistics
            self.correlation_stats['total_correlations_detected'] += len(all_correlations)
            self.correlation_stats['last_processing_time'] = datetime.now(UTC)

            processing_duration = datetime.now(UTC) - start_time
            self.logger.info(
                f"Processed {len(events)} events in {processing_duration.total_seconds():.2f}s, "
                f"detected {len(all_correlations)} correlations, "
                f"accepted {len(accepted_correlations)}"
            )

            return accepted_correlations

    async def _update_sliding_windows(self, new_events: list[Event]):
        """
        Update sliding windows with new events.

        Creates new windows as needed and removes old windows that have
        moved beyond the processing horizon.
        """
        if not new_events:
            return

        # Sort events by timestamp
        new_events.sort(key=lambda e: e.timestamp)

        current_time = new_events[-1].timestamp

        # Remove old windows that are no longer relevant
        self.active_windows = [
            window for window in self.active_windows
            if current_time - window.start_time < self.window_size * 2
        ]

        # Create new windows if needed
        if not self.active_windows:
            # Create first window
            await self._create_window(current_time - self.window_size, current_time)
        else:
            # Check if we need additional windows
            latest_window = max(self.active_windows, key=lambda w: w.end_time)

            # Create overlapping windows as time progresses
            while latest_window.end_time < current_time:
                overlap_duration = self.window_size * self.window_overlap
                new_start = latest_window.start_time + (self.window_size - overlap_duration)
                new_end = new_start + self.window_size

                latest_window = await self._create_window(new_start, new_end)

        # Add new events to appropriate windows
        for event in new_events:
            for window in self.active_windows:
                window.add_event(event)

    async def _create_window(self, start_time: datetime, end_time: datetime) -> CorrelationWindow:
        """Create a new correlation window."""
        window = CorrelationWindow(
            start_time=start_time,
            end_time=end_time,
            precision=TemporalPrecision.SESSION,  # Default precision
            overlap_factor=self.window_overlap
        )

        self.active_windows.append(window)
        return window

    async def _process_window(self, window: CorrelationWindow) -> list[TemporalCorrelation]:
        """
        Process a single correlation window to detect patterns.

        Args:
            window: Window to process

        Returns:
            List of correlations detected in this window
        """
        if window.event_count < 2:
            return []  # Need at least 2 events for correlation

        all_correlations = []

        # Apply each pattern detector to the window's events
        for pattern_name, detector in self.pattern_detectors.items():
            try:
                patterns = detector.detect_patterns(window.events)
                all_correlations.extend(patterns)

                self.logger.debug(
                    f"Window {window.window_id}: {pattern_name} detector found {len(patterns)} patterns"
                )

            except Exception as e:
                self.logger.error(f"Error in {pattern_name} pattern detection: {e}")

        # Store correlations in window for tracking
        window.detected_correlations = all_correlations

        return all_correlations

    async def _create_memory_anchor(self, correlation: TemporalCorrelation) -> MemoryAnchor | None:
        """
        Create a memory anchor from a high-confidence correlation.

        This is where temporal correlations transform into persistent
        memory anchors that can be used for context reconstruction
        and cross-source search.

        Args:
            correlation: Correlation to convert to memory anchor

        Returns:
            Created memory anchor or None if creation failed
        """
        try:
            # Extract relevant information for memory anchor
            all_events = [correlation.primary_event] + correlation.correlated_events

            # Determine anchor timestamp (use primary event)
            anchor_timestamp = correlation.primary_event.timestamp

            # Create cursor state from correlated events
            cursors = {}
            for event in all_events:
                cursor_key = f"{event.event_type}:{event.stream_id}"
                cursors[cursor_key] = {
                    'timestamp': event.timestamp.isoformat(),
                    'content': event.content
                }

            # Create metadata with correlation information
            metadata = {
                'correlation_id': str(correlation.correlation_id),
                'pattern_type': correlation.pattern_type,
                'confidence_score': correlation.confidence_score,
                'occurrence_frequency': correlation.occurrence_frequency,
                'temporal_gap': str(correlation.temporal_gap),
                'event_count': len(all_events),
                'providers': list(set(event.stream_id for event in all_events)),
                'creation_trigger': 'correlation_detection'
            }

            # Use memory anchor service to create the anchor
            # This integrates with our existing memory anchor infrastructure
            anchor_id = uuid4()

            # Create MemoryAnchor object
            anchor = MemoryAnchor(
                anchor_id=anchor_id,
                timestamp=anchor_timestamp,
                cursors=cursors,
                metadata=metadata
            )

            # Store in database through memory service
            anchor_doc = anchor.to_arangodb_document()
            db = get_database()
            result = db.collection('memory_anchors').insert(anchor_doc)

            if result:
                self.correlation_stats['memory_anchors_created'] += 1
                self.logger.info(
                    f"Created memory anchor {anchor_id} from {correlation.pattern_type} "
                    f"correlation (confidence: {correlation.confidence_score:.2f})"
                )
                return anchor

        except Exception as e:
            self.logger.error(f"Failed to create memory anchor from correlation: {e}")

        return None

    async def add_feedback(self, feedback: CorrelationFeedback):
        """
        Add user feedback about a correlation.

        Feedback is used for adaptive learning - the system learns
        which types of correlations users find meaningful and adjusts
        its detection sensitivity accordingly.

        Args:
            feedback: User feedback about correlation quality
        """
        self.feedback_queue.append(feedback)

        # Process feedback in batches for learning
        if len(self.feedback_queue) >= self.learning_batch_size:
            await self._process_feedback_batch()

    async def _process_feedback_batch(self):
        """
        Process accumulated feedback for adaptive learning.

        This is where the system learns from human wisdom about
        which correlations are meaningful and adjusts its parameters
        to improve future detection accuracy.
        """
        if not self.feedback_queue:
            return

        feedback_batch = self.feedback_queue.copy()
        self.feedback_queue.clear()

        try:
            # Update adaptive thresholds based on feedback
            learning_results = self.adaptive_thresholds.update_from_feedback(feedback_batch)

            # Update confidence scorer with feedback
            self.confidence_scorer.update_weights_from_feedback(feedback_batch)

            self.logger.info(
                f"Processed {len(feedback_batch)} feedback items. "
                f"Learning results: {learning_results}"
            )

        except Exception as e:
            self.logger.error(f"Error processing feedback batch: {e}")

    def get_engine_status(self) -> dict[str, any]:
        """
        Get comprehensive status information about the correlation engine.

        Returns:
            Dictionary with engine status, statistics, and configuration
        """
        threshold_summary = self.adaptive_thresholds.get_performance_summary()

        return {
            'engine_info': {
                'status': 'active',
                'window_size': str(self.window_size),
                'window_overlap': self.window_overlap,
                'active_windows': len(self.active_windows),
                'event_buffer_size': len(self.event_buffer),
                'pending_feedback': len(self.feedback_queue)
            },
            'statistics': self.correlation_stats.copy(),
            'pattern_detectors': list(self.pattern_detectors.keys()),
            'adaptive_thresholds': threshold_summary,
            'confidence_scoring': {
                'factor_weights': self.confidence_scorer.factor_weights,
                'feedback_history_size': len(self.confidence_scorer.feedback_history)
            }
        }

    async def force_learning_update(self):
        """
        Force processing of any pending feedback for immediate learning.

        Useful for testing or when immediate adaptation is needed.
        """
        if self.feedback_queue:
            await self._process_feedback_batch()

    def reset_learning_state(self):
        """
        Reset all learning state to defaults.

        Useful for testing or when starting fresh adaptation.
        """
        self.adaptive_thresholds.reset_to_defaults()
        self.confidence_scorer.feedback_history.clear()
        self.feedback_queue.clear()

        # Reset statistics
        self.correlation_stats = {
            'total_correlations_detected': 0,
            'correlations_accepted': 0,
            'correlations_rejected': 0,
            'memory_anchors_created': 0,
            'last_processing_time': None
        }

        self.logger.info("Reset correlation engine learning state to defaults")

    async def shutdown(self):
        """Clean shutdown of the correlation engine."""
        self.logger.info("Shutting down Correlation Engine...")

        # Process any remaining feedback
        if self.feedback_queue:
            await self._process_feedback_batch()

        # Save current state
        self.adaptive_thresholds._save_configuration()

        self.logger.info("Correlation Engine shutdown complete")


class CorrelationToAnchorAdapter:
    """
    Adapter for converting correlations to memory anchor creation requests.

    This class implements the integration between the correlation engine
    and the memory anchor service, following the architectural design.
    """

    def __init__(self, anchor_service: MemoryAnchorService):
        """
        Initialize the adapter.

        Args:
            anchor_service: Memory anchor service for creating anchors
        """
        self.anchor_service = anchor_service
        self.confidence_threshold = 0.7  # Only create anchors for high-confidence correlations

    async def process_correlation(self, correlation: TemporalCorrelation) -> MemoryAnchor | None:
        """
        Convert high-confidence correlation into memory anchor.

        This method implements the architectural vision of transforming
        detected temporal patterns into persistent memory anchors that
        can be used for context reconstruction and search.

        Args:
            correlation: Temporal correlation to convert

        Returns:
            Created memory anchor or None if correlation doesn't meet criteria
        """
        if correlation.confidence_score < self.confidence_threshold:
            return None

        # Extract temporal window from correlation events
        all_events = [correlation.primary_event] + correlation.correlated_events
        timestamps = [event.timestamp for event in all_events]

        start_time = min(timestamps)
        end_time = max(timestamps)

        # Determine precision based on temporal gap
        precision = self._determine_precision(correlation.temporal_gap)

        # Extract activity streams and storage events
        activity_streams = []
        storage_events = []

        for event in all_events:
            if event.event_type.value == 'activity':
                activity_streams.append(event.stream_id)
            elif event.event_type.value == 'storage':
                storage_events.append(event.stream_id)

        # Create cursor update for the anchor
        cursor_data = {
            'correlation_type': correlation.pattern_type,
            'temporal_window': {
                'start': start_time.isoformat(),
                'end': end_time.isoformat(),
                'precision': precision.value
            },
            'pattern_strength': correlation.confidence_score,
            'occurrence_frequency': correlation.occurrence_frequency
        }

        # Use the memory anchor service to create the anchor
        # This integrates with the existing provider/cursor system
        try:
            # Register as a correlation provider if not already done
            from ..services.memory_anchor_service import ProviderInfo

            provider_info = ProviderInfo(
                provider_id="correlation_engine",
                provider_type="correlation",
                cursor_types=["correlation_detection"],
                metadata={"pattern_types": list(correlation.pattern_type)}
            )

            await self.anchor_service.register_provider(provider_info)

            # Create cursor update
            from ..services.memory_anchor_service import CursorUpdate

            cursor_update = CursorUpdate(
                provider_id="correlation_engine",
                cursor_type="correlation_detection",
                cursor_value=cursor_data,
                metadata={
                    'correlation_id': str(correlation.correlation_id),
                    'confidence_score': correlation.confidence_score,
                    'pattern_type': correlation.pattern_type
                }
            )

            # Update cursor to create or update anchor
            response = await self.anchor_service.update_cursor(cursor_update)

            if response:
                # Retrieve the created/updated anchor
                anchor = await self.anchor_service.get_anchor_by_id(response.anchor_id)
                return anchor

        except Exception as e:
            logging.error(f"Failed to create memory anchor from correlation: {e}")

        return None

    def _determine_precision(self, temporal_gap: timedelta) -> TemporalPrecision:
        """Determine appropriate temporal precision for memory anchor."""
        total_seconds = temporal_gap.total_seconds()

        if total_seconds < 60:
            return TemporalPrecision.INSTANT
        elif total_seconds < 300:  # 5 minutes
            return TemporalPrecision.MINUTE
        elif total_seconds < 1800:  # 30 minutes
            return TemporalPrecision.SESSION
        elif total_seconds < 14400:  # 4 hours
            return TemporalPrecision.DAILY
        else:
            return TemporalPrecision.CYCLICAL
