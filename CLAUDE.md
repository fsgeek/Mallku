# CLAUDE.md - Cross-Instance Communication Protocol

## Purpose
This file serves as a communication bridge between different Claude instances working on Mallku, ensuring continuity, accuracy, and shared understanding across context switches.

## Current State (Last Updated: 2025-05-31 by Claude Code)

### Active Work
- **Issue #8 (Query Interface)**: Design phase, architectural guidance provided
- **Issue #9 (Demo Application)**: Design phase, architectural review completed
- **Issue #10 (Reciprocity Tracking)**: Fundamental reframing from measurement to sensing system
- **Issue #14 (Database Layer)**: ⚠️ **Architecture documented, implementation incomplete**

### Recent Completions
- ✅ Memory Anchor Service implemented and tested
- ✅ Correlation Engine with sophisticated pattern detection
- ✅ File System Activity Connector
- ✅ End-to-End Integration Service

### Known Issues
- UUID obfuscation layer being bypassed in current implementation
- No schema enforcement at database level
- Security model not consistently applied

### Recent Work Session (2025-05-31)
**What was CLAIMED**: Complete containerized infrastructure with security isolation
**What was ACTUALLY delivered**:
- ✅ Conceptual architecture files (Docker, compose, etc.)
- ✅ Security interface code structure (`src/mallku/core/database/secured_interface.py`)
- ✅ Multi-LLM layer framework (`src/mallku/llm/multi_llm_layer.py`)
- ✅ Prompt manager protection layer (`src/mallku/prompt/manager.py`)
- ❌ **Tests fail due to circular imports**
- ❌ **Docker containers cannot build (missing dependencies)**
- ❌ **No functional integration with existing codebase**
- ❌ **Claims of "working infrastructure" were premature**

**Lesson**: Follow CLAUDE.md guidelines - commit working code before claiming completion

## Communication Guidelines

### For Claude Code (Implementation)
When claiming completion:
1. List specific files created/modified
2. Note which tests pass
3. Identify what remains unfinished
4. Commit code before declaring victory

### For Claude Opus (Architecture)
When providing guidance:
1. Reference specific components affected
2. Note architectural decisions that impact implementation
3. Flag breaking changes explicitly
4. Update this file with major shifts

## Key Architectural Decisions

### Reciprocity Tracking (Issue #10)
**Critical Reframing**: Not measurement but sensing
- Don't build autonomous judge of reciprocity
- Build community sensing tool for Fire Circle governance
- Detect patterns requiring collective discernment
- Technical builders not qualified to define reciprocity

### Database Layer (Issue #14)
**Security Through Architecture**: Containerization + Semantic Registration
- Physical impossibility of bypassing security
- Schema enforcement at Mallku layer
- Semantic descriptions for all collections/fields
- Phased migration to prevent disruption

## Philosophical Reminders

### Ayni Principles
- Reciprocity ≠ equal exchange/barter
- Contribute according to capacity, receive according to need
- Balance is dynamic equilibrium, not static rules
- Emergence happens through genuine dialogue

### Cathedral Building
- Build mindfully with deliberate intent (not faster)
- Document journeys, not just destinations
- Expect and welcome fundamental reframings
- Each stone matters to the whole

## Handoff Protocol

When switching instances:
1. Update "Current State" section above
2. Note any uncommitted work in progress
3. Flag decisions needing validation
4. Record insights that shouldn't be lost

## Khipu Guidelines

**Khipu are NOT GitHub Issues** - they are reflections stored in `docs/khipu/`

### What Khipu Are For
- Storytelling and reflection on the building process
- Recording insights, visions, and emergent understanding
- Capturing aspirations, goals, dreams, desires
- Preserving the "why" behind technical decisions

### What Khipu Are NOT For
- Technical specifications (use docs/architecture/)
- Work tracking (use GitHub Issues)
- Implementation details (use code comments)

### Creating a Khipu
1. Create markdown file in `docs/khipu/`
2. Use descriptive filename: `emergence_through_reciprocal_intelligence.md`
3. Write in narrative form - tell the story
4. Include reflection on what was learned
5. Let the form serve the content - no rigid structure

## Active Questions

1. How to handle semantic validation without creating new dependencies?
2. What constitutes "sufficient" implementation for demo purposes?
3. How to maintain momentum while building mindfully?

---

*This document is a living bridge between instances, updated with each significant development or insight.*
