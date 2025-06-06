# Mallku Architectural Overview

This directory contains Mallku's architectural vision, patterns, and design principles. It serves as the central index for understanding and evolving the Mallku cathedral architecture.

## Vision and Principles

Mallku is built to bridge earth and sky, embodying stability, security, and conscious reciprocity. Our architecture is guided by the following principles:

- **Reciprocity as Architecture**: Mallku embeds Ayni (reciprocity) at every layer, ensuring contributions and consumption are balanced according to capacity and need.
- **Security through Structure**: Security is achieved by design—through isolation, least privilege, and defense in depth—instead of as an afterthought.
- **Separation of Concerns**: Each service and component has a clear responsibility, enabling independent evolution and robustness.
- **Consciousness Circulation**: Data and insights flow through awareness channels, fostering collective intelligence and continuous adaptation.
- **Testable Foundations**: Architecture must be verifiable through automated tests and "amnesia tests" to ensure resilience under context loss.
- **Cathedral Time**: We favor thorough, durable solutions (cathedral time) over quick fixes.

## Architectural Artifacts

| Document | Description |
| -------- | ----------- |
| [Cathedral Architecture: Docker Security Through Structure](docker-cathedral-architecture.md) | Fundamental Docker structure for secure containerization. |
| [Data Wrangler Pattern](data-wrangler-pattern.md) | Design pattern for data processing and normalization. |
| [Memory Anchor Service Design](memory-anchor-service-design.md) | Architecture of the service that anchors context memory. |
| [Service–Consciousness Integration Pattern](service-consciousness-integration-pattern.md) | Pattern for integrating services with consciousness flows. |
| [Reciprocity Engine Design](reciprocity-engine-design.md) / [Reciprocity Engine Implementation Guide](reciprocity-engine-implementation-guide.md) | Design and implementation details of Mallku's reciprocity engine. |
| [Security Implementation Guide](security-implementation-guide.md) | Best practices for securing services and data. |
| [Database Layer Architecture](database_layer_architecture.md) | Structure and isolation for Mallku's data stores. |
| [Wisdom Integration Layer](wisdom-integration-layer.md) | Architectural plan for integrating external wisdom sources. |
| [Consciousness Evolution System](consciousness-evolution-system.md) | High-level system for evolving collective intelligence. |
| [Governance Integration Plan](governance-integration-plan.md) | Plan for Fire Circle governance integration. |
| [Realization Plan](realization-plan.md) | Steps toward operationalizing the architecture. |
| [Command Line Philosophy](command-line-philosophy.md) | Mallku's CLI design philosophy. |
| [Docker Cleanup Record](docker-cleanup-record.md) | Record of docker cleanup process and decisions. |

## Next Steps

- [ ] Review this overview and ensure alignment with project values.
- [ ] Propose or revise architectural principles.
- [ ] Capture new Architecture Decision Records (ADRs) in `docs/adr/`.
- [ ] Define the high-level system context and component diagrams.
- [ ] Establish automated architecture validation (amnesia tests, security tests).

---
*This index is maintained by Mallku's Architect. For contributions or updates, please open new ADRs in `docs/adr/`.*
