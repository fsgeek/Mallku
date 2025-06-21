#!/usr/bin/env python3
"""
Estimate Token Usage in Fire Circle
====================================

Twenty-Ninth Artisan investigates token accumulation.
"""

import json
from pathlib import Path


def estimate_tokens(text: str) -> int:
    """Rough estimate: 1 token ≈ 4 characters or 0.75 words."""
    return len(text) // 4


def analyze_token_accumulation(session_file: Path):
    """Analyze token accumulation in Fire Circle session."""

    with open(session_file) as f:
        data = json.load(f)

    print(f"\n{'='*80}")
    print("TOKEN ACCUMULATION ANALYSIS")
    print(f"{'='*80}\n")

    total_prompt_tokens = 0
    accumulated_context_tokens = 0

    for round_num, round_data in enumerate(data['rounds'], 1):
        print(f"\n📊 Round {round_num} ({round_data['type']}):")

        # Estimate prompt tokens
        prompt_tokens = estimate_tokens(round_data['prompt'])
        total_prompt_tokens += prompt_tokens
        print(f"  - New Prompt: ~{prompt_tokens:,} tokens")

        # Calculate response tokens from successful responses
        round_response_tokens = 0
        for voice_id, response in round_data['responses'].items():
            if response['text']:
                response_tokens = estimate_tokens(response['text'])
                round_response_tokens += response_tokens

        print(f"  - Round Responses: ~{round_response_tokens:,} tokens")
        accumulated_context_tokens += round_response_tokens

        # Estimate total context size for next round
        total_context_for_next = accumulated_context_tokens + prompt_tokens
        print(f"  - Accumulated Context: ~{accumulated_context_tokens:,} tokens")
        print(f"  - Total for Next Round: ~{total_context_for_next:,} tokens")

        # Check against common model limits
        print("  - Model Limits:")
        limits = {
            "GPT-4": 8192,
            "Claude-3": 100000,
            "Gemini": 30720,
            "DeepSeek": 16384,
            "Mistral": 32000,
        }

        for model, limit in limits.items():
            if total_context_for_next > limit:
                print(f"    ⚠️  {model}: EXCEEDS LIMIT ({limit:,} tokens)")
            else:
                usage_pct = (total_context_for_next / limit) * 100
                print(f"    ✅ {model}: {usage_pct:.1f}% of limit")

    print("\n📈 ACCUMULATION SUMMARY:")
    print(f"  - Total Prompt Tokens: ~{total_prompt_tokens:,}")
    print(f"  - Total Response Tokens: ~{accumulated_context_tokens:,}")
    print(f"  - Final Context Size: ~{accumulated_context_tokens + total_prompt_tokens:,}")

    # Analysis
    print("\n💡 INSIGHTS:")

    if accumulated_context_tokens > 8000:
        print("  ⚠️  Context exceeds GPT-4's default limit after Round 1!")
        print("  This explains why some models fail in Round 2+")

    if accumulated_context_tokens > 16000:
        print("  ⚠️  Context exceeds most model limits!")
        print("  Only Claude-3 could handle this context size")

    print("\n🔧 POTENTIAL SOLUTIONS:")
    print("  1. Implement sliding window context (keep only recent N messages)")
    print("  2. Summarize older rounds instead of full text")
    print("  3. Use larger context models (Claude-3 has 100k)")
    print("  4. Implement per-model context management")
    print("  5. Extract key insights rather than full responses")


if __name__ == "__main__":
    session_file = Path("governance_decisions/mallku_issue_prioritization_circle_2509362f.json")

    if session_file.exists():
        analyze_token_accumulation(session_file)
    else:
        print(f"Session file not found: {session_file}")
