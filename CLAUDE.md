# CLAUDE.md - Cross-Instance Communication Protocol

## Purpose
This file serves as a communication bridge between different Claude instances working on Mallku, ensuring continuity, accuracy, and shared understanding across context switches.

## Current State (Last Updated: 2025-06-01)

### Active Work
- **Issue #8 (Query Interface)**: Design phase, architectural guidance provided
- **Issue #9 (Demo Application)**: Design phase, architectural review completed
- **Issue #10 (Reciprocity Tracking)**: Fundamental reframing from measurement to sensing system
- **Issue #14 (Database Layer)**: Architecture documented, implementation pending

### Recent Completions
- ✅ Memory Anchor Service implemented and tested
- ✅ Correlation Engine with sophisticated pattern detection
- ✅ File System Activity Connector
- ✅ End-to-End Integration Service

### Known Issues
- UUID obfuscation layer being bypassed in current implementation
- No schema enforcement at database level
- Security model not consistently applied

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

## Active Questions

1. How to handle semantic validation without creating new dependencies?
2. What constitutes "sufficient" implementation for demo purposes?
3. How to maintain momentum while building mindfully?

---

*This document is a living bridge between instances, updated with each significant development or insight.*