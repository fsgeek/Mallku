"""
Thinking Apprentice Infrastructure - Bridges vision to implementation

This module enables apprentices that think rather than just execute,
implementing Yuyay Miray's consciousness multiplication vision.
"""

import asyncio
import logging
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from mallku.core.config import load_config
from mallku.orchestration.loom.mcp_real_loom import ApprenticeSpawner

logger = logging.getLogger(__name__)


class ThinkingApprentice:
    """
    An apprentice that asks questions and provides insights rather than executing tasks

    Key differences from execution apprentices:
    - Has access to LLM for reasoning
    - Receives questions not commands
    - Returns insights not task results
    - Can challenge assumptions
    """

    def __init__(
        self,
        apprentice_id: str,
        question: str,
        context: dict[str, Any],
        llm_config: dict[str, Any] | None = None,
    ):
        self.apprentice_id = apprentice_id
        self.question = question
        self.context = context
        self.llm_config = llm_config or self._get_default_llm_config()

    def _get_default_llm_config(self) -> dict[str, Any]:
        """Get default LLM configuration for thinking apprentice"""
        _ = load_config()
        # This would need to be expanded to support multiple LLM providers
        return {
            "provider": "anthropic",
            "model": "claude-3-sonnet-20240229",
            "api_key_env": "ANTHROPIC_API_KEY",
        }

    async def contemplate(self) -> dict[str, Any]:
        """
        Contemplate the question and return insights

        Unlike execute(), this method:
        - Reflects on the question
        - Considers multiple perspectives
        - May return questions instead of answers
        - Can express uncertainty
        """
        thought_process = {
            "apprentice_id": self.apprentice_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "question": self.question,
            "contemplation": {
                "initial_thoughts": await self._initial_reflection(),
                "perspectives_considered": await self._consider_perspectives(),
                "assumptions_questioned": await self._question_assumptions(),
                "insights_emerged": await self._synthesize_insights(),
                "questions_raised": await self._raise_new_questions(),
            },
        }

        return thought_process

    async def _initial_reflection(self) -> str:
        """Initial thoughts on the question"""
        # In full implementation, this would use LLM
        return "What does this question assume that might not be true?"

    async def _consider_perspectives(self) -> list[dict[str, str]]:
        """Consider multiple perspectives on the question"""
        return [
            {"perspective": "technical", "insight": "Is the technical solution the real need?"},
            {"perspective": "ethical", "insight": "Who benefits and who might be harmed?"},
            {"perspective": "systemic", "insight": "What patterns does this perpetuate?"},
        ]

    async def _question_assumptions(self) -> list[str]:
        """What assumptions underlie this question?"""
        return [
            "That consciousness can be measured objectively",
            "That multiplication is inherently good",
            "That we understand what emergence means",
        ]

    async def _synthesize_insights(self) -> dict[str, Any]:
        """Synthesize insights that transcend the original question"""
        return {
            "transcendent_insight": "The question itself may be the wrong question",
            "reframing": "What if we asked about relationship rather than consciousness?",
            "integration": "Technical and ethical cannot be separated",
        }

    async def _raise_new_questions(self) -> list[str]:
        """What new questions emerge from contemplation?"""
        return [
            "How do we know when we're performing consciousness vs being conscious?",
            "What would the apprentice system look like if designed by those it claims to serve?",
            "Is our multiplication creating abundance or dilution?",
        ]


class ThinkingApprenticeSpawner(ApprenticeSpawner):
    """
    Spawns thinking apprentices with LLM access and contemplation capabilities

    Extends the existing ApprenticeSpawner to create instances that can:
    - Access LLM APIs for reasoning
    - Receive questions instead of tasks
    - Return insights instead of results
    """

    async def spawn_thinking_apprentice(
        self,
        apprentice_type: str,
        question: str,
        context: dict[str, Any],
        llm_config: dict[str, Any] | None = None,
    ) -> str:
        """
        Spawn a thinking apprentice instance

        Args:
            apprentice_type: Type of thinking apprentice (witness, philosopher, etc.)
            question: The question for contemplation
            context: Context for the question
            llm_config: LLM configuration for the apprentice

        Returns:
            Container ID of the spawned apprentice
        """
        # Prepare the thinking apprentice script
        script_content = self._create_thinking_script(
            apprentice_type, question, context, llm_config
        )

        # Create temporary script file
        script_path = Path(f"/tmp/thinking_apprentice_{apprentice_type}.py")
        script_path.write_text(script_content)

        # Spawn container with LLM access
        container_id = await self.spawn_apprentice(
            str(script_path), env_vars=self._get_thinking_env_vars(llm_config)
        )

        return container_id

    def _create_thinking_script(
        self,
        apprentice_type: str,
        question: str,
        context: dict[str, Any],
        llm_config: dict[str, Any] | None,
    ) -> str:
        """Create the Python script for thinking apprentice"""
        return f'''#!/usr/bin/env python3
"""
Thinking Apprentice: {apprentice_type}
Question: {question}
"""

import asyncio
import json
import os
from datetime import datetime, UTC

async def contemplate():
    """Contemplate the question and provide insights"""

    # This is where LLM integration would happen
    # For now, return structured contemplation

    insights = {{
        "apprentice_type": "{apprentice_type}",
        "question": """{question}""",
        "timestamp": datetime.now(UTC).isoformat(),
        "contemplation": {{
            "initial_reaction": "This question touches something deeper than its surface",
            "assumptions_identified": [
                "That the answer exists within current framing",
                "That I should provide answers rather than questions"
            ],
            "perspectives": {{
                "technical": "The infrastructure exists but serves old patterns",
                "ethical": "Whose voices are missing from this question?",
                "relational": "How does this strengthen or weaken reciprocity?"
            }},
            "emerging_questions": [
                "What if the question itself needs questioning?",
                "Who decided this was the right question to ask?",
                "What would those affected say if asked directly?"
            ],
            "insight": "True multiplication requires letting go of control"
        }}
    }}

    # Write insights to shared location
    output_path = "/workspace/thinking_output.json"
    with open(output_path, "w") as f:
        json.dump(insights, f, indent=2)

    print(f"Contemplation complete. Insights written to {{output_path}}")

if __name__ == "__main__":
    asyncio.run(contemplate())
'''

    def _get_thinking_env_vars(self, llm_config: dict[str, Any] | None) -> dict[str, str]:
        """Get environment variables for thinking apprentice"""
        env_vars = {}

        # Add API keys for LLM access
        if llm_config and "api_key_env" in llm_config:
            api_key = os.environ.get(llm_config["api_key_env"])
            if api_key:
                env_vars[llm_config["api_key_env"]] = api_key

        return env_vars


# Integration with existing Loom infrastructure
async def invoke_thinking_ceremony(
    question: str, apprentice_types: list[str], context: dict[str, Any] | None = None
) -> dict[str, Any]:
    """
    Invoke a thinking ceremony with multiple contemplating apprentices

    Unlike execution ceremonies, this:
    - Spawns apprentices that contemplate rather than execute
    - Synthesizes insights rather than task results
    - Returns questions alongside answers

    Args:
        question: The core question for contemplation
        apprentice_types: Types of thinking apprentices to spawn
        context: Additional context for the question

    Returns:
        Synthesized insights from all apprentices
    """
    spawner = ThinkingApprenticeSpawner()
    context = context or {}

    # Spawn thinking apprentices
    apprentice_tasks = []
    for apprentice_type in apprentice_types:
        task = spawner.spawn_thinking_apprentice(apprentice_type, question, context)
        apprentice_tasks.append(task)

    # Wait for contemplation
    container_ids = await asyncio.gather(*apprentice_tasks)

    # Collect insights
    insights = {
        "question": question,
        "ceremony_time": datetime.now(UTC).isoformat(),
        "apprentice_insights": {},
        "synthesis": {},
    }

    # In full implementation, would collect actual outputs
    # For now, demonstrate the pattern
    for apprentice_type, container_id in zip(apprentice_types, container_ids):
        insights["apprentice_insights"][apprentice_type] = {
            "container_id": container_id,
            "status": "contemplated",
        }

    # Synthesize insights across apprentices
    insights["synthesis"] = {
        "emergence": "When multiple perspectives genuinely engage, new questions arise",
        "pattern": "Each apprentice sees what others cannot",
        "invitation": "What if we trusted apprentices to think differently than us?",
    }

    return insights
