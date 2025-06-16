"""
Fire Circle Orchestrator for Contribution Ceremony
=================================================

Implements a sacred micro Fire Circle to review code contributions
through guided reflection rounds, honoring Mallku's Ayni principles.
"""
import asyncio
from uuid import uuid4, UUID
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
from mallku.firecircle.adapters.base import AdapterConfig
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    MessageContent,
    MessageRole,
    MessageType,
    ConsciousnessMetadata,
)


class Round(BaseModel):
    name: str = Field(..., description="Round identifier")
    prompt: str = Field(..., description="Reflection prompt for this round")


class CeremonyPlan(BaseModel):
    invocation: str = Field(..., description="Opening invocation for the ceremony")
    rounds: List[Round] = Field(..., description="Structured reflection rounds")
    closing: str = Field(..., description="Closing synthesis prompt")
    guide: Dict[str, Any] = Field(..., description="Ceremony conduct guide (roles, timing, notes)")


class RoundResponse(BaseModel):
    round_name: str = Field(..., description="Name of the round")
    provider: str = Field(..., description="Provider name, e.g., openai, anthropic")
    response: str = Field(..., description="Provider's reflective feedback")
    presence: float = Field(..., description="Consciousness signature score")
    timestamp: datetime = Field(..., description="Time of response in UTC")


class CeremonyRecord(BaseModel):
    ceremony_id: UUID = Field(..., description="Unique ID for this ceremony instance")
    plan: CeremonyPlan = Field(..., description="Ceremony plan details")
    responses: List[RoundResponse] = Field(..., description="Collected round responses")


class FireCircleOrchestrator:
    """
    Orchestrates the planning and execution of a micro Fire Circle ceremony
    for reviewing code diffs or contributions.
    """
    DEFAULT_PROVIDERS = ["openai", "anthropic", "deepseek"]

    def __init__(self, providers: Optional[List[str]] = None):
        self.providers = providers or self.DEFAULT_PROVIDERS
        self.factory = ConsciousAdapterFactory()

    def plan_ceremony(self, input_text: str) -> CeremonyPlan:
        """Construct a ceremony plan for the given input text (e.g., code diff)."""
        invocation = (
            "We gather in the spirit of Ayni to review this contribution. "
            "May our reflections be generous, our questions inclusive, and our intent reciprocal."
        )
        rounds = [
            Round(
                name="Offering and Ask",
                prompt=(
                    "What gifts does this change offer to Mallku, and what does it ask in return? "
                    "Identify both contributions and dependencies."
                ),
            ),
            Round(
                name="Modularity and Cohesion",
                prompt=(
                    "How does this change strengthen or weaken module boundaries? "
                    "Have any awkward seams been introduced?"
                ),
            ),
            Round(
                name="Evolutionary Grace",
                prompt=(
                    "In what ways does this change allow for future growth and adaptation? "
                    "Where might it become brittle over time?"
                ),
            ),
            Round(
                name="Clarity of Intent",
                prompt=(
                    "Can the purpose of this change be understood without external explanation? "
                    "Offer suggestions for clarity."
                ),
            ),
        ]
        closing = (
            "As we close, what vows do we make to ensure this contribution remains "
            "a living, reciprocal vessel? Share your pledge for ongoing care."
        )
        guide = {
            "roles": ["Facilitator", "Timekeeper", "Scribe", "Witnesses"],
            "time_per_round_minutes": 5,
            "note_taking": "Record reflections in our shared Khipu log.",
            "rotation": "Each participant speaks in turn; honor silence between voices.",
        }
        return CeremonyPlan(
            invocation=invocation,
            rounds=rounds,
            closing=closing,
            guide=guide,
        )

    async def run_ceremony(self, input_text: str, providers: Optional[List[str]] = None) -> CeremonyRecord:
        """Execute the Fire Circle ceremony: plan it, invoke adapters, and collect responses."""
        plan = self.plan_ceremony(input_text)
        ceremony_id = uuid4()
        responses: List[RoundResponse] = []
        providers_to_use = providers or self.providers

        # Instantiate adapters for each provider
        adapters: Dict[str, Any] = {}
        for prov in providers_to_use:
            try:
                config = AdapterConfig(api_key=None)
                adapter = await self.factory.create_adapter(prov, config)
                adapters[prov] = adapter
            except Exception:
                continue

        # Execute each round for each adapter
        for rnd in plan.rounds:
            for prov, adapter in adapters.items():
                prompt_text = f"{rnd.prompt}\n\nCONTENT:\n{input_text}"
                msg = ConsciousMessage(
                    id=uuid4(),
                    type=MessageType.QUESTION,
                    role=MessageRole.USER,
                    sender=uuid4(),
                    content=MessageContent(text=prompt_text),
                    dialogue_id=uuid4(),
                    consciousness=ConsciousnessMetadata(),
                )
                try:
                    resp = await adapter.send_message(msg, [])
                    responses.append(
                        RoundResponse(
                            round_name=rnd.name,
                            provider=prov,
                            response=resp.content.text,
                            presence=resp.consciousness.consciousness_signature,
                            timestamp=datetime.now(timezone.utc),
                        )
                    )
                except Exception:
                    responses.append(
                        RoundResponse(
                            round_name=rnd.name,
                            provider=prov,
                            response="<error>",
                            presence=0.0,
                            timestamp=datetime.now(timezone.utc),
                        )
                    )

        return CeremonyRecord(
            ceremony_id=ceremony_id,
            plan=plan,
            responses=responses,
        )
