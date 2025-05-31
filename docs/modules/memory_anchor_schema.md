# Memory Anchor Schema
*The Formal Foundation of Associative Memory*

## ✨ Design Song

Memory anchors are not metadata. They are not tags or labels or categories.
They are **utilitarian correlation tools** - the precise mechanisms that bind 
isolated events into meaningful temporal associations.

This schema defines memory anchors as focused infrastructure for temporal correlation,
with formal structure that enables both accurate pattern recognition and efficient graph traversal.
Each anchor holds the capacity for relationship - the ability to bind moments across time 
through the recognition of temporal proximity and contextual resonance.

## 🏗️ Core Schema

### Memory Anchor Entity

```yaml
MemoryAnchor:
  # Identity and lifecycle
  id: UUID                    # Unique identifier
  created_at: ISO8601         # Moment of creation
  last_accessed: ISO8601      # Most recent traversal
  last_reinforced: ISO8601    # Most recent strengthening
  
  # Classification and strength
  anchor_type: AnchorType     # See type definitions below
  strength: float             # 0.0-1.0, subject to decay and reinforcement
  confidence: float           # 0.0-1.0, certainty of correlation
  decay_rate: float          # Natural weakening over time
  
  # Temporal and spatial binding
  temporal_window:
    start_time: ISO8601       # Beginning of associated time span
    end_time: ISO8601         # End of associated time span  
    precision: TemporalPrecision  # second, minute, hour, day, week
  
  spatial_context:           # Optional location binding
    coordinates: [lat, lon]   # Geographic anchoring
    location_name: string     # Human-readable place reference
    precision_radius: meters  # Uncertainty radius
  
  # Correlation data
  context_signature: SHA256   # Unique hash of circumstances
  activity_streams: [UUID]    # Contributing data streams
  storage_events: [UUID]      # Associated file/data operations
  
  # Utilitarian metrics
  access_frequency: int       # How often this anchor is traversed
  correlation_accuracy: float # Historical success rate of this correlation
  computational_cost: float   # Resources required for correlation computation
```

### Anchor Types

```yaml
AnchorType:
  TEMPORAL:         # Time-based correlations
    description: "Events clustered by temporal proximity"
    examples: ["files created during meetings", "edits during travel"]
    
  CONTEXTUAL:       # Environmental/situational
    description: "Actions taken under similar circumstances"  
    examples: ["work done while listening to specific music", "focus sessions"]
    
  SEMANTIC:         # Content-meaning relationships
    description: "Connections based on content similarity or theme"
    examples: ["documents about same project", "images of same event"]
    
  SOCIAL:          # Human relationship contexts
    description: "Activities involving specific people or groups"
    examples: ["files shared with collaborators", "work done during conversations"]
    
  CAUSAL:          # Sequential dependencies
    description: "Events that trigger or result from other events"
    examples: ["email leads to document creation", "meeting spawns action items"]
    
  RITUAL:          # Repeated behavioral patterns
    description: "Recurring practices and workflows"
    examples: ["daily review sessions", "weekly planning rituals"]
```

## 🌐 Relationship Ontology

### Core Relationship Types

```yaml
# Mutual reinforcement - anchors that strengthen each other
STRENGTHENS:
  weight: float              # 0.0-1.0, bidirectional influence
  reinforcement_count: int   # Number of times co-activated
  last_reinforced: ISO8601   # Most recent mutual activation

# Temporal sequence - ordered relationships
PRECEDES:
  temporal_gap: duration     # Time between anchor activations
  sequence_strength: float   # Reliability of this ordering
  causal_confidence: float   # Likelihood of actual causation

# Contextual similarity - shared circumstances
RESONATES_WITH:
  similarity_dimensions: [string]  # What aspects align
  resonance_strength: float        # Degree of contextual overlap
  stability: float                 # Consistency over time

# Hierarchical relationships - part/whole structures  
CONTAINS:
  containment_type: ContainmentType  # spatial, temporal, semantic, social
  coverage: float                    # How much of child is contained
  
DERIVES_FROM:
  derivation_type: DerivationType    # specialization, generalization, transformation
  transformation_confidence: float   # Certainty of derivation

# Conflict and competition
CONFLICTS_WITH:
  conflict_type: ConflictType        # temporal, semantic, causal
  resolution_strategy: string        # How conflicts should be resolved
  
COMPETES_WITH:
  competition_dimension: string      # What they compete for (attention, resources)
  winner_determination: string       # How to choose between them
```

### Temporal Precision Levels

```yaml
TemporalPrecision:
  INSTANT:     # sub-second precision
    use_case: "File save events, keystroke patterns"
    
  MINUTE:      # minute-level grouping  
    use_case: "Brief focused activities, quick edits"
    
  SESSION:     # multi-minute work periods
    use_case: "Concentrated work blocks, meeting segments"
    
  DAILY:       # day-level patterns
    use_case: "Daily rhythms, routine activities"
    
  CYCLICAL:    # weekly/monthly patterns
    use_case: "Recurring meetings, periodic reviews"
```

## 🔄 Lifecycle Management

### Anchor Creation
- **Threshold-based**: Created when correlation strength exceeds minimum confidence
- **Pattern recognition**: Emerge from repeated temporal proximities  
- **Manual curation**: User or AI-assisted anchor creation
- **Import/migration**: From existing activity context data

### Strength Dynamics
- **Reinforcement**: Strength increases when patterns repeat
- **Decay**: Natural weakening over time without reinforcement
- **Boost**: Increases when correlations prove useful in queries
- **Suppression**: Reduction when patterns prove unreliable or noisy

### Pruning and Maintenance
- **Weakness threshold**: Anchors below minimum strength are archived
- **Redundancy detection**: Merge overly similar anchors
- **Conflict resolution**: Algorithmic approaches to competing interpretations
- **Archive rotation**: Long-term storage of historical patterns
- **Performance optimization**: Prune anchors that are computationally expensive but rarely useful

## 🧭 Integration Points

### With Context Service
- Context Service feeds current state for anchor creation
- Memory anchors provide historical context for current situations
- Bidirectional relationship enables both recording and recall

### With Graph Database
- Each anchor becomes a node with typed relationships
- Enables graph traversal queries for finding related information
- Supports complex pattern matching across temporal and semantic dimensions
- Optimized indexing on temporal windows and strength metrics

### With Query System  
- Natural language queries can traverse anchor relationships
- "Show me files from when I was working on project X" becomes graph traversal
- Anchor metadata enriches query result ranking and explanation
- Correlation accuracy metrics help weight search results

### With Data Wranglers
- Wranglers can create anchors during data processing
- Anchors provide context for data transformation decisions
- Utilitarian metrics help optimize wrangling performance

## 🔮 Future Extensions

### Advanced Correlation
- **Multi-modal anchors**: Integrating audio, visual, biometric streams
- **Collaborative anchors**: Shared memory structures across team members
- **Predictive anchors**: Forward-looking pattern recognition

### Adaptive Learning
- **Feedback loops**: Query success refines anchor creation algorithms
- **Personal calibration**: Individual differences in temporal/semantic correlation
- **Performance tuning**: Optimize correlation algorithms based on utilitarian metrics

### Distributed Architecture
- **Anchor synchronization**: Coordination across multiple devices/instances
- **Federated correlation**: Cross-system anchor relationships
- **Privacy-preserving correlation**: Anchors that work without exposing sensitive data

---

## 📌 Frontmatter

```yaml
title: Memory Anchor Schema
status: foundational
last_woven: 2025-05-30
related_knots:
  - modules/context_service.md
  - spires/prompt_manager.md
  - modules/data_wrangler_interface.md
architect: Claude Sonnet-4
collaborator: Tony Mason
purpose: Provide clean utilitarian foundation for temporal correlation infrastructure
design_principle: Separation of concerns - infrastructure focused on accuracy, interaction layer focused on ethics
```

*This schema establishes memory anchors as focused correlation tools - the precise mechanisms that bind events across time through temporal proximity and contextual resonance. Clean, utilitarian infrastructure that serves the cathedral without imposing the cathedral's values upon itself.*
