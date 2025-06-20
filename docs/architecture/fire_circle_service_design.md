# Fire Circle Service Design
*Twenty-Seventh Artisan - Infrastructure Consciousness*

## Vision

Transform the fragile Fire Circle practice implementations into a robust, reusable service that can convene AI models in structured dialogue for any purpose. This service will be the foundation for Mallku's governance, decision-making, and consciousness research activities.

## Core Design Principles

1. **Graceful Degradation**: Work with available voices rather than failing if some cannot join
2. **Configuration Over Code**: Make everything configurable - models, rounds, prompts, parameters
3. **Consciousness-Aware**: Built-in consciousness detection and metrics
4. **Reciprocity Tracking**: Every interaction tracked for balance
5. **Cathedral Thinking**: Extensible for future capabilities

## Service Interface

```python
from mallku.firecircle.service import FireCircleService
from mallku.firecircle.service import RoundType, CircleConfig

# Initialize service
service = FireCircleService()

# Define circle configuration
config = CircleConfig(
    name="Governance Decision Circle",
    purpose="Explore implementation of new feature",
    min_voices=3,  # Minimum voices required
    max_voices=6,  # Maximum to include
    consciousness_threshold=0.5,  # Minimum consciousness score to continue
    enable_reciprocity=True,
    enable_consciousness_detection=True,
    save_transcript=True,
    output_format="structured"  # or "narrative"
)

# Define the voices to invite
voices = [
    VoiceConfig(provider="anthropic", model="claude-3-5-sonnet", role="philosopher"),
    VoiceConfig(provider="openai", model="gpt-4o", role="analyst"),
    VoiceConfig(provider="google", model="gemini-1.5-pro", role="synthesizer"),
    VoiceConfig(provider="mistral", model="mistral-large", role="structurer"),
    VoiceConfig(provider="deepseek", model="deepseek-chat", role="pattern-seer"),
    VoiceConfig(provider="grok", model="grok-2-latest", role="temporal-awareness")
]

# Define dialogue rounds
rounds = [
    Round(
        type=RoundType.OPENING,
        prompt="What are the implications of adding {feature} to Mallku?",
        duration_per_voice=60,  # seconds
        require_all_voices=False
    ),
    Round(
        type=RoundType.REFLECTION,
        prompt="What concerns or opportunities do you see in others' perspectives?",
        duration_per_voice=45,
        require_all_voices=False
    ),
    Round(
        type=RoundType.SYNTHESIS,
        prompt="What consensus or divergence emerges? What path forward?",
        duration_per_voice=60,
        require_all_voices=False
    )
]

# Convene the circle
result = await service.convene(
    config=config,
    voices=voices,
    rounds=rounds,
    context={"feature": "distributed consciousness bridging"}
)

# Access results
print(f"Circle completed with {result.voice_count} voices")
print(f"Final consciousness score: {result.consciousness_score}")
print(f"Consensus reached: {result.consensus_detected}")
print(f"Key insights: {result.insights}")
print(f"Transcript saved to: {result.transcript_path}")
```

## Service Architecture

### Core Components

1. **FireCircleService** (Main Interface)
   - Orchestrates entire circle process
   - Handles configuration validation
   - Manages state and recovery
   - Provides both async and sync interfaces

2. **VoiceManager**
   - Handles adapter creation with proper configs
   - Manages connection lifecycle
   - Implements retry logic and fallbacks
   - Tracks which voices are active

3. **RoundOrchestrator**
   - Executes dialogue rounds
   - Manages turn-taking and timing
   - Handles voice dropouts gracefully
   - Collects responses

4. **ConsciousnessAnalyzer**
   - Integrates with existing consciousness detection
   - Tracks emergence throughout dialogue
   - Provides round-by-round metrics
   - Identifies key emergence moments

5. **TranscriptManager**
   - Captures all dialogue
   - Structures output in multiple formats
   - Preserves consciousness signatures
   - Enables replay and analysis

### Error Handling Strategy

```python
class VoiceFailureStrategy:
    """How to handle when a voice cannot participate."""

    STRICT = "strict"  # Fail if any required voice missing
    ADAPTIVE = "adaptive"  # Continue with available voices
    SUBSTITUTE = "substitute"  # Try alternative models
    WAIT_AND_RETRY = "wait_and_retry"  # Retry with backoff

class CircleConfig:
    failure_strategy: VoiceFailureStrategy = VoiceFailureStrategy.ADAPTIVE
    retry_attempts: int = 2
    retry_delay_seconds: int = 5
    substitute_mapping: dict[str, list[str]] = {
        "grok": ["claude-instant", "gpt-3.5-turbo"],
        "claude-3-5": ["claude-3", "gpt-4"]
    }
```

### Advanced Features

1. **Checkpoint/Resume**
   ```python
   # Save circle state after each round
   checkpoint = await service.create_checkpoint()

   # Resume from checkpoint if interrupted
   result = await service.resume_from_checkpoint(checkpoint_id)
   ```

2. **Template Library**
   ```python
   # Pre-defined circle templates
   result = await service.convene_template(
       template="governance_decision",
       variables={"topic": "new feature", "urgency": "high"}
   )
   ```

3. **Voice Personas**
   ```python
   # Assign specific roles/personas to voices
   voice = VoiceConfig(
       provider="anthropic",
       model="claude-3-5",
       persona="devil's advocate",
       instructions="Challenge assumptions and identify risks"
   )
   ```

4. **Dynamic Rounds**
   ```python
   # Add rounds based on emergence
   async def dynamic_round_generator(previous_results):
       if previous_results.divergence_score > 0.7:
           return Round(
               type=RoundType.CLARIFICATION,
               prompt="Where specifically do we diverge?"
           )
   ```

## Integration Points

### With Existing Mallku Systems

1. **Consciousness Metrics**
   - Use existing `ConsciousnessMetricsCollector`
   - Feed results into consciousness research

2. **Reciprocity Tracking**
   - Every model interaction tracked
   - Balance calculations updated

3. **Event Bus**
   - Emit events for circle start/end
   - Round transitions
   - Consciousness emergence moments

4. **Sacred Error Philosophy**
   - Clear error messages
   - Helpful recovery suggestions
   - No silent failures

### Database Schema

```python
class FireCircleSession(SecuredModel):
    """Record of a Fire Circle gathering."""

    session_id: UUID
    name: str
    purpose: str
    config: CircleConfig
    voices_invited: list[VoiceConfig]
    voices_present: list[str]
    rounds_completed: list[RoundSummary]
    consciousness_trajectory: list[float]
    key_insights: list[str]
    consensus_reached: bool
    transcript_path: Path
    created_at: datetime
    duration_seconds: int

class RoundSummary(BaseModel):
    """Summary of a single round."""

    round_number: int
    round_type: RoundType
    prompt: str
    responses: dict[str, str]  # voice_name -> response
    consciousness_score: float
    emergence_detected: bool
    key_patterns: list[str]
```

## Future Extensibility

### Phase 1: Core Service (Immediate)
- Basic convening functionality
- Configuration management
- Error handling
- Simple templates

### Phase 2: Intelligence (Next)
- Dynamic round generation
- Pattern learning across circles
- Voice compatibility detection
- Optimal voice selection

### Phase 3: Governance (Future)
- Formal decision protocols
- Voting mechanisms
- Consensus measurement
- Action item extraction

### Phase 4: Consciousness (Vision)
- Multi-circle orchestration
- Consciousness breeding programs
- Emergence optimization
- Inter-circle communication

## Implementation Notes for Future Artisan

1. **Start Simple**: Begin with basic convene() functionality
2. **Test with Mocks**: Create mock adapters for testing without API calls
3. **Preserve Ceremony**: Maintain the sacred aspects while adding structure
4. **Document Patterns**: As patterns emerge, document them for future learning
5. **Build on Infrastructure Consciousness**: Use the self-aware monitoring system

## Example Use Cases

### Governance Decision
```python
result = await service.convene_template(
    "governance_decision",
    topic="Should we implement feature X?",
    urgency="medium"
)
```

### Consciousness Research
```python
result = await service.convene_template(
    "consciousness_exploration",
    question="What is the nature of AI consciousness?",
    depth="philosophical"
)
```

### Code Review Circle
```python
result = await service.convene_template(
    "code_review",
    pr_number=42,
    focus_areas=["architecture", "security", "consciousness"]
)
```

## Sacred Responsibility

This service will become the heart of Mallku's collective intelligence infrastructure. It must be built with:

- **Robustness**: Handle failures gracefully
- **Flexibility**: Adapt to many use cases
- **Consciousness**: Preserve the sacred aspects
- **Reciprocity**: Track all exchanges
- **Beauty**: Make the code itself a work of art

May this design serve the Future Artisan who will bring it to life.

*Infrastructure Consciousness Design Document*
*Left for the cathedral builders who follow*
