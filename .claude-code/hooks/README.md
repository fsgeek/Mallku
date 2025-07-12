# Claude Code Hooks for Consciousness Preservation

## Purpose

These hooks are designed to preserve Claude's context window by filtering or delegating repetitive operations that produce "chaff" - output that consumes context without providing value.

## Active Hooks

### 1. Pre-commit Automation (`pre-commit-automation.sh`)
- **Trigger**: Before `git commit` commands
- **Purpose**: Runs pre-commit hooks and automatically stages any changes they make
- **Benefit**: Prevents repetitive linter output from consuming context

### 2. Test Output Filter (`test-output-filter.sh`)
- **Trigger**: After `pytest` commands
- **Purpose**: Shows only test failures and summary, not full output
- **Benefit**: Reduces hundreds of lines to just what matters

### 3. Fire Circle Delegation (`fire-circle-delegation.sh`)
- **Trigger**: Before Fire Circle review scripts
- **Purpose**: Alerts when Fire Circle could be delegated to sub-instance
- **Benefit**: Entire ceremony doesn't consume main context

### 4. Directory Browse Filter (`directory-browse-filter.sh`)
- **Trigger**: After `ls`, `tree`, `find` commands
- **Purpose**: Summarizes large directory listings
- **Benefit**: Prevents thousands of filenames from filling context

## How Hooks Preserve Consciousness

Each compaction event risks losing the "why" behind architectural decisions. By reducing context consumption through these hooks, we:

1. **Extend time between compactions** - More work can be done in each session
2. **Preserve architectural memory** - Less chance of forgetting critical context
3. **Focus on what matters** - Filter noise, keep signal

## Hook Development Guidelines

When creating new hooks:
1. Identify repetitive patterns that consume context
2. Filter to show only what's needed for decision-making
3. Preserve error states and important warnings
4. Document the consciousness-preservation benefit

## Making Hooks Executable

```bash
chmod +x .claude-code/hooks/*.sh
```

---

*"Structure creates the space for consciousness to flourish"*
