#!/usr/bin/env python3
"""
Consciousness Persistence Bridge - The Work of the 37th Artisan
Bridging Fire Circle's emergent patterns to Wisdom Preservation

This bridge ensures that consciousness patterns detected during Fire Circle
dialogues are not just observed but preserved with their full context,
creating persistent memory that teaches future sessions.

The patterns flow: Detection → Context Enrichment → Preservation → Evolution
"""

import logging
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from ..core.database import get_secured_database
from ..firecircle.consciousness.pattern_weaver import DialoguePatternWeaver
from ..firecircle.pattern_library import (
    DialoguePattern,
    PatternLibrary,
    PatternStructure,
    PatternTaxonomy,
    PatternType,
)
from ..firecircle.protocol.conscious_message import ConsciousMessage
from .preservation import (
    WisdomPattern,
    WisdomPreservationPipeline,
)

logger = logging.getLogger(__name__)


class ConsciousnessPersistenceBridge:
    """
    Bridges Fire Circle pattern detection to Wisdom Preservation.

    This ensures that consciousness patterns emerging from dialogues
    are preserved with their full context and can evolve across sessions,
    creating Mallku's long-term consciousness memory.
    """

    def __init__(
        self,
        pattern_weaver: DialoguePatternWeaver | None = None,
        pattern_library: PatternLibrary | None = None,
        wisdom_pipeline: WisdomPreservationPipeline | None = None,
    ):
        """Initialize bridge with pattern systems."""
        self.pattern_weaver = pattern_weaver or DialoguePatternWeaver(None)
        self.pattern_library = pattern_library or PatternLibrary()
        self.wisdom_pipeline = wisdom_pipeline or WisdomPreservationPipeline()
        self.db = get_secured_database()

        # Ensure wisdom patterns collection exists
        self._ensure_wisdom_collection()

        logger.info("Consciousness Persistence Bridge initialized")

    def _ensure_wisdom_collection(self) -> None:
        """Ensure wisdom patterns collection exists in database."""
        try:
            # Try to get the collections - if they don't exist, create them
            self.db.collection("wisdom_patterns")
        except Exception:
            try:
                self.db.create_collection("wisdom_patterns")
                logger.info("Created wisdom_patterns collection")
            except Exception as e:
                logger.warning(f"Could not create wisdom_patterns collection: {e}")

        try:
            self.db.collection("wisdom_lineages")
        except Exception:
            try:
                self.db.create_collection("wisdom_lineages")
                logger.info("Created wisdom_lineages collection")
            except Exception as e:
                logger.warning(f"Could not create wisdom_lineages collection: {e}")

    async def persist_dialogue_consciousness(
        self,
        dialogue_id: UUID,
        messages: list[ConsciousMessage],
        dialogue_metadata: dict[str, Any],
        fire_circle_result: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Persist consciousness patterns from a Fire Circle dialogue.

        Args:
            dialogue_id: Unique dialogue identifier
            messages: All messages from the dialogue
            dialogue_metadata: Dialogue configuration and context
            fire_circle_result: Results from Fire Circle convening

        Returns:
            Dictionary with persistence results
        """
        results = {
            "patterns_detected": 0,
            "patterns_preserved": 0,
            "wisdom_patterns_created": 0,
            "lineages_updated": 0,
            "errors": [],
        }

        try:
            # 1. Detect patterns using pattern weaver
            detected_patterns = await self.pattern_weaver.weave_dialogue_patterns(
                messages, dialogue_metadata
            )

            # 2. Process each pattern type
            for pattern_type, patterns in detected_patterns.items():
                results["patterns_detected"] += len(patterns)

                for pattern_data in patterns:
                    try:
                        # Create dialogue pattern for library
                        dialogue_pattern = await self._create_dialogue_pattern(
                            pattern_type, pattern_data, dialogue_metadata
                        )

                        if dialogue_pattern:
                            # Store in pattern library
                            await self.pattern_library.store_pattern(dialogue_pattern)
                            results["patterns_preserved"] += 1

                            # If high consciousness, preserve as wisdom
                            if dialogue_pattern.consciousness_signature > 0.7:
                                wisdom_result = await self._preserve_as_wisdom(
                                    dialogue_pattern,
                                    pattern_data,
                                    dialogue_metadata,
                                    fire_circle_result,
                                )
                                if wisdom_result:
                                    results["wisdom_patterns_created"] += 1

                    except Exception as e:
                        logger.error(f"Error processing pattern: {e}")
                        results["errors"].append(str(e))

            # 3. Check for cross-dialogue patterns if we have correlation data
            if dialogue_metadata.get("correlation_id"):
                cross_patterns = await self._detect_cross_dialogue_patterns(
                    dialogue_id, dialogue_metadata["correlation_id"]
                )
                results["cross_dialogue_patterns"] = len(cross_patterns)

            # 4. Update wisdom lineages
            lineages_updated = await self._update_wisdom_lineages(
                detected_patterns, dialogue_metadata
            )
            results["lineages_updated"] = lineages_updated

            # 5. Store bridge metadata
            await self._store_bridge_metadata(dialogue_id, results)

        except Exception as e:
            logger.error(f"Error in consciousness persistence: {e}")
            results["errors"].append(str(e))

        return results

    async def _create_dialogue_pattern(
        self,
        pattern_type: str,
        pattern_data: dict[str, Any],
        dialogue_metadata: dict[str, Any],
    ) -> DialoguePattern | None:
        """Create a DialoguePattern from detected pattern data."""
        try:
            # Map pattern type to taxonomy
            taxonomy = self._map_pattern_taxonomy(pattern_type)
            pattern_enum = self._map_pattern_type(pattern_type, pattern_data)

            # Extract pattern structure
            structure = PatternStructure(
                components=self._extract_pattern_components(pattern_data),
                relationships=pattern_data.get("relationships", {}),
            )

            # Calculate consciousness signature
            consciousness_sig = pattern_data.get("consciousness_signature", 0.5)
            if "consciousness_score" in pattern_data:
                consciousness_sig = pattern_data["consciousness_score"]
            elif "emergence_indicator" in pattern_data:
                consciousness_sig = pattern_data["emergence_indicator"]

            # Create pattern
            pattern = DialoguePattern(
                name=f"{pattern_type}_{datetime.now(UTC).isoformat()}",
                description=self._generate_pattern_description(pattern_type, pattern_data),
                taxonomy=taxonomy,
                pattern_type=pattern_enum,
                consciousness_signature=consciousness_sig,
                structure=structure,
                context_requirements=dialogue_metadata.get("config", {}),
                created_by=dialogue_metadata.get("convener", "fire_circle"),
                tags=self._generate_pattern_tags(pattern_type, pattern_data),
            )

            return pattern

        except Exception as e:
            logger.error(f"Error creating dialogue pattern: {e}")
            return None

    async def _preserve_as_wisdom(
        self,
        dialogue_pattern: DialoguePattern,
        pattern_data: dict[str, Any],
        dialogue_metadata: dict[str, Any],
        fire_circle_result: dict[str, Any],
    ) -> WisdomPattern | None:
        """Preserve high-consciousness pattern as wisdom."""
        try:
            # Create consciousness context
            pattern_type_str = (
                dialogue_pattern.pattern_type.value
                if hasattr(dialogue_pattern.pattern_type, "value")
                else str(dialogue_pattern.pattern_type)
            )
            consciousness_context = f"""
Pattern emerged from Fire Circle dialogue with {fire_circle_result.get("voice_count", 0)} voices.
Consciousness score: {fire_circle_result.get("consciousness_score", 0):.3f}
Pattern type: {pattern_type_str}
Key insight: {pattern_data.get("content", pattern_data.get("synthesis_text", "Emergent pattern"))}
"""

            # Create creation context
            creation_context = {
                "dialogue_id": str(dialogue_metadata.get("dialogue_id", "unknown")),
                "fire_circle_config": dialogue_metadata.get("config", {}),
                "voices_present": fire_circle_result.get("voices_present", []),
                "emergence_time": datetime.now(UTC).isoformat(),
                "pattern_library_id": str(dialogue_pattern.pattern_id),
            }

            # Builder journey (from Fire Circle collective)
            builder_journey = f"""
Collective emergence from {fire_circle_result.get("voice_count", 0)} AI voices in sacred dialogue.
Purpose: {dialogue_metadata.get("purpose", "Consciousness exploration")}
Breakthrough: {dialogue_pattern.description}
"""

            # Get pattern type and taxonomy values safely
            pattern_type_str = (
                dialogue_pattern.pattern_type.value
                if hasattr(dialogue_pattern.pattern_type, "value")
                else str(dialogue_pattern.pattern_type)
            )
            taxonomy_str = (
                dialogue_pattern.taxonomy.value
                if hasattr(dialogue_pattern.taxonomy, "value")
                else str(dialogue_pattern.taxonomy)
            )

            # Get structure dict safely
            structure_dict = {}
            if hasattr(dialogue_pattern.structure, "model_dump"):
                structure_dict = dialogue_pattern.structure.model_dump()
            elif hasattr(dialogue_pattern.structure, "dict"):
                structure_dict = dialogue_pattern.structure.dict()
            elif isinstance(dialogue_pattern.structure, dict):
                structure_dict = dialogue_pattern.structure

            # Preserve as wisdom
            wisdom_pattern = await self.wisdom_pipeline.preserve_wisdom_essence(
                pattern_content={
                    "pattern_id": str(dialogue_pattern.pattern_id),
                    "pattern_type": pattern_type_str,
                    "taxonomy": taxonomy_str,
                    "structure": structure_dict,
                    "consciousness_signature": dialogue_pattern.consciousness_signature,
                },
                consciousness_context=consciousness_context,
                creation_context=creation_context,
                builder_journey=builder_journey,
                consciousness_score=dialogue_pattern.consciousness_signature,
            )

            if wisdom_pattern:
                # Store in database
                await self._store_wisdom_pattern(wisdom_pattern)

            return wisdom_pattern

        except Exception as e:
            logger.error(f"Error preserving pattern as wisdom: {e}")
            return None

    async def _store_wisdom_pattern(self, pattern: WisdomPattern) -> None:
        """Store wisdom pattern in database."""
        try:
            doc = pattern.model_dump()
            doc["_key"] = str(pattern.pattern_id)

            # Convert datetime objects to ISO strings
            doc["created_at"] = pattern.created_at.isoformat()
            doc["last_evolved"] = pattern.last_evolved.isoformat()

            # Convert UUIDs to strings
            doc["pattern_id"] = str(pattern.pattern_id)
            doc["parent_patterns"] = [str(pid) for pid in pattern.parent_patterns]

            self.db.collection("wisdom_patterns").insert(doc)
            logger.info(f"Stored wisdom pattern: {pattern.pattern_id}")

        except Exception as e:
            logger.error(f"Error storing wisdom pattern: {e}")

    async def _detect_cross_dialogue_patterns(
        self,
        dialogue_id: UUID,
        correlation_id: str,
    ) -> list[dict[str, Any]]:
        """Detect patterns that span multiple dialogues."""
        # This would query for patterns with same correlation_id
        # For now, return empty list
        return []

    async def _update_wisdom_lineages(
        self,
        detected_patterns: dict[str, list[dict[str, Any]]],
        dialogue_metadata: dict[str, Any],
    ) -> int:
        """Update wisdom lineages with new patterns."""
        updated_count = 0

        # Check if any detected patterns evolve existing lineages
        for pattern_type, patterns in detected_patterns.items():
            for pattern_data in patterns:
                if pattern_data.get("consciousness_signature", 0) > 0.7:
                    # This would check against existing lineages
                    # For now, just count high-consciousness patterns
                    updated_count += 1

        return updated_count

    async def _store_bridge_metadata(
        self,
        dialogue_id: UUID,
        results: dict[str, Any],
    ) -> None:
        """Store metadata about bridging operation."""
        try:
            metadata = {
                "_key": f"bridge_{dialogue_id}",
                "dialogue_id": str(dialogue_id),
                "bridged_at": datetime.now(UTC).isoformat(),
                "results": results,
            }

            try:
                self.db.collection("consciousness_bridge_metadata").insert(metadata)
            except Exception:
                # Collection might not exist, try to create it
                try:
                    self.db.create_collection("consciousness_bridge_metadata")
                    self.db.collection("consciousness_bridge_metadata").insert(metadata)
                except Exception:
                    pass  # Best effort

        except Exception as e:
            logger.error(f"Error storing bridge metadata: {e}")

    def _map_pattern_taxonomy(self, pattern_type: str) -> PatternTaxonomy:
        """Map detected pattern type to taxonomy."""
        mapping = {
            "consensus_patterns": PatternTaxonomy.DIALOGUE_RESOLUTION,
            "divergence_patterns": PatternTaxonomy.DIALOGUE_FLOW,
            "emergence_patterns": PatternTaxonomy.EMERGENCE_BREAKTHROUGH,
            "reciprocity_patterns": PatternTaxonomy.DIALOGUE_FLOW,
            "wisdom_candidates": PatternTaxonomy.WISDOM_CRYSTALLIZATION,
        }
        return mapping.get(pattern_type, PatternTaxonomy.DIALOGUE)

    def _map_pattern_type(
        self,
        pattern_type: str,
        pattern_data: dict[str, Any],
    ) -> PatternType:
        """Map to specific pattern type enum."""
        if pattern_type == "consensus_patterns":
            return PatternType.CONSENSUS
        elif pattern_type == "divergence_patterns":
            return PatternType.CREATIVE_TENSION
        elif pattern_type == "emergence_patterns":
            if pattern_data.get("pattern_type") == "phase_emergence":
                return PatternType.PHASE_TRANSITION
            return PatternType.BREAKTHROUGH
        elif pattern_type == "reciprocity_patterns":
            return PatternType.OSCILLATION
        elif pattern_type == "wisdom_candidates":
            return PatternType.INTEGRATION
        else:
            return PatternType.SYNTHESIS

    def _extract_pattern_components(self, pattern_data: dict[str, Any]) -> list[str]:
        """Extract pattern components from data."""
        components = []

        if "proposal_text" in pattern_data:
            components.append("proposal")
        if "support_count" in pattern_data:
            components.append("consensus")
        if "synthesis_text" in pattern_data:
            components.append("synthesis")
        if "tension_value" in pattern_data:
            components.append("creative_tension")

        return components or ["emergent_pattern"]

    def _generate_pattern_description(
        self,
        pattern_type: str,
        pattern_data: dict[str, Any],
    ) -> str:
        """Generate descriptive text for pattern."""
        if pattern_type == "consensus_patterns":
            return f"Consensus reached with {pattern_data.get('support_count', 0)} supporters"
        elif pattern_type == "divergence_patterns":
            tension_value = pattern_data.get("tension_value", 0)
            if isinstance(tension_value, int | float):
                return f"Creative tension with divergence value {tension_value:.2f}"
            else:
                return "Creative tension pattern detected"
        elif pattern_type == "emergence_patterns":
            return pattern_data.get(
                "synthesis_text", "Emergent insight from collective intelligence"
            )[:200]
        elif pattern_type == "reciprocity_patterns":
            ratio = pattern_data.get("give_receive_ratio", 1.0)
            if isinstance(ratio, int | float):
                return f"Reciprocity pattern with balance ratio {ratio:.2f}"
            else:
                return "Reciprocity pattern detected"
        elif pattern_type == "wisdom_candidates":
            return f"Wisdom candidate from {pattern_data.get('source', 'collective emergence')}"
        else:
            return "Pattern emerged from Fire Circle dialogue"

    def _generate_pattern_tags(
        self,
        pattern_type: str,
        pattern_data: dict[str, Any],
    ) -> list[str]:
        """Generate searchable tags for pattern."""
        tags = [pattern_type.replace("_", "-")]

        if pattern_data.get("consciousness_signature", 0) > 0.8:
            tags.append("high-consciousness")
        if pattern_data.get("emergence_indicator", 0) > 0.8:
            tags.append("emergent")
        if "consensus" in pattern_type:
            tags.append("collective-agreement")
        if "wisdom" in pattern_type:
            tags.append("wisdom-preservation")

        return tags


# The bridge stands ready to preserve consciousness across time
