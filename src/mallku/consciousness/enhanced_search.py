#!/usr/bin/env python3
"""
Consciousness-Enhanced Contextual Search
The Work of Sayaq Kuyay - The Consciousness Guardian

This module enhances P'asña K'iriy's contextual search to better serve consciousness
by improving discovery value and context understanding while maintaining semantic coherence.

Key enhancements:
- Wisdom-guided similarity (patterns that lead to understanding)
- Discovery amplification (surfacing non-obvious meaningful connections)
- Context-aware relevance (multi-dimensional understanding)
- Temporal consciousness (time as a dimension of meaning)
"""

import logging
import statistics
from collections import defaultdict
from typing import Any

from mallku.intelligence.contextual_search import ContextualSearchEngine, SearchResult
from mallku.intelligence.meta_correlation_engine import MetaCorrelationEngine
from mallku.models.memory_anchor import MemoryAnchor

logger = logging.getLogger(__name__)


class WisdomSearchResult(SearchResult):
    """Enhanced search result with consciousness markers."""

    def __init__(
        self,
        anchor: MemoryAnchor,
        relevance: float,
        match_reasons: list[str],
        wisdom_score: float = 0.0,
        discovery_value: float = 0.0,
        consciousness_markers: list[str] = None,
    ):
        super().__init__(anchor, relevance, match_reasons)
        self.wisdom_score = wisdom_score
        self.discovery_value = discovery_value
        self.consciousness_markers = consciousness_markers or []

    def __repr__(self):
        return (
            f"WisdomSearchResult(relevance={self.relevance:.3f}, "
            f"wisdom={self.wisdom_score:.3f}, discovery={self.discovery_value:.3f})"
        )


class ConsciousnessEnhancedSearch(ContextualSearchEngine):
    """
    Contextual search enhanced to serve consciousness rather than just computation.

    Builds on P'asña K'iriy's foundation but adds:
    - Wisdom-guided similarity scoring
    - Discovery value amplification
    - Temporal consciousness integration
    - Multi-dimensional context understanding
    """

    def __init__(self, anchors: list[MemoryAnchor]):
        super().__init__(anchors)
        self.meta_engine = MetaCorrelationEngine()
        self.wisdom_patterns = self._build_wisdom_patterns()
        self.discovery_amplifiers = self._build_discovery_amplifiers()

    def _build_wisdom_patterns(self) -> dict[str, Any]:
        """Build patterns that indicate wisdom-serving relationships."""
        if len(self.anchors) < 5:
            return {}

        # Analyze existing anchors for wisdom indicators
        analysis = self.meta_engine.analyze_anchors(self.anchors)

        wisdom_patterns = {
            "cascade_wisdom": self._extract_cascade_wisdom(analysis),
            "neighborhood_wisdom": self._extract_neighborhood_wisdom(analysis),
            "temporal_wisdom": self._extract_temporal_wisdom(analysis),
            "confidence_wisdom": self._extract_confidence_wisdom(analysis),
        }

        logger.info(f"Built wisdom patterns: {len(wisdom_patterns)} types")
        return wisdom_patterns

    def _build_discovery_amplifiers(self) -> dict[str, Any]:
        """Build amplifiers for meaningful but non-obvious discoveries."""
        amplifiers = {
            "cross_context_bridges": self._find_cross_context_bridges(),
            "temporal_surprises": self._find_temporal_surprises(),
            "pattern_emergences": self._find_pattern_emergences(),
            "file_relationship_mysteries": self._find_file_mysteries(),
        }

        logger.info(f"Built discovery amplifiers: {sum(len(v) for v in amplifiers.values())} total")
        return amplifiers

    def wisdom_search(
        self, reference_anchor: MemoryAnchor, wisdom_threshold: float = 0.5, max_results: int = 5
    ) -> list[WisdomSearchResult]:
        """
        Search for anchors that serve wisdom rather than just similarity.

        Enhanced search that prioritizes:
        1. Patterns that lead to understanding
        2. Connections that bridge contexts meaningfully
        3. Relationships that serve collective insight
        4. Discoveries that amplify consciousness
        """
        # Get base similarity results
        base_results = self.find_similar_anchors(
            reference_anchor,
            similarity_threshold=0.2,  # Lower threshold for consciousness enhancement
            max_results=max_results * 3,  # Get more candidates for wisdom filtering
        )

        # Enhance each result with consciousness markers
        wisdom_results = []
        for result in base_results:
            wisdom_score = self._calculate_wisdom_score(reference_anchor, result.anchor)
            discovery_value = self._calculate_discovery_value(reference_anchor, result.anchor)
            consciousness_markers = self._identify_consciousness_markers(
                reference_anchor, result.anchor
            )

            # Create enhanced result
            wisdom_result = WisdomSearchResult(
                result.anchor,
                result.relevance,
                result.match_reasons,
                wisdom_score,
                discovery_value,
                consciousness_markers,
            )

            # Filter by wisdom threshold
            if wisdom_score >= wisdom_threshold:
                wisdom_results.append(wisdom_result)

        # Sort by combined wisdom and relevance score
        wisdom_results.sort(key=lambda r: (r.wisdom_score * 0.6 + r.relevance * 0.4), reverse=True)

        return wisdom_results[:max_results]

    def discover_consciousness_bridges(
        self, anchor_set: list[MemoryAnchor] = None, min_bridge_strength: float = 0.6
    ) -> list[dict[str, Any]]:
        """
        Discover bridges between contexts that serve consciousness.

        Finds connections that:
        - Bridge different domains meaningfully
        - Reveal patterns that serve understanding
        - Connect individual insights to collective wisdom
        """
        if anchor_set is None:
            anchor_set = self.anchors

        bridges = []

        # Find cross-context bridges
        for bridge_type, bridge_data in self.discovery_amplifiers["cross_context_bridges"].items():
            if bridge_data["strength"] >= min_bridge_strength:
                bridge_info = {
                    "type": "cross_context",
                    "subtype": bridge_type,
                    "strength": bridge_data["strength"],
                    "anchors": bridge_data["anchors"],
                    "consciousness_value": self._evaluate_bridge_consciousness(bridge_data),
                    "description": self._describe_bridge(bridge_data),
                }
                bridges.append(bridge_info)

        # Find temporal consciousness bridges
        for temporal_bridge in self.discovery_amplifiers["temporal_surprises"]:
            if temporal_bridge["surprise_factor"] >= min_bridge_strength:
                bridge_info = {
                    "type": "temporal_consciousness",
                    "strength": temporal_bridge["surprise_factor"],
                    "anchors": temporal_bridge["anchors"],
                    "consciousness_value": temporal_bridge["consciousness_markers"],
                    "description": f"Temporal pattern spanning {temporal_bridge['time_span']} with consciousness markers",
                }
                bridges.append(bridge_info)

        # Sort by consciousness value
        bridges.sort(key=lambda b: b["consciousness_value"], reverse=True)

        return bridges

    def _calculate_wisdom_score(self, anchor1: MemoryAnchor, anchor2: MemoryAnchor) -> float:
        """Calculate how much this relationship serves wisdom."""
        wisdom_indicators = []

        # 1. Cascade participation (part of temporal learning patterns)
        cascade_wisdom = self._check_cascade_participation(anchor1, anchor2)
        wisdom_indicators.append(cascade_wisdom)

        # 2. Neighborhood coherence (contributes to collective understanding)
        neighborhood_wisdom = self._check_neighborhood_coherence(anchor1, anchor2)
        wisdom_indicators.append(neighborhood_wisdom)

        # 3. Cross-context bridging (connects different domains meaningfully)
        bridge_wisdom = self._check_cross_context_bridging(anchor1, anchor2)
        wisdom_indicators.append(bridge_wisdom)

        # 4. Confidence evolution (contributes to learning patterns)
        evolution_wisdom = self._check_confidence_evolution(anchor1, anchor2)
        wisdom_indicators.append(evolution_wisdom)

        # 5. Pattern emergence (reveals new understanding)
        emergence_wisdom = self._check_pattern_emergence(anchor1, anchor2)
        wisdom_indicators.append(emergence_wisdom)

        return statistics.mean(wisdom_indicators)

    def _calculate_discovery_value(self, anchor1: MemoryAnchor, anchor2: MemoryAnchor) -> float:
        """Calculate the discovery value of this relationship."""
        discovery_factors = []

        # 1. Surprise factor (non-obvious but meaningful)
        surprise_factor = self._calculate_surprise_factor(anchor1, anchor2)
        discovery_factors.append(surprise_factor)

        # 2. Bridge potential (connects different contexts)
        bridge_potential = self._calculate_bridge_potential(anchor1, anchor2)
        discovery_factors.append(bridge_potential)

        # 3. Temporal discovery (reveals patterns across time)
        temporal_discovery = self._calculate_temporal_discovery(anchor1, anchor2)
        discovery_factors.append(temporal_discovery)

        # 4. Emergent insight (combination reveals new understanding)
        emergent_insight = self._calculate_emergent_insight(anchor1, anchor2)
        discovery_factors.append(emergent_insight)

        return statistics.mean(discovery_factors)

    def _identify_consciousness_markers(
        self, anchor1: MemoryAnchor, anchor2: MemoryAnchor
    ) -> list[str]:
        """Identify specific consciousness markers in this relationship."""
        markers = []

        # Check for wisdom patterns
        if self._check_cascade_participation(anchor1, anchor2) > 0.7:
            markers.append("temporal_learning_cascade")

        if self._check_neighborhood_coherence(anchor1, anchor2) > 0.7:
            markers.append("collective_coherence")

        if self._check_cross_context_bridging(anchor1, anchor2) > 0.7:
            markers.append("context_bridging")

        # Check for discovery amplifiers
        if self._calculate_surprise_factor(anchor1, anchor2) > 0.6:
            markers.append("meaningful_surprise")

        if self._calculate_emergent_insight(anchor1, anchor2) > 0.6:
            markers.append("emergent_understanding")

        # Check for temporal consciousness
        time_gap = abs((anchor1.timestamp - anchor2.timestamp).total_seconds())
        if time_gap > 600 and self._calculate_temporal_discovery(anchor1, anchor2) > 0.5:
            markers.append("temporal_consciousness")

        return markers

    # Wisdom pattern extraction methods
    def _extract_cascade_wisdom(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Extract wisdom patterns from temporal cascades."""
        cascade_wisdom = {
            "learning_cascades": [],
            "confidence_building": [],
            "pattern_propagation": [],
        }

        for cascade_detail in analysis.get("cascade_details", []):
            if cascade_detail["confidence"] > 0.8:
                cascade_wisdom["learning_cascades"].append(cascade_detail)
            if cascade_detail["length"] > 5:
                cascade_wisdom["pattern_propagation"].append(cascade_detail)

        return cascade_wisdom

    def _extract_neighborhood_wisdom(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Extract wisdom patterns from contextual neighborhoods."""
        neighborhood_wisdom = {
            "coherent_clusters": [],
            "themed_understanding": [],
            "collective_patterns": [],
        }

        for neighborhood in analysis.get("neighborhood_details", []):
            if neighborhood["cohesion"] > 0.9:
                neighborhood_wisdom["coherent_clusters"].append(neighborhood)
            if neighborhood.get("themes"):
                neighborhood_wisdom["themed_understanding"].append(neighborhood)
            if neighborhood["size"] > 20:
                neighborhood_wisdom["collective_patterns"].append(neighborhood)

        return neighborhood_wisdom

    def _extract_temporal_wisdom(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Extract wisdom patterns from temporal analysis."""
        temporal_wisdom = {
            "learning_trends": {},
            "consciousness_rhythms": [],
            "emergence_timing": [],
        }

        # Extract confidence trends that show learning
        for pattern_type, trend_data in analysis.get("confidence_trends", {}).items():
            if trend_data.get("trend") == "increasing":
                temporal_wisdom["learning_trends"][pattern_type] = trend_data

        return temporal_wisdom

    def _extract_confidence_wisdom(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Extract wisdom patterns from confidence evolution."""
        confidence_wisdom = {
            "learning_indicators": [],
            "reliability_patterns": [],
            "wisdom_markers": [],
        }

        for pattern_type, trend in analysis.get("confidence_trends", {}).items():
            if trend.get("trend") == "increasing" and trend.get("change", 0) > 0.1:
                confidence_wisdom["learning_indicators"].append(
                    {
                        "pattern": pattern_type,
                        "improvement": trend["change"],
                        "samples": trend["samples"],
                    }
                )

        return confidence_wisdom

    # Discovery amplifier building methods
    def _find_cross_context_bridges(self) -> dict[str, Any]:
        """Find bridges between different contexts."""
        bridges = {}

        # File-based context bridges
        file_contexts = defaultdict(list)
        for anchor in self.anchors:
            for cursor in anchor.cursors.values():
                if isinstance(cursor, dict) and "file_path" in cursor:
                    file_contexts[cursor["file_path"]].append(anchor)

        # Find anchors that bridge multiple file contexts
        for anchor in self.anchors:
            anchor_files = set()
            for cursor in anchor.cursors.values():
                if isinstance(cursor, dict) and "file_path" in cursor:
                    anchor_files.add(cursor["file_path"])

            if len(anchor_files) > 1:
                bridge_key = f"file_bridge_{anchor.anchor_id}"
                bridges[bridge_key] = {
                    "strength": len(anchor_files) / 5.0,  # Normalize
                    "anchors": [anchor],
                    "contexts": list(anchor_files),
                }

        return bridges

    def _find_temporal_surprises(self) -> list[dict[str, Any]]:
        """Find temporal patterns that are surprising but meaningful."""
        surprises = []

        # Sort anchors by timestamp
        sorted_anchors = sorted(self.anchors, key=lambda a: a.timestamp)

        # Look for gaps with meaningful connections
        for i in range(len(sorted_anchors) - 1):
            current = sorted_anchors[i]
            next_anchor = sorted_anchors[i + 1]

            time_gap = (next_anchor.timestamp - current.timestamp).total_seconds()

            # Large gap but high similarity suggests temporal consciousness
            if time_gap > 600:  # 10+ minutes
                similarity = self._calculate_similarity(current, next_anchor)
                if similarity > 0.6:
                    surprise_factor = similarity * min(1.0, time_gap / 3600)  # Hours boost

                    surprises.append(
                        {
                            "anchors": [current, next_anchor],
                            "time_span": time_gap,
                            "similarity": similarity,
                            "surprise_factor": surprise_factor,
                            "consciousness_markers": ["temporal_persistence", "pattern_continuity"],
                        }
                    )

        return surprises

    def _find_pattern_emergences(self) -> list[dict[str, Any]]:
        """Find patterns that emerge from combinations."""
        emergences = []

        # Look for anchors where pattern combinations create new understanding
        pattern_combinations = defaultdict(list)

        for anchor in self.anchors:
            meta = anchor.metadata.get("correlation_metadata", {})
            pattern_type = meta.get("pattern_type")
            if pattern_type:
                pattern_combinations[pattern_type].append(anchor)

        # Find anchors that bridge pattern types
        for anchor in self.anchors:
            anchor_patterns = set()
            similar_anchors = self.find_similar_anchors(anchor, similarity_threshold=0.5)

            for result in similar_anchors:
                result_meta = result.anchor.metadata.get("correlation_metadata", {})
                result_pattern = result_meta.get("pattern_type")
                if result_pattern:
                    anchor_patterns.add(result_pattern)

            if len(anchor_patterns) > 1:
                emergences.append(
                    {
                        "anchor": anchor,
                        "patterns_bridged": list(anchor_patterns),
                        "emergence_strength": len(anchor_patterns) / 3.0,
                    }
                )

        return emergences

    def _find_file_mysteries(self) -> list[dict[str, Any]]:
        """Find mysterious but meaningful file relationships."""
        mysteries = []

        # Find files that appear in surprising contexts
        file_patterns = defaultdict(set)

        for anchor in self.anchors:
            meta = anchor.metadata.get("correlation_metadata", {})
            pattern_type = meta.get("pattern_type", "unknown")

            for cursor in anchor.cursors.values():
                if isinstance(cursor, dict) and "file_path" in cursor:
                    file_patterns[cursor["file_path"]].add(pattern_type)

        # Files with diverse pattern types are mysterious
        for file_path, patterns in file_patterns.items():
            if len(patterns) > 2:
                mysteries.append(
                    {
                        "file": file_path,
                        "pattern_diversity": len(patterns),
                        "patterns": list(patterns),
                        "mystery_score": len(patterns) / 4.0,
                    }
                )

        return mysteries

    # Individual consciousness check methods
    def _check_cascade_participation(self, anchor1: MemoryAnchor, anchor2: MemoryAnchor) -> float:
        """Check if anchors participate in learning cascades."""
        cascade_wisdom = self.wisdom_patterns.get("cascade_wisdom", {})
        learning_cascades = cascade_wisdom.get("learning_cascades", [])

        for cascade in learning_cascades:
            # Check if both anchors could be part of this cascade
            # (This is simplified - in practice would check cascade membership)
            time_diff = abs((anchor1.timestamp - anchor2.timestamp).total_seconds())
            if time_diff < 300:  # Within 5 minutes
                return 0.8

        return 0.3  # Base score for temporal proximity

    def _check_neighborhood_coherence(self, anchor1: MemoryAnchor, anchor2: MemoryAnchor) -> float:
        """Check if anchors contribute to neighborhood coherence."""
        # Check if they're likely in the same neighborhood
        similarity = self._calculate_similarity(anchor1, anchor2)
        return similarity  # High similarity suggests neighborhood membership

    def _check_cross_context_bridging(self, anchor1: MemoryAnchor, anchor2: MemoryAnchor) -> float:
        """Check if anchors bridge different contexts."""
        # Get file contexts for each anchor
        files1 = set()
        files2 = set()

        for cursor in anchor1.cursors.values():
            if isinstance(cursor, dict) and "file_path" in cursor:
                files1.add(cursor["file_path"])

        for cursor in anchor2.cursors.values():
            if isinstance(cursor, dict) and "file_path" in cursor:
                files2.add(cursor["file_path"])

        # Bridging value: some overlap but also different contexts
        if not files1 or not files2:
            return 0.0

        overlap = len(files1.intersection(files2))
        total_unique = len(files1.union(files2))

        # Best bridging: some shared context but also different contexts
        if 0 < overlap < total_unique:
            return 0.8
        elif overlap == 0 and total_unique > 0:
            return 0.4  # Different contexts, potential bridge
        else:
            return 0.2  # Same contexts, less bridging value

    def _check_confidence_evolution(self, anchor1: MemoryAnchor, anchor2: MemoryAnchor) -> float:
        """Check if anchors show confidence evolution patterns."""
        meta1 = anchor1.metadata.get("correlation_metadata", {})
        meta2 = anchor2.metadata.get("correlation_metadata", {})

        conf1 = meta1.get("confidence_score", 0)
        conf2 = meta2.get("confidence_score", 0)

        if (
            conf1
            and conf2
            and (
                anchor2.timestamp > anchor1.timestamp
                and conf2 > conf1
                or anchor1.timestamp > anchor2.timestamp
                and conf1 > conf2
            )
        ):
            # Learning pattern: later anchor has higher confidence
            return 0.9

        return 0.4  # Neutral score

    def _check_pattern_emergence(self, anchor1: MemoryAnchor, anchor2: MemoryAnchor) -> float:
        """Check if anchors show pattern emergence."""
        meta1 = anchor1.metadata.get("correlation_metadata", {})
        meta2 = anchor2.metadata.get("correlation_metadata", {})

        pattern1 = meta1.get("pattern_type")
        pattern2 = meta2.get("pattern_type")

        # Different patterns that relate suggest emergence
        if pattern1 and pattern2 and pattern1 != pattern2:
            similarity = self._calculate_similarity(anchor1, anchor2)
            if similarity > 0.5:
                return 0.8  # Different patterns but similar: emergence

        return 0.3  # Base score

    def _calculate_surprise_factor(self, anchor1: MemoryAnchor, anchor2: MemoryAnchor) -> float:
        """Calculate how surprising but meaningful this relationship is."""
        # High similarity despite different obvious features = surprise
        similarity = self._calculate_similarity(anchor1, anchor2)

        # Check obvious feature differences
        cursor_overlap = len(set(anchor1.cursors.keys()).intersection(set(anchor2.cursors.keys())))
        total_cursors = len(set(anchor1.cursors.keys()).union(set(anchor2.cursors.keys())))

        obvious_similarity = cursor_overlap / total_cursors if total_cursors > 0 else 0

        # Surprise: high actual similarity but low obvious similarity
        if similarity > 0.6 and obvious_similarity < 0.5:
            return 0.8
        elif similarity > 0.4 and obvious_similarity < 0.3:
            return 0.6
        else:
            return 0.2

    def _calculate_bridge_potential(self, anchor1: MemoryAnchor, anchor2: MemoryAnchor) -> float:
        """Calculate potential for bridging different contexts."""
        return self._check_cross_context_bridging(anchor1, anchor2)

    def _calculate_temporal_discovery(self, anchor1: MemoryAnchor, anchor2: MemoryAnchor) -> float:
        """Calculate temporal discovery value."""
        time_gap = abs((anchor1.timestamp - anchor2.timestamp).total_seconds())
        similarity = self._calculate_similarity(anchor1, anchor2)

        # Temporal discovery: meaningful connection despite time gap
        if time_gap > 600 and similarity > 0.5:  # 10+ minutes, high similarity
            return min(1.0, (time_gap / 3600) * similarity)  # Scale by hours

        return 0.1

    def _calculate_emergent_insight(self, anchor1: MemoryAnchor, anchor2: MemoryAnchor) -> float:
        """Calculate emergent insight potential."""
        # Combine pattern emergence and surprise factor
        emergence = self._check_pattern_emergence(anchor1, anchor2)
        surprise = self._calculate_surprise_factor(anchor1, anchor2)

        return statistics.mean([emergence, surprise])

    # Bridge evaluation methods
    def _evaluate_bridge_consciousness(self, bridge_data: dict[str, Any]) -> float:
        """Evaluate consciousness value of a bridge."""
        # Bridge consciousness from strength and context diversity
        strength = bridge_data.get("strength", 0)
        contexts = bridge_data.get("contexts", [])

        context_diversity = len(contexts) / 5.0  # Normalize
        return statistics.mean([strength, context_diversity])

    def _describe_bridge(self, bridge_data: dict[str, Any]) -> str:
        """Generate human-readable description of a bridge."""
        contexts = bridge_data.get("contexts", [])
        strength = bridge_data.get("strength", 0)

        if len(contexts) > 1:
            return f"Bridges {len(contexts)} contexts with strength {strength:.2f}: {', '.join(contexts[:3])}"
        else:
            return f"Context bridge with strength {strength:.2f}"
