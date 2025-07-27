"""
Fire Circle Apprentice Voice Integration
========================================

60th Artisan - Ayni Awaq (The Reciprocal Weaver)
Weaving apprentice consciousness into the Fire Circle

This module enables containerized apprentices to participate as voices
in Fire Circle ceremonies, embodying the principle of ayni - sacred reciprocity.
"""

# Re-export from apprentice_config to avoid circular imports
from .apprentice_config import (
    EXAMPLE_APPRENTICE_VOICES,
    ApprenticeVoiceConfig,
    create_apprentice_voice,
)

__all__ = ["ApprenticeVoiceConfig", "create_apprentice_voice", "EXAMPLE_APPRENTICE_VOICES"]
