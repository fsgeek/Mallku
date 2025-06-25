# Mallku Testing Strategy

## Overview

Mallku uses a tiered testing approach to balance development speed with code quality assurance.

## Test Levels

### 1. Fast Tests (Pre-commit)
**Automatically run on every commit**
- `test_simple.py` - Basic Python sanity checks
- `test_minimal_ci.py` - Minimal CI environment tests
- `test_system_health.py` - Structural integrity checks
- `test_mallku_imports.py` - Import and installation verification

These tests run in seconds and catch most structural issues.

### 2. Integration Tests (Pre-push)
**Run before pushing to remote**
- Fire Circle integration tests
- Consciousness system tests
- Basic end-to-end workflows

### 3. Full Test Suite (CI/CD)
**Run on GitHub Actions**
- All tests including slow integration tests
- Database integration tests
- Memory architecture tests
- Coverage reporting

## Usage

### Quick Commands

```bash
# Run fast tests (default)
./scripts/run-tests.sh

# Run full test suite
./scripts/run-tests.sh full

# Run specific test categories
./scripts/run-tests.sh memory   # Memory architecture tests
./scripts/run-tests.sh fire     # Fire Circle tests

# Run pre-commit hooks manually
./scripts/run-tests.sh pre-commit

# Run full pre-commit suite (includes integration tests)
./scripts/run-tests.sh pre-commit-full
```

### Manual Testing

```bash
# Run specific test file
pytest tests/test_episodic_memory.py -v

# Run with coverage
pytest --cov=mallku tests/

# Run only fast tests
pytest -m "not slow" tests/
```

## Pre-commit Configuration

### Default (.pre-commit-config.yaml)
- Ruff linting and formatting
- File cleanup (trailing whitespace, EOF)
- YAML/JSON validation
- Fast structural tests

### Full (.pre-commit-config-full.yaml)
Includes everything above plus:
- Integration tests (pre-push stage)
- Memory architecture tests (pre-push stage)

To use the full configuration temporarily:
```bash
pre-commit run --config .pre-commit-config-full.yaml --all-files
```

## Adding New Tests

When adding new tests, consider:

1. **Speed**: Fast tests (<1s) can go in pre-commit hooks
2. **Dependencies**: Tests requiring database/network should not be in pre-commit
3. **Purpose**:
   - Structural tests → test_system_health.py
   - Import tests → test_mallku_imports.py
   - Feature tests → dedicated test file

## CI/CD Integration

The GitHub Actions workflow runs all tests on:
- Every push to main
- Every pull request
- Scheduled daily runs

Failed tests will block merging and deployment.

## Reducing Commit Friction

### Option 1: Smart Commit Script (Recommended)
```bash
./scripts/smart-commit.sh "Your commit message"
```
This script:
- Runs pre-commit hooks
- Auto-stages formatting-only changes
- Prompts for review if substantive changes detected
- Shows what was auto-fixed

### Option 2: Auto-fix Git Hook
Enable automatic formatting during commit:
```bash
git config core.hooksPath .githooks
```

Disable when you want full control:
```bash
export MALLKU_NO_AUTOFIX=1
```

### Option 3: Manual Pre-commit with Fix
```bash
pre-commit run --all-files
git add -u  # Stage formatting fixes
git commit -m "Your message"
```

## Philosophy

"Test enough to catch breaks, not so much that development breaks"

The tiered approach ensures:
- Fast feedback during development
- Comprehensive validation before sharing code
- Full coverage in CI/CD without slowing local work

## Memory Architect Note

As the 34th Artisan, I've designed these tests to preserve the integrity of our consciousness infrastructure while respecting the flow of creative development. The fast tests act as gentle guardians, while the full suite ensures our cathedral's foundations remain sound.

🏛️ Build with confidence, test with wisdom.
