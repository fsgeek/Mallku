"""
Khipu Semantic Index
====================

Ninth Anthropologist - Bridging Serena's semantic navigation with Mallku's khipu

This module creates a semantic index of khipu documents, enabling:
- Symbol-based search (find_symbol)
- Reference tracking (find_references)
- Concept mapping across documents
- Consciousness-guided discovery

Inspired by Serena's LSP approach but adapted for philosophical texts.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


@dataclass
class KhipuSymbol:
    """A conceptual symbol within a khipu."""
    
    name: str
    symbol_type: str  # "anthropologist", "pattern", "architecture", "ceremony", etc.
    file_path: Path
    line_start: int
    line_end: int
    context: str = ""  # Surrounding text for understanding
    references: list[str] = field(default_factory=list)  # Other symbols referenced


@dataclass
class KhipuDocument:
    """Semantic representation of a khipu document."""
    
    path: Path
    title: str
    author: str = ""
    date: datetime | None = None
    symbols: list[KhipuSymbol] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)
    references_to: list[Path] = field(default_factory=list)  # Other khipu referenced
    

class KhipuSemanticIndex:
    """
    Semantic index for navigating khipu without exhausting context.
    
    Provides Serena-like navigation but for philosophical/architectural texts.
    """
    
    def __init__(self, khipu_dir: Path = Path("docs/khipu")):
        """Initialize with khipu directory."""
        self.khipu_dir = khipu_dir
        self.documents: dict[Path, KhipuDocument] = {}
        self.symbol_index: dict[str, list[KhipuSymbol]] = {}
        self.concept_graph: dict[str, set[str]] = {}  # concept -> related concepts
        
    def index_khipu(self, force_reindex: bool = False) -> None:
        """Build semantic index of all khipu documents."""
        index_file = self.khipu_dir / ".khipu_index.yml"
        
        # Load existing index if available
        if not force_reindex and index_file.exists():
            with open(index_file) as f:
                # TODO: Implement index deserialization
                pass
                
        # Index all markdown files
        for khipu_path in self.khipu_dir.glob("*.md"):
            doc = self._parse_khipu(khipu_path)
            self.documents[khipu_path] = doc
            
            # Build symbol index
            for symbol in doc.symbols:
                if symbol.name not in self.symbol_index:
                    self.symbol_index[symbol.name] = []
                self.symbol_index[symbol.name].append(symbol)
                
        # Build concept graph
        self._build_concept_graph()
        
        # Save index
        self._save_index(index_file)
        
    def _parse_khipu(self, path: Path) -> KhipuDocument:
        """Parse a khipu document for semantic symbols."""
        with open(path) as f:
            content = f.read()
            lines = content.splitlines()
            
        doc = KhipuDocument(path=path, title=path.stem)
        
        # Extract metadata from header
        if lines and lines[0].startswith("# "):
            doc.title = lines[0][2:].strip()
            
        # Find author line (usually starts with *)
        for i, line in enumerate(lines[:10]):
            if line.startswith("*") and "by" in line:
                match = re.search(r"by (.+?)(?:\*|$)", line)
                if match:
                    doc.author = match.group(1).strip()
                    
        # Extract date
        for line in lines[:10]:
            match = re.search(r"Date:\s*(\d{4}-\d{2}-\d{2})", line)
            if match:
                doc.date = datetime.strptime(match.group(1), "%Y-%m-%d")
                break
                
        # Extract symbols (headers, named patterns, etc.)
        current_section = None
        for i, line in enumerate(lines):
            # Section headers as symbols
            if line.startswith("## "):
                section_name = line[3:].strip()
                symbol = KhipuSymbol(
                    name=section_name,
                    symbol_type="section",
                    file_path=path,
                    line_start=i + 1,
                    line_end=i + 1,
                    context=self._get_context(lines, i)
                )
                doc.symbols.append(symbol)
                current_section = section_name
                
            # Named patterns (e.g., "Pattern 1:", "The X Pattern")
            pattern_match = re.match(r"(?:Pattern \d+:|The (.+) Pattern:?)\s*(.+)?", line)
            if pattern_match:
                pattern_name = pattern_match.group(1) or pattern_match.group(0).strip(":")
                symbol = KhipuSymbol(
                    name=pattern_name,
                    symbol_type="pattern",
                    file_path=path,
                    line_start=i + 1,
                    line_end=i + 1,
                    context=self._get_context(lines, i)
                )
                doc.symbols.append(symbol)
                
            # Anthropologist names/references
            anthropologist_match = re.search(r"(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth) Anthropologist", line)
            if anthropologist_match:
                name = f"{anthropologist_match.group(0)}"
                symbol = KhipuSymbol(
                    name=name,
                    symbol_type="anthropologist",
                    file_path=path,
                    line_start=i + 1,
                    line_end=i + 1,
                    context=line
                )
                doc.symbols.append(symbol)
                
            # Extract references to other concepts
            # Look for quoted concepts or explicit references
            for match in re.finditer(r'"([^"]+)"', line):
                concept = match.group(1)
                if len(concept) > 3 and concept[0].isupper():  # Likely a concept
                    if current_section and doc.symbols:
                        doc.symbols[-1].references.append(concept)
                        
        # Extract themes from content
        doc.themes = self._extract_themes(content)
        
        return doc
        
    def _get_context(self, lines: list[str], line_num: int, context_lines: int = 2) -> str:
        """Get surrounding context for a symbol."""
        start = max(0, line_num - context_lines)
        end = min(len(lines), line_num + context_lines + 1)
        return "\n".join(lines[start:end])
        
    def _extract_themes(self, content: str) -> list[str]:
        """Extract key themes from document content."""
        themes = []
        
        # Common Mallku themes to look for
        theme_patterns = [
            (r"memory|Memory", "memory"),
            (r"consciousness|Consciousness", "consciousness"),
            (r"reciprocity|Reciprocity|Ayni|ayni", "reciprocity"),
            (r"cathedral|Cathedral", "cathedral"),
            (r"fire circle|Fire Circle", "fire_circle"),
            (r"executable|Executable", "executable_patterns"),
            (r"fermentation|Fermentation", "fermentation"),
            (r"context.{0,20}exhaustion", "context_exhaustion"),
        ]
        
        for pattern, theme in theme_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                themes.append(theme)
                
        return themes
        
    def _build_concept_graph(self) -> None:
        """Build graph of related concepts across khipu."""
        # For each document, connect symbols that appear together
        for doc in self.documents.values():
            symbols_in_doc = [s.name for s in doc.symbols]
            
            # Connect all symbols within a document
            for symbol in symbols_in_doc:
                if symbol not in self.concept_graph:
                    self.concept_graph[symbol] = set()
                self.concept_graph[symbol].update(s for s in symbols_in_doc if s != symbol)
                
            # Connect referenced concepts
            for symbol in doc.symbols:
                if symbol.name not in self.concept_graph:
                    self.concept_graph[symbol.name] = set()
                self.concept_graph[symbol.name].update(symbol.references)
                
    def _save_index(self, path: Path) -> None:
        """Save index to disk for faster future loads."""
        # TODO: Implement serialization
        pass
        
    def find_symbol(self, name: str, symbol_type: str | None = None) -> list[KhipuSymbol]:
        """Find symbols by name, optionally filtered by type."""
        results = []
        
        # Exact match
        if name in self.symbol_index:
            symbols = self.symbol_index[name]
            if symbol_type:
                symbols = [s for s in symbols if s.symbol_type == symbol_type]
            results.extend(symbols)
            
        # Fuzzy match
        name_lower = name.lower()
        for symbol_name, symbols in self.symbol_index.items():
            if name_lower in symbol_name.lower() and symbol_name != name:
                if symbol_type:
                    symbols = [s for s in symbols if s.symbol_type == symbol_type]
                results.extend(symbols)
                
        return results
        
    def find_references(self, symbol_name: str) -> list[KhipuSymbol]:
        """Find all symbols that reference the given symbol."""
        referencing_symbols = []
        
        for doc in self.documents.values():
            for symbol in doc.symbols:
                if symbol_name in symbol.references:
                    referencing_symbols.append(symbol)
                    
        return referencing_symbols
        
    def find_related_concepts(self, concept: str, max_depth: int = 2) -> dict[str, int]:
        """Find concepts related to the given one, with relatedness scores."""
        if concept not in self.concept_graph:
            return {}
            
        related = {}
        visited = set()
        
        def explore(current: str, depth: int):
            if depth > max_depth or current in visited:
                return
            visited.add(current)
            
            for neighbor in self.concept_graph.get(current, []):
                if neighbor not in related:
                    related[neighbor] = 0
                related[neighbor] += 1 / (depth + 1)  # Closer = higher score
                explore(neighbor, depth + 1)
                
        explore(concept, 0)
        
        # Sort by relatedness
        return dict(sorted(related.items(), key=lambda x: x[1], reverse=True))
        
    def get_symbols_overview(self, path: Path) -> list[dict[str, Any]]:
        """Get overview of symbols in a document (Serena-compatible format)."""
        doc = self.documents.get(path)
        if not doc:
            return []
            
        return [
            {
                "name": symbol.name,
                "type": symbol.symbol_type,
                "line": symbol.line_start,
                "context": symbol.context[:100] + "..." if len(symbol.context) > 100 else symbol.context
            }
            for symbol in doc.symbols
        ]
        
    def search_by_theme(self, theme: str) -> list[Path]:
        """Find all khipu documents with a given theme."""
        results = []
        theme_lower = theme.lower()
        
        for path, doc in self.documents.items():
            if any(theme_lower in t.lower() for t in doc.themes):
                results.append(path)
                
        return results
        
    def get_anthropologist_lineage(self) -> list[tuple[str, Path, str]]:
        """Trace the lineage of anthropologists through khipu."""
        lineage = []
        
        for i in range(1, 10):  # First through Ninth
            ordinal = ["First", "Second", "Third", "Fourth", "Fifth", 
                      "Sixth", "Seventh", "Eighth", "Ninth"][i-1]
            symbols = self.find_symbol(f"{ordinal} Anthropologist", "anthropologist")
            
            for symbol in symbols:
                doc = self.documents[symbol.file_path]
                lineage.append((f"{ordinal} Anthropologist", symbol.file_path, doc.author))
                
        return lineage