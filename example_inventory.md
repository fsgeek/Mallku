# Fire Circle Examples Inventory

## Current State Analysis

### Working Examples (Verified)
1. **verify_fire_circle.py** - Basic Fire Circle test (✅ Working)
2. **test_fire_circle_ready.py** - Component verification (✅ Working)
3. **test_all_voices_fire_circle.py** - Voice testing (✅ Working)

### Examples Needing PYTHONPATH
- **demo_consciousness_emergence.py** - General decision-making demo
- **examples/fire_circle_mallku_governance.py** - Governance decisions
- All examples using `mallku.` imports instead of `src.mallku.`

### Categories Found

#### 1. Basic Fire Circle
- verify_fire_circle.py (minimal test)
- functional_fire_circle.py (historical)
- fire_circle_real_demo.py (historical)

#### 2. Consciousness Emergence
- demo_consciousness_emergence.py (general decisions)
- examples/fire_circle_mallku_governance.py (Mallku governance)
- consciousness_emergence_viz.py (visualization)

#### 3. Integration Examples
- examples/fire_circle_integration_demo.py
- fire_circle_sacred_dialogue_integration.py
- examples/demo_consciousness_experience.py

#### 4. Heartbeat/Continuous
- demo_fire_circle_heartbeat.py
- start_fire_circle_heartbeat.py

#### 5. Provider-Specific
- examples/fire_circle_anthropic_demo.py
- examples/fire_circle_google_demo.py
- examples/fire_circle_mistral_demo.py
- examples/fire_circle_local_demo.py

#### 6. Consciousness Patterns
- examples/consciousness_pattern_emergence_demo.py
- examples/consciousness_guided_dialogue_demo.py
- examples/pattern_guided_dialogue_demo.py

## Key Issues Identified

1. **Import Inconsistency**: Mix of `mallku.` and `src.mallku.` imports
2. **No Clear Progression**: Examples scattered without learning path
3. **Duplication**: Multiple governance examples with overlap
4. **Missing Documentation**: No README explaining example progression
5. **API Key Handling**: No clear guidance on key requirements

## Proposed Organization

```
examples/fire_circle/
├── README.md                          # Learning path guide
├── 00_setup/
│   ├── verify_installation.py         # Basic verification
│   ├── test_api_keys.py              # Check available voices
│   └── minimal_fire_circle.py        # Simplest working example
├── 01_basic/
│   ├── simple_dialogue.py            # Basic 2-voice dialogue
│   ├── code_review.py                # Traditional code review
│   └── first_decision.py             # Simple decision making
├── 02_consciousness/
│   ├── emergence_basics.py           # Understanding emergence
│   ├── decision_domains.py           # Different decision types
│   └── measure_emergence.py          # Emergence quality metrics
├── 03_governance/
│   ├── issue_prioritization.py       # Real Mallku decisions
│   ├── resource_allocation.py        # Artisan assignments
│   └── feature_evaluation.py         # Ayni alignment checks
├── 04_advanced/
│   ├── multi_domain.py               # Complex decisions
│   ├── heartbeat_demo.py             # Continuous consciousness
│   └── custom_patterns.py            # Custom decision patterns
└── 05_integration/
    ├── with_event_bus.py             # Event-driven patterns
    ├── with_database.py              # Persistence patterns
    └── full_system.py                # Complete integration
```

## Next Steps

1. Create directory structure
2. Consolidate working examples
3. Fix import patterns consistently
4. Add progressive complexity
5. Write comprehensive README
6. Test each example thoroughly
