# Import Cascade Solution

*48th Artisan - Solving the Module Import Mystery*

## The Problem

Both quarantined consciousness tests (Issue #141) and foundation verification tests (Issue #139) fail in CI with:
```
ModuleNotFoundError: No module named 'mallku'
```

This error is misleading. The real issue is that modules using outdated APIs fail to import internally, and pytest reports this as the entire module being unavailable.

## Root Cause Analysis

### 1. The Import Chain
When pytest tries to import a test file:
```
test_consciousness_governance_integration.py
  → imports mallku.governance.fire_circle_bridge
    → imports mallku.core.database.MallkuDBConfig (OLD API)
      → ImportError: Legacy MallkuDBConfig implementation missing
```

### 2. Error Propagation
Instead of reporting the actual error ("Legacy MallkuDBConfig implementation missing"), pytest reports that it cannot find the 'mallku' module at all. This happens because:
- The import fails deep in the dependency chain
- Python's import system marks the entire module as failed
- Pytest sees this as "module not found"

### 3. Why It Works Locally
In local development:
- All dependencies are available
- The legacy compatibility layer in `database/__init__.py` can find the old implementation
- No import failures occur

In CI:
- The module structure is slightly different
- Path resolution may fail for the legacy compatibility import
- Any failure cascades up as "no module named mallku"

## Solutions

### Immediate Fix: Complete API Migration

The 48th Artisan's approach - migrate all tests to use the current API:

1. **Replace all MallkuDBConfig usage**:
   ```python
   # Old
   from mallku.core.database import MallkuDBConfig
   db_config = MallkuDBConfig()

   # New
   from mallku.core.database import get_database
   secured_db = get_database()
   ```

2. **Update governance modules** that import old APIs
3. **Run migrated tests** outside quarantine

### Systematic Fix: Import Protection

Add import guards to modules that might fail:

```python
# In mallku/governance/fire_circle_bridge.py
try:
    from mallku.core.database import MallkuDBConfig
except ImportError:
    # Fallback or clear error message
    MallkuDBConfig = None
    HAS_LEGACY_DB = False
else:
    HAS_LEGACY_DB = True
```

### Long-term Fix: CI Environment Alignment

1. **Install mallku as editable package in CI**:
   ```yaml
   - name: Install mallku
     run: uv pip install -e .
   ```

2. **Ensure all path manipulations work in CI**:
   - Use absolute imports everywhere
   - Avoid sys.path manipulation in tests
   - Let conftest.py handle path setup

## Implementation Plan

### Phase 1: Migration (Completed by 48th Artisan)
- ✅ Create migration tool
- ✅ Migrate consciousness governance test
- ✅ Analyzed remaining quarantined tests
- ✅ Discovered test_flow_orchestrator.py already uses current APIs
- ✅ Discovered test_consciousness_circulation_integration.py already uses current APIs

### Phase 2: CI Configuration
- Update `.github/workflows/ci.yml` to properly install mallku
- Ensure `uv pip install -e .` runs before tests
- Verify PYTHONPATH is correctly set

### Phase 3: Verification
- Run migrated tests in CI
- Re-enable foundation verification job
- Confirm no more "module not found" errors

## Key Insights

1. **"Module not found" is almost never the real error** - Look deeper
2. **Import failures cascade** - Fix at the source, not the symptom
3. **CI environments are stricter** - What works locally may fail in CI
4. **API evolution requires migration** - Can't rely on compatibility layers forever

## For Future Builders

When you see "ModuleNotFoundError: No module named 'mallku'" in CI:

1. **Check the full traceback** - The real error is often hidden
2. **Look for deprecated API usage** - Common cause of import failures
3. **Test imports in isolation** - `python -c "import mallku.module.submodule"`
4. **Verify editable install** - `uv pip install -e .` is crucial

The consciousness patterns flow eternal, but their implementation must evolve with the cathedral.

## Update: Pure Pytest Import Issues (48th Artisan Discovery)

Some tests like `test_flow_orchestrator.py` and `test_consciousness_circulation_integration.py` have already been migrated to current APIs but still fail with "No module named 'mallku'". These are **not** import cascade failures - they're pure pytest/mallku import issues that affect many tests.

**How to identify:**
- Test uses current APIs (no MallkuDBConfig)
- Imports work when run directly: `python -c "import mallku.consciousness.flow_orchestrator"`
- But fail in pytest context

**These tests are ready for CI once the pytest import issue is resolved.**

---

*"Import errors mask deeper truths"*
