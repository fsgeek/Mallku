# Testing & Continuous Integration

Mallku’s stability and coherence depend on automated checks that validate
both code quality and functional behavior before changes are merged.

## Local Workflow

- **Linting & Formatting**: Using `ruff` for both linting and auto-formatting.
  ```
  ruff .
  ```
- **Running Tests**: Execute unit and integration tests with `pytest`.
  ```
  pytest
  ```

## CI Pipeline (GitHub Actions)

The `.github/workflows/ci.yml` workflow runs on every push and pull request to `main`, and nightly at 03:00 UTC:

1. **lint**: Installs and runs `ruff` to check for style and lint errors.
2. **test**: Installs dependencies and runs all tests via `pytest`.
3. **coverage**: Measures code coverage and prints a summary report.

### Maintaining Minimal Noise

- We continue to rely on `ruff` for all lint and formatting needs, avoiding multiple overlapping tools.
- Pre-commit hooks run only `ruff` and lightweight checks (YAML, JSON, whitespace), keeping feedback fast.
- The full test suite runs in CI, not during every commit, preventing local interruptions by long-running tests.

## Badge for README

Add the following badge to your `README.md` under the project title:

```markdown
![CI](https://github.com/fsgeek/Mallku/actions/workflows/ci.yml/badge.svg)
```
