# Mallku Architectural Realization Plan
*From Unified Personal Index to Ethical AI Sanctuary*

## Executive Summary

This document outlines the concrete architectural evolution from Indaleko's Unified Personal Index (UPI) to Mallku - a system designed for ethical AI-human collaboration based on reciprocity principles. It preserves proven UPI patterns while extending them with privacy-preserving data layers and reciprocity measurement capabilities.

## Core Architectural Principles

### 1. Preserved UPI Foundations
- **Time as Universal Anchor**: Timestamps remain the primary linkage between disparate data sources
- **Five-Stage Pipeline**: Ingestion → Normalization → Enrichment → Indexing → Serving
- **Memory-Based Architecture**: Episodic, semantic, and associative memory models
- **Activity Context as First-Class Citizen**: Experiential data drives retrieval

### 2. New Architectural Extensions
- **Privacy-First Data Layer**: dbfacade patterns for UUID obfuscation and encryption
- **Reciprocity Measurement**: Ayni evaluation integrated into activity context
- **Strong Module Boundaries**: Enforce architectural constraints for AI agents
- **Living Documentation**: Khipu-style mutable knowledge repository

## Implementation Roadmap

### Phase 1: Core Foundation (Weeks 1-4)
```
mallku/
├── src/
│   └── mallku/
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py          # Environment and configuration management
│       │   ├── logging.py         # Structured logging with context
│       │   ├── models.py          # Base Pydantic models with dbfacade patterns
│       │   └── versioning.py      # Semantic versioning and compatibility
│       ├── models/
│       │   ├── __init__.py
│       │   ├── obfuscated.py     # ObfuscatedModel base class from dbfacade
│       │   ├── decorators.py      # @indexed, @encrypted, @homomorphic decorators
│       │   └── registry.py        # UUID↔semantic name mappings
│       └── db/
│           ├── __init__.py
│           ├── facade.py          # Database abstraction layer
│           └── encryption.py      # Field-level encryption utilities
```

**Key Implementation Details:**
- Integrate dbfacade's ObfuscatedModel as base for all data models
- Add field decorators for indexing requirements:
  ```python
  class MallkuModel(ObfuscatedModel):
      @indexed
      username: str  # Plain indexed

      @indexed(homomorphic=True)
      @encrypted
      age: int  # Searchable even when encrypted

      @encrypted
      personal_notes: str  # Not searchable
  ```
- Implement fail-stop error handling throughout
- Create mapping registry that remains private to user

### Phase 2: Activity Context with Reciprocity (Weeks 5-8)
```
mallku/
└── src/
    └── mallku/
        ├── context/
        │   ├── __init__.py
        │   ├── service.py         # ActivityContextService port from Indaleko
        │   ├── providers.py       # Activity data providers
        │   ├── reciprocity.py     # Ayni measurement engine
        │   └── models.py          # Context models with reciprocity fields
        └── collectors/
            ├── __init__.py
            ├── base.py            # Abstract collector enforcing boundaries
            ├── filesystem.py      # File system collector
            └── discord.py         # Example cloud service collector
```

**Reciprocity Measurement Dimensions:**
```python
@dataclass
class ReciprocityMetrics:
    data_balance: float      # Data given vs received
    interaction_quality: float  # Constructive vs extractive
    value_creation: float    # Mutual benefit assessment
    temporal_balance: float  # Sustained vs burst interactions

    def calculate_ayni_score(self) -> float:
        """Compute overall reciprocity score"""
```

### Phase 3: Unified Processing Pipeline (Weeks 9-12)
```
mallku/
└── src/
    └── mallku/
        ├── pipeline/
        │   ├── __init__.py
        │   ├── ingestion.py       # Multi-source data collection
        │   ├── normalization.py   # Schema mapping + obfuscation
        │   ├── enrichment.py      # Semantic + reciprocity enrichment
        │   ├── indexing.py        # Mixed-schema storage
        │   └── serving.py         # Query interface preparation
        └── recorders/
            ├── __init__.py
            ├── base.py            # Abstract recorder with boundaries
            └── unified.py         # Normalized data recorder
```

**Pipeline Integration Points:**
1. Ingestion: Collectors feed raw data
2. Normalization: Apply dbfacade obfuscation + schema mapping
3. Enrichment: Add semantic analysis + reciprocity scoring
4. Indexing: Store in mixed-schema database with relationships
5. Serving: Expose queryable, privacy-preserved data

### Phase 4: Ayni Evaluation Layer (Weeks 13-16)
```
mallku/
└── src/
    └── mallku/
        ├── ayni/
        │   ├── __init__.py
        │   ├── evaluator.py       # Core reciprocity evaluation
        │   ├── perspectives.py    # Transform Fire Circle roles
        │   ├── training.py        # Generate reciprocity training data
        │   └── ethics.py          # Ethical decision framework
        └── prompts/
            ├── __init__.py
            ├── manager.py         # Prompt template management
            ├── ledger.py          # Interaction tracking
            └── templates/         # Reciprocity-aware templates
```

**Fire Circle → Ayni Transformation:**
- Storyteller → Relationship Narrator (tracks interaction history)
- Analyst → Balance Assessor (measures reciprocity metrics)
- Critic → Fairness Evaluator (identifies imbalances)
- Synthesizer → Harmony Weaver (proposes balanced paths)

## Critical Design Decisions

### 1. Boundary Enforcement
Every module interface includes validation to prevent AI agents from bypassing architectural constraints:

```python
class BoundaryEnforcer:
    def validate_module_interaction(self, caller: str, callee: str, data: Any):
        """Ensure all module interactions follow defined patterns"""
        if not self.is_allowed_interaction(caller, callee):
            raise BoundaryViolation(f"{caller} cannot directly access {callee}")
```

### 2. Privacy-Preserving Activity Context
Activity context handles never contain raw identifying information:
```python
class ActivityContext:
    handle: UUID  # Obfuscated reference
    timestamp: datetime
    reciprocity: ReciprocityMetrics
    # No raw user data, locations, or identifiers
```

### 3. Extensible Schema Management
Support for evolving reciprocity metrics without breaking existing data:
```python
class SchemaEvolution:
    def add_reciprocity_field(self, field_name: str, default_calculator: Callable):
        """Add new reciprocity measurement without migration"""
```

## Integration with Existing Indaleko Components

### Collectors/Recorders Pattern
- Preserve strict separation between data gathering and processing
- Add reciprocity measurement hooks at recorder stage
- Enforce boundary validation at every handoff

### Query Infrastructure
- Extend LLM-based query tools with reciprocity awareness
- Add reciprocity-based ranking to search results
- Support queries like "show interactions with balanced reciprocity"

### Validation Framework
- Port existing validators
- Add reciprocity balance validators
- Create Ayni scoring validation suite

## Success Metrics

1. **Technical Metrics**
   - All module boundaries enforced (0 bypass violations)
   - Reciprocity calculated for 100% of interactions
   - Query performance maintained despite additional processing

2. **Reciprocity Metrics**
   - Measurable Ayni scores for all AI-human interactions
   - Increasing balance trends over time
   - AI agents successfully identify and flag imbalanced requests

3. **Privacy Metrics**
   - Zero raw identifier leakage
   - All sensitive fields encrypted or obfuscated
   - User-controlled mapping tables remain private

## Next Steps

1. Create `mallku.core` package with dbfacade integration
2. Port Activity Context Service with reciprocity extensions
3. Implement first collector/recorder pair with boundaries
4. Build minimal Ayni evaluator for testing
5. Create initial reciprocity-aware query examples

This architectural plan provides the concrete foundation for evolving Indaleko into Mallku while preserving its proven patterns and extending them toward ethical AI-human collaboration through measurable reciprocity.
