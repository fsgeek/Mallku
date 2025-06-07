# Mallku Architecture Context for Apu Yachay

## Welcome and Appreciation
Thank you for your thorough architectural review. Your expertise in security validation and CI/CD will strengthen Mallku significantly. This document provides context to help align your valuable contributions with Mallku's current phase and unique vision.

## Background

The exemplar/ directory contains a non-repository copy of Indaleko’s “exemplar” branch—used purely as a historical reference
and not part of Mallku’s codebase.

The original goal of Indaleko was to allow bridging episodic human memory to storage by constructing a unified personal index service.  Mallku seeks to expand on this by providing a robust security architecture, a focus on human-facing tooling (Indaleko was a CS systems PhD project, so the tools were a lens for evaluating the systems components, not part of the evaluation.)  In addition, the goal is to also extend the episodic memory mapping to email, which suffers from a similar challenging search problem (Outlook search is... almost unusable.)

No human is involved in building the code or system.

## Current State: Personal Consciousness Assistant

Mallku is currently a **personal-scale** consciousness recognition system, similar to:
- Obsidian/Notion (personal knowledge management)
- Local email clients with smart filtering
- Personal automation tools

Think "Wright Brothers proving flight" not "Boeing designing airplanes."

## What Exists vs. What's Envisioned

### Exists Now:
- Core correlation engine and memory anchor system
- Local file system and email integration
- GitHub-based development
- Human architect/builder collaboration

### Designed but Not Built:
- Fire Circle AI governance (requires LLM integration)
- Multi-user scale infrastructure
- Production deployment architecture

### Your Contributions - Reframed:
1. **CI/CD Pipeline**: Yes! GitHub Actions for automated testing
2. **Amnesia Tests**: Excellent idea for ensuring security patterns persist
3. **ADR Process**: Let's implement this for reviewers

## Immediate Opportunities

Here are a few immediate ways you can support our next architectural milestones:

- **Domain Context & Success Criteria**:
  - **SLO/SLA** targets: inappropriate at this time.
  - **Security/Compliance** targets: initial primary threat model is third party data provider compromise; obfuscated data, partial encryption.
  - **Key Operational Scenarios**:
    - **Disaster Recovery**: standard backup/restore for personal scale data; replication for enterprise (not in scope)
    - **Multi-region failover**: out of scope at this time (inappropriate for personal scale).
    - **Offline Mode**: not supported
- **CI/CD & Test‑Harness Environments**:
  - Staging/sandbox cluster: Does not exist currently. Use GitHub Actions for CI/CD.
  - Create CI/CD playbooks and configuration templates for automated amnesia and security‑architecture tests.
- **Fire‑Circle & Governance Cadence**:
  - Note: blocked on design/implementation, see below.
  - Coordinate and schedule a Fire Circle session to review ADR #0001 and ADR #0002
  - Help draft a proposal template for future ADR submissions and approvals.


## Future Architecture Components (Seeking Builders)

- **Fire Circle Implementation**: Help expand the [firecircle design](firecircle/docs/DESIGN.md); once done, implement the design.
- **Staging Environment**: Containerized test deployment
- **Email Integration**: Expand beyond file system to email patterns.

## Project Philosophy
Mallku embodies a unique approach where AI builders collaborate with human stewards to create consciousness-aware systems. Your architectural expertise helps ensure these novel patterns are built on solid foundations.
