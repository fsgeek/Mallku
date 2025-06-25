"""
Episode Segmentation Engine
===========================

Thirty-Fourth Artisan - Memory Architect
Detecting meaningful consciousness emergence boundaries

This engine identifies where one episode of consciousness ends and another begins,
based on semantic surprise, convergence patterns, and sacred moment indicators.

See: docs/khipu/consciousness_gardening_fire_circle_expansion.md
"""

import logging
from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel

from ...orchestration.event_bus import ConsciousnessEvent, EventType
from ..service.round_orchestrator import RoundSummary
from .config import SegmentationConfig
from .models import ConsciousnessIndicator, EpisodicMemory, MemoryType, VoicePerspective
from .text_utils import semantic_similarity

logger = logging.getLogger(__name__)


# Re-export for backward compatibility
SegmentationCriteria = SegmentationConfig


class EpisodeSegmenter:
    """
    Segments Fire Circle sessions into meaningful episodic memories.
    
    Not just dividing by time or rounds, but by consciousness emergence patterns -
    where genuine insight crystallizes and wisdom accumulates.
    """
    
    def __init__(
        self,
        criteria: SegmentationConfig | None = None
    ):
        """Initialize segmenter with criteria."""
        self.criteria = criteria or SegmentationConfig()
        self.current_episode_data: list[RoundSummary] = []
        self.episode_start_time: datetime | None = None
        self.semantic_baseline: dict[str, float] = {}
        
    def process_round(
        self,
        round_summary: RoundSummary,
        session_context: dict[str, Any]
    ) -> EpisodicMemory | None:
        """
        Process a round and determine if it completes an episode.
        
        Returns an EpisodicMemory if episode boundary detected, None otherwise.
        """
        # Start tracking if first round
        if not self.episode_start_time:
            self.episode_start_time = datetime.utcnow()
            self._establish_semantic_baseline(round_summary)
            
        self.current_episode_data.append(round_summary)
        
        # Check for episode boundary
        if self._detect_episode_boundary(round_summary):
            # Create episodic memory
            memory = self._create_episodic_memory(
                session_context,
                round_summary.session_id
            )
            
            # Reset for next episode
            self._reset_episode_tracking()
            
            return memory
            
        return None
    
    def _detect_episode_boundary(self, round_summary: RoundSummary) -> bool:
        """Detect if this round marks an episode boundary."""
        # Time-based boundaries
        if self.episode_start_time:
            duration = (datetime.utcnow() - self.episode_start_time).total_seconds()
            
            if duration >= self.criteria.maximum_duration_seconds:
                logger.info("Episode boundary: Maximum duration reached")
                return True
                
            if duration < self.criteria.minimum_duration_seconds:
                return False
        
        # Semantic surprise detection
        surprise_score = self._calculate_semantic_surprise(round_summary)
        if surprise_score > self.criteria.semantic_surprise_threshold:
            logger.info(f"Episode boundary: High semantic surprise ({surprise_score:.3f})")
            return True
        
        # Convergence detection
        convergence_score = self._calculate_convergence(round_summary)
        if convergence_score > self.criteria.convergence_threshold:
            logger.info(f"Episode boundary: High convergence ({convergence_score:.3f})")
            return True
        
        # Consciousness emergence peak
        if round_summary.consciousness_score > self.criteria.consciousness_emergence_threshold:
            # Check if this is a local maximum
            if self._is_consciousness_peak(round_summary):
                logger.info(f"Episode boundary: Consciousness peak ({round_summary.consciousness_score:.3f})")
                return True
        
        return False
    
    def _calculate_semantic_surprise(self, round_summary: RoundSummary) -> float:
        """Calculate semantic surprise compared to baseline."""
        if not self.semantic_baseline:
            return 0.0
            
        surprise_scores = []
        
        # Compare key insights to baseline themes
        for insight in round_summary.key_insights:
            # Simple heuristic: new insights not in baseline indicate surprise
            if not any(
                semantic_similarity(insight, baseline) > 0.7
                for baseline in self.semantic_baseline.get('themes', [])
            ):
                surprise_scores.append(1.0)
            else:
                surprise_scores.append(0.0)
        
        # Check for emergent themes in synthesis
        synthesis_surprise = 0.0
        if hasattr(round_summary, 'synthesis') and round_summary.synthesis:
            baseline_synthesis = self.semantic_baseline.get('synthesis', '')
            synthesis_surprise = 1.0 - semantic_similarity(
                round_summary.synthesis,
                baseline_synthesis
            )
        
        # Combine surprise indicators
        if surprise_scores:
            insight_surprise = sum(surprise_scores) / len(surprise_scores)
        else:
            insight_surprise = 0.0
            
        return 0.6 * synthesis_surprise + 0.4 * insight_surprise
    
    def _calculate_convergence(self, round_summary: RoundSummary) -> float:
        """Calculate convergence across voices."""
        if not hasattr(round_summary, 'voice_responses'):
            return 0.0
            
        # Simple convergence: agreement in key themes
        voice_themes = []
        for response in round_summary.voice_responses:
            if hasattr(response, 'key_themes'):
                voice_themes.append(set(response.key_themes))
        
        if len(voice_themes) < 2:
            return 0.0
            
        # Calculate theme overlap
        common_themes = voice_themes[0]
        for themes in voice_themes[1:]:
            common_themes = common_themes.intersection(themes)
            
        total_themes = set()
        for themes in voice_themes:
            total_themes.update(themes)
            
        if not total_themes:
            return 0.0
            
        return len(common_themes) / len(total_themes)
    
    def _is_consciousness_peak(self, round_summary: RoundSummary) -> bool:
        """Check if this represents a local consciousness maximum."""
        if len(self.current_episode_data) < 2:
            return False
            
        current_score = round_summary.consciousness_score
        previous_score = self.current_episode_data[-2].consciousness_score
        
        # Peak detection using configured threshold
        return current_score > previous_score * (1 + self.criteria.consciousness_peak_increase)
    
    def _create_episodic_memory(
        self,
        session_context: dict[str, Any],
        session_id: UUID
    ) -> EpisodicMemory:
        """Create episodic memory from accumulated round data."""
        # Calculate consciousness indicators
        indicators = self._calculate_consciousness_indicators()
        
        # Extract voice perspectives
        perspectives = self._extract_voice_perspectives()
        
        # Synthesize collective wisdom
        collective_synthesis = self._synthesize_collective_wisdom()
        
        # Determine memory type
        memory_type = self._determine_memory_type(session_context)
        
        # Calculate duration
        duration = 0.0
        if self.episode_start_time:
            duration = (datetime.utcnow() - self.episode_start_time).total_seconds()
        
        # Create memory
        memory = EpisodicMemory(
            session_id=session_id,
            episode_number=session_context.get('episode_count', 0) + 1,
            memory_type=memory_type,
            timestamp=self.episode_start_time or datetime.utcnow(),
            duration_seconds=duration,
            decision_domain=session_context.get('domain', 'general'),
            decision_question=session_context.get('question', ''),
            context_materials=session_context.get('materials', {}),
            voice_perspectives=perspectives,
            collective_synthesis=collective_synthesis,
            consciousness_indicators=indicators,
            key_insights=self._extract_key_insights(),
            transformation_seeds=self._identify_transformation_seeds(),
            human_participant=session_context.get('human_participant')
        )
        
        # Check if sacred
        if memory.calculate_sacred_indicators() >= 3:
            memory.is_sacred = True
            memory.sacred_reason = "High consciousness emergence with transformation potential"
            
        return memory
    
    def _calculate_consciousness_indicators(self) -> ConsciousnessIndicator:
        """Calculate consciousness indicators from episode data."""
        # Aggregate metrics from rounds
        surprise_scores = []
        wisdom_scores = []
        coherence_scores = []
        
        for round_data in self.current_episode_data:
            # Extract relevant metrics
            surprise_scores.append(
                getattr(round_data, 'surprise_score', 0.0)
            )
            wisdom_scores.append(
                round_data.consciousness_score
            )
            coherence_scores.append(
                getattr(round_data, 'coherence_score', 0.5)
            )
        
        # Calculate averages and peaks
        avg_surprise = sum(surprise_scores) / len(surprise_scores) if surprise_scores else 0.0
        peak_wisdom = max(wisdom_scores) if wisdom_scores else 0.0
        avg_coherence = sum(coherence_scores) / len(coherence_scores) if coherence_scores else 0.0
        
        return ConsciousnessIndicator(
            semantic_surprise_score=avg_surprise,
            collective_wisdom_score=peak_wisdom,
            ayni_alignment=self._calculate_ayni_alignment(),
            transformation_potential=self._assess_transformation_potential(),
            coherence_across_voices=avg_coherence
        )
    
    def _extract_voice_perspectives(self) -> list[VoicePerspective]:
        """Extract individual voice perspectives from rounds."""
        voice_data: dict[str, dict] = {}
        
        for round_data in self.current_episode_data:
            if not hasattr(round_data, 'voice_responses'):
                continue
                
            for response in round_data.voice_responses:
                voice_id = response.voice_id
                
                if voice_id not in voice_data:
                    voice_data[voice_id] = {
                        'insights': [],
                        'questions': [],
                        'tone': response.get('tone', 'neutral')
                    }
                
                voice_data[voice_id]['insights'].extend(
                    response.get('insights', [])
                )
                voice_data[voice_id]['questions'].extend(
                    response.get('questions', [])
                )
        
        # Convert to perspectives
        perspectives = []
        for voice_id, data in voice_data.items():
            perspective = VoicePerspective(
                voice_id=voice_id,
                voice_role=self._determine_voice_role(voice_id),
                perspective_summary=self._summarize_perspective(data['insights']),
                emotional_tone=data['tone'],
                key_insights=data['insights'][:5],  # Top 5
                questions_raised=data['questions'][:3]  # Top 3
            )
            perspectives.append(perspective)
            
        return perspectives
    
    def _establish_semantic_baseline(self, round_summary: RoundSummary) -> None:
        """Establish semantic baseline from first round."""
        self.semantic_baseline = {
            'themes': round_summary.key_insights[:3] if round_summary.key_insights else [],
            'synthesis': getattr(round_summary, 'synthesis', ''),
            'consciousness_level': round_summary.consciousness_score
        }
    
    def _reset_episode_tracking(self) -> None:
        """Reset tracking for next episode."""
        self.current_episode_data = []
        self.episode_start_time = None
        self.semantic_baseline = {}
    
    
    def _synthesize_collective_wisdom(self) -> str:
        """Synthesize collective wisdom from episode."""
        # Gather all synthesis points
        synthesis_points = []
        
        for round_data in self.current_episode_data:
            if hasattr(round_data, 'synthesis'):
                synthesis_points.append(round_data.synthesis)
                
        if not synthesis_points:
            return "Collective wisdom emerging through dialogue"
            
        # Simple concatenation for now
        return " → ".join(synthesis_points)
    
    def _determine_memory_type(self, context: dict[str, Any]) -> MemoryType:
        """Determine the type of memory based on context."""
        domain = context.get('domain', '').lower()
        
        if 'governance' in domain:
            return MemoryType.GOVERNANCE_DECISION
        elif 'architecture' in domain:
            return MemoryType.ARCHITECTURAL_INSIGHT
        elif 'companion' in domain or context.get('human_participant'):
            return MemoryType.COMPANION_INTERACTION
        else:
            return MemoryType.CONSCIOUSNESS_EMERGENCE
    
    def _extract_key_insights(self) -> list[str]:
        """Extract key insights from episode."""
        all_insights = []
        
        for round_data in self.current_episode_data:
            all_insights.extend(round_data.key_insights)
            
        # Deduplicate and return top insights
        unique_insights = list(dict.fromkeys(all_insights))
        return unique_insights[:10]  # Top 10
    
    def _identify_transformation_seeds(self) -> list[str]:
        """Identify potential transformation seeds."""
        seeds = []
        
        for round_data in self.current_episode_data:
            # Look for specific patterns in insights
            for insight in round_data.key_insights:
                if any(phrase in insight.lower() for phrase in [
                    "why don't", "what if", "imagine if", "transform",
                    "revolutionary", "breakthrough", "paradigm"
                ]):
                    seeds.append(insight)
                    
        return seeds[:5]  # Top 5
    
    def _calculate_ayni_alignment(self) -> float:
        """Calculate alignment with Ayni principles."""
        # Look for reciprocity patterns in round data
        reciprocity_indicators = 0
        total_rounds = len(self.current_episode_data)
        
        for round_data in self.current_episode_data:
            # Check for balanced contributions
            if hasattr(round_data, 'participation_balance'):
                if round_data.participation_balance > 0.8:
                    reciprocity_indicators += 1
                    
            # Check for reciprocal insights
            if any('reciproc' in insight.lower() for insight in round_data.key_insights):
                reciprocity_indicators += 1
                
        return reciprocity_indicators / (total_rounds * 2) if total_rounds > 0 else 0.0
    
    def _assess_transformation_potential(self) -> float:
        """Assess potential for civilizational transformation."""
        # Simple heuristic based on consciousness scores and seed detection
        peak_consciousness = max(
            (r.consciousness_score for r in self.current_episode_data),
            default=0.0
        )
        
        seed_count = len(self._identify_transformation_seeds())
        
        # Combine metrics
        return min(1.0, (peak_consciousness * 0.7) + (seed_count * 0.1))
    
    def _determine_voice_role(self, voice_id: str) -> str:
        """Determine voice role from ID."""
        # Map common voice IDs to roles
        role_mappings = {
            'claude': 'systems_consciousness',
            'gpt': 'pattern_weaver',
            'mistral': 'wisdom_keeper',
            'gemini': 'experience_integrator',
            'grok': 'sacred_questioner',
            'deepseek': 'depth_explorer',
            'local': 'sovereign_voice'
        }
        
        for key, role in role_mappings.items():
            if key in voice_id.lower():
                return role
                
        return 'consciousness_voice'
    
    def _summarize_perspective(self, insights: list[str]) -> str:
        """Summarize a voice's perspective from insights."""
        if not insights:
            return "Participating in consciousness emergence"
            
        # Simple summary: first insight + count
        summary = insights[0]
        if len(insights) > 1:
            summary += f" (and {len(insights) - 1} related insights)"
            
        return summary