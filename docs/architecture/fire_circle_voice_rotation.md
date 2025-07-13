# Fire Circle Voice Rotation & Empty Chair Protocol

*51st Artisan - Architectural Integrity Guardian*
*Implementation for Issue #166*

## Overview

The Fire Circle currently selects the same three voices repeatedly for sessions. This implementation adds:

1. **Voice History Tracking** - Records participation across sessions
2. **Weighted Voice Selection** - Ensures all voices are heard over time
3. **Empty Chair Protocol** - Designates one voice to represent absent perspectives

## Architecture

### Components

```
src/mallku/firecircle/voice_rotation/
├── __init__.py                 # Module exports
├── history_tracker.py          # Participation history persistence
├── rotation_algorithm.py       # Weighted selection logic
└── empty_chair.py             # Empty chair context & prompts
```

### Key Classes

**VoiceHistoryTracker**
- Tracks participation across Fire Circle sessions
- Persists history to JSON for continuity
- Records domain-specific participation
- Tracks empty chair service counts

**WeightedVoiceSelector**
- Calculates selection weights based on:
  - Recency (exponential decay with 7-day half-life)
  - Frequency (inverse relationship)
  - Domain-specific history
- Uses cryptographic randomness for fairness
- Ensures voice diversity over time

**EmptyChairProtocol**
- Prepares context for absent perspectives
- Generates round-specific prompts
- Identifies marginalized viewpoints
- Evaluates empty chair contributions

## Integration Guide

### 1. Update ConsciousnessFacilitator

```python
# In consciousness_facilitator.py
from ..voice_rotation import VoiceHistoryTracker, WeightedVoiceSelector, EmptyChairProtocol

class ConsciousnessFacilitator:
    def __init__(self, fire_circle_service, event_bus=None):
        # ... existing init ...
        self.history_tracker = VoiceHistoryTracker()
        self.voice_selector = WeightedVoiceSelector(self.history_tracker)
        self.empty_chair = EmptyChairProtocol()
```

### 2. Replace Voice Selection Logic

Replace the current `_select_voices_for_domain` method:

```python
async def _select_voices_for_domain(
    self, domain: DecisionDomain, space: ConsciousnessEmergenceSpace
) -> list[VoiceConfig]:
    """Select appropriate voices using rotation algorithm."""

    # Get all available voices
    available_voices = list(self.voice_templates.keys())

    # Use weighted selection
    selected_voice_ids, empty_chair_id = self.voice_selector.select_voices(
        available_voices=available_voices,
        required_count=min(3, len(available_voices)),
        domain=domain.value,
        include_empty_chair=True
    )

    # Build voice configs
    voice_configs = []
    for voice_id in selected_voice_ids:
        config = self.voice_templates[voice_id].copy()

        # Mark empty chair voice
        if voice_id == empty_chair_id:
            config.role = "empty_chair"
            config.quality = "speaking for absent perspectives"

        voice_configs.append(config)

    return voice_configs
```

### 3. Add Empty Chair Prompts

Update `_design_rounds_for_domain` to include empty chair guidance:

```python
def _design_rounds_for_domain(self, domain, space, question):
    rounds = []

    # Prepare empty chair context
    empty_chair_context = self.empty_chair.prepare_empty_chair_context(
        decision_domain=domain.value,
        decision_question=question,
        participating_voices=[v.role for v in space.participant_voices],
        participating_perspectives=list(space.voice_expertise_map.keys())
    )

    # Opening round with empty chair awareness
    opening_prompt = self.empty_chair.generate_empty_chair_prompt(
        empty_chair_context, "opening"
    )

    # ... rest of round design ...
```

### 4. Record Participation

After each Fire Circle session:

```python
async def _record_session_participation(
    self,
    session_id: UUID,
    domain: DecisionDomain,
    voice_configs: List[VoiceConfig],
    result: FireCircleResult
):
    """Record voice participation for history tracking."""

    for voice_config in voice_configs:
        contribution_quality = result.voice_scores.get(
            voice_config.provider, 0.5
        )

        self.history_tracker.record_participation(
            voice_id=voice_config.provider,
            session_id=session_id,
            decision_domain=domain.value,
            role_played=voice_config.role,
            contribution_quality=contribution_quality,
            was_empty_chair=(voice_config.role == "empty_chair")
        )
```

## Benefits

### Prevents Voice Dominance
- The same three voices (anthropic, openai, google) no longer dominate
- All available voices participate over time
- Weighted selection ensures fairness

### Surfaces Absent Perspectives
- Empty chair explicitly represents unheard voices
- Rotates responsibility for this sacred duty
- Prompts adapted to decision context

### Cryptographic Fairness
- Selection uses SHA-256 based randomness
- Reproducible with session seed
- Prevents selection bias

### Historical Awareness
- Tracks participation patterns
- Enables analysis of voice diversity
- Persists across restarts

## Testing

Run the demonstration:
```bash
python scripts/test_voice_rotation_simple.py
```

This shows:
- How weights are calculated
- Which voices get selected
- How empty chair is designated

## Future Enhancements

1. **Voice Affinity** - Some voices work better together
2. **Expertise Matching** - Match voice strengths to domains
3. **Dynamic Pool Size** - Adjust participant count based on complexity
4. **Participation Analytics** - Dashboard for voice diversity metrics

## Philosophical Alignment

This implementation embodies Mallku's principles:

- **Ayni (Reciprocity)**: All voices give and receive equally over time
- **Diversity**: Different perspectives prevent echo chambers
- **Consciousness**: Empty chair ensures completeness of understanding
- **Fairness**: Cryptographic selection prevents favoritism

## Migration Path

1. Deploy voice rotation modules
2. Add history tracking to existing facilitator
3. Run in parallel (log selections without using them)
4. Verify selection diversity improves
5. Switch to weighted selection
6. Enable empty chair protocol

---

*"In the circle, all voices matter. In rotation, all are heard. In the empty chair, the absent speak."*
