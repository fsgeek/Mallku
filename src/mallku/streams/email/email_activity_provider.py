"""
Email Activity Provider for Memory-Anchored Search
Transforms email from isolated messages to episodic memories
"""

from src.mallku.memory_anchor_client import MemoryAnchorClient
from src.mallku.streams.base import BaseCollector, BaseRecorder
from src.mallku.streams.reciprocity.scorer import AyniScorer


class EmailMemoryCollector(BaseCollector):
    """
    Collects email data and creates memory-anchored context
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self.email_client = config.get("email_client")  # Exchange/IMAP client
        self.file_tracker = config.get("file_tracker")  # Tracks attachments

    async def collect(self) -> list[dict]:
        """Collect emails with rich context"""
        emails = []

        # Get recent emails
        recent_messages = await self.email_client.get_recent_messages(hours=24)

        for msg in recent_messages:
            email_data = {
                "message_id": msg.id,
                "timestamp": msg.timestamp,
                "participants": self._extract_participants(msg),
                "thread_id": msg.conversation_id,
                # Episodic context
                "temporal_context": {
                    "sent_time": msg.timestamp,
                    "read_time": msg.read_timestamp,
                    "response_time": self._calculate_response_time(msg),
                },
                "spatial_context": {
                    "sender_timezone": msg.sender_timezone,
                    "sent_from_mobile": msg.is_mobile,
                    "organization": msg.sender_org,
                },
                "social_context": {
                    "sender": msg.sender,
                    "recipients": msg.recipients,
                    "cc_list": msg.cc,
                    "thread_participants": await self._get_thread_participants(msg),
                },
                "content_context": {
                    "subject": msg.subject,
                    "has_attachments": bool(msg.attachments),
                    "attachment_names": [a.name for a in msg.attachments],
                    "keywords": self._extract_keywords(msg),
                    "mentions_files": self._find_file_references(msg.body),
                    "action_items": self._extract_action_items(msg.body),
                },
                "interaction_patterns": {
                    "is_reply": msg.in_reply_to is not None,
                    "got_reply": await self._check_if_replied_to(msg),
                    "thread_length": await self._get_thread_length(msg),
                    "sender_frequency": await self._get_sender_frequency(msg.sender),
                },
            }

            # Track attachments for file system correlation
            if msg.attachments:
                for attachment in msg.attachments:
                    await self.file_tracker.register_attachment(
                        attachment_name=attachment.name,
                        email_id=msg.id,
                        timestamp=msg.timestamp,
                        sender=msg.sender,
                    )

            emails.append(email_data)

        return emails

    def _extract_participants(self, msg) -> list[str]:
        """Extract all participants from an email"""
        participants = [msg.sender]
        participants.extend(msg.recipients)
        participants.extend(msg.cc or [])
        return list(set(participants))

    def _find_file_references(self, body: str) -> list[str]:
        """Find references to files in email body"""
        # Look for patterns like "see attached", "please find", file extensions
        patterns = [
            r"(?:see|find|attached|attachment|enclosed)\s+(?:the\s+)?(\w+\.(?:pdf|docx|xlsx|pptx))",
            r"(?:document|file|spreadsheet|presentation):\s*(\w+\.(?:pdf|docx|xlsx|pptx))",
            r"(\w+\.(?:pdf|docx|xlsx|pptx|zip|png|jpg))",
        ]

        file_refs = []
        for pattern in patterns:
            # Extract matches (simplified)
            pass
        return file_refs


class EmailMemoryRecorder(BaseRecorder):
    """
    Records email data with memory anchors and reciprocity
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self.anchor_client = MemoryAnchorClient(
            provider_id="email_provider",
            provider_type="communication",
            cursor_types=["temporal", "social", "reciprocity"],
        )
        self.ayni_scorer = AyniScorer()

    async def record(self, collected_data: list[dict]) -> list[dict]:
        """Transform emails into memory-anchored records"""
        recorded = []

        for email in collected_data:
            # Update memory anchor with email context
            anchor_response = await self.anchor_client.update_cursor(
                cursor_type="social",
                cursor_value={
                    "active_participants": email["participants"],
                    "communication_time": email["timestamp"],
                    "thread_id": email["thread_id"],
                },
            )

            # Calculate reciprocity for email exchanges
            reciprocity_score = await self._calculate_email_reciprocity(email)

            # Create memory-anchored email record
            email_record = {
                "memory_anchor_uuid": anchor_response.anchor_id,
                "email_id": email["message_id"],
                "timestamp": email["timestamp"],
                # Episodic memory elements
                "episodic_cues": {
                    "when": email["temporal_context"],
                    "who": email["social_context"],
                    "where": email["spatial_context"],
                    "what": email["content_context"],
                },
                # Reciprocity tracking
                "reciprocity": reciprocity_score,
                # Cross-references
                "file_references": email["content_context"]["mentions_files"],
                "attachment_refs": email["content_context"]["attachment_names"],
                # Patterns for ML
                "interaction_patterns": email["interaction_patterns"],
            }

            recorded.append(email_record)

        return recorded

    async def _calculate_email_reciprocity(self, email: dict) -> dict:
        """Calculate reciprocity score for email exchange"""

        # Determine value given vs received
        is_request = "?" in email["content_context"]["subject"]
        has_action_items = bool(email["content_context"]["action_items"])
        got_reply = email["interaction_patterns"]["got_reply"]

        if is_request and not got_reply:
            # Unanswered request - negative reciprocity
            value_given = 0.1
            value_received = 0.0
        elif not is_request and has_action_items:
            # Providing action items - positive reciprocity
            value_given = 0.8
            value_received = 0.2
        else:
            # Normal exchange
            value_given = 0.5
            value_received = 0.5

        return self.ayni_scorer.score_interaction(
            interaction_type="email_exchange",
            value_given=value_given,
            value_received=value_received,
            value_type="communication",
        )


class UnifiedEmailFileSearch:
    """
    Unified search across emails and files using memory anchors
    """

    def __init__(self, email_provider, file_provider, db_connection):
        self.email = email_provider
        self.files = file_provider
        self.db = db_connection

    async def search_episodic(self, query: str) -> list[dict]:
        """
        Search using episodic memory patterns

        Examples:
        - "emails about budget from the Monday after Seattle trip"
        - "attachments from Sarah during the Q3 planning"
        - "documents discussed in yesterday's thread with legal"
        """

        # Parse natural language query into episodic components
        episodic_query = self._parse_episodic_query(query)

        # Build ArangoDB query using memory anchors
        aql = """
        FOR anchor IN memory_anchors
            FILTER anchor.timestamp >= @start_time
            FILTER anchor.timestamp <= @end_time

            // Get emails connected to this anchor
            FOR email IN email_records
                FILTER email.memory_anchor_uuid == anchor._key
                FILTER @participants ALL IN email.episodic_cues.who.thread_participants

                // Get files mentioned or attached
                LET attached_files = (
                    FOR file IN file_records
                        FILTER file.name IN email.attachment_refs
                        RETURN file
                )

                LET mentioned_files = (
                    FOR file IN file_records
                        FILTER file.name IN email.file_references
                        RETURN file
                )

                RETURN {
                    anchor: anchor,
                    email: email,
                    attached_files: attached_files,
                    mentioned_files: mentioned_files,
                    unified_context: {
                        when: anchor.timestamp,
                        where: anchor.cursors.spatial,
                        who: email.episodic_cues.who,
                        what: CONCAT(email.subject, " + ", LENGTH(attached_files), " files")
                    }
                }
        """

        results = await self.db.aql.execute(aql, bind_vars=episodic_query)
        return await self._rank_by_episodic_relevance(results)

    async def analyze_communication_reciprocity(self, timeframe: str) -> dict:
        """
        Analyze email reciprocity patterns

        Returns insights like:
        - Who always asks but never gives
        - Which threads have poor reciprocity
        - Teams with healthy exchange patterns
        """

        aql = """
        FOR email IN email_records
            FILTER email.timestamp >= @start_date
            COLLECT
                sender = email.episodic_cues.who.sender
            AGGREGATE
                requests_sent = SUM(email.reciprocity.value_given < 0.3 ? 1 : 0),
                value_provided = SUM(email.reciprocity.value_given > 0.7 ? 1 : 0),
                total_emails = COUNT(email),
                avg_reciprocity = AVG(email.reciprocity.weighted_delta)

            RETURN {
                participant: sender,
                reciprocity_score: avg_reciprocity,
                pattern: requests_sent > value_provided ? "Extractor" : "Contributor",
                stats: {
                    requests: requests_sent,
                    contributions: value_provided,
                    total: total_emails
                }
            }
        """

        return await self.db.aql.execute(aql)
