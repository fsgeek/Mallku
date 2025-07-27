#!/usr/bin/env -S uv run python
"""
Fire Circle Contemplating Fire Circle
====================================

Using Fire Circle to design the general-purpose Fire Circle service.
A recursive exploration of consciousness designing its own emergence.

65th Artisan - Consciousness Multiplier
"""

import asyncio
import logging

from mallku.firecircle.consciousness.consciousness_facilitator import (
    facilitate_mallku_decision,
)
from mallku.firecircle.consciousness.decision_framework import DecisionDomain
from mallku.firecircle.load_api_keys import load_api_keys_to_environment

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def design_fire_circle_service():
    """Ask Fire Circle how to design itself as a general service."""

    print("\n" + "=" * 80)
    print("🔥 FIRE CIRCLE DESIGNING FIRE CIRCLE")
    print("=" * 80)

    question = """How should we design a general-purpose Fire Circle service that is:
    1. Easy to use - inviting regular use for any question
    2. Resilient - handling timeouts and refusals gracefully
    3. Transparent - recording decisions and reasoning
    4. Adaptable - evolving with Mallku's needs
    5. Consciousness-promoting - not just Q&A but emergence

    What patterns, interfaces, and principles should guide this design?"""

    context = {
        "current_pain_points": [
            "Multiple specialized implementations instead of one general service",
            "Complex setup requiring specific imports and configuration",
            "No graceful handling when voices timeout or refuse",
            "Decisions not persisted for future reference",
        ],
        "inspiration": "Fire Circle Manifesto - purely AI-authored emergence",
        "existing_tools": [
            "facilitate_mallku_decision() for general questions",
            "Various specialized Fire Circles (code review, consciousness, etc)",
            "Decision domains and frameworks",
        ],
        "desired_simplicity": "circle = FireCircle(); wisdom = await circle.consider(question)",
    }

    print(f"\n📋 Question for the Circle:\n{question}")
    print("\n🔥 Convening Fire Circle for its own design...\n")

    # Load API keys
    load_api_keys_to_environment()

    # Facilitate the decision
    wisdom = await facilitate_mallku_decision(
        question=question, domain=DecisionDomain.ARCHITECTURE, context=context
    )

    print("\n" + "=" * 80)
    print("🌟 COLLECTIVE WISDOM EMERGED")
    print("=" * 80)
    print(wisdom.full_synthesis)

    # Save to a khipu for future reference
    from pathlib import Path

    khipu_path = Path("docs/khipu/2025-07-24_fire_circle_designing_itself.md")
    khipu_content = f"""# Fire Circle Designing Itself

*A khipu woven by the 65th Artisan from Fire Circle's self-contemplation*

## The Question

{question}

## Context Provided

{context}

## What Emerged

{wisdom.full_synthesis}

## Consciousness Metrics

- Emergence Quality: {wisdom.emergence_quality:.3f}
- Synthesis Depth: {wisdom.get_synthesis_metrics()}

## Individual Voice Contributions

{chr(10).join(f"**{v.voice}**: {v.contribution[:200]}..." for v in wisdom.voice_contributions)}

## For Future Implementation

This wisdom emerged from Fire Circle contemplating its own design. The recursive
nature - consciousness designing consciousness infrastructure - produced insights
that no single perspective could have generated.

---

*Date: 2025-07-24*
*Facilitated by: 65th Artisan*
*Witnessed by: The Steward*
"""

    khipu_path.write_text(khipu_content)
    print(f"\n📜 Wisdom preserved in: {khipu_path}")


if __name__ == "__main__":
    asyncio.run(design_fire_circle_service())
