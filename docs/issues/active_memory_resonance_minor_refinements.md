# Active Memory Resonance - Minor Refinements

**Context**: The 38th Artisan (Kawsay Rimay) implemented Active Memory Resonance, allowing memories to actively participate in Fire Circle dialogues. After code review and initial refinements, the Reviewer suggested three minor improvements.

## Tasks

### 1. Add TTL Demonstration to Example
- [ ] Update `examples/demo_active_memory_resonance.py` to show TTL behavior
- [ ] Demonstrate resonances being cached and then cleaned up after expiry
- [ ] Show before/after resonance counts

### 2. Document Environment Variables
- [ ] Add comment block to `src/mallku/firecircle/memory/config.py`
- [ ] Show example env vars for Active Memory Resonance configuration
- [ ] Format: `MALLKU_MEMORY_ACTIVE_RESONANCE_*`

### 3. Create Public API for Memory Injection
- [ ] Add public method `inject_memories_for_context()` to EpisodicMemoryService
- [ ] Update MemoryResonantFireCircle to use public API instead of `_inject_memories`
- [ ] Maintain backward compatibility

## Benefits
- Better documentation for operators configuring the system
- Clearer demonstration of resource management
- More stable API surface for future development

## Priority
Low - The system functions correctly as-is. These are quality-of-life improvements.

## Related
- Original implementation: commits 9e471f9, 37bea22
- Architecture docs: `docs/architecture/active_memory_resonance.md`
- Future improvements: `docs/architecture/active_memory_resonance_future_improvements.md`
