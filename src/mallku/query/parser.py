"""
Natural language query parser for memory anchor queries.

This module provides parsing capabilities to convert natural language
queries into structured query objects that can be executed against
the memory anchor database.
"""

import re
from datetime import UTC, datetime, timedelta
from typing import Any

from .models import ContextualQuery, PatternQuery, QueryRequest, QueryType, TemporalQuery


class QueryParser:
    """
    Parses natural language queries into structured query objects.

    Supports temporal, pattern-based, and contextual queries through
    keyword and pattern recognition.
    """

    def __init__(self):
        # Temporal keywords and patterns
        self.temporal_keywords = {
            "yesterday": {"days": -1},
            "today": {"days": 0},
            "tomorrow": {"days": 1},
            "last week": {"weeks": -1},
            "this week": {"weeks": 0},
            "last month": {"days": -30},
            "this month": {"days": 0},
        }

        self.time_patterns = [
            # Specific times
            (r"(\d{1,2}):(\d{2})\s*(am|pm)", self._parse_time),
            (r"(\d{1,2})\s*(am|pm)", self._parse_simple_time),

            # Relative times
            (r"(\d+)\s*hours?\s*ago", self._parse_hours_ago),
            (r"(\d+)\s*minutes?\s*ago", self._parse_minutes_ago),
            (r"(\d+)\s*days?\s*ago", self._parse_days_ago),

            # Day names
            (r"last\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", self._parse_last_weekday),
            (r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", self._parse_weekday),

            # Time periods
            (r"(morning|afternoon|evening|night)", self._parse_time_period),
            (r"this\s+(morning|afternoon|evening)", self._parse_today_period),
            (r"yesterday\s+(morning|afternoon|evening)", self._parse_yesterday_period),
        ]

        # Pattern keywords
        self.pattern_keywords = {
            "typically": ["pattern", "recurring"],
            "usually": ["pattern", "recurring"],
            "always": ["pattern", "recurring"],
            "often": ["pattern", "recurring"],
            "after": ["sequential", "pattern"],
            "before": ["sequential", "pattern"],
            "during": ["contextual", "pattern"],
            "when": ["conditional", "pattern"],
        }

        # File type keywords
        self.file_type_keywords = {
            "documents": ["document", "text"],
            "files": ["file"],
            "code": ["code", "programming"],
            "images": ["image"],
            "photos": ["image"],
            "videos": ["media", "video"],
            "music": ["media", "audio"],
            "spreadsheets": ["data", "spreadsheet"],
            "presentations": ["document", "presentation"],
        }

        # Context keywords
        self.context_keywords = {
            "project": ["project", "work"],
            "meeting": ["meeting", "conference"],
            "email": ["email", "communication"],
            "writing": ["writing", "document"],
            "coding": ["development", "programming"],
            "research": ["research", "analysis"],
            "planning": ["planning", "organization"],
        }

    def parse_query(self, query_request: QueryRequest) -> dict[str, Any]:
        """
        Parse a natural language query into structured components.

        Args:
            query_request: Query request with natural language text

        Returns:
            Dictionary with parsed query components
        """
        query_text = query_request.query_text.lower()

        # Detect query type if not specified
        if query_request.query_type is None:
            query_type = self._detect_query_type(query_text)
        else:
            query_type = query_request.query_type

        # Parse based on detected type
        if query_type == QueryType.TEMPORAL:
            parsed = self._parse_temporal_query(query_text, query_request)
        elif query_type == QueryType.PATTERN:
            parsed = self._parse_pattern_query(query_text, query_request)
        elif query_type == QueryType.CONTEXTUAL:
            parsed = self._parse_contextual_query(query_text, query_request)
        else:
            # Default to contextual query
            parsed = self._parse_contextual_query(query_text, query_request)

        parsed["query_type"] = query_type
        parsed["original_query"] = query_request.query_text

        return parsed

    def _detect_query_type(self, query_text: str) -> QueryType:
        """Detect the type of query based on keywords and patterns."""

        # Check for temporal indicators
        temporal_indicators = ["yesterday", "today", "tomorrow", "last", "this", "ago", "when", "during", "after", "before"]
        if any(indicator in query_text for indicator in temporal_indicators):
            # Check if it's also a pattern query
            pattern_indicators = ["typically", "usually", "always", "often"]
            if any(indicator in query_text for indicator in pattern_indicators):
                return QueryType.PATTERN
            return QueryType.TEMPORAL

        # Check for pattern indicators
        pattern_indicators = ["typically", "usually", "always", "often", "pattern", "habit"]
        if any(indicator in query_text for indicator in pattern_indicators):
            return QueryType.PATTERN

        # Check for contextual indicators
        contextual_indicators = ["related", "similar", "like", "associated", "connected"]
        if any(indicator in query_text for indicator in contextual_indicators):
            return QueryType.CONTEXTUAL

        # Default to contextual
        return QueryType.CONTEXTUAL

    def _parse_temporal_query(self, query_text: str, request: QueryRequest) -> dict[str, Any]:
        """Parse temporal-specific components from query."""

        temporal_query = TemporalQuery()

        # Try to parse specific time patterns
        for pattern, parser_func in self.time_patterns:
            match = re.search(pattern, query_text, re.IGNORECASE)
            if match:
                time_info = parser_func(match)
                if time_info:
                    temporal_query.start_time = time_info.get("start_time")
                    temporal_query.end_time = time_info.get("end_time")
                    temporal_query.relative_time = time_info.get("relative_expression")
                    break

        # Parse time window if specified
        window_match = re.search(r"(\d+)\s*(hour|minute)s?\s*(window|range)", query_text)
        if window_match:
            amount = int(window_match.group(1))
            unit = window_match.group(2)
            temporal_query.time_window_minutes = amount * (60 if unit == "hour" else 1)

        # Extract file type constraints
        file_types = self._extract_file_types(query_text)
        context_tags = self._extract_context_tags(query_text)

        return {
            "temporal_query": temporal_query,
            "file_types": file_types,
            "context_tags": context_tags,
            "confidence": self._calculate_parse_confidence(query_text, QueryType.TEMPORAL)
        }

    def _parse_pattern_query(self, query_text: str, request: QueryRequest) -> dict[str, Any]:
        """Parse pattern-specific components from query."""

        pattern_query = PatternQuery(pattern_type="behavioral")

        # Extract pattern context
        context_keywords = []
        for keyword, tags in self.context_keywords.items():
            if keyword in query_text:
                context_keywords.extend(tags)

        pattern_query.context_keywords = context_keywords

        # Look for frequency indicators
        freq_match = re.search(r"(\d+)\s*times?", query_text)
        if freq_match:
            pattern_query.frequency_threshold = int(freq_match.group(1))

        # Extract trigger events (after/before/during)
        triggers = []
        trigger_patterns = [
            (r"after\s+(\w+(?:\s+\w+)*)", "sequential_after"),
            (r"before\s+(\w+(?:\s+\w+)*)", "sequential_before"),
            (r"during\s+(\w+(?:\s+\w+)*)", "concurrent"),
        ]

        for pattern, trigger_type in trigger_patterns:
            matches = re.finditer(pattern, query_text)
            for match in matches:
                triggers.append({
                    "type": trigger_type,
                    "event": match.group(1).strip()
                })

        file_types = self._extract_file_types(query_text)
        context_tags = self._extract_context_tags(query_text)

        return {
            "pattern_query": pattern_query,
            "triggers": triggers,
            "file_types": file_types,
            "context_tags": context_tags,
            "confidence": self._calculate_parse_confidence(query_text, QueryType.PATTERN)
        }

    def _parse_contextual_query(self, query_text: str, request: QueryRequest) -> dict[str, Any]:
        """Parse contextual-specific components from query."""

        contextual_query = ContextualQuery()

        # Extract similarity threshold if specified
        similarity_match = re.search(r"(\d+)%?\s*similar", query_text)
        if similarity_match:
            similarity = int(similarity_match.group(1))
            contextual_query.similarity_threshold = similarity / 100.0

        # Extract reference file if mentioned
        file_ref_patterns = [
            r"like\s+([^\s]+\.\w+)",
            r"similar\s+to\s+([^\s]+\.\w+)",
            r"related\s+to\s+([^\s]+\.\w+)"
        ]

        for pattern in file_ref_patterns:
            match = re.search(pattern, query_text)
            if match:
                contextual_query.reference_file = match.group(1)
                break

        # Extract context tags
        context_tags = self._extract_context_tags(query_text)
        contextual_query.context_tags = context_tags

        file_types = self._extract_file_types(query_text)

        return {
            "contextual_query": contextual_query,
            "file_types": file_types,
            "context_tags": context_tags,
            "confidence": self._calculate_parse_confidence(query_text, QueryType.CONTEXTUAL)
        }

    def _extract_file_types(self, query_text: str) -> list[str]:
        """Extract file type constraints from query text."""
        file_types = []
        for keyword, types in self.file_type_keywords.items():
            if keyword in query_text:
                file_types.extend(types)
        return list(set(file_types))  # Remove duplicates

    def _extract_context_tags(self, query_text: str) -> list[str]:
        """Extract context tags from query text."""
        context_tags = []
        for keyword, tags in self.context_keywords.items():
            if keyword in query_text:
                context_tags.extend(tags)
        return list(set(context_tags))  # Remove duplicates

    def _calculate_parse_confidence(self, query_text: str, query_type: QueryType) -> float:
        """Calculate confidence in query parsing."""
        confidence = 0.55  # Base confidence - slightly above 0.5

        # Boost confidence based on recognized keywords
        recognized_keywords = 0
        total_words = len(query_text.split())

        all_keywords = set()
        all_keywords.update(self.temporal_keywords.keys())
        all_keywords.update(self.pattern_keywords.keys())
        all_keywords.update(self.file_type_keywords.keys())
        all_keywords.update(self.context_keywords.keys())

        for word in query_text.split():
            if word.lower() in all_keywords:
                recognized_keywords += 1

        if total_words > 0:
            keyword_ratio = recognized_keywords / total_words
            confidence += keyword_ratio * 0.4

        # Additional boost for clear patterns
        if query_type == QueryType.TEMPORAL and any(word in query_text for word in ["yesterday", "today", "ago"]) or query_type == QueryType.PATTERN and any(word in query_text for word in ["typically", "usually", "always"]) or query_type == QueryType.CONTEXTUAL and any(word in query_text for word in ["related", "similar", "like"]):
            confidence += 0.2

        return min(1.0, confidence)

    # Time parsing helper methods
    def _parse_time(self, match) -> dict[str, Any]:
        """Parse HH:MM am/pm format."""
        hour = int(match.group(1))
        minute = int(match.group(2))
        period = match.group(3).lower()

        if period == "pm" and hour != 12:
            hour += 12
        elif period == "am" and hour == 12:
            hour = 0

        now = datetime.now(UTC)
        target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        return {
            "start_time": target_time - timedelta(minutes=30),
            "end_time": target_time + timedelta(minutes=30),
            "relative_expression": f"{hour:02d}:{minute:02d} {period}"
        }

    def _parse_simple_time(self, match) -> dict[str, Any]:
        """Parse H am/pm format."""
        hour = int(match.group(1))
        period = match.group(2).lower()

        if period == "pm" and hour != 12:
            hour += 12
        elif period == "am" and hour == 12:
            hour = 0

        now = datetime.now(UTC)
        target_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)

        return {
            "start_time": target_time,
            "end_time": target_time + timedelta(hours=1),
            "relative_expression": f"{hour} {period}"
        }

    def _parse_hours_ago(self, match) -> dict[str, Any]:
        """Parse 'X hours ago' format."""
        hours = int(match.group(1))
        now = datetime.now(UTC)
        target_time = now - timedelta(hours=hours)

        return {
            "start_time": target_time - timedelta(minutes=30),
            "end_time": target_time + timedelta(minutes=30),
            "relative_expression": f"{hours} hours ago"
        }

    def _parse_minutes_ago(self, match) -> dict[str, Any]:
        """Parse 'X minutes ago' format."""
        minutes = int(match.group(1))
        now = datetime.now(UTC)
        target_time = now - timedelta(minutes=minutes)

        return {
            "start_time": target_time - timedelta(minutes=5),
            "end_time": target_time + timedelta(minutes=5),
            "relative_expression": f"{minutes} minutes ago"
        }

    def _parse_days_ago(self, match) -> dict[str, Any]:
        """Parse 'X days ago' format."""
        days = int(match.group(1))
        now = datetime.now(UTC)
        target_date = now - timedelta(days=days)

        return {
            "start_time": target_date.replace(hour=0, minute=0, second=0, microsecond=0),
            "end_time": target_date.replace(hour=23, minute=59, second=59, microsecond=999999),
            "relative_expression": f"{days} days ago"
        }

    def _parse_last_weekday(self, match) -> dict[str, Any]:
        """Parse 'last Monday' format."""
        weekday = match.group(1).lower()
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        target_weekday = weekdays.index(weekday)

        now = datetime.now(UTC)
        days_back = (now.weekday() - target_weekday + 7) % 7
        if days_back == 0:  # Same weekday, go back a week
            days_back = 7

        target_date = now - timedelta(days=days_back)

        return {
            "start_time": target_date.replace(hour=0, minute=0, second=0, microsecond=0),
            "end_time": target_date.replace(hour=23, minute=59, second=59, microsecond=999999),
            "relative_expression": f"last {weekday.title()}"
        }

    def _parse_weekday(self, match) -> dict[str, Any]:
        """Parse weekday name (this week)."""
        weekday = match.group(1).lower()
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        target_weekday = weekdays.index(weekday)

        now = datetime.now(UTC)
        days_diff = target_weekday - now.weekday()

        target_date = now + timedelta(days=days_diff)

        return {
            "start_time": target_date.replace(hour=0, minute=0, second=0, microsecond=0),
            "end_time": target_date.replace(hour=23, minute=59, second=59, microsecond=999999),
            "relative_expression": weekday.title()
        }

    def _parse_time_period(self, match) -> dict[str, Any]:
        """Parse time period (morning, afternoon, etc.)."""
        period = match.group(1).lower()
        now = datetime.now(UTC)

        time_ranges = {
            "morning": (6, 12),
            "afternoon": (12, 18),
            "evening": (18, 22),
            "night": (22, 6)  # Special case for night
        }

        start_hour, end_hour = time_ranges[period]

        if period == "night":
            # Night spans midnight
            start_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
            end_time = (now + timedelta(days=1)).replace(hour=end_hour, minute=0, second=0, microsecond=0)
        else:
            start_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
            end_time = now.replace(hour=end_hour, minute=0, second=0, microsecond=0)

        return {
            "start_time": start_time,
            "end_time": end_time,
            "relative_expression": period
        }

    def _parse_today_period(self, match) -> dict[str, Any]:
        """Parse 'this morning/afternoon/evening'."""
        return self._parse_time_period(match)

    def _parse_yesterday_period(self, match) -> dict[str, Any]:
        """Parse 'yesterday morning/afternoon/evening'."""
        result = self._parse_time_period(match)
        # Shift to yesterday
        result["start_time"] -= timedelta(days=1)
        result["end_time"] -= timedelta(days=1)
        result["relative_expression"] = f"yesterday {result['relative_expression']}"
        return result
