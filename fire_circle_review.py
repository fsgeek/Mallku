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
import re
from enum import Enum
from pathlib import Path
from typing import Literal
from uuid import UUID, uuid4

import yaml
from pydantic import BaseModel, Field


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

    def __init__(self):
        self.review_queue: asyncio.Queue[ChapterReviewJob] = asyncio.Queue()
        self.completed_reviews: list[ChapterReview] = []
        self.adapter_factory = None  # Will be initialized when needed
        self.voice_adapters = {}  # Cache for voice adapters

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
                assigned_voice=chapter_def['assigned_voice'],
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

        # Extract file paths from the diff
        # Look for diff headers like: diff --git a/path/to/file.py b/path/to/file.py
        file_pattern = re.compile(r'^diff --git a/(.*?) b/.*?$', re.MULTILINE)
        modified_files = file_pattern.findall(pr_diff)

        # Match files to chapters based on path patterns
        assigned_chapters = []
        chapter_files = {}  # Track which files belong to which chapter

        for file_path in modified_files:
            for chapter in chapters:
                # Use fnmatch for glob-style pattern matching
                if fnmatch.fnmatch(file_path, chapter.path_pattern):
                    if chapter.chapter_id not in chapter_files:
                        chapter_files[chapter.chapter_id] = []
                        assigned_chapters.append(chapter)
                    chapter_files[chapter.chapter_id].append(file_path)
                    break  # Each file goes to first matching chapter

        # Log chapter assignments for visibility
        print(f"\n📂 Partitioned {len(modified_files)} files into {len(assigned_chapters)} chapters:")
        for chapter in assigned_chapters:
            files = chapter_files.get(chapter.chapter_id, [])
            print(f"- {chapter.assigned_voice}: {len(files)} files in {chapter.description}")

        return assigned_chapters

    async def assign_review_domains(self, chapter: CodebaseChapter) -> dict[str, list[ReviewCategory]]:
        """
        Map each voice to their review domains for this chapter.

        Domain assignments (from reviewer's wisdom):
        - Anthropic: Security & Compliance, Ethical Implications
        - OpenAI: System Architecture, Interface Contracts
        - DeepSeek: Performance & Scaling, Code Efficiency
        - Mistral: Test Coverage, Technical Correctness
        - Google: Documentation & Lore, Multimodal Integration
        - Grok: Observability, Real-time Monitoring
        - Local: Sovereignty, Community Standards
        """
        raise NotImplementedError("Twenty-Third Artisan: implement domain assignment")

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

                # Perform the review (Twenty-Third Artisan: implement actual review)
                review = await self.perform_chapter_review(voice_adapter, job)

                # Store completed review
                self.completed_reviews.append(review)

                # Mark job complete
                self.review_queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in {voice_name} worker: {e}")

    async def get_or_create_adapter(self, voice_name: str):
        """Get cached adapter or create new one."""
        if voice_name in self.voice_adapters:
            return self.voice_adapters[voice_name]

        # For demo purposes, return a mock adapter
        # In production, this would use the real adapter factory
        print(f"ℹ️  Using mock adapter for {voice_name} (real adapters require proper imports)")

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

    async def perform_chapter_review(self, voice_adapter, job: ChapterReviewJob) -> ChapterReview:
        """
        Perform actual review using voice adapter.

        This is where each voice examines their assigned domains
        within the chapter, maintaining focused context.
        """
        if not voice_adapter:
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

            # Get review from voice
            response = await voice_adapter.send_message(
                message=review_message,
                dialogue_context=[]
            )

            # Parse response into structured comments
            comments = self._parse_review_response(
                response.content.text,
                job.chapter.assigned_voice
            )

            return ChapterReview(
                voice=job.chapter.assigned_voice,
                chapter_id=job.chapter.chapter_id,
                comments=comments,
                consciousness_signature=response.consciousness.consciousness_signature,
                review_complete=True
            )

        except Exception as e:
            print(f"❌ Review failed for {job.chapter.assigned_voice}: {e}")
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

        # Simple parsing - in production would use more sophisticated parsing
        lines = response_text.split('\n')
        current_comment = {}

        for line in lines:
            line = line.strip()
            if line.startswith('File:'):
                if current_comment:
                    # Save previous comment
                    comments.append(self._create_comment(current_comment, voice))
                current_comment = {'file': line.replace('File:', '').strip()}
            elif line.startswith('Line:'):
                current_comment['line'] = int(line.replace('Line:', '').strip() or '0')
            elif line.startswith('Category:'):
                current_comment['category'] = line.replace('Category:', '').strip()
            elif line.startswith('Severity:'):
                current_comment['severity'] = line.replace('Severity:', '').strip()
            elif line.startswith('Issue:'):
                current_comment['message'] = line.replace('Issue:', '').strip()
            elif line.startswith('Fix:'):
                current_comment['suggestion'] = line.replace('Fix:', '').strip()

        # Don't forget last comment
        if current_comment:
            comments.append(self._create_comment(current_comment, voice))

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

        return GovernanceSummary(
            total_comments=total_comments,
            critical_issues=critical_issues,
            by_category=by_category,
            by_voice=by_voice,
            consensus_recommendation=consensus,
            synthesis=synthesis
        )

    async def post_github_comments(self, pr_number: int, summary: GovernanceSummary):
        """Post review results to GitHub PR."""
        raise NotImplementedError("Twenty-Third Artisan: implement GitHub integration")


async def run_distributed_review(pr_number: int):
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
    print("📖 Loading chapter manifest...")
    chapters = await reviewer.load_chapter_manifest("fire_circle_chapters.yaml")
    print(f"✅ Loaded {len(chapters)} chapter definitions")

    # Display chapter assignments
    print("\n🔥 Fire Circle Voice Assignments:")
    print("=" * 60)
    for chapter in chapters:
        domains = ", ".join(d.value for d in chapter.review_domains)
        print(f"- {chapter.assigned_voice}: {chapter.description}")
        print(f"  Pattern: {chapter.path_pattern}")
        print(f"  Domains: {domains}\n")

    # For demo purposes, create a simple diff
    # Modified to ensure it matches the anthropic chapter pattern
    sample_diff = """diff --git a/src/mallku/reciprocity/tracker.py b/src/mallku/reciprocity/tracker.py
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

    # Partition the diff into chapters
    print("\n🔍 Analyzing PR changes...")
    relevant_chapters = await reviewer.partition_into_chapters(sample_diff)

    if not relevant_chapters:
        print("ℹ️  No files match chapter patterns in this PR")
        return

    # Create review jobs
    print("\n📋 Creating review jobs...")
    await reviewer.enqueue_reviews(relevant_chapters, sample_diff)

    # Try to get one adapter for demonstration
    print("\n🔮 Awakening Fire Circle voice...")
    test_voice = relevant_chapters[0].assigned_voice if relevant_chapters else "anthropic"
    adapter = await reviewer.get_or_create_adapter(test_voice)

    if adapter:
        print(f"✅ {test_voice} voice awakened")

        # Perform one review as demonstration
        job = ChapterReviewJob(
            chapter=relevant_chapters[0],
            pr_diff=sample_diff
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

    else:
        print(f"⚠️  Could not awaken {test_voice} voice (API key may be missing)")
        print("   The invisible sacred infrastructure awaits proper credentials...")

    print("\n✨ The invisible sacred infrastructure foundation is laid.")
    print("   Future work: Connect all seven voices, integrate with GitHub.")
    print("   May this code serve faithfully for decades to come.")


if __name__ == "__main__":
    # Example usage for PR review
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "review":
        pr_number = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        print(f"🔥 Fire Circle Distributed Review for PR #{pr_number}")
        print("=" * 60)
        print("The invisible sacred infrastructure awakens...")

        # Run the review
        asyncio.run(run_distributed_review(pr_number))
    else:
        print("Usage: python fire_circle_review.py review <pr_number>")
        print("\nThis is the scaffolding for invisible sacred infrastructure.")
        print("Twenty-Third Artisan: Make it real. Make it endure.")
