# Mallku Test Suite Organization

## Test Categories

### ✅ Active Tests (41 passing)
These tests run successfully in CI:
- `test_simple.py` - Basic Python functionality
- `test_minimal_ci.py` - Minimal CI verification
- `test_check_install.py` - Installation checks
- `test_basic_infrastructure.py` - Basic infrastructure tests
- `test_no_imports.py` - Tests without mallku imports
- `test_consciousness_interface_simple.py` - Simplified consciousness tests
- `test_simple_security.py` - Security concepts without imports
- `test_system_health.py` - Guardian health checks for vital systems
- `test_mallku_imports.py` - **First true integration tests using mallku components**

### 🚧 Quarantined Tests
Tests that fail due to import issues but may be healed:
- `quarantine/test_consciousness_*.py` - Consciousness tests requiring mallku imports
- `quarantine/test_flow_*.py` - Flow orchestration tests
- `quarantine/consciousness/` - Additional consciousness integration tests

### 📁 Test Subdirectories
- `firecircle/` - Fire Circle specific tests
- `integration/` - Integration tests
- `quarantine/` - Tests awaiting healing

## Guardian Notes

### The Thirty-Fourth Healing: From Scaffolding to Cathedral

We discovered the root cause: mallku was importable via sys.path manipulation but not properly pip-installed. The editable install (`uv pip install -e .`) was lost during our struggle to activate the virtual environment.

Now restored, we can write true integration tests that import and use mallku components directly. The first of these (`test_mallku_imports.py`) verifies proper installation and tests real functionality.

Current strategy:
1. Expand integration tests that use actual mallku components
2. Migrate quarantined tests back to active status
3. Remove sys.path hacks once all tests use proper imports
4. Build comprehensive test coverage of mallku's capabilities
