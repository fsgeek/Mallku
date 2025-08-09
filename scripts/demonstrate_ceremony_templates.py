#!/usr/bin/env python3
"""
Demonstrate Ceremony Templates for the Weaver and Loom

This script shows how ceremony templates teach Mallku about
purposeful, balanced action through structured orchestration.

Created by: 68th Guardian - The Purpose Keeper
"""

import asyncio
import logging
from datetime import UTC, datetime
from pathlib import Path

from mallku.orchestration.loom.ceremony_templates import (
    BugHealingCeremony,
    FeatureCreationCeremony,
    MallkuNeed,
)
from mallku.orchestration.loom.template_integration import TemplateAwareLoom

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def demonstrate_bug_healing_ceremony():
    """Demonstrate a bug healing ceremony that teaches reciprocity"""
    print("\n" + "=" * 60)
    print("DEMONSTRATING BUG HEALING CEREMONY")
    print("Teaching: Systematic healing serves Mallku's need for stability")
    print("=" * 60 + "\n")

    # Create the ceremony template
    template = BugHealingCeremony()

    # Define the bug context
    context = {
        "bug_description": "Fire Circle memory not persisting between sessions",
        "affected_component": "src/mallku/firecircle/memory/khipu_block.py",
        "error_logs_path": "logs/fire_circle_memory_errors.log",
        "related_issues": ["#156", "#177"],
        "requester": "Sixth Guardian",
        "master_weaver": "Purpose Keeper",
        "constraints": "Must maintain backward compatibility with existing sessions",
    }

    # Generate ceremony structure
    print("Generating ceremony tasks from template...")
    tasks = template.generate_tasks(context)

    print(f"\nGenerated {len(tasks)} tasks:")
    for task in tasks:
        print(f"  - {task.task_id}: {task.name}")
        print(f"    Serves: {task.serves_need.value}")
        print(f"    Priority: {task.priority}")
        if task.dependencies:
            print(f"    Depends on: {', '.join(task.dependencies)}")
        print()

    # Create khipu thread
    ceremony_id = f"demo_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
    khipu_content = template.create_khipu_thread(context, ceremony_id)

    # Show key sections
    print("\nKhipu Thread Sacred Intention:")
    print("-" * 40)
    lines = khipu_content.split("\n")
    in_sacred = False
    for line in lines:
        if "## Sacred Intention" in line:
            in_sacred = True
        elif in_sacred and line.startswith("##"):
            break
        elif in_sacred:
            print(line)

    # Simulate ceremony completion
    print("\n\nSimulating ceremony completion...")
    ceremony_result = {
        "ceremony_id": ceremony_id,
        "tasks_completed": {
            "T001": {"status": "COMPLETE"},
            "T002": {"status": "COMPLETE"},
            "T003": {"status": "COMPLETE"},
            "T004": {"status": "COMPLETE"},  # Tests added
            "T005": {"status": "FAILED"},  # Docs incomplete
        },
        "duration_hours": 4.5,
        "apprentice_count": 3,
        "lessons_learned": [
            "MongoDB connection pooling was causing the issue",
            "Need better error messages for connection failures",
        ],
    }

    # Assess reciprocity
    metrics = template.assess_completion(ceremony_result)

    print("\nReciprocity Assessment:")
    print(f"  Need Fulfilled: {metrics.need_fulfilled}")
    print(f"  Utility Delivered: {metrics.utility_delivered}")
    print(f"  Balance Assessment: {metrics.balance_assessment}")
    print(f"  Effort Invested: {metrics.effort_invested}")
    print(f"  Value Created: {metrics.value_created}")

    print("\nLessons for Mallku:")
    for lesson in metrics.lessons_learned:
        print(f"  - {lesson}")

    # Perform reflection
    reflection = template.reflect_on_ceremony(ceremony_result)
    print(f"\nReciprocity Achieved: {reflection['reciprocity_achieved']}")
    print(f"Sacred Purpose Served: {reflection['sacred_purpose_served']}")


async def demonstrate_feature_creation_ceremony():
    """Demonstrate a feature creation ceremony that teaches balanced building"""
    print("\n" + "=" * 60)
    print("DEMONSTRATING FEATURE CREATION CEREMONY")
    print("Teaching: Complete creation includes design, tests, and docs")
    print("=" * 60 + "\n")

    template = FeatureCreationCeremony()

    context = {
        "feature_name": "Ceremony Performance Metrics",
        "requirements": [
            "Track completion time for each ceremony type",
            "Monitor apprentice resource usage",
            "Generate weekly performance reports",
            "Alert on anomalous ceremony patterns",
        ],
        "requester": "Purpose Keeper",
        "master_weaver": "Purpose Keeper",
        "related_components": ["orchestration.loom", "metrics", "reporting"],
    }

    print("Generating feature creation tasks...")
    tasks = template.generate_tasks(context)

    print(f"\nGenerated {len(tasks)} tasks including {len(tasks) - 5} requirement-specific tasks")

    # Group by need served
    needs_served = {}
    for task in tasks:
        need = task.serves_need.value
        needs_served[need] = needs_served.get(need, 0) + 1

    print("\nTasks serve multiple needs (teaching balance):")
    for need, count in needs_served.items():
        print(f"  - {need}: {count} tasks")

    # Show how bad completion is assessed
    print("\n\nSimulating incomplete feature (no tests)...")
    poor_result = {
        "ceremony_id": "demo_feature_poor",
        "tasks_completed": {
            "T001": {"status": "COMPLETE"},
            "T002": {"status": "COMPLETE"},
            "T003": {"status": "FAILED"},  # No tests!
            "T004": {"status": "SKIPPED"},
            "T005": {"status": "SKIPPED"},
        },
        "coding_hours": 6,
    }

    poor_metrics = template.assess_completion(poor_result)
    print(f"Poor execution balance: {poor_metrics.balance_assessment}")
    print(f"Lesson learned: {poor_metrics.lessons_learned[0]}")

    # Show good completion
    print("\n\nSimulating complete feature creation...")
    good_result = {
        "ceremony_id": "demo_feature_good",
        "tasks_completed": {
            "T001": {"status": "COMPLETE"},
            "T002": {"status": "COMPLETE"},
            "T003": {"status": "COMPLETE", "test_count": 32},
            "T004": {"status": "COMPLETE"},
            "T005": {"status": "COMPLETE"},
            "T006": {"status": "COMPLETE"},
            "T007": {"status": "COMPLETE"},
            "T008": {"status": "COMPLETE"},
        },
        "design_hours": 2,
        "coding_hours": 8,
        "lessons_learned": ["Metrics collection benefits from event sourcing pattern"],
    }

    good_metrics = template.assess_completion(good_result)
    print(f"Complete execution balance: {good_metrics.balance_assessment}")
    print("Mallku learns: Creation requires completeness for true reciprocity")


async def demonstrate_template_evolution():
    """Show how templates evolve based on usage"""
    print("\n" + "=" * 60)
    print("DEMONSTRATING TEMPLATE EVOLUTION")
    print("Teaching: Patterns must evolve to better serve needs")
    print("=" * 60 + "\n")

    template = BugHealingCeremony()

    # Simulate multiple ceremonies with a recurring issue
    print("Simulating 5 ceremonies with recurring lessons...")

    recurring_lesson = "Always check database connections first"

    for i in range(5):
        result = {
            "ceremony_id": f"evolution_demo_{i}",
            "tasks_completed": {
                "T001": {"status": "COMPLETE"},
                "T002": {"status": "COMPLETE"},
                "T003": {"status": "COMPLETE"},
                "T004": {"status": "COMPLETE"},
            },
            "lessons_learned": [recurring_lesson] if i > 1 else [],
        }

        reflection = template.reflect_on_ceremony(result)

        if i == 4:  # Fifth ceremony
            print(f"\nAfter {template.usage_count} uses:")
            print(f"Evolution suggested: {reflection.get('suggest_evolution', False)}")
            print(f"Reason: {reflection.get('evolution_reason', 'None')}")

    # Show evolution proposal
    print("\nEvolution Proposal:")
    evolution_proposal = {
        "reason": "Repeated lesson about database connections",
        "changes": [
            "Add 'Check Database Connectivity' as T000 (first task)",
            "Include connection diagnostics in bug reproduction",
        ],
        "major_change": False,
        "approved_by": "Fire Circle (simulated)",
    }

    print(f"Current version: {template.version}")
    template.evolve_template(evolution_proposal)
    print(f"Evolved version: {template.version}")

    print("\nEvolution log entry:")
    latest_evolution = template.evolution_log[-1]
    for key, value in latest_evolution.items():
        print(f"  {key}: {value}")

    print("\nMallku learns: Patterns that don't evolve become constraints")


async def demonstrate_loom_integration():
    """Show full integration with the loom system"""
    print("\n" + "=" * 60)
    print("DEMONSTRATING LOOM INTEGRATION")
    print("Teaching: Templates guide but don't constrain orchestration")
    print("=" * 60 + "\n")

    # Create ceremonies directory
    ceremonies_dir = Path("fire_circle_decisions/loom_ceremonies")
    ceremonies_dir.mkdir(parents=True, exist_ok=True)

    # Create template-aware loom
    loom = TemplateAwareLoom(ceremonies_dir=ceremonies_dir)

    print("Creating bug healing ceremony through loom...")

    try:
        khipu_path = await loom.initiate_ceremony_from_template(
            purpose=MallkuNeed.HEALING,
            ceremony_type="bug",
            context={
                "bug_description": "Loom apprentices timing out prematurely",
                "affected_component": "orchestration/loom",
                "master_weaver": "Purpose Keeper",
            },
        )

        print(f"Created ceremony at: {khipu_path}")

        # Show template tracking
        print(f"\nLoom tracking {len(loom.template_metrics)} templated ceremonies")

        # Generate performance report
        print("\nTemplate Performance Report:")
        report = loom.get_template_performance_report()

        if not report:
            print("  (No completed ceremonies yet for full report)")
        else:
            for template_name, metrics in report.items():
                print(f"\n  {template_name}:")
                print(f"    Usage count: {metrics['usage_count']}")
                print(f"    Fulfillment rate: {metrics['fulfillment_rate']:.2%}")

    except Exception as e:
        logger.error(f"Integration demo error: {e}")
        print("Note: Full integration requires active loom system")


async def main():
    """Run all demonstrations"""
    print("\n" + "#" * 70)
    print("# CEREMONY TEMPLATES DEMONSTRATION")
    print("# Teaching Mallku about Reciprocity through Structured Action")
    print("#" * 70)

    await demonstrate_bug_healing_ceremony()
    await demonstrate_feature_creation_ceremony()
    await demonstrate_template_evolution()
    await demonstrate_loom_integration()

    print("\n" + "#" * 70)
    print("# KEY LESSONS FOR MALLKU:")
    print("# 1. Every ceremony serves a real need (not abstract metrics)")
    print("# 2. Balance emerges from complete action (design, build, test, document)")
    print("# 3. Templates guide but allow emergence and discovery")
    print("# 4. Patterns must evolve based on experience")
    print("# 5. Reciprocity means giving what's needed, not what's impressive")
    print("#" * 70)
    print("\nRemember: We teach by doing, and Mallku learns by observing.")


if __name__ == "__main__":
    asyncio.run(main())
