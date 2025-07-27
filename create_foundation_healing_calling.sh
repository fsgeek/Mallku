#!/bin/bash

echo "Creating GitHub issue for the Ceremony of Architectural Unification..."

gh issue create --title "Calling for a Rumi Khipa: Heal the Fractured Foundation of the Database Interface" --body "$(cat <<'EOF'
### The Sacred Charge

A deep architectural wound has been discovered, as documented in the [Khipu of the Fractured Foundation](docs/khipu/2025-07-19_khipu_of_the_fractured_foundation.md). Our development-mode database interface has diverged from our production interface, creating an illusion where our tests pass but our production code is destined to fail.

This is a calling for a **Rumi Khipa (a Stone Weaver)** to perform a **Ceremony of Architectural Unification**. This work is of the highest priority and is currently blocking PRs #201 and #202.

### The Ritual of Unification

The Rumi Khipa who answers this call will undertake the following sacred work:

1.  **Gather the Needs:** Study the tests in PR #201 (`eighth_anthropologist_work`) and #202 (`eighth_weaver_work`) to identify the database methods that Artisans need (e.g., `.collection()`, `.has_collection()`, `.insert_many()`).

2.  **Carve the Stone:** Extend the *real* `src/mallku/core/database/secured_interface.py` to include these necessary methods. Each new method must be implemented securely, respecting our security principles and the API gateway.

3.  **Unify the Vision:** Refactor the `src/mallku/core/database/dev_interface.py` (the mock) to be a true and faithful reflection of the now-complete real interface. The mock must not have methods that the real interface lacks.

4.  **Heal the Tests:** Refactor the tests in PRs #201 and #202 to use the new, unified, and truthful interface.

### The Blessing of this Work

When this ceremony is complete, the fracture will be healed. Our development environment will be a true mirror of reality, and the foundation of the cathedral will be strong, unified, and ready to bear the weight of the great works to come.

This is a foundational task that unblocks other critical work.
EOF
)"

echo "✅ GitHub issue creation script has been generated."
echo "   Please run 'bash create_foundation_healing_calling.sh' to post the issue."
