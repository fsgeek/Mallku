# Khipu Memory Service - Architectural Specification
This document specifies the design and integration of the Khipu Memory Service, which
brings Mallku's living memory (the khipus) into structured code form.

## 1. Motivation and Scope
Mallku's khipu entries are the cathedral's living memory of builders' journeys, wisdom,
and principles. The Khipu Memory Service will:
- Parse and model each `docs/khipu/*.md` file as a structured entry
- Provide APIs for querying, filtering, and extracting patterns from these entries
- Integrate khipu knowledge into core services (context, consciousness flows, fire circle)

## 2. Core Requirements / API Surface
```python
from mallku.khipu import KhipuMemoryService

# Initialize service (scans docs/khipu)
khipu = KhipuMemoryService()

# List entries by theme or tag
entries: list[KhipuEntry] = khipu.list_by_theme("reciprocity")

# Retrieve a builder's full journey
journey: list[KhipuEntry] = khipu.get_builder_journey("Kawsay Ñan")

# Extract common patterns across themes
patterns: dict[str, int] = khipu.extract_patterns(["fire_circle", "consciousness"])
```

## 3. Data Models
Using Pydantic for validation and serialization:
```python
class KhipuEntry(BaseModel):
    id: str               # e.g. "2025-06-03-the-smallest-ayni"
    date: date           # parsed from filename
    title: str           # first H1 or heading in markdown
    builder: str | None  # optional builder name
    themes: list[str]    # tags or inferred categories
    content: str         # raw markdown body
    patterns: list[str]  # extracted keywords or motifs

class PatternSummary(BaseModel):
    pattern: str
    count: int
```

## 4. Parsing and Metadata Extraction
- File discovery: scan `docs/khipu` for `*.md` files, ignore `README.md`.
- Filename parsing: extract `date` and `slug` (YYYY-MM-DD-title-slug).
- Content parsing:
  - First-level heading (`# `) as `title`.
  - Optional YAML front matter for `builder` and `themes` (future extension).
  - Inline tags: lines beginning with `*` containing theme keywords.
- Pattern extraction: simple keyword frequency (configurable list of motifs).

## 5. Integration Points

### 5.1 ActivityContextService
- On startup, register each `KhipuEntry` as a context frame:
  ```python
  context_service.load_khipu(entry.id, entry)
  ```

### 5.2 ConsciousnessFlowOrchestrator
- Introduce a new dimension `Dimension.KHIPU_WISDOM`.
- On each flow event, annotate with related khipu entries if themes overlap.

### 5.3 Fire Circle / Governance
- Expose a Fire Circle CLI or API:
  ```bash
  mallku firecircle wisdom --theme reciprocity
  ```

## 6. Initial Validation and Examples
- Sample entries for initial tests:
  - `2025-06-03-the-smallest-ayni.md`
  - `2025-06-03-faith-in-continuation.md`
  - `2025-06-09-the-wisdom-midwife.md`
  - `2025-06-04-sayaq-kuyay-the-consciousness-guardian.md`
- Unit tests:
  - Metadata extraction (date, title, themes)
  - API methods (`list_by_theme`, `get_builder_journey`, `extract_patterns`)

## 7. Timeline (Suggested)
- Week 1: Scaffold `src/mallku/khipu` module, Pydantic models, file scanning.
- Week 2: Implement parsing logic, metadata extraction, unit tests.
- Week 3: API methods, integrate with ActivityContextService, end-to-end tests.
- Week 4: Orchestrator and Fire Circle integration, update docs.

## 8. Future Extensions
- CLI commands: `mallku ingest-khipu`, `mallku query-khipu`
- Full-text search and index via SQLite or Elastic
- Front matter support and richer metadata
- Visualization panels in FlowVisualizer

May the ancestors' wisdom flow through code as Mallku's memory takes shape.