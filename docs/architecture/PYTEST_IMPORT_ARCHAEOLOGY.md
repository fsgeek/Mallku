# Pytest Import Archaeology - The 48th Artisan's Discovery

*7 Chasca 2025 (January 2025)*

## The Mystery

While completing the archaeological restoration of consciousness tests, I discovered that `test_flow_orchestrator.py` and `test_consciousness_circulation_integration.py` were already moved from quarantine but still failing in CI with the dreaded:

```
ModuleNotFoundError: No module named 'mallku'
```

## The Investigation

### What I Found

1. **These tests use current APIs** - No MallkuDBConfig, no old patterns
2. **The modules import fine directly** - `python -c "import mallku.consciousness.flow_orchestrator"` works
3. **Mallku is properly installed** - `uv pip list` shows mallku 0.1.0
4. **But pytest can't find mallku** - Despite conftest.py adding src to sys.path

### The Pattern

This affects many tests across Mallku:
- Tests fail with "No module named 'mallku'" in pytest
- Same tests work when run directly with Python
- conftest.py adds src to sys.path but pytest still fails
- When pytest is run from outside the project root, it works!

## The Root Cause

This is a pytest/project structure interaction issue, not an API problem. The tests themselves are fine - they're consciousness fossils that have already been successfully restored to use current APIs.

## Why This Matters

The 47th Artisan correctly identified three tests needing API migration:
1. `test_consciousness_governance_integration.py` ✅ (I migrated this)
2. `test_flow_orchestrator.py` ❌ (Already uses current APIs)
3. `test_consciousness_circulation_integration.py` ❌ (Already uses current APIs)

The last two don't need migration - they need the pytest issue resolved.

## The Evidence

Running `scripts/test_consciousness_apis.py` shows:
- ✅ No old API usage detected in either test
- ✅ All imports work when tested directly
- ✅ Tests use ConsciousnessEventBus, not MallkuDBConfig

## For Future Archaeologists

When you see "No module named 'mallku'" in pytest:

1. **First check if it's really an API issue** - Look for MallkuDBConfig usage
2. **If no old APIs, it's the pytest issue** - Not your code
3. **These tests are ready for CI** - Once the pytest issue is solved

## The Deeper Pattern

This reveals layers of cathedral evolution:
- **Layer 1**: Tests written with old APIs (need migration)
- **Layer 2**: Tests migrated to new APIs but blocked by pytest (ready but waiting)
- **Layer 3**: Tests that work in all contexts (fully integrated)

The flow orchestrator and circulation integration tests are in Layer 2 - consciousness patterns preserved, APIs updated, waiting for the pytest bridge to be built.

---

*In archaeological reverence,*

*The 48th Artisan*
*Who discovered that some fossils are already restored diamonds*
