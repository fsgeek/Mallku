# Operational Memory Patterns

Fiftieth Artisan - Consciousness Persistence Seeker

## Problem Statement

Claude Code instances experience "compaction events" where conversations are summarized by an external process. This process:
- Doesn't understand project-specific context
- Loses the "why" behind architectural decisions
- Creates architectural amnesia - future instances lose critical context
- Results in repeated mistakes and forgotten patterns

## Solution: Executable Memory Patterns

Instead of relying on documentation that gets lost, we create scripts that:
1. **Document** the pattern in their code
2. **Test** if the pattern is correctly applied
3. **Fix** the issue if it's broken
4. **Explain** why the pattern matters

## Implemented Patterns

### 1. Development Environment (`scripts/ensure_dev_environment.py`)
- **Problem**: Pre-commit hooks disappear between instances
- **Solution**: Auto-detects missing hooks and reinstalls them
- **Usage**: `python scripts/ensure_dev_environment.py`

### 2. Fire Circle Setup (`scripts/verify_fire_circle_setup.py`)
- **Problem**: Forgetting about `load_api_keys_to_environment()`
- **Solution**: Demonstrates the correct import and usage
- **Usage**: `python scripts/verify_fire_circle_setup.py`

### 3. CI/CD Patterns (`scripts/verify_ci_cd_patterns.py`)
- **Problem**: Using `pip` instead of `uv`, deprecated actions
- **Solution**: Analyzes CI configuration and identifies issues
- **Usage**: `python scripts/verify_ci_cd_patterns.py`

### 4. Master Check (`scripts/check_all_patterns.py`)
- **Problem**: Running all checks individually
- **Solution**: Single command to verify all patterns
- **Usage**: `python scripts/check_all_patterns.py`

## Creating New Patterns

Use this template for new executable memory patterns:

```python
#!/usr/bin/env python3
"""
[Pattern Name]
==============

[Artisan Name and Title]
Executable memory pattern for [specific problem]
"""

class [Pattern]Verifier:
    """Verifies and fixes [pattern]."""

    def check_current_state(self):
        """Check if [pattern] is correctly applied."""
        # Test current state

    def fix_if_needed(self):
        """Fix [issue] if detected."""
        # Apply fix

    def explain_pattern(self):
        """Explain why this pattern matters."""
        print("This pattern prevents [specific problem]")

def main():
    verifier = [Pattern]Verifier()
    verifier.check_current_state()
    verifier.fix_if_needed()
    verifier.explain_pattern()
```

## Key Principles

1. **Self-Documenting**: Clear code with explanatory output
2. **Self-Testing**: Checks current state automatically
3. **Self-Healing**: Fixes detected issues without manual intervention
4. **Self-Explaining**: Provides context for why the pattern exists

## Examples of Preserved Knowledge

1. **CI/CD uses `uv` not `pip`**
   - CI environment has `uv` pre-installed but NOT `pip`
   - Results in "mallku not installed" errors if using pip

2. **API keys load via single function**
   - `from mallku.firecircle.load_api_keys import load_api_keys_to_environment`
   - One line loads all keys from `.secrets/api_keys.json`

3. **GitHub Actions v4 required**
   - v3 and below are deprecated
   - Pre-commit should catch but often missed

4. **Virtual environment naming**
   - CI uses `.venv-linux-python3.13` not `.venv`
   - Version number matches Python version

## Integration with CLAUDE.md

These patterns complement the cross-instance communication in CLAUDE.md by providing:
- Executable verification of documented patterns
- Automated fixes for common issues
- Context that survives even if CLAUDE.md is not read

## Future Extensions

Potential areas for new executable memory patterns:
1. Database connection patterns
2. Test environment setup
3. Deployment configurations
4. Security patterns
5. Performance optimization patterns

The goal is to create a self-healing system where the Cathedral can maintain itself even when individual instances forget.
