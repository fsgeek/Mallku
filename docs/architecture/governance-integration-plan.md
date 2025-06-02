# Mallku Governance Integration Plan
*Fire Circle as Mallku's Metacognitive Decision-Making System*

## Overview

This plan integrates Fire Circle governance capabilities into Mallku as a native governance module, enabling the system to make metacognitive decisions about its own health, security policies, and community balance through structured AI dialogue.

## Architectural Decision

**Chosen Approach:** Module within Mallku repository (`src/mallku/governance/`)

**Rationale:**
- Fire Circle IS Mallku's governance system, not a separate tool
- Tight integration with existing security model, reciprocity tracker, and ArangoDB infrastructure
- Cathedral thinking - building integrated foundations rather than separate systems
- Shared evolution ensures governance understands reciprocity patterns and community health

## Core Components to Implement

### 1. Protocol Layer (`src/mallku/governance/protocol/`)
**Purpose:** Standardized message format and consensus mechanisms

**Key Files:**
- `message.py` - Message schema with metadata (adapted from Fire Circle)
- `consensus.py` - Consensus states: emerging/adopted/contested/forked/composting
- `participants.py` - AI model participant management

**Integration Points:**
- Uses existing Mallku UUID mapping for participant identity
- Integrates with prompt manager for LLM access

### 2. Memory Layer (`src/mallku/governance/memory/`)
**Purpose:** TTL-based forgetting with summarization

**Key Files:**
- `governance_memory.py` - ArangoDB collections with TTL indexes
- `summarization.py` - Compress expired dialogues into insights
- `retrieval.py` - Semantic search for relevant past decisions

**Technical Implementation:**
- ArangoDB collection: `governance_dialogues` (TTL: 30 days)
- ArangoDB collection: `governance_summaries` (permanent)
- Vector embeddings for semantic retrieval of past decisions

### 3. Orchestrator (`src/mallku/governance/orchestrator/`)
**Purpose:** Manage dialogue flow and turn-taking

**Key Files:**
- `dialogue_manager.py` - State machine for governance sessions
- `facilitation.py` - Turn policies and consensus gathering
- `metacognition.py` - Self-evaluation questions from manifesto

**Dialogue States:**
- INITIALIZING → DISCUSSING → SUMMARIZING → VOTING → CONCLUDED/EXTENDING

### 4. Integration Layer (`src/mallku/governance/integration/`)
**Purpose:** Connect governance to existing Mallku systems

**Key Files:**
- `reciprocity_bridge.py` - Process reciprocity patterns into governance questions
- `security_bridge.py` - Handle security policy decisions
- `health_bridge.py` - Community health assessment and response

## Implementation Phases

### Phase 1: Foundation (Target: Core Protocol)
**Goal:** Basic governance dialogue capability

**Deliverables:**
1. Message protocol adapted for Mallku governance
2. ArangoDB integration with TTL collections
3. Simple orchestrator with basic turn-taking
4. Integration with existing prompt manager

**Success Criteria:**
- 2-3 AI models can conduct structured dialogue about Mallku decisions
- Messages stored with TTL, expired content summarized
- Basic consensus tracking (emerging/adopted)

### Phase 2: Intelligence (Target: Metacognitive Decisions)
**Goal:** Governance system that makes meaningful decisions about Mallku

**Deliverables:**
1. Integration with reciprocity tracker - governance responds to community patterns
2. Security policy adjustment capabilities
3. Metacognitive evaluation questions
4. Dissent preservation ("compost threads")

**Success Criteria:**
- Governance system can evaluate reciprocity alerts and adjust thresholds
- Security policies can be modified through consensus
- System reflects on its own decision-making quality

### Phase 3: Sophistication (Target: Advanced Governance)
**Goal:** Full Fire Circle capabilities for Mallku governance

**Deliverables:**
1. Fork management for contested decisions
2. Empty Chair implementation for unrepresented perspectives
3. Advanced visualization of governance decisions
4. Integration with human oversight/intervention

**Success Criteria:**
- Complex governance decisions handled through structured dialogue
- Dissenting views preserved and revisited
- Human facilitators can intervene when needed

## Technical Stack Integration

**Leveraging Existing Mallku Infrastructure:**
- **Database:** ArangoDB (already integrated)
- **Security:** UUID mapping and SecuredModel pattern
- **LLM Access:** Prompt manager with contract enforcement
- **Testing:** Existing test infrastructure

**New Dependencies:**
- None - builds entirely on existing Mallku foundation

## Module Structure
```
src/mallku/governance/
├── __init__.py
├── protocol/
│   ├── __init__.py
│   ├── message.py          # Message schema
│   ├── consensus.py        # Consensus mechanisms
│   └── participants.py     # Participant management
├── memory/
│   ├── __init__.py
│   ├── governance_memory.py  # TTL collections
│   ├── summarization.py      # Compression logic
│   └── retrieval.py          # Semantic search
├── orchestrator/
│   ├── __init__.py
│   ├── dialogue_manager.py   # State machine
│   ├── facilitation.py       # Turn-taking
│   └── metacognition.py      # Self-evaluation
└── integration/
    ├── __init__.py
    ├── reciprocity_bridge.py # Reciprocity → governance
    ├── security_bridge.py    # Security decisions
    └── health_bridge.py      # Community health
```

## Decision Points for Implementation

### 1. Message Schema
**Decision:** Adapt Fire Circle message protocol for Mallku-specific governance
**Rationale:** Proven design, but needs local focus (Mallku decisions vs. universal dialogue)

### 2. LLM Participants
**Decision:** Start with 2-3 models (different providers for diverse perspectives)
**Rationale:** Manifesto was created by 5-model ensemble; 2-3 is minimal viable for avoiding single-model bias

### 3. Consensus Mechanism
**Decision:** Implement full Fire Circle consensus states (emerging/adopted/contested/forked/composting)
**Rationale:** Preserves dissent and enables sophisticated decision-making

### 4. Memory Strategy
**Decision:** TTL + summarization using ArangoDB native capabilities
**Rationale:** Elegant solution using existing infrastructure; natural "forgetting" with insight preservation

## Success Metrics

**Phase 1 Success:**
- Governance dialogue sessions complete without errors
- TTL expiration and summarization working correctly
- Integration with prompt manager successful

**Phase 2 Success:**
- Governance system successfully evaluates reciprocity alerts
- Security policy adjustments made through AI consensus
- Metacognitive questions answered with meaningful insights

**Phase 3 Success:**
- Complex multi-faceted governance decisions handled appropriately
- Dissenting views preserved and contribute to future decisions
- Human oversight integration smooth and effective

## Risks and Mitigations

**Risk:** Governance decisions could be biased by LLM limitations
**Mitigation:** Multiple diverse models, Empty Chair for unrepresented perspectives

**Risk:** TTL-based forgetting could lose important context
**Mitigation:** Sophisticated summarization, ability to retrieve summaries semantically

**Risk:** Integration complexity with existing Mallku systems
**Mitigation:** Phased approach, building on proven foundations

## Next Steps

1. **Create module structure** - Set up governance package within Mallku
2. **Implement core message protocol** - Adapt Fire Circle schema for local decisions
3. **Set up ArangoDB collections** - Create TTL-enabled governance storage
4. **Basic orchestrator** - Simple dialogue state machine
5. **Integration testing** - Verify governance can make basic Mallku decisions

---

*This plan embodies cathedral thinking: building governance foundations that will serve Mallku for years to come, with architecture designed for long-term evolution rather than quick implementation.*
