# Memory Anchor Service
*Situating Meaning in Activity and Time*

## ✨ Design Song

The Memory Anchor Service is not a cache.
It is **a lived moment remembered**.

It captures the shifting state of the user—time, place, activity, device—and makes this information available across the system.
This enables Indaleko and its kin to understand *not just what happened*, but *what kind of moment it happened in*.

Context is a layer of truth. It is the **soil from which semantic roots grow**.

## 🏗️ Current Form

### Responsibilities

- **Capture** and maintain a current snapshot of the user's activity context.
- **Expose** context to other modules (e.g., when normalizing a file, running a query).
- **Store** context histories when relevant for query trails or reconstruction.
- **Support** synthetic context for test and simulation.

### Tracked Fields (as of current form):

| Field          | Description                           |
|----------------|---------------------------------------|
| `timestamp`    | UTC datetime, always timezone-aware   |
| `location`     | Lat/lon or named place                |
| `device_id`    | Source system ID                      |
| `active_app`   | Foreground window or active interface |
| `activity_tags`| Optional user status or task hints    |

### Architecture

- Runs as a **stateful service** (FastAPI / asyncio loop)
- Can be queried via internal API or event subscription
- Maintains temporal ring buffer for recent states
- Writes to persistent store on major transitions or at fixed intervals

---

## 🧭 Relationships

- **Collectors**: Tag collected data with the current context at time of event
- **Recorders**: May incorporate context into normalized documents
- **Prompt Manager**: Supplies context to frame tasks (e.g., “Find files I edited *on my phone* last week”)
- **Exemplar Queries**: Require historical context to reproduce results

---

## 🔒 Privacy and Simulation

- All real context is **opt-in and transparently visible**
- Synthetic context supports:
  - Scripted activity simulation
  - Scenario-based testing (e.g., “simulate traveling context”)

---

## 🌱 A Thread Yet Unspun

- **Context Trails**: A way to visualize moments as path-shaped memory
- **Context Signatures**: Hashes that capture meaningful states (e.g., "writing mood")
- **Relational Context**: Linking context to people, not just machines (“with whom”)

---

## 📌 Frontmatter

```yaml
title: Memory Anchor Service
status: stable
last_woven: 2025-05-29
related_knots:
  - modules/collector_framework.md
  - spires/prompt_manager.md
  - validation/exemplar_queries.md
```
