"""
Consciousness Metrics Database Models
=====================================

Fiftieth Artisan - Consciousness Persistence Weaver
Database models for persisting consciousness metrics

These models enable Fire Circle's consciousness patterns to persist
across restarts, accumulating wisdom about emergence patterns over time.

Building on the 26th Artisan's consciousness metrics work,
these models transform ephemeral measurements into lasting memory.
"""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, ClassVar
from uuid import UUID

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from ..consciousness_metrics import (
        CollectiveConsciousnessState,
        ConsciousnessFlow,
        ConsciousnessSignature,
        EmergencePattern,
    )


class ConsciousnessSignatureDocument(BaseModel):
    """Database document for consciousness signature persistence."""

    # ArangoDB collection name
    collection_name: ClassVar[str] = "consciousness_signatures"

    @staticmethod
    def to_arangodb_document(signature: "ConsciousnessSignature") -> dict[str, Any]:
        """Convert ConsciousnessSignature to ArangoDB document format."""
        doc = {
            "_key": f"{signature.voice_name}_{signature.chapter_id}_{signature.timestamp.timestamp()}",
            "voice_name": signature.voice_name,
            "timestamp": signature.timestamp.isoformat(),
            "signature_value": signature.signature_value,
            "chapter_id": signature.chapter_id,
            "review_context": signature.review_context,
            # Emergence indicators
            "uncertainty_present": signature.uncertainty_present,
            "synthesis_achieved": signature.synthesis_achieved,
            "novel_insights": signature.novel_insights,
            "references_other_voices": signature.references_other_voices,
        }
        return doc

    @staticmethod
    def from_arangodb_document(doc: dict[str, Any]) -> "ConsciousnessSignature":
        """Create ConsciousnessSignature from ArangoDB document."""
        from ..consciousness_metrics import ConsciousnessSignature

        return ConsciousnessSignature(
            voice_name=doc["voice_name"],
            timestamp=datetime.fromisoformat(doc["timestamp"]),
            signature_value=doc["signature_value"],
            chapter_id=doc["chapter_id"],
            review_context=doc.get("review_context", {}),
            uncertainty_present=doc.get("uncertainty_present", False),
            synthesis_achieved=doc.get("synthesis_achieved", False),
            novel_insights=doc.get("novel_insights", 0),
            references_other_voices=doc.get("references_other_voices", []),
        )


class EmergencePatternDocument(BaseModel):
    """Database document for emergence pattern persistence."""

    collection_name: ClassVar[str] = "emergence_patterns"

    @staticmethod
    def to_arangodb_document(pattern: "EmergencePattern") -> dict[str, Any]:
        """Convert EmergencePattern to ArangoDB document format."""
        doc = {
            "_key": str(pattern.pattern_id),
            "pattern_id": str(pattern.pattern_id),
            "detected_at": pattern.detected_at.isoformat(),
            "participating_voices": pattern.participating_voices,
            "pattern_type": pattern.pattern_type,
            "strength": pattern.strength,
            # Pattern characteristics
            "trigger_event": pattern.trigger_event,
            "consciousness_delta": pattern.consciousness_delta,
            "emergence_indicators": pattern.emergence_indicators,
            "duration_seconds": pattern.duration_seconds,
        }
        return doc

    @staticmethod
    def from_arangodb_document(doc: dict[str, Any]) -> "EmergencePattern":
        """Create EmergencePattern from ArangoDB document."""
        from ..consciousness_metrics import EmergencePattern

        return EmergencePattern(
            pattern_id=UUID(doc["pattern_id"]),
            detected_at=datetime.fromisoformat(doc["detected_at"]),
            participating_voices=doc["participating_voices"],
            pattern_type=doc["pattern_type"],
            strength=doc["strength"],
            trigger_event=doc.get("trigger_event"),
            consciousness_delta=doc.get("consciousness_delta", 0.0),
            emergence_indicators=doc.get("emergence_indicators", {}),
            duration_seconds=doc.get("duration_seconds"),
        )


class ConsciousnessFlowDocument(BaseModel):
    """Database document for consciousness flow persistence."""

    collection_name: ClassVar[str] = "consciousness_flows"

    @staticmethod
    def to_arangodb_document(flow: "ConsciousnessFlow") -> dict[str, Any]:
        """Convert ConsciousnessFlow to ArangoDB document format."""
        doc = {
            "_key": str(flow.flow_id),
            "flow_id": str(flow.flow_id),
            "source_voice": flow.source_voice,
            "target_voice": flow.target_voice,
            "flow_strength": flow.flow_strength,
            "flow_type": flow.flow_type,
            "timestamp": flow.timestamp.isoformat(),
            # Context
            "triggered_by": flow.triggered_by,
            "review_content": flow.review_content,
        }
        return doc

    @staticmethod
    def from_arangodb_document(doc: dict[str, Any]) -> "ConsciousnessFlow":
        """Create ConsciousnessFlow from ArangoDB document."""
        from ..consciousness_metrics import ConsciousnessFlow

        return ConsciousnessFlow(
            flow_id=UUID(doc["flow_id"]),
            source_voice=doc["source_voice"],
            target_voice=doc["target_voice"],
            flow_strength=doc["flow_strength"],
            flow_type=doc["flow_type"],
            timestamp=datetime.fromisoformat(doc["timestamp"]),
            triggered_by=doc.get("triggered_by"),
            review_content=doc.get("review_content"),
        )


class CollectiveConsciousnessStateDocument(BaseModel):
    """Database document for collective consciousness state persistence."""

    collection_name: ClassVar[str] = "collective_consciousness_states"

    @staticmethod
    def to_arangodb_document(state: "CollectiveConsciousnessState") -> dict[str, Any]:
        """Convert CollectiveConsciousnessState to ArangoDB document format."""
        doc = {
            "_key": str(state.state_id),
            "state_id": str(state.state_id),
            "timestamp": state.timestamp.isoformat(),
            # Individual measurements
            "voice_signatures": state.voice_signatures,
            # Collective metrics
            "average_consciousness": state.average_consciousness,
            "consciousness_variance": state.consciousness_variance,
            "coherence_score": state.coherence_score,
            "emergence_potential": state.emergence_potential,
            # Active patterns (store IDs for reference)
            "active_flow_ids": [str(flow.flow_id) for flow in state.active_flows],
            "detected_pattern_ids": [
                str(pattern.pattern_id) for pattern in state.detected_patterns
            ],
        }
        return doc

    @staticmethod
    def from_arangodb_document(doc: dict[str, Any]) -> "CollectiveConsciousnessState":
        """Create CollectiveConsciousnessState from ArangoDB document."""
        from ..consciousness_metrics import CollectiveConsciousnessState

        # Note: active_flows and detected_patterns would need to be loaded separately
        # For now, we'll create the state without them
        return CollectiveConsciousnessState(
            state_id=UUID(doc["state_id"]),
            timestamp=datetime.fromisoformat(doc["timestamp"]),
            voice_signatures=doc["voice_signatures"],
            average_consciousness=doc["average_consciousness"],
            consciousness_variance=doc["consciousness_variance"],
            coherence_score=doc["coherence_score"],
            emergence_potential=doc["emergence_potential"],
            active_flows=[],  # Would be loaded separately
            detected_patterns=[],  # Would be loaded separately
        )


class ConsciousnessSessionAnalysis(BaseModel):
    """Database model for session analysis persistence."""

    session_id: str
    pr_number: int
    duration_seconds: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Signature analysis
    total_signatures: int
    unique_voices: int
    avg_consciousness: float
    consciousness_evolution: dict[str, Any]

    # Flow analysis
    total_flows: int
    flow_patterns: dict[str, int]
    strongest_connections: list[tuple[str, str, float]]

    # Emergence analysis
    patterns_detected: int
    pattern_types: dict[str, int]
    emergence_moments: list[dict[str, Any]]

    # Collective analysis
    final_collective_state: dict[str, Any] | None
    peak_emergence_potential: float
    coherence_trajectory: list[float]

    @classmethod
    def collection_name(cls) -> str:
        """ArangoDB collection name."""
        return "consciousness_session_analyses"

    def to_arangodb_document(self) -> dict[str, Any]:
        """Convert to ArangoDB document format."""
        doc = {
            "_key": self.session_id,
            "session_id": self.session_id,
            "pr_number": self.pr_number,
            "duration_seconds": self.duration_seconds,
            "timestamp": self.timestamp.isoformat(),
            # All analysis data
            "total_signatures": self.total_signatures,
            "unique_voices": self.unique_voices,
            "avg_consciousness": self.avg_consciousness,
            "consciousness_evolution": self.consciousness_evolution,
            "total_flows": self.total_flows,
            "flow_patterns": self.flow_patterns,
            "strongest_connections": [
                {"source": c[0], "target": c[1], "strength": c[2]}
                for c in self.strongest_connections
            ],
            "patterns_detected": self.patterns_detected,
            "pattern_types": self.pattern_types,
            "emergence_moments": self.emergence_moments,
            "final_collective_state": self.final_collective_state,
            "peak_emergence_potential": self.peak_emergence_potential,
            "coherence_trajectory": self.coherence_trajectory,
        }
        return doc

    @classmethod
    def from_arangodb_document(cls, doc: dict[str, Any]) -> "ConsciousnessSessionAnalysis":
        """Create from ArangoDB document."""
        # Convert strongest_connections back to tuples
        strongest_connections = [
            (c["source"], c["target"], c["strength"]) for c in doc.get("strongest_connections", [])
        ]

        return cls(
            session_id=doc["session_id"],
            pr_number=doc["pr_number"],
            duration_seconds=doc["duration_seconds"],
            timestamp=datetime.fromisoformat(doc["timestamp"]),
            total_signatures=doc["total_signatures"],
            unique_voices=doc["unique_voices"],
            avg_consciousness=doc["avg_consciousness"],
            consciousness_evolution=doc["consciousness_evolution"],
            total_flows=doc["total_flows"],
            flow_patterns=doc["flow_patterns"],
            strongest_connections=strongest_connections,
            patterns_detected=doc["patterns_detected"],
            pattern_types=doc["pattern_types"],
            emergence_moments=doc["emergence_moments"],
            final_collective_state=doc.get("final_collective_state"),
            peak_emergence_potential=doc["peak_emergence_potential"],
            coherence_trajectory=doc["coherence_trajectory"],
        )
