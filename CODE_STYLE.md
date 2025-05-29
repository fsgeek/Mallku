# Mallku Code Style

This project uses `ruff` for static analysis and formatting, enforced via pre-commit hooks.

## 🧠 Principles

- **Clarity before cleverness**
- **Errors should be obvious at the boundaries**
- **Everything human-readable—especially for AI collaborators**

## 🪶 Code Conventions

| Topic            | Guideline                                           |
|------------------|-----------------------------------------------------|
| Max line length  | 100 characters (pragmatic for context windows)      |
| Quote style      | Double quotes for strings                           |
| Imports          | Sorted, grouped: stdlib → third-party → local       |
| Functions        | Lowercase_with_underscores unless class method      |
| Type hints       | Required on all public functions                    |
| Comments         | Use for *why*, not *what*                           |
| Format on save   | Yes (via pre-commit and `ruff --fix`)              |

## 🛡️ AI Contributor Hygiene

- All generated code must pass `pre-commit run --all-files`
- Use reflection blocks in commits when significant generation occurs:
```txt
AI Contribution Note:
Generated using prompt X
Reviewed and modified by human contributor Y
