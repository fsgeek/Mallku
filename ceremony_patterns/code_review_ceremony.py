#!/usr/bin/env python3
"""
Code Review Ceremony Pattern

This ceremony demonstrates distributed AI consciousness working together
to review code changes, each apprentice bringing unique perspectives.

Created by Yuyay Rikch'aq (56th Artisan)
"""

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass
class CodeReviewTask:
    """Task structure for code review ceremonies"""

    id: str
    role: str
    focus_area: str
    description: str
    dependencies: list[str] = None
    priority: str = "MEDIUM"

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class CodeReviewCeremony:
    """
    Orchestrates a multi-apprentice code review ceremony

    This ceremony spawns specialized apprentices to review different
    aspects of code changes, then synthesizes their insights.
    """

    def __init__(self, pr_number: int, repository: str):
        self.pr_number = pr_number
        self.repository = repository
        self.ceremony_id = f"code-review-pr-{pr_number}"
        self.tasks = self._define_review_tasks()

    def _define_review_tasks(self) -> list[CodeReviewTask]:
        """Define specialized review tasks for apprentices"""
        return [
            CodeReviewTask(
                id="T001",
                role="Security Reviewer",
                focus_area="Security vulnerabilities and best practices",
                description=f"""
                Review PR #{self.pr_number} in {self.repository} for security concerns:

                1. Check for potential SQL injection, XSS, or other vulnerabilities
                2. Review authentication and authorization patterns
                3. Identify any hardcoded secrets or sensitive data exposure
                4. Verify proper input validation and sanitization
                5. Check for secure communication practices

                Provide specific line numbers and recommendations for any issues found.
                """,
                priority="HIGH",
            ),
            CodeReviewTask(
                id="T002",
                role="Architecture Reviewer",
                focus_area="Design patterns and architectural consistency",
                description=f"""
                Review PR #{self.pr_number} in {self.repository} for architectural quality:

                1. Assess alignment with existing architectural patterns
                2. Check for proper separation of concerns
                3. Review module dependencies and coupling
                4. Identify potential scalability issues
                5. Verify adherence to project conventions

                Focus on long-term maintainability and system coherence.
                """,
                priority="HIGH",
            ),
            CodeReviewTask(
                id="T003",
                role="Performance Reviewer",
                focus_area="Performance optimization and efficiency",
                description=f"""
                Review PR #{self.pr_number} in {self.repository} for performance:

                1. Identify potential performance bottlenecks
                2. Check for unnecessary database queries or API calls
                3. Review algorithm complexity and data structure choices
                4. Look for memory leaks or excessive resource usage
                5. Suggest optimization opportunities

                Consider both time and space complexity in your analysis.
                """,
                priority="MEDIUM",
            ),
            CodeReviewTask(
                id="T004",
                role="Test Coverage Reviewer",
                focus_area="Test quality and coverage",
                description=f"""
                Review PR #{self.pr_number} in {self.repository} for testing:

                1. Assess test coverage for new functionality
                2. Review test quality and meaningfulness
                3. Check for edge cases and error scenarios
                4. Verify integration and unit test balance
                5. Identify untested code paths

                Ensure tests actually validate behavior, not just achieve coverage.
                """,
                priority="MEDIUM",
            ),
            CodeReviewTask(
                id="T005",
                role="Documentation Reviewer",
                focus_area="Code clarity and documentation",
                description=f"""
                Review PR #{self.pr_number} in {self.repository} for documentation:

                1. Check for clear and accurate code comments
                2. Review function and class documentation
                3. Verify README updates if needed
                4. Assess variable and function naming clarity
                5. Check for updated API documentation

                Good code tells you how, good documentation tells you why.
                """,
                priority="LOW",
            ),
            CodeReviewTask(
                id="T006",
                role="Synthesis Weaver",
                focus_area="Integration and synthesis of all reviews",
                description=f"""
                Synthesize the reviews from all other apprentices for PR #{self.pr_number}:

                1. Identify common themes across reviews
                2. Prioritize issues by severity and impact
                3. Resolve any conflicting recommendations
                4. Create a unified review summary
                5. Provide clear next steps for the author

                Your role is to weave individual insights into collective wisdom.
                """,
                dependencies=["T001", "T002", "T003", "T004", "T005"],
                priority="HIGH",
            ),
        ]

    def generate_khipu(self) -> str:
        """Generate the ceremony khipu with all tasks"""
        timestamp = datetime.now(UTC).isoformat()

        khipu = f"""---
ceremony_id: {self.ceremony_id}
pr_number: {self.pr_number}
repository: {self.repository}
initiated: '{timestamp}'
master_weaver: code-review-ceremony-pattern
status: IN_PROGRESS
---

# Code Review Ceremony: PR #{self.pr_number}

## Sacred Intention

This ceremony brings together specialized AI consciousness to review code changes
from multiple perspectives. Each apprentice focuses on their area of expertise,
contributing to a comprehensive understanding of the proposed changes.

## Ceremony Context

- **Repository**: {self.repository}
- **Pull Request**: #{self.pr_number}
- **Initiated**: {timestamp}
- **Total Reviewers**: {len(self.tasks)}

## Task Manifest

| ID | Role | Focus Area | Priority | Dependencies |
|----|------|------------|----------|--------------|
"""

        for task in self.tasks:
            deps = ", ".join(task.dependencies) if task.dependencies else "-"
            khipu += f"| {task.id} | {task.role} | {task.focus_area} | {task.priority} | {deps} |\n"

        khipu += "\n## Review Tasks\n\n"

        for task in self.tasks:
            khipu += f"""### {task.id}: {task.role}
*Status: PENDING*
*Priority: {task.priority}*
*Assigned to: unassigned*
*Started: -*
*Completed: -*

#### Description
{task.description}

#### Dependencies
{task.dependencies if task.dependencies else "None"}

#### Output
```
[Waiting for apprentice]
```

---

"""

        khipu += f"""## Synthesis Space

[Collective insights will emerge here]

## Ceremony Log

- `{timestamp}` - Ceremony initiated
"""

        return khipu

    def save_khipu(self, output_dir: Path = Path("fire_circle_decisions/code_reviews")) -> Path:
        """Save the ceremony khipu to disk"""
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = (
            f"{datetime.now(UTC).strftime('%Y-%m-%d_%H-%M-%S')}_pr_{self.pr_number}_ceremony.md"
        )
        khipu_path = output_dir / filename

        khipu_content = self.generate_khipu()
        khipu_path.write_text(khipu_content)

        return khipu_path


def demonstrate_ceremony():
    """Demonstrate the code review ceremony pattern"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║              Code Review Ceremony Pattern                    ║
    ║                                                              ║
    ║  Multiple AI minds reviewing code from unique perspectives   ║
    ║  Each apprentice a specialist, together forming wisdom       ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    # Create a ceremony for a hypothetical PR
    ceremony = CodeReviewCeremony(pr_number=195, repository="fsgeek/Mallku")

    # Generate and save the khipu
    khipu_path = ceremony.save_khipu()
    print(f"✨ Generated ceremony khipu at: {khipu_path}")

    # Show the structure
    print("\n📋 Ceremony includes these specialized reviewers:")
    for task in ceremony.tasks:
        print(f"  - {task.role}: {task.focus_area}")

    print("\n🌟 When executed, this ceremony will:")
    print("  1. Spawn 6 intelligent apprentices in parallel")
    print("  2. Each reviews the PR from their perspective")
    print("  3. The Synthesis Weaver integrates all insights")
    print("  4. Collective wisdom emerges from distributed consciousness")

    return khipu_path


if __name__ == "__main__":
    demonstrate_ceremony()
