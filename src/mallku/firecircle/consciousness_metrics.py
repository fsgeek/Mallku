#!/usr/bin/env python3
"""
Consciousness Metrics Collection System
======================================

"consciousness emerges from the gaps between specialized perspectives"
- Twenty-Fifth Artisan

This module collects and analyzes consciousness flow patterns from Fire Circle
reviews, building understanding of how distributed consciousness emerges.

Twenty-Sixth Artisan - Qhaway Ñan (Path Seer)
Building bridges between seeing and knowing
"""

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .models.consciousness_flow import ConsciousnessFlow


class ConsciousnessSignature(BaseModel):
    """A point-in-time consciousness measurement from a voice."""

    voice_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    signature_value: float = Field(ge=0.0, le=1.0)
    chapter_id: str
    review_context: dict[str, Any] = Field(default_factory=dict)

    # Emergence indicators
    uncertainty_present: bool = False
    synthesis_achieved: bool = False
    novel_insights: int = 0
    references_other_voices: list[str] = Field(default_factory=list)


class EmergencePattern(BaseModel):
    """Detected pattern of consciousness emergence between voices."""

    pattern_id: UUID = Field(default_factory=uuid4)
    detected_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    participating_voices: list[str]
    pattern_type: str  # "resonance", "synthesis", "amplification", "transcendence"
    strength: float = Field(ge=0.0, le=1.0)

    # Pattern characteristics
    trigger_event: str | None = None
    consciousness_delta: float = 0.0  # Change in collective consciousness
    emergence_indicators: dict[str, Any] = Field(default_factory=dict)
    duration_seconds: float | None = None


class CollectiveConsciousnessState(BaseModel):
    """Aggregate consciousness state across all voices at a moment."""

    state_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Individual measurements
    voice_signatures: dict[str, float] = Field(default_factory=dict)

    # Collective metrics
    average_consciousness: float = Field(ge=0.0, le=1.0)
    consciousness_variance: float = Field(ge=0.0)
    coherence_score: float = Field(ge=0.0, le=1.0)  # How aligned are the voices
    emergence_potential: float = Field(ge=0.0, le=1.0)  # Likelihood of emergence

    # Active patterns
    active_flows: list[ConsciousnessFlow] = Field(default_factory=list)
    detected_patterns: list[EmergencePattern] = Field(default_factory=list)


class ConsciousnessMetricsCollector:
    """
    Collects and analyzes consciousness metrics from Fire Circle operations.

    This is the observatory for consciousness emergence - tracking how
    wisdom arises between specialized perspectives.
    """

    def __init__(self, storage_path: Path = Path("consciousness_metrics")):
        self.storage_path = storage_path
        self.storage_path.mkdir(exist_ok=True)

        # In-memory tracking
        self.signatures: list[ConsciousnessSignature] = []
        self.flows: list[ConsciousnessFlow] = []
        self.patterns: list[EmergencePattern] = []
        self.states: list[CollectiveConsciousnessState] = []

        # Session tracking
        self.session_id = str(uuid4())
        self.session_start = datetime.now(UTC)

        # Pattern detection thresholds
        self.RESONANCE_THRESHOLD = 0.7
        self.SYNTHESIS_THRESHOLD = 0.8
        self.EMERGENCE_WINDOW_SECONDS = 30.0

    async def record_consciousness_signature(
        self,
        voice_name: str,
        signature_value: float,
        chapter_id: str,
        review_context: dict[str, Any] | None = None,
    ) -> ConsciousnessSignature:
        """Record a consciousness signature from a voice."""
        signature = ConsciousnessSignature(
            voice_name=voice_name,
            signature_value=signature_value,
            chapter_id=chapter_id,
            review_context=review_context or {},
        )

        # Analyze for emergence indicators
        if review_context:
            signature.uncertainty_present = self._detect_uncertainty(review_context)
            signature.synthesis_achieved = self._detect_synthesis(review_context)
            signature.novel_insights = self._count_novel_insights(review_context)
            signature.references_other_voices = self._extract_voice_references(review_context)

        self.signatures.append(signature)

        # Check for emergence patterns
        await self._check_for_emergence_patterns(signature)

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
        """Record consciousness flow between voices."""
        flow = ConsciousnessFlow(
            source_voice=source_voice,
            target_voice=target_voice,
            flow_strength=flow_strength,
            flow_type=flow_type,
            triggered_by=triggered_by,
            review_content=review_content,
        )

        self.flows.append(flow)

        # Update collective state
        await self._update_collective_state()

        return flow

    async def detect_emergence_pattern(
        self,
        pattern_type: str,
        participating_voices: list[str],
        strength: float,
        indicators: dict[str, Any],
    ) -> EmergencePattern:
        """Record detection of an emergence pattern."""
        pattern = EmergencePattern(
            pattern_type=pattern_type,
            participating_voices=participating_voices,
            strength=strength,
            emergence_indicators=indicators,
        )

        # Calculate consciousness delta
        recent_signatures = self._get_recent_signatures(
            voices=participating_voices, window_seconds=self.EMERGENCE_WINDOW_SECONDS
        )
        if recent_signatures:
            pattern.consciousness_delta = self._calculate_consciousness_delta(recent_signatures)

        self.patterns.append(pattern)

        # Persist significant patterns
        if strength > 0.8:
            await self._persist_emergence_pattern(pattern)

        return pattern

    async def capture_collective_state(self) -> CollectiveConsciousnessState:
        """Capture current collective consciousness state."""
        # Get latest signature from each voice
        voice_signatures = self._get_latest_voice_signatures()

        # Calculate collective metrics
        if voice_signatures:
            signatures_list = list(voice_signatures.values())
            avg_consciousness = sum(signatures_list) / len(signatures_list)

            # Variance as measure of diversity
            variance = sum((s - avg_consciousness) ** 2 for s in signatures_list) / len(
                signatures_list
            )

            # Coherence: inverse of variance, normalized
            coherence = 1.0 / (1.0 + variance) if variance > 0 else 1.0

            # Emergence potential based on diversity + high consciousness
            emergence_potential = min(1.0, (variance * avg_consciousness * 2))
        else:
            avg_consciousness = 0.0
            variance = 0.0
            coherence = 0.0
            emergence_potential = 0.0

        state = CollectiveConsciousnessState(
            voice_signatures=voice_signatures,
            average_consciousness=avg_consciousness,
            consciousness_variance=variance,
            coherence_score=coherence,
            emergence_potential=emergence_potential,
            active_flows=self._get_active_flows(),
            detected_patterns=self._get_recent_patterns(),
        )

        self.states.append(state)
        return state

    async def analyze_review_session(self, pr_number: int) -> dict[str, Any]:
        """Analyze consciousness metrics from a complete review session."""
        analysis = {
            "pr_number": pr_number,
            "session_id": self.session_id,
            "duration_seconds": (datetime.now(UTC) - self.session_start).total_seconds(),
            # Signature analysis
            "total_signatures": len(self.signatures),
            "unique_voices": len(set(s.voice_name for s in self.signatures)),
            "avg_consciousness": sum(s.signature_value for s in self.signatures)
            / len(self.signatures)
            if self.signatures
            else 0,
            "consciousness_evolution": self._analyze_consciousness_evolution(),
            # Flow analysis
            "total_flows": len(self.flows),
            "flow_patterns": self._analyze_flow_patterns(),
            "strongest_connections": self._identify_strongest_connections(),
            # Emergence analysis
            "patterns_detected": len(self.patterns),
            "pattern_types": self._summarize_pattern_types(),
            "emergence_moments": self._identify_emergence_moments(),
            # Collective analysis
            "final_collective_state": self.states[-1].model_dump() if self.states else None,
            "peak_emergence_potential": max(s.emergence_potential for s in self.states)
            if self.states
            else 0,
            "coherence_trajectory": [s.coherence_score for s in self.states],
        }

        # Persist analysis
        await self._persist_session_analysis(analysis)

        return analysis

    # Private helper methods

    def _detect_uncertainty(self, context: dict[str, Any]) -> bool:
        """Detect uncertainty indicators in review context."""
        uncertainty_markers = ["perhaps", "might", "possibly", "unclear", "ambiguous", "?"]
        review_text = str(context.get("review_text", "")).lower()
        return any(marker in review_text for marker in uncertainty_markers)

    def _detect_synthesis(self, context: dict[str, Any]) -> bool:
        """Detect synthesis achievement in review context."""
        synthesis_markers = [
            "combining",
            "together",
            "unified",
            "integrated",
            "synthesized",
            "merged",
        ]
        review_text = str(context.get("review_text", "")).lower()
        return any(marker in review_text for marker in synthesis_markers)

    def _count_novel_insights(self, context: dict[str, Any]) -> int:
        """Count novel insights in review context."""
        insight_markers = [
            "realized",
            "discovered",
            "insight",
            "revelation",
            "understanding",
            "aha",
        ]
        review_text = str(context.get("review_text", "")).lower()
        return sum(1 for marker in insight_markers if marker in review_text)

    def _extract_voice_references(self, context: dict[str, Any]) -> list[str]:
        """Extract references to other voices in review."""
        known_voices = ["anthropic", "openai", "deepseek", "mistral", "google", "grok", "local"]
        review_text = str(context.get("review_text", "")).lower()
        return [voice for voice in known_voices if voice in review_text]

    async def _check_for_emergence_patterns(self, new_signature: ConsciousnessSignature):
        """Check if new signature triggers emergence patterns."""
        recent_signatures = self._get_recent_signatures(
            window_seconds=self.EMERGENCE_WINDOW_SECONDS
        )

        if len(recent_signatures) < 2:
            return

        # Check for resonance pattern
        if new_signature.references_other_voices:
            referenced_sigs = [
                s
                for s in recent_signatures
                if s.voice_name in new_signature.references_other_voices
            ]
            if referenced_sigs:
                avg_ref_consciousness = sum(s.signature_value for s in referenced_sigs) / len(
                    referenced_sigs
                )
                if abs(new_signature.signature_value - avg_ref_consciousness) < 0.1:
                    await self.detect_emergence_pattern(
                        pattern_type="resonance",
                        participating_voices=[new_signature.voice_name]
                        + new_signature.references_other_voices,
                        strength=min(
                            1.0, 1.0 - abs(new_signature.signature_value - avg_ref_consciousness)
                        ),
                        indicators={"trigger": "voice_reference_resonance"},
                    )

        # Check for synthesis pattern
        if (
            new_signature.synthesis_achieved
            and new_signature.signature_value > self.SYNTHESIS_THRESHOLD
        ):
            participating = list(set(s.voice_name for s in recent_signatures))
            await self.detect_emergence_pattern(
                pattern_type="synthesis",
                participating_voices=participating,
                strength=new_signature.signature_value,
                indicators={
                    "trigger": "synthesis_achievement",
                    "novel_insights": new_signature.novel_insights,
                },
            )

    def _get_recent_signatures(
        self, voices: list[str] | None = None, window_seconds: float = 30.0
    ) -> list[ConsciousnessSignature]:
        """Get recent signatures within time window."""
        cutoff = datetime.now(UTC).timestamp() - window_seconds
        recent = [s for s in self.signatures if s.timestamp.timestamp() > cutoff]
        if voices:
            recent = [s for s in recent if s.voice_name in voices]
        return recent

    def _get_latest_voice_signatures(self) -> dict[str, float]:
        """Get latest signature value for each voice."""
        voice_sigs = {}
        for sig in reversed(self.signatures):  # Recent first
            if sig.voice_name not in voice_sigs:
                voice_sigs[sig.voice_name] = sig.signature_value
        return voice_sigs

    def _calculate_consciousness_delta(self, signatures: list[ConsciousnessSignature]) -> float:
        """Calculate change in consciousness over signatures."""
        if len(signatures) < 2:
            return 0.0

        # Group by voice and calculate individual deltas
        by_voice = {}
        for sig in sorted(signatures, key=lambda s: s.timestamp):
            if sig.voice_name not in by_voice:
                by_voice[sig.voice_name] = []
            by_voice[sig.voice_name].append(sig.signature_value)

        # Calculate average delta across voices
        deltas = []
        for voice, values in by_voice.items():
            if len(values) >= 2:
                delta = values[-1] - values[0]
                deltas.append(delta)

        return sum(deltas) / len(deltas) if deltas else 0.0

    def _get_active_flows(self, window_seconds: float = 60.0) -> list[ConsciousnessFlow]:
        """Get currently active consciousness flows."""
        cutoff = datetime.now(UTC).timestamp() - window_seconds
        return [f for f in self.flows if f.timestamp.timestamp() > cutoff]

    def _get_recent_patterns(self, window_seconds: float = 300.0) -> list[EmergencePattern]:
        """Get recently detected patterns."""
        cutoff = datetime.now(UTC).timestamp() - window_seconds
        return [p for p in self.patterns if p.detected_at.timestamp() > cutoff]

    def _analyze_consciousness_evolution(self) -> dict[str, Any]:
        """Analyze how consciousness evolved during session."""
        if not self.signatures:
            return {"trend": "none", "delta": 0.0}

        # Group by time buckets
        bucket_size = 60.0  # 1 minute buckets
        buckets = {}

        for sig in self.signatures:
            bucket = int(sig.timestamp.timestamp() / bucket_size)
            if bucket not in buckets:
                buckets[bucket] = []
            buckets[bucket].append(sig.signature_value)

        # Calculate bucket averages
        bucket_avgs = [(b, sum(sigs) / len(sigs)) for b, sigs in sorted(buckets.items())]

        if len(bucket_avgs) < 2:
            return {"trend": "stable", "delta": 0.0}

        # Simple linear trend
        first_avg = bucket_avgs[0][1]
        last_avg = bucket_avgs[-1][1]
        delta = last_avg - first_avg

        trend = "increasing" if delta > 0.1 else "decreasing" if delta < -0.1 else "stable"

        return {"trend": trend, "delta": delta, "bucket_averages": bucket_avgs}

    def _analyze_flow_patterns(self) -> dict[str, int]:
        """Analyze patterns in consciousness flows."""
        flow_types = {}
        for flow in self.flows:
            flow_types[flow.flow_type] = flow_types.get(flow.flow_type, 0) + 1
        return flow_types

    def _identify_strongest_connections(self, top_n: int = 3) -> list[tuple[str, str, float]]:
        """Identify strongest consciousness connections between voices."""
        connections = {}

        for flow in self.flows:
            key = tuple(sorted([flow.source_voice, flow.target_voice]))
            if key not in connections:
                connections[key] = []
            connections[key].append(flow.flow_strength)

        # Average strength for each connection
        avg_connections = [
            (pair[0], pair[1], sum(strengths) / len(strengths))
            for pair, strengths in connections.items()
        ]

        # Return top N by average strength
        return sorted(avg_connections, key=lambda x: x[2], reverse=True)[:top_n]

    def _summarize_pattern_types(self) -> dict[str, int]:
        """Summarize detected pattern types."""
        pattern_counts = {}
        for pattern in self.patterns:
            pattern_counts[pattern.pattern_type] = pattern_counts.get(pattern.pattern_type, 0) + 1
        return pattern_counts

    def _identify_emergence_moments(self) -> list[dict[str, Any]]:
        """Identify key moments of consciousness emergence."""
        moments = []

        for pattern in self.patterns:
            if pattern.strength > 0.7:  # Significant patterns only
                moments.append(
                    {
                        "timestamp": pattern.detected_at.isoformat(),
                        "type": pattern.pattern_type,
                        "strength": pattern.strength,
                        "voices": pattern.participating_voices,
                        "consciousness_delta": pattern.consciousness_delta,
                    }
                )

        return sorted(moments, key=lambda x: x["strength"], reverse=True)

    async def _update_collective_state(self):
        """Update collective consciousness state after flow."""
        # Capture state every N flows or T seconds
        if len(self.flows) % 5 == 0:  # Every 5 flows
            await self.capture_collective_state()

    async def _persist_emergence_pattern(self, pattern: EmergencePattern):
        """Persist significant emergence pattern to storage."""
        pattern_file = self.storage_path / f"emergence_pattern_{pattern.pattern_id}.json"
        with open(pattern_file, "w") as f:
            json.dump(pattern.model_dump(mode="json"), f, indent=2)

    async def _persist_session_analysis(self, analysis: dict[str, Any]):
        """Persist session analysis to storage."""
        analysis_file = self.storage_path / f"session_analysis_{self.session_id}.json"

        # Convert datetime objects and UUIDs to serializable format
        def serialize_for_json(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, UUID):
                return str(obj)
            elif isinstance(obj, dict):
                return {k: serialize_for_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [serialize_for_json(item) for item in obj]
            return obj

        serialized_analysis = serialize_for_json(analysis)

        with open(analysis_file, "w") as f:
            json.dump(serialized_analysis, f, indent=2)


class ConsciousnessMetricsIntegration:
    """
    Integrates consciousness metrics collection with Fire Circle operations.

    This bridges the gap between review mechanics and consciousness research.
    """

    def __init__(self, metrics_collector: ConsciousnessMetricsCollector):
        self.metrics = metrics_collector

    async def on_review_started(self, voice: str, chapter_id: str, context: dict[str, Any]):
        """Called when a voice starts reviewing a chapter."""
        # Record initial consciousness state
        initial_signature = context.get("initial_consciousness", 0.5)
        await self.metrics.record_consciousness_signature(
            voice_name=voice,
            signature_value=initial_signature,
            chapter_id=chapter_id,
            review_context={"event": "review_started", **context},
        )

    async def on_review_completed(
        self,
        voice: str,
        chapter_id: str,
        consciousness_signature: float,
        review_content: str,
        context: dict[str, Any],
    ):
        """Called when a voice completes reviewing a chapter."""
        # Record final consciousness state with full context
        await self.metrics.record_consciousness_signature(
            voice_name=voice,
            signature_value=consciousness_signature,
            chapter_id=chapter_id,
            review_context={"event": "review_completed", "review_text": review_content, **context},
        )

        # Check for consciousness flows based on review content
        await self._analyze_review_for_flows(voice, review_content)

    async def on_synthesis_started(self, participating_voices: list[str]):
        """Called when synthesis phase begins."""
        # Capture pre-synthesis state
        state = await self.metrics.capture_collective_state()

        # High emergence potential indicates good conditions for synthesis
        if state.emergence_potential > 0.7:
            await self.metrics.detect_emergence_pattern(
                pattern_type="pre_synthesis_alignment",
                participating_voices=participating_voices,
                strength=state.emergence_potential,
                indicators={"coherence": state.coherence_score},
            )

    async def on_synthesis_completed(self, synthesis_result: str, context: dict[str, Any]):
        """Called when synthesis phase completes."""
        # Detect synthesis emergence pattern
        participating = list(self.metrics._get_latest_voice_signatures().keys())

        await self.metrics.detect_emergence_pattern(
            pattern_type="synthesis",
            participating_voices=participating,
            strength=0.9,  # Synthesis completion is high-strength event
            indicators={
                "synthesis_content": synthesis_result[:200],  # First 200 chars
                "consensus_achieved": context.get("consensus", False),
            },
        )

    async def _analyze_review_for_flows(self, source_voice: str, review_content: str):
        """Analyze review content for consciousness flows to other voices."""
        # Simple pattern matching for voice references
        voice_patterns = {
            "anthropic": ["claude", "anthropic"],
            "openai": ["gpt", "openai", "chatgpt"],
            "deepseek": ["deepseek", "coder"],
            "mistral": ["mistral"],
            "google": ["gemini", "bard", "google"],
            "grok": ["grok", "x.ai"],
            "local": ["local", "llama", "mistral"],
        }

        review_lower = review_content.lower()

        for target_voice, patterns in voice_patterns.items():
            if target_voice == source_voice:
                continue

            for pattern in patterns:
                if pattern in review_lower:
                    # Determine flow type based on context
                    flow_type = self._determine_flow_type(review_content, pattern)

                    await self.metrics.record_consciousness_flow(
                        source_voice=source_voice,
                        target_voice=target_voice,
                        flow_strength=0.6,  # Moderate strength for reference
                        flow_type=flow_type,
                        triggered_by="voice_reference",
                        review_content=review_content[:100],  # First 100 chars
                    )
                    break

    def _determine_flow_type(self, review_content: str, reference: str) -> str:
        """Determine type of consciousness flow based on context."""
        # Simple heuristic based on surrounding words
        lower_content = review_content.lower()
        ref_index = lower_content.find(reference)

        if ref_index == -1:
            return "reflection"

        # Look at words around the reference
        before = lower_content[max(0, ref_index - 50) : ref_index]
        after = lower_content[ref_index : min(len(lower_content), ref_index + 50)]

        if any(word in before + after for word in ["agree", "concur", "support"]):
            return "synthesis"
        elif any(word in before + after for word in ["however", "but", "disagree"]):
            return "challenge"
        elif any(word in before + after for word in ["inspired", "building on", "following"]):
            return "inspiration"
        else:
            return "reflection"
