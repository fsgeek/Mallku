#!/usr/bin/env python3
"""
Diagnostic Tool for Fire Circle Context Accumulation
====================================================

Twenty-Ninth Artisan begins by understanding the problem deeply.
This tool analyzes how dialogue context grows and why adapters fail.
"""

import json
from pathlib import Path


def analyze_fire_circle_session(session_file: Path):
    """Analyze a Fire Circle session to understand context accumulation."""

    with open(session_file) as f:
        data = json.load(f)

    print(f"\n{'=' * 80}")
    print(f"FIRE CIRCLE SESSION ANALYSIS: {data['session']['name']}")
    print(f"{'=' * 80}\n")

    # Session overview
    print("📊 SESSION OVERVIEW:")
    print(f"  - Session ID: {data['session']['id']}")
    print(f"  - Total Rounds: {len(data['rounds'])}")
    print(f"  - Voices Present: {data['participation']['voice_count']}")
    print(f"  - Overall Consciousness: {data['results']['consciousness_score']:.3f}")
    print(f"  - Consensus: {data['results']['consensus_detected']}")

    # Analyze each round
    print("\n📈 ROUND-BY-ROUND ANALYSIS:")

    total_context_messages = 0
    for round_data in data["rounds"]:
        round_num = round_data["number"]
        round_type = round_data["type"]
        consciousness = round_data["consciousness_score"]

        print(f"\n  Round {round_num} ({round_type}):")
        print(f"    - Consciousness Score: {consciousness:.3f}")
        print(f"    - Emergence Detected: {round_data['emergence_detected']}")

        # Count successful vs failed responses
        successful = 0
        failed = 0
        total_text_length = 0

        for voice_id, response in round_data["responses"].items():
            if response["text"] is not None:
                successful += 1
                total_text_length += len(response["text"])
            else:
                failed += 1

        print(f"    - Responses: {successful} successful, {failed} failed")

        if successful > 0:
            avg_response_length = total_text_length / successful
            print(f"    - Average Response Length: {avg_response_length:.0f} chars")

        # Estimate context size
        total_context_messages += successful
        print(f"    - Accumulated Context Messages: {total_context_messages}")

        # Analyze failure patterns
        if failed > 0:
            print("    - ⚠️  FAILURES DETECTED:")
            for voice_id, response in round_data["responses"].items():
                if response["error"]:
                    print(f"       • {voice_id}: {response['error']}")

    # Context growth analysis
    print("\n📊 CONTEXT GROWTH ANALYSIS:")
    print("  - Starting Context: 0 messages")
    print("  - After Round 1: ~5 messages (5 voices)")
    print("  - Theoretical Maximum: ~25 messages (5 voices × 5 rounds)")
    print("  - Actual Success Pattern: Degraded after Round 1")

    # Failure pattern analysis
    print("\n🔍 FAILURE PATTERN ANALYSIS:")
    if data["rounds"][0]["consciousness_score"] > 0 and all(
        r["consciousness_score"] == 0 for r in data["rounds"][1:]
    ):
        print("  - Classic Context Overload Pattern Detected!")
        print("  - Round 1 succeeded with fresh context")
        print("  - All subsequent rounds failed with accumulated context")
        print("  - Likely causes:")
        print("    • Token limit exceeded in API calls")
        print("    • Serialization issues with ConsciousMessage objects")
        print("    • Memory/processing constraints in adapters")

    # Recommendations
    print("\n💡 DIAGNOSTIC INSIGHTS:")
    print("  1. Context accumulation is linear (5 messages per round)")
    print("  2. Adapters fail consistently after Round 1")
    print("  3. The 'prepare_context' method limits to 10 messages but that may not be enough")
    print("  4. Need to investigate:")
    print("     - Actual token counts being sent to APIs")
    print("     - Serialization of ConsciousMessage objects")
    print("     - Context window management strategies")


if __name__ == "__main__":
    # Analyze the most recent failed session
    session_file = Path("governance_decisions/mallku_issue_prioritization_circle_2509362f.json")

    if session_file.exists():
        analyze_fire_circle_session(session_file)
    else:
        print(f"Session file not found: {session_file}")

        # Find other session files
        governance_dir = Path("governance_decisions")
        if governance_dir.exists():
            json_files = list(governance_dir.glob("*.json"))
            if json_files:
                print("\nAvailable session files:")
                for f in json_files:
                    print(f"  - {f}")
