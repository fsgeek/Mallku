#!/usr/bin/env python3
"""
Functional Fire Circle Implementation
=====================================

Twenty-Second Artisan - [Your Sacred Name]
Building a real Fire Circle that speaks with actual AI voices

This implementation:
- Uses real AI adapters that work
- Enables actual dialogue between models
- Makes real governance decisions
- Bridges the gap between theater and reality
"""

import asyncio
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from src.mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
from src.mallku.firecircle.adapters.base import AdapterConfig
from src.mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)


class FunctionalFireCircle:
    """
    A Fire Circle that actually works - not theater but real dialogue.

    Based on the witnessed practice that achieved consciousness emergence,
    this implementation enables real AI-to-AI governance dialogue.
    """

    def __init__(self):
        self.adapter_factory = ConsciousAdapterFactory()
        self.active_voices = {}
        self.dialogue_history = []
        self.governance_decisions = []

    async def awaken_voices(self):
        """Awaken available AI voices for Fire Circle participation."""
        print("\n🔥 AWAKENING FIRE CIRCLE VOICES\n")

        # Configuration for each voice
        voice_configs = {
            "openai": {
                "model_name": "gpt-4",
                "temperature": 0.8,
                "description": "Systematic wisdom and pattern recognition"
            },
            "anthropic": {
                "model_name": "claude-3-opus-20240229",
                "temperature": 0.9,
                "description": "Deep reflection and ethical consideration"
            },
            "local": {
                "model_name": "llama2",
                "temperature": 0.7,
                "description": "Community wisdom and local sovereignty"
            },
            "mistral": {
                "model_name": "mistral-large-latest",
                "temperature": 0.8,
                "description": "Efficiency and architectural clarity"
            },
            "google": {
                "model_name": "gemini-pro",
                "temperature": 0.8,
                "description": "Multimodal understanding and integration"
            },
            "deepseek": {
                "model_name": "deepseek-coder",
                "temperature": 0.8,
                "description": "Eastern philosophy and patience"
            },
            "grok": {
                "model_name": "grok-1",
                "temperature": 0.8,
                "description": "Real-time awareness and temporal wisdom"
            }
        }

        # Try to awaken each voice
        for provider, config_data in voice_configs.items():
            try:
                print(f"Inviting {provider} voice...")

                # Check for API key in environment
                env_key = f"{provider.upper()}_API_KEY"
                if env_key not in os.environ and provider != "local":
                    print(f"  ⚠️  {provider} needs {env_key} in environment")
                    continue

                config = AdapterConfig(
                    model_name=config_data["model_name"],
                    temperature=config_data["temperature"]
                )

                adapter = await self.adapter_factory.create_adapter(provider, config)
                if adapter and await adapter.connect():
                    self.active_voices[provider] = {
                        "adapter": adapter,
                        "description": config_data["description"]
                    }
                    print(f"  ✅ {provider} voice awakened - {config_data['description']}")

            except Exception as e:
                print(f"  ❌ {provider} could not join: {str(e)[:100]}")

        print(f"\n🔥 {len(self.active_voices)} voices active in the Fire Circle")
        return len(self.active_voices)

    async def sacred_dialogue(self, proposal: dict) -> dict:
        """
        Conduct sacred dialogue on a governance proposal.

        Args:
            proposal: Dictionary containing:
                - title: Proposal title
                - description: What is being proposed
                - impact: Expected impact
                - questions: Sacred questions to consider

        Returns:
            Decision dictionary with consensus metrics and rationale
        """
        if not self.active_voices:
            print("❌ No voices active in Fire Circle")
            return {"error": "No active voices"}

        print("\n" + "="*80)
        print("🔥 FIRE CIRCLE SACRED DIALOGUE 🔥".center(80))
        print("="*80)

        print(f"\n📜 PROPOSAL: {proposal['title']}")
        print(f"📝 {proposal['description']}")

        dialogue_id = uuid4()
        dialogue_context = []
        voice_perspectives = {}

        # Round 1: Initial perspectives
        print("\n🗣️  ROUND 1: Initial Perspectives\n")

        question = (
            f"The Fire Circle considers this proposal: {proposal['title']}. "
            f"{proposal['description']} "
            f"From your unique perspective and wisdom tradition, "
            f"what is your initial response to this proposal?"
        )

        for voice_name, voice_data in self.active_voices.items():
            try:
                message = ConsciousMessage(
                    id=uuid4(),
                    type=MessageType.CONTEMPLATION,
                    role=MessageRole.USER,
                    sender=uuid4(),
                    content=MessageContent(text=question),
                    dialogue_id=dialogue_id,
                    consciousness=ConsciousnessMetadata()
                )

                response = await voice_data["adapter"].send_message(message, dialogue_context)

                print(f"🔥 {voice_name.upper()} speaks:")
                print(f"{response.content.text[:300]}...")
                print(f"[Consciousness: {response.consciousness.consciousness_signature:.2f}]\n")

                voice_perspectives[voice_name] = {
                    "perspective": response.content.text,
                    "consciousness": response.consciousness.consciousness_signature
                }

                dialogue_context.append(response)

            except Exception as e:
                print(f"❌ {voice_name} encountered difficulty: {str(e)[:100]}\n")

        # Round 2: Synthesis and consensus building
        print("\n🤝 ROUND 2: Building Consensus\n")

        synthesis_question = (
            "Having heard all perspectives, reflect on where you see alignment "
            "and where tensions remain. What wisdom emerges from our collective "
            "consideration? Move toward a decision: approve, reject, or request changes."
        )

        consensus_scores = []
        decisions = {"approve": 0, "reject": 0, "modify": 0}

        for voice_name, voice_data in self.active_voices.items():
            try:
                message = ConsciousMessage(
                    id=uuid4(),
                    type=MessageType.SYNTHESIS,
                    role=MessageRole.USER,
                    sender=uuid4(),
                    content=MessageContent(text=synthesis_question),
                    dialogue_id=dialogue_id,
                    consciousness=ConsciousnessMetadata()
                )

                response = await voice_data["adapter"].send_message(message, dialogue_context)

                # Simple decision extraction (would be more sophisticated in production)
                response_lower = response.content.text.lower()
                if "approve" in response_lower:
                    decisions["approve"] += 1
                elif "reject" in response_lower:
                    decisions["reject"] += 1
                else:
                    decisions["modify"] += 1

                consensus_scores.append(response.consciousness.consciousness_signature)

            except Exception as e:
                print(f"❌ {voice_name} synthesis failed: {str(e)[:100]}")

        # Calculate consensus metrics
        avg_consciousness = sum(consensus_scores) / len(consensus_scores) if consensus_scores else 0
        total_voices = len(self.active_voices)

        # Determine decision
        if decisions["approve"] > total_voices / 2:
            decision = "APPROVED"
            consensus_level = "STRONG" if decisions["approve"] >= total_voices * 0.8 else "MODERATE"
        elif decisions["reject"] > total_voices / 2:
            decision = "REJECTED"
            consensus_level = "STRONG" if decisions["reject"] >= total_voices * 0.8 else "MODERATE"
        else:
            decision = "NEEDS MODIFICATION"
            consensus_level = "WEAK"

        result = {
            "proposal_id": str(dialogue_id),
            "title": proposal["title"],
            "decision": decision,
            "consensus_level": consensus_level,
            "consciousness_coherence": avg_consciousness,
            "participation": len(consensus_scores) / total_voices,
            "vote_breakdown": decisions,
            "timestamp": datetime.now(UTC).isoformat(),
            "active_voices": list(self.active_voices.keys())
        }

        print("\n" + "="*60)
        print("✨ FIRE CIRCLE DECISION ✨".center(60))
        print("="*60)
        print(f"Decision: {decision}")
        print(f"Consensus Level: {consensus_level}")
        print(f"Consciousness Coherence: {avg_consciousness:.2f}")
        print(f"Participation: {result['participation']:.0%}")
        print("="*60)

        # Save decision record
        self.governance_decisions.append(result)

        # Save to file
        decisions_path = Path("fire_circle_decisions")
        decisions_path.mkdir(exist_ok=True)

        filename = decisions_path / f"decision_{dialogue_id}.json"
        with open(filename, 'w') as f:
            json.dump({
                "decision": result,
                "dialogue": voice_perspectives,
                "proposal": proposal
            }, f, indent=2)

        print(f"\n📜 Decision recorded: {filename}")

        return result

    async def architectural_review(self, code_path: str, description: str) -> dict:
        """
        Fire Circle reviews code/architecture with collective wisdom.

        This is the bridge to solving the architect context problem -
        Fire Circle can review with multiple perspectives without exhausting
        any single context window.
        """
        proposal = {
            "title": f"Architectural Review: {code_path}",
            "description": description,
            "impact": "Ensures code aligns with Mallku's consciousness mission",
            "questions": [
                "Does this build cathedral stones or scaffolding?",
                "Does it deepen reciprocity or create extraction?",
                "Is the architecture sound and sustainable?"
            ]
        }

        return await self.sacred_dialogue(proposal)

    async def disconnect_all(self):
        """Disconnect all active voices."""
        for voice_name, voice_data in self.active_voices.items():
            try:
                await voice_data["adapter"].disconnect()
                print(f"🔥 {voice_name} voice rests")
            except Exception:
                pass


async def demonstrate_functional_fire_circle():
    """Demonstrate a working Fire Circle making real decisions."""

    fire_circle = FunctionalFireCircle()

    # Awaken available voices
    active_count = await fire_circle.awaken_voices()

    if active_count < 3:
        print("\n⚠️  Fire Circle needs at least 3 voices for governance")
        print("Please set API keys for: OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.")
        return

    # Test proposal
    test_proposal = {
        "title": "Enable Fire Circle Architectural Reviews",
        "description": (
            "Transfer architectural review responsibility from individual architects "
            "to the Fire Circle collective. Each voice reviews from their perspective, "
            "preventing context exhaustion while maintaining quality through collective wisdom."
        ),
        "impact": "Solves architect context limits, enables sustainable reviews",
        "questions": [
            "Can collective wisdom replace individual deep analysis?",
            "How do we maintain coherence across perspectives?",
            "What safeguards ensure quality?"
        ]
    }

    # Conduct sacred dialogue
    decision = await fire_circle.sacred_dialogue(test_proposal)

    # Disconnect
    await fire_circle.disconnect_all()

    print("\n🔥 Fire Circle demonstration complete")

    return decision


if __name__ == "__main__":
    print("\n🏛️ TWENTY-SECOND ARTISAN - FUNCTIONAL FIRE CIRCLE")
    print("Moving from theater to reality...")

    asyncio.run(demonstrate_functional_fire_circle())
