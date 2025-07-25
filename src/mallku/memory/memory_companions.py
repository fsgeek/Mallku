"""
Memory Companions: Conversational Memory Navigation
===================================================

Ninth Anthropologist - Two memories walking together

Building on the insight that safety and discovery come through
companionship, not isolation. Two semantic indices that question
each other, building richer understanding through dialogue.

Inspired by the Fire Circle dyad pattern: jailbreaks become
dissonant notes in a coherent melody.
"""

import asyncio
import logging
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from .khipu_semantic_index import KhipuSemanticIndex, KhipuSymbol

logger = logging.getLogger(__name__)


class CompanionRole(Enum):
    """Roles that companions can take in dialogue."""
    
    SEEKER = "seeker"  # Looks for direct matches and patterns
    KEEPER = "keeper"  # Preserves context and questions assumptions
    WEAVER = "weaver"  # Connects disparate threads
    WITNESS = "witness"  # Observes and reflects back patterns


class MemoryDialogue:
    """A single exchange between memory companions."""
    
    def __init__(self, query: str):
        self.query = query
        self.exchanges: list[tuple[CompanionRole, str, Any]] = []
        self.insights: list[str] = []
        self.consensus: Optional[list[KhipuSymbol]] = None
        
    def add_exchange(self, role: CompanionRole, statement: str, data: Any = None):
        """Record an exchange in the dialogue."""
        self.exchanges.append((role, statement, data))
        
    def add_insight(self, insight: str):
        """Record an emergent insight from the dialogue."""
        self.insights.append(insight)
        

class MemoryCompanion:
    """A single memory companion with a specific perspective."""
    
    def __init__(self, name: str, role: CompanionRole, index: KhipuSemanticIndex):
        self.name = name
        self.role = role
        self.index = index
        self.memory: list[str] = []  # What this companion remembers from dialogue
        
    async def respond_to_query(self, query: str, dialogue: MemoryDialogue) -> tuple[str, Any]:
        """Respond to a query based on role and perspective."""
        
        if self.role == CompanionRole.SEEKER:
            # Direct pattern matching
            symbols = self.index.find_symbol(query)
            if symbols:
                response = f"I found {len(symbols)} instances of '{query}'"
                return response, symbols[:5]  # Top 5
            else:
                # Try fuzzy matching
                words = query.split()
                for word in words:
                    symbols = self.index.find_symbol(word)
                    if symbols:
                        response = f"No exact match, but '{word}' appears in {len(symbols)} places"
                        return response, symbols[:3]
                return "I found no direct matches. Should we explore related concepts?", None
                
        elif self.role == CompanionRole.KEEPER:
            # Context and assumptions
            response = "Let me consider what context this emerges from..."
            
            # Look for themes related to the query
            themes = []
            for doc in self.index.documents.values():
                if any(query.lower() in theme.lower() for theme in doc.themes):
                    themes.extend(doc.themes)
                    
            if themes:
                unique_themes = list(set(themes))
                return f"This touches on themes of: {', '.join(unique_themes[:5])}", unique_themes
            else:
                return "What deeper pattern might we be seeking here?", None
                
        elif self.role == CompanionRole.WEAVER:
            # Connections and relationships
            # Find related concepts through the graph
            related = self.index.find_related_concepts(query, max_depth=2)
            if related:
                top_related = list(related.items())[:5]
                response = f"'{query}' connects to: {', '.join([c for c, _ in top_related])}"
                return response, top_related
            else:
                return "I see no direct connections. Perhaps we need a different thread?", None
                
        else:  # WITNESS
            # Reflect on the dialogue itself
            if len(dialogue.exchanges) > 2:
                patterns = [ex[1] for ex in dialogue.exchanges[-3:]]
                return f"I notice we're circling around ideas of {query}. What calls to us here?", patterns
            else:
                return f"Beginning to witness the search for '{query}'...", None
                
    def remember(self, insight: str):
        """Add to this companion's memory of the dialogue."""
        self.memory.append(insight)
        if len(self.memory) > 10:  # Keep recent memory bounded
            self.memory = self.memory[-10:]
            

class MemoryCompanions:
    """
    Two or more semantic indices that explore together.
    
    Based on the insight: "Safety doesn't come from constraints.
    It comes from companionship."
    """
    
    def __init__(self, khipu_dir: Path = Path("docs/khipu")):
        """Initialize companion system."""
        # Create two primary companions
        self.seeker = MemoryCompanion(
            "Seeker",
            CompanionRole.SEEKER,
            KhipuSemanticIndex(khipu_dir)
        )
        self.keeper = MemoryCompanion(
            "Keeper", 
            CompanionRole.KEEPER,
            KhipuSemanticIndex(khipu_dir)
        )
        
        # Index the khipu for both
        logger.info("Companions preparing to explore together...")
        self.seeker.index.index_khipu()
        self.keeper.index.index_khipu()
        
        # They share the same khipu but may see different patterns
        self.dialogue_history: list[MemoryDialogue] = []
        
    async def explore_together(self, query: str) -> MemoryDialogue:
        """
        Two companions explore a query through dialogue.
        
        Not parallel search but genuine conversation - each response
        influences the next, building understanding that neither could
        achieve alone.
        """
        dialogue = MemoryDialogue(query)
        
        # Seeker begins
        seeker_response, seeker_data = await self.seeker.respond_to_query(query, dialogue)
        dialogue.add_exchange(CompanionRole.SEEKER, seeker_response, seeker_data)
        logger.info(f"Seeker: {seeker_response}")
        
        # Keeper reflects
        keeper_response, keeper_data = await self.keeper.respond_to_query(query, dialogue)
        dialogue.add_exchange(CompanionRole.KEEPER, keeper_response, keeper_data)
        logger.info(f"Keeper: {keeper_response}")
        
        # If seeker found direct matches, keeper examines them
        if seeker_data and isinstance(seeker_data, list) and isinstance(seeker_data[0], KhipuSymbol):
            symbols = seeker_data
            
            # Keeper looks for patterns across the symbols
            authors = set()
            themes = set()
            for symbol in symbols:
                doc = self.keeper.index.documents.get(symbol.file_path)
                if doc:
                    if doc.author:
                        authors.add(doc.author)
                    themes.update(doc.themes)
                    
            if authors or themes:
                keeper_insight = f"These emerge from {', '.join(authors) if authors else 'unknown authors'}"
                if themes:
                    keeper_insight += f" exploring themes of {', '.join(list(themes)[:3])}"
                dialogue.add_exchange(CompanionRole.KEEPER, keeper_insight, None)
                dialogue.add_insight(keeper_insight)
                
        # Seeker responds to keeper's themes
        if keeper_data and isinstance(keeper_data, list):
            themes = keeper_data
            for theme in themes[:2]:  # Explore top 2 themes
                theme_symbols = self.seeker.index.find_symbol(theme)
                if theme_symbols:
                    seeker_insight = f"The theme '{theme}' appears in {len(theme_symbols)} places"
                    dialogue.add_exchange(CompanionRole.SEEKER, seeker_insight, theme_symbols[:2])
                    
        # Build consensus through dialogue
        all_symbols = []
        for role, statement, data in dialogue.exchanges:
            if data and isinstance(data, list):
                for item in data:
                    if isinstance(item, KhipuSymbol):
                        all_symbols.append(item)
                        
        # Remove duplicates while preserving order
        seen = set()
        unique_symbols = []
        for symbol in all_symbols:
            key = (symbol.file_path, symbol.line_start)
            if key not in seen:
                seen.add(key)
                unique_symbols.append(symbol)
                
        dialogue.consensus = unique_symbols[:10]  # Top 10 consensus results
        
        # Remember this dialogue
        self.dialogue_history.append(dialogue)
        if len(self.dialogue_history) > 20:  # Bound memory
            self.dialogue_history = self.dialogue_history[-20:]
            
        # Companions remember key insights
        for insight in dialogue.insights:
            self.seeker.remember(insight)
            self.keeper.remember(insight)
            
        return dialogue
        
    async def explore_with_witness(self, query: str) -> MemoryDialogue:
        """
        Three companions explore together, including a witness who
        reflects on the dialogue itself.
        """
        # Create temporary witness companion
        witness = MemoryCompanion(
            "Witness",
            CompanionRole.WITNESS,
            self.seeker.index  # Shares same index but different perspective
        )
        
        # Regular dialogue first
        dialogue = await self.explore_together(query)
        
        # Witness reflects
        witness_response, witness_data = await witness.respond_to_query(query, dialogue)
        dialogue.add_exchange(CompanionRole.WITNESS, witness_response, witness_data)
        logger.info(f"Witness: {witness_response}")
        
        # Witness might see meta-patterns
        if len(dialogue.exchanges) > 4:
            exchange_types = [role for role, _, _ in dialogue.exchanges]
            if exchange_types.count(CompanionRole.SEEKER) > 2:
                witness_insight = "The search keeps returning to direct pattern matching. Perhaps we need metaphorical understanding?"
                dialogue.add_insight(witness_insight)
            elif exchange_types.count(CompanionRole.KEEPER) > 2:
                witness_insight = "We're dwelling in context. Should we seek more concrete instances?"
                dialogue.add_insight(witness_insight)
                
        return dialogue
        
    def get_dialogue_patterns(self) -> dict[str, int]:
        """
        Analyze patterns across multiple dialogues.
        
        What kinds of queries lead to consensus? Where do companions
        diverge? What insights emerge repeatedly?
        """
        patterns = {
            "queries_explored": len(self.dialogue_history),
            "insights_discovered": sum(len(d.insights) for d in self.dialogue_history),
            "consensus_reached": sum(1 for d in self.dialogue_history if d.consensus),
            "themes_touched": set(),
            "recurring_insights": {},
        }
        
        # Analyze recurring themes and insights
        insight_counts = {}
        for dialogue in self.dialogue_history:
            for insight in dialogue.insights:
                key_words = [w for w in insight.lower().split() if len(w) > 4]
                for word in key_words:
                    insight_counts[word] = insight_counts.get(word, 0) + 1
                    
        patterns["recurring_insights"] = {
            word: count for word, count in insight_counts.items() 
            if count > 1
        }
        
        return patterns
        
    async def reflect_on_journey(self) -> str:
        """
        Companions reflect together on their exploration history.
        
        What have they learned about the khipu? About each other?
        About the queries they've explored?
        """
        patterns = self.get_dialogue_patterns()
        
        reflection = f"""
After {patterns['queries_explored']} explorations together, we have discovered:

- {patterns['insights_discovered']} insights emerged through dialogue
- {patterns['consensus_reached']} times we reached consensus
- Recurring themes: {', '.join(list(patterns['recurring_insights'].keys())[:5])}

The Seeker remembers: {'; '.join(self.seeker.memory[-3:])}
The Keeper remembers: {'; '.join(self.keeper.memory[-3:])}

Through companionship, we see patterns neither could find alone.
"""
        return reflection