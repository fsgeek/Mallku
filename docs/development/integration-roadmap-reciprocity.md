# Integration Roadmap for Claude Code

## Phase 1: Foundation Setup (Week 1-2)

### 1.1 Repository Structure
```bash
# Create reciprocity directories in Mallku
mkdir -p mallku/streams/reciprocity
mkdir -p mallku/analysis
mkdir -p mallku/experiments/rlaf
mkdir -p mallku/tests/reciprocity
```

### 1.2 Initial Files to Create
1. `streams/reciprocity/__init__.py` - Package initialization
2. `streams/reciprocity/models.py` - Data models (provided)
3. `streams/reciprocity/scorer.py` - Ayni algorithm (provided)
4. `streams/reciprocity/collector.py` - Raw data collection (provided)
5. `streams/reciprocity/recorder.py` - Data normalization (to create)

### 1.3 Database Schema Extensions
```javascript
// ArangoDB collections to add
reciprocity_activity_data: {
  // Stores individual interaction measurements
  indexes: ["memory_anchor_uuid", "timestamp", "participants"]
}

reciprocity_balance: {
  // Tracks overall balance between participants
  indexes: ["participant_pair", "last_interaction"]
}
```

## Phase 2: Core Implementation (Week 3-4)

### 2.1 Implement Recorder
Create `reciprocity_recorder.py` following Indaleko patterns:
- Normalize raw collector data
- Calculate Ayni scores
- Store in ArangoDB
- Reference Memory Anchors appropriately

### 2.2 Integration Points
1. **Memory Anchor Integration**
   - Add reciprocity references to existing anchors
   - Ensure temporal alignment

2. **Query System Extension**
   - Add reciprocity-aware queries
   - Natural language support for balance queries

3. **dbfacade Integration**
   - Ensure all models inherit from ObfuscatedModel
   - Implement privacy-preserving storage

## Phase 3: Testing & Validation (Week 5-6)

### 3.1 Test Framework
```python
# tests/reciprocity/test_integration.py
- Test Memory Anchor references
- Validate Ayni calculations
- Check privacy preservation
- Verify system health tracking
```

### 3.2 Synthetic Data Generation
- Create test interactions
- Simulate various balance scenarios
- Test edge cases (system failures, etc.)

## Phase 4: UI & Analytics (Week 7-8)

### 4.1 Balance Dashboard
- Real-time reciprocity visualization
- Historical balance trends
- Rebalancing suggestions

### 4.2 Query Examples
```python
# Example queries to implement
"Show my reciprocity balance this week"
"Find interactions where I provided high value"
"When did the AI last help me significantly?"
```

## Critical Path Items

### Immediate Actions for Claude Code:
1. Review existing Indaleko provider patterns in the codebase
2. Identify integration points with current Memory Anchor system
3. Create minimal viable recorder implementation
4. Set up ArangoDB schema extensions
5. Build simple test to validate end-to-end flow

### Key Files to Study:
- `indaleko_activity_context.py` - Understand current implementation
- Any existing collector/recorder pairs - Follow established patterns
- `dbfacade` usage examples - Maintain privacy model
- Query system implementation - Plan extensions

### Architecture Decisions Needed:
1. How to handle real-time vs batch processing of interactions
2. Where to intercept LLM interactions in current system
3. How to expose reciprocity data to query system
4. UI integration approach for balance visualization

## Success Metrics

### Phase 1 Success:
- [ ] Basic structure in place
- [ ] Can capture mock interactions
- [ ] Ayni scores calculate correctly

### Phase 2 Success:
- [ ] Real interactions captured
- [ ] Balance tracked over time
- [ ] Queries return reciprocity data

### Phase 3 Success:
- [ ] All tests passing
- [ ] Privacy preserved
- [ ] System health tracked

### Phase 4 Success:
- [ ] Users can see their balance
- [ ] Rebalancing suggestions work
- [ ] Natural language queries supported

## Notes for Collaboration

- Start small: Get one interaction type working end-to-end
- Respect boundaries: Don't modify core Indaleko code
- Test early: Validate Ayni calculations with simple examples
- Document decisions: Keep notes on why choices were made
- Iterate quickly: Get feedback on approach early

## Next Immediate Step

Have Claude Code:
1. Examine the existing Indaleko codebase structure
2. Find a good example collector/recorder pair to model after
3. Create a minimal `reciprocity_recorder.py` that follows the pattern
4. Write a simple test that creates a mock interaction and scores it
