# Collector Framework
*Holding the Edge Between Observation and Meaning*

## ✨ Design Song

Collectors are the scouts of Mallku.
They observe, record, and pass along—but they do **not** interpret.

This framework enforces a sacred boundary:
- **Collectors** gather raw data.
- **Recorders** transform and store.

This separation ensures auditability, modularity, and respect for original data.
It is the foundation of truthfulness in a system that aspires to remember responsibly.

---

## 🧱 Structure

### 📦 `indaleko.collector`

Each collector is a standalone component with a single responsibility.

Collectors must:
- Gather raw data from a specified source (e.g., filesystem, calendar, app logs)
- Output raw artifacts (JSON, CSV, plain text, etc.) to a defined staging area
- Annotate each artifact with metadata: timestamp, source, collector version
- NEVER write to the database
- NEVER modify or interpret the data

---

## 📦 Collector Interface

Each collector implements:

```python
class BaseCollector(Protocol):
    def collect(self) -> list[RawArtifact]:
        ...
```

Where RawArtifact includes:
- content: bytes | str
- metadata: dict[str, Any]
- timestamp: datetime
- collector_name: str
- source_type: str

## 🔒 Boundaries

| Function                  | Collector      | Recorder      |
|---------------------------|:--------------:|:-------------:|
| Raw data acquisition      | ✅ Yes         | ❌ Never      |
| Data normalization        | ❌ Never       | ✅ Yes        |
| Database writes           | ❌ Never       | ✅ Yes        |
| Inter-collector calls     | ❌ Prohibited  | ❌ Prohibited |
| Output format enforcement | ✅ Strongly Typed | ✅ Strongly Typed |

## 🧭 Relationships
- Context Service: Each collected artifact is tagged with the current activity context.
- Recorder Framework: Recorders consume outputs from collectors, transforming them into structured data for storage.
- Validation Layer: The output of collectors is included in validation runs to detect drift, format violations, or edge-case behavior.

## 🔧 Staging Directory
Collectors write output to:

```bash
$INDALEKO_ROOT/data/staging/{collector_name}/{timestamp}/
```

This staging area is preserved and can be re-processed, audited, or replayed by recorders.

## 🌱 A Thread Yet Unspun
Synthetic Collectors: Mirror real collectors to produce synthetic datasets for evaluation.

Collector Provenance Ledger: Track every artifact back to collector version, environment, and invocation.

Consent-aware Collectors: Add fine-grained capture controls based on user context or time of day.

title: Collector Framework
status: stable
last_woven: 2025-05-29
related_knots:
  - modules/context_service.md
  - validation/exemplar_queries.md
  - rituals/interaction_etiquette.md

# Note
Collectors are not interpreters.
They are witnesses.
And in a world of systems that assume too much,
a witness that says only what it saw is a sacred thing.
