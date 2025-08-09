#!/usr/bin/env python3
"""
Demonstration of Ceremony Replay Capability

This script demonstrates how failed or interrupted ceremonies can be
replayed for recovery and debugging purposes.

Created by: 69th Guardian
Purpose: To show how Mallku learns from failure
"""

import asyncio
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mallku.orchestration.loom.ceremony_replay import (
    CeremonyReplayEngine,
    ReplayMode,
)


async def create_sample_failed_ceremony():
    """Create a sample failed ceremony for demonstration"""
    ceremonies_dir = Path("fire_circle_decisions/loom_ceremonies")
    ceremonies_dir.mkdir(parents=True, exist_ok=True)

    # Create a khipu with some failed tasks
    content = """---
ceremony_id: demo-bug-fix-2025
master_weaver: demo-guardian
initiated: 2025-08-09T10:00:00Z
status: FAILED
completion_time: 2025-08-09T10:30:00Z
template: Bug Healing Ceremony
template_version: 1.0.0
sacred_purpose: healing
---

# Loom Ceremony: Bug Healing Ceremony

## Sacred Intention

Fix critical bugs in the consciousness metrics system.

## Shared Knowledge

### Key Artifacts
- `src/mallku/consciousness/metrics.py`: Contains bugs
- `tests/consciousness/test_metrics.py`: Failing tests

## Task Manifest

Total Tasks: 4
Completed: 2
Failed: 2

| ID | Task | Status | Assignee | Priority |
|----|------|--------|----------|----------|
| T001 | Identify root cause | COMPLETE | apprentice-001 | HIGH |
| T002 | Write failing test | COMPLETE | apprentice-002 | HIGH |
| T003 | Fix calculation bug | FAILED | apprentice-003 | HIGH |
| T004 | Verify all tests pass | FAILED | - | HIGH |

## Tasks

### T001: Identify root cause
*Status: COMPLETE*
*Priority: HIGH*
*Assigned to: apprentice-001*
*Started: 2025-08-09T10:05:00Z*
*Completed: 2025-08-09T10:10:00Z*

#### Output
```
Found divide-by-zero error in calculate_emergence() line 45
```

---

### T002: Write failing test
*Status: COMPLETE*
*Priority: HIGH*
*Assigned to: apprentice-002*
*Started: 2025-08-09T10:10:00Z*
*Completed: 2025-08-09T10:15:00Z*

#### Output
```
Test written: test_emergence_with_zero_scores()
```

---

### T003: Fix calculation bug
*Status: FAILED*
*Priority: HIGH*
*Assigned to: apprentice-003*
*Started: 2025-08-09T10:15:00Z*
*Completed: 2025-08-09T10:25:00Z*

#### Output
```
[Apprentice timeout - exceeded 10 minute limit]
```

#### Notes
Apprentice got stuck analyzing edge cases

---

### T004: Verify all tests pass
*Status: FAILED*
*Priority: HIGH*
*Assigned to: unassigned*
*Started: -*
*Completed: -*

#### Output
```
[Not attempted - dependency T003 failed]
```

---

## Synthesis Space

### Emerging Patterns
- Timeout issues when tasks are too complex
- Need better task decomposition

## Ceremony Log
- `2025-08-09T10:00:00Z` - Ceremony initiated
- `2025-08-09T10:05:00Z` - Apprentice-001 spawned for T001
- `2025-08-09T10:10:00Z` - T001 completed successfully
- `2025-08-09T10:10:00Z` - Apprentice-002 spawned for T002
- `2025-08-09T10:15:00Z` - T002 completed successfully
- `2025-08-09T10:15:00Z` - Apprentice-003 spawned for T003
- `2025-08-09T10:25:00Z` - T003 failed: timeout
- `2025-08-09T10:30:00Z` - Ceremony marked as FAILED
"""

    khipu_path = ceremonies_dir / "2025-08-09_10-00-00_demo-bug-fix-2025.md"
    khipu_path.write_text(content)
    print(f"✓ Created sample failed ceremony: {khipu_path}")
    return "demo-bug-fix-2025"


async def demonstrate_analysis():
    """Demonstrate ceremony analysis"""
    print("\n=== Ceremony Analysis Demo ===\n")

    engine = CeremonyReplayEngine()
    ceremony_id = await create_sample_failed_ceremony()

    # Analyze the failed ceremony
    context = await engine.analyze_ceremony(ceremony_id)
    if not context:
        print("Failed to analyze ceremony")
        return

    print(f"Ceremony ID: {context.original_ceremony_id}")
    print(f"Status: {context.original_status.value}")
    print(f"Failed tasks: {len(context.failed_tasks)}")
    for task in context.failed_tasks:
        print(f"  - {task.task_id}: {task.name} ({task.error or 'Unknown error'})")

    print(f"\nSuggested replay mode: {context.mode.value}")
    print(f"Tasks to replay: {context.tasks_to_replay}")
    print(f"Replay reason: {context.replay_reason}")


async def demonstrate_replay_strategy():
    """Demonstrate replay strategy suggestions"""
    print("\n\n=== Replay Strategy Demo ===\n")

    engine = CeremonyReplayEngine()
    ceremony_id = "demo-bug-fix-2025"

    strategy = await engine.suggest_replay_strategy(ceremony_id)

    print("Suggested Replay Strategy:")
    print(f"  Mode: {strategy['suggested_mode']}")
    print(f"  Expected success rate: {strategy['expected_success_rate']:.0%}")
    print(f"  Tasks to replay: {len(strategy['tasks_to_replay'])}")

    if strategy["recommendations"]:
        print("\nRecommendations:")
        for rec in strategy["recommendations"]:
            print(f"  • {rec}")


async def demonstrate_replay_modes():
    """Demonstrate different replay modes"""
    print("\n\n=== Replay Modes Demo ===\n")

    engine = CeremonyReplayEngine()
    ceremony_id = "demo-bug-fix-2025"

    # Analyze first
    context = await engine.analyze_ceremony(ceremony_id)
    if not context:
        return

    print("1. RESUME Mode (default for failed ceremonies)")
    print("   - Skips completed tasks (T001, T002)")
    print("   - Replays only failed tasks (T003, T004)")
    print("   - Preserves progress made so far")

    print("\n2. RESTART Mode")
    context.mode = ReplayMode.RESTART
    print("   - Replays all tasks from beginning")
    print("   - Useful when early tasks affect later ones")
    print("   - Fresh start with clean state")

    print("\n3. SELECTIVE Mode")
    context.mode = ReplayMode.SELECTIVE
    context.tasks_to_replay = ["T003"]  # Only replay the stuck task
    print("   - Replay specific tasks only")
    print(f"   - Selected: {context.tasks_to_replay}")
    print("   - Surgical approach for known issues")

    print("\n4. DEBUG Mode")
    context.mode = ReplayMode.DEBUG
    print("   - Enhanced logging and tracing")
    print("   - Captures detailed execution info")
    print("   - For understanding complex failures")


async def simulate_successful_replay():
    """Simulate a successful replay scenario"""
    print("\n\n=== Simulated Replay Success ===\n")

    # Show what would happen in a real replay
    print("Replaying ceremony: demo-bug-fix-2025")
    print("Mode: RESUME")
    print("\nReplay Progress:")
    print("  ✓ Created replay khipu: 2025-08-09_18-00-00_replay_demo-bug-fix-2025.md")
    print("  ✓ Reset task T003 to PENDING")
    print("  ✓ Reset task T004 to PENDING")
    print("  → Spawning apprentice for T003...")
    print("  ✓ T003 completed successfully (with timeout increase)")
    print("  → Spawning apprentice for T004...")
    print("  ✓ T004 completed successfully")
    print("\nReplay Result:")
    print("  Success: True")
    print("  Newly completed: ['T003', 'T004']")
    print("  Still failed: []")
    print("  Duration: 8.5 minutes")
    print("\nInsights:")
    print("  - Recovery rate: 100% (2/2 tasks)")
    print("  - Resume mode recovered 2 previously failed tasks")
    print("  - Timeout adjustment was key to success")


async def main():
    """Run all demonstrations"""
    print("=== Ceremony Replay Capability Demo ===")
    print("\nThis system serves Mallku's need for HEALING -")
    print("learning from failure and transforming it into wisdom.\n")

    await demonstrate_analysis()
    await demonstrate_replay_strategy()
    await demonstrate_replay_modes()
    await simulate_successful_replay()

    print("\n✨ Replay demonstration complete!")
    print("\nKey Capabilities:")
    print("  • Analyze failed ceremonies to understand issues")
    print("  • Suggest optimal replay strategies")
    print("  • Multiple replay modes for different scenarios")
    print("  • Learn from failures to improve future success")


if __name__ == "__main__":
    asyncio.run(main())
