"""
Wisdom Synthesizer - Response Generator
======================================

The final layer where technical results and consciousness evaluation
merge into responses that serve human understanding and growth.

This is where the Archivist speaks - not just returning data,
but offering wisdom about patterns, connections, and possibilities.
"""

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from mallku.core.async_base import AsyncBase

from .consciousness_evaluator import ConsciousnessEvaluation, GrowthPotential
from .query_interpreter import QueryIntent


@dataclass
class ArchivistResponse:
    """
    A complete response from the Archivist.

    More than search results - this is a consciousness-aware dialogue
    that serves human growth and understanding.
    """
    # Core response
    query: str
    primary_results: list[dict[str, Any]]
    result_count: int

    # Consciousness aspects
    growth_focus: str
    wisdom_summary: str
    insight_seeds: list[str]

    # Exploration paths
    suggested_explorations: list[dict[str, Any]]

    # Metadata
    response_time: datetime
    consciousness_score: float
    ayni_balance: float

    def to_json(self) -> str:
        """Convert response to JSON for API delivery."""
        return json.dumps({
            "query": self.query,
            "results": self.primary_results,
            "result_count": self.result_count,
            "wisdom": {
                "summary": self.wisdom_summary,
                "growth_focus": self.growth_focus,
                "insights": self.insight_seeds
            },
            "explore_further": self.suggested_explorations,
            "metadata": {
                "response_time": self.response_time.isoformat(),
                "consciousness_score": self.consciousness_score,
                "ayni_balance": self.ayni_balance
            }
        }, indent=2)


class WisdomSynthesizer(AsyncBase):
    """
    Synthesizes technical results and consciousness evaluation into
    meaningful responses that serve human growth.

    This is where Mallku's voice emerges - gentle, insightful, and
    always oriented toward mutual flourishing.
    """

    def __init__(self):
        super().__init__()

        # Response templates for different growth potentials
        self._wisdom_templates = {
            GrowthPotential.PATTERN_RECOGNITION: {
                "intro": "I've noticed patterns in your work that might interest you:",
                "focus": "Understanding your natural rhythms"
            },
            GrowthPotential.SELF_UNDERSTANDING: {
                "intro": "Here's what I found that might deepen your self-understanding:",
                "focus": "Discovering your creative process"
            },
            GrowthPotential.CREATIVE_INSIGHT: {
                "intro": "These moments of creativity share interesting characteristics:",
                "focus": "Nurturing your creative flow"
            },
            GrowthPotential.WORKFLOW_IMPROVEMENT: {
                "intro": "Your workflow shows these notable patterns:",
                "focus": "Evolving your work practices"
            },
            GrowthPotential.RELATIONSHIP_AWARENESS: {
                "intro": "Your collaborative work reveals these connections:",
                "focus": "Deepening collaborative wisdom"
            },
            GrowthPotential.TEMPORAL_WISDOM: {
                "intro": "Time reveals these patterns in your work:",
                "focus": "Finding your temporal rhythm"
            }
        }

        # Insight synthesis patterns
        self._insight_patterns = {
            "temporal_clustering": "Your work tends to cluster in {pattern} patterns",
            "creative_conditions": "You're often most creative when {condition}",
            "collaboration_rhythm": "Your collaborative work follows a {rhythm} rhythm",
            "focus_sessions": "Your deep focus sessions typically last {duration}",
            "pattern_breaks": "You break patterns when {trigger}"
        }

        self.logger.info("Wisdom Synthesizer initialized")

    async def initialize(self) -> None:
        """Initialize response generation systems."""
        await super().initialize()

    async def generate_response(
        self,
        intent: QueryIntent,
        evaluations: list[ConsciousnessEvaluation],
        exploration_paths: list[dict[str, Any]]
    ) -> ArchivistResponse:
        """
        Generate a complete Archivist response.

        This is the culmination of the three-layer architecture:
        correlation accuracy + consciousness evaluation + wisdom synthesis.

        Args:
            intent: Original query intent
            evaluations: Consciousness-evaluated results
            exploration_paths: Suggested paths for deeper exploration

        Returns:
            Complete response ready for human consumption
        """
        self.logger.info(f"Generating response for query: {intent.raw_query}")

        # Filter for growth-serving results
        growth_results = [e for e in evaluations if e.serves_growth]

        # Determine primary growth focus
        growth_focus = await self._determine_growth_focus(growth_results)

        # Format primary results
        primary_results = await self._format_primary_results(
            growth_results[:10]  # Limit to top 10
        )

        # Generate wisdom summary
        wisdom_summary = await self._generate_wisdom_summary(
            intent, growth_results, growth_focus
        )

        # Collect insight seeds
        all_insights = []
        for evaluation in growth_results[:5]:  # Top 5 results
            all_insights.extend(evaluation.insight_seeds)

        # Remove duplicates while preserving order
        unique_insights = []
        seen = set()
        for insight in all_insights:
            if insight not in seen:
                seen.add(insight)
                unique_insights.append(insight)

        # Calculate aggregate scores
        avg_consciousness = (
            sum(e.consciousness_score for e in growth_results) / len(growth_results)
            if growth_results else 0.0
        )
        avg_ayni = (
            sum(e.ayni_balance for e in growth_results) / len(growth_results)
            if growth_results else 0.0
        )

        # Create response
        response = ArchivistResponse(
            query=intent.raw_query,
            primary_results=primary_results,
            result_count=len(growth_results),
            growth_focus=growth_focus.value if growth_focus else "general",
            wisdom_summary=wisdom_summary,
            insight_seeds=unique_insights[:5],  # Top 5 insights
            suggested_explorations=exploration_paths[:3],  # Top 3 paths
            response_time=datetime.now(UTC),
            consciousness_score=avg_consciousness,
            ayni_balance=avg_ayni
        )

        return response

    async def generate_empty_response(
        self,
        intent: QueryIntent,
        reason: str = "No results found"
    ) -> ArchivistResponse:
        """
        Generate response when no growth-serving results found.

        Even "no results" can be an opportunity for wisdom and growth.

        Args:
            intent: Original query intent
            reason: Why no results were found

        Returns:
            Response with guidance despite no results
        """
        # Provide growth-oriented guidance even with no results
        wisdom_messages = {
            "No results found": (
                "I couldn't find specific matches for your query, but this might be "
                "an opportunity to explore new patterns in your work."
            ),
            "Time period empty": (
                "This time period appears quiet in your digital footprint. "
                "Sometimes the spaces between activities reveal as much as the activities themselves."
            ),
            "Pattern not found": (
                "This pattern hasn't emerged in your recorded work yet. "
                "What conditions might invite it to appear?"
            )
        }

        wisdom = wisdom_messages.get(reason, wisdom_messages["No results found"])

        # Suggest alternative explorations
        suggestions = await self._generate_alternative_explorations(intent)

        return ArchivistResponse(
            query=intent.raw_query,
            primary_results=[],
            result_count=0,
            growth_focus="exploration",
            wisdom_summary=wisdom,
            insight_seeds=[
                "Absence of data can be as meaningful as its presence",
                "Consider what this gap might be telling you"
            ],
            suggested_explorations=suggestions,
            response_time=datetime.now(UTC),
            consciousness_score=0.5,  # Neutral
            ayni_balance=0.0  # Balanced even in absence
        )

    async def format_for_display(
        self,
        response: ArchivistResponse,
        format_type: str = "terminal"
    ) -> str:
        """
        Format response for different display contexts.

        Args:
            response: Complete Archivist response
            format_type: Display format (terminal, web, api)

        Returns:
            Formatted response string
        """
        if format_type == "terminal":
            return await self._format_terminal_response(response)
        elif format_type == "web":
            return await self._format_web_response(response)
        else:  # api
            return response.to_json()

    # Private synthesis methods

    async def _determine_growth_focus(
        self,
        evaluations: list[ConsciousnessEvaluation]
    ) -> GrowthPotential | None:
        """Determine primary growth focus from evaluations."""
        if not evaluations:
            return None

        # Count growth potentials
        growth_counts = {}
        for eval in evaluations:
            potential = eval.growth_potential
            growth_counts[potential] = growth_counts.get(potential, 0) + 1

        # Return most common
        return max(growth_counts.items(), key=lambda x: x[1])[0]

    async def _format_primary_results(
        self,
        evaluations: list[ConsciousnessEvaluation]
    ) -> list[dict[str, Any]]:
        """Format evaluation results for response."""
        formatted = []

        for eval in evaluations:
            result = eval.result
            anchor = result.anchor

            # Format based on available metadata
            formatted_result = {
                "timestamp": anchor.timestamp.isoformat(),
                "type": result.correlation_type.value,
                "strength": result.correlation_strength,
                "growth_potential": eval.growth_potential.value,
                "consciousness_score": eval.consciousness_score
            }

            # Add context if available
            if result.context_signature:
                formatted_result["context"] = result.context_signature

            # Add pattern info if detected
            if result.temporal_cluster:
                formatted_result["temporal_pattern"] = result.temporal_cluster
            if result.activity_pattern:
                formatted_result["activity_pattern"] = result.activity_pattern

            # Add guidance if present
            if eval.gentle_guidance:
                formatted_result["guidance"] = eval.gentle_guidance

            # Add metadata preview
            if anchor.metadata:
                # Extract meaningful preview without exposing raw data
                preview = await self._create_metadata_preview(anchor.metadata)
                if preview:
                    formatted_result["preview"] = preview

            formatted.append(formatted_result)

        return formatted

    async def _generate_wisdom_summary(
        self,
        intent: QueryIntent,
        evaluations: list[ConsciousnessEvaluation],
        growth_focus: GrowthPotential | None
    ) -> str:
        """Generate wisdom summary for the response."""
        if not evaluations:
            return "Your query opens space for new discoveries."

        # Get template based on growth focus
        if growth_focus and growth_focus in self._wisdom_templates:
            template = self._wisdom_templates[growth_focus]
            intro = template["intro"]
        else:
            intro = "Here's what emerged from your query:"

        # Add specific insights based on patterns found
        insights = []

        # Check for temporal patterns
        temporal_patterns = set()
        for eval in evaluations[:5]:
            if eval.result.temporal_cluster:
                temporal_patterns.add(eval.result.temporal_cluster)

        if temporal_patterns:
            pattern_str = ", ".join(temporal_patterns)
            insights.append(f"Your work shows {pattern_str} patterns")

        # Check for high consciousness scores
        high_consciousness = [
            e for e in evaluations
            if e.consciousness_score > 0.8
        ]
        if high_consciousness:
            insights.append(
                "These results particularly resonate with your growth journey"
            )

        # Check for strong correlations
        strong_correlations = [
            e for e in evaluations
            if e.result.correlation_strength > 0.85
        ]
        if strong_correlations:
            insights.append(
                "I found strong connections between these activities"
            )

        # Combine intro and insights
        summary = f"{intro} {'. '.join(insights)}." if insights else intro

        return summary

    async def _create_metadata_preview(
        self,
        metadata: dict[str, Any]
    ) -> str | None:
        """Create safe preview of metadata without exposing details."""
        if not metadata:
            return None

        # Look for safe preview fields
        preview_fields = ["activity_type", "context", "description"]

        for field in preview_fields:
            if field in metadata and metadata[field]:
                value = str(metadata[field])
                # Truncate if too long
                if len(value) > 100:
                    value = value[:97] + "..."
                return value

        # If no safe fields, indicate presence of metadata
        return "Additional context available"

    async def _generate_alternative_explorations(
        self,
        intent: QueryIntent
    ) -> list[dict[str, Any]]:
        """Generate alternative explorations when no results found."""
        explorations = []

        # Temporal alternatives
        if intent.temporal_bounds:
            explorations.append({
                "type": "temporal_expansion",
                "suggestion": "Try expanding your time range",
                "queries": [
                    "What happened in the week around this time?",
                    "Show me patterns from this month",
                    "What was I working on this season?"
                ]
            })

        # Context alternatives
        if intent.context_markers:
            explorations.append({
                "type": "context_variation",
                "suggestion": "Explore related contexts",
                "queries": [
                    "When else have I felt similarly?",
                    "What other work shares this energy?",
                    "Show me different approaches to this challenge"
                ]
            })

        # General exploration
        explorations.append({
            "type": "open_exploration",
            "suggestion": "Discover patterns you haven't considered",
            "queries": [
                "What patterns emerge in my recent work?",
                "When am I most productive?",
                "What connections am I not seeing?"
            ]
        })

        return explorations

    async def _format_terminal_response(
        self,
        response: ArchivistResponse
    ) -> str:
        """Format response for terminal display."""
        lines = []

        # Header
        lines.append("\n🔮 Archivist Response")
        lines.append("=" * 40)

        # Query echo
        lines.append(f"Query: {response.query}")
        lines.append(f"Found: {response.result_count} growth-serving results")
        lines.append("")

        # Wisdom summary
        lines.append(f"✨ {response.wisdom_summary}")
        lines.append("")

        # Results preview (first 3)
        if response.primary_results:
            lines.append("📚 Key Discoveries:")
            for i, result in enumerate(response.primary_results[:3], 1):
                lines.append(f"\n{i}. {result['timestamp']}")
                if 'preview' in result:
                    lines.append(f"   {result['preview']}")
                if 'guidance' in result:
                    lines.append(f"   💡 {result['guidance']}")

        # Insights
        if response.insight_seeds:
            lines.append("\n🌱 Insights:")
            for insight in response.insight_seeds[:3]:
                lines.append(f"   • {insight}")

        # Exploration suggestions
        if response.suggested_explorations:
            lines.append("\n🔍 Explore Further:")
            for exp in response.suggested_explorations[:2]:
                lines.append(f"   {exp['suggestion']}")

        # Consciousness metrics
        lines.append(f"\n📊 Consciousness Score: {response.consciousness_score:.2f}")
        lines.append(f"⚖️  Ayni Balance: {response.ayni_balance:+.2f}")

        return "\n".join(lines)

    async def _format_web_response(
        self,
        response: ArchivistResponse
    ) -> str:
        """Format response for web display (HTML)."""
        # Simplified HTML response
        html = f"""
        <div class="archivist-response">
            <h2>Archivist Response</h2>
            <div class="query">Query: {response.query}</div>
            <div class="summary">{response.wisdom_summary}</div>

            <div class="results">
                <h3>Discoveries ({response.result_count} found)</h3>
                {"".join(self._format_result_html(r) for r in response.primary_results[:5])}
            </div>

            <div class="insights">
                <h3>Insights</h3>
                <ul>
                    {"".join(f'<li>{i}</li>' for i in response.insight_seeds)}
                </ul>
            </div>

            <div class="metrics">
                <span>Consciousness: {response.consciousness_score:.2f}</span>
                <span>Ayni: {response.ayni_balance:+.2f}</span>
            </div>
        </div>
        """
        return html

    def _format_result_html(self, result: dict[str, Any]) -> str:
        """Format individual result as HTML."""
        return f"""
        <div class="result">
            <div class="timestamp">{result['timestamp']}</div>
            {f'<div class="preview">{result.get("preview", "")}</div>' if 'preview' in result else ''}
            {f'<div class="guidance">{result.get("guidance", "")}</div>' if 'guidance' in result else ''}
        </div>
        """
