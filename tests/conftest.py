"""Pytest configuration for Mallku test suite.

This file ensures that the repository root is present on ``sys.path``
*before* any test modules are imported.  Several tests perform

    import src.mallku ...

and those imports can fail when the working directory during test
collection is a nested directory (e.g. ``tests/`` or
``tests/consciousness``).  Adding the project root to ``sys.path``
guarantees that the top-level ``src`` package is discoverable from any
working directory.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

# Resolve the repository root (two levels up from this file)
ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"

# Prepend to ``sys.path`` so it takes precedence over installed packages
# Ensure both root and ``src`` are importable, with ``src`` first so that
# ``import mallku`` works without needing ``import src.mallku`` indirection.
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(ROOT_DIR))

# Remove *other* Mallku copies that might be earlier on the import path
# Remove *other* Mallku copies (both root and src) that might shadow the
# local checkout.
_ALT_ROOT = ROOT_DIR.parent / "Mallku"
UNWANTED_PATHS = {
    str(_ALT_ROOT),
    str(_ALT_ROOT / "src"),
}

sys.path[:] = [p for p in sys.path if p not in UNWANTED_PATHS]

# ---------------------------------------------------------------------------
# Ensure compatibility shims are present even if an older copy of Mallku is
# already on the interpreter path (e.g. from a developer’s global
# installation).  By importing and patching after we have manipulated
# ``sys.path`` we guarantee that the *local* source tree takes
# precedence.
# ---------------------------------------------------------------------------


# Reload the top-level package so it is sourced from the local checkout
if "mallku" in sys.modules:
    importlib.reload(sys.modules["mallku"])

# Patch reciprocity tracker alias if required
try:
    tracker_mod = importlib.import_module("mallku.reciprocity.tracker")
    if not hasattr(tracker_mod, "ReciprocityTracker") and hasattr(
        tracker_mod, "SecureReciprocityTracker"
    ):
        tracker_mod.ReciprocityTracker = tracker_mod.SecureReciprocityTracker  # type: ignore[attr-defined]
except ImportError:
    # Module might not be available yet; individual tests will fail and
    # make the missing dependency obvious.  We keep the safety net
    pass
