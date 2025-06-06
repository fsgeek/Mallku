---
# System Context & Component Diagrams

Below are the high-level System Context and Component diagrams for Mallku.

```mermaid
%% System Context Diagram
graph TB
  subgraph External Entities
    User[User / Client Apps]
    Admin[Administrator]
    ThirdParty[External Services]
  end

  subgraph Mallku_System[ ]
    API[API Gateway]
    Auth[Auth & Identity Service]
    Reciprocity[Reciprocity Engine]
    Memory[Memory Anchor Service]
    DataStore[Data Stores]
    Governance[Governance & Fire Circle]
  end

  User -->|REST / RPC| API
  Admin -->|Web UI / CLI| API
  ThirdParty -->|Webhook / API| API
  API --> Auth
  API --> Reciprocity
  API --> Memory
  Reciprocity --> DataStore
  Memory --> DataStore
  Governance --> API
  Governance --> DataStore
```

```mermaid
%% Component Diagram
graph LR
  API -->|Authenticates via| Auth
  API -->|Invokes| Reciprocity
  Reciprocity -->|Reads/Writes| Memory
  Memory -->|Stores in| Database[(PostgreSQL / Redis)]
  Reciprocity -->|Exports Metrics| Metrics[Metrics & Observability]
  API -->|Publishes Events| EventBus[(Kafka / PubSub)]
  EventBus -->|Consumed by| ExternalIntegration[External Integration Services]
  Governance -->|Subscribes to| EventBus
```

*Figures: System Context (top), Component interactions (bottom).*
---

*Maintained by Mallku Architect. Adjust diagrams in tandem with ADRs and architecture updates.*
---
