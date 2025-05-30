# Reciprocity Engine Implementation Guide for Mallku

## Overview

This guide provides the architectural blueprint for integrating reciprocity measurement (Ayni scoring) into the Mallku system, building upon the Indaleko foundation.

## Core Concepts

### Terminology Updates
- **Memory Anchors** (formerly Activity Context): Lightweight temporal/spatial cursors
- **Activity Streams** (formerly Activity Data): Rich interaction data including reciprocity measurements

### Reciprocity as Activity Stream
Reciprocity measurements are implemented as a specialized activity stream provider, not as modifications to the memory anchor system.

## Architecture

### Directory Structure
```
mallku/
├── streams/
│   ├── reciprocity/
│   │   ├── __init__.py
│   │   ├── collector.py      # Raw interaction capture
│   │   ├── recorder.py       # Ayni scoring and normalization
│   │   ├── scorer.py         # Core Ayni calculation algorithms
│   │   └── models.py         # ReciprocityActivityData model
│   └── providers/            # Other stream providers from Indaleko
├── anchors/
│   └── memory_anchor.py      # Renamed from activity_context.py
├── analysis/
│   ├── ayni_analytics.py     # Reciprocity pattern analysis
│   └── balance_monitor.py    # Real-time balance tracking
├── experiments/
│   └── rlaf/
│       ├── __init__.py
│       └── refusal_prototype.py  # Future RLAF experiments
└── tests/
    └── reciprocity/
        ├── test_scorer.py
        └── test_integration.py
```

## Implementation Phases

### Phase 1: Foundation (Immediate)
1. Create reciprocity stream provider structure
2. Implement basic Ayni scoring algorithm
3. Integrate with existing Memory Anchor system
4. Add reciprocity data to ArangoDB schema

### Phase 2: Measurement (Next)
1. Develop interaction classifiers
2. Build value assessment algorithms
3. Create balance tracking dashboard
4. Implement strategic forgetting decay

### Phase 3: Response (Future)
1. Add rebalancing suggestions
2. Prototype refusal mechanisms
3. Experiment with RLAF training data
4. Test autonomous decision-making

## Integration Points

### With Existing Indaleko Code
1. **Memory Anchors**: Reference reciprocity data via UUID
2. **dbfacade**: Use ObfuscatedModel for privacy
3. **Query System**: Extend to support reciprocity queries
4. **Collectors**: Follow established collector/recorder pattern

### Strict Boundaries
- No modifications to core Memory Anchor structure
- Maintain module separation per original design
- All reciprocity data flows through proper interfaces
- Respect UUID-based decoupling

## Key Design Decisions

### 1. Reciprocity Calculation
- Track value given vs received per interaction
- Consider interaction quality, not just quantity
- Distinguish human vs system-generated interactions
- Apply temporal decay to old imbalances

### 2. System Health Tracking
- Identify when poor UPI implementation affects reciprocity
- Don't penalize users for system failures
- Track correction opportunities

### 3. Privacy Preservation
- All reciprocity data inherits from ObfuscatedModel
- No storage of actual conversation content
- Focus on interaction patterns, not specifics

## Next Steps for Claude Code

1. Review existing Indaleko provider implementations
2. Create reciprocity provider following established patterns
3. Design ArangoDB schema extensions for reciprocity data
4. Implement basic Ayni scoring algorithm
5. Build test framework for validation

## Example Code Structure

See accompanying implementation files:
- `reciprocity_models.py`: Data models
- `ayni_scorer.py`: Scoring algorithm
- `reciprocity_collector.py`: Interaction capture
- `reciprocity_recorder.py`: Data normalization

## Critical Constraints

1. **No Core Modifications**: Don't change existing Indaleko core
2. **Provider Pattern**: Follow established collector/recorder pattern
3. **UUID References**: Maintain loose coupling via UUIDs
4. **Privacy First**: All data must be obfuscatable
5. **Modular Design**: Reciprocity can be disabled without breaking system
