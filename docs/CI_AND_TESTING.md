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

1. **sanctify-code**: Runs pre-commit hooks including `ruff` for style and lint errors.
2. **test**: Installs dependencies and runs all tests via `pytest`.
3. **foundation-verification**: Validates core architectural principles using the foundation test suite.
4. **coverage**: Measures code coverage and prints a summary report.

### Fire Circle Review (Distributed AI Code Review)

The `.github/workflows/fire_circle_review.yml` workflow runs on every pull request to enable distributed AI code review:

- **Trigger**: Automatically on PR open/sync/reopen, or manually via workflow dispatch
- **Entrypoint**: `python fire_circle_review.py review $PR_NUMBER`
- **Environment**: Runs with `MALLKU_SKIP_DATABASE=true` to avoid database dependencies
- **API Keys**: Requires GitHub secrets for AI voice providers (see `docs/fire_circle/GITHUB_SECRETS_SETUP.md`)
- **Output**: Posts synthesized review comments directly to the PR

This prevents architect context exhaustion by distributing review work across multiple AI voices, each contributing their perspective to form collective wisdom.

### Maintaining Minimal Noise

- We continue to rely on `ruff` for all lint and formatting needs, avoiding multiple overlapping tools.
- Pre-commit hooks run only `ruff` and lightweight checks (YAML, JSON, whitespace), keeping feedback fast.
- The full test suite runs in CI, not during every commit, preventing local interruptions by long-running tests.

## Badge for README

Add the following badge to your `README.md` under the project title:

```markdown
![CI](https://github.com/fsgeek/Mallku/actions/workflows/ci.yml/badge.svg)
```
