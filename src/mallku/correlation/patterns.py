"""
Pattern detection algorithms for the Correlation Engine.

These classes implement the four fundamental types of temporal correlations:
Sequential, Concurrent, Cyclical, and Contextual patterns. Each pattern type
represents a different way that human activities can be meaningfully related
across time.
"""

import math
import statistics
from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import timedelta

# Note: numpy and scipy removed to avoid dependencies for initial testing
from .models import Event, TemporalCorrelation, TemporalPrecision


class PatternDetector(ABC):
    """
    Abstract base class for pattern detection algorithms.

    Each pattern detector implements a specific algorithm for recognizing
    one type of temporal correlation in streams of events.
    """

    def __init__(self, min_occurrences: int = 3, min_confidence: float = 0.6):
        self.min_occurrences = min_occurrences
        self.min_confidence = min_confidence

    @abstractmethod
    def detect_patterns(self, events: list[Event]) -> list[TemporalCorrelation]:
        """
        Detect patterns of this type in the given events.

        Args:
            events: List of events to analyze, sorted by timestamp

        Returns:
            List of detected correlations
        """
        pass

    @abstractmethod
    def get_pattern_type(self) -> str:
        """Return the name of this pattern type."""
        pass


class SequentialPattern(PatternDetector):
    """
    Detects sequential patterns: Event A consistently followed by Event B.

    Examples:
    - Email received -> Document created
    - Meeting started -> File accessed
    - Calendar reminder -> Task completed
    """

    def get_pattern_type(self) -> str:
        return "sequential"

    def detect_patterns(self, events: list[Event]) -> list[TemporalCorrelation]:
        """
        Detect sequential patterns using temporal ordering analysis.

        Algorithm:
        1. Group events by type/stream
        2. For each pair of event types, find instances where A precedes B
        3. Analyze timing consistency and frequency
        4. Generate correlations for patterns meeting thresholds
        """
        correlations = []

        # Group events by type and stream for pattern analysis
        event_groups = self._group_events(events)

        # Analyze all pairs of event groups for sequential patterns
        for primary_key, primary_events in event_groups.items():
            for secondary_key, secondary_events in event_groups.items():
                if primary_key == secondary_key:
                    continue

                pattern = self._analyze_sequential_pair(
                    primary_events, secondary_events, primary_key, secondary_key
                )

                if pattern and pattern.occurrence_frequency >= self.min_occurrences:
                    correlations.append(pattern)

        return [c for c in correlations if c.confidence_score >= self.min_confidence]

    def _group_events(self, events: list[Event]) -> dict[str, list[Event]]:
        """Group events by type and stream for pattern analysis."""
        groups = defaultdict(list)

        for event in events:
            # Create group key from event type and stream
            key = f"{event.event_type}:{event.stream_id}"
            groups[key].append(event)

        # Sort events within each group by timestamp
        for group in groups.values():
            group.sort(key=lambda e: e.timestamp)

        return dict(groups)

    def _analyze_sequential_pair(
        self,
        primary_events: list[Event],
        secondary_events: list[Event],
        primary_key: str,
        secondary_key: str,
    ) -> TemporalCorrelation | None:
        """
        Analyze a pair of event groups for sequential patterns.

        Returns a TemporalCorrelation if a strong sequential pattern is found.
        """
        sequences = []

        # Find instances where primary events are followed by secondary events
        for primary in primary_events:
            for secondary in secondary_events:
                if secondary.timestamp > primary.timestamp:
                    gap = secondary.timestamp - primary.timestamp

                    # Only consider reasonable time gaps (up to 24 hours)
                    if gap <= timedelta(hours=24):
                        sequences.append({"primary": primary, "secondary": secondary, "gap": gap})

        if len(sequences) < self.min_occurrences:
            return None

        # Analyze timing consistency
        gaps = [seq["gap"].total_seconds() for seq in sequences]
        gap_mean = statistics.mean(gaps)
        gap_variance = statistics.variance(gaps) if len(gaps) > 1 else 0

        # Calculate pattern stability (inverse of coefficient of variation)
        if gap_mean > 0:
            cv = math.sqrt(gap_variance) / gap_mean
            stability = 1.0 / (1.0 + cv)  # Higher stability = lower variance
        else:
            stability = 0.0

        # Determine temporal precision based on gap consistency
        precision = self._determine_precision(timedelta(seconds=gap_mean))

        # Calculate confidence based on frequency and consistency
        frequency_score = min(len(sequences) / 10.0, 1.0)  # Normalize to 0-1
        consistency_score = stability
        confidence = (frequency_score + consistency_score) / 2.0

        # Select representative events for the correlation
        primary_event = sequences[0]["primary"]
        correlated_events = [seq["secondary"] for seq in sequences[:5]]  # Limit examples

        return TemporalCorrelation(
            primary_event=primary_event,
            correlated_events=correlated_events,
            temporal_gap=timedelta(seconds=gap_mean),
            gap_variance=gap_variance,
            temporal_precision=precision,
            occurrence_frequency=len(sequences),
            pattern_stability=stability,
            pattern_type=self.get_pattern_type(),
            confidence_score=confidence,
            confidence_factors={
                "frequency_strength": frequency_score,
                "temporal_consistency": consistency_score,
            },
            last_occurrence=max(seq["secondary"].timestamp for seq in sequences),
        )

    def _determine_precision(self, avg_gap: timedelta) -> TemporalPrecision:
        """Determine appropriate temporal precision based on average gap."""
        total_seconds = avg_gap.total_seconds()

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


class ConcurrentPattern(PatternDetector):
    """
    Detects concurrent patterns: Events A and B consistently occur together.

    Examples:
    - Music playing + Code editing
    - Location X + Document type Y
    - Video call + Note taking
    """

    def get_pattern_type(self) -> str:
        return "concurrent"

    def detect_patterns(self, events: list[Event]) -> list[TemporalCorrelation]:
        """
        Detect concurrent patterns using temporal overlap analysis.

        Algorithm:
        1. Define temporal windows for concurrency (seconds to minutes)
        2. Find event pairs that occur within the same window
        3. Analyze co-occurrence frequency and context similarity
        4. Generate correlations for strong concurrent patterns
        """
        correlations = []

        # Define concurrency windows (events must be within these timeframes)
        concurrency_windows = [
            timedelta(seconds=30),  # Very tight concurrency
            timedelta(minutes=2),  # Loose concurrency
            timedelta(minutes=5),  # Session-level concurrency
        ]

        event_groups = self._group_events(events)

        # Analyze concurrent patterns within each window size
        for window in concurrency_windows:
            window_correlations = self._find_concurrent_patterns(event_groups, window)
            correlations.extend(window_correlations)

        return [c for c in correlations if c.confidence_score >= self.min_confidence]

    def _group_events(self, events: list[Event]) -> dict[str, list[Event]]:
        """Group events by type and stream."""
        groups = defaultdict(list)

        for event in events:
            key = f"{event.event_type}:{event.stream_id}"
            groups[key].append(event)

        return dict(groups)

    def _find_concurrent_patterns(
        self, event_groups: dict[str, list[Event]], window: timedelta
    ) -> list[TemporalCorrelation]:
        """Find concurrent patterns within a specific time window."""
        correlations = []

        # Analyze all pairs of event groups
        group_keys = list(event_groups.keys())
        for i, primary_key in enumerate(group_keys):
            for secondary_key in group_keys[i + 1 :]:
                pattern = self._analyze_concurrent_pair(
                    event_groups[primary_key],
                    event_groups[secondary_key],
                    window,
                    primary_key,
                    secondary_key,
                )

                if pattern and pattern.occurrence_frequency >= self.min_occurrences:
                    correlations.append(pattern)

        return correlations

    def _analyze_concurrent_pair(
        self,
        primary_events: list[Event],
        secondary_events: list[Event],
        window: timedelta,
        primary_key: str,
        secondary_key: str,
    ) -> TemporalCorrelation | None:
        """Analyze two event groups for concurrent patterns."""
        concurrent_pairs = []

        # Find event pairs that occur within the concurrency window
        for primary in primary_events:
            for secondary in secondary_events:
                time_diff = abs((secondary.timestamp - primary.timestamp).total_seconds())

                if time_diff <= window.total_seconds():
                    concurrent_pairs.append(
                        {
                            "primary": primary,
                            "secondary": secondary,
                            "gap": abs(secondary.timestamp - primary.timestamp),
                        }
                    )

        if len(concurrent_pairs) < self.min_occurrences:
            return None

        # Calculate concurrency metrics
        gaps = [pair["gap"].total_seconds() for pair in concurrent_pairs]
        avg_gap = statistics.mean(gaps)
        gap_variance = statistics.variance(gaps) if len(gaps) > 1 else 0

        # Pattern stability (prefer tighter temporal clustering)
        max_gap = window.total_seconds()
        avg_tightness = 1.0 - (avg_gap / max_gap)
        stability = avg_tightness

        # Calculate context similarity if available
        context_similarity = self._calculate_context_similarity(concurrent_pairs)

        # Confidence scoring
        frequency_score = min(len(concurrent_pairs) / 10.0, 1.0)
        temporal_score = stability
        context_score = context_similarity

        confidence = (frequency_score + temporal_score + context_score) / 3.0

        # Create correlation
        primary_event = concurrent_pairs[0]["primary"]
        correlated_events = [pair["secondary"] for pair in concurrent_pairs[:5]]

        return TemporalCorrelation(
            primary_event=primary_event,
            correlated_events=correlated_events,
            temporal_gap=timedelta(seconds=avg_gap),
            gap_variance=gap_variance,
            temporal_precision=TemporalPrecision.MINUTE,  # Concurrent patterns are typically minute-scale
            occurrence_frequency=len(concurrent_pairs),
            pattern_stability=stability,
            pattern_type=self.get_pattern_type(),
            confidence_score=confidence,
            confidence_factors={
                "frequency_strength": frequency_score,
                "temporal_consistency": temporal_score,
                "context_coherence": context_score,
            },
            last_occurrence=max(pair["secondary"].timestamp for pair in concurrent_pairs),
        )

    def _calculate_context_similarity(self, concurrent_pairs: list[dict]) -> float:
        """Calculate context similarity between concurrent events."""
        if not concurrent_pairs:
            return 0.0

        # Simple context similarity based on shared context keys
        similarities = []

        for pair in concurrent_pairs:
            primary_context = set(pair["primary"].context.keys())
            secondary_context = set(pair["secondary"].context.keys())

            if primary_context or secondary_context:
                intersection = len(primary_context & secondary_context)
                union = len(primary_context | secondary_context)
                similarity = intersection / union if union > 0 else 0.0
                similarities.append(similarity)

        return statistics.mean(similarities) if similarities else 0.5


class CyclicalPattern(PatternDetector):
    """
    Detects cyclical patterns: Events that repeat on predictable schedules.

    Examples:
    - Weekly review + Planning documents
    - Daily standup + Task updates
    - Monthly reports + Data analysis
    """

    def get_pattern_type(self) -> str:
        return "cyclical"

    def detect_patterns(self, events: list[Event]) -> list[TemporalCorrelation]:
        """
        Detect cyclical patterns using periodicity analysis.

        Algorithm:
        1. Group events by type/stream
        2. For each group, analyze temporal distribution
        3. Use frequency domain analysis to detect periodic patterns
        4. Validate cycles with statistical significance testing
        """
        correlations = []

        event_groups = self._group_events(events)

        # Analyze each event group for cyclical patterns
        for group_key, group_events in event_groups.items():
            if len(group_events) < self.min_occurrences:
                continue

            patterns = self._analyze_cyclical_group(group_events, group_key)
            correlations.extend(patterns)

        return [c for c in correlations if c.confidence_score >= self.min_confidence]

    def _group_events(self, events: list[Event]) -> dict[str, list[Event]]:
        """Group events by type and stream."""
        groups = defaultdict(list)

        for event in events:
            key = f"{event.event_type}:{event.stream_id}"
            groups[key].append(event)

        # Sort by timestamp
        for group in groups.values():
            group.sort(key=lambda e: e.timestamp)

        return dict(groups)

    def _analyze_cyclical_group(
        self, events: list[Event], group_key: str
    ) -> list[TemporalCorrelation]:
        """Analyze a group of events for cyclical patterns."""
        if len(events) < 3:  # Need at least 3 events to detect cycles
            return []

        correlations = []

        # Calculate inter-event intervals
        intervals = []
        for i in range(1, len(events)):
            interval = events[i].timestamp - events[i - 1].timestamp
            intervals.append(interval.total_seconds())

        # Detect periodic patterns in intervals
        cycles = self._detect_periodic_cycles(intervals)

        for cycle_period, cycle_strength in cycles:
            if cycle_strength >= 0.5:  # Minimum cycle strength threshold
                pattern = self._create_cyclical_correlation(
                    events, cycle_period, cycle_strength, group_key
                )
                if pattern:
                    correlations.append(pattern)

        return correlations

    def _detect_periodic_cycles(self, intervals: list[float]) -> list[tuple[float, float]]:
        """
        Detect periodic cycles in interval data using frequency analysis.

        Returns list of (period, strength) tuples.
        """
        if len(intervals) < 3:
            return []

        cycles = []

        # Test common cycle periods (in seconds)
        test_periods = [
            3600,  # Hourly
            86400,  # Daily
            604800,  # Weekly
            2629746,  # Monthly (average)
        ]

        for period in test_periods:
            strength = self._calculate_cycle_strength(intervals, period)
            if strength > 0.3:  # Minimum strength threshold
                cycles.append((period, strength))

        return cycles

    def _calculate_cycle_strength(self, intervals: list[float], period: float) -> float:
        """
        Calculate how well the intervals match a given period.

        Uses statistical analysis to measure periodicity strength.
        """
        if not intervals:
            return 0.0

        # Calculate how well intervals cluster around the period
        deviations = []
        for interval in intervals:
            # Find nearest multiple of period
            nearest_multiple = round(interval / period) * period
            deviation = abs(interval - nearest_multiple) / period
            deviations.append(deviation)

        # Strength is inverse of average deviation
        avg_deviation = statistics.mean(deviations)
        strength = max(0.0, 1.0 - avg_deviation)

        return strength

    def _create_cyclical_correlation(
        self, events: list[Event], cycle_period: float, cycle_strength: float, group_key: str
    ) -> TemporalCorrelation | None:
        """Create a TemporalCorrelation for a detected cyclical pattern."""

        # Use first event as primary, recent events as correlated
        primary_event = events[0]
        correlated_events = events[1:6]  # Limit to 5 examples

        # Calculate average gap (cycle period)
        avg_gap = timedelta(seconds=cycle_period)

        # Determine precision based on cycle period
        if cycle_period < 7200:  # < 2 hours
            precision = TemporalPrecision.SESSION
        elif cycle_period < 172800:  # < 2 days
            precision = TemporalPrecision.DAILY
        else:
            precision = TemporalPrecision.CYCLICAL

        # Calculate confidence
        frequency_score = min(len(events) / 10.0, 1.0)
        periodicity_score = cycle_strength
        confidence = (frequency_score + periodicity_score) / 2.0

        return TemporalCorrelation(
            primary_event=primary_event,
            correlated_events=correlated_events,
            temporal_gap=avg_gap,
            gap_variance=0.0,  # TODO: Calculate actual variance
            temporal_precision=precision,
            occurrence_frequency=len(events),
            pattern_stability=cycle_strength,
            pattern_type=self.get_pattern_type(),
            confidence_score=confidence,
            confidence_factors={
                "frequency_strength": frequency_score,
                "periodicity_strength": periodicity_score,
            },
            last_occurrence=events[-1].timestamp,
        )


class ContextualPattern(PatternDetector):
    """
    Detects contextual patterns: Events clustered by environmental similarity.

    Examples:
    - Travel context + Expense reports
    - Home office + Personal projects
    - Late evening + Creative work
    """

    def get_pattern_type(self) -> str:
        return "contextual"

    def detect_patterns(self, events: list[Event]) -> list[TemporalCorrelation]:
        """
        Detect contextual patterns using context vector clustering.

        Algorithm:
        1. Extract context vectors from events
        2. Perform clustering analysis on context similarity
        3. Identify temporal patterns within clusters
        4. Generate correlations for significant context-based patterns
        """
        correlations = []

        # Group events by context similarity
        context_clusters = self._cluster_events_by_context(events)

        # Analyze each cluster for temporal patterns
        for cluster_id, cluster_events in context_clusters.items():
            if len(cluster_events) >= self.min_occurrences:
                pattern = self._analyze_contextual_cluster(cluster_events, cluster_id)
                if pattern:
                    correlations.append(pattern)

        return [c for c in correlations if c.confidence_score >= self.min_confidence]

    def _cluster_events_by_context(self, events: list[Event]) -> dict[str, list[Event]]:
        """
        Cluster events based on context similarity.

        Simple clustering based on shared context keys and values.
        """
        clusters = defaultdict(list)

        for event in events:
            # Create cluster key from context
            cluster_key = self._create_context_signature(event.context)
            clusters[cluster_key].append(event)

        # Filter out small clusters
        return {k: v for k, v in clusters.items() if len(v) >= 2}

    def _create_context_signature(self, context: dict) -> str:
        """Create a signature string from event context."""
        if not context:
            return "no_context"

        # Sort context items for consistent signatures
        items = sorted(context.items())

        # Create signature from key-value pairs
        signature_parts = []
        for key, value in items:
            if isinstance(value, str | int | float | bool):
                signature_parts.append(f"{key}:{value}")
            else:
                signature_parts.append(f"{key}:complex")

        return "|".join(signature_parts)

    def _analyze_contextual_cluster(
        self, cluster_events: list[Event], cluster_id: str
    ) -> TemporalCorrelation | None:
        """Analyze a context cluster for temporal patterns."""

        # Sort events by timestamp
        cluster_events.sort(key=lambda e: e.timestamp)

        # Calculate temporal characteristics
        if len(cluster_events) < 2:
            return None

        # Analyze time gaps between events in cluster
        gaps = []
        for i in range(1, len(cluster_events)):
            gap = cluster_events[i].timestamp - cluster_events[i - 1].timestamp
            gaps.append(gap.total_seconds())

        if not gaps:
            return None

        avg_gap = statistics.mean(gaps)
        gap_variance = statistics.variance(gaps) if len(gaps) > 1 else 0

        # Calculate context coherence (how similar contexts are)
        context_coherence = self._calculate_cluster_coherence(cluster_events)

        # Pattern stability based on temporal consistency
        if avg_gap > 0:
            cv = math.sqrt(gap_variance) / avg_gap
            stability = 1.0 / (1.0 + cv)
        else:
            stability = 1.0

        # Confidence scoring
        frequency_score = min(len(cluster_events) / 10.0, 1.0)
        context_score = context_coherence
        temporal_score = stability

        confidence = (frequency_score + context_score + temporal_score) / 3.0

        # Determine precision
        precision = self._determine_precision(timedelta(seconds=avg_gap))

        # Create correlation
        primary_event = cluster_events[0]
        correlated_events = cluster_events[1:6]  # Limit examples

        return TemporalCorrelation(
            primary_event=primary_event,
            correlated_events=correlated_events,
            temporal_gap=timedelta(seconds=avg_gap),
            gap_variance=gap_variance,
            temporal_precision=precision,
            occurrence_frequency=len(cluster_events),
            pattern_stability=stability,
            pattern_type=self.get_pattern_type(),
            confidence_score=confidence,
            confidence_factors={
                "frequency_strength": frequency_score,
                "context_coherence": context_score,
                "temporal_consistency": temporal_score,
            },
            last_occurrence=cluster_events[-1].timestamp,
        )

    def _calculate_cluster_coherence(self, events: list[Event]) -> float:
        """Calculate how coherent the context is within a cluster."""
        if len(events) < 2:
            return 1.0

        # Simple coherence: ratio of shared context keys
        all_contexts = [event.context for event in events if event.context]

        if not all_contexts:
            return 0.5  # Neutral score for events without context

        # Find common context keys
        common_keys = set(all_contexts[0].keys())
        for context in all_contexts[1:]:
            common_keys &= set(context.keys())

        # Calculate coherence as ratio of common to total keys
        all_keys = set()
        for context in all_contexts:
            all_keys.update(context.keys())

        if not all_keys:
            return 0.5

        coherence = len(common_keys) / len(all_keys)
        return coherence

    def _determine_precision(self, avg_gap: timedelta) -> TemporalPrecision:
        """Determine appropriate temporal precision."""
        total_seconds = avg_gap.total_seconds()

        if total_seconds < 300:  # 5 minutes
            return TemporalPrecision.MINUTE
        elif total_seconds < 1800:  # 30 minutes
            return TemporalPrecision.SESSION
        elif total_seconds < 14400:  # 4 hours
            return TemporalPrecision.DAILY
        else:
            return TemporalPrecision.CYCLICAL
