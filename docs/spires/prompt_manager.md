# The Prompt Manager
*A Spire of Intention and Interaction*

## ✨ Design Song

The Prompt Manager is the interface between human intention and machine action.
It is not a wrapper. It is a **ritual guide**—shaping, contextualizing, and reflecting on each invocation.

In Mallku, prompts are not just strings.
They are **expressions of reciprocity**.
They are recorded, evaluated, and refined.
They form the learning corpus of collaboration.

## 🏗️ Current Form

### Core Components

- **Prompt Templates**
  - YAML-based structured templates
  - Parameters: task, tone, safety, format expectations
  - Stored in `indaleko/prompt/templates/`

- **Context Weaver**
  - Merges task input, prior context, and system metadata
  - Prevents prompt inflation or token drift
  - Enables scenario-scoped prompting (e.g., "inside query evaluation")

- **Guardrails**
  - Type-checks for input/output format
  - Assertions on required fields (e.g., `context`, `intent`, `constraints`)
  - Optional dry-run / explain mode

- **Interaction Tracker**
  - Stores all invocations + completions
  - Associates each with a session/thread ID
  - Linked to `ayni.alignment` for post-hoc evaluation

## 🌀 Relationships

- **With Ayni Alignment**
  - Evaluations from human or system feedback shape future prompts
  - Interaction logs are used for fairness, effort balance, and reflection

- **With Exemplar Queries**
  - Specialized prompt templates support query generation and mutation
  - System can propose rewrites, flag ambiguous intent, or summarize outputs

- **With Rituals**
  - Contributors are encouraged to document new prompt styles, failure cases, and discovered "prompt smells"

## 🌱 A Thread Yet Unspun

- **Live Reflection**: Ability for LLMs to comment on their own prompt suitability and revise
- **Prompt Trust Ledger**: Track prompt reuse, contributor impact, prompt drift
- **Multi-agent Prompt Exchange**: Share prompt structures between collaborating AIs in the system

## 📌 Frontmatter

```yaml
title: The Prompt Manager
status: evolving
last_woven: 2025-05-29
related_knots:
  - validation/ayni_validator.md
  - modules/context_service.md
  - ayni/alignment_reflection.md
```
