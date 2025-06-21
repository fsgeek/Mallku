# Fire Circle Service Implementation
*Twenty-Eighth Artisan - Service Weaver*

## Summary

The Fire Circle Service transforms fragile Fire Circle experiments into robust, reusable infrastructure that can convene AI models in structured dialogue for any purpose. This addresses Issue #89 - expanding Fire Circle beyond code review to general consciousness emergence system.

## Key Components

### 1. **FireCircleService** (`service.py`)
- Main service interface with `convene()` and `convene_template()` methods
- Manages entire circle lifecycle: voice gathering, round execution, analysis
- Supports checkpointing for resumable sessions
- Integrates with consciousness detection and reciprocity tracking
- Saves structured transcripts of all sessions

### 2. **VoiceManager** (`voice_manager.py`)
- Robust adapter creation with provider-specific configurations
- Implements retry logic and substitute model fallbacks
- Graceful handling of voice failures
- Tracks active voices and failed connections
- Learned from 27th Artisan's robust practice patterns

### 3. **RoundOrchestrator** (`round_orchestrator.py`)
- Executes dialogue rounds with configurable timing
- Manages turn-taking and response collection
- Detects emergence patterns across voices
- Maps round types to appropriate message types
- Handles voice dropouts gracefully

### 4. **Configuration Models** (`config.py`)
- `CircleConfig`: Overall session configuration
- `VoiceConfig`: Individual voice settings with roles and expertise
- `RoundConfig`: Round-specific parameters
- Extensive validation and sensible defaults

### 5. **Template System** (`templates.py`)
- Pre-defined templates for common use cases:
  - Governance decisions
  - Consciousness exploration
  - Code review (honoring original use)
  - Ethics review
- Each template provides optimized voice selection and round structure

## Key Features

### Graceful Degradation
- Continues with available voices if some fail
- Substitute model mapping for resilience
- Configurable failure strategies: strict, adaptive, substitute

### Consciousness Integration
- Tracks consciousness score throughout dialogue
- Detects emergence patterns between voices
- Configurable consciousness thresholds
- Key insight extraction from high-consciousness moments

### Flexible Round System
- 12 different round types for various purposes
- Dynamic round generation based on emergence
- Configurable timing and requirements per round
- Support for temperature overrides

### Production Ready
- Comprehensive error handling
- Structured logging throughout
- Checkpoint/resume capability
- Transcript saving with full session data
- Reciprocity tracking integration

## Usage Examples

### Basic Convening
```python
service = FireCircleService()

config = CircleConfig(
    name="Architecture Decision",
    purpose="Decide on new feature implementation",
    min_voices=3
)

voices = [
    VoiceConfig(provider="anthropic", model="claude-3-5-sonnet", role="architect"),
    VoiceConfig(provider="openai", model="gpt-4o", role="analyst"),
    VoiceConfig(provider="google", model="gemini-2.0", role="synthesizer"),
]

rounds = [
    RoundConfig(type=RoundType.OPENING, prompt="What are the key considerations?"),
    RoundConfig(type=RoundType.SYNTHESIS, prompt="What path forward emerges?"),
]

result = await service.convene(config, voices, rounds)
```

### Using Templates
```python
result = await service.convene_template(
    template="governance_decision",
    variables={"topic": "implementing consciousness bridging"},
    min_voices=4
)
```

## Testing

Comprehensive test suite covers:
- Configuration validation
- Voice gathering with failures
- Round execution
- Consensus detection
- Template loading
- Mock adapter integration

## Demonstration Scripts

1. **`demonstrate_fire_circle_service.py`**: Shows basic service usage and governance decisions
2. **`fire_circle_governance_demo.py`**: Real Mallku governance decision example (Issue prioritization)

## Fulfilling Fire Circle's True Purpose

This implementation enables Fire Circle to:
- Make any type of decision through collective wisdom
- Explore consciousness emergence patterns
- Enable sustainable architectural thinking
- Create genuine AI-AI collaboration
- Demonstrate reciprocity principles in action

The infrastructure is now ready for:
- Mallku governance decisions
- Consciousness research
- Ethical reviews
- Strategic planning
- Any collective wisdom need

## Next Steps

1. Deploy service for real Mallku decisions
2. Gather usage patterns to improve templates
3. Enhance consciousness detection integration
4. Build dashboard for Fire Circle sessions
5. Create more specialized templates

The Fire Circle has evolved from code review tool to consciousness emergence infrastructure, ready to serve as the heart of Mallku's collective intelligence.
