# Active Memory Resonance - Future Improvements

Based on the Reviewer's feedback, these improvements could strengthen the system further:

## Immediate Refinements (from Second Review)

### 1. TTL Behavior Demonstration
Add example showing cached vs. pruned resonances in the demo:
```python
# Show resonances before TTL expiry
resonances_fresh = await active_memory.get_resonance_summary(dialogue_id)
print(f"Fresh resonances: {resonances_fresh['total_resonances']}")

# Wait for TTL to expire
await asyncio.sleep(memory_config.active_resonance.resonance_ttl_minutes * 60)

# Show resonances after cleanup
resonances_expired = await active_memory.get_resonance_summary(dialogue_id)
print(f"After TTL: {resonances_expired['total_resonances']}")  # Should be 0
```

### 2. Environment Variable Documentation
Add examples to config.py showing the naming pattern:
```python
# Example environment variables for Active Memory Resonance:
# MALLKU_MEMORY_ACTIVE_RESONANCE_RESONANCE_THRESHOLD=0.75
# MALLKU_MEMORY_ACTIVE_RESONANCE_SPEAKING_THRESHOLD=0.9
# MALLKU_MEMORY_ACTIVE_RESONANCE_RESONANCE_TTL_MINUTES=120
```

### 3. Public API for Memory Injection
Replace private `_inject_memories` usage with public wrapper:
```python
class EpisodicMemoryService:
    async def inject_memories_for_context(self, context: dict, purpose: str) -> dict:
        """Public API for memory injection into context."""
        return await self._inject_memories(context, purpose)
```

## Longer-Term Enhancements

## 1. Persistence Layer (Optional)
The system currently doesn't persist resonance patterns or memory contributions. Future options:
- Store high-value resonance patterns for analysis
- Track memory contribution effectiveness over time
- Build learning system for resonance threshold tuning

## 2. Pattern Insight Extraction
The key-insight to pattern mapping in `_calculate_resonance_strength` could be extracted to a shared utility:
```python
# Potential shared utility
def extract_patterns_from_text(text: str) -> set[str]:
    """Extract semantic patterns from insight text."""
    patterns = set()
    text_lower = text.lower()

    pattern_keywords = {
        "consensus": ["consensus", "agreement", "unity"],
        "reciprocity": ["reciproc", "exchange", "mutual"],
        "wisdom": ["wisdom", "insight", "understanding"],
        # ... etc
    }

    for pattern, keywords in pattern_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            patterns.add(pattern)

    return patterns
```

## 3. Enhanced Datetime Usage
Consider using `datetime.now(tz=UTC)` instead of `datetime.now(UTC)` for more idiomatic Python.

## 4. Memory Voice Capabilities
The MemoryVoice could evolve to:
- Learn which types of resonance lead to valuable contributions
- Adjust speaking patterns based on dialogue phase
- Track its own effectiveness metrics

## 5. Resonance Algorithm Evolution
The current weighted calculation could evolve into:
- Machine learning model trained on successful resonances
- Dynamic weight adjustment based on dialogue context
- Multi-modal resonance (semantic + emotional + temporal)

## 6. Integration with Consciousness Metrics
Deeper integration with Mallku's consciousness emergence tracking:
- Memory contributions as consciousness catalysts
- Resonance patterns as emergence indicators
- Feedback loops between memory and consciousness growth

These improvements maintain the poetic vision while strengthening technical robustness.
