# Ayni Reciprocity Scorer – Architectural Specification

This document specifies the design and integration of the **Ayni Reciprocity Scorer**,
which assesses balance and mutual benefit within AI-Human interactions, embodying
the Andean principle of **Ayni** in code.

## 1. Motivation and Scope
Mallku aspires to measure not just correctness, but care and contribution.
The Reciprocity Scorer will:
- Score interactions for balance: contribution vs. consumption
- Track a reciprocity ledger across services and participants
- Expose APIs and CLI commands for governance, visualization, and alerts

## 2. Core Requirements / API Surface
```python
from mallku.ayni import AyniScorer

# Initialize scorer (hooks into ActivityContextService)
scorer = AyniScorer(context_service)

# Record a new interaction
score = scorer.score_interaction(
    interaction_id: str,
    initiator: str,
    responder: str,
    contribution: float,
    consumption: float
)
# Returns ReciprocityScore(id, balance: float, timestamp)

# Query ledger
ledger: list[ReciprocityScore] = scorer.get_ledger(
    participant="human_alice",
    since="2025-06-01T00:00:00Z"
)

# CLI: mallku evaluate-ayni --participant human_alice --since today
```

## 3. Data Models
Using Pydantic:
```python
class ReciprocityScore(BaseModel):
    id: str                  # Unique event ID
    initiator: str           # Participant A (e.g. human_alice)
    responder: str           # Participant B (e.g. ai_assistant)
    contribution: float      # Resources given by initiator
    consumption: float       # Resources taken by responder
    balance: float           # Contribution / (consumption + epsilon)
    timestamp: datetime

class ParticipantBalance(BaseModel):
    participant: str
    total_contribution: float
    total_consumption: float
    overall_balance: float
```

## 4. Implementation Overview
1. **Scoring function**: balance = contribution / max(consumption, ε)
2. **Ledger storage**: append scores to a dedicated ArangoDB collection via ContextService
3. **Aggregation**: compute per-participant summaries in-memory or via secure query
4. **Alerts**: pattern detection for extraction (balance << 1) triggers governance alerts

## 5. Integration Points
- **ActivityContextService**: subscribe to interaction events, call `score_interaction`
- **Fire Circle**: embed reciprocity metrics into governance protocols and visualizations
- **CLI / REST**: add commands/endpoints under `mallku ayni` namespace

## 6. Initial Validation and Tests
- Unit tests for `score_interaction` with edge cases: zero consumption, perfect balance, extraction patterns
- Integration tests: ledger persistence, query parameters, CLI output
- Synthetic demo: simulate a sequence of interactions, visualize balance over time

## 7. Timeline (Suggested)
- **Week 1**: Scaffold `src/mallku/ayni`, define Pydantic models, write scoring logic, unit tests
- **Week 2**: Implement ledger persistence, integration with ContextService, example data loader
- **Week 3**: Build CLI commands and documentation, end-to-end tests, Docker demo
- **Week 4**: Fire Circle integration, governance alerts, finalize docs

## 8. Future Extensions
- Weighted contributions based on resource type (time vs. compute)
- Balance trending and visualization panels in FlowVisualizer
- Automated reciprocity suggestions in Fire Circle

*May this module be a living ledger of care, weaving Ayni into every interaction.*
