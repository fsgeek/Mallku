"""
Universal Activity Collector using webhook/API integrations
Transforms hundreds of services into activity streams with minimal effort
"""

from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from src.mallku.memory_anchor_client import MemoryAnchorClient


class WebhookEvent(BaseModel):
    """Generic webhook event from any service"""
    source: str  # "zapier", "slack", "github", etc.
    service: str  # "gmail", "calendar", "jira", etc.
    event_type: str  # "email.received", "meeting.started", etc.
    timestamp: datetime
    data: dict[str, object]
    metadata: dict[str, object] = Field(default_factory=dict)


class ServiceMapping(BaseModel):
    """Maps service events to memory anchor cursors"""
    service_name: str
    cursor_mappings: dict[str, str]  # event_field -> cursor_type
    reciprocity_rules: dict[str, object] | None
    correlation_hints: list[str]  # Fields that link to other services


class UniversalActivityCollector:
    """
    Collects activity from any service via webhooks/APIs
    Uses Zapier, Make.com, n8n, or direct webhooks
    """

    def __init__(self):
        self.anchor_client = MemoryAnchorClient(
            provider_id="universal_collector",
            provider_type="integration_hub",
            cursor_types=["temporal", "social", "content", "workflow"]
        )

        # Service mappings define how to interpret each service
        self.service_mappings = {
            "gmail": ServiceMapping(
                service_name="gmail",
                cursor_mappings={
                    "from": "social",
                    "subject": "content",
                    "timestamp": "temporal"
                },
                reciprocity_rules={"request_indicators": ["?", "please", "need"]},
                correlation_hints=["message_id", "thread_id", "attachment_names"]
            ),

            "slack": ServiceMapping(
                service_name="slack",
                cursor_mappings={
                    "user": "social",
                    "channel": "workflow",
                    "timestamp": "temporal",
                    "text": "content"
                },
                reciprocity_rules={"value_indicators": ["here's", "solution", "fixed"]},
                correlation_hints=["thread_ts", "files", "user_mentions"]
            ),

            "calendar": ServiceMapping(
                service_name="calendar",
                cursor_mappings={
                    "attendees": "social",
                    "location": "spatial",
                    "start_time": "temporal",
                    "title": "content"
                },
                reciprocity_rules={"meeting_value": "duration * attendee_count"},
                correlation_hints=["meeting_id", "recurring_id", "attached_docs"]
            ),

            "jira": ServiceMapping(
                service_name="jira",
                cursor_mappings={
                    "assignee": "social",
                    "updated": "temporal",
                    "status": "workflow",
                    "summary": "content"
                },
                reciprocity_rules={"completion_value": 1.0, "assignment_cost": 0.3},
                correlation_hints=["issue_key", "epic_link", "related_issues"]
            ),

            "github": ServiceMapping(
                service_name="github",
                cursor_mappings={
                    "author": "social",
                    "created_at": "temporal",
                    "repo": "workflow",
                    "title": "content"
                },
                reciprocity_rules={"pr_value": "additions * 0.01 + deletions * 0.005"},
                correlation_hints=["pr_number", "issue_refs", "commit_shas"]
            ),

            "zoom": ServiceMapping(
                service_name="zoom",
                cursor_mappings={
                    "participants": "social",
                    "start_time": "temporal",
                    "duration": "workflow",
                    "topic": "content"
                },
                reciprocity_rules={"participation_value": "speaking_time / total_time"},
                correlation_hints=["meeting_id", "recording_url", "calendar_event"]
            )
        }

        # Cross-service correlation engine
        self.correlation_engine = CrossServiceCorrelator()

    async def process_webhook(self, event: WebhookEvent) -> dict:
        """
        Process incoming webhook from any service
        Creates memory anchors and tracks reciprocity
        """

        # Get service mapping
        mapping = self.service_mappings.get(event.service)
        if not mapping:
            # Unknown service - use generic processing
            mapping = self._create_generic_mapping(event)

        # Extract cursors based on mapping
        cursors = self._extract_cursors(event, mapping)

        # Update memory anchors
        for cursor_type, cursor_value in cursors.items():
            await self.anchor_client.update_cursor(
                cursor_type=cursor_type,
                cursor_value=cursor_value,
                metadata={
                    "source": event.source,
                    "service": event.service,
                    "event_type": event.event_type
                }
            )

        # Calculate reciprocity if applicable
        reciprocity = self._calculate_service_reciprocity(event, mapping)

        # Find cross-service correlations
        correlations = await self.correlation_engine.find_correlations(event, mapping)

        # Store enriched activity record
        activity_record = {
            "activity_id": str(uuid4()),
            "memory_anchor_uuid": self.anchor_client.current_anchor_id,
            "service": event.service,
            "event": event.dict(),
            "extracted_cursors": cursors,
            "reciprocity": reciprocity,
            "correlations": correlations,
            "timestamp": event.timestamp
        }

        await self._store_activity(activity_record)

        return {
            "status": "processed",
            "activity_id": activity_record["activity_id"],
            "correlations_found": len(correlations)
        }

    def _extract_cursors(self, event: WebhookEvent, mapping: ServiceMapping) -> dict:
        """Extract cursor values from event data using mapping"""
        cursors = {}

        for field, cursor_type in mapping.cursor_mappings.items():
            value = event.data.get(field)
            if value:
                cursors[cursor_type] = value

        return cursors

    async def register_zapier_integration(self, zap_config: dict) -> str:
        """
        Register a Zapier integration endpoint
        Returns webhook URL for Zapier to send events to
        """

        integration_id = str(uuid4())
        webhook_url = f"https://api.mallku.ai/webhooks/zapier/{integration_id}"

        # Store configuration
        await self._store_integration_config({
            "integration_id": integration_id,
            "type": "zapier",
            "config": zap_config,
            "webhook_url": webhook_url,
            "created": datetime.now(UTC)
        })

        return webhook_url


class CrossServiceCorrelator:
    """
    Finds connections between activities across different services
    This is where the magic happens - linking email to docs to tasks
    """

    async def find_correlations(self, event: WebhookEvent, mapping: ServiceMapping) -> list[dict]:
        """
        Find activities in other services that correlate with this event
        """
        correlations = []

        # Extract correlation hints
        for hint_field in mapping.correlation_hints:
            hint_value = event.data.get(hint_field)
            if not hint_value:
                continue

            # Search for this hint in other services
            correlated = await self._search_correlation(hint_field, hint_value, event.timestamp)
            correlations.extend(correlated)

        # Time-based correlation (activities within temporal window)
        temporal_correlations = await self._find_temporal_correlations(event)
        correlations.extend(temporal_correlations)

        return correlations

    async def _search_correlation(self, field: str, value: object, timestamp: datetime) -> list[dict]:
        """Search for correlated activities across all services"""

        # Query pattern: find activities that reference this value
        _ = """
        FOR activity IN universal_activities
            FILTER activity.timestamp >= DATE_SUBTRACT(@timestamp, 1, 'hour')
            FILTER activity.timestamp <= DATE_ADD(@timestamp, 1, 'hour')
            FILTER CONTAINS(TO_STRING(activity.event.data), @value)
            FILTER activity.service != @exclude_service

            RETURN {
                correlated_activity: activity.activity_id,
                service: activity.service,
                correlation_type: @field,
                correlation_value: @value,
                time_distance: ABS(DATE_DIFF(activity.timestamp, @timestamp, 'minute'))
            }
        """

        # Execute search (simplified)
        return []

    async def _find_temporal_correlations(self, event: WebhookEvent) -> list[dict]:
        """Find activities that happened around the same time"""

        # Look for burst of activity across services
        # Often indicates related work (email → doc edit → task update)

        _ = event.timestamp.timestamp() - 300  # 5 min before
        _ = event.timestamp.timestamp() + 300    # 5 min after

        # Find all activities in temporal window
        # Group by service and look for patterns

        return []


class UnifiedQueryEngine:
    """
    Query across all integrated services using natural language
    """

    async def search(self, query: str) -> list[dict]:
        """
        Example queries:
        - "Everything related to the Austin project last week"
        - "All activities after the budget email from Sarah"
        - "Documents, messages, and tasks from the Monday planning session"
        """

        results = []

        # Parse query into components
        _ = self._parse_unified_query(query)

        # Build cross-service search
        _ = """
        LET anchor_matches = (
            FOR anchor IN memory_anchors
                FILTER anchor.timestamp >= @start_time
                FILTER anchor.timestamp <= @end_time
                RETURN anchor
        )

        FOR anchor IN anchor_matches
            LET email_activities = (
                FOR activity IN universal_activities
                    FILTER activity.memory_anchor_uuid == anchor._key
                    FILTER activity.service == "gmail"
                    FILTER @search_terms ANY IN activity.event.data.subject
                    RETURN activity
            )

            LET doc_activities = (
                FOR activity IN universal_activities
                    FILTER activity.memory_anchor_uuid == anchor._key
                    FILTER activity.service IN ["gdrive", "dropbox", "sharepoint"]
                    RETURN activity
            )

            LET task_activities = (
                FOR activity IN universal_activities
                    FILTER activity.memory_anchor_uuid == anchor._key
                    FILTER activity.service IN ["jira", "asana", "trello"]
                    RETURN activity
            )

            LET meeting_activities = (
                FOR activity IN universal_activities
                    FILTER activity.memory_anchor_uuid == anchor._key
                    FILTER activity.service IN ["calendar", "zoom"]
                    RETURN activity
            )

            // Find all correlated activities
            LET all_correlated = FLATTEN(
                FOR activity IN UNION(email_activities, doc_activities, task_activities)
                    FOR correlation IN activity.correlations
                        RETURN correlation.correlated_activity
            )

            RETURN {
                anchor: anchor,
                emails: email_activities,
                documents: doc_activities,
                tasks: task_activities,
                meetings: meeting_activities,
                correlation_graph: all_correlated,
                unified_context: {
                    total_activities: LENGTH(email_activities) + LENGTH(doc_activities) + LENGTH(task_activities),
                    services_involved: UNIQUE([email_activities[*].service, doc_activities[*].service, task_activities[*].service]),
                    time_span: anchor.timestamp
                }
            }
        """

        return results
