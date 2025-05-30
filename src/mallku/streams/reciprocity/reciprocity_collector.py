"""
Reciprocity Collector - Captures raw interaction data for Ayni scoring
Follows Indaleko's collector/recorder pattern
"""

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from base_collector import BaseCollector  # From Indaleko


class ReciprocityCollector(BaseCollector):
    """
    Collects raw interaction data between humans and AI systems.

    This collector is intentionally broad in what it captures, following
    the principle that we may not know what data will be valuable until later.
    The recorder will normalize and filter this data.
    """

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.collection_id = str(uuid4())
        self.interaction_buffer = []
        self.buffer_size = config.get("buffer_size", 100)

    async def collect(self) -> list[dict]:
        """
        Main collection method - gathers interaction data from various sources.

        In production, this would integrate with:
        - LLM API endpoints
        - Chat interfaces
        - Prompt management systems
        - System-generated interactions

        Returns:
            List of raw interaction records
        """

        collected_data = []

        # Collect from different sources
        # Note: These are placeholder methods that would connect to real systems

        llm_interactions = await self._collect_llm_interactions()
        collected_data.extend(llm_interactions)

        prompt_manager_data = await self._collect_prompt_manager_data()
        collected_data.extend(prompt_manager_data)

        ui_interactions = await self._collect_ui_interactions()
        collected_data.extend(ui_interactions)

        # Add collection metadata
        for record in collected_data:
            record["collection_metadata"] = {
                "collector_id": self.collection_id,
                "collected_at": datetime.now(UTC).isoformat(),
                "collector_version": "0.1.0"
            }

        return collected_data

    async def _collect_llm_interactions(self) -> list[dict]:
        """
        Collect direct LLM interactions.

        This would integrate with your LLM API layer to capture:
        - Prompts sent
        - Responses received
        - Token counts
        - Response times
        - Error states
        """

        # Placeholder implementation
        # In production, this would hook into your LLM middleware

        interactions = []

        # Example structure of collected data
        _ = {
            "source": "llm_api",
            "timestamp": datetime.now(UTC).isoformat(),
            "interaction_id": str(uuid4()),
            "participants": ["human_user_001", "claude"],
            "initiator": "human",
            "raw_data": {
                "prompt_tokens": 150,
                "response_tokens": 500,
                "total_tokens": 650,
                "model": "claude-3",
                "temperature": 0.7,
                "response_time_ms": 2300,
                "success": True,
                # Note: We don't store actual prompt/response content
                # Just metadata about the interaction
                "prompt_complexity": 0.7,  # From complexity analyzer
                "response_categories": ["technical", "explanatory"],
                "interaction_type": "query"
            }
        }

        # In production, fetch real interactions
        # interactions = await self.llm_client.get_recent_interactions()

        return interactions

    async def _collect_prompt_manager_data(self) -> list[dict]:
        """
        Collect system-generated prompt interactions.

        These are automated prompts from the UPI system, not direct human queries.
        Important for tracking system health and not penalizing users.
        """

        interactions = []

        # Example of system-generated interaction
        _ = {
            "source": "prompt_manager",
            "timestamp": datetime.now(UTC).isoformat(),
            "interaction_id": str(uuid4()),
            "participants": ["upi_system", "claude"],
            "initiator": "system",
            "raw_data": {
                "prompt_template": "semantic_extraction_v2",
                "target_file_count": 50,
                "success_rate": 0.96,
                "average_response_time": 1500,
                "errors": ["timeout", "rate_limit"],
                "system_health": {
                    "prompt_quality": 0.85,
                    "template_effectiveness": 0.92
                }
            }
        }  # noqa: F841 -- this is an example

        # In production, fetch from prompt management system
        # interactions = await self.prompt_manager.get_recent_automated()

        return interactions

    async def _collect_ui_interactions(self) -> list[dict]:
        """
        Collect UI-based interactions (chat interface, etc.)

        Captures interaction patterns without content:
        - Message lengths
        - Interaction timing
        - Correction patterns
        - Feedback signals
        """

        interactions = []

        # Example UI interaction metadata (not used, shown for reference)
        _ = {
            "source": "chat_ui",
            "timestamp": datetime.now(UTC).isoformat(),
            "interaction_id": str(uuid4()),
            "participants": ["human_user_001", "claude"],
            "initiator": "human",
            "raw_data": {
                "session_id": "sess_xyz123",
                "message_index": 5,
                "time_since_last": 45.2,  # seconds
                "includes_correction": False,
                "includes_feedback": True,
                "feedback_type": "positive",
                "interaction_pattern": "iterative_refinement",
                "estimated_value": {
                    "human_effort": 0.6,
                    "ai_computation": 0.8
                }
            }
        }

        # In production, fetch from UI layer
        # interactions = await self.ui_service.get_interaction_metadata()

        return interactions

    def buffer_interaction(self, interaction: dict):
        """
        Buffer interactions for batch processing.

        Useful for high-frequency collection scenarios.
        """

        self.interaction_buffer.append(interaction)

        if len(self.interaction_buffer) >= self.buffer_size:
            self._flush_buffer()

    def _flush_buffer(self):
        """Flush buffered interactions to storage"""

        if not self.interaction_buffer:
            return

        # In production, this would write to your storage layer
        # For now, just clear the buffer

        self.interaction_buffer.clear()

    async def validate_collection(self, data: list[dict]) -> bool:
        """
        Validate collected data meets minimum requirements.

        Args:
            data: Collected interaction records

        Returns:
            True if data is valid for recording
        """

        for record in data:
            # Check required fields
            required = ["source", "timestamp", "interaction_id", "participants"]
            if not all(field in record for field in required):
                return False

            # Validate timestamp format
            try:
                datetime.fromisoformat(record["timestamp"])
            except (ValueError, TypeError):
                return False

        return True

    def get_collector_stats(self) -> dict:
        """Get statistics about collector performance"""

        return {
            "collector_id": self.collection_id,
            "buffer_size": len(self.interaction_buffer),
            "total_collected": 0,  # Would track this in production
            "last_collection": datetime.now(UTC).isoformat(),
            "status": "active"
        }
