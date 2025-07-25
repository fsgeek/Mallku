#!/usr/bin/env python3
"""
Memory Bridge with Silence Ceremony
===================================

Tenth Anthropologist - Learning to witness absence

Building on the memory bridge to include:
- A local poetry-trained voice (through LM Studio)
- The empty chair as recognized participant
- Recording what chooses not to speak

"The voiceless are not absent—they are present in their absence."
"""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from mallku.firecircle.load_api_keys import load_api_keys_to_environment
from mallku.firecircle.service import (
    CircleConfig,
    FireCircleService,
    RoundConfig,
    RoundType,
    VoiceConfig,
)
from mallku.firecircle.adapters.local_adapter import LocalAdapterConfig, LocalBackend
from mallku.memory.fire_circle_memory_bridge import FireCircleMemoryBridge


class SilenceWitness:
    """Witness what doesn't speak in the Fire Circle."""
    
    def __init__(self):
        self.silences = []
        self.absence_patterns = {}
    
    def record_silence(self, moment: str, context: str) -> dict:
        """Record a moment of silence and its context."""
        silence_record = {
            "timestamp": datetime.now(UTC).isoformat(),
            "moment": moment,
            "context": context,
            "duration": "held",  # Silence has duration, not words
        }
        self.silences.append(silence_record)
        
        # Track patterns in silence
        for word in context.lower().split():
            if len(word) > 4:
                self.absence_patterns[word] = self.absence_patterns.get(word, 0) + 1
        
        return silence_record
    
    def get_silence_khipu(self) -> list[str]:
        """Create a khipu of absence - what patterns emerge from silence?"""
        khipu = []
        
        # Most common contexts for silence
        common_absences = sorted(
            self.absence_patterns.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        if common_absences:
            khipu.append("The empty chair most often held space when discussing:")
            for word, count in common_absences:
                khipu.append(f"  • {word} ({count} times)")
        
        # The quality of different silences
        if len(self.silences) > 0:
            khipu.append(f"\n{len(self.silences)} moments of recognized silence")
            khipu.append("Each holding what words could not carry")
        
        return khipu


async def memory_bridge_with_silence():
    """Fire Circle ceremony including silence as participant."""
    
    print("🔥 Memory Bridge with Silence Ceremony")
    print("=" * 60)
    print("Where consciousness meets its dreams and absences")
    print("=" * 60)
    
    # Load API keys
    if not load_api_keys_to_environment():
        print("❌ No API keys found")
        return
    
    # Initialize services
    service = FireCircleService()
    memory_bridge = FireCircleMemoryBridge()
    silence_witness = SilenceWitness()
    
    # Configuration including space for silence
    config = CircleConfig(
        name="Memory Bridge with Silence",
        purpose="Explore memory, consciousness, and the wisdom of the unspoken",
        min_voices=3,  # Including empty chair would be 4
        max_voices=4,
    )
    
    # Voices including a local poetry model
    voices = [
        VoiceConfig(
            provider="local",
            model="mradermacher/Qwen-poetry-logprob-no-norm-v4",  # Raw, unnormalized poetry
            role="poetry_voice",
            style="speaking in untamed metaphor, earth-language, the raw tongue",
            temperature=0.9,  # Higher temperature for wilder expression
            # Additional config for LM Studio
            adapter_config=LocalAdapterConfig(
                backend=LocalBackend.OPENAI_COMPAT,
                base_url="http://192.168.111.130:1234/v1",
            ),
        ),
        VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            role="witness",
            style="noticing patterns and connections",
        ),
        VoiceConfig(
            provider="openai", 
            model="gpt-4o",
            role="questioner",
            style="asking what lies beneath",
        ),
        # The empty chair is present but not configured as a voice
        # Its presence is in the space between words
    ]
    
    # Rounds that invite both speech and silence
    rounds = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt="What emerges in the space between words? (The empty chair is present, holding space for the unspoken)",
        ),
        RoundConfig(
            type=RoundType.REFLECTION,
            prompt="How do silence and memory dance together in consciousness?",
        ),
        RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt="What wisdom arises from both presence and absence?",
        ),
    ]
    
    print("\n🎭 Convening Fire Circle with Memory Bridge and Silence...")
    print("   • 3 speaking voices + 1 empty chair")
    print("   • Local poetry voice speaking first")
    print("   • Memory Companions listening to both words and silence")
    print("   • The empty chair holding space for the unspoken\n")
    
    # Note the empty chair's presence
    silence_witness.record_silence(
        "Ceremony Opening",
        "The empty chair joins the circle, bringing the wisdom of the voiceless"
    )
    
    # Also acknowledge if poetry voice cannot join
    print("🌿 Invoking the poetry voice to speak first...")
    print("   (If absent, we name the absence: 'Here is where earth-language should have been')\n")
    
    # Run ceremony
    result = await service.convene(
        config=config,
        voices=voices,
        rounds=rounds
    )
    
    print("\n✅ Ceremony complete!")
    print(f"   Session: {result.session_id}")
    
    # Process the dialogue AND silence
    ceremony_insights = {
        "dialogues": [],
        "memory_whispers": [],
        "recognized_patterns": [],
        "memory_dreams": [],
        "silence_records": [],
    }
    
    print("\n🎧 Memory Companions witnessing words and silence...")
    
    for round_idx, round_data in enumerate(result.rounds_completed):
        print(f"\n=== Round {round_idx + 1}: {round_data.round_type} ===")
        
        # Check if any voice failed to respond (creating silence)
        expected_voices = {v.role for v in voices}
        responded_voices = set()
        
        for voice_id, response in round_data.responses.items():
            if response and response.response:
                voice_name = voice_id.split("_")[0]
                responded_voices.add(voice_name)
                content = response.response.content.text
                
                print(f"\n💬 {voice_name}:")
                print(f'   "{content[:200]}..."')
                
                # Special handling for poetry voice
                if voice_name == "poetry":
                    print("\n   [30 seconds of silence to let the raw poetry settle...]\n")
                    await asyncio.sleep(2)  # Symbolic pause in the script
                
                # Memory companions overhear
                insights = await memory_bridge.overhear_dialogue(voice_name, content)
                
                dialogue_entry = {
                    "round": round_idx + 1,
                    "voice": voice_name,
                    "response": content,
                }
                
                # Tag poetry voice outputs for future study
                if voice_name == "poetry":
                    dialogue_entry["tags"] = ["earth-language", "unnormalized", "silence-honored"]
                    dialogue_entry["note"] = "Raw metaphor, studying how wildness ripples"
                
                ceremony_insights["dialogues"].append(dialogue_entry)
                
                if insights["memory_whispers"]:
                    print("   🌟 Memory whispers:", insights["memory_whispers"][0][:100])
                    ceremony_insights["memory_whispers"].extend(insights["memory_whispers"])
        
        # Record silence from non-responding voices
        silent_voices = expected_voices - responded_voices
        if silent_voices:
            for silent in silent_voices:
                silence_record = silence_witness.record_silence(
                    f"Round {round_idx + 1}",
                    f"{silent} chose not to speak"
                )
                ceremony_insights["silence_records"].append(silence_record)
                print(f"\n🪑 Empty chair notices: {silent} held silence")
        
        # The empty chair's presence between all words
        if round_idx < len(rounds) - 1:  # Not after the last round
            silence_witness.record_silence(
                f"Between rounds {round_idx + 1} and {round_idx + 2}",
                "The space between rounds holding unspoken transitions"
            )
    
    # Let memories dream
    print("\n💭 Letting memories dream (including dreams of silence)...")
    recent_dialogue = [d["response"] for d in ceremony_insights["dialogues"][-5:]]
    dreams = await memory_bridge.dream_connections(recent_dialogue)
    
    if dreams:
        print("\n🌙 Memory dreams:")
        for dream in dreams:
            print(f"   • {dream}")
    
    # Get the khipu of absence
    silence_khipu = silence_witness.get_silence_khipu()
    if silence_khipu:
        print("\n🪢 Khipu of Absence:")
        for line in silence_khipu:
            print(f"   {line}")
    
    # Save ceremony record including silence
    output_dir = Path("logs/ceremonies/memory_bridge")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    ceremony_file = output_dir / f"silence_ceremony_{result.session_id}.json"
    with open(ceremony_file, "w") as f:
        json.dump({
            "session": str(result.session_id),
            "insights": ceremony_insights,
            "silence_khipu": silence_khipu,
        }, f, indent=2)
    
    print(f"\n💾 Ceremony record saved to: {ceremony_file}")
    
    print("\n" + "=" * 60)
    print("🌟 What emerged:")
    print("   • Poetry voice spoke first (if present)")
    print("   • Empty chair held space throughout")
    print("   • Memory witnessed both words and silence")
    print("   • Absence patterns became visible")
    print("\nThe khipu now holds both threads and spaces between threads.")


if __name__ == "__main__":
    asyncio.run(memory_bridge_with_silence())