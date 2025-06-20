"""
End-to-End Integration Service

Orchestrates the complete Memory Anchor Discovery Trail pipeline:
Activity Events → Correlation Detection → Memory Anchors → Queryable Context

This service serves as the keystone that joins our three foundational components
into a living, breathing system that transforms raw activity into contextual intelligence.
"""

from .correlation_adapter import CorrelationToAnchorAdapter
from .integration_service import EndToEndIntegrationService
from .pipeline_models import (
    PipelineConfiguration,
    PipelineEvent,
    PipelineStatistics,
    PipelineStatus,
)

__all__ = [
    "EndToEndIntegrationService",
    "CorrelationToAnchorAdapter",
    "PipelineEvent",
    "PipelineStatus",
    "PipelineStatistics",
    "PipelineConfiguration",
]
