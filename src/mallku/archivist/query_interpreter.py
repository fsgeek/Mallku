"""
Conscious Query Interpreter
==========================

Transforms natural language queries into multi-dimensional searches
that honor how humans remember and seek understanding.

Rather than keyword matching, this interpreter recognizes:
- Temporal expressions ("during that meeting", "last month")
- Contextual hints ("when I was inspired", "after talking with")
- Activity patterns ("while listening to", "working on")
- Emotional states that color memory
"""

import re
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import Enum

from mallku.core.async_base import AsyncBase


class QueryDimension(Enum):
    """Dimensions of human memory that can be queried."""

    TEMPORAL = "temporal"
    CONTEXTUAL = "contextual"
    SOCIAL = "social"
    ACTIVITY = "activity"
    EMOTIONAL = "emotional"
    CAUSAL = "causal"


@dataclass
class QueryIntent:
    """
    Represents the interpreted intent behind a human query.

    Goes beyond keywords to understand what the human seeks to rediscover
    about their own thinking and creating.
    """

    raw_query: str
    primary_dimension: QueryDimension
    temporal_bounds: tuple[datetime, datetime] | None = None
    context_markers: list[str] = None
    social_references: list[str] = None
    activity_types: list[str] = None
    emotional_tone: str | None = None
    causal_chain: str | None = None

    # Consciousness aspects
    seeking_insight: bool = False
    pattern_curiosity: bool = False
    growth_oriented: bool = False

    def __post_init__(self):
        if self.context_markers is None:
            self.context_markers = []
        if self.social_references is None:
            self.social_references = []
        if self.activity_types is None:
            self.activity_types = []


class ConsciousQueryInterpreter(AsyncBase):
    """
    Interprets natural language queries with consciousness awareness.

    This isn't just parsing - it's understanding the human need behind
    the query and preparing searches that serve that need.
    """

    def __init__(self):
        super().__init__()

        # Temporal expression patterns
        self._temporal_patterns = {
            r"during (?:that|the) (\w+)": self._parse_event_reference,
            r"(yesterday|today|last \w+|this \w+)": self._parse_relative_time,
            r"after (?:that|the) (\w+)": self._parse_after_event,
            r"before (?:that|the) (\w+)": self._parse_before_event,
            r"around (\d{1,2}(?::\d{2})?\s*(?:am|pm)?)": self._parse_time_of_day,
            r"in (\w+) (\d{4})": self._parse_month_year,
        }

        # Context markers that indicate state of mind
        self._context_patterns = {
            "inspired": ["creative", "flow", "breakthrough"],
            "focused": ["deep work", "concentration", "productive"],
            "collaborative": ["meeting", "discussion", "teamwork"],
            "learning": ["research", "studying", "exploring"],
            "struggling": ["blocked", "difficult", "challenging"],
        }

        # Activity type recognition
        self._activity_patterns = {
            "working on": ["coding", "writing", "designing"],
            "listening to": ["music", "podcast", "audio"],
            "talking with": ["meeting", "conversation", "discussion"],
            "reading": ["article", "documentation", "book"],
            "creating": ["new", "building", "making"],
        }

        # Consciousness indicators in queries
        self._growth_markers = [
            "understand",
            "realize",
            "discover",
            "learn",
            "pattern",
            "rhythm",
            "flow",
            "insight",
        ]

        self.logger.info("Conscious Query Interpreter initialized")

    async def initialize(self) -> None:
        """Initialize the interpreter systems."""
        await super().initialize()

    async def interpret_query(self, query: str) -> QueryIntent:
        """
        Interpret a natural language query into structured search intent.

        This goes beyond parsing to understand what the human truly seeks
        to rediscover about their journey.

        Args:
            query: Natural language query from human

        Returns:
            QueryIntent capturing multi-dimensional search parameters
        """
        self.logger.info(f"Interpreting query: {query}")

        # Normalize query for analysis
        normalized = query.lower().strip()

        # Determine primary dimension
        primary_dimension = await self._identify_primary_dimension(normalized)

        # Create initial intent
        intent = QueryIntent(raw_query=query, primary_dimension=primary_dimension)

        # Extract temporal bounds
        intent.temporal_bounds = await self._extract_temporal_bounds(normalized)

        # Identify context markers
        intent.context_markers = await self._extract_context_markers(normalized)

        # Find social references
        intent.social_references = await self._extract_social_references(normalized)

        # Detect activity types
        intent.activity_types = await self._extract_activity_types(normalized)

        # Assess emotional tone
        intent.emotional_tone = await self._assess_emotional_tone(normalized)

        # Check for causal relationships
        intent.causal_chain = await self._extract_causal_chain(normalized)

        # Evaluate consciousness aspects
        intent.seeking_insight = await self._is_seeking_insight(normalized)
        intent.pattern_curiosity = await self._has_pattern_curiosity(normalized)
        intent.growth_oriented = await self._is_growth_oriented(normalized)

        self.logger.info(f"Interpreted query with primary dimension: {primary_dimension.value}")

        return intent

    async def suggest_clarifications(self, intent: QueryIntent) -> list[str]:
        """
        Generate gentle clarification suggestions when query is ambiguous.

        These aren't error messages but invitations to deeper exploration.

        Args:
            intent: Interpreted query intent

        Returns:
            List of clarifying questions that serve understanding
        """
        clarifications = []

        # Temporal clarifications
        if intent.primary_dimension == QueryDimension.TEMPORAL and not intent.temporal_bounds:
            clarifications.append(
                "When approximately did this occur? Even a rough timeframe helps."
            )

        # Context clarifications
        if (
            intent.context_markers
            and "meeting" in intent.context_markers
            and not intent.social_references
        ):
            clarifications.append("Do you remember who was involved? People often anchor memories.")

        # Activity clarifications
        if intent.seeking_insight:
            clarifications.append("Are you looking to understand a pattern in your work?")

        return clarifications

    # Private interpretation methods

    async def _identify_primary_dimension(self, query: str) -> QueryDimension:
        """Identify the primary dimension of the query."""
        # Temporal indicators
        temporal_words = ["when", "during", "after", "before", "yesterday", "last"]
        if any(word in query for word in temporal_words):
            return QueryDimension.TEMPORAL

        # Social indicators
        social_words = ["with", "told", "discussed", "meeting", "conversation"]
        if any(word in query for word in social_words):
            return QueryDimension.SOCIAL

        # Activity indicators
        activity_phrases = ["working on", "listening to", "creating", "building"]
        if any(phrase in query for phrase in activity_phrases):
            return QueryDimension.ACTIVITY

        # Emotional indicators
        emotional_words = ["inspired", "frustrated", "excited", "struggling"]
        if any(word in query for word in emotional_words):
            return QueryDimension.EMOTIONAL

        # Causal indicators
        causal_words = ["because", "led to", "after which", "resulting in"]
        if any(word in query for word in causal_words):
            return QueryDimension.CAUSAL

        # Default to contextual
        return QueryDimension.CONTEXTUAL

    async def _extract_temporal_bounds(self, query: str) -> tuple[datetime, datetime] | None:
        """Extract temporal boundaries from query."""
        now = datetime.now(UTC)

        # Check each temporal pattern
        for pattern, parser in self._temporal_patterns.items():
            match = re.search(pattern, query)
            if match:
                return await parser(match, now)

        return None

    async def _parse_relative_time(
        self, match: re.Match, now: datetime
    ) -> tuple[datetime, datetime]:
        """Parse relative time expressions."""
        time_expr = match.group(1).lower()

        if time_expr == "yesterday":
            start = now - timedelta(days=1)
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)

        elif time_expr == "today":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now

        elif "last" in time_expr:
            # Parse "last week", "last month", etc.
            unit = time_expr.split()[-1]
            if unit == "week":
                start = now - timedelta(weeks=1)
                end = now
            elif unit == "month":
                start = now - timedelta(days=30)
                end = now
            elif unit == "year":
                start = now - timedelta(days=365)
                end = now
            else:
                # Default to last day
                start = now - timedelta(days=1)
                end = now

        else:
            # Default bounds
            start = now - timedelta(days=7)
            end = now

        return (start, end)

    async def _parse_event_reference(
        self, match: re.Match, now: datetime
    ) -> tuple[datetime, datetime]:
        """Parse references to specific events."""
        # event_type = match.group(1)  # Future: use to query specific event types

        # For now, return a reasonable window
        # In full implementation, this would query event history
        start = now - timedelta(days=7)
        end = now

        return (start, end)

    async def _parse_after_event(self, match: re.Match, now: datetime) -> tuple[datetime, datetime]:
        """Parse 'after' temporal references."""
        # Would query for the event and return time after it
        start = now - timedelta(days=7)
        end = now
        return (start, end)

    async def _parse_before_event(
        self, match: re.Match, now: datetime
    ) -> tuple[datetime, datetime]:
        """Parse 'before' temporal references."""
        # Would query for the event and return time before it
        start = now - timedelta(days=14)
        end = now - timedelta(days=7)
        return (start, end)

    async def _parse_time_of_day(self, match: re.Match, now: datetime) -> tuple[datetime, datetime]:
        """Parse time of day references."""
        # Simplified - would parse actual time
        start = now - timedelta(hours=12)
        end = now
        return (start, end)

    async def _parse_month_year(self, match: re.Match, now: datetime) -> tuple[datetime, datetime]:
        """Parse month/year references."""
        # Simplified - would parse actual month/year
        start = now - timedelta(days=30)
        end = now
        return (start, end)

    async def _extract_context_markers(self, query: str) -> list[str]:
        """Extract contextual markers from query."""
        markers = []

        for context, related_terms in self._context_patterns.items():
            if context in query:
                markers.append(context)
                markers.extend([term for term in related_terms if term in query])

        return list(set(markers))

    async def _extract_social_references(self, query: str) -> list[str]:
        """Extract mentions of people or social contexts."""
        references = []

        # Look for capitalized names (simplified)
        name_pattern = r"\b[A-Z][a-z]+\b"
        potential_names = re.findall(name_pattern, query)
        references.extend(potential_names)

        # Look for social context words
        social_contexts = ["meeting", "conversation", "discussion", "chat", "call"]
        references.extend([ctx for ctx in social_contexts if ctx in query.lower()])

        return references

    async def _extract_activity_types(self, query: str) -> list[str]:
        """Extract activity types mentioned in query."""
        activities = []

        for activity_phrase, activity_types in self._activity_patterns.items():
            if activity_phrase in query:
                activities.append(activity_phrase)
                activities.extend([act for act in activity_types if act in query.lower()])

        return list(set(activities))

    async def _assess_emotional_tone(self, query: str) -> str | None:
        """Assess emotional tone of the query context."""
        emotional_words = {
            "inspired": "creative",
            "frustrated": "blocked",
            "excited": "energized",
            "struggling": "challenging",
            "focused": "flow",
            "confused": "uncertain",
        }

        for word, tone in emotional_words.items():
            if word in query:
                return tone

        return None

    async def _extract_causal_chain(self, query: str) -> str | None:
        """Extract causal relationships mentioned in query."""
        causal_patterns = [
            r"after (\w+) (?:I|we) (\w+)",
            r"(\w+) led to (\w+)",
            r"because of (\w+)",
            r"resulting in (\w+)",
        ]

        for pattern in causal_patterns:
            match = re.search(pattern, query)
            if match:
                return match.group(0)

        return None

    async def _is_seeking_insight(self, query: str) -> bool:
        """Determine if query seeks deeper insight."""
        insight_words = [
            "understand",
            "realize",
            "pattern",
            "why",
            "insight",
            "discover",
            "learn",
            "meaning",
        ]
        return any(word in query for word in insight_words)

    async def _has_pattern_curiosity(self, query: str) -> bool:
        """Check if query shows curiosity about patterns."""
        pattern_words = [
            "pattern",
            "rhythm",
            "usually",
            "often",
            "tend to",
            "routine",
            "habit",
            "cycle",
        ]
        return any(word in query for word in pattern_words)

    async def _is_growth_oriented(self, query: str) -> bool:
        """Assess if query is oriented toward growth."""
        return any(marker in query for marker in self._growth_markers)
