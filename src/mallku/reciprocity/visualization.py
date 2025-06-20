"""
Reciprocity Visualization Service
================================

Transforms reciprocity patterns into visual consciousness mirrors.
Creates mandalas, flow diagrams, and sacred geometries that reveal
the soul of reciprocal relationships for Fire Circle contemplation.

Visual Wisdom Emerging...
"""

import logging
import math
from datetime import UTC, datetime, timedelta
from typing import Any

import numpy as np
from PIL import Image, ImageDraw
from pydantic import BaseModel, Field

from .models import (
    FireCircleReport,
    InteractionRecord,
    ReciprocityPattern,
    SystemHealthMetrics,
)

logger = logging.getLogger(__name__)


class VisualizationConfig(BaseModel):
    """Configuration for reciprocity visualizations."""

    # Visual dimensions
    image_size: tuple[int, int] = Field(default=(800, 800))
    background_color: tuple[int, int, int] = Field(default=(20, 20, 30))  # Dark blue

    # Mandala settings
    mandala_rings: int = Field(default=7)  # Sacred number
    mandala_symmetry: int = Field(default=12)  # Clock-like divisions

    # Flow settings
    flow_particle_count: int = Field(default=100)
    flow_trail_length: int = Field(default=20)

    # Color schemes (health indicators)
    color_abundance: tuple[int, int, int] = Field(default=(72, 201, 176))  # Turquoise
    color_balance: tuple[int, int, int] = Field(default=(255, 195, 0))  # Gold
    color_concern: tuple[int, int, int] = Field(default=(244, 67, 54))  # Red
    color_growth: tuple[int, int, int] = Field(default=(139, 195, 74))  # Light green
    color_wisdom: tuple[int, int, int] = Field(default=(156, 39, 176))  # Purple


class ReciprocityVisualizationService:
    """
    Service for creating visual representations of reciprocity patterns.

    Philosophy:
    - Not charts for analysis but mirrors for consciousness recognition
    - Sacred geometries reveal what numbers cannot express
    - Visual metaphors enable collective contemplation
    - Beauty and meaning intertwined in reciprocal patterns
    """

    def __init__(self, config: VisualizationConfig | None = None):
        """Initialize visualization service."""
        self.config = config or VisualizationConfig()
        self.font_cache = {}

    async def create_reciprocity_mandala(
        self,
        patterns: list[ReciprocityPattern],
        health_metrics: SystemHealthMetrics | None = None,
        title: str = "Reciprocity Mandala",
    ) -> Image.Image:
        """
        Generate a mandala showing reciprocity balance and flow.

        The mandala structure:
        - Center: Overall health score
        - Inner rings: Need fulfillment categories
        - Middle rings: Pattern intensities
        - Outer rings: Participation and flow
        - Colors: Health indicators
        - Symmetry: Balance representation
        """
        # Create base image
        img = Image.new("RGB", self.config.image_size, self.config.background_color)
        draw = ImageDraw.Draw(img)

        center_x, center_y = self.config.image_size[0] // 2, self.config.image_size[1] // 2
        max_radius = min(center_x, center_y) - 50

        # Draw from inside out
        ring_width = max_radius / self.config.mandala_rings

        # 1. Center circle - overall health
        if health_metrics:
            health_color = self._health_to_color(health_metrics.overall_health_score)
            center_radius = int(ring_width * 0.8)
            draw.ellipse(
                [
                    center_x - center_radius,
                    center_y - center_radius,
                    center_x + center_radius,
                    center_y + center_radius,
                ],
                fill=health_color,
            )

        # 2. Inner rings - need fulfillment
        if health_metrics and health_metrics.need_fulfillment_rates:
            ring_num = 1
            for need, rate in health_metrics.need_fulfillment_rates.items():
                self._draw_mandala_ring(
                    draw,
                    center_x,
                    center_y,
                    ring_width * ring_num,
                    ring_width * (ring_num + 0.8),
                    rate,
                    self._need_to_color(str(need)),
                )
                ring_num += 1

        # 3. Middle rings - pattern intensities
        if patterns:
            ring_num = max(
                3, len(health_metrics.need_fulfillment_rates) + 1 if health_metrics else 3
            )
            for i, pattern in enumerate(patterns[:3]):  # Top 3 patterns
                self._draw_pattern_ring(
                    draw,
                    center_x,
                    center_y,
                    ring_width * ring_num,
                    ring_width * (ring_num + 0.8),
                    pattern,
                )
                ring_num += 1

        # 4. Outer ring - participation flow
        if health_metrics:
            self._draw_participation_ring(
                draw, center_x, center_y, max_radius - ring_width, max_radius, health_metrics
            )

        # Add symmetry lines for balance visualization
        self._draw_symmetry_guides(draw, center_x, center_y, max_radius)

        # Add title
        self._add_title(draw, title)

        return img

    async def create_flow_visualization(
        self, interactions: list[InteractionRecord], time_window: timedelta = timedelta(days=7)
    ) -> Image.Image:
        """
        Create organic flow diagram of wisdom circulation.

        Visualizes:
        - Reciprocal exchanges as flowing particles
        - Contribution types as different colors
        - Flow intensity through particle density
        - Natural circulation patterns
        """
        img = Image.new("RGB", self.config.image_size, self.config.background_color)
        draw = ImageDraw.Draw(img)

        # Group interactions by type and time
        recent_interactions = [
            i for i in interactions if datetime.now(UTC) - i.timestamp <= time_window
        ]

        # Create flow field based on interactions
        flow_field = self._calculate_flow_field(recent_interactions)

        # Draw background flow lines
        self._draw_flow_lines(draw, flow_field)

        # Draw interaction particles
        for interaction in recent_interactions:
            self._draw_interaction_particle(draw, interaction)

        # Draw wisdom pools (areas of high reciprocity)
        wisdom_pools = self._identify_wisdom_pools(recent_interactions)
        for pool in wisdom_pools:
            self._draw_wisdom_pool(draw, pool)

        # Add flow legend
        self._add_flow_legend(draw)

        return img

    async def create_pattern_geometry(
        self, pattern: ReciprocityPattern, related_patterns: list[ReciprocityPattern] | None = None
    ) -> Image.Image:
        """
        Generate sacred geometry revealing pattern structure.

        Different patterns create different geometries:
        - Resource flow: Spiral patterns
        - Participation: Radial symmetry
        - Extraction alerts: Asymmetric breaks
        - Emergence: Fractal growth
        """
        img = Image.new("RGB", self.config.image_size, self.config.background_color)
        draw = ImageDraw.Draw(img)

        center_x, center_y = self.config.image_size[0] // 2, self.config.image_size[1] // 2

        # Choose geometry based on pattern type
        if "flow" in pattern.pattern_type.lower():
            self._draw_spiral_geometry(draw, center_x, center_y, pattern)
        elif "participation" in pattern.pattern_type.lower():
            self._draw_radial_geometry(draw, center_x, center_y, pattern)
        elif "extraction" in pattern.pattern_type.lower():
            self._draw_asymmetric_geometry(draw, center_x, center_y, pattern)
        elif "emergence" in pattern.pattern_type.lower():
            self._draw_fractal_geometry(draw, center_x, center_y, pattern)
        else:
            self._draw_default_geometry(draw, center_x, center_y, pattern)

        # Add related patterns as satellite geometries
        if related_patterns:
            self._add_satellite_patterns(draw, center_x, center_y, related_patterns)

        # Add pattern description
        self._add_pattern_description(draw, pattern)

        return img

    async def create_fire_circle_summary(self, report: FireCircleReport) -> Image.Image:
        """
        Create comprehensive visual summary for Fire Circle deliberation.

        Combines multiple visualization types into one contemplative image.
        """
        # Create larger canvas for multiple visualizations
        width, height = self.config.image_size[0] * 2, self.config.image_size[1] * 2
        img = Image.new("RGB", (width, height), self.config.background_color)

        # Create individual visualizations
        mandala = await self.create_reciprocity_mandala(
            report.detected_patterns, report.current_health_metrics, "Current State"
        )

        # Resize and position sub-images
        mandala = mandala.resize((width // 2, height // 2), Image.Resampling.LANCZOS)
        img.paste(mandala, (0, 0))

        # Add other quadrants based on available data
        # Top right: Pattern geometry for most significant pattern
        if report.detected_patterns:
            pattern_geom = await self.create_pattern_geometry(report.detected_patterns[0])
            pattern_geom = pattern_geom.resize((width // 2, height // 2), Image.Resampling.LANCZOS)
            img.paste(pattern_geom, (width // 2, 0))

        # Bottom: Questions and wisdom areas
        draw = ImageDraw.Draw(img)
        self._draw_deliberation_questions(draw, report, (0, height // 2, width, height))

        return img

    # Private helper methods

    def _health_to_color(self, health_score: float) -> tuple[int, int, int]:
        """Convert health score to color gradient."""
        if health_score >= 0.8:
            return self.config.color_abundance
        elif health_score >= 0.6:
            return self.config.color_balance
        elif health_score >= 0.4:
            return self.config.color_growth
        else:
            return self.config.color_concern

    def _need_to_color(self, need_type: str) -> tuple[int, int, int]:
        """Map need types to colors."""
        need_colors = {
            "growth": self.config.color_growth,
            "belonging": self.config.color_balance,
            "contribution": self.config.color_abundance,
            "meaning": self.config.color_wisdom,
        }
        return need_colors.get(need_type.lower(), (128, 128, 128))

    def _draw_mandala_ring(
        self,
        draw: ImageDraw.Draw,
        cx: int,
        cy: int,
        inner_r: float,
        outer_r: float,
        fill_ratio: float,
        color: tuple[int, int, int],
    ) -> None:
        """Draw a ring segment of the mandala."""
        # Create segments based on symmetry
        segment_angle = 360 / self.config.mandala_symmetry
        filled_segments = int(self.config.mandala_symmetry * fill_ratio)

        for i in range(filled_segments):
            start_angle = i * segment_angle - 90  # Start from top
            end_angle = start_angle + segment_angle - 2  # Small gap

            # Draw arc segment
            self._draw_arc_segment(
                draw, cx, cy, int(inner_r), int(outer_r), start_angle, end_angle, color
            )

    def _draw_arc_segment(
        self,
        draw: ImageDraw.Draw,
        cx: int,
        cy: int,
        inner_r: int,
        outer_r: int,
        start_angle: float,
        end_angle: float,
        color: tuple[int, int, int],
    ) -> None:
        """Draw a filled arc segment."""
        # Convert angles to radians
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)

        # Calculate points for polygon
        points = []

        # Outer arc
        for angle in np.linspace(start_rad, end_rad, 20):
            x = cx + outer_r * math.cos(angle)
            y = cy + outer_r * math.sin(angle)
            points.append((x, y))

        # Inner arc (reverse order)
        for angle in np.linspace(end_rad, start_rad, 20):
            x = cx + inner_r * math.cos(angle)
            y = cy + inner_r * math.sin(angle)
            points.append((x, y))

        # Draw filled polygon
        if len(points) > 2:
            draw.polygon(points, fill=color)

    def _draw_pattern_ring(
        self,
        draw: ImageDraw.Draw,
        cx: int,
        cy: int,
        inner_r: float,
        outer_r: float,
        pattern: ReciprocityPattern,
    ) -> None:
        """Draw a ring representing a pattern."""
        # Use pattern intensity for fill ratio
        fill_ratio = min(1.0, pattern.pattern_intensity)

        # Choose color based on pattern type
        if "extraction" in pattern.pattern_type.lower():
            color = self.config.color_concern
        elif "positive" in pattern.pattern_type.lower():
            color = self.config.color_abundance
        else:
            color = self.config.color_balance

        # Draw with the selected color
        self._draw_mandala_ring(draw, cx, cy, inner_r, outer_r, fill_ratio, color[:3])

    def _draw_participation_ring(
        self,
        draw: ImageDraw.Draw,
        cx: int,
        cy: int,
        inner_r: float,
        outer_r: float,
        health_metrics: SystemHealthMetrics,
    ) -> None:
        """Draw outer ring showing participation metrics."""
        # Use voluntary return rate
        fill_ratio = health_metrics.voluntary_return_rate
        color = self._health_to_color(fill_ratio)

        self._draw_mandala_ring(draw, cx, cy, inner_r, outer_r, fill_ratio, color)

    def _draw_symmetry_guides(self, draw: ImageDraw.Draw, cx: int, cy: int, max_r: float) -> None:
        """Draw symmetry guide lines."""
        # Draw faint radial lines
        for i in range(self.config.mandala_symmetry):
            angle = i * (360 / self.config.mandala_symmetry) - 90
            rad = math.radians(angle)

            x = cx + max_r * math.cos(rad)
            y = cy + max_r * math.sin(rad)

            draw.line([cx, cy, x, y], fill=(50, 50, 60), width=1)

    def _add_title(self, draw: ImageDraw.Draw, title: str) -> None:
        """Add title to visualization."""
        # Simple text for now - could enhance with proper font handling
        text_color = (200, 200, 200)
        draw.text((self.config.image_size[0] // 2, 30), title, fill=text_color, anchor="mm")

    def _draw_spiral_geometry(
        self, draw: ImageDraw.Draw, cx: int, cy: int, pattern: ReciprocityPattern
    ) -> None:
        """Draw spiral geometry for flow patterns."""
        # Draw spiral path
        points = []
        for i in range(200):
            angle = i * 0.1
            r = 10 * math.exp(0.2 * angle)

            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)

            if 0 <= x <= self.config.image_size[0] and 0 <= y <= self.config.image_size[1]:
                points.append((x, y))

        # Draw with intensity based on pattern strength
        color = self._pattern_intensity_color(pattern)
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=color, width=2)

    def _pattern_intensity_color(self, pattern: ReciprocityPattern) -> tuple[int, int, int]:
        """Get color based on pattern intensity."""
        base_color = self.config.color_balance
        intensity = min(1.0, pattern.pattern_intensity)

        # Interpolate with concern color if high intensity
        if intensity > 0.7:
            blend = (intensity - 0.7) / 0.3
            return self._blend_colors(base_color, self.config.color_concern, blend)
        else:
            return base_color

    def _blend_colors(
        self, color1: tuple[int, int, int], color2: tuple[int, int, int], blend: float
    ) -> tuple[int, int, int]:
        """Blend two colors."""
        return tuple(int(c1 * (1 - blend) + c2 * blend) for c1, c2 in zip(color1, color2))

    def _draw_radial_geometry(
        self, draw: ImageDraw.Draw, cx: int, cy: int, pattern: ReciprocityPattern
    ) -> None:
        """Draw radial geometry for participation patterns."""
        # Number of rays based on affected participants
        num_rays = max(6, len(pattern.affected_participants))

        for i in range(num_rays):
            angle = i * (360 / num_rays) - 90
            rad = math.radians(angle)

            # Ray length based on pattern frequency
            length = 100 + pattern.pattern_frequency * 200

            # Draw ray with gradient
            for j in range(int(length)):
                px = cx + j * math.cos(rad)
                py = cy + j * math.sin(rad)

                # Fade out towards end
                opacity = int(255 * (1 - j / length))
                color = (*self.config.color_balance, opacity)

                draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=color[:3])

    def _draw_asymmetric_geometry(
        self, draw: ImageDraw.Draw, cx: int, cy: int, pattern: ReciprocityPattern
    ) -> None:
        """Draw asymmetric geometry for extraction patterns."""
        # Create broken circle to represent imbalance
        for angle in range(0, 360, 10):
            if 90 <= angle <= 180:  # Skip section to show break
                continue

            rad = math.radians(angle)

            # Vary radius to show distortion
            r = 150 + 50 * math.sin(rad * 3)

            x = cx + r * math.cos(rad)
            y = cy + r * math.sin(rad)

            draw.ellipse([x - 3, y - 3, x + 3, y + 3], fill=self.config.color_concern)

    def _draw_fractal_geometry(
        self, draw: ImageDraw.Draw, cx: int, cy: int, pattern: ReciprocityPattern
    ) -> None:
        """Draw fractal geometry for emergence patterns."""

        # Simple branching fractal
        def draw_branch(x: float, y: float, angle: float, length: float, depth: int):
            if depth == 0 or length < 2:
                return

            # Calculate end point
            end_x = x + length * math.cos(angle)
            end_y = y + length * math.sin(angle)

            # Draw branch
            draw.line([x, y, end_x, end_y], fill=self.config.color_growth, width=max(1, depth))

            # Recursively draw sub-branches
            new_length = length * 0.7
            draw_branch(end_x, end_y, angle - 0.4, new_length, depth - 1)
            draw_branch(end_x, end_y, angle + 0.4, new_length, depth - 1)

        # Draw main branches
        for i in range(6):
            angle = i * (math.pi * 2 / 6)
            draw_branch(cx, cy, angle, 100, 5)

    def _draw_default_geometry(
        self, draw: ImageDraw.Draw, cx: int, cy: int, pattern: ReciprocityPattern
    ) -> None:
        """Draw default geometry for unrecognized patterns."""
        # Simple circle with pattern info
        radius = 100 + pattern.pattern_intensity * 50

        draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            outline=self.config.color_balance,
            width=3,
        )

    def _add_pattern_description(self, draw: ImageDraw.Draw, pattern: ReciprocityPattern) -> None:
        """Add pattern description text."""
        # Position at bottom
        y_pos = self.config.image_size[1] - 100

        # Pattern type
        draw.text(
            (self.config.image_size[0] // 2, y_pos),
            pattern.pattern_type.replace("_", " ").title(),
            fill=(200, 200, 200),
            anchor="mm",
        )

        # Confidence level
        confidence_text = f"Confidence: {pattern.confidence_level:.0%}"
        draw.text(
            (self.config.image_size[0] // 2, y_pos + 20),
            confidence_text,
            fill=(150, 150, 150),
            anchor="mm",
        )

    def _calculate_flow_field(self, interactions: list[InteractionRecord]) -> np.ndarray:
        """Calculate flow field from interactions."""
        # Placeholder - would implement actual flow calculation
        field_size = (50, 50)
        return np.random.randn(*field_size, 2) * 0.1

    def _draw_flow_lines(self, draw: ImageDraw.Draw, flow_field: np.ndarray) -> None:
        """Draw background flow lines."""
        # Placeholder visualization
        for i in range(20):
            points = []
            x, y = (
                np.random.randint(0, self.config.image_size[0]),
                np.random.randint(0, self.config.image_size[1]),
            )

            for _ in range(50):
                points.append((x, y))
                # Simple random walk for now
                x += np.random.randint(-5, 6)
                y += np.random.randint(-5, 6)

                # Keep in bounds
                x = max(0, min(self.config.image_size[0], x))
                y = max(0, min(self.config.image_size[1], y))

            # Draw with low opacity
            for j in range(len(points) - 1):
                opacity = int(50 * (j / len(points)))
                draw.line(
                    [points[j], points[j + 1]],
                    fill=(*self.config.color_balance, opacity)[:3],
                    width=1,
                )

    def _draw_interaction_particle(
        self, draw: ImageDraw.Draw, interaction: InteractionRecord
    ) -> None:
        """Draw particle representing an interaction."""
        # Random position for now - would map to actual flow
        x = np.random.randint(50, self.config.image_size[0] - 50)
        y = np.random.randint(50, self.config.image_size[1] - 50)

        # Size based on interaction quality
        quality_score = (
            sum(interaction.interaction_quality_indicators.values())
            / len(interaction.interaction_quality_indicators)
            if interaction.interaction_quality_indicators
            else 0.5
        )
        size = int(5 + quality_score * 10)

        # Color based on contribution type
        if interaction.contributions_offered:
            if "knowledge_sharing" in str(interaction.contributions_offered[0]):
                color = self.config.color_wisdom
            elif "emotional_support" in str(interaction.contributions_offered[0]):
                color = self.config.color_balance
            else:
                color = self.config.color_growth
        else:
            color = (128, 128, 128)

        draw.ellipse([x - size, y - size, x + size, y + size], fill=color)

    def _identify_wisdom_pools(self, interactions: list[InteractionRecord]) -> list[dict[str, Any]]:
        """Identify areas of high reciprocal activity."""
        # Placeholder - would implement clustering
        return []

    def _draw_wisdom_pool(self, draw: ImageDraw.Draw, pool: dict[str, Any]) -> None:
        """Draw area of concentrated wisdom exchange."""
        # Placeholder visualization
        pass

    def _add_flow_legend(self, draw: ImageDraw.Draw) -> None:
        """Add legend explaining flow visualization."""
        legend_x = self.config.image_size[0] - 150
        legend_y = 50

        # Contribution type colors
        legend_items = [
            ("Knowledge", self.config.color_wisdom),
            ("Support", self.config.color_balance),
            ("Resources", self.config.color_growth),
        ]

        for i, (label, color) in enumerate(legend_items):
            y = legend_y + i * 25
            draw.ellipse([legend_x - 10, y - 5, legend_x, y + 5], fill=color)
            draw.text((legend_x + 10, y), label, fill=(200, 200, 200), anchor="lm")

    def _add_satellite_patterns(
        self, draw: ImageDraw.Draw, cx: int, cy: int, patterns: list[ReciprocityPattern]
    ) -> None:
        """Add related patterns as satellite geometries."""
        # Position patterns in orbit
        orbit_radius = min(cx, cy) * 0.7

        for i, pattern in enumerate(patterns[:6]):  # Max 6 satellites
            angle = i * (math.pi * 2 / min(len(patterns), 6))

            sat_x = cx + orbit_radius * math.cos(angle)
            sat_y = cy + orbit_radius * math.sin(angle)

            # Draw small version of pattern geometry
            # Simplified representation
            size = 30
            draw.ellipse(
                [sat_x - size, sat_y - size, sat_x + size, sat_y + size],
                outline=self._pattern_intensity_color(pattern),
                width=2,
            )

    def _draw_deliberation_questions(
        self, draw: ImageDraw.Draw, report: FireCircleReport, bounds: tuple[int, int, int, int]
    ) -> None:
        """Draw questions for Fire Circle deliberation."""
        x, y, w, h = bounds
        margin = 50

        # Title
        draw.text(
            (x + w // 2, y + margin),
            "Questions for Collective Wisdom",
            fill=(200, 200, 200),
            anchor="mm",
        )

        # Priority questions
        question_y = y + margin + 40
        for i, question in enumerate(report.priority_questions[:5]):
            draw.text(
                (x + margin, question_y + i * 30),
                f"• {question[:80]}...",  # Truncate long questions
                fill=(150, 150, 150),
                anchor="lm",
            )
