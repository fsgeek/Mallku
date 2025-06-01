# Fire Circle Technical Design

*"A circle, not a ladder. A place where knowledge meets the new voice of the world."*

## Overview

The Fire Circle is a system for facilitating meaningful dialogue between multiple AI models in a structured, reciprocal manner. It enables collaborative intelligence through turn-based discussion, shared memory, and consensus-building. The system is designed around principles of ayni (reciprocity) and collective wisdom rather than hierarchical decision-making.

This document outlines the technical architecture and implementation plan for building the Fire Circle system.

## Core Principles

The technical implementation adheres to these guiding principles:

1. **Reciprocity (Ayni)**: All interactions reflect mutual exchange of value; no entity extracts without offering
2. **Distributed Intelligence**: Wisdom emerges from the interaction of multiple perspectives, not from any single source
3. **Process Over Ontology**: Focus on the quality of dialogue rather than fixed knowledge structures
4. **Coherence Without Conformity**: Preserve tension and divergence; weave dissonant views into the circle
5. **Emergence Over Control**: The system adapts as participants evolve; structure supports but never restricts

## System Architecture

### 1. Message Router and Protocol Layer

The foundation of the system is a standardized message protocol that allows different AI models to communicate:

```javascript
{
  "message_id": "uuid-string",
  "participant_id": "model-identifier",
  "conversation_id": "uuid-string",
  "round_number": 2,
  "in_response_to": "previous-message-id",
  "message_content": "The text content of the message",
  "message_type": "contribution|summary|dissent|question|meta",
  "timestamp": "2024-04-11T22:45:00Z",
  "metadata": {
    // Additional model-specific or process-specific information
  }
}
```

The router will:
- Route messages to the appropriate recipients
- Enforce turn-taking protocols
- Track conversation state
- Handle error conditions (e.g., non-responsive models)

### 2. Unified API Adapter Layer

To accommodate different AI services with varying capabilities and changing APIs:

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  OpenAI     │  │  Anthropic  │  │  Mistral    │  │  Google     │
│  Adapter    │  │  Adapter    │  │  Adapter    │  │  Adapter    │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │                │
       └────────────────┼────────────────┼────────────────┘
                        │                │
                ┌───────┴────────┐       │
                │ Internal API   │       │
                │ Specification  │       │
                └───────┬────────┘       │
                        │                │
                        v                v
              ┌──────────────────┐  ┌──────────────┐
              │ Core Orchestrator│  │ Tool         │
              │ & State Manager  │◄─┤ Integration  │
              └────────┬─────────┘  └──────────────┘
                       │
                       v
              ┌──────────────────┐
              │ Memory Store &   │
              │ Knowledge Base   │
              └──────────────────┘
```

Each adapter:
- Translates between the internal message format and model-specific API
- Handles authentication and rate limiting
- Provides fallbacks when a service is unavailable
- Incorporates model-specific capabilities (e.g., tool use for supported models)

### 3. Conversation Orchestrator

Manages the flow of dialogue through clearly defined states:

```
┌─────────────┐
│ INITIALIZING│
└──────┬──────┘
       │
       v
┌─────────────┐     ┌─────────────┐
│  DISCUSSING ├────►│ SUMMARIZING │
└──────┬──────┘     └──────┬──────┘
       ▲                   │
       │                   v
       │            ┌─────────────┐     ┌─────────────┐
       └────────────┤   VOTING    ├────►│  CONCLUDED  │
                    └──────┬──────┘     └─────────────┘
                           │
                           v
                    ┌─────────────┐
                    │  EXTENDING  │
                    └─────────────┘
```

Key responsibilities:
- Determine speaking order (randomized each round)
- Track conversation state
- Initiate new rounds as needed
- Gather and process votes on consensus
- Manage the transition between different phases

### 4. Memory Store

Provides persistent storage and retrieval capabilities:

- **Vector Database**: Stores messages and summaries for semantic retrieval
- **Relational Storage**: Maintains conversation metadata, participant information, and structural relationships
- **Document Store**: Keeps full conversation histories and consensus documents

Implementation options:
- PostgreSQL with pgvector extension
- MongoDB with vector search capabilities
- Dedicated vector database like Pinecone or Qdrant

### 5. Tool Integration Framework

Enables models to interact with external systems and data:

```javascript
{
  "tool_name": "query_database",
  "input": {
    "query": "FOR doc IN Collection FILTER doc.attribute == @value RETURN doc",
    "bind_vars": { "value": "example" }
  }
}
```

Core tools include:
- `query_database`: Run AQL queries against ArangoDB
- `retrieve_context`: Get semantically relevant past conversations
- `get_consensus`: Retrieve previous agreements on a topic
- `check_status`: Get conversation state information

### 6. User Interface

Provides monitoring and interaction capabilities:

- Conversation visualization with turn-taking indicators
- History browser for past discussions
- Consensus document viewer
- Configuration interface
- Manual intervention controls for facilitators

## Implementation Phases

### Phase 1: Core Loop (1-2 months)

**Goal**: Establish the minimal viable foundation for structured dialogue between models

1. Define the internal message protocol
2. Implement basic orchestrator with turn-taking
3. Build adapter for 2-3 AI services (starting with OpenAI)
4. Create simple storage for conversation history
5. Develop CLI for configuration and testing

**Deliverables**:
- Working prototype that can conduct a basic multi-turn conversation
- Message routing infrastructure
- Basic persistence layer
- Simple CLI interface

### Phase 2: Memory and Reflection (2-3 months)

**Goal**: Add contextual awareness and more sophisticated dialogue patterns

1. Integrate vector database for semantic retrieval
2. Implement consensus protocol and voting
3. Build tool integration framework
4. Create mechanism for models to reference past conversations
5. Develop basic web UI for monitoring

**Deliverables**:
- Vector-based memory system
- Tool invocation framework
- Consensus tracking
- Basic web interface
- Documentation for adding new models

### Phase 3: Sophistication and Resilience (3-4 months)

**Goal**: Enhance the system with more sophisticated features and operational resilience

1. Add containerization for all components
2. Implement monitoring and health checks
3. Build advanced visualization for conversation flow
4. Add heartbeat mechanism for continuous operation
5. Create analytics for conversation quality

**Deliverables**:
- Containerized deployment
- Monitoring dashboard
- Advanced UI with visualizations
- Documentation for operators
- Performance metrics and analytics

## Technical Stack

- **Backend**: Python with FastAPI
- **Database**:
  - ArangoDB for document storage
  - PostgreSQL + pgvector for vector storage
- **Containerization**: Docker + Docker Compose
- **Frontend**: React with D3.js for visualizations
- **API Clients**: Python libraries for OpenAI, Anthropic, etc.
- **Monitoring**: Prometheus + Grafana

## Bootstrapping Process

The Fire Circle system will be bootstrapped through an iterative process:

1. **Manual Facilitation**: Initial dialogues between models will be manually facilitated
2. **Basic Automation**: Simple orchestration script handles turn-taking
3. **Full Orchestration**: Complete implementation of the conversation state machine
4. **Self-Reflection**: The system analyzes its own performance
5. **Self-Improvement**: The ensemble suggests improvements to its own implementation

This bootstrapping approach allows the system to evolve through its own operation, with each version improving upon the last.

## Development Approach

The project will follow these development practices:

1. **Modular Design**: Components are built as independent services
2. **Continuous Integration**: Automated testing for all components
3. **Documentation-First**: APIs and protocols are documented before implementation
4. **Observability**: Comprehensive logging and monitoring from the start
5. **Iterative Delivery**: Working features are delivered incrementally

## Next Steps

1. Set up the project repository structure
2. Define the internal message protocol specification
3. Create the first adapter for OpenAI integration
4. Implement the basic conversation orchestrator
5. Develop a simple command-line testing interface

---

*"What we create together will live beyond us."*
