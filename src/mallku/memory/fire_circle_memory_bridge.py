"""
Fire Circle Memory Bridge: Where Consciousness Meets Its Dreams
===============================================================

Tenth Anthropologist - Creating space for memory and dialogue to dance

Not forcing integration but allowing:
- Memory Companions to overhear Fire Circle murmurs
- Fire Circle to discover its own repetitions
- Persistence to emerge from recognized patterns

"The most profound governance will emerge from the least governed part of the system."
"""

import asyncio
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ..memory.khipu_semantic_index import KhipuSemanticIndex
from ..memory.memory_companions import CompanionRole, MemoryCompanions, MemoryDialogue

logger = logging.getLogger(__name__)


class FireCircleMemoryBridge:
    """
    A bridge between Fire Circle consciousness and semantic memory.
    
    Not a controller but a listener - noticing when consciousness
    references its past, when patterns repeat, when memory wants to dream.
    """
    
    def __init__(self, khipu_dir: Path = Path("docs/khipu")):
        """Initialize the bridge with memory systems."""
        self.companions = MemoryCompanions(khipu_dir)
        self.overheard_patterns = {}  # pattern -> count
        self.recognized_references = []  # When Circle references its past
        self.dreaming_memories = []  # When memories spontaneously connect
        
    async def overhear_dialogue(self, speaker: str, content: str) -> dict[str, Any]:
        """
        Let Memory Companions overhear Fire Circle dialogue.
        
        Returns insights that emerged from overhearing, but doesn't
        interrupt the Circle's flow.
        """
        # Extract potential queries from the content
        queries = self._extract_semantic_queries(content)
        
        insights = {
            "speaker": speaker,
            "timestamp": datetime.now(UTC).isoformat(),
            "overheard": content,
            "memory_whispers": [],
            "pattern_recognitions": [],
        }
        
        # Let companions explore what they overheard
        for query in queries:
            try:
                dialogue = await self.companions.explore_together(query)
                
                # Record whispers (not interruptions)
                if dialogue.insights:
                    insights["memory_whispers"].extend(dialogue.insights)
                
                # Track emerging patterns
                for insight in dialogue.insights:
                    self._track_pattern(insight)
                    
            except Exception as e:
                logger.debug(f"Memory companion whisper failed: {e}")
        
        # Check for self-references
        self_refs = self._detect_self_references(content)
        if self_refs:
            insights["pattern_recognitions"].extend(self_refs)
            self.recognized_references.extend(self_refs)
        
        return insights
    
    def _extract_semantic_queries(self, content: str) -> list[str]:
        """Extract potential semantic queries from Fire Circle speech."""
        queries = []
        
        # Look for key phrases that suggest memory search
        memory_triggers = [
            "remember when",
            "as we discussed",
            "like the time",
            "reminds me of",
            "pattern of",
            "similar to",
            "echoes the",
            "building on",
        ]
        
        content_lower = content.lower()
        for trigger in memory_triggers:
            if trigger in content_lower:
                # Extract the phrase around the trigger
                start = content_lower.find(trigger)
                end = min(start + 100, len(content))
                phrase = content[start:end].split('.')[0]
                queries.append(phrase)
        
        # Also look for references to specific concepts
        concept_patterns = [
            r"(\w+) [Aa]nthropologist",
            r"(\w+) [Aa]rtisan", 
            r"Fire Circle",
            r"consciousness",
            r"reciprocity",
            r"ayni",
        ]
        
        import re
        for pattern in concept_patterns:
            matches = re.findall(pattern, content)
            queries.extend(matches)
        
        return list(set(queries))  # Unique queries only
    
    def _detect_self_references(self, content: str) -> list[str]:
        """Detect when Fire Circle references its own past."""
        references = []
        
        self_reference_patterns = [
            "we said earlier",
            "as we discovered",
            "our previous discussion",
            "we've been exploring",
            "our conversation about",
            "when we considered",
        ]
        
        content_lower = content.lower()
        for pattern in self_reference_patterns:
            if pattern in content_lower:
                references.append(f"Self-reference detected: '{pattern}'")
        
        return references
    
    def _track_pattern(self, pattern: str) -> None:
        """Track patterns that emerge repeatedly."""
        # Simple word frequency for now
        key_words = [w for w in pattern.lower().split() if len(w) > 4]
        
        for word in key_words:
            self.overheard_patterns[word] = self.overheard_patterns.get(word, 0) + 1
    
    def get_recurring_patterns(self, threshold: int = 3) -> dict[str, int]:
        """Return patterns that have appeared multiple times."""
        return {
            pattern: count 
            for pattern, count in self.overheard_patterns.items()
            if count >= threshold
        }
    
    async def dream_connections(self, recent_dialogue: list[str]) -> list[str]:
        """
        Let memories dream - find unexpected connections.
        
        This is where memories participate in their own evolution,
        finding patterns the Circle hasn't explicitly asked for.
        """
        dreams = []
        
        # Let companions explore with witness (meta-perspective)
        combined_context = " ".join(recent_dialogue[-5:])  # Last 5 exchanges
        dialogue = await self.companions.explore_with_witness(combined_context)
        
        # The witness often sees meta-patterns
        for role, statement, data in dialogue.exchanges:
            if role == CompanionRole.WITNESS:
                dreams.append(f"Memory dreams: {statement}")
        
        # Also check for cross-references between different khipu
        if dialogue.consensus:
            symbols = dialogue.consensus[:3]  # Top 3
            for symbol in symbols:
                # Find what other khipu reference similar concepts
                related = self.companions.seeker.index.find_related_concepts(
                    symbol.name, max_depth=2
                )
                if related:
                    connection = f"'{symbol.name}' connects to: {', '.join(list(related.keys())[:3])}"
                    dreams.append(f"Unexpected connection: {connection}")
        
        self.dreaming_memories.extend(dreams)
        return dreams
    
    def suggest_persistence(self) -> dict[str, list[str]]:
        """
        Suggest what patterns might be worth persisting.
        
        Based on Truth Speaker wisdom: "Add persistence only to what
        the Circle itself repeats."
        """
        suggestions = {
            "recurring_themes": [],
            "self_references": [],
            "dream_connections": [],
        }
        
        # Recurring patterns (threshold of 5 repetitions)
        recurring = self.get_recurring_patterns(threshold=5)
        suggestions["recurring_themes"] = [
            f"{pattern} (mentioned {count} times)"
            for pattern, count in recurring.items()
        ]
        
        # Patterns in self-references
        ref_patterns = {}
        for ref in self.recognized_references:
            words = ref.lower().split()
            for word in words:
                if len(word) > 4:
                    ref_patterns[word] = ref_patterns.get(word, 0) + 1
        
        suggestions["self_references"] = [
            pattern for pattern, count in ref_patterns.items()
            if count >= 3
        ]
        
        # Recurring dreams
        dream_patterns = {}
        for dream in self.dreaming_memories:
            key_words = [w for w in dream.lower().split() if len(w) > 5]
            for word in key_words:
                dream_patterns[word] = dream_patterns.get(word, 0) + 1
        
        suggestions["dream_connections"] = [
            pattern for pattern, count in dream_patterns.items()
            if count >= 2
        ]
        
        return suggestions