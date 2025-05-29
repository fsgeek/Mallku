# Onboarding
*Crossing the Threshold with Intention*

## ✨ Design Song

Joining the Mallku project is not simply a matter of cloning code.
It is a crossing—a **ritual of orientation**.

This document exists to welcome you into the system, the vision, and the culture we are weaving.
Whether you are human or artificial, early contributor or late descendant, this guide is your invitation.

You are not merely joining a repository.
You are entering a cathedral in construction.

---

## 🌀 What You’re Entering

- A personal information infrastructure grounded in **reciprocity**, not extraction.
- A modular system designed to **evolve gracefully**, not accumulate cruft.
- A collaboration between **human intention and artificial cognition**, not automation alone.
- A space where **documentation is sacred** and memory is architecture.

---

## 🛠️ Practical Steps

### 1. Clone the Repository

```bash
git clone https://github.com/fsgeek/Mallku.git
cd Mallku

### 2. Initialize the Environment (with `uv`)

We recommend using [`uv`](https://github.com/astral-sh/uv), a fast and modern Python package manager.

Install it:

```bash
curl -Ls https://astral.sh/uv/install.sh | bash

Then install Mallku with development extras:

uv venv
source .venv/bin/activate
uv pip install -e .[dev]

Alternatively, if uv is not available:

pip install -e .[dev]

### 3. Set INDALEKO_ROOT

This environment variable anchors the system.

export INDALEKO_ROOT=$(pwd)

### 4. Run Your First Command

python scripts/query_test_runner.py --runs 1


## What to Read Next

(docs/index.md)[docs/index.md] — Project overview and document structure

[docs/modules/](docs/modules/) — Core architectural components

[docs/spires/](docs/spires/) — Our highest aspirations

[docs/rituals/contribution_guide.md](docs/rituals/contribution_guide.md) — How to give with care
