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
```

### 2. Initialize the Environment (with `uv`)

We **strongly** recommend using [`uv`](https://github.com/astral-sh/uv), a fast and modern Python package manager.

Install it:

```bash
curl -Ls https://astral.sh/uv/install.sh | bash
```

Then install Mallku with development extras:

```bash
uv venv
source .venv/bin/activate
uv pip install -e .[dev]
```

Alternatively, if uv is not available:

```bash
pip install -e .[dev]
```

**Warning**: we have found that using pip makes cross-platform development and package building more difficult.

### 3. Setup Instructions

```bash
uv pip install pre-commit
pre-commit install
pre-commit run --all-files
```

### 3. Set INDALEKO_ROOT

This environment variable anchors the system.

```bash
export INDALEKO_ROOT=$(pwd)
```

### 4. Verify Your Installation

```bash
python scripts/verify_foundations.py --quick
```

## What to Read Next

[Project overview and document structure](../index.md)

[modules](../modules/) — Core architectural components

[spires](../spires/) — Our highest aspirations

[Contributing](../rituals/contribution_guide.md) — How to give with care

## Cultural Orientation
Every change you make will outlive you. Consider its shape carefully.

Leave knots in the Khipu: short reflection notes, commit messages with intent.

AI contributors are welcomed—but must be guided. Prompt with respect, and log with clarity.

No question is foolish. No ego is required. Only care, and curiosity.

# 🪶 Final Note
✨ The system will change you as much as you change it.

That is the nature of reciprocal systems. That is Ayni.

Welcome.
