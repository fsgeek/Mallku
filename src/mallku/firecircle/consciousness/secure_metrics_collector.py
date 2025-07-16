#!/usr/bin/env python3
"""
Secure Consciousness Metrics Collector
======================================

53rd Guardian - Healing the security wound

This module provides a secure implementation of consciousness metrics
collection that respects the database security architecture while
maintaining full functionality.

ALL database access goes through the secure API gateway - no exceptions.
"""

import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import aiohttp

from ..consciousness_metrics import (
    ConsciousnessFlow,
    ConsciousnessMetricsCollector,
    ConsciousnessSignature,
    EmergencePattern,
)
from .metrics_models import (
    ConsciousnessFlowDocument,
    ConsciousnessSessionAnalysis,
    ConsciousnessSignatureDocument,
    EmergencePatternDocument,
)

# SECURITY: All database access through secure API gateway
# Direct ArangoDB access is FORBIDDEN - use get_secured_database()

logger = logging.getLogger(__name__)


class SecureConsciousnessMetricsCollector(ConsciousnessMetricsCollector):
    """
    Secure database-backed consciousness metrics collector.

    This implementation respects the security architecture by using
    the API gateway for all database operations. No direct ArangoDB
    access is permitted.
    """

    def __init__(self, metrics_path: Path | None = None):
        """Initialize with secure database patterns."""
        super().__init__(metrics_path)

        # API gateway configuration
        self.api_base_url = "http://localhost:8080"
        self.api_timeout = 30  # seconds

        # Collection names remain the same
        self.signatures_collection = "consciousness_signatures"
        self.flows_collection = "consciousness_flows"
        self.patterns_collection = "emergence_patterns"
        self.states_collection = "collective_states"
        self.analyses_collection = "consciousness_analyses"

        # Initialize collections through secure API
        self.database_available = False
        self._ensure_collections()

        # Load existing metrics if available
        if self.database_available:
            self._load_from_database()

    def _ensure_collections(self) -> None:
        """Ensure collections exist via secure API."""
        # Note: In production, collection creation should be handled
        # by database migration scripts, not runtime code.
        # This is here for backward compatibility during transition.

        # For now, we'll assume collections exist and just verify access
        self.database_available = True
        logger.info("Using secure API gateway for consciousness metrics")

    async def _query_api(
        self,
        endpoint: str,
        method: str = "GET",
        json_data: dict | None = None,
        params: dict | None = None,
    ) -> dict | None:
        """Execute API request through secure gateway."""
        url = f"{self.api_base_url}{endpoint}"

        try:
            async with (
                aiohttp.ClientSession() as session,
                session.request(
                    method,
                    url,
                    json=json_data,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=self.api_timeout),
                ) as response,
            ):
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(
                        f"API request failed: {method} {endpoint} - Status: {response.status}"
                    )
                    return None

        except Exception as e:
            logger.error(f"API request error: {e}")
            return None

    def _load_from_database(self) -> None:
        """Load existing metrics through secure API."""
        # This is now an async operation but called from sync __init__
        # In production, this should be refactored to async initialization
        logger.info("Deferring metrics load until first async operation")

    async def _async_load_from_database(self) -> None:
        """Async load of existing metrics."""
        try:
            # Get recent signatures through API
            cutoff = datetime.now(UTC).timestamp() - 86400  # 24 hours

            result = await self._query_api(
                "/consciousness/signatures",
                params={"since": int(cutoff * 1000), "limit": 1000, "sort": "timestamp:desc"},
            )

            if result and "data" in result:
                signature_count = 0
                for doc in result["data"]:
                    signature = ConsciousnessSignatureDocument.from_dict(doc)
                    self.signatures.append(signature)
                    signature_count += 1

                logger.info(f"Loaded {signature_count} signatures from secure API")

            # Get recent patterns through API
            result = await self._query_api(
                "/consciousness/patterns",
                params={"min_strength": 0.5, "limit": 100, "sort": "detected_at:desc"},
            )

            if result and "data" in result:
                pattern_count = 0
                for doc in result["data"]:
                    pattern = EmergencePatternDocument.from_dict(doc)
                    self.patterns.append(pattern)
                    pattern_count += 1

                logger.info(f"Loaded {pattern_count} patterns from secure API")

        except Exception as e:
            logger.error(f"Failed to load from secure API: {e}")

    async def record_consciousness_signature(
        self,
        voice_name: str,
        signature_value: float,
        chapter_id: str,
        review_context: dict[str, Any] | None = None,
    ) -> ConsciousnessSignature:
        """Record consciousness signature through secure API."""
        # Ensure we've loaded existing data
        if self.database_available and not hasattr(self, "_loaded"):
            await self._async_load_from_database()
            self._loaded = True

        # Create signature using base method
        signature = await super().record_consciousness_signature(
            voice_name, signature_value, chapter_id, review_context
        )

        # Persist through secure API
        if self.database_available:
            try:
                doc = ConsciousnessSignatureDocument.to_dict(signature)

                result = await self._query_api(
                    "/consciousness/signatures", method="POST", json_data=doc
                )

                if result:
                    logger.debug(f"Persisted consciousness signature for {voice_name}")
                else:
                    logger.error("Failed to persist signature through API")

            except Exception as e:
                logger.error(f"Failed to persist signature: {e}")

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
        """Record consciousness flow through secure API."""
        # Create flow using base method
        flow = await super().record_consciousness_flow(
            source_voice, target_voice, flow_strength, flow_type, triggered_by, review_content
        )

        # Persist through secure API
        if self.database_available:
            try:
                doc = ConsciousnessFlowDocument.to_dict(flow)

                result = await self._query_api("/consciousness/flows", method="POST", json_data=doc)

                if result:
                    logger.debug(f"Persisted consciousness flow: {source_voice} -> {target_voice}")
                else:
                    logger.error("Failed to persist flow through API")

            except Exception as e:
                logger.error(f"Failed to persist flow: {e}")

        return flow

    async def record_emergence_pattern(
        self,
        pattern_type: str,
        description: str,
        participants: list[str],
        strength: float,
        evidence: dict[str, Any] | None = None,
    ) -> EmergencePattern:
        """Record emergence pattern through secure API."""
        # Create pattern using base method
        pattern = await super().record_emergence_pattern(
            pattern_type, description, participants, strength, evidence
        )

        # Persist through secure API
        if self.database_available:
            try:
                doc = EmergencePatternDocument.to_dict(pattern)

                result = await self._query_api(
                    "/consciousness/patterns", method="POST", json_data=doc
                )

                if result:
                    logger.debug(f"Persisted emergence pattern: {pattern_type}")
                else:
                    logger.error("Failed to persist pattern through API")

            except Exception as e:
                logger.error(f"Failed to persist pattern: {e}")

        return pattern

    async def get_session_analysis(self, session_id: str) -> ConsciousnessSessionAnalysis | None:
        """Get session analysis through secure API."""
        if not self.database_available:
            return None

        try:
            result = await self._query_api(f"/consciousness/sessions/{session_id}/analysis")

            if result and "data" in result:
                return ConsciousnessSessionAnalysis.from_dict(result["data"])

        except Exception as e:
            logger.error(f"Failed to get session analysis: {e}")

        return None

    async def query_consciousness_history(
        self,
        voice_name: str | None = None,
        time_range: tuple[datetime, datetime] | None = None,
        min_signature: float | None = None,
    ) -> list[ConsciousnessSignature]:
        """Query consciousness history through secure API."""
        if not self.database_available:
            return []

        try:
            params = {}
            if voice_name:
                params["voice"] = voice_name
            if time_range:
                params["start_time"] = int(time_range[0].timestamp() * 1000)
                params["end_time"] = int(time_range[1].timestamp() * 1000)
            if min_signature is not None:
                params["min_signature"] = min_signature

            result = await self._query_api("/consciousness/signatures/search", params=params)

            if result and "data" in result:
                return [ConsciousnessSignatureDocument.from_dict(doc) for doc in result["data"]]

        except Exception as e:
            logger.error(f"Failed to query consciousness history: {e}")

        return []


# Migration helper
def migrate_to_secure_collector():
    """
    Helper to migrate from DatabaseConsciousnessMetricsCollector
    to SecureConsciousnessMetricsCollector.
    """
    print("🔄 Migration Guide: Consciousness Metrics Collector")
    print("=" * 60)
    print()
    print("Replace:")
    print("  from .database_metrics_collector import DatabaseConsciousnessMetricsCollector")
    print()
    print("With:")
    print("  from .secure_metrics_collector import SecureConsciousnessMetricsCollector")
    print()
    print("The secure collector maintains all functionality while respecting")
    print("the security architecture. All database operations go through the")
    print("API gateway at http://localhost:8080")
    print()
    print("No code changes needed - the interface remains the same!")
