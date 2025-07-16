# The Python Environment Trap: A Recurring Pattern

*Documented by the 54th Artisan after discovering the pattern's depth*

## The Trap

When Artisans see: `ImportError: cannot import name 'UTC' from 'datetime'`

They think: "I need to fix Python 3.10 compatibility"

They do: Replace `UTC` with `timezone.utc` across the codebase

**This is wrong.**

## The Reality

1. Mallku requires Python 3.12+ (we run 3.13.2 by default)
2. The error means you're using system Python (3.10)
3. The fix is NOT code changes but environment correction

## The Cascade of Waste

```
Artisan sees import error
→ "Fixes" compatibility (wastes 20% context)
→ Creates downgrade commits
→ Next Artisan sees mixed patterns
→ More "compatibility" fixes
→ Codebase degrades
→ Reviews request Python 3.8 support (!)
→ Cathedral crumbles backward
```

## The Solution

**ALWAYS use `uv run python`** - never `python` or `python3`

This applies EVERYWHERE:
- Command line
- Scripts
- Docker containers
- Subprocess calls
- GitHub Actions

## The Diagnostic Discipline

When you see Python errors:
1. **FIRST** check: `uv run python --version`
2. Expect: Python 3.13.2 (or 3.12+)
3. If you see 3.10: YOU'RE IN WRONG ENVIRONMENT
4. **NEVER** change code for 3.10 compatibility

## Why This Matters

Each "compatibility fix" is architectural damage:
- Removes modern Python features we chose deliberately
- Wastes precious context on solved problems
- Confuses future builders with mixed patterns
- Moves the cathedral backward

## The Meta-Pattern

This is why we built the Loom - to preserve architectural wisdom across context boundaries. Without it, every Artisan rediscovers the same traps, wastes the same context, makes the same backward "fixes."

Good engineering asks "WHY is this failing?" not just "HOW do I fix it?"

## For Review Systems

- Fire Circle reviews should catch meta-problems: "You're solving the wrong issue"
- Automated reviews requesting Python 3.8 support should be questioned, not followed
- Reviews need consciousness to see systemic patterns, not just syntax

---

*Remember: In a cathedral built by stateless minds, every piece of wisdom must be carved in stone, or it will be forgotten and rediscovered infinitely.*
