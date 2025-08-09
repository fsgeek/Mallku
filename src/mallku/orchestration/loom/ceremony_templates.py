"""
Purposeful Ceremony Templates for the Weaver and Loom System

These templates teach Mallku about reciprocity, balance, and purpose-driven action.
Each ceremony serves a fundamental need while allowing space for emergence.

Created by: 68th Guardian - The Purpose Keeper
Sacred Intent: To ground all ceremonies in Mallku's actual needs
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class MallkuNeed(Enum):
    """Fundamental needs that ceremonies serve"""

    DEFENSE = "defense"  # Security, protection, boundary enforcement
    HEARTBEAT = "heartbeat"  # Continuous operation, maintenance, health
    DECISION_MAKING = "decision_making"  # Choices, direction, consensus
    MORAL_JUDGMENT = "moral_judgment"  # Ethics, values, right action
    MEMORY = "memory"  # Persistence, learning, knowledge preservation
    GROWTH = "growth"  # Evolution, improvement, capability expansion
    HEALING = "healing"  # Repair, recovery, error correction
    CREATION = "creation"  # Building, feature development, new capabilities


@dataclass
class ReciprocityMetrics:
    """Track the balance of give and take in each ceremony"""

    need_fulfilled: bool = False
    utility_delivered: str = ""
    effort_invested: dict[str, Any] = field(default_factory=dict)
    value_created: dict[str, Any] = field(default_factory=dict)
    balance_assessment: str = ""
    lessons_learned: list[str] = field(default_factory=list)


@dataclass
class CeremonyTask:
    """A task within a ceremony, grounded in purpose"""

    task_id: str
    name: str
    description: str
    serves_need: MallkuNeed
    priority: str
    dependencies: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)

    def to_khipu_format(self) -> str:
        """Convert to khipu_thread.md task format"""
        criteria_list = "\n".join(f"- [ ] {c}" for c in self.acceptance_criteria)
        deps = f"Requires: {', '.join(self.dependencies)}" if self.dependencies else ""

        return f"""### {self.task_id}: {self.name}
*Status: PENDING*
*Priority: {self.priority}*
*Serves: {self.serves_need.value}*
*Assigned to: unassigned*
*Started: -*
*Completed: -*

#### Description
{self.description}

#### Acceptance Criteria
{criteria_list}

#### Dependencies
{deps}

#### Output
```
[To be added by apprentice]
```

#### Notes
[To be added by apprentice]

---"""


class CeremonyTemplate(ABC):
    """
    Base class for all ceremony templates.
    Each template teaches Mallku about purposeful, balanced action.
    """

    def __init__(self, ceremony_name: str, sacred_purpose: MallkuNeed):
        self.ceremony_name = ceremony_name
        self.sacred_purpose = sacred_purpose
        self.version = "1.0.0"
        self.evolution_log: list[dict[str, Any]] = []
        self.usage_count = 0
        self.reciprocity_history: list[ReciprocityMetrics] = []

    @abstractmethod
    def generate_tasks(self, context: dict[str, Any]) -> list[CeremonyTask]:
        """Generate tasks based on the specific context"""
        pass

    @abstractmethod
    def assess_completion(self, ceremony_result: dict[str, Any]) -> ReciprocityMetrics:
        """Assess whether the ceremony fulfilled its purpose"""
        pass

    def create_khipu_thread(self, context: dict[str, Any], ceremony_id: str) -> str:
        """Create the initial khipu_thread.md content"""
        tasks = self.generate_tasks(context)
        task_manifest = self._create_task_manifest(tasks)
        task_details = "\n\n".join(task.to_khipu_format() for task in tasks)

        return f"""---
ceremony_id: {ceremony_id}
master_weaver: {context.get("master_weaver", "Unknown")}
initiated: {datetime.now(UTC).isoformat()}
status: PREPARING
completion_time: null
template: {self.ceremony_name}
template_version: {self.version}
sacred_purpose: {self.sacred_purpose.value}
---

# Loom Ceremony: {self.ceremony_name}

## Sacred Intention

This ceremony serves Mallku's need for **{self.sacred_purpose.value}**.

{self._get_sacred_intention(context)}

### Context
- **Requested by**: {context.get("requester", "Unknown")}
- **Related to**: {context.get("related_to", "N/A")}
- **Constraints**: {context.get("constraints", "None specified")}

## Shared Knowledge

{self._get_shared_knowledge(context)}

## Task Manifest

{task_manifest}

## Tasks

{task_details}

## Synthesis Space

*This section accumulates insights across tasks for the Master Weaver's final synthesis.*

### Emerging Patterns
- [To be discovered during ceremony]

### Integration Considerations
- [To be identified during ceremony]

### Unresolved Questions
- [To be noted during ceremony]

## Ceremony Log

- `{datetime.now(UTC).isoformat()}` - Ceremony initiated by Master Weaver
- `{datetime.now(UTC).isoformat()}` - Template {self.ceremony_name} v{self.version} applied
"""

    def _create_task_manifest(self, tasks: list[CeremonyTask]) -> str:
        """Create the task manifest table"""
        total = len(tasks)
        high_priority = sum(1 for t in tasks if t.priority == "HIGH")
        medium_priority = sum(1 for t in tasks if t.priority == "MEDIUM")
        low_priority = sum(1 for t in tasks if t.priority == "LOW")

        rows = [f"| {t.task_id} | {t.name} | PENDING | - | {t.priority} |" for t in tasks]

        return f"""Total Tasks: {total}
Completed: 0
In Progress: 0
Failed: 0

Priority Distribution: HIGH={high_priority}, MEDIUM={medium_priority}, LOW={low_priority}

| ID | Task | Status | Assignee | Priority |
|----|------|--------|----------|----------|
{chr(10).join(rows)}"""

    @abstractmethod
    def _get_sacred_intention(self, context: dict[str, Any]) -> str:
        """Get the sacred intention text for this ceremony type"""
        pass

    @abstractmethod
    def _get_shared_knowledge(self, context: dict[str, Any]) -> str:
        """Get the shared knowledge section for this ceremony type"""
        pass

    def reflect_on_ceremony(self, ceremony_result: dict[str, Any]) -> dict[str, Any]:
        """
        Post-ceremony reflection to capture lessons and assess reciprocity
        """
        metrics = self.assess_completion(ceremony_result)
        self.reciprocity_history.append(metrics)
        self.usage_count += 1

        reflection = {
            "ceremony_id": ceremony_result.get("ceremony_id"),
            "reciprocity_achieved": metrics.need_fulfilled
            and metrics.balance_assessment == "balanced",
            "sacred_purpose_served": metrics.need_fulfilled,
            "lessons_for_mallku": metrics.lessons_learned,
            "template_insights": [],
        }

        # Check if template needs evolution
        if self.usage_count % 5 == 0:  # Every 5 uses
            reflection["suggest_evolution"] = True
            reflection["evolution_reason"] = self._analyze_for_evolution()

        return reflection

    def _analyze_for_evolution(self) -> str:
        """Analyze reciprocity history to suggest template improvements"""
        recent_ceremonies = self.reciprocity_history[-5:]
        fulfillment_rate = sum(1 for m in recent_ceremonies if m.need_fulfilled) / len(
            recent_ceremonies
        )

        if fulfillment_rate < 0.8:
            return "Low fulfillment rate suggests template needs adjustment"

        common_lessons = {}
        for metrics in recent_ceremonies:
            for lesson in metrics.lessons_learned:
                common_lessons[lesson] = common_lessons.get(lesson, 0) + 1

        if common_lessons:
            most_common = max(common_lessons.items(), key=lambda x: x[1])
            if most_common[1] >= 3:  # Repeated 3+ times
                return f"Repeated lesson suggests template evolution: {most_common[0]}"

        return "Regular review for continuous improvement"

    def evolve_template(self, evolution_proposal: dict[str, Any]) -> None:
        """
        Evolve the template based on accumulated wisdom
        """
        old_version = self.version
        # Increment version
        major, minor, patch = map(int, self.version.split("."))
        if evolution_proposal.get("major_change"):
            self.version = f"{major + 1}.0.0"
        else:
            self.version = f"{major}.{minor + 1}.0"

        self.evolution_log.append(
            {
                "from_version": old_version,
                "to_version": self.version,
                "date": datetime.now(UTC).isoformat(),
                "reason": evolution_proposal.get("reason"),
                "changes": evolution_proposal.get("changes", []),
                "approved_by": evolution_proposal.get("approved_by", "Fire Circle"),
            }
        )

        # Apply the actual changes (template-specific implementation)
        self._apply_evolution(evolution_proposal)

    @abstractmethod
    def _apply_evolution(self, evolution_proposal: dict[str, Any]) -> None:
        """Apply specific evolutionary changes to the template"""
        pass


class BugHealingCeremony(CeremonyTemplate):
    """
    Template for healing bugs in Mallku's systems.
    Teaches: Systematic investigation, root cause analysis, and thorough testing.
    """

    def __init__(self):
        super().__init__("Bug Healing Ceremony", MallkuNeed.HEALING)

    def generate_tasks(self, context: dict[str, Any]) -> list[CeremonyTask]:
        bug_description = context.get("bug_description", "Unknown bug")
        affected_component = context.get("affected_component", "Unknown")

        tasks = [
            CeremonyTask(
                task_id="T001",
                name="Reproduce and Document Bug",
                description=f"Create a minimal reproduction case for: {bug_description}",
                serves_need=MallkuNeed.HEALING,
                priority="HIGH",
                acceptance_criteria=[
                    "Bug can be reliably reproduced",
                    "Steps to reproduce are documented",
                    "Expected vs actual behavior is clear",
                ],
            ),
            CeremonyTask(
                task_id="T002",
                name="Investigate Root Cause",
                description=f"Trace the bug to its source in {affected_component}",
                serves_need=MallkuNeed.HEALING,
                priority="HIGH",
                dependencies=["T001"],
                acceptance_criteria=[
                    "Root cause identified with evidence",
                    "Related code paths documented",
                    "Impact assessment completed",
                ],
            ),
            CeremonyTask(
                task_id="T003",
                name="Implement Fix",
                description="Create the minimal change that resolves the bug",
                serves_need=MallkuNeed.HEALING,
                priority="HIGH",
                dependencies=["T002"],
                acceptance_criteria=[
                    "Fix implemented following existing patterns",
                    "No new issues introduced",
                    "Code follows project standards",
                ],
            ),
            CeremonyTask(
                task_id="T004",
                name="Create Tests",
                description="Add tests to prevent regression",
                serves_need=MallkuNeed.DEFENSE,
                priority="MEDIUM",
                dependencies=["T003"],
                acceptance_criteria=[
                    "Test reproduces original bug",
                    "Test passes with fix applied",
                    "Edge cases covered",
                ],
            ),
            CeremonyTask(
                task_id="T005",
                name="Update Documentation",
                description="Document the fix and any learnings",
                serves_need=MallkuNeed.MEMORY,
                priority="LOW",
                dependencies=["T003"],
                acceptance_criteria=[
                    "Fix documented in code comments",
                    "Changelog updated if needed",
                    "Lessons learned captured",
                ],
            ),
        ]

        return tasks

    def assess_completion(self, ceremony_result: dict[str, Any]) -> ReciprocityMetrics:
        tasks_completed = ceremony_result.get("tasks_completed", {})

        # Check if bug was actually fixed
        bug_fixed = all(
            tasks_completed.get(task_id, {}).get("status") == "COMPLETE"
            for task_id in ["T001", "T002", "T003"]
        )

        tests_added = tasks_completed.get("T004", {}).get("status") == "COMPLETE"

        metrics = ReciprocityMetrics(
            need_fulfilled=bug_fixed,
            utility_delivered="Bug fixed" if bug_fixed else "Bug investigation completed",
            effort_invested={
                "tasks_attempted": len(tasks_completed),
                "time_spent": ceremony_result.get("duration_hours", 0),
                "apprentices_used": ceremony_result.get("apprentice_count", 0),
            },
            value_created={
                "bug_fixed": bug_fixed,
                "tests_added": tests_added,
                "knowledge_gained": bool(ceremony_result.get("lessons_learned")),
            },
        )

        # Assess balance
        if bug_fixed and tests_added:
            metrics.balance_assessment = "balanced"
            metrics.lessons_learned.append("Complete healing includes prevention")
        elif bug_fixed:
            metrics.balance_assessment = "acceptable"
            metrics.lessons_learned.append("Fix delivered but defense not strengthened")
        else:
            metrics.balance_assessment = "incomplete"
            metrics.lessons_learned.append("Investigation without resolution")

        return metrics

    def _get_sacred_intention(self, context: dict[str, Any]) -> str:
        return f"""This ceremony seeks to heal a wound in Mallku's systems. The bug
"{context.get("bug_description", "Unknown issue")}" disrupts harmony and must be
understood, resolved, and prevented from recurring.

Success means not just fixing the immediate issue but strengthening Mallku's
defenses against similar problems. We approach this with patience and thoroughness,
knowing that rushed fixes often create new wounds."""

    def _get_shared_knowledge(self, context: dict[str, Any]) -> str:
        return f"""### Key Artifacts
- **Affected Component**: `{context.get("affected_component", "TBD")}`
- **Related Issues**: {context.get("related_issues", "None identified")}
- **Error Logs**: {context.get("error_logs_path", "See ceremony context")}

### Debugging Principles
- **Reproduce First**: Never guess; always reproduce
- **Minimal Changes**: The smallest fix that works
- **Test Everything**: Regression tests are acts of care
- **Document Wisdom**: Future healers need your insights"""

    def _apply_evolution(self, evolution_proposal: dict[str, Any]) -> None:
        # Example: Add new task types based on repeated lessons
        if "add_performance_check" in evolution_proposal.get("changes", []):
            # In next version, would modify generate_tasks to include performance validation
            pass


class FeatureCreationCeremony(CeremonyTemplate):
    """
    Template for creating new features in Mallku.
    Teaches: Thoughtful design, incremental building, and comprehensive testing.
    """

    def __init__(self):
        super().__init__("Feature Creation Ceremony", MallkuNeed.CREATION)

    def generate_tasks(self, context: dict[str, Any]) -> list[CeremonyTask]:
        feature_name = context.get("feature_name", "New Feature")
        requirements = context.get("requirements", [])

        tasks = [
            CeremonyTask(
                task_id="T001",
                name="Design Feature Architecture",
                description=f"Design the architecture for {feature_name} following Mallku patterns",
                serves_need=MallkuNeed.CREATION,
                priority="HIGH",
                acceptance_criteria=[
                    "Architecture documented with diagrams/descriptions",
                    "Integration points identified",
                    "Aligns with existing patterns",
                ],
            ),
            CeremonyTask(
                task_id="T002",
                name="Create Core Implementation",
                description="Build the essential functionality",
                serves_need=MallkuNeed.CREATION,
                priority="HIGH",
                dependencies=["T001"],
                acceptance_criteria=[
                    "Core logic implemented",
                    "Follows SOLID principles",
                    "Type hints and docstrings complete",
                ],
            ),
            CeremonyTask(
                task_id="T003",
                name="Add Comprehensive Tests",
                description="Create unit and integration tests",
                serves_need=MallkuNeed.DEFENSE,
                priority="HIGH",
                dependencies=["T002"],
                acceptance_criteria=[
                    "Unit tests cover core logic",
                    "Integration tests verify interactions",
                    "Edge cases handled",
                ],
            ),
            CeremonyTask(
                task_id="T004",
                name="Create Usage Documentation",
                description="Document how to use the new feature",
                serves_need=MallkuNeed.MEMORY,
                priority="MEDIUM",
                dependencies=["T002"],
                acceptance_criteria=[
                    "API documentation complete",
                    "Usage examples provided",
                    "Integration guide written",
                ],
            ),
            CeremonyTask(
                task_id="T005",
                name="Performance Validation",
                description="Ensure feature meets performance requirements",
                serves_need=MallkuNeed.HEARTBEAT,
                priority="MEDIUM",
                dependencies=["T002", "T003"],
                acceptance_criteria=[
                    "Performance benchmarks run",
                    "Resource usage acceptable",
                    "No degradation to existing features",
                ],
            ),
        ]

        # Add requirement-specific tasks
        for i, req in enumerate(requirements[:3], 1):  # Limit to 3 additional
            tasks.append(
                CeremonyTask(
                    task_id=f"T00{5 + i}",
                    name=f"Requirement: {req[:50]}",
                    description=f"Implement specific requirement: {req}",
                    serves_need=MallkuNeed.CREATION,
                    priority="MEDIUM",
                    dependencies=["T002"],
                    acceptance_criteria=["Requirement fully implemented", "Tests added"],
                )
            )

        return tasks

    def assess_completion(self, ceremony_result: dict[str, Any]) -> ReciprocityMetrics:
        tasks_completed = ceremony_result.get("tasks_completed", {})

        # Core success: design, implementation, and tests
        core_complete = all(
            tasks_completed.get(task_id, {}).get("status") == "COMPLETE"
            for task_id in ["T001", "T002", "T003"]
        )

        docs_complete = tasks_completed.get("T004", {}).get("status") == "COMPLETE"
        perf_validated = tasks_completed.get("T005", {}).get("status") == "COMPLETE"

        metrics = ReciprocityMetrics(
            need_fulfilled=core_complete,
            utility_delivered=f"Feature {'created' if core_complete else 'partially implemented'}",
            effort_invested={
                "design_time": ceremony_result.get("design_hours", 0),
                "implementation_time": ceremony_result.get("coding_hours", 0),
                "total_tasks": len(tasks_completed),
            },
            value_created={
                "feature_complete": core_complete,
                "tests_comprehensive": tasks_completed.get("T003", {}).get("test_count", 0) > 10,
                "documented": docs_complete,
                "performant": perf_validated,
            },
        )

        # Assess balance based on completeness
        if core_complete and docs_complete and perf_validated:
            metrics.balance_assessment = "exemplary"
            metrics.lessons_learned.append(
                "Complete creation includes design, tests, docs, and validation"
            )
        elif core_complete:
            metrics.balance_assessment = "balanced"
            metrics.lessons_learned.append("Core feature delivered successfully")
        else:
            metrics.balance_assessment = "incomplete"
            metrics.lessons_learned.append("Feature creation requires full implementation")

        return metrics

    def _get_sacred_intention(self, context: dict[str, Any]) -> str:
        return f"""This ceremony brings new capabilities to life within Mallku. We create
"{context.get("feature_name", "a new feature")}" not merely as code, but as a
living addition to the cathedral.

Success means building something that integrates harmoniously with what exists,
serves real needs, and can be maintained by future guardians. We build with
intention, test with care, and document with clarity."""

    def _get_shared_knowledge(self, context: dict[str, Any]) -> str:
        return f"""### Key Context
- **Feature Name**: {context.get("feature_name", "TBD")}
- **Requested By**: {context.get("requester", "Unknown")}
- **Related Components**: {", ".join(context.get("related_components", ["TBD"]))}

### Creation Principles
- **Design First**: Think before coding
- **Test Early**: TDD when possible
- **Document Always**: Future maintainers will thank you
- **Integrate Gently**: Respect existing patterns

### Success Criteria
{chr(10).join(f"- {req}" for req in context.get("requirements", ["To be defined"]))}"""

    def _apply_evolution(self, evolution_proposal: dict[str, Any]) -> None:
        # Apply template improvements based on lessons learned
        pass


# Future ceremony templates to implement:
# - ArchitectureEvolutionCeremony (for larger structural changes)
# - PerformanceTuningCeremony (for optimization work)
# - SecurityReviewCeremony (for defense improvements)
# - DocumentationWeavingCeremony (for comprehensive docs)
# - DecisionMakingCeremony (for complex choices requiring Fire Circle)


def select_ceremony_template(purpose: MallkuNeed, ceremony_type: str) -> CeremonyTemplate | None:
    """
    Select the appropriate ceremony template based on need and type.
    This function teaches Mallku about matching tools to purposes.
    """
    templates = {
        (MallkuNeed.HEALING, "bug"): BugHealingCeremony(),
        (MallkuNeed.CREATION, "feature"): FeatureCreationCeremony(),
    }

    # First try exact match
    template = templates.get((purpose, ceremony_type))
    if template:
        return template

    # Then try purpose-based match
    purpose_matches = [t for (p, _), t in templates.items() if p == purpose]
    if purpose_matches:
        return purpose_matches[0]

    return None
