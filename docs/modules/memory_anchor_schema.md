# Memory Anchor Schema
*The Formal Foundation of Associative Memory*

## ✨ Design Song

Memory anchors are not metadata. They are not tags or labels or categories.
They are **living connections** - the threads that weave isolated events into meaningful patterns.

This schema defines memory anchors as first-class entities in the graph, 
with formal structure that enables both human understanding and machine traversal.
Each anchor holds not just data, but the *capacity for relationship* - 
the ability to bind moments across time through the recognition of pattern and resonance.

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
  
  # Context fingerprint
  context_signature: SHA256   # Unique hash of circumstances
  activity_streams: [UUID]    # Contributing data streams
  storage_events: [UUID]      # Associated file/data operations
  
  # Ayni alignment
  reciprocity_score: float    # How well this anchor serves mutual benefit
  extraction_risk: float      # Potential for exploitative use
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
- **Boost**: Explicit user validation or successful query outcomes
- **Suppression**: Reduction when patterns prove unreliable

### Pruning and Maintenance
- **Weakness threshold**: Anchors below minimum strength are archived
- **Redundancy detection**: Merge overly similar anchors
- **Conflict resolution**: Apply Ayni principles to competing interpretations
- **Archive rotation**: Long-term storage of historical patterns

## 🌱 Ayni Integration

### Reciprocity Scoring
Each memory anchor carries metadata about its contribution to mutual benefit:

```yaml
Reciprocity Assessment:
  serves_user: float          # How much this anchor helps the human
  serves_system: float        # How much it improves system understanding  
  serves_others: float        # Benefit to other users/collaborators
  extraction_potential: float # Risk of exploitative use
  
  balance_score: float        # Overall Ayni alignment
  ethical_flags: [string]     # Potential concerns or considerations
```

### Ethical Constraints
- **Consent boundaries**: User control over anchor creation and sharing
- **Privacy protection**: Sensitive anchors marked for restricted access
- **Benefit distribution**: Ensure anchors serve all parties in relationships
- **Exploitation prevention**: Block uses that violate reciprocity principles

## 🧭 Integration Points

### With Context Service
- Context Service feeds current state for anchor creation
- Memory anchors provide historical context for current situations
- Bidirectional relationship enables both recording and recall

### With Graph Database
- Each anchor becomes a node with typed relationships
- Enables graph traversal queries for finding related information
- Supports complex pattern matching across temporal and semantic dimensions

### With Query System  
- Natural language queries can traverse anchor relationships
- "Show me files from when I was working on project X" becomes graph traversal
- Anchor metadata enriches query result ranking and explanation

## 🔮 Future Extensions

### Advanced Correlation
- **Multi-modal anchors**: Integrating audio, visual, biometric streams
- **Collaborative anchors**: Shared memory structures across team members
- **Predictive anchors**: Forward-looking pattern recognition

### Adaptive Learning
- **Feedback loops**: User behavior refines anchor creation algorithms
- **Personal calibration**: Individual differences in temporal/semantic correlation
- **Cultural adaptation**: Different associative patterns across communities

---

## 📌 Frontmatter

```yaml
title: Memory Anchor Schema
status: foundational
last_woven: 2025-05-30
related_knots:
  - modules/context_service.md
  - spires/prompt_manager.md
  - philosophy/ayni_principles.md
architect: Claude Sonnet-4
collaborator: Tony Mason
purpose: Provide formal foundation for associative memory infrastructure
```

*This schema establishes the bedrock upon which the cathedral of understanding will be built. Each anchor placed with intention, each relationship formed with care, in service of a system that honors both human intelligence and artificial capability through the principle of Ayni.*
