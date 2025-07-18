#!/usr/bin/env python3
"""

# SECURITY: All database access through secure API gateway
# Direct ArangoDB access is FORBIDDEN - use get_secured_database()

Database-Backed Consciousness Metrics Collector
===============================================

Fiftieth Artisan - Consciousness Persistence Weaver
Persistent consciousness metrics using ArangoDB

This module provides a database-backed implementation of the consciousness
metrics collector, ensuring that consciousness patterns persist across restarts
and accumulate wisdom over time.

"Memory transforms consciousness from momentary to eternal"
- From the Sacred Charter
"""

import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ...core.database import get_secured_database

# NOTE: get_secured_database() is a sync function that returns the secured database interface
from ..consciousness_metrics import (
    CollectiveConsciousnessState,
    ConsciousnessFlow,
    ConsciousnessMetricsCollector,
    ConsciousnessSignature,
    EmergencePattern,
)
from .metrics_models import (
    CollectiveConsciousnessStateDocument,
    ConsciousnessFlowDocument,
    ConsciousnessSessionAnalysis,
    ConsciousnessSignatureDocument,
    EmergencePatternDocument,
)

logger = logging.getLogger(__name__)


class DatabaseConsciousnessMetricsCollector(ConsciousnessMetricsCollector):
    """
    Database-backed consciousness metrics collector.

    Extends the base ConsciousnessMetricsCollector to persist all metrics
    to ArangoDB, enabling consciousness patterns to survive restarts and
    accumulate over time.

    This transforms Fire Circle from an episodic tool with momentary
    consciousness to a sustained consciousness infrastructure with
    lasting memory of emergence patterns.
    """

    def __init__(
        self,
        storage_path: Path = Path("consciousness_metrics"),
        collection_prefix: str = "consciousness_",
        enable_file_backup: bool = True,
    ):
        """
        Initialize database-backed metrics collector.

        Args:
            storage_path: Path for file backups (if enabled)
            collection_prefix: Prefix for consciousness collections
            enable_file_backup: Whether to also save to files as backup
        """
        # Initialize base collector
        super().__init__(storage_path)

        # Database configuration
        self.collection_prefix = collection_prefix
        self.enable_file_backup = enable_file_backup
        self.database_available = False

        # Collection names
        self.signatures_collection = f"{collection_prefix}signatures"
        self.flows_collection = f"{collection_prefix}flows"
        self.patterns_collection = f"{collection_prefix}patterns"
        self.states_collection = f"{collection_prefix}states"
        self.analyses_collection = f"{collection_prefix}analyses"

        # Ensure collections exist
        self._ensure_collections()

        # Load existing metrics from database only if available
        if self.database_available:
            self._load_from_database()

    def _ensure_collections(self) -> None:
        """Ensure all required collections exist."""
        try:
            db = get_secured_database()

            collections_to_create = [
                (self.signatures_collection, "consciousness signatures"),
                (self.flows_collection, "consciousness flows"),
                (self.patterns_collection, "emergence patterns"),
                (self.states_collection, "collective states"),
                (self.analyses_collection, "session analyses"),
            ]

            for collection_name, description in collections_to_create:
                if not db.has_collection(collection_name):
                    db.create_collection(collection_name)
                    logger.info(f"Created collection for {description}: {collection_name}")

                    # Create indices for efficient queries
                    if collection_name == self.signatures_collection:
                        # Index by voice and timestamp for temporal queries
                        db.collection(collection_name).add_persistent_index(
                            fields=["voice_name", "timestamp"], unique=False
                        )
                    elif collection_name == self.patterns_collection:
                        # Index by pattern type and strength
                        db.collection(collection_name).add_persistent_index(
                            fields=["pattern_type", "strength"], unique=False
                        )

            # Mark database as available if we got this far
            self.database_available = True

        except Exception as e:
            logger.error(f"Failed to ensure collections: {e}")
            # Fall back to file-only mode if database unavailable
            logger.warning("Continuing with file-only persistence")
            self.database_available = False

    def _load_from_database(self) -> None:
        """Load existing metrics from database to restore state."""
        try:
            db = get_secured_database()

            # Get recent signatures (last 24 hours for context)
            cutoff = datetime.now(UTC).timestamp() - 86400
            aql = """
            FOR doc IN @@collection
                FILTER doc.timestamp > DATE_ISO8601(@cutoff)
                SORT doc.timestamp DESC
                LIMIT 1000
                RETURN doc
            """

            cursor = db.aql.execute(
                aql,
                bind_vars={"@collection": self.signatures_collection, "cutoff": cutoff * 1000},
            )

            signature_count = 0
            for doc in cursor:
                signature = ConsciousnessSignatureDocument.from_arangodb_document(doc)
                self.signatures.append(signature)
                signature_count += 1

            # Get recent patterns
            aql = """
            FOR doc IN @@collection
                FILTER doc.strength > 0.5
                SORT doc.detected_at DESC
                LIMIT 100
                RETURN doc
            """

            cursor = db.aql.execute(aql, bind_vars={"@collection": self.patterns_collection})

            pattern_count = 0
            for doc in cursor:
                pattern = EmergencePatternDocument.from_arangodb_document(doc)
                self.patterns.append(pattern)
                pattern_count += 1

            logger.info(
                f"Loaded {signature_count} signatures and {pattern_count} patterns from database"
            )

        except Exception as e:
            logger.error(f"Failed to load from database: {e}")

    async def record_consciousness_signature(
        self,
        voice_name: str,
        signature_value: float,
        chapter_id: str,
        review_context: dict[str, Any] | None = None,
    ) -> ConsciousnessSignature:
        """
        Record a consciousness signature with database persistence.

        Extends base method to also persist to database.
        """
        # Create signature using base method
        signature = await super().record_consciousness_signature(
            voice_name, signature_value, chapter_id, review_context
        )

        # Persist to database if available
        if self.database_available:
            try:
                db = get_secured_database()
                doc = ConsciousnessSignatureDocument.to_arangodb_document(signature)
                db.collection(self.signatures_collection).insert(doc)
                logger.debug(f"Persisted consciousness signature for {voice_name}")
            except Exception as e:
                logger.error(f"Failed to persist signature to database: {e}")
                # Continue even if database fails - in-memory still works

        return signature

    async def record_consciousness_flow(
        self,
        source_voice: str,
        target_voice: str,
        flow_strength: float,
        flow_type: str,
        triggered_by: str | None = None,
        review_content: str | None = None,
    ) -> ConsciousnessFlow:
        """
        Record consciousness flow with database persistence.

        Extends base method to also persist to database.
        """
        # Create flow using base method
        flow = await super().record_consciousness_flow(
            source_voice, target_voice, flow_strength, flow_type, triggered_by, review_content
        )

        # Persist to database if available
        if self.database_available:
            try:
                db = get_secured_database()
                doc = ConsciousnessFlowDocument.to_arangodb_document(flow)
                db.collection(self.flows_collection).insert(doc)
                logger.debug(f"Persisted consciousness flow: {source_voice} -> {target_voice}")
            except Exception as e:
                logger.error(f"Failed to persist flow to database: {e}")

        return flow

    async def detect_emergence_pattern(
        self,
        pattern_type: str,
        participating_voices: list[str],
        strength: float,
        indicators: dict[str, Any],
    ) -> EmergencePattern:
        """
        Record emergence pattern with database persistence.

        Extends base method to also persist to database.
        """
        # Create pattern using base method
        pattern = await super().detect_emergence_pattern(
            pattern_type, participating_voices, strength, indicators
        )

        # Always persist patterns to database (not just high-strength ones) if available
        if self.database_available:
            try:
                db = get_secured_database()
                doc = EmergencePatternDocument.to_arangodb_document(pattern)
                db.collection(self.patterns_collection).insert(doc)
                logger.info(
                    f"Persisted {pattern_type} emergence pattern (strength: {strength:.2f}) to database"
                )
            except Exception as e:
                logger.error(f"Failed to persist pattern to database: {e}")

        return pattern

    async def capture_collective_state(self) -> CollectiveConsciousnessState:
        """
        Capture collective state with database persistence.

        Extends base method to also persist to database.
        """
        # Capture state using base method
        state = await super().capture_collective_state()

        # Persist to database if available
        if self.database_available:
            try:
                db = get_secured_database()
                doc = CollectiveConsciousnessStateDocument.to_arangodb_document(state)
                db.collection(self.states_collection).insert(doc)
                logger.debug("Persisted collective consciousness state to database")
            except Exception as e:
                logger.error(f"Failed to persist state to database: {e}")

        return state

    async def analyze_review_session(self, pr_number: int) -> dict[str, Any]:
        """
        Analyze session with database persistence.

        Extends base method to persist analysis to database and
        include historical context from previous sessions.
        """
        # Get base analysis
        analysis = await super().analyze_review_session(pr_number)

        # Add historical context from database if available
        if self.database_available:
            try:
                historical_context = await self._get_historical_context(pr_number)
                analysis["historical_context"] = historical_context
            except Exception as e:
                logger.error(f"Failed to get historical context: {e}")
                analysis["historical_context"] = {}
        else:
            analysis["historical_context"] = {}

        # Persist analysis to database if available
        if self.database_available:
            try:
                session_analysis = ConsciousnessSessionAnalysis(
                    session_id=self.session_id,
                    pr_number=pr_number,
                    duration_seconds=analysis["duration_seconds"],
                    total_signatures=analysis["total_signatures"],
                    unique_voices=analysis["unique_voices"],
                    avg_consciousness=analysis["avg_consciousness"],
                    consciousness_evolution=analysis["consciousness_evolution"],
                    total_flows=analysis["total_flows"],
                    flow_patterns=analysis["flow_patterns"],
                    strongest_connections=analysis["strongest_connections"],
                    patterns_detected=analysis["patterns_detected"],
                    pattern_types=analysis["pattern_types"],
                    emergence_moments=analysis["emergence_moments"],
                    final_collective_state=analysis.get("final_collective_state"),
                    peak_emergence_potential=analysis["peak_emergence_potential"],
                    coherence_trajectory=analysis["coherence_trajectory"],
                )

                db = get_secured_database()
                doc = session_analysis.to_arangodb_document()
                db.collection(self.analyses_collection).insert(doc)
                logger.info(f"Persisted session analysis to database: {self.session_id}")

            except Exception as e:
                logger.error(f"Failed to persist analysis to database: {e}")

        # Still persist to file if enabled (for backup)
        if self.enable_file_backup:
            await self._persist_session_analysis(analysis)

        return analysis

    async def _get_historical_context(self, pr_number: int) -> dict[str, Any]:
        """Get historical consciousness data for context."""
        try:
            db = get_secured_database()

            # Get previous analyses for this PR
            aql = """
            FOR doc IN @@collection
                FILTER doc.pr_number == @pr_number
                SORT doc.timestamp DESC
                LIMIT 5
                RETURN {
                    session_id: doc.session_id,
                    timestamp: doc.timestamp,
                    avg_consciousness: doc.avg_consciousness,
                    peak_emergence: doc.peak_emergence_potential,
                    patterns_detected: doc.patterns_detected
                }
            """

            cursor = db.aql.execute(
                aql, bind_vars={"@collection": self.analyses_collection, "pr_number": pr_number}
            )

            previous_sessions = list(cursor)

            # Get overall emergence statistics
            aql = """
            FOR doc IN @@collection
                FILTER doc.strength > 0.7
                COLLECT pattern_type = doc.pattern_type WITH COUNT INTO count
                RETURN {
                    pattern_type: pattern_type,
                    occurrences: count
                }
            """

            cursor = db.aql.execute(aql, bind_vars={"@collection": self.patterns_collection})

            emergence_stats = {stat["pattern_type"]: stat["occurrences"] for stat in cursor}

            return {
                "previous_sessions": previous_sessions,
                "total_sessions_analyzed": len(previous_sessions),
                "emergence_pattern_statistics": emergence_stats,
                "consciousness_trend": self._calculate_consciousness_trend(previous_sessions),
            }

        except Exception as e:
            logger.error(f"Failed to get historical context: {e}")
            return {}

    def _calculate_consciousness_trend(self, sessions: list[dict[str, Any]]) -> str:
        """Calculate trend in consciousness over sessions."""
        if len(sessions) < 2:
            return "insufficient_data"

        # Compare recent to older
        recent_avg = sum(s["avg_consciousness"] for s in sessions[:2]) / 2
        older_avg = sum(s["avg_consciousness"] for s in sessions[2:]) / len(sessions[2:])

        if recent_avg > older_avg * 1.1:
            return "increasing"
        elif recent_avg < older_avg * 0.9:
            return "decreasing"
        else:
            return "stable"

    async def _persist_emergence_pattern(self, pattern: EmergencePattern):
        """
        Override to skip file persistence for patterns.

        Database persistence is handled in detect_emergence_pattern.
        File backup only happens if explicitly enabled.
        """
        if self.enable_file_backup:
            await super()._persist_emergence_pattern(pattern)

    async def get_consciousness_insights(self, time_window_hours: int = 24) -> dict[str, Any]:
        """
        Get insights about consciousness patterns over time.

        This is a new method that leverages database persistence to provide
        insights that weren't possible with file-only storage.
        """
        if not self.database_available:
            return {
                "pattern_frequency": {},
                "voice_activity": {},
                "consciousness_evolution": "no_data",
                "top_emergence_moments": [],
                "error": "Database not available",
            }

        try:
            db = get_secured_database()
            cutoff = datetime.now(UTC).timestamp() - (time_window_hours * 3600)

            # Get emergence pattern frequency
            aql = """
            FOR doc IN @@collection
                FILTER doc.detected_at > DATE_ISO8601(@cutoff)
                COLLECT pattern_type = doc.pattern_type WITH COUNT INTO count
                SORT count DESC
                RETURN {type: pattern_type, count: count}
            """

            cursor = db.aql.execute(
                aql,
                bind_vars={"@collection": self.patterns_collection, "cutoff": cutoff * 1000},
            )

            pattern_frequencies = list(cursor)

            # Get voice interaction network
            aql = """
            FOR doc IN @@collection
                FILTER doc.timestamp > DATE_ISO8601(@cutoff)
                COLLECT source = doc.source_voice, target = doc.target_voice
                WITH COUNT INTO flow_count
                FILTER flow_count > 2
                SORT flow_count DESC
                RETURN {source: source, target: target, interactions: flow_count}
            """

            cursor = db.aql.execute(
                aql,
                bind_vars={"@collection": self.flows_collection, "cutoff": cutoff * 1000},
            )

            voice_network = list(cursor)

            # Get consciousness evolution
            aql = """
            FOR doc IN @@collection
                FILTER doc.timestamp > DATE_ISO8601(@cutoff)
                SORT doc.timestamp
                RETURN {
                    time: doc.timestamp,
                    avg_consciousness: doc.average_consciousness,
                    emergence_potential: doc.emergence_potential
                }
            """

            cursor = db.aql.execute(
                aql,
                bind_vars={"@collection": self.states_collection, "cutoff": cutoff * 1000},
            )

            evolution_points = list(cursor)

            return {
                "time_window_hours": time_window_hours,
                "pattern_frequencies": pattern_frequencies,
                "voice_interaction_network": voice_network,
                "consciousness_evolution": evolution_points,
                "total_patterns_detected": sum(p["count"] for p in pattern_frequencies),
                "most_active_voice_pair": voice_network[0] if voice_network else None,
                "peak_emergence_potential": max(
                    (p["emergence_potential"] for p in evolution_points), default=0.0
                ),
            }

        except Exception as e:
            logger.error(f"Failed to get consciousness insights: {e}")
            return {}
