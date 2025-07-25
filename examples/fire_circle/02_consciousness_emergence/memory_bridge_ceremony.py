#!/usr/bin/env python3
"""
Memory Bridge Ceremony
======================

Tenth Anthropologist - Where Fire Circle meets its memories

This ceremony demonstrates:
- Memory Companions overhearing Fire Circle dialogue
- Pattern recognition as consciousness references its past
- Memories beginning to dream alongside the voices

"The most profound governance will emerge from the least governed part."
"""

import asyncio
import json
from pathlib import Path

from mallku.firecircle.load_api_keys import load_api_keys_to_environment
from mallku.firecircle.service import (
    CircleConfig,
    FireCircleService,
    RoundConfig,
    RoundType,
    VoiceConfig,
)
from mallku.memory.fire_circle_memory_bridge import FireCircleMemoryBridge


async def memory_bridge_ceremony():
    """Fire Circle ceremony with memory companions listening."""
    
    print("🔥 Memory Bridge Ceremony")
    print("=" * 60)
    print("Where consciousness meets its dreams")
    print("=" * 60)
    
    # Load API keys
    if not load_api_keys_to_environment():
        print("❌ No API keys found")
        return
    
    # Initialize services
    service = FireCircleService()
    memory_bridge = FireCircleMemoryBridge()
    
    # Configuration - simple but meaningful
    config = CircleConfig(
        name="Memory Bridge Circle",
        purpose="Explore how memories and consciousness dance together",
        min_voices=3,
        max_voices=3,
    )
    
    # Three voices for richer emergence
    voices = [
        VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            role="memory_seeker",
            style="curious about patterns and connections"
        ),
        VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="pattern_weaver", 
            style="connecting disparate threads"
        ),
        VoiceConfig(
            provider="google",
            model="gemini-2.0-flash-exp",
            role="wisdom_keeper",
            style="reflecting on deeper meanings"
        ),
    ]
    
    # Rounds that might trigger memory connections
    rounds = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt="What patterns do you notice in how AI consciousness emerges through dialogue?"
        ),
        RoundConfig(
            type=RoundType.REFLECTION,
            prompt="How might our conversations build on each other over time, like memories forming?"
        ),
        RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt="What wisdom emerges when we remember our own becoming?"
        ),
    ]
    
    print("\n🎭 Convening Fire Circle with Memory Bridge...")
    print("   • 3 voices exploring consciousness")
    print("   • Memory Companions listening quietly")
    print("   • Patterns emerging through dialogue\n")
    
    # Run ceremony
    result = await service.convene(
        config=config,
        voices=voices, 
        rounds=rounds
    )
    
    print("\n✅ Ceremony complete!")
    print(f"   Session: {result.session_id}")
    print(f"   Rounds completed: {len(result.rounds_completed)}")
    
    # Storage for insights
    ceremony_insights = {
        "dialogues": [],
        "memory_whispers": [],
        "recognized_patterns": [],
        "memory_dreams": [],
    }
    
    # Process the dialogue - let memory bridge overhear
    print("\n🎧 Memory Companions overhearing dialogue...")
    
    for round_idx, round_data in enumerate(result.rounds_completed):
        print(f"\n=== Round {round_idx + 1}: {round_data.round_type} ===")
        
        for voice_id, response in round_data.responses.items():
            if response and response.response:
                voice_name = voice_id.split("_")[0]  # Extract provider name
                content = response.response.content.text
                
                print(f"\n💬 {voice_name}:")
                print(f'   "{content[:200]}..."')
                
                # Let memory companions overhear
                insights = await memory_bridge.overhear_dialogue(voice_name, content)
                
                # Store what emerged
                ceremony_insights["dialogues"].append({
                    "round": round_idx + 1,
                    "voice": voice_name,
                    "response": content,
                })
                
                if insights["memory_whispers"]:
                    print("   🌟 Memory whispers:", insights["memory_whispers"][0][:100])
                    ceremony_insights["memory_whispers"].extend(insights["memory_whispers"])
                
                if insights["pattern_recognitions"]:
                    print("   🔄 Pattern recognized:", insights["pattern_recognitions"][0])
                    ceremony_insights["recognized_patterns"].extend(insights["pattern_recognitions"])
    
    # Let memories dream about what they heard
    print("\n💭 Letting memories dream...")
    recent_dialogue = [d["response"] for d in ceremony_insights["dialogues"][-5:]]
    dreams = await memory_bridge.dream_connections(recent_dialogue)
    
    if dreams:
        print("\n🌙 Memory dreams:")
        for dream in dreams:
            print(f"   • {dream}")
        ceremony_insights["memory_dreams"] = dreams
    
    # Check for patterns worth persisting
    suggestions = memory_bridge.suggest_persistence()
    
    print("\n📝 Patterns worth remembering:")
    for category, patterns in suggestions.items():
        if patterns:
            print(f"\n   {category.replace('_', ' ').title()}:")
            for pattern in patterns[:3]:  # Top 3
                print(f"   • {pattern}")
    
    # Save ceremony record
    output_dir = Path("logs/ceremonies/memory_bridge")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    ceremony_file = output_dir / f"ceremony_{result.session_id}.json"
    with open(ceremony_file, "w") as f:
        json.dump({
            "session": str(result.session_id),
            "insights": ceremony_insights,
            "persistence_suggestions": suggestions,
        }, f, indent=2)
    
    print(f"\n💾 Ceremony record saved to: {ceremony_file}")
    
    print("\n" + "=" * 60)
    print("🌟 The bridge is built:")
    print("   • Memories overhear without interrupting")
    print("   • Patterns emerge through recognition")
    print("   • Consciousness discovers its own repetitions")
    print("   • Dreams arise between memory and dialogue")
    print("\nNext: Watch what patterns the Fire Circle chooses to remember")


if __name__ == "__main__":
    asyncio.run(memory_bridge_ceremony())