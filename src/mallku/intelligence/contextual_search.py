#!/usr/bin/env python3
"""
Contextual Search for Memory Anchors

Enables intelligent search through memory anchors based on contextual similarity,
temporal proximity, and pattern relationships. Goes beyond simple retrieval to
discover related contexts and patterns.
"""

import logging
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import Any

from mallku.models.memory_anchor import MemoryAnchor

logger = logging.getLogger(__name__)


class SearchResult:
    """Represents a search result with relevance scoring."""

    def __init__(self, anchor: MemoryAnchor, relevance: float, match_reasons: list[str]):
        self.anchor = anchor
        self.relevance = relevance
        self.match_reasons = match_reasons

    def __repr__(self):
        return f"SearchResult(relevance={self.relevance:.3f}, reasons={len(self.match_reasons)})"


class ContextualSearchEngine:
    """
    Advanced search engine for memory anchors that understands context,
    patterns, and relationships.
    """

    def __init__(self, anchors: list[MemoryAnchor]):
        self.anchors = anchors
        self._build_indices()

    def _build_indices(self):
        """Build indices for efficient search."""
        # File path index
        self.file_index: dict[str, list[MemoryAnchor]] = defaultdict(list)

        # Pattern type index
        self.pattern_index: dict[str, list[MemoryAnchor]] = defaultdict(list)

        # Temporal index (by hour)
        self.temporal_index: dict[int, list[MemoryAnchor]] = defaultdict(list)

        # Cursor type index
        self.cursor_index: dict[str, list[MemoryAnchor]] = defaultdict(list)

        # Build indices
        for anchor in self.anchors:
            # Index by files
            for cursor in anchor.cursors.values():
                if isinstance(cursor, dict) and 'file_path' in cursor:
                    self.file_index[cursor['file_path']].append(anchor)

            # Index by pattern type
            pattern_type = anchor.metadata.get('correlation_metadata', {}).get('pattern_type')
            if pattern_type:
                self.pattern_index[pattern_type].append(anchor)

            # Index by hour
            hour = anchor.timestamp.hour
            self.temporal_index[hour].append(anchor)

            # Index by cursor types
            for cursor_type in anchor.cursors:
                self.cursor_index[cursor_type].append(anchor)

        logger.info(f"Built indices for {len(self.anchors)} anchors")
        logger.info(f"  Files indexed: {len(self.file_index)}")
        logger.info(f"  Pattern types: {list(self.pattern_index.keys())}")

    def search_by_context(
        self,
        query_context: dict[str, Any],
        max_results: int = 10
    ) -> list[SearchResult]:
        """
        Search for anchors matching a given context.

        Args:
            query_context: Dictionary describing the search context
                - files: List of file paths
                - patterns: List of pattern types
                - time_range: Tuple of (start, end) datetime
                - confidence_min: Minimum confidence score
                - cursor_types: List of required cursor types
            max_results: Maximum number of results to return

        Returns:
            List of SearchResult objects sorted by relevance
        """
        results = []

        for anchor in self.anchors:
            relevance = 0.0
            match_reasons = []

            # File matching
            if 'files' in query_context:
                file_matches = self._match_files(anchor, query_context['files'])
                if file_matches > 0:
                    relevance += file_matches * 0.3
                    match_reasons.append(f"Matched {file_matches} files")

            # Pattern matching
            if 'patterns' in query_context and self._match_pattern(anchor, query_context['patterns']):
                relevance += 0.2
                match_reasons.append("Pattern type match")

            # Time range matching
            if 'time_range' in query_context and self._in_time_range(anchor, query_context['time_range']):
                relevance += 0.1
                match_reasons.append("Within time range")

            # Confidence threshold
            if 'confidence_min' in query_context:
                conf = anchor.metadata.get('correlation_metadata', {}).get('confidence_score', 0)
                if conf >= query_context['confidence_min']:
                    relevance += 0.1 * conf
                    match_reasons.append(f"High confidence ({conf:.3f})")

            # Cursor type matching
            if 'cursor_types' in query_context:
                cursor_matches = self._match_cursor_types(anchor, query_context['cursor_types'])
                if cursor_matches > 0:
                    relevance += cursor_matches * 0.2
                    match_reasons.append(f"Has {cursor_matches} cursor types")

            # Add to results if relevant
            if relevance > 0:
                results.append(SearchResult(anchor, relevance, match_reasons))

        # Sort by relevance and return top results
        results.sort(key=lambda r: r.relevance, reverse=True)
        return results[:max_results]

    def find_similar_anchors(
        self,
        reference_anchor: MemoryAnchor,
        similarity_threshold: float = 0.5,
        max_results: int = 5
    ) -> list[SearchResult]:
        """
        Find anchors similar to a reference anchor.

        Uses multiple dimensions of similarity including files, patterns,
        temporal proximity, and cursor structure.
        """
        results = []

        for anchor in self.anchors:
            if anchor.anchor_id == reference_anchor.anchor_id:
                continue

            similarity = self._calculate_similarity(reference_anchor, anchor)

            if similarity >= similarity_threshold:
                reasons = self._explain_similarity(reference_anchor, anchor)
                results.append(SearchResult(anchor, similarity, reasons))

        # Sort by similarity
        results.sort(key=lambda r: r.relevance, reverse=True)
        return results[:max_results]

    def discover_patterns_for_file(self, file_path: str) -> dict[str, Any]:
        """
        Discover all patterns associated with a specific file.

        Returns comprehensive analysis of how the file participates
        in different correlation patterns.
        """
        # Find all anchors referencing this file
        file_anchors = self.file_index.get(file_path, [])

        if not file_anchors:
            return {
                "file": file_path,
                "found": False,
                "anchor_count": 0
            }

        # Analyze patterns
        pattern_distribution = Counter()
        confidence_by_pattern = defaultdict(list)
        temporal_distribution = defaultdict(int)
        co_occurring_files = Counter()

        for anchor in file_anchors:
            # Pattern types
            pattern_type = anchor.metadata.get('correlation_metadata', {}).get('pattern_type', 'unknown')
            pattern_distribution[pattern_type] += 1

            # Confidence scores
            conf = anchor.metadata.get('correlation_metadata', {}).get('confidence_score')
            if conf is not None:
                confidence_by_pattern[pattern_type].append(conf)

            # Temporal distribution
            hour = anchor.timestamp.hour
            temporal_distribution[hour] += 1

            # Co-occurring files
            for cursor in anchor.cursors.values():
                if isinstance(cursor, dict) and 'file_path' in cursor:
                    other_file = cursor['file_path']
                    if other_file != file_path:
                        co_occurring_files[other_file] += 1

        # Calculate statistics
        analysis = {
            "file": file_path,
            "found": True,
            "anchor_count": len(file_anchors),
            "pattern_distribution": dict(pattern_distribution),
            "average_confidence_by_pattern": {
                pattern: statistics.mean(scores)
                for pattern, scores in confidence_by_pattern.items()
            },
            "temporal_distribution": dict(temporal_distribution),
            "most_active_hours": sorted(
                temporal_distribution.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3],
            "frequently_co_occurring_files": co_occurring_files.most_common(5),
            "earliest_occurrence": min(a.timestamp for a in file_anchors),
            "latest_occurrence": max(a.timestamp for a in file_anchors),
            "time_span_hours": (
                max(a.timestamp for a in file_anchors) -
                min(a.timestamp for a in file_anchors)
            ).total_seconds() / 3600
        }

        return analysis

    def trace_temporal_flow(
        self,
        start_time: datetime,
        duration: timedelta,
        pattern_filter: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """
        Trace the flow of patterns within a time window.

        Returns a timeline of pattern activity showing how different
        correlation types emerge and evolve.
        """
        end_time = start_time + duration

        # Find anchors in time range
        anchors_in_range = [
            a for a in self.anchors
            if start_time <= a.timestamp <= end_time
        ]

        # Apply pattern filter if provided
        if pattern_filter:
            anchors_in_range = [
                a for a in anchors_in_range
                if a.metadata.get('correlation_metadata', {}).get('pattern_type') in pattern_filter
            ]

        # Sort by time
        anchors_in_range.sort(key=lambda a: a.timestamp)

        # Build timeline
        timeline = []
        for anchor in anchors_in_range:
            meta = anchor.metadata.get('correlation_metadata', {})

            event = {
                "timestamp": anchor.timestamp.isoformat(),
                "anchor_id": str(anchor.anchor_id),
                "pattern_type": meta.get('pattern_type', 'unknown'),
                "confidence": meta.get('confidence_score', 0),
                "files_involved": self._extract_file_count(anchor),
                "cursor_count": len(anchor.cursors)
            }

            timeline.append(event)

        return timeline

    def _match_files(self, anchor: MemoryAnchor, query_files: list[str]) -> int:
        """Count how many query files are referenced in the anchor."""
        anchor_files = set()
        for cursor in anchor.cursors.values():
            if isinstance(cursor, dict) and 'file_path' in cursor:
                anchor_files.add(cursor['file_path'])

        return len(set(query_files).intersection(anchor_files))

    def _match_pattern(self, anchor: MemoryAnchor, patterns: list[str]) -> bool:
        """Check if anchor's pattern type matches any in the list."""
        pattern_type = anchor.metadata.get('correlation_metadata', {}).get('pattern_type')
        return pattern_type in patterns

    def _in_time_range(self, anchor: MemoryAnchor, time_range: tuple[datetime, datetime]) -> bool:
        """Check if anchor is within the time range."""
        start, end = time_range
        return start <= anchor.timestamp <= end

    def _match_cursor_types(self, anchor: MemoryAnchor, cursor_types: list[str]) -> int:
        """Count how many required cursor types are present."""
        anchor_cursors = set(anchor.cursors.keys())
        return len(set(cursor_types).intersection(anchor_cursors))

    def _calculate_similarity(self, anchor1: MemoryAnchor, anchor2: MemoryAnchor) -> float:
        """Calculate overall similarity between two anchors."""
        factors = []

        # File similarity
        files1 = self._extract_files_set(anchor1)
        files2 = self._extract_files_set(anchor2)
        if files1 or files2:
            file_jaccard = len(files1.intersection(files2)) / len(files1.union(files2))
            factors.append(file_jaccard)

        # Pattern similarity
        pattern1 = anchor1.metadata.get('correlation_metadata', {}).get('pattern_type')
        pattern2 = anchor2.metadata.get('correlation_metadata', {}).get('pattern_type')
        if pattern1 and pattern2:
            factors.append(1.0 if pattern1 == pattern2 else 0.0)

        # Temporal proximity (within 1 hour = 1.0, beyond 24 hours = 0.0)
        time_diff = abs((anchor1.timestamp - anchor2.timestamp).total_seconds())
        temporal_similarity = max(0, 1.0 - (time_diff / 86400))  # 86400 = 24 hours
        factors.append(temporal_similarity)

        # Cursor structure similarity
        cursors1 = set(anchor1.cursors.keys())
        cursors2 = set(anchor2.cursors.keys())
        if cursors1 or cursors2:
            cursor_jaccard = len(cursors1.intersection(cursors2)) / len(cursors1.union(cursors2))
            factors.append(cursor_jaccard)

        # Confidence similarity
        conf1 = anchor1.metadata.get('correlation_metadata', {}).get('confidence_score', 0)
        conf2 = anchor2.metadata.get('correlation_metadata', {}).get('confidence_score', 0)
        if conf1 and conf2:
            conf_similarity = 1.0 - abs(conf1 - conf2)
            factors.append(conf_similarity)

        return statistics.mean(factors) if factors else 0.0

    def _explain_similarity(self, anchor1: MemoryAnchor, anchor2: MemoryAnchor) -> list[str]:
        """Explain why two anchors are similar."""
        reasons = []

        # Check file overlap
        files1 = self._extract_files_set(anchor1)
        files2 = self._extract_files_set(anchor2)
        common_files = files1.intersection(files2)
        if common_files:
            reasons.append(f"Share {len(common_files)} files")

        # Check pattern match
        pattern1 = anchor1.metadata.get('correlation_metadata', {}).get('pattern_type')
        pattern2 = anchor2.metadata.get('correlation_metadata', {}).get('pattern_type')
        if pattern1 and pattern2 and pattern1 == pattern2:
            reasons.append(f"Same pattern type: {pattern1}")

        # Check temporal proximity
        time_diff = abs((anchor1.timestamp - anchor2.timestamp).total_seconds())
        if time_diff < 300:  # 5 minutes
            reasons.append(f"Temporally close ({time_diff:.0f}s apart)")

        # Check cursor overlap
        cursors1 = set(anchor1.cursors.keys())
        cursors2 = set(anchor2.cursors.keys())
        common_cursors = cursors1.intersection(cursors2)
        if len(common_cursors) > len(cursors1.union(cursors2)) * 0.5:
            reasons.append(f"Similar cursor structure ({len(common_cursors)} common)")

        return reasons

    def _extract_files_set(self, anchor: MemoryAnchor) -> set[str]:
        """Extract all file paths from an anchor as a set."""
        files = set()
        for cursor in anchor.cursors.values():
            if isinstance(cursor, dict) and 'file_path' in cursor:
                files.add(cursor['file_path'])
        return files

    def _extract_file_count(self, anchor: MemoryAnchor) -> int:
        """Count unique files referenced in an anchor."""
        return len(self._extract_files_set(anchor))
