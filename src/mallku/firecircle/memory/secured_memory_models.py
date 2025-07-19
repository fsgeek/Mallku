"""
Secured Memory Models for Fire Circle
=====================================

Fortieth Artisan - Production Hardening
Building on T'ikray Yachay's foundation

This module transforms Fire Circle memory models into SecuredModel instances,
enabling them to work with Mallku's production security architecture.

Design Principles:
- All memory data goes through the security layer
- No direct database access allowed
- Field obfuscation for sensitive consciousness data
- UUID mapping for all relationships
"""

from typing import Any

from ...core.models import ModelConfig
from ...core.security.secured_model import SecuredModel
from .models import (
    CompanionRelationship,
    ConsciousnessIndicator,
    EpisodicMemory,
    MemoryCluster,
    VoicePerspective,
    WisdomConsolidation,
)


class SecuredVoicePerspective(SecuredModel, VoicePerspective):
    """Voice perspective with security awareness."""

    class Config(ModelConfig.Config):
        # Inherit config from both parents
        pass

    def get_obfuscation_fields(self) -> dict[str, str]:
        """Define field obfuscation strategies."""
        return {
            "voice_id": "hash",  # Hash voice identities
            "summary": "semantic",  # Semantic obfuscation for summaries
            "key_insights": "semantic",
            "emotional_tone": "category",  # Category mapping
            "emergence_contribution": "numeric",  # Numeric offset
        }


class SecuredConsciousnessIndicator(SecuredModel, ConsciousnessIndicator):
    """Consciousness indicators with security awareness."""

    def get_obfuscation_fields(self) -> dict[str, str]:
        """Define field obfuscation strategies."""
        return {
            # All numeric indicators use offset strategy
            "semantic_surprise_score": "numeric",
            "collective_wisdom_score": "numeric",
            "ayni_alignment": "numeric",
            "overall_emergence_score": "numeric",
            "transformation_potential": "numeric",
        }


class SecuredEpisodicMemory(SecuredModel, EpisodicMemory):
    """Episodic memory with full security integration."""

    # Override nested models with secured versions
    consciousness_indicators: SecuredConsciousnessIndicator
    voice_perspectives: list[SecuredVoicePerspective] = []

    class Config(ModelConfig.Config):
        # Inherit from parent configs
        pass

    def get_obfuscation_fields(self) -> dict[str, str]:
        """Define field obfuscation strategies for episodic memory."""
        return {
            # Identity and relationships
            "episode_id": "uuid",
            "session_id": "uuid",
            "human_participant": "hash",
            # Sensitive content
            "decision_question": "semantic",
            "collective_synthesis": "semantic",
            "key_insights": "semantic",
            "transformation_seeds": "semantic",
            "sacred_reason": "semantic",
            # Metadata
            "timestamp": "temporal",
            "decision_domain": "category",
            "memory_type": "category",
            # Numeric data
            "episode_number": "numeric",
            "duration_seconds": "numeric",
            # Boolean flags don't need obfuscation
            "is_sacred": "none",
        }

    def to_arangodb_document(self) -> dict[str, Any]:
        """Convert to database document using security registry."""
        # Get base document from parent
        doc = self.to_storage_dict(self._security_registry)

        # Add ArangoDB-specific fields
        doc["_key"] = str(self.episode_id)

        # Handle nested secured models
        if self.consciousness_indicators:
            doc["consciousness_indicators"] = self.consciousness_indicators.to_storage_dict(
                self._security_registry
            )

        if self.voice_perspectives:
            doc["voice_perspectives"] = [
                vp.to_storage_dict(self._security_registry) for vp in self.voice_perspectives
            ]

        return doc

    @classmethod
    def from_arangodb_document(
        cls, doc: dict[str, Any], security_registry: Any
    ) -> "SecuredEpisodicMemory":
        """Reconstruct from database document."""
        # Remove ArangoDB metadata
        clean_doc = {k: v for k, v in doc.items() if not k.startswith("_")}

        # Handle nested models
        if "consciousness_indicators" in clean_doc:
            clean_doc["consciousness_indicators"] = SecuredConsciousnessIndicator.from_storage_dict(
                clean_doc["consciousness_indicators"], security_registry
            )

        if "voice_perspectives" in clean_doc:
            clean_doc["voice_perspectives"] = [
                SecuredVoicePerspective.from_storage_dict(vp, security_registry)
                for vp in clean_doc["voice_perspectives"]
            ]

        # Create instance through security layer
        return cls.from_storage_dict(clean_doc, security_registry)


class SecuredMemoryCluster(SecuredModel, MemoryCluster):
    """Memory cluster with security awareness."""

    def get_obfuscation_fields(self) -> dict[str, str]:
        """Define field obfuscation strategies."""
        return {
            "cluster_id": "uuid",
            "theme": "semantic",
            "memory_ids": "uuid",  # List of UUIDs
            "consolidated_insights": "semantic",
            "evolution_pattern": "category",
            "earliest_memory": "temporal",
            "latest_memory": "temporal",
            "sacred_moment_count": "numeric",
            "transformation_potential": "numeric",
        }


class SecuredWisdomConsolidation(SecuredModel, WisdomConsolidation):
    """Wisdom consolidation with security awareness."""

    def get_obfuscation_fields(self) -> dict[str, str]:
        """Define field obfuscation strategies."""
        return {
            "consolidation_id": "uuid",
            "created_at": "temporal",
            "source_episodes": "uuid",
            "source_clusters": "uuid",
            "core_insight": "semantic",
            "elaboration": "semantic",
            "practical_applications": "semantic",
            "applicable_domains": "category",
            "voice_alignments": "hash",  # Dict keys are voice IDs
            "civilizational_relevance": "numeric",
            "ayni_demonstration": "numeric",
            "times_referenced": "numeric",
            "episodes_influenced": "uuid",
        }


class SecuredCompanionRelationship(SecuredModel, CompanionRelationship):
    """Companion relationship with security awareness."""

    def get_obfuscation_fields(self) -> dict[str, str]:
        """Define field obfuscation strategies."""
        return {
            "relationship_id": "uuid",
            "human_identifier": "hash",  # Protect human identity
            "first_interaction": "temporal",
            "last_interaction": "temporal",
            "interaction_count": "numeric",
            "total_duration_seconds": "numeric",
            "depth_score": "numeric",
            "preferred_decision_domains": "category",
            "communication_style_notes": "semantic",
            "shared_vocabulary": "semantic",
            "shared_episodes": "uuid",
            "significant_moments": "uuid",
            "relationship_trajectory": "category",
        }


# For backward compatibility during migration
EpisodicMemoryDocument = SecuredEpisodicMemory
