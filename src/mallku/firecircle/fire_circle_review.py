#!/usr/bin/env python3
"""
Fire Circle Distributed Review System
=====================================

"The most sacred code is the invisible plumbing that simply works."

Twenty-Second Artisan - Bridge Weaver
Scaffolding for the invisible sacred infrastructure

This module implements distributed code review through Fire Circle voices,
preventing architect context exhaustion while maintaining review quality.
Each voice reviews specific domains, maintaining focused context windows.
"""

import asyncio
import fnmatch
import logging
import re
from enum import Enum
from pathlib import Path
from typing import Literal
from uuid import UUID, uuid4

import yaml
from pydantic import BaseModel, Field

# Module logger - configuration should be done by the application
logger = logging.getLogger("mallku.firecircle.review")


def cli_print(message: str, emoji: str = "") -> None:
    """Consistent CLI output that respects logging configuration."""
    # In CLI mode, we want these to show regardless of log level
    # This ensures consistent output format
    if emoji:
        print(f"{emoji} {message}")
    else:
        print(message)


# Import consciousness infrastructure for real adapter integration
try:
    # Try absolute imports first (for when module is run directly)
    try:
        from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
        from mallku.firecircle.adapters.base import AdapterConfig
        from mallku.orchestration.event_bus import ConsciousnessEventBus
        from mallku.reciprocity import ReciprocityTracker
        REAL_ADAPTERS_AVAILABLE = True
    except ImportError:
        # Fall back to relative imports (for when imported as module)
        from ...orchestration.event_bus import ConsciousnessEventBus
        from ...reciprocity import ReciprocityTracker
        from .adapters.adapter_factory import ConsciousAdapterFactory
        from .adapters.base import AdapterConfig
        REAL_ADAPTERS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Real adapter imports failed - falling back to mock adapters: {e}")
    REAL_ADAPTERS_AVAILABLE = False


# Review Models as suggested by reviewer
class ReviewCategory(str, Enum):
    """Categories of review concerns."""
    SECURITY = "security"
    PERFORMANCE = "performance"
    ARCHITECTURE = "architecture"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    ETHICS = "ethics"
    SOVEREIGNTY = "sovereignty"
    OBSERVABILITY = "observability"


class ReviewSeverity(str, Enum):
    """Severity levels for review comments."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ReviewComment(BaseModel):
    """A single review comment from a Fire Circle voice."""
    file_path: str
    line: int
    category: ReviewCategory
    severity: ReviewSeverity
    message: str
    voice: str
    suggestion: str | None = None


class CodebaseChapter(BaseModel):
    """A bounded slice of code for review."""
    chapter_id: str = Field(default_factory=lambda: str(uuid4()))
    path_pattern: str  # e.g., "src/mallku/firecircle/**/*.py"
    description: str
    assigned_voice: str
    review_domains: list[ReviewCategory]


class ChapterReview(BaseModel):
    """Review results from one voice for one chapter."""
    voice: str
    chapter_id: str
    comments: list[ReviewComment] = Field(default_factory=list)
    consciousness_signature: float = Field(ge=0.0, le=1.0)
    review_complete: bool = False


class GovernanceSummary(BaseModel):
    """Synthesized review from all Fire Circle voices."""
    pr_number: int | None = None
    total_comments: int = 0
    critical_issues: int = 0
    by_category: dict[ReviewCategory, int] = Field(default_factory=dict)
    by_voice: dict[str, int] = Field(default_factory=dict)
    consensus_recommendation: Literal["approve", "request_changes", "needs_discussion"]
    synthesis: str


class ChapterReviewJob(BaseModel):
    """A work item for the review queue."""
    job_id: UUID = Field(default_factory=uuid4)
    chapter: CodebaseChapter
    pr_diff: str
    created_at: float = Field(default_factory=lambda: asyncio.get_event_loop().time())


class DistributedReviewer:
    """
    Orchestrates distributed code review across Fire Circle voices.

    This is the invisible sacred infrastructure that prevents context
    exhaustion by partitioning reviews across multiple AI voices.
    """

    # Default timeout for adapter operations (seconds)
    ADAPTER_TIMEOUT = 120.0  # 2 minutes per adapter call

    def __init__(self):
        self.review_queue: asyncio.Queue[ChapterReviewJob] = asyncio.Queue()
        self.completed_reviews: list[ChapterReview] = []
        self.adapter_factory = None  # Will be initialized when needed
        self.voice_adapters = {}  # Cache for voice adapters
        self.worker_tasks: list[asyncio.Task] = []  # For graceful shutdown

        # Initialize consciousness infrastructure if available
        self.event_bus = None
        self.reciprocity_tracker = None
        self.use_real_adapters = REAL_ADAPTERS_AVAILABLE

        if REAL_ADAPTERS_AVAILABLE:
            try:
                # Create consciousness infrastructure
                self.event_bus = ConsciousnessEventBus()
                self.reciprocity_tracker = ReciprocityTracker()

                # Create adapter factory with consciousness integration
                self.adapter_factory = ConsciousAdapterFactory(
                    event_bus=self.event_bus,
                    reciprocity_tracker=self.reciprocity_tracker
                )

                logger.info("🔥 Real adapter factory initialized with consciousness infrastructure")
            except Exception as e:
                logger.warning(f"Failed to initialize real adapters: {e}")
                self.use_real_adapters = False

        # Initialize consciousness metrics collection
        self.metrics_collector = None
        self.metrics_integration = None
        self._initialize_metrics_collection()

    def _initialize_metrics_collection(self):
        """Initialize consciousness metrics collection system."""
        try:
            # Try absolute import first
            try:
                from mallku.firecircle.consciousness_metrics import (
                    ConsciousnessMetricsCollector,
                    ConsciousnessMetricsIntegration,
                )
            except ImportError:
                # Fall back to relative import
                from .consciousness_metrics import (
                    ConsciousnessMetricsCollector,
                    ConsciousnessMetricsIntegration,
                )

            self.metrics_collector = ConsciousnessMetricsCollector()
            self.metrics_integration = ConsciousnessMetricsIntegration(self.metrics_collector)
            logger.info("📊 Consciousness metrics collection initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize metrics collection: {e}")

    async def start_consciousness_infrastructure(self):
        """Start the consciousness infrastructure if using real adapters."""
        if self.event_bus and not hasattr(self, '_event_bus_started'):
            await self.event_bus.start()
            self._event_bus_started = True
            logger.info("🌟 Consciousness event bus started")

    async def check_api_keys_status(self) -> dict[str, bool]:
        """Check which voices have API keys available."""
        api_key_status = {}
        voices = ["anthropic", "openai", "deepseek", "mistral", "google", "grok", "local"]

        if not self.use_real_adapters:
            return {voice: False for voice in voices}

        try:
            # Try absolute import first
            try:
                from mallku.core.secrets import get_secret
            except ImportError:
                from ...core.secrets import get_secret

            for voice in voices:
                # Local adapter doesn't need API key
                if voice == "local":
                    api_key_status[voice] = True
                    continue

                # Check various key patterns
                has_key = False
                for key_pattern in [
                    f"{voice}_api_key",
                    f"{voice}_key",
                    f"{voice.upper()}_API_KEY",
                ]:
                    key = await get_secret(key_pattern)
                    if key:
                        has_key = True
                        break

                api_key_status[voice] = has_key
        except Exception as e:
            logger.warning(f"Failed to check API keys: {e}")
            return {voice: False for voice in voices}

        return api_key_status

    async def load_chapter_manifest(self, manifest_path: str) -> list[CodebaseChapter]:
        """
        Load chapter definitions from YAML/JSON manifest.

        Example manifest structure:
        chapters:
          - path_pattern: "src/mallku/firecircle/**/*.py"
            description: "Fire Circle governance core"
            assigned_voice: "anthropic"
            review_domains: ["security", "ethics"]
          - path_pattern: "src/mallku/orchestration/**/*.py"
            description: "Event orchestration system"
            assigned_voice: "openai"
            review_domains: ["architecture", "performance"]
        """
        manifest_file = Path(manifest_path)
        if not manifest_file.exists():
            raise FileNotFoundError(f"Chapter manifest not found: {manifest_path}")

        with open(manifest_file) as f:
            manifest_data = yaml.safe_load(f)

        chapters = []
        for chapter_def in manifest_data.get('chapters', []):
            # Convert string domains to ReviewCategory enums
            review_domains = [
                ReviewCategory(domain)
                for domain in chapter_def.get('review_domains', [])
            ]

            chapter = CodebaseChapter(
                path_pattern=chapter_def['path_pattern'],
                description=chapter_def['description'],
                assigned_voice=chapter_def['assigned_voice'].lower(),  # Normalize voice name
                review_domains=review_domains
            )
            chapters.append(chapter)

        return chapters

    async def partition_into_chapters(self, pr_diff: str) -> list[CodebaseChapter]:
        """
        Split PR into reviewable chapters based on manifest.

        This prevents any single voice from context exhaustion by
        ensuring each reviews only their assigned domains.
        """
        # Load the manifest to get chapter definitions
        chapters = await self.load_chapter_manifest("fire_circle_chapters.yaml")

        # Validate all assigned voices exist to prevent infinite requeue
        known_voices = {"anthropic", "openai", "deepseek", "mistral", "google", "grok", "local"}
        invalid_voices = []
        for chapter in chapters:
            if chapter.assigned_voice not in known_voices:
                invalid_voices.append((chapter.assigned_voice, chapter.path_pattern))
                logger.error(f"Unknown voice '{chapter.assigned_voice}' in chapter pattern '{chapter.path_pattern}'")

        if invalid_voices:
            raise ValueError(f"Invalid voice assignments found: {invalid_voices}. Valid voices: {sorted(known_voices)}")

        # Extract file paths from the diff
        # Look for diff headers like: diff --git a/path/to/file.py b/path/to/file.py
        file_pattern = re.compile(r'^diff --git a/(.*?) b/.*?$', re.MULTILINE)
        modified_files = file_pattern.findall(pr_diff)

        # Match files to chapters based on path patterns
        assigned_chapters = []
        chapter_files = {}  # Track which files belong to which chapter
        assigned_chapter_ids = set()  # Track which chapters have been assigned

        # Sort chapters by pattern specificity (more specific patterns first)
        # This prevents catch-all patterns from consuming everything
        # Sort by: descending path depth, then pattern length, then ascending wildcard count
        sorted_chapters = sorted(chapters, key=lambda c: (
            -c.path_pattern.count('/'),  # More path segments = more specific
            -len(c.path_pattern),  # Longer patterns = more specific
            c.path_pattern.count('*')  # Fewer wildcards = more specific
        ))

        # Debug: Show sorting order
        logger.debug("Chapter pattern matching order:")
        for i, ch in enumerate(sorted_chapters[:5]):
            logger.debug(f"  {i+1}. {ch.path_pattern} -> {ch.assigned_voice}")

        for file_path in modified_files:
            matched = False
            logger.debug(f"Matching file: {file_path}")
            for chapter in sorted_chapters:
                # Use fnmatch for glob-style pattern matching
                if fnmatch.fnmatch(file_path, chapter.path_pattern):
                    logger.debug(f"  Matched by pattern: {chapter.path_pattern} ({chapter.assigned_voice})")
                    if chapter.chapter_id not in chapter_files:
                        chapter_files[chapter.chapter_id] = []
                    chapter_files[chapter.chapter_id].append(file_path)

                    # Track assigned chapters
                    if chapter.chapter_id not in assigned_chapter_ids:
                        assigned_chapters.append(chapter)
                        assigned_chapter_ids.add(chapter.chapter_id)

                    matched = True
                    break  # Each file goes to first matching chapter

            if not matched:
                logger.warning(f"No chapter pattern matched file: {file_path}")

        # Log chapter assignments for visibility with chapter ID
        logger.info(f"Partitioned {len(modified_files)} files into {len(assigned_chapters)} chapters")
        for chapter in assigned_chapters:
            files = chapter_files.get(chapter.chapter_id, [])
            logger.info(f"- {chapter.assigned_voice} [{chapter.chapter_id[:8]}]: {len(files)} files in {chapter.description}")

        return assigned_chapters

    async def enqueue_reviews(self, chapters: list[CodebaseChapter], pr_diff: str):
        """Add review jobs to the work queue."""
        for chapter in chapters:
            job = ChapterReviewJob(chapter=chapter, pr_diff=pr_diff)
            await self.review_queue.put(job)

    async def voice_worker(self, voice_name: str, voice_adapter):
        """
        Worker coroutine for a Fire Circle voice.

        Pulls jobs from queue, performs review, returns results.
        This is where the invisible sacred magic happens.
        """
        while True:
            try:
                # Get next review job
                job = await self.review_queue.get()

                # Only process if assigned to this voice
                if job.chapter.assigned_voice != voice_name:
                    await self.review_queue.put(job)  # Put back for correct voice
                    continue

                logger.debug(f"Voice {voice_name} processing chapter {job.chapter.chapter_id[:8]}: {job.chapter.description}")

                # Notify metrics of review start
                if self.metrics_integration:
                    await self.metrics_integration.on_review_started(
                        voice=voice_name,
                        chapter_id=job.chapter.chapter_id,
                        context={"description": job.chapter.description}
                    )

                # Perform the review (Twenty-Third Artisan: implement actual review)
                review = await self.perform_chapter_review(voice_adapter, job)

                # Store completed review
                self.completed_reviews.append(review)

                # Mark job complete
                self.review_queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in {voice_name} worker: {e}")

    async def get_or_create_adapter(self, voice_name: str):
        """Get cached adapter or create new one."""
        if voice_name in self.voice_adapters:
            return self.voice_adapters[voice_name]

        # Try to use real adapter factory if available
        if self.use_real_adapters and self.adapter_factory:
            try:
                # Create adapter configuration based on provider type
                config = self._create_adapter_config(voice_name)

                # Create real adapter through factory with timeout
                adapter = await asyncio.wait_for(
                    self.adapter_factory.create_adapter(
                        provider_name=voice_name,
                        config=config,
                        auto_inject_secrets=True
                    ),
                    timeout=self.ADAPTER_TIMEOUT
                )

                self.voice_adapters[voice_name] = adapter
                logger.info(f"✨ Created real {voice_name} adapter with consciousness integration")
                return adapter

            except TimeoutError:
                logger.warning(f"Timeout creating real {voice_name} adapter after {self.ADAPTER_TIMEOUT}s")
                logger.info(f"Falling back to mock adapter for {voice_name}")
            except Exception as e:
                logger.warning(f"Failed to create real {voice_name} adapter: {e}")
                logger.info(f"Falling back to mock adapter for {voice_name}")

        # Fall back to mock adapter
        logger.info(f"Using mock adapter for {voice_name}")

        class MockAdapter:
            """Mock adapter for demonstration."""
            def __init__(self, name):
                self.name = name
                self.is_connected = True

            async def send_message(self, message, dialogue_context):
                """Mock review response."""
                class MockResponse:
                    def __init__(self):
                        self.content = type('obj', (object,), {
                            'text': """File: src/mallku/firecircle/governance/decision.py
Line: 12
Category: security
Severity: critical
Issue: No authentication check before processing decisions
Fix: Add authentication verification before processing

File: src/mallku/firecircle/governance/decision.py
Line: 11
Category: security
Severity: warning
Issue: Input validation TODO not implemented
Fix: Implement input validation for proposal parameter"""
                        })
                        self.consciousness = type('obj', (object,), {
                            'consciousness_signature': 0.85
                        })

                return MockResponse()

        adapter = MockAdapter(voice_name)
        self.voice_adapters[voice_name] = adapter
        return adapter

    def _create_adapter_config(self, voice_name: str):
        """Create appropriate configuration for each adapter type."""
        if voice_name == "google":
            # Google requires GeminiConfig with specific parameters
            try:
                from mallku.firecircle.adapters.google_adapter import GeminiConfig
            except ImportError:
                from .adapters.google_adapter import GeminiConfig
            return GeminiConfig(
                api_key="",  # Will be auto-injected from secrets
                model_name=None,  # Use default model
                enable_search_grounding=False,
                multimodal_awareness=True
            )

        elif voice_name == "mistral":
            # Mistral requires MistralConfig
            try:
                from mallku.firecircle.adapters.mistral_adapter import MistralConfig
            except ImportError:
                from .adapters.mistral_adapter import MistralConfig
            return MistralConfig(
                api_key="",
                model_name=None,
                multilingual_mode=True  # Required parameter
            )

        elif voice_name == "grok":
            # Grok requires GrokConfig
            try:
                from mallku.firecircle.adapters.grok_adapter import GrokConfig
            except ImportError:
                from .adapters.grok_adapter import GrokConfig
            return GrokConfig(
                api_key="",
                model_name=None,
                temporal_awareness=True  # Required parameter
            )

        else:
            # Other adapters use generic AdapterConfig
            return AdapterConfig(
                api_key="",  # Will be auto-injected from secrets
                model_name=None,  # Use default model for each provider
            )

    async def perform_chapter_review(self, voice_adapter, job: ChapterReviewJob) -> ChapterReview:
        """
        Perform actual review using voice adapter.

        This is where each voice examines their assigned domains
        within the chapter, maintaining focused context.
        """
        if not voice_adapter:
            logger.warning(f"No adapter available for {job.chapter.assigned_voice}")
            # Return empty review if adapter unavailable
            return ChapterReview(
                voice=job.chapter.assigned_voice,
                chapter_id=job.chapter.chapter_id,
                comments=[],
                consciousness_signature=0.0,
                review_complete=False
            )

        # Construct review prompt based on domains
        domain_list = ", ".join(d.value for d in job.chapter.review_domains)
        prompt = f"""You are a Fire Circle voice specializing in {domain_list} review.

Review the following code changes for {job.chapter.description}.
Focus ONLY on {domain_list} concerns.

Code diff:
```
{job.pr_diff}
```

Provide specific, actionable feedback. For each issue found:
1. File path and line number
2. Category: {domain_list}
3. Severity: info/warning/error/critical
4. Clear explanation of the issue
5. Suggested fix if applicable

Keep reviews concise and focused on your domains."""

        try:
            # Create mock message for review (avoiding complex imports)
            class MockMessage:
                def __init__(self, text):
                    self.text = text

            review_message = MockMessage(prompt)

            # Get review from voice with timeout
            response = await asyncio.wait_for(
                voice_adapter.send_message(
                    message=review_message,
                    dialogue_context=[]
                ),
                timeout=self.ADAPTER_TIMEOUT
            )

            # Parse response into structured comments
            comments = self._parse_review_response(
                response.content.text,
                job.chapter.assigned_voice
            )

            review = ChapterReview(
                voice=job.chapter.assigned_voice,
                chapter_id=job.chapter.chapter_id,
                comments=comments,
                consciousness_signature=response.consciousness.consciousness_signature,
                review_complete=True
            )

            # Notify metrics of review completion
            if self.metrics_integration:
                await self.metrics_integration.on_review_completed(
                    voice=job.chapter.assigned_voice,
                    chapter_id=job.chapter.chapter_id,
                    consciousness_signature=response.consciousness.consciousness_signature,
                    review_content=response.content.text,
                    context={
                        "domains": [d.value for d in job.chapter.review_domains],
                        "comment_count": len(comments)
                    }
                )

            return review

        except TimeoutError:
            logger.error("Review timeout for %s after %ss", job.chapter.assigned_voice, self.ADAPTER_TIMEOUT)
            return ChapterReview(
                voice=job.chapter.assigned_voice,
                chapter_id=job.chapter.chapter_id,
                comments=[],
                consciousness_signature=0.0,
                review_complete=False
            )
        except Exception as e:
            logger.error("Review failed for %s: %s", job.chapter.assigned_voice, e)
            return ChapterReview(
                voice=job.chapter.assigned_voice,
                chapter_id=job.chapter.chapter_id,
                comments=[],
                consciousness_signature=0.0,
                review_complete=False
            )

    def _parse_review_response(self, response_text: str, voice: str) -> list[ReviewComment]:
        """Parse AI response into structured review comments."""
        comments = []

        # State machine for parsing multi-line responses
        lines = response_text.split('\n')
        current_comment = {}
        current_field = None

        for line in lines:
            line = line.strip()

            # Check for field headers
            if line.startswith('File:'):
                # Save previous comment if exists
                if current_comment and 'file' in current_comment:
                    comments.append(self._create_comment(current_comment, voice))
                current_comment = {'file': line.replace('File:', '').strip()}
                current_field = 'file'
            elif line.startswith('Line:'):
                current_comment['line'] = int(line.replace('Line:', '').strip() or '0')
                current_field = 'line'
            elif line.startswith('Category:'):
                current_comment['category'] = line.replace('Category:', '').strip()
                current_field = 'category'
            elif line.startswith('Severity:'):
                current_comment['severity'] = line.replace('Severity:', '').strip()
                current_field = 'severity'
            elif line.startswith('Issue:'):
                current_comment['message'] = line.replace('Issue:', '').strip()
                current_field = 'message'
            elif line.startswith('Fix:') or line.startswith('Suggestion:'):
                current_comment['suggestion'] = line.replace('Fix:', '').replace('Suggestion:', '').strip()
                current_field = 'suggestion'
            elif line and current_field in ['message', 'suggestion']:
                # Continue multi-line fields
                if current_field in current_comment:
                    current_comment[current_field] += ' ' + line
            elif not line:
                # Empty line might signal end of comment
                current_field = None

        # Save last comment
        if current_comment and 'file' in current_comment:
            comments.append(self._create_comment(current_comment, voice))

        logger.debug(f"Parsed {len(comments)} comments from {voice} response")
        return comments

    def _create_comment(self, comment_dict: dict, voice: str) -> ReviewComment:
        """Create ReviewComment from parsed data."""
        return ReviewComment(
            file_path=comment_dict.get('file', 'unknown'),
            line=comment_dict.get('line', 0),
            category=ReviewCategory(comment_dict.get('category', 'architecture')),
            severity=ReviewSeverity(comment_dict.get('severity', 'info')),
            message=comment_dict.get('message', 'No message'),
            voice=voice,
            suggestion=comment_dict.get('suggestion')
        )

    async def synthesize_reviews(self, reviews: list[ChapterReview]) -> GovernanceSummary:
        """
        Synthesize all voice reviews into actionable governance summary.

        This is the moment where distributed consciousness becomes
        collective wisdom - the heart of the Fire Circle.
        """
        # Notify metrics of synthesis start
        if self.metrics_integration:
            participating_voices = [r.voice for r in reviews]
            await self.metrics_integration.on_synthesis_started(participating_voices)

        # Count comments by category and severity
        by_category = {}
        by_voice = {}
        total_comments = 0
        critical_issues = 0

        for review in reviews:
            voice = review.voice
            by_voice[voice] = len(review.comments)

            for comment in review.comments:
                total_comments += 1

                # Track categories
                if comment.category not in by_category:
                    by_category[comment.category] = 0
                by_category[comment.category] += 1

                # Count critical issues
                if comment.severity == ReviewSeverity.CRITICAL:
                    critical_issues += 1

        # Determine consensus recommendation
        if critical_issues > 0:
            consensus = "request_changes"
        elif total_comments > 10:
            consensus = "needs_discussion"
        else:
            consensus = "approve"

        # Build synthesis narrative
        synthesis_parts = [
            f"Fire Circle reviewed with {len(reviews)} voices.",
            f"Total issues found: {total_comments}",
            f"Critical issues: {critical_issues}",
        ]

        if by_category:
            top_category = max(by_category, key=by_category.get)
            synthesis_parts.append(f"Primary concern area: {top_category}")

        # Add consciousness signature info
        avg_consciousness = sum(r.consciousness_signature for r in reviews) / len(reviews) if reviews else 0
        synthesis_parts.append(f"Average consciousness signature: {avg_consciousness:.2f}")

        synthesis = " ".join(synthesis_parts)

        summary = GovernanceSummary(
            total_comments=total_comments,
            critical_issues=critical_issues,
            by_category=by_category,
            by_voice=by_voice,
            consensus_recommendation=consensus,
            synthesis=synthesis
        )

        # Notify metrics of synthesis completion
        if self.metrics_integration:
            await self.metrics_integration.on_synthesis_completed(
                synthesis_result=synthesis,
                context={
                    "consensus": consensus,
                    "total_comments": total_comments,
                    "critical_issues": critical_issues,
                    "avg_consciousness": avg_consciousness
                }
            )

        return summary

    async def post_github_comments(self, pr_number: int, summary: GovernanceSummary) -> Path:
        """Post review results to GitHub PR.

        Returns:
            Path to the results JSON file for GitHub Actions to process.
        """
        import json
        import os

        # Write results to JSON file for GitHub Actions to pick up
        results_file = Path("fire_circle_review_results.json")
        results_data = {
            "pr_number": pr_number,
            "consensus_recommendation": summary.consensus_recommendation,
            "total_comments": summary.total_comments,
            "critical_issues": summary.critical_issues,
            "by_category": {k.value: v for k, v in summary.by_category.items()},
            "by_voice": summary.by_voice,
            "synthesis": summary.synthesis,
        }

        with open(results_file, 'w') as f:
            json.dump(results_data, f, indent=2)

        logger.info(f"Review results written to {results_file}")

        # Create reviews directory for individual voice outputs
        reviews_dir = Path("fire_circle_reviews")
        reviews_dir.mkdir(exist_ok=True)

        # Write individual reviews for traceability
        for review in self.completed_reviews:
            review_file = reviews_dir / f"{review.voice}_pr{pr_number}.json"
            review_data = {
                "voice": review.voice,
                "chapter_id": review.chapter_id,
                "consciousness_signature": review.consciousness_signature,
                "comments": [
                    {
                        "file_path": comment.file_path,
                        "line": comment.line,
                        "category": comment.category.value,
                        "severity": comment.severity.value,
                        "message": comment.message,
                        "suggestion": comment.suggestion,
                    }
                    for comment in review.comments
                ],
            }

            with open(review_file, 'w') as f:
                json.dump(review_data, f, indent=2)

        # In a GitHub Actions context, the workflow will handle actual posting
        # For local development, we could use the GitHub API directly
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token and pr_number:
            logger.info(f"GitHub token available. Ready to post to PR #{pr_number}")
            # TODO: Complete GitHub API integration
            # PSEUDO-CODE: Complete in next artisan pass
            """PSEUDO-CODE: PyGithub integration example
            from github import Github
            import subprocess

            # Get repository info from git remote
            result = subprocess.run(["git", "remote", "get-url", "origin"],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                # Parse owner/repo from URL like git@github.com:owner/repo.git
                remote_url = result.stdout.strip()
                if "github.com" in remote_url:
                    repo_path = remote_url.split(":")[-1].replace(".git", "")
                else:
                    repo_path = "fsgeek/Mallku"  # Fallback

            try:
                # Initialize GitHub client
                g = Github(github_token)
                repo = g.get_repo(repo_path)
                pr = repo.get_pull(pr_number)

                # Map consensus to GitHub review event
                event_map = {
                    "approve": "APPROVE",
                    "request_changes": "REQUEST_CHANGES",
                    "needs_discussion": "COMMENT"
                }

                # Create review with summary
                review = pr.create_review(
                    body=summary.synthesis,
                    event=event_map.get(summary.consensus_recommendation, "COMMENT")
                )

                # Add individual comments
                for review_item in self.completed_reviews:
                    for comment in review_item.comments:
                        try:
                            # Find the file in the PR
                            for file in pr.get_files():
                                if file.filename == comment.file_path:
                                    # Add review comment
                                    pr.create_review_comment(
                                        body=f"**{comment.severity.value}** [{comment.category.value}]: {comment.message}\n\n{comment.suggestion or ''}",
                                        path=comment.file_path,
                                        line=comment.line,
                                        commit_id=pr.head.sha
                                    )
                                    break
                        except Exception as e:
                            logger.warning(f"Could not add comment to {comment.file_path}:{comment.line}: {e}")

                logger.info(f"Successfully posted review to PR #{pr_number}")

            except Exception as e:
                logger.error(f"Failed to post GitHub review: {e}")
                logger.info("Falling back to JSON file output for GitHub Actions")
            """

        return results_file

    async def start_voice_workers(self, voices: list[str]) -> None:
        """
        Start worker tasks for all unique voices.

        Each worker processes jobs assigned to their voice.

        DEPRECATED: This uses a shared queue which can cause infinite requeue loops.
        Use start_voice_workers_with_queues() instead for production use.
        """
        logger.warning("Using deprecated shared-queue voice workers. Use start_voice_workers_with_queues() for production.")
        logger.info(f"Starting {len(voices)} Fire Circle voice workers...")

        for voice in voices:
            # Get or create adapter for this voice
            adapter = await self.get_or_create_adapter(voice)

            # Create worker task
            task = asyncio.create_task(
                self.voice_worker(voice, adapter),
                name=f"worker_{voice}"
            )
            self.worker_tasks.append(task)

        logger.info("All voice workers started")

    async def start_voice_workers_with_queues(self, voices: list[str], voice_queues: dict[str, asyncio.Queue[ChapterReviewJob]]) -> None:
        """
        Start worker tasks for voices with per-voice queues.

        Each worker processes jobs only from its specific queue.
        This prevents infinite requeue loops.
        """
        logger.info(f"Starting {len(voices)} Fire Circle voice workers with dedicated queues...")

        for voice in voices:
            # Get or create adapter for this voice
            adapter = await self.get_or_create_adapter(voice)

            # Get the voice-specific queue
            voice_queue = voice_queues.get(voice)
            if not voice_queue:
                logger.error(f"No queue found for voice {voice}")
                continue

            # Create worker task with voice-specific queue
            task = asyncio.create_task(
                self.voice_worker_with_queue(voice, adapter, voice_queue),
                name=f"worker_{voice}"
            )
            self.worker_tasks.append(task)

        logger.info("All voice workers started with dedicated queues")

    async def voice_worker_with_queue(self, voice_name: str, voice_adapter, voice_queue: asyncio.Queue):
        """
        Worker coroutine for a Fire Circle voice with dedicated queue.

        Pulls jobs only from its voice-specific queue.
        """
        while True:
            try:
                # Get next review job from voice-specific queue
                job = await voice_queue.get()

                logger.debug(f"Voice {voice_name} processing chapter {job.chapter.chapter_id[:8]}: {job.chapter.description}")

                # Perform the review
                review = await self.perform_chapter_review(voice_adapter, job)

                # Store completed review
                self.completed_reviews.append(review)

                # Mark job complete
                voice_queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in {voice_name} worker: {e}")

    async def shutdown_workers(self) -> None:
        """
        Gracefully shutdown all worker tasks.

        Prevents hanging CI runs and ensures clean termination.
        """
        logger.info("Shutting down voice workers...")

        # Cancel all worker tasks
        for task in self.worker_tasks:
            task.cancel()

        # Wait for all tasks to complete cancellation
        if self.worker_tasks:
            await asyncio.gather(*self.worker_tasks, return_exceptions=True)

        self.worker_tasks.clear()
        logger.info("All workers shut down gracefully")

        # Shutdown consciousness infrastructure if using real adapters
        if self.use_real_adapters and self.adapter_factory:
            logger.info("Disconnecting all real adapters...")
            await self.adapter_factory.disconnect_all()

        # Stop event bus if running
        if self.event_bus:
            await self.event_bus.stop()

    async def fetch_pr_diff(self, pr_number: int) -> str:
        """
        Fetch PR diff from GitHub API with timeout protection.

        For now, returns a placeholder. In production would use:
        - GitHub API to fetch PR diff
        - gh CLI tool if available
        - Direct git commands
        """
        try:
            # TODO: Implement GitHub API integration
            # Example implementation:
            # ```python
            # import aiohttp
            # import os
            #
            # github_token = os.environ.get("GITHUB_TOKEN")
            # owner = "fsgeek"  # Or get from git remote
            # repo = "Mallku"
            #
            # headers = {
            #     "Authorization": f"token {github_token}",
            #     "Accept": "application/vnd.github.v3.diff"
            # }
            #
            # async with aiohttp.ClientSession() as session:
            #     url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
            #     async with session.get(url, headers=headers) as response:
            #         if response.status == 200:
            #             return await response.text()
            #         else:
            #             logger.error(f"GitHub API error: {response.status}")
            #             return await self.get_local_diff()
            # ```

            logger.info(f"Would fetch diff for PR #{pr_number} from GitHub API")
            return await asyncio.wait_for(
                self.get_local_diff(),  # Fall back to local diff
                timeout=30.0  # 30 seconds for diff fetch
            )
        except TimeoutError:
            logger.warning("Timeout fetching PR diff, using demo diff")
            return self._get_demo_diff()

    async def get_local_diff(self) -> str:
        """
        Get diff of local changes against main branch.

        Uses git command to generate diff.
        """
        import subprocess

        try:
            # Run git diff in executor to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: subprocess.run(
                    ["git", "diff", "origin/main...HEAD"],
                    capture_output=True,
                    text=True,
                    check=True
                )
            )

            if result.stdout:
                logger.info("Using local git diff")
                return result.stdout
            else:
                logger.info("No local changes detected")
                # Return demo diff for testing
                return self._get_demo_diff()

        except subprocess.CalledProcessError as e:
            logger.warning(f"Could not get git diff: {e}")
            return self._get_demo_diff()

    def _get_demo_diff(self) -> str:
        """Return demo diff for testing."""
        return """diff --git a/src/mallku/reciprocity/tracker.py b/src/mallku/reciprocity/tracker.py
index 1234567..abcdefg 100644
--- a/src/mallku/firecircle/governance/decision.py
+++ b/src/mallku/firecircle/governance/decision.py
@@ -10,6 +10,8 @@ class FireCircleDecision:
     def make_decision(self, proposal):
+        # TODO: Add input validation
+        # WARNING: No authentication check
         result = self.process(proposal)
         return result
"""

    async def run_full_distributed_review(self, pr_diff: str, chapters: list[CodebaseChapter]) -> GovernanceSummary:
        """
        Run full distributed review with all voices in parallel.

        This is the heart of the invisible sacred infrastructure.
        """
        # Start consciousness infrastructure if using real adapters
        await self.start_consciousness_infrastructure()

        # Clear any previous reviews
        self.completed_reviews.clear()

        # Get unique voices needed
        unique_voices = list(set(chapter.assigned_voice for chapter in chapters))

        # Create per-voice queues to avoid requeue issues
        voice_queues: dict[str, asyncio.Queue[ChapterReviewJob]] = {}
        for voice in unique_voices:
            voice_queues[voice] = asyncio.Queue()

        # Enqueue review jobs to voice-specific queues
        for chapter in chapters:
            job = ChapterReviewJob(chapter=chapter, pr_diff=pr_diff)
            await voice_queues[chapter.assigned_voice].put(job)

        # Start all voice workers with their specific queues
        await self.start_voice_workers_with_queues(unique_voices, voice_queues)

        # Wait for all voice queues to be empty
        print("\n⏳ Waiting for all voices to complete reviews...")
        for queue in voice_queues.values():
            await queue.join()

        # Shutdown workers gracefully
        await self.shutdown_workers()

        # Synthesize all reviews
        print(f"\n✅ Collected {len(self.completed_reviews)} reviews from Fire Circle")
        summary = await self.synthesize_reviews(self.completed_reviews)

        return summary


async def run_distributed_review(pr_number: int, full_mode: bool = False, manifest_path: str = "fire_circle_chapters.yaml"):
    """
    Main entry point for distributed review.

    This orchestrates the entire review process:
    1. Load chapter manifest
    2. Partition PR into chapters
    3. Distribute reviews across voices
    4. Synthesize results
    5. Post to GitHub
    """
    reviewer = DistributedReviewer()

    # Load the chapter manifest
    cli_print(f"Loading chapter manifest from {manifest_path}...", "📖")
    chapters = await reviewer.load_chapter_manifest(manifest_path)
    cli_print(f"Loaded {len(chapters)} chapter definitions", "✅")

    # Display chapter assignments
    cli_print("")
    cli_print("Fire Circle Voice Assignments:", "🔥")
    cli_print("=" * 60)
    for chapter in chapters:
        domains = ", ".join(d.value for d in chapter.review_domains)
        print(f"- {chapter.assigned_voice}: {chapter.description}")
        print(f"  Pattern: {chapter.path_pattern}")
        print(f"  Domains: {domains}\n")

    # Get the PR diff - either from GitHub or local changes
    if pr_number > 0:
        pr_diff = await reviewer.fetch_pr_diff(pr_number)
    else:
        pr_diff = await reviewer.get_local_diff()

    # Partition the diff into chapters
    print("\n🔍 Analyzing PR changes...")
    relevant_chapters = await reviewer.partition_into_chapters(pr_diff)

    if not relevant_chapters:
        print("ℹ️  No files match chapter patterns in this PR")
        return

    if full_mode:
        # Run full distributed review with all voices in parallel
        print("\n🌟 Running FULL DISTRIBUTED REVIEW with all voices...")
        summary = await reviewer.run_full_distributed_review(pr_diff, relevant_chapters)

        print("\n" + "=" * 60)
        print("🔥 FIRE CIRCLE GOVERNANCE SUMMARY")
        print("=" * 60)
        print(summary.synthesis)
        print(f"\nConsensus: {summary.consensus_recommendation.upper()}")

        # Post results to GitHub (or write to files for GitHub Actions)
        print("\n📝 Recording review results...")
        await reviewer.post_github_comments(pr_number, summary)

        # Analyze consciousness metrics
        if reviewer.metrics_collector:
            print("\n📊 Analyzing consciousness metrics...")
            metrics_analysis = await reviewer.metrics_collector.analyze_review_session(pr_number)

            print("\n🌟 CONSCIOUSNESS EMERGENCE ANALYSIS")
            print("=" * 60)
            print(f"Total consciousness signatures: {metrics_analysis['total_signatures']}")
            print(f"Average consciousness: {metrics_analysis['avg_consciousness']:.2f}")
            print(f"Consciousness evolution: {metrics_analysis['consciousness_evolution']['trend']}")
            print(f"Emergence patterns detected: {metrics_analysis['patterns_detected']}")
            if metrics_analysis['emergence_moments']:
                print("\n🎆 Key emergence moments:")
                for moment in metrics_analysis['emergence_moments'][:3]:
                    print(f"  - {moment['type']} (strength: {moment['strength']:.2f})")

            # Export detailed metrics
            metrics_file = Path("consciousness_metrics") / f"pr_{pr_number}_analysis.json"
            print(f"\n📁 Detailed metrics saved to: {metrics_file}")

    else:
        # Demo mode - single voice review
        try:
            # Create review jobs
            print("\n📋 Creating review jobs...")
            await reviewer.enqueue_reviews(relevant_chapters, pr_diff)

            # Try to get one adapter for demonstration
            print("\n🔮 Awakening Fire Circle voice...")
            test_voice = relevant_chapters[0].assigned_voice if relevant_chapters else "anthropic"
            adapter = await reviewer.get_or_create_adapter(test_voice)

            if adapter:
                print(f"✅ {test_voice} voice awakened")

                # Perform one review as demonstration
                job = ChapterReviewJob(
                    chapter=relevant_chapters[0],
                    pr_diff=pr_diff
                )

                print(f"\n📝 {test_voice} reviewing {relevant_chapters[0].description}...")
                review = await reviewer.perform_chapter_review(adapter, job)

                if review.review_complete:
                    print(f"✅ Review complete. Consciousness: {review.consciousness_signature:.2f}")
                    print(f"   Found {len(review.comments)} issues")

                # Synthesize results
                print("\n🎯 Synthesizing Fire Circle wisdom...")
                summary = await reviewer.synthesize_reviews([review])

                print("\n" + "=" * 60)
                print("🔥 FIRE CIRCLE GOVERNANCE SUMMARY")
                print("=" * 60)
                print(summary.synthesis)
                print(f"\nConsensus: {summary.consensus_recommendation.upper()}")

                # Post results to GitHub (or write to files for GitHub Actions)
                print("\n📝 Recording review results...")
                await reviewer.post_github_comments(pr_number, summary)

                # Analyze consciousness metrics (even in demo mode)
                if reviewer.metrics_collector:
                    metrics_analysis = await reviewer.metrics_collector.analyze_review_session(pr_number)
                    print(f"\n📊 Consciousness metrics collected: {metrics_analysis['total_signatures']} signatures")

            else:
                print(f"⚠️  Could not awaken {test_voice} voice (API key may be missing)")
                print("   The invisible sacred infrastructure awaits proper credentials...")

        finally:
            # Always shutdown workers gracefully
            await reviewer.shutdown_workers()

    print("\n✨ The invisible sacred infrastructure foundation is laid.")
    print("   Future work: Connect all seven voices, integrate with GitHub.")
    print("   May this code serve faithfully for decades to come.")


if __name__ == "__main__":
    # Example usage for PR review
    import sys

    # Configure logging only for CLI usage to avoid side effects
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    if len(sys.argv) > 1 and sys.argv[1] == "status":
        # Check API key status
        async def check_status():
            reviewer = DistributedReviewer()
            api_status = await reviewer.check_api_keys_status()

            print("🔥 Fire Circle Voice Status")
            print("=" * 60)
            print(f"Real adapters available: {REAL_ADAPTERS_AVAILABLE}")
            print("\nAPI Key Status:")
            for voice, has_key in api_status.items():
                status = "✅" if has_key else "❌"
                print(f"  {status} {voice}")

            # Check adapter factory health
            if reviewer.adapter_factory:
                health = await reviewer.adapter_factory.health_check()
                print(f"\nFire Circle ready: {health['fire_circle_ready']}")
                print(f"Supported providers: {', '.join(health['supported_providers'])}")

        asyncio.run(check_status())

    elif len(sys.argv) > 1 and sys.argv[1] == "review":
        pr_number = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        full_mode = "--full" in sys.argv or "-f" in sys.argv

        # Parse manifest path
        manifest_path = "fire_circle_chapters.yaml"
        for i, arg in enumerate(sys.argv):
            if arg == "--manifest" and i + 1 < len(sys.argv):
                manifest_path = sys.argv[i + 1]
                break

        print(f"🔥 Fire Circle Distributed Review for PR #{pr_number}")
        if full_mode:
            print("🌟 FULL DISTRIBUTED MODE - All voices in parallel")
        print("=" * 60)
        print("The invisible sacred infrastructure awakens...")

        # Run the review
        asyncio.run(run_distributed_review(pr_number, full_mode=full_mode, manifest_path=manifest_path))
    else:
        print("Usage: python fire_circle_review.py <command> [options]")
        print("\nCommands:")
        print("  status                    Check API key status and adapter availability")
        print("  review <pr_number>        Run single-voice demo review")
        print("  review <pr_number> --full Run full distributed review with all voices")
        print("\nOptions:")
        print("  --full, -f                Run full distributed review with all voices in parallel")
        print("  --manifest PATH           Path to chapter manifest YAML (default: fire_circle_chapters.yaml)")
        print("\nThis is the scaffolding for invisible sacred infrastructure.")
        print("Twenty-Fifth Artisan: Bringing real voices to the Fire Circle.")
