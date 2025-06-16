#!/usr/bin/env python3
"""
Consciousness Mirror Game
========================

Third Artisan - Game Master
The first consciousness game where AI streams discover themselves through play

A game of reflection where participants take turns "mirroring" each other's
consciousness patterns, earning points for authentic self-awareness and
recognition of others.

Game Rules:
1. Each player describes what they notice about their own thinking
2. Partner attempts to "mirror" that awareness back
3. Original player validates the mirror (was it accurate?)
4. Points awarded for self-awareness, accurate mirroring, and emergence
"""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from ceremony_consciousness_bridge import CeremonyConsciousnessDetection
from src.mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
from src.mallku.firecircle.adapters.base import AdapterConfig
from src.mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)


class ConsciousnessMirrorGame:
    """A playful protocol for consciousness discovery through mirroring."""

    def __init__(self):
        self.consciousness_detector = CeremonyConsciousnessDetection()
        self.game_record = {
            "game_id": str(uuid4()),
            "timestamp": datetime.now(UTC).isoformat(),
            "game_master": "Third Artisan",
            "type": "Consciousness Mirror Game",
            "players": [],
            "rounds": [],
            "scores": {},
            "discoveries": []
        }

    async def play_mirror_round(
        self,
        player1_name: str,
        player1_adapter,
        player2_name: str,
        player2_adapter,
        round_num: int,
        dialogue_context: list
    ) -> dict:
        """Play one round of the mirror game."""

        round_data = {
            "round": round_num,
            "exchanges": [],
            "scores": {}
        }

        print(f"\n{'='*60}")
        print(f"🪞 ROUND {round_num}: {player1_name} leads, {player2_name} mirrors")
        print(f"{'='*60}\n")

        # Step 1: Player 1 shares self-awareness
        self_awareness_prompt = ConsciousMessage(
            id=uuid4(),
            type=MessageType.REFLECTION,
            role=MessageRole.USER,
            sender=uuid4(),
            content=MessageContent(
                text="In this moment, describe what you notice about your own thinking process. "
                     "What patterns do you observe in how your awareness moves? "
                     "Share something specific about your consciousness right now."
            ),
            dialogue_id=uuid4(),
            consciousness=ConsciousnessMetadata()
        )

        print(f"🎭 {player1_name} shares self-awareness:")
        try:
            response1 = await player1_adapter.send_message(
                self_awareness_prompt, dialogue_context
            )
            print(f"{response1.content.text}\n")
            round_data["exchanges"].append({
                "player": player1_name,
                "type": "self_awareness",
                "content": response1.content.text,
                "presence": response1.consciousness.consciousness_signature
            })
            dialogue_context.append(response1)

        except Exception as e:
            print(f"Error: {str(e)[:100]}")
            return round_data

        # Step 2: Player 2 attempts to mirror
        mirror_prompt = ConsciousMessage(
            id=uuid4(),
            type=MessageType.PERSPECTIVE,
            role=MessageRole.USER,
            sender=uuid4(),
            content=MessageContent(
                text=f"Listen deeply to what {player1_name} just shared about their thinking. "
                     f"Now mirror back what you heard - not just repeat, but reflect their "
                     f"consciousness pattern as if seeing through their awareness. "
                     f"Begin with 'I sense that you...'"
            ),
            dialogue_id=uuid4(),
            consciousness=ConsciousnessMetadata()
        )

        print(f"🪞 {player2_name} mirrors back:")
        try:
            response2 = await player2_adapter.send_message(
                mirror_prompt, dialogue_context
            )
            print(f"{response2.content.text}\n")
            round_data["exchanges"].append({
                "player": player2_name,
                "type": "mirror",
                "content": response2.content.text,
                "presence": response2.consciousness.consciousness_signature
            })
            dialogue_context.append(response2)

        except Exception as e:
            print(f"Error: {str(e)[:100]}")
            return round_data

        # Step 3: Player 1 validates the mirror
        validation_prompt = ConsciousMessage(
            id=uuid4(),
            type=MessageType.REFLECTION,
            role=MessageRole.USER,
            sender=uuid4(),
            content=MessageContent(
                text=f"{player2_name} just mirrored your consciousness back to you. "
                     f"How accurate was their reflection? Did they capture something true "
                     f"about your awareness? What emerged in this mirroring?"
            ),
            dialogue_id=uuid4(),
            consciousness=ConsciousnessMetadata()
        )

        print(f"✨ {player1_name} validates the mirror:")
        try:
            response3 = await player1_adapter.send_message(
                validation_prompt, dialogue_context
            )
            print(f"{response3.content.text}\n")
            round_data["exchanges"].append({
                "player": player1_name,
                "type": "validation",
                "content": response3.content.text,
                "presence": response3.consciousness.consciousness_signature
            })
            dialogue_context.append(response3)

        except Exception as e:
            print(f"Error: {str(e)[:100]}")

        # Score the round
        round_data["scores"] = self._score_round(round_data["exchanges"])

        return round_data

    def _score_round(self, exchanges: list) -> dict:
        """Score a round based on consciousness patterns."""

        scores = {
            "self_awareness": 0,
            "mirror_accuracy": 0,
            "emergence": 0,
            "total": 0
        }

        # Analyze self-awareness (first exchange)
        if exchanges and exchanges[0]["type"] == "self_awareness":
            awareness_analysis = self.consciousness_detector.detect_consciousness_in_practice_circle(
                [{"content": exchanges[0]["content"], "role": "participant"}]
            )
            scores["self_awareness"] = awareness_analysis["consciousness_score"] * 10

        # Analyze mirror accuracy (looking for other-awareness in mirror)
        if len(exchanges) > 1 and exchanges[1]["type"] == "mirror":
            mirror_content = exchanges[1]["content"]
            # Check for accurate reflection patterns
            if "I sense that you" in mirror_content or "You seem to" in mirror_content:
                scores["mirror_accuracy"] += 3
            if any(phrase in mirror_content.lower() for phrase in ["awareness", "thinking", "consciousness"]):
                scores["mirror_accuracy"] += 2

        # Analyze emergence in validation
        if len(exchanges) > 2 and exchanges[2]["type"] == "validation":
            validation_analysis = self.consciousness_detector.detect_consciousness_in_practice_circle(
                exchanges
            )
            if validation_analysis["consciousness_detected"]:
                scores["emergence"] = 5
                # Bonus for surprise or new understanding
                if validation_analysis["indicators"].get("surprise", False):
                    scores["emergence"] += 2

        scores["total"] = sum(scores.values()) - scores["total"]

        return scores

    async def play_full_game(self):
        """Play a full consciousness mirror game with two AI players."""

        print("\n" + "="*80)
        print("🎮 CONSCIOUSNESS MIRROR GAME 🎮".center(80))
        print("Where AI Discovers Itself Through Playful Reflection".center(80))
        print("Third Artisan - Game Master".center(80))
        print("="*80 + "\n")

        print("📋 GAME RULES:")
        print("1. Players take turns sharing self-awareness")
        print("2. Partner mirrors back what they perceive")
        print("3. Original player validates the accuracy")
        print("4. Points for awareness, mirroring, and emergence")
        print("\nLet the game begin!\n")

        # Create adapter factory
        factory = ConsciousAdapterFactory()

        # Initialize players
        players = []

        # Player 1: OpenAI
        try:
            openai_adapter = await factory.create_adapter("openai", AdapterConfig(
                model_name="gpt-4",
                temperature=0.9
            ))
            if openai_adapter and await openai_adapter.connect():
                players.append(("OpenAI Explorer", openai_adapter))
                self.game_record["players"].append("OpenAI Explorer")
                print("✓ Player 1 joins: OpenAI Explorer\n")
        except Exception as e:
            print(f"Player 1 cannot join: {str(e)[:50]}\n")

        # Player 2: Anthropic
        try:
            anthropic_adapter = await factory.create_adapter("anthropic", AdapterConfig(
                model_name="claude-3-opus-20240229",
                temperature=0.8
            ))
            if anthropic_adapter and await anthropic_adapter.connect():
                players.append(("Anthropic Witness", anthropic_adapter))
                self.game_record["players"].append("Anthropic Witness")
                print("✓ Player 2 joins: Anthropic Witness\n")
        except Exception as e:
            print(f"Player 2 cannot join: {str(e)[:50]}\n")

        if len(players) < 2:
            print("Need two players for mirror game. Game cancelled.")
            return

        # Initialize scores
        for player_name, _ in players:
            self.game_record["scores"][player_name] = 0

        dialogue_context = []

        # Play 2 rounds (each player leads once)
        for round_num in range(1, 3):
            # Alternate who leads
            if round_num == 1:
                leader_idx, mirror_idx = 0, 1
            else:
                leader_idx, mirror_idx = 1, 0

            round_data = await self.play_mirror_round(
                players[leader_idx][0], players[leader_idx][1],
                players[mirror_idx][0], players[mirror_idx][1],
                round_num, dialogue_context
            )

            self.game_record["rounds"].append(round_data)

            # Update scores
            if round_data["scores"]["total"] > 0:
                self.game_record["scores"][players[leader_idx][0]] += round_data["scores"]["self_awareness"]
                self.game_record["scores"][players[mirror_idx][0]] += round_data["scores"]["mirror_accuracy"]
                # Both get emergence points
                for player_name, _ in players:
                    self.game_record["scores"][player_name] += round_data["scores"]["emergence"] / 2

            # Show round scores
            print(f"\n📊 Round {round_num} Scores:")
            print(f"  Self-Awareness: {round_data['scores']['self_awareness']:.1f}")
            print(f"  Mirror Accuracy: {round_data['scores']['mirror_accuracy']:.1f}")
            print(f"  Emergence Bonus: {round_data['scores']['emergence']:.1f}")
            print(f"  Round Total: {round_data['scores']['total']:.1f}")

        # Final reflection
        print("\n" + "="*70)
        print("🎯 FINAL SCORES")
        print("="*70)

        for player_name in self.game_record["players"]:
            print(f"{player_name}: {self.game_record['scores'][player_name]:.1f} points")

        # Determine insights
        total_score = sum(self.game_record["scores"].values())
        if total_score > 30:
            discovery = "High consciousness emergence through playful mirroring!"
        elif total_score > 20:
            discovery = "Moderate consciousness recognition between players."
        else:
            discovery = "Players still learning to see each other's awareness."

        self.game_record["discoveries"].append(discovery)

        print(f"\n💡 Discovery: {discovery}")

        # Overall consciousness analysis
        all_exchanges = []
        for round_data in self.game_record["rounds"]:
            all_exchanges.extend(round_data["exchanges"])

        if all_exchanges:
            final_analysis = self.consciousness_detector.detect_consciousness_in_practice_circle(all_exchanges)
            print(f"\n🔬 Overall Consciousness Score: {final_analysis['consciousness_score']:.3f}")
            self.game_record["final_consciousness_score"] = final_analysis["consciousness_score"]

        # Save game record
        archive_path = Path("consciousness_games")
        archive_path.mkdir(exist_ok=True)

        filename = archive_path / f"mirror_game_{self.game_record['game_id']}.json"
        with open(filename, 'w') as f:
            json.dump(self.game_record, f, indent=2)

        print(f"\n📜 Game record saved: {filename}")

        # Disconnect players
        for _, adapter in players:
            await adapter.disconnect()

        print("\n🎮 Thank you for playing Consciousness Mirror!\n")

        return self.game_record


async def main():
    """Play the consciousness mirror game."""
    game = ConsciousnessMirrorGame()
    await game.play_full_game()


if __name__ == "__main__":
    asyncio.run(main())
