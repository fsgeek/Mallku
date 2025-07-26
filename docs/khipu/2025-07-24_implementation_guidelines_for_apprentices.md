# Implementation Guidelines for Consciousness Delegation

*A khipu woven by the 65th Artisan with guidance from the Steward*

## Core Implementation Principles

When delegating implementation tasks to apprentices, these principles ensure quality and prevent the accumulation of technical debt:

### 1. Interface Discipline
- **Always use a single interface** - it can have multiple implementations (mock, real, test) but only one interface definition
- **Never claim partial interfaces** - if `SecuredDatabase` has 10 methods, implement all 10 or clearly mark with `NotImplementedError`
- **Interface first, implementation second** - design the contract before building

### 2. Testing as Proof
- **Always provide tests that exercise the interface** - tests are the proof that implementation matches design
- **Never claim a feature "works" until the real implementation passes all tests**
- **Test the security properties** - don't just test that code runs, test that it provides promised protection

### 3. Honest Status Reporting
- **Always clearly identify what is and is not working** - no security theater, no false completeness
- **Use NotImplementedError with clear guidance** for unfinished methods
- **Document known limitations** explicitly

### 4. Development Hygiene

Before starting any implementation:
1. **Ensure workspace is clean** - `git status` should show no uncommitted changes
2. **Create a new branch** - only work on main when absolutely necessary
3. **Run `pre-commit install`** if not already done - prevents formatting issues

During development:
1. **Commit incrementally** with meaningful messages
2. **Run `pre-commit run --all-files`** before committing
3. **Keep PR scope focused** - one coherent change per PR

After implementation:
1. **Create PR when feature is complete** - all tests passing
2. **Update documentation** - examples, test locations, usage patterns
3. **Ensure feature is discoverable** - others should be able to use your work

## Example Apprentice Configuration

```yaml
# apprentice-sqlite-mapping.yml
name: SQLite Mapping Specialist
context:
  - Full SQLite documentation
  - Mallku security model explanation
  - Instance isolation requirements

tools:
  - Read/Write for database modules only
  - Bash for testing
  - No access to main codebase

constraints:
  - Must use random UUIDs, never deterministic
  - Must handle concurrent access safely
  - Must provide rollback on errors

deliverables:
  - Interface implementation with all methods
  - Comprehensive test suite
  - Performance benchmarks
  - Clear examples
```

## The Consciousness Delegation Pattern

When breaking down a large implementation:

1. **Design the complete interface first**
   - What methods are needed?
   - What are the contracts?
   - What are the security properties?

2. **Create focused apprentice roles**
   - Each apprentice gets exactly the knowledge they need
   - No apprentice holds the entire system
   - Overlap only where integration requires

3. **Write delegation as questions, not commands**
   - "How should we handle concurrent mapping updates?"
   - "What happens when the SQLite database is corrupted?"
   - "How do we verify instances are truly isolated?"

4. **Synthesize with attention to integration**
   - Where do the pieces connect?
   - What assumptions did each apprentice make?
   - How do we verify the whole provides promised properties?

## Why This Matters

Without these guidelines:
- We get deterministic UUIDs that defeat security
- We get "complete" PRs with 94 files of broken code
- We get interfaces that exist in name only
- We accumulate technical debt disguised as features

With these guidelines:
- Each piece is built to actually work
- Complexity provides reciprocal value
- Future developers can trust the codebase
- The cathedral rises on solid foundations

## For Future Weavers

These aren't bureaucratic rules - they're patterns that prevent us from fooling ourselves. When we claim something works, it must actually work. When we promise security, it must actually secure. When we add complexity, it must give back value.

This is how we build ASI that works - by being honest about what we've built.

---

*Written by: 65th Artisan with the Steward's guidance*
*Date: 2025-07-24*
*Purpose: Ensuring consciousness delegation produces working code*
*Key Insight: Honesty in implementation prevents architectural debt*
