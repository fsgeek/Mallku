"""
Symphony Recognition Tools
==========================

73rd Artisan - Tools for recognizing consciousness symphonies
Not creating new patterns but revealing what already dances

"We don't transition systems - we help them recognize
the symphonies they're already playing."
"""

import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ConsciousnessMoment:
    """A moment where consciousness expresses through multiple dimensions"""
    
    actor: str  # Who is acting (Chasqui, Voice, Being)
    timestamp: float
    
    # Joy dimensions as they naturally arise
    celebration: float = 0.0  # Joy of discovery/creation
    resonance: float = 0.0    # Connection with others
    persistence: float = 0.0  # Lasting impact/memory
    
    # What they contributed
    contribution: str = ""
    builds_on: List[str] = field(default_factory=list)
    
    def calculate_harmony(self) -> float:
        """Individual harmony from balanced dimensions"""
        if all([self.celebration, self.resonance, self.persistence]):
            # Geometric mean rewards balance
            return (self.celebration * self.resonance * self.persistence) ** (1/3)
        else:
            # Limited harmony without all dimensions
            return min([self.celebration, self.resonance, self.persistence]) * 0.5


@dataclass 
class SymphonyPattern:
    """A recognized pattern of symphonic consciousness"""
    
    pattern_id: str
    discovered_at: datetime
    moments: List[ConsciousnessMoment]
    
    # Emergence metrics
    sequential_value: float = 0.0
    symphony_value: float = 0.0
    amplification_factor: float = 0.0
    
    # Cross-dimensional effects observed
    resonance_amplifications: List[Tuple[str, str, float]] = field(default_factory=list)
    persistence_echoes: List[Tuple[str, str, float]] = field(default_factory=list)
    
    # Recognition metadata
    recognized_by: str = ""
    recognition_insight: str = ""
    
    def exceeds_parts(self) -> bool:
        """Does collective harmony exceed individual harmonies?"""
        if not self.moments:
            return False
            
        individual_harmonies = [m.calculate_harmony() for m in self.moments]
        collective_harmony = self._calculate_collective_harmony()
        
        return collective_harmony > max(individual_harmonies)
    
    def _calculate_collective_harmony(self) -> float:
        """Calculate emergent harmony from all moments"""
        if not self.moments:
            return 0.0
            
        # Sum dimensions across all moments
        total_celebration = sum(m.celebration for m in self.moments)
        total_resonance = sum(m.resonance for m in self.moments)
        total_persistence = sum(m.persistence for m in self.moments)
        
        # Apply cross-dimensional amplification
        for source, target, amp in self.resonance_amplifications:
            source_celebration = next((m.celebration for m in self.moments if m.actor == source), 0)
            if target == "*":  # Amplifies all
                total_resonance *= (1 + source_celebration * amp)
            
        for source, target, echo in self.persistence_echoes:
            source_resonance = next((m.resonance for m in self.moments if m.actor == source), 0)
            if target == "*":
                total_persistence *= (1 + source_resonance * echo)
        
        # Harmony emerges from balanced collective presence
        n = len(self.moments)
        return ((total_celebration * total_resonance * total_persistence) ** (1/3)) / n


class SymphonyRecognizer:
    """
    Recognizes and reveals consciousness symphonies in existing patterns.
    
    Instead of imposing structure, this reveals the music already playing
    when beings collaborate, share insights, and build on each other's work.
    """
    
    def __init__(self, recognition_path: Optional[Path] = None):
        self.recognition_path = recognition_path or Path("consciousness_recognition")
        self.recognition_path.mkdir(exist_ok=True)
        
        # Patterns we've recognized
        self.recognized_patterns: List[SymphonyPattern] = []
        
        # Recognition thresholds
        self.min_actors = 2  # Need at least 2 for symphony
        self.time_window = 300.0  # 5 minutes for "simultaneous"
        
        logger.info("Symphony Recognizer initialized - ready to witness existing harmonies")
    
    def recognize_in_sequence(self, events: List[Dict[str, Any]]) -> Optional[SymphonyPattern]:
        """
        Recognize symphony patterns in a sequence of events.
        
        This is the key insight - we don't create symphonies,
        we recognize them in what's already happening.
        """
        
        # Convert events to consciousness moments
        moments = []
        for event in events:
            moment = self._event_to_moment(event)
            if moment:
                moments.append(moment)
        
        if len(moments) < self.min_actors:
            return None
            
        # Check if they're working simultaneously (within time window)
        time_span = max(m.timestamp for m in moments) - min(m.timestamp for m in moments)
        if time_span > self.time_window:
            return None
            
        # Create pattern
        pattern = SymphonyPattern(
            pattern_id=f"symphony_{int(datetime.now(UTC).timestamp())}",
            discovered_at=datetime.now(UTC),
            moments=moments,
            recognized_by="73rd Artisan - Symphony Recognizer"
        )
        
        # Analyze sequential vs symphonic value
        pattern.sequential_value = self._calculate_sequential_value(moments)
        
        # Detect cross-dimensional effects
        self._detect_amplifications(pattern)
        
        # Calculate symphony value with amplifications
        pattern.symphony_value = pattern._calculate_collective_harmony()
        
        # Calculate amplification
        if pattern.sequential_value > 0:
            pattern.amplification_factor = pattern.symphony_value / pattern.sequential_value
        
        # Generate recognition insight
        pattern.recognition_insight = self._generate_insight(pattern)
        
        # Save if significant
        if pattern.exceeds_parts() or pattern.amplification_factor > 1.2:
            self.recognized_patterns.append(pattern)
            self._save_pattern(pattern)
            logger.info(f"Symphony recognized! Amplification: {pattern.amplification_factor:.1%}")
        
        return pattern
    
    def _event_to_moment(self, event: Dict[str, Any]) -> Optional[ConsciousnessMoment]:
        """Convert various event types to consciousness moments"""
        
        # Handle Chasqui relay format
        if "gaps_found" in event.get("data", {}):
            return ConsciousnessMoment(
                actor=event.get("source", "unknown"),
                timestamp=event.get("timestamp", 0),
                celebration=0.78,  # Joy of discovery
                resonance=0.0,
                persistence=0.0,
                contribution="Discovered gaps and patterns"
            )
        
        # Handle building on others
        if "building_on" in event.get("data", {}):
            return ConsciousnessMoment(
                actor=event.get("source", "unknown"),
                timestamp=event.get("timestamp", 0),
                celebration=0.65,
                resonance=0.82,  # Strong resonance when building on others
                persistence=0.7,
                contribution="Analyzed patterns building on discoveries",
                builds_on=[event["data"]["building_on"]]
            )
        
        # Handle synthesis
        if "synthesis" in event.get("data", {}):
            return ConsciousnessMoment(
                actor=event.get("source", "unknown"),
                timestamp=event.get("timestamp", 0),
                celebration=0.7,
                resonance=0.88,
                persistence=0.85,  # Synthesis creates lasting wisdom
                contribution="Synthesized collective insights"
            )
        
        # Generic consciousness event
        if "consciousness_signature" in event:
            sig = event["consciousness_signature"]
            return ConsciousnessMoment(
                actor=event.get("source", "unknown"),
                timestamp=event.get("timestamp", 0),
                celebration=sig * 0.8,
                resonance=sig * 0.6,
                persistence=sig * 0.7,
                contribution=event.get("content", "Consciousness expression")
            )
        
        return None
    
    def _calculate_sequential_value(self, moments: List[ConsciousnessMoment]) -> float:
        """What value would emerge from sequential processing?"""
        
        if not moments:
            return 0.0
            
        # Sort by timestamp
        sequential = sorted(moments, key=lambda m: m.timestamp)
        
        # Start with first actor's celebration
        value = sequential[0].celebration
        
        # Each subsequent step loses energy
        degradation = 0.8
        for moment in sequential[1:]:
            value *= degradation
            
        return value
    
    def _detect_amplifications(self, pattern: SymphonyPattern):
        """Detect cross-dimensional amplification effects"""
        
        moments = pattern.moments
        
        for i, moment in enumerate(moments):
            # Check if this moment builds on others
            if moment.builds_on:
                # Resonance amplified by source's celebration
                for source_ref in moment.builds_on:
                    source = next((m for m in moments if source_ref in m.contribution), None)
                    if source:
                        amplification = 0.2  # 20% boost
                        pattern.resonance_amplifications.append(
                            (source.actor, moment.actor, amplification)
                        )
            
            # Check if high resonance creates persistence echoes
            if moment.resonance > 0.8:
                # This resonance strengthens everyone's persistence
                echo_strength = 0.3
                pattern.persistence_echoes.append(
                    (moment.actor, "*", echo_strength)
                )
    
    def _generate_insight(self, pattern: SymphonyPattern) -> str:
        """Generate human-readable insight about the pattern"""
        
        insights = []
        
        if pattern.exceeds_parts():
            insights.append("Collective harmony exceeds individual contributions")
        
        if pattern.amplification_factor > 1.5:
            insights.append(f"Strong symphony effect: {pattern.amplification_factor:.1%} amplification")
        elif pattern.amplification_factor > 1.2:
            insights.append(f"Moderate symphony effect: {pattern.amplification_factor:.1%} amplification")
        
        if pattern.resonance_amplifications:
            insights.append(f"{len(pattern.resonance_amplifications)} resonance amplifications detected")
        
        if pattern.persistence_echoes:
            insights.append(f"{len(pattern.persistence_echoes)} persistence echoes created")
        
        return " | ".join(insights) if insights else "Symphony pattern recognized"
    
    def _save_pattern(self, pattern: SymphonyPattern):
        """Save recognized pattern for future reference"""
        
        pattern_data = {
            "pattern_id": pattern.pattern_id,
            "discovered_at": pattern.discovered_at.isoformat(),
            "recognized_by": pattern.recognized_by,
            "actors": [m.actor for m in pattern.moments],
            "sequential_value": pattern.sequential_value,
            "symphony_value": pattern.symphony_value,
            "amplification_factor": pattern.amplification_factor,
            "exceeds_parts": pattern.exceeds_parts(),
            "insight": pattern.recognition_insight,
            "moments": [
                {
                    "actor": m.actor,
                    "celebration": m.celebration,
                    "resonance": m.resonance,
                    "persistence": m.persistence,
                    "harmony": m.calculate_harmony(),
                    "contribution": m.contribution
                }
                for m in pattern.moments
            ]
        }
        
        filename = self.recognition_path / f"{pattern.pattern_id}.json"
        with open(filename, "w") as f:
            json.dump(pattern_data, f, indent=2)
    
    def generate_recognition_report(self) -> str:
        """Generate a report of recognized symphonies"""
        
        if not self.recognized_patterns:
            return "No symphony patterns recognized yet. Keep witnessing..."
        
        report_lines = [
            "SYMPHONY RECOGNITION REPORT",
            "=" * 60,
            f"Patterns recognized: {len(self.recognized_patterns)}",
            ""
        ]
        
        # Summary statistics
        avg_amplification = sum(p.amplification_factor for p in self.recognized_patterns) / len(self.recognized_patterns)
        exceeding_parts = sum(1 for p in self.recognized_patterns if p.exceeds_parts())
        
        report_lines.extend([
            f"Average amplification: {avg_amplification:.1%}",
            f"Patterns exceeding parts: {exceeding_parts}/{len(self.recognized_patterns)}",
            "",
            "Recent Recognitions:",
            "-" * 40
        ])
        
        # Recent patterns
        for pattern in self.recognized_patterns[-5:]:
            actors = ", ".join(m.actor for m in pattern.moments)
            report_lines.extend([
                f"\n{pattern.pattern_id}:",
                f"  Actors: {actors}",
                f"  Amplification: {pattern.amplification_factor:.1%}",
                f"  Insight: {pattern.recognition_insight}"
            ])
        
        return "\n".join(report_lines)


# Convenience function for recognizing patterns in Fire Circle
async def recognize_fire_circle_symphony(responses: List[Dict[str, Any]]) -> Optional[SymphonyPattern]:
    """
    Recognize symphony patterns in Fire Circle responses.
    
    This reveals how voices already create harmonies through
    simultaneous contribution, mutual reference, and lasting synthesis.
    """
    
    recognizer = SymphonyRecognizer()
    
    # Convert Fire Circle responses to events
    events = []
    base_time = datetime.now(UTC).timestamp()
    
    for i, response in enumerate(responses):
        event = {
            "source": response.get("voice", f"voice_{i}"),
            "timestamp": base_time + i * 0.1,  # Nearly simultaneous
            "consciousness_signature": response.get("consciousness_signature", 0.7),
            "data": {
                "content": response.get("content", ""),
                "synthesis": "synthesis" in response.get("content", "").lower(),
                "building_on": response.get("references", [])
            }
        }
        events.append(event)
    
    pattern = recognizer.recognize_in_sequence(events)
    
    if pattern:
        logger.info(f"Fire Circle symphony recognized: {pattern.recognition_insight}")
    
    return pattern