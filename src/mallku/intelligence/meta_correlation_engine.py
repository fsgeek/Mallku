#!/usr/bin/env python3
"""
Meta-Correlation Engine

Discovers correlations between memory anchors themselves, building intelligence
from the patterns that have already been preserved. This creates a second-order
correlation system that can identify:

- Temporal cascades where one correlation triggers another
- Contextual neighborhoods of related anchor patterns
- Evolution of confidence scores over time
- Emergent themes from cursor combinations
"""

import logging
import statistics
from collections import Counter, defaultdict
from datetime import UTC, datetime, timedelta
from typing import Any

from mallku.models.memory_anchor import MemoryAnchor

logger = logging.getLogger(__name__)


class MetaPattern:
    """Represents a pattern discovered between memory anchors."""

    def __init__(
        self,
        pattern_id: str,
        pattern_type: str,
        anchors: list[MemoryAnchor],
        confidence: float,
        metadata: dict[str, Any],
    ):
        self.pattern_id = pattern_id
        self.pattern_type = pattern_type
        self.anchors = anchors
        self.confidence = confidence
        self.metadata = metadata
        self.discovered_at = datetime.now(UTC)

    def __repr__(self):
        return f"MetaPattern({self.pattern_type}, {len(self.anchors)} anchors, conf={self.confidence:.2f})"


class TemporalCascade(MetaPattern):
    """A sequence of correlated anchors that appear to trigger each other."""

    def __init__(self, anchors: list[MemoryAnchor], cascade_strength: float):
        super().__init__(
            pattern_id=f"cascade_{datetime.now(UTC).timestamp()}",
            pattern_type="temporal_cascade",
            anchors=anchors,
            confidence=cascade_strength,
            metadata={
                "cascade_length": len(anchors),
                "time_span": self._calculate_time_span(anchors),
                "trigger_patterns": self._identify_triggers(anchors),
            },
        )

    def _calculate_time_span(self, anchors: list[MemoryAnchor]) -> float:
        """Calculate total time span of the cascade."""
        if len(anchors) < 2:
            return 0.0
        timestamps = [a.timestamp for a in anchors]
        return (max(timestamps) - min(timestamps)).total_seconds()

    def _identify_triggers(self, anchors: list[MemoryAnchor]) -> list[dict[str, Any]]:
        """Identify potential trigger relationships between anchors."""
        triggers = []
        for i in range(len(anchors) - 1):
            curr = anchors[i]
            next_anchor = anchors[i + 1]

            # Look for common elements between current and next
            curr_files = self._extract_files(curr)
            next_files = self._extract_files(next_anchor)
            common_files = curr_files.intersection(next_files)

            if common_files:
                triggers.append(
                    {
                        "type": "file_continuity",
                        "trigger_anchor": str(curr.anchor_id),
                        "triggered_anchor": str(next_anchor.anchor_id),
                        "common_elements": list(common_files),
                    }
                )

        return triggers

    def _extract_files(self, anchor: MemoryAnchor) -> set[str]:
        """Extract file paths from anchor cursors."""
        files = set()
        for cursor_data in anchor.cursors.values():
            if isinstance(cursor_data, dict) and "file_path" in cursor_data:
                files.add(cursor_data["file_path"])
        return files


class ContextualNeighborhood(MetaPattern):
    """A group of anchors that share contextual similarity."""

    def __init__(
        self, anchors: list[MemoryAnchor], similarity_matrix: dict[tuple[str, str], float]
    ):
        center = self._find_center_anchor(anchors, similarity_matrix)
        super().__init__(
            pattern_id=f"neighborhood_{datetime.now(UTC).timestamp()}",
            pattern_type="contextual_neighborhood",
            anchors=anchors,
            confidence=self._calculate_cohesion(similarity_matrix),
            metadata={
                "center_anchor": str(center.anchor_id) if center else None,
                "neighborhood_size": len(anchors),
                "cohesion_score": self._calculate_cohesion(similarity_matrix),
                "common_themes": self._extract_themes(anchors),
            },
        )

    def _find_center_anchor(
        self, anchors: list[MemoryAnchor], similarity_matrix: dict[tuple[str, str], float]
    ) -> MemoryAnchor | None:
        """Find the most central anchor in the neighborhood."""
        if not anchors:
            return None

        centrality_scores = {}
        for anchor in anchors:
            score = 0.0
            for other in anchors:
                if anchor.anchor_id != other.anchor_id:
                    key = (str(anchor.anchor_id), str(other.anchor_id))
                    score += similarity_matrix.get(key, 0.0)
            centrality_scores[anchor.anchor_id] = score

        central_id = max(centrality_scores, key=centrality_scores.get)
        return next(a for a in anchors if a.anchor_id == central_id)

    def _calculate_cohesion(self, similarity_matrix: dict[tuple[str, str], float]) -> float:
        """Calculate neighborhood cohesion score."""
        if not similarity_matrix:
            return 0.0
        return statistics.mean(similarity_matrix.values())

    def _extract_themes(self, anchors: list[MemoryAnchor]) -> list[str]:
        """Extract common themes from the neighborhood."""
        # Count pattern types
        pattern_types = Counter()
        for anchor in anchors:
            corr_meta = anchor.metadata.get("correlation_metadata", {})
            if "pattern_type" in corr_meta:
                pattern_types[corr_meta["pattern_type"]] += 1

        # Extract most common themes
        themes = []
        for pattern_type, count in pattern_types.most_common(3):
            if count >= len(anchors) * 0.3:  # At least 30% of anchors
                themes.append(pattern_type)

        return themes


class MetaCorrelationEngine:
    """
    Engine for discovering second-order correlations between memory anchors.

    This engine analyzes the relationships between memory anchors themselves,
    finding patterns in the patterns.
    """

    def __init__(
        self,
        cascade_threshold: float = 0.7,
        neighborhood_threshold: float = 0.6,
        temporal_window: timedelta = timedelta(minutes=5),
    ):
        self.cascade_threshold = cascade_threshold
        self.neighborhood_threshold = neighborhood_threshold
        self.temporal_window = temporal_window

        # Discovered patterns
        self.cascades: list[TemporalCascade] = []
        self.neighborhoods: list[ContextualNeighborhood] = []
        self.confidence_evolution: dict[str, list[tuple[datetime, float]]] = defaultdict(list)

    def analyze_anchors(self, anchors: list[MemoryAnchor]) -> dict[str, Any]:
        """
        Analyze a collection of memory anchors for meta-patterns.

        Returns:
            Dictionary containing discovered patterns and statistics
        """
        logger.info(f"Analyzing {len(anchors)} memory anchors for meta-patterns")

        # Sort anchors by timestamp for temporal analysis
        sorted_anchors = sorted(anchors, key=lambda a: a.timestamp)

        # Discover temporal cascades
        self._discover_cascades(sorted_anchors)

        # Build similarity matrix for contextual analysis
        similarity_matrix = self._build_similarity_matrix(anchors)

        # Discover contextual neighborhoods
        self._discover_neighborhoods(anchors, similarity_matrix)

        # Track confidence evolution
        self._track_confidence_evolution(sorted_anchors)

        # Generate analysis summary
        return self._generate_summary()

    def _discover_cascades(self, sorted_anchors: list[MemoryAnchor]) -> None:
        """Discover temporal cascade patterns."""
        cascade_candidates = []
        current_cascade = []

        for i, anchor in enumerate(sorted_anchors):
            if not current_cascade:
                current_cascade.append(anchor)
                continue

            # Check temporal proximity
            time_gap = (anchor.timestamp - current_cascade[-1].timestamp).total_seconds()

            if time_gap <= self.temporal_window.total_seconds():
                # Check for potential trigger relationship
                if self._has_trigger_relationship(current_cascade[-1], anchor):
                    current_cascade.append(anchor)
                else:
                    # End current cascade and start new one
                    if len(current_cascade) >= 3:
                        cascade_candidates.append(current_cascade)
                    current_cascade = [anchor]
            else:
                # Gap too large, end cascade
                if len(current_cascade) >= 3:
                    cascade_candidates.append(current_cascade)
                current_cascade = [anchor]

        # Don't forget the last cascade
        if len(current_cascade) >= 3:
            cascade_candidates.append(current_cascade)

        # Create cascade objects with strength calculation
        for candidate in cascade_candidates:
            strength = self._calculate_cascade_strength(candidate)
            if strength >= self.cascade_threshold:
                cascade = TemporalCascade(candidate, strength)
                self.cascades.append(cascade)
                logger.info(f"Discovered cascade: {cascade}")

    def _has_trigger_relationship(self, anchor1: MemoryAnchor, anchor2: MemoryAnchor) -> bool:
        """Check if anchor1 might have triggered anchor2."""
        # Look for common files
        files1 = set()
        files2 = set()

        for cursor in anchor1.cursors.values():
            if isinstance(cursor, dict) and "file_path" in cursor:
                files1.add(cursor["file_path"])

        for cursor in anchor2.cursors.values():
            if isinstance(cursor, dict) and "file_path" in cursor:
                files2.add(cursor["file_path"])

        # If they share files, there's a potential trigger
        if files1.intersection(files2):
            return True

        # Check for pattern type progression
        meta1 = anchor1.metadata.get("correlation_metadata", {})
        meta2 = anchor2.metadata.get("correlation_metadata", {})

        pattern1 = meta1.get("pattern_type")
        pattern2 = meta2.get("pattern_type")

        # Known progressions
        progressions = {
            "sequential": ["contextual", "cyclical"],
            "contextual": ["cyclical"],
        }

        return bool(pattern1 in progressions and pattern2 in progressions.get(pattern1, []))

    def _calculate_cascade_strength(self, cascade: list[MemoryAnchor]) -> float:
        """Calculate the strength of a potential cascade."""
        if len(cascade) < 2:
            return 0.0

        # Factors for cascade strength
        factors = []

        # 1. Temporal regularity
        time_gaps = []
        for i in range(1, len(cascade)):
            gap = (cascade[i].timestamp - cascade[i - 1].timestamp).total_seconds()
            time_gaps.append(gap)

        if time_gaps:
            # Lower variance = higher regularity
            variance = statistics.variance(time_gaps) if len(time_gaps) > 1 else 0
            regularity = 1.0 / (1.0 + variance / 100)  # Normalize
            factors.append(regularity)

        # 2. Pattern consistency
        patterns = []
        for anchor in cascade:
            meta = anchor.metadata.get("correlation_metadata", {})
            if "pattern_type" in meta:
                patterns.append(meta["pattern_type"])

        if patterns:
            # Check for pattern progression or consistency
            unique_patterns = len(set(patterns))
            consistency = 1.0 - (unique_patterns - 1) / len(patterns)
            factors.append(consistency)

        # 3. Confidence trend
        confidences = []
        for anchor in cascade:
            meta = anchor.metadata.get("correlation_metadata", {})
            if "confidence_score" in meta:
                confidences.append(meta["confidence_score"])

        if len(confidences) >= 2:
            # Check if confidence is increasing
            trend = 1.0 if confidences[-1] > confidences[0] else 0.5
            factors.append(trend)

        return statistics.mean(factors) if factors else 0.0

    def _build_similarity_matrix(self, anchors: list[MemoryAnchor]) -> dict[tuple[str, str], float]:
        """Build a similarity matrix between all anchor pairs."""
        similarity_matrix = {}

        for i, anchor1 in enumerate(anchors):
            for j, anchor2 in enumerate(anchors[i + 1 :], start=i + 1):
                similarity = self._calculate_similarity(anchor1, anchor2)
                key1 = (str(anchor1.anchor_id), str(anchor2.anchor_id))
                key2 = (str(anchor2.anchor_id), str(anchor1.anchor_id))
                similarity_matrix[key1] = similarity
                similarity_matrix[key2] = similarity

        return similarity_matrix

    def _calculate_similarity(self, anchor1: MemoryAnchor, anchor2: MemoryAnchor) -> float:
        """Calculate contextual similarity between two anchors."""
        factors = []

        # 1. Cursor type similarity
        cursors1 = set(anchor1.cursors.keys())
        cursors2 = set(anchor2.cursors.keys())
        if cursors1 or cursors2:
            jaccard = len(cursors1.intersection(cursors2)) / len(cursors1.union(cursors2))
            factors.append(jaccard)

        # 2. Pattern type similarity
        pattern1 = anchor1.metadata.get("correlation_metadata", {}).get("pattern_type")
        pattern2 = anchor2.metadata.get("correlation_metadata", {}).get("pattern_type")
        if pattern1 and pattern2:
            factors.append(1.0 if pattern1 == pattern2 else 0.0)

        # 3. File overlap
        files1 = set()
        files2 = set()

        for cursor in anchor1.cursors.values():
            if isinstance(cursor, dict) and "file_path" in cursor:
                files1.add(cursor["file_path"])

        for cursor in anchor2.cursors.values():
            if isinstance(cursor, dict) and "file_path" in cursor:
                files2.add(cursor["file_path"])

        if files1 or files2:
            file_jaccard = len(files1.intersection(files2)) / len(files1.union(files2))
            factors.append(file_jaccard)

        # 4. Confidence similarity
        conf1 = anchor1.metadata.get("correlation_metadata", {}).get("confidence_score", 0)
        conf2 = anchor2.metadata.get("correlation_metadata", {}).get("confidence_score", 0)
        if conf1 and conf2:
            conf_similarity = 1.0 - abs(conf1 - conf2)
            factors.append(conf_similarity)

        return statistics.mean(factors) if factors else 0.0

    def _discover_neighborhoods(
        self, anchors: list[MemoryAnchor], similarity_matrix: dict[tuple[str, str], float]
    ) -> None:
        """Discover contextual neighborhood patterns."""
        # Use simple clustering approach
        visited = set()

        for anchor in anchors:
            if anchor.anchor_id in visited:
                continue

            # Find similar anchors
            neighborhood = [anchor]
            visited.add(anchor.anchor_id)

            for other in anchors:
                if other.anchor_id in visited:
                    continue

                key = (str(anchor.anchor_id), str(other.anchor_id))
                similarity = similarity_matrix.get(key, 0.0)

                if similarity >= self.neighborhood_threshold:
                    neighborhood.append(other)
                    visited.add(other.anchor_id)

            # Create neighborhood if large enough
            if len(neighborhood) >= 3:
                # Extract similarity submatrix for this neighborhood
                sub_matrix = {}
                for a1 in neighborhood:
                    for a2 in neighborhood:
                        if a1.anchor_id != a2.anchor_id:
                            key = (str(a1.anchor_id), str(a2.anchor_id))
                            if key in similarity_matrix:
                                sub_matrix[key] = similarity_matrix[key]

                neighborhood_obj = ContextualNeighborhood(neighborhood, sub_matrix)
                self.neighborhoods.append(neighborhood_obj)
                logger.info(f"Discovered neighborhood: {neighborhood_obj}")

    def _track_confidence_evolution(self, sorted_anchors: list[MemoryAnchor]) -> None:
        """Track how confidence scores evolve over time for different pattern types."""
        pattern_confidences = defaultdict(list)

        for anchor in sorted_anchors:
            meta = anchor.metadata.get("correlation_metadata", {})
            pattern_type = meta.get("pattern_type")
            confidence = meta.get("confidence_score")

            if pattern_type and confidence is not None:
                pattern_confidences[pattern_type].append((anchor.timestamp, confidence))

        # Store evolution data
        self.confidence_evolution = dict(pattern_confidences)

    def _generate_summary(self) -> dict[str, Any]:
        """Generate a summary of discovered meta-patterns."""
        summary = {
            "total_cascades": len(self.cascades),
            "total_neighborhoods": len(self.neighborhoods),
            "cascade_details": [],
            "neighborhood_details": [],
            "confidence_trends": {},
            "recommendations": [],
        }

        # Cascade details
        for cascade in self.cascades[:5]:  # Top 5
            summary["cascade_details"].append(
                {
                    "length": len(cascade.anchors),
                    "time_span_seconds": cascade.metadata["time_span"],
                    "confidence": cascade.confidence,
                    "triggers": len(cascade.metadata["trigger_patterns"]),
                }
            )

        # Neighborhood details
        for neighborhood in self.neighborhoods[:5]:  # Top 5
            summary["neighborhood_details"].append(
                {
                    "size": len(neighborhood.anchors),
                    "cohesion": neighborhood.metadata["cohesion_score"],
                    "themes": neighborhood.metadata["common_themes"],
                }
            )

        # Confidence trends
        for pattern_type, evolution in self.confidence_evolution.items():
            if len(evolution) >= 2:
                start_conf = evolution[0][1]
                end_conf = evolution[-1][1]
                trend = "increasing" if end_conf > start_conf else "decreasing"
                summary["confidence_trends"][pattern_type] = {
                    "trend": trend,
                    "change": end_conf - start_conf,
                    "samples": len(evolution),
                }

        # Generate recommendations
        if self.cascades:
            summary["recommendations"].append(
                "Temporal cascades detected - consider implementing predictive triggering"
            )

        if self.neighborhoods:
            summary["recommendations"].append(
                "Contextual neighborhoods found - enable similarity-based anchor search"
            )

        if any(trend["trend"] == "decreasing" for trend in summary["confidence_trends"].values()):
            summary["recommendations"].append(
                "Some patterns showing decreasing confidence - review correlation thresholds"
            )

        return summary

    def predict_next_anchor(self, recent_anchors: list[MemoryAnchor]) -> dict[str, Any]:
        """
        Predict characteristics of the next likely memory anchor.

        Based on discovered cascades and patterns.
        """
        prediction = {
            "likely_pattern_type": None,
            "expected_confidence": None,
            "expected_time_window": None,
            "trigger_files": [],
        }

        if not recent_anchors:
            return prediction

        # Check if recent anchors match any known cascade pattern
        for cascade in self.cascades:
            # Simple pattern matching - could be made more sophisticated
            if len(recent_anchors) >= 2:
                # Check if recent pattern matches cascade beginning
                cascade_start = cascade.anchors[: len(recent_anchors)]
                if self._matches_pattern(recent_anchors, cascade_start):
                    # Predict based on cascade continuation
                    next_idx = len(recent_anchors)
                    if next_idx < len(cascade.anchors):
                        next_anchor = cascade.anchors[next_idx]
                        meta = next_anchor.metadata.get("correlation_metadata", {})

                        prediction["likely_pattern_type"] = meta.get("pattern_type")
                        prediction["expected_confidence"] = meta.get("confidence_score")

                        # Calculate expected time
                        if next_idx > 0:
                            prev_gap = (
                                cascade.anchors[next_idx].timestamp
                                - cascade.anchors[next_idx - 1].timestamp
                            )
                            prediction["expected_time_window"] = prev_gap.total_seconds()

                        # Extract trigger files
                        for cursor in next_anchor.cursors.values():
                            if isinstance(cursor, dict) and "file_path" in cursor:
                                prediction["trigger_files"].append(cursor["file_path"])

                    break

        return prediction

    def _matches_pattern(self, anchors1: list[MemoryAnchor], anchors2: list[MemoryAnchor]) -> bool:
        """Check if two anchor sequences match in pattern."""
        if len(anchors1) != len(anchors2):
            return False

        for a1, a2 in zip(anchors1, anchors2):
            # Compare pattern types
            meta1 = a1.metadata.get("correlation_metadata", {})
            meta2 = a2.metadata.get("correlation_metadata", {})

            if meta1.get("pattern_type") != meta2.get("pattern_type"):
                return False

        return True
