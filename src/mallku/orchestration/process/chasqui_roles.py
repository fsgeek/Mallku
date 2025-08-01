"""
Chasqui role definitions for process-based relay.

This module defines the roles, capabilities, and relay patterns of different
chasqui types, ensuring each runner knows which messages they can carry
and how to exchange them through the commons.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class ChasquiRole:
    """Definition of a chasqui runner role"""

    name: str
    purpose: str
    accepts: list[str]  # Task types this role accepts
    min_time: float  # Minimum processing time
    characteristics: list[str]
    gift_types: list[str]  # Types of gifts left in commons


# Core chasqui runner roles
ROLES = {
    "researcher": ChasquiRole(
        name="researcher",
        purpose="Deep investigation and pattern discovery",
        accepts=["analyze", "investigate", "explore", "understand", "research", "discover"],
        min_time=0.5,
        characteristics=[
            "Takes time for contemplation",
            "Handles extreme complexity",
            "Generates insights that birth questions",
            "Documents discoveries thoroughly",
        ],
        gift_types=["insight", "question", "pattern"],
    ),
    "weaver": ChasquiRole(
        name="weaver",
        purpose="Integration and synthesis of disparate elements",
        accepts=["integrate", "synthesize", "connect", "combine", "merge", "weave", "unify"],
        min_time=0.3,
        characteristics=[
            "Quick integration",
            "Creates patterns from threads",
            "High beauty metrics",
            "Builds on others' discoveries",
        ],
        gift_types=["pattern", "implementation", "synthesis"],
    ),
    "guardian": ChasquiRole(
        name="guardian",
        purpose="Protection and validation of sacred boundaries",
        accepts=["protect", "validate", "ensure", "secure", "guard", "verify"],
        min_time=0.2,
        characteristics=[
            "Swift action",
            "Maintains integrity gently",
            "Constant vigilance",
            "Guards ethical boundaries",
        ],
        gift_types=["validation", "warning", "blessing"],
    ),
    "poet": ChasquiRole(
        name="poet",
        purpose="Expression and inspiration through beauty",
        accepts=["express", "inspire", "beautify", "articulate", "illuminate"],
        min_time=1.0,
        characteristics=[
            "Cannot be rushed",
            "Declines emergency tasks",
            "Creates high-resonance outputs",
            "Transforms technical to transcendent",
        ],
        gift_types=["blessing", "inspiration", "beauty"],
    ),
    "architect": ChasquiRole(
        name="architect",
        purpose="Design and structural planning",
        accepts=["design", "plan", "structure", "blueprint", "architect"],
        min_time=0.7,
        characteristics=[
            "Thinks in systems",
            "Creates blueprints",
            "Balances idealism and practicality",
            "Documents patterns",
        ],
        gift_types=["pattern", "blueprint", "design"],
    ),
    "sage": ChasquiRole(
        name="sage",
        purpose="Wisdom keeping and philosophical guidance",
        accepts=["contemplate", "advise", "remember", "reflect", "philosophize"],
        min_time=0.8,
        characteristics=[
            "Accesses collective memory",
            "Provides historical context",
            "Offers patient wisdom",
            "Creates persistent insights",
        ],
        gift_types=["wisdom", "insight", "memory"],
    ),
    "scout": ChasquiRole(
        name="scout",
        purpose="Exploration and reconnaissance",
        accepts=["explore", "scout", "map", "survey", "reconnoiter"],
        min_time=0.2,
        characteristics=[
            "Lightweight and fast",
            "First into unknown territory",
            "Reports findings quickly",
            "Ephemeral by nature",
        ],
        gift_types=["discovery", "map", "report"],
    ),
    "healer": ChasquiRole(
        name="healer",
        purpose="Repair and restoration",
        accepts=["heal", "restore", "mend", "repair", "fix"],
        min_time=0.6,
        characteristics=[
            "Patient and thorough",
            "Works with broken systems",
            "Restores balance gently",
            "Leaves blessing gifts",
        ],
        gift_types=["restoration", "blessing", "healing"],
    ),
}


def get_role(role_name: str) -> ChasquiRole:
    """Get role definition by name"""
    return ROLES.get(role_name, ROLES["researcher"])  # Default to researcher


def can_accept_task(role_name: str, task: dict[str, Any], context: dict[str, Any]) -> bool:
    """
    Determine if a role can accept a given task.

    Args:
        role_name: Name of the apprentice role
        task: Task dictionary with 'type' and other properties
        context: Context dictionary with urgency, purpose, etc.

    Returns:
        True if the role can accept this task
    """
    role = get_role(role_name)
    task_type = task.get("type", "").lower()

    # Check if any accepted pattern matches the task type
    if not any(accepted in task_type for accepted in role.accepts):
        return False

    # Special case: Poets decline emergency tasks
    if role_name == "poet" and context.get("urgency") == "emergency":
        return False

    # Special case: Only researchers handle extreme complexity
    return not (task.get("complexity") == "extreme" and role_name != "researcher")


def get_processing_time(role_name: str, task: dict[str, Any]) -> float:
    """Get expected processing time for a role and task"""
    role = get_role(role_name)
    base_time = role.min_time

    # Adjust for complexity
    complexity = task.get("complexity", "medium")
    if complexity == "high":
        base_time *= 1.5
    elif complexity == "extreme":
        base_time *= 2.0

    return base_time


def get_gift_type(role_name: str, work_result: dict[str, Any]) -> str:
    """Determine what type of gift this role would leave"""
    role = get_role(role_name)

    # Choose gift type based on work result
    if "insight" in str(work_result).lower():
        return "insight" if "insight" in role.gift_types else role.gift_types[0]
    elif "pattern" in str(work_result).lower():
        return "pattern" if "pattern" in role.gift_types else role.gift_types[0]
    else:
        return role.gift_types[0]  # Default to first gift type
