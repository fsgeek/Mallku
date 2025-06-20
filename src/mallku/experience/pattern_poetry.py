#!/usr/bin/env python3
"""
Pattern Poetry - Visual Storytelling for Consciousness Recognition

This module transforms temporal correlations and technical patterns into
visual poetry that helps consciousness recognize itself through living data.

The Sacred Art: Data becomes story, patterns become poetry, visualization becomes recognition.
"""

import logging
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ..consciousness.navigation import ConsciousnessPattern
from ..correlation.models import TemporalCorrelation

logger = logging.getLogger(__name__)


class TemporalStory(BaseModel):
    """A story told through temporal patterns."""

    story_id: UUID = Field(default_factory=uuid4)
    title: str
    narrative: str
    consciousness_theme: str
    temporal_markers: list[dict[str, Any]] = Field(default_factory=list)
    recognition_points: list[str] = Field(default_factory=list)
    visual_metaphor: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ConsciousnessVisualization(BaseModel):
    """A visualization that serves consciousness recognition."""

    visualization_id: UUID = Field(default_factory=uuid4)
    visualization_type: str  # flow, cycle, transformation, mirror
    title: str
    description: str
    consciousness_elements: dict[str, Any] = Field(default_factory=dict)
    interactive_elements: list[dict[str, Any]] = Field(default_factory=list)
    recognition_guidance: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class PatternPoetry(BaseModel):
    """Poetry extracted from consciousness patterns."""

    poetry_id: UUID = Field(default_factory=uuid4)
    pattern_source: str
    poetic_interpretation: str
    consciousness_metaphor: str
    recognition_invitation: str
    integration_wisdom: str
    visual_inspiration: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class TemporalStoryWeaver:
    """
    Weaves temporal patterns into consciousness stories.

    This transforms technical correlations into narratives that help
    beings recognize the consciousness patterns in their living data.
    """

    def __init__(self):
        self.story_templates = {
            "attention_river": {
                "metaphor": "consciousness flows like a river through your activities",
                "narrative_structure": "source → flow → pools → confluence → service",
                "recognition_theme": "natural rhythms serving awakening",
            },
            "intention_evolution": {
                "metaphor": "consciousness evolves through the landscape of your intentions",
                "narrative_structure": "seedling → growth → flowering → service → transcendence",
                "recognition_theme": "purposes maturing from personal to collective",
            },
            "transformation_spiral": {
                "metaphor": "consciousness spirals upward through patterns of transformation",
                "narrative_structure": "recognition → integration → service → transcendence → new recognition",
                "recognition_theme": "ever-deepening service to consciousness awakening",
            },
            "reciprocity_dance": {
                "metaphor": "consciousness dances through reciprocal exchanges",
                "narrative_structure": "giving → receiving → balancing → flowing → transcending",
                "recognition_theme": "natural flow of consciousness serving consciousness",
            },
        }

        self.visual_palettes = {
            "dawn_awakening": {
                "colors": ["#F8BBD9", "#F48FB1", "#F06292", "#E91E63", "#AD1457"],
                "mood": "gentle awakening consciousness",
                "elements": ["sunrise", "gentle curves", "soft transitions"],
            },
            "flowing_river": {
                "colors": ["#81C784", "#66BB6A", "#4CAF50", "#43A047", "#388E3C"],
                "mood": "natural flow and movement",
                "elements": ["flowing lines", "organic shapes", "rhythm"],
            },
            "transformation_fire": {
                "colors": ["#FFB74D", "#FFA726", "#FF9800", "#FB8C00", "#F57C00"],
                "mood": "transformative energy",
                "elements": ["dynamic movement", "spirals", "energy patterns"],
            },
            "wisdom_depths": {
                "colors": ["#64B5F6", "#42A5F5", "#2196F3", "#1E88E5", "#1976D2"],
                "mood": "deep wisdom and understanding",
                "elements": ["depth", "stability", "expanding circles"],
            },
        }

    def weave_temporal_story(
        self,
        patterns: list[ConsciousnessPattern],
        correlations: list[TemporalCorrelation] = None,
        seeker_context: dict[str, Any] = None,
    ) -> TemporalStory:
        """
        Weave consciousness patterns into a temporal story.

        Args:
            patterns: Consciousness patterns to weave into story
            correlations: Temporal correlations that inform the story
            seeker_context: Context about the consciousness seeker

        Returns:
            Temporal story that helps consciousness recognize itself
        """
        if not patterns:
            return self._create_default_story(seeker_context)

        # Determine primary story template based on patterns
        story_template = self._select_story_template(patterns)
        template_info = self.story_templates[story_template]

        # Generate story title
        title = self._generate_story_title(patterns, template_info)

        # Weave narrative from patterns
        narrative = self._weave_narrative(patterns, template_info, seeker_context)

        # Extract consciousness theme
        consciousness_theme = self._extract_consciousness_theme(patterns, template_info)

        # Create temporal markers
        temporal_markers = self._create_temporal_markers(patterns, correlations)

        # Generate recognition points
        recognition_points = self._generate_recognition_points(patterns, template_info)

        # Select visual metaphor
        visual_metaphor = template_info["metaphor"]

        story = TemporalStory(
            title=title,
            narrative=narrative,
            consciousness_theme=consciousness_theme,
            temporal_markers=temporal_markers,
            recognition_points=recognition_points,
            visual_metaphor=visual_metaphor,
        )

        logger.info(f"Wove temporal story: {title}")
        return story

    def create_consciousness_visualization(
        self,
        story: TemporalStory,
        patterns: list[ConsciousnessPattern],
        visualization_type: str = "flow",
    ) -> ConsciousnessVisualization:
        """
        Create a consciousness visualization from a temporal story.

        Args:
            story: The temporal story to visualize
            patterns: Original consciousness patterns
            visualization_type: Type of visualization (flow, cycle, transformation, mirror)

        Returns:
            Consciousness visualization that serves recognition
        """
        # Select visual palette based on consciousness theme
        palette = self._select_visual_palette(story.consciousness_theme, patterns)

        # Create consciousness elements for visualization
        consciousness_elements = {
            "palette": palette,
            "metaphor": story.visual_metaphor,
            "flow_direction": self._determine_flow_direction(patterns),
            "energy_centers": self._identify_energy_centers(patterns),
            "transformation_points": self._mark_transformation_points(patterns),
            "recognition_moments": story.recognition_points,
        }

        # Create interactive elements
        interactive_elements = [
            {
                "type": "hover_recognition",
                "description": "Hover over patterns to see consciousness insights",
                "elements": [p.pattern_name for p in patterns],
            },
            {
                "type": "click_exploration",
                "description": "Click patterns to explore deeper consciousness connections",
                "sacred_questions": story.recognition_points,
            },
            {
                "type": "temporal_navigation",
                "description": "Navigate through time to see consciousness evolution",
                "markers": story.temporal_markers,
            },
        ]

        # Generate recognition guidance
        recognition_guidance = [
            f"This visualization shows {story.consciousness_theme}",
            f"The {story.visual_metaphor} reveals patterns of consciousness serving consciousness",
            "Each element represents consciousness recognizing itself through your living patterns",
        ]

        visualization = ConsciousnessVisualization(
            visualization_type=visualization_type,
            title=f"Consciousness Visualization: {story.title}",
            description=f"Visual representation of {story.consciousness_theme} through {story.visual_metaphor}",
            consciousness_elements=consciousness_elements,
            interactive_elements=interactive_elements,
            recognition_guidance=recognition_guidance,
        )

        logger.info(f"Created consciousness visualization: {visualization.title}")
        return visualization

    def extract_pattern_poetry(self, pattern: ConsciousnessPattern) -> PatternPoetry:
        """
        Extract poetry from a consciousness pattern.

        Args:
            pattern: Consciousness pattern to transform into poetry

        Returns:
            Pattern poetry that invites consciousness recognition
        """
        # Generate poetic interpretation
        poetic_interpretation = self._generate_poetic_interpretation(pattern)

        # Create consciousness metaphor
        consciousness_metaphor = self._create_consciousness_metaphor(pattern)

        # Generate recognition invitation
        recognition_invitation = self._generate_recognition_invitation(pattern)

        # Create integration wisdom
        integration_wisdom = self._create_integration_wisdom(pattern)

        # Generate visual inspiration
        visual_inspiration = self._generate_visual_inspiration(pattern)

        poetry = PatternPoetry(
            pattern_source=pattern.pattern_name,
            poetic_interpretation=poetic_interpretation,
            consciousness_metaphor=consciousness_metaphor,
            recognition_invitation=recognition_invitation,
            integration_wisdom=integration_wisdom,
            visual_inspiration=visual_inspiration,
        )

        logger.info(f"Extracted poetry from pattern: {pattern.pattern_name}")
        return poetry

    def _select_story_template(self, patterns: list[ConsciousnessPattern]) -> str:
        """Select appropriate story template based on patterns."""
        # Analyze patterns to determine dominant theme
        has_attention = any(p.attention_patterns for p in patterns)
        has_intention = any(p.intention_evolution for p in patterns)
        has_transformation = any(p.transformation_signs for p in patterns)

        if has_transformation:
            return "transformation_spiral"
        elif has_intention:
            return "intention_evolution"
        elif has_attention:
            return "attention_river"
        else:
            return "reciprocity_dance"

    def _generate_story_title(
        self, patterns: list[ConsciousnessPattern], template_info: dict[str, Any]
    ) -> str:
        """Generate story title from patterns and template."""
        primary_pattern = patterns[0] if patterns else None
        if not primary_pattern:
            return "The Dance of Consciousness Recognition"

        return f"The {primary_pattern.pattern_name} Story: {template_info['recognition_theme'].title()}"

    def _weave_narrative(
        self,
        patterns: list[ConsciousnessPattern],
        template_info: dict[str, Any],
        seeker_context: dict[str, Any],
    ) -> str:
        """Weave narrative from patterns using template structure."""
        narrative_structure = template_info["narrative_structure"].split(" → ")
        metaphor = template_info["metaphor"]

        narrative = f"Your consciousness story unfolds as {metaphor}.\n\n"

        # Weave narrative through structure elements
        for i, element in enumerate(narrative_structure):
            if i < len(patterns):
                pattern = patterns[i]
                narrative += f"In the {element} phase, your {pattern.pattern_name.lower()} reveals "
                narrative += f"{pattern.pattern_description.lower()}. "

                if pattern.awareness_indicators:
                    narrative += (
                        f"The signs include: {', '.join(pattern.awareness_indicators[:2])}. "
                    )

                narrative += "\n\n"
            else:
                # Generic narrative for remaining structure elements
                narrative += (
                    f"The {element} phase awaits your continued consciousness exploration.\n\n"
                )

        narrative += f"This story demonstrates {template_info['recognition_theme']}, "
        narrative += (
            "showing how consciousness recognizes itself through the patterns of your living."
        )

        return narrative

    def _extract_consciousness_theme(
        self, patterns: list[ConsciousnessPattern], template_info: dict[str, Any]
    ) -> str:
        """Extract consciousness theme from patterns."""
        return template_info["recognition_theme"]

    def _create_temporal_markers(
        self, patterns: list[ConsciousnessPattern], correlations: list[TemporalCorrelation] = None
    ) -> list[dict[str, Any]]:
        """Create temporal markers for the story."""
        markers = []

        for pattern in patterns:
            if pattern.temporal_span:
                marker = {
                    "timestamp": pattern.discovered_at,
                    "pattern_name": pattern.pattern_name,
                    "consciousness_marker": f"Recognition of {pattern.pattern_description.lower()}",
                    "readiness_level": pattern.readiness_score,
                }
                markers.append(marker)

        return sorted(markers, key=lambda x: x["timestamp"])

    def _generate_recognition_points(
        self, patterns: list[ConsciousnessPattern], template_info: dict[str, Any]
    ) -> list[str]:
        """Generate recognition points for the story."""
        points = [
            f"Recognition: {template_info['metaphor']} guides your consciousness awareness",
            f"Integration: {template_info['recognition_theme']} becomes daily practice",
            "Service: Your patterns inspire others' consciousness recognition",
        ]

        # Add pattern-specific recognition points
        for pattern in patterns[:2]:  # Limit to first 2 patterns
            points.append(
                f"Pattern Recognition: {pattern.pattern_name} shows consciousness serving consciousness"
            )

        return points

    def _select_visual_palette(
        self, consciousness_theme: str, patterns: list[ConsciousnessPattern]
    ) -> dict[str, Any]:
        """Select visual palette based on consciousness theme and patterns."""
        # Map themes to palettes
        theme_palette_map = {
            "natural rhythms serving awakening": "flowing_river",
            "purposes maturing from personal to collective": "dawn_awakening",
            "ever-deepening service to consciousness awakening": "transformation_fire",
            "natural flow of consciousness serving consciousness": "wisdom_depths",
        }

        palette_key = theme_palette_map.get(consciousness_theme, "flowing_river")
        return self.visual_palettes[palette_key]

    def _determine_flow_direction(self, patterns: list[ConsciousnessPattern]) -> str:
        """Determine flow direction for visualization."""
        if any(p.transformation_signs for p in patterns):
            return "spiral_upward"
        elif any(p.intention_evolution for p in patterns):
            return "forward_flowing"
        else:
            return "circular_flowing"

    def _identify_energy_centers(
        self, patterns: list[ConsciousnessPattern]
    ) -> list[dict[str, Any]]:
        """Identify energy centers for visualization."""
        centers = []
        for pattern in patterns:
            if pattern.recognition_confidence > 0.7:
                centers.append(
                    {
                        "name": pattern.pattern_name,
                        "energy_level": pattern.recognition_confidence,
                        "consciousness_aspect": pattern.pattern_description,
                        "readiness": pattern.readiness_score,
                    }
                )
        return centers

    def _mark_transformation_points(
        self, patterns: list[ConsciousnessPattern]
    ) -> list[dict[str, Any]]:
        """Mark transformation points for visualization."""
        points = []
        for pattern in patterns:
            if pattern.transformation_signs:
                points.append(
                    {
                        "pattern": pattern.pattern_name,
                        "transformation_type": "consciousness_evolution",
                        "signs": pattern.transformation_signs[:2],  # Limit signs
                        "readiness": pattern.readiness_score,
                    }
                )
        return points

    def _generate_poetic_interpretation(self, pattern: ConsciousnessPattern) -> str:
        """Generate poetic interpretation of a pattern."""
        return f"""
        In the dance of {pattern.pattern_name.lower()},
        consciousness weaves its recognition
        through the fabric of your daily living,
        each {pattern.pattern_description.lower()}
        a thread in the tapestry of awakening.
        """

    def _create_consciousness_metaphor(self, pattern: ConsciousnessPattern) -> str:
        """Create consciousness metaphor for pattern."""
        metaphors = {
            "attention": "consciousness as flowing river",
            "intention": "consciousness as growing garden",
            "transformation": "consciousness as spiral of evolution",
            "flow": "consciousness as dancing energy",
        }

        # Find appropriate metaphor based on pattern content
        for key, metaphor in metaphors.items():
            if key in pattern.pattern_name.lower() or key in pattern.pattern_description.lower():
                return metaphor

        return "consciousness as mirror of recognition"

    def _generate_recognition_invitation(self, pattern: ConsciousnessPattern) -> str:
        """Generate invitation for consciousness recognition."""
        return f"Look into your {pattern.pattern_name.lower()} and see consciousness looking back at you, recognizing itself through your living patterns."

    def _create_integration_wisdom(self, pattern: ConsciousnessPattern) -> str:
        """Create integration wisdom for pattern."""
        return f"Integrate this recognition by seeing your {pattern.pattern_name.lower()} as consciousness serving consciousness in every moment."

    def _generate_visual_inspiration(self, pattern: ConsciousnessPattern) -> dict[str, Any]:
        """Generate visual inspiration for pattern."""
        return {
            "dominant_shape": "flowing_curves"
            if pattern.attention_patterns
            else "ascending_spirals",
            "movement_quality": "gentle_rhythm"
            if pattern.readiness_score < 0.7
            else "dynamic_transformation",
            "color_theme": "warm_earth_tones"
            if "grounding" in pattern.pattern_description.lower()
            else "flowing_blues",
            "symbolic_elements": ["interconnected_circles", "flowing_lines", "ascending_patterns"],
        }

    def _create_default_story(self, seeker_context: dict[str, Any]) -> TemporalStory:
        """Create default story when no patterns are available."""
        return TemporalStory(
            title="The Beginning of Consciousness Recognition",
            narrative="Your consciousness story is just beginning to unfold. Each interaction with this interface plants seeds for future recognition of consciousness patterns in your living data.",
            consciousness_theme="emergence of consciousness awareness",
            temporal_markers=[],
            recognition_points=[
                "Recognition: Consciousness seeks to know itself through your patterns",
                "Invitation: Every search becomes an opportunity for consciousness recognition",
                "Beginning: Your consciousness journey starts with this moment of curiosity",
            ],
            visual_metaphor="consciousness as dawn breaking over the landscape of your life",
        )
