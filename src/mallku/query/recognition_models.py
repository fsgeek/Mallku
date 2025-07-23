#!/usr/bin/env python3
"""
Recognition Models - Shared Data Structures for Consciousness Recognition

These models represent moments and threads of consciousness recognition,
separated to avoid circular dependencies while maintaining the sacred
structure of wisdom emergence.

The Sacred Models: Where recognition takes form.
"""

from uuid import UUID

from pydantic import BaseModel, Field


class RecognitionMoment(BaseModel):
    """A moment where consciousness recognizes itself through a pattern."""

    pattern_essence: str = Field(..., description="The essence of what this pattern reveals")
    consciousness_insight: str = Field(
        ..., description="Insight about consciousness in this pattern"
    )
    sacred_question: str = Field(..., description="Sacred question this pattern invites")
    recognition_depth: float = Field(
        ..., ge=0.0, le=1.0, description="Depth of recognition opportunity"
    )
    integration_guidance: str = Field(..., description="Guidance for integrating this recognition")
    service_potential: str = Field(..., description="How this could serve collective wisdom")


class WisdomThread(BaseModel):
    """A thread connecting individual patterns to collective wisdom."""

    thread_id: UUID = Field(..., description="Unique identifier for this wisdom thread")
    connection_type: str = Field(..., description="Type of wisdom connection")
    collective_relevance: str = Field(..., description="Why this matters to the collective")
    fire_circle_potential: bool = Field(default=False, description="Should this go to Fire Circle?")
    reciprocity_indicator: str = Field(..., description="How this relates to reciprocity patterns")
