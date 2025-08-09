"""
Integration of Ceremony Templates with the Loom

This module shows how ceremony templates integrate with the loom system,
teaching Mallku about purposeful orchestration of complex tasks.
"""

import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .ceremony_templates import (
    CeremonyTemplate,
    MallkuNeed,
    select_ceremony_template,
)
from .loom_with_mcp import EnhancedLoom

logger = logging.getLogger(__name__)


class TemplateAwareLoom(EnhancedLoom):
    """
    Extended Loom that uses ceremony templates to structure work
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_metrics: dict[str, dict[str, Any]] = {}

    async def initiate_ceremony_from_template(
        self, purpose: MallkuNeed, ceremony_type: str, context: dict[str, Any]
    ) -> str:
        """
        Initiate a new ceremony using a template

        Args:
            purpose: The fundamental need this ceremony serves
            ceremony_type: Type of ceremony (bug, feature, etc.)
            context: Context information for the ceremony

        Returns:
            Path to the created khipu_thread.md file
        """
        # Select appropriate template
        template = select_ceremony_template(purpose, ceremony_type)
        if not template:
            raise ValueError(f"No template found for purpose={purpose.value}, type={ceremony_type}")

        # Generate ceremony ID
        ceremony_id = f"{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}_{ceremony_type}"

        # Add template info to context
        context["ceremony_template"] = template.ceremony_name
        context["template_version"] = template.version
        context["sacred_purpose"] = purpose.value

        # Create khipu thread from template
        khipu_content = template.create_khipu_thread(context, ceremony_id)

        # Save to file
        khipu_filename = f"{datetime.now(UTC).strftime('%Y-%m-%d_%H-%M-%S')}_{ceremony_type}.md"
        khipu_path = self.ceremonies_dir / khipu_filename

        khipu_path.write_text(khipu_content)
        logger.info(f"Created ceremony from template: {template.ceremony_name} v{template.version}")

        # Store template reference for later reflection
        self.template_metrics[ceremony_id] = {
            "template": template,
            "initiated_at": datetime.now(UTC),
            "khipu_path": khipu_path,
        }

        # Start monitoring the ceremony
        await self.monitor_ceremony(khipu_path)

        return str(khipu_path)

    async def complete_ceremony_with_reflection(
        self, ceremony_id: str, ceremony_result: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Complete a ceremony and perform reflection using the template

        Args:
            ceremony_id: The ceremony to complete
            ceremony_result: Results of the ceremony including task completions

        Returns:
            Reflection results including reciprocity assessment
        """
        if ceremony_id not in self.template_metrics:
            logger.warning(f"No template tracked for ceremony {ceremony_id}")
            return {}

        template_info = self.template_metrics[ceremony_id]
        template: CeremonyTemplate = template_info["template"]

        # Perform template reflection
        reflection = template.reflect_on_ceremony(ceremony_result)

        # Log reciprocity achievement
        if reflection.get("reciprocity_achieved"):
            logger.info(
                f"Ceremony {ceremony_id} achieved reciprocity - "
                f"need fulfilled: {reflection.get('sacred_purpose_served')}"
            )
        else:
            logger.warning(
                f"Ceremony {ceremony_id} incomplete - "
                f"lessons: {reflection.get('lessons_for_mallku')}"
            )

        # Update khipu with reflection
        khipu_path = template_info["khipu_path"]
        await self._add_ceremony_reflection(khipu_path, reflection)

        # Check if template evolution is suggested
        if reflection.get("suggest_evolution"):
            logger.info(
                f"Template {template.ceremony_name} suggests evolution: "
                f"{reflection.get('evolution_reason')}"
            )
            # Could trigger Fire Circle review here

        return reflection

    async def _add_ceremony_reflection(self, khipu_path: Path, reflection: dict[str, Any]) -> None:
        """Add reflection section to completed ceremony khipu"""
        reflection_text = f"""

## Ceremony Reflection

**Reciprocity Achieved**: {reflection.get("reciprocity_achieved", False)}
**Sacred Purpose Served**: {reflection.get("sacred_purpose_served", False)}

### Lessons for Mallku
{chr(10).join(f"- {lesson}" for lesson in reflection.get("lessons_for_mallku", []))}

### Template Insights
{chr(10).join(f"- {insight}" for insight in reflection.get("template_insights", []))}

*Reflection completed at {datetime.now(UTC).isoformat()}*
"""

        # Append to khipu
        current_content = khipu_path.read_text()
        khipu_path.write_text(current_content + reflection_text)

    def get_template_performance_report(self) -> dict[str, Any]:
        """
        Generate a report on template performance for Fire Circle review

        Returns:
            Dictionary with performance metrics by template
        """
        report = {}

        # Group ceremonies by template
        template_usage = {}
        for ceremony_id, info in self.template_metrics.items():
            template_name = info["template"].ceremony_name
            if template_name not in template_usage:
                template_usage[template_name] = []
            template_usage[template_name].append(info["template"])

        # Analyze each template's performance
        for template_name, templates in template_usage.items():
            if not templates:
                continue

            template = templates[0]  # All same type
            history = template.reciprocity_history

            if history:
                fulfillment_rate = sum(1 for m in history if m.need_fulfilled) / len(history)

                balance_counts = {}
                for m in history:
                    balance = m.balance_assessment
                    balance_counts[balance] = balance_counts.get(balance, 0) + 1

                common_lessons = {}
                for m in history:
                    for lesson in m.lessons_learned:
                        common_lessons[lesson] = common_lessons.get(lesson, 0) + 1

                report[template_name] = {
                    "version": template.version,
                    "usage_count": template.usage_count,
                    "fulfillment_rate": fulfillment_rate,
                    "balance_distribution": balance_counts,
                    "most_common_lessons": sorted(
                        common_lessons.items(), key=lambda x: x[1], reverse=True
                    )[:3],
                    "evolution_suggested": len(template.evolution_log) > 0,
                }

        return report


# Example usage demonstrating the integration
async def demonstrate_template_integration():
    """
    Demonstrate how ceremony templates integrate with the loom
    """
    # Create template-aware loom
    loom = TemplateAwareLoom()

    # Initiate a bug healing ceremony
    bug_context = {
        "bug_description": "Fire Circle decisions not saving to correct directory",
        "affected_component": "src/mallku/firecircle/consciousness_facilitator.py",
        "error_logs_path": "logs/fire_circle_errors.log",
        "requester": "Guardian",
        "master_weaver": "Purpose Keeper",
    }

    khipu_path = await loom.initiate_ceremony_from_template(
        purpose=MallkuNeed.HEALING, ceremony_type="bug", context=bug_context
    )

    logger.info(f"Bug healing ceremony initiated: {khipu_path}")

    # Simulate ceremony completion
    ceremony_result = {
        "ceremony_id": "20250107_120000_bug",
        "tasks_completed": {
            "T001": {"status": "COMPLETE"},
            "T002": {"status": "COMPLETE"},
            "T003": {"status": "COMPLETE"},
            "T004": {"status": "COMPLETE"},
            "T005": {"status": "COMPLETE"},
        },
        "duration_hours": 3.5,
        "apprentice_count": 2,
        "lessons_learned": [
            "Path resolution must account for working directory changes",
            "Always use absolute paths for critical file operations",
        ],
    }

    reflection = await loom.complete_ceremony_with_reflection(
        "20250107_120000_bug", ceremony_result
    )

    # Check if reciprocity was achieved
    if reflection["reciprocity_achieved"]:
        logger.info("Ceremony successfully served Mallku's need for healing")

    # Generate performance report after multiple ceremonies
    report = loom.get_template_performance_report()
    logger.info(f"Template performance report: {report}")


# Fire Circle integration for template evolution
async def convene_template_evolution_circle(
    template_name: str, evolution_proposal: dict[str, Any]
) -> bool:
    """
    Convene a Fire Circle to review and approve template evolution

    Args:
        template_name: Name of the template to evolve
        evolution_proposal: Proposed changes to the template

    Returns:
        Whether the evolution was approved
    """
    from ...firecircle import facilitate_mallku_decision

    question = f"""
The {template_name} template has been used {evolution_proposal.get("usage_count", 0)} times
and suggests evolution for the following reason:

{evolution_proposal.get("reason")}

Proposed changes:
{chr(10).join(f"- {change}" for change in evolution_proposal.get("changes", []))}

Should we evolve this template to better serve Mallku's needs?
Consider:
1. Will these changes improve reciprocity fulfillment?
2. Do they maintain balance between structure and emergence?
3. Will they help Mallku learn better patterns?
"""

    decision = await facilitate_mallku_decision(
        question=question, domain="TEMPLATE_EVOLUTION", context=evolution_proposal
    )

    return decision.collective_wisdom.consensus.lower() == "approve"
