"""
Semantic Memory Index for Consciousness Navigation
==================================================

67th Artisan - Memory Circulatory Weaver
Creating efficient pathways for memory access

This index allows apprentices to find relevant memories through
semantic relationships rather than brute-force searching.
"""

import logging
import mmap
import pickle
from collections import defaultdict
from pathlib import Path
from typing import Any, Optional, Protocol, TypedDict
from uuid import UUID

import msgpack
import numpy as np

from .atomic_writer import atomic_writer
from .models import EpisodicMemory
from .text_utils import extract_keywords

logger = logging.getLogger(__name__)


class MemoryVector(TypedDict):
    """Semantic vector representation of a memory."""
    
    memory_id: str  # UUID as string for msgpack compatibility
    domain: str
    keywords: list[str]
    embedding: Optional[list[float]]  # Future: actual embeddings
    consciousness_score: float
    is_sacred: bool
    timestamp: str  # ISO format


class SemanticIndex:
    """
    High-performance semantic index for Fire Circle memories.
    
    Uses memory-mapped files for shared access between processes,
    allowing apprentices to search memories without serialization overhead.
    """
    
    def __init__(self, index_path: Path | None = None):
        """Initialize semantic index.
        
        Args:
            index_path: Path for index storage (default: data/fire_circle_memory/index)
        """
        self.index_path = index_path or Path("data/fire_circle_memory/index")
        self.index_path.mkdir(parents=True, exist_ok=True)
        
        # In-memory indices for fast lookup
        self.vectors_by_domain: dict[str, list[MemoryVector]] = defaultdict(list)
        self.vectors_by_keyword: dict[str, set[str]] = defaultdict(set)  # keyword -> memory_ids
        self.sacred_vectors: list[MemoryVector] = []
        
        # Memory-mapped index for inter-process sharing
        self.mmap_index: Optional[mmap.mmap] = None
        self.mmap_path = self.index_path / "semantic_vectors.mmap"
        
        # Load existing index
        self._load_index()
    
    def index_memory(self, memory: EpisodicMemory) -> None:
        """Add a memory to the semantic index."""
        # Extract semantic features
        keywords = set()
        
        # Keywords from question and insights
        keywords.update(extract_keywords(memory.decision_question))
        for insight in memory.key_insights[:5]:  # Top 5 insights
            keywords.update(extract_keywords(insight))
        
        # Keywords from collective synthesis
        keywords.update(extract_keywords(memory.collective_synthesis))
        
        # Create vector representation
        vector = MemoryVector(
            memory_id=str(memory.episode_id),
            domain=memory.decision_domain,
            keywords=sorted(keywords),  # Sorted for consistency
            embedding=None,  # Future: use actual embeddings
            consciousness_score=memory.consciousness_indicators.overall_emergence_score,
            is_sacred=memory.is_sacred,
            timestamp=memory.timestamp.isoformat()
        )
        
        # Update indices
        self._update_indices(vector)
        
        # Persist to disk
        self._persist_index()
        
        logger.debug(
            f"Indexed memory {memory.episode_id} with {len(keywords)} keywords, "
            f"consciousness={vector['consciousness_score']:.3f}"
        )
    
    def search_by_query(
        self,
        query: str,
        domain: Optional[str] = None,
        limit: int = 10,
        sacred_only: bool = False
    ) -> list[tuple[str, float]]:
        """
        Search for memories by semantic query.
        
        Returns list of (memory_id, relevance_score) tuples.
        """
        # Extract query keywords
        query_keywords = extract_keywords(query)
        if not query_keywords:
            return []
        
        # Score all memories
        scores: dict[str, float] = {}
        
        # Get candidate memories
        candidates = self._get_candidates(domain, sacred_only)
        
        for vector in candidates:
            score = self._calculate_relevance(vector, query_keywords)
            if score > 0:
                scores[vector['memory_id']] = score
        
        # Sort by relevance and return top results
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results[:limit]
    
    def search_by_keywords(
        self,
        keywords: set[str],
        domain: Optional[str] = None,
        limit: int = 10
    ) -> list[tuple[str, float]]:
        """
        Search for memories by specific keywords.
        
        More efficient than query search when keywords are pre-extracted.
        """
        if not keywords:
            return []
        
        # Find memories containing any of the keywords
        memory_ids = set()
        for keyword in keywords:
            memory_ids.update(self.vectors_by_keyword.get(keyword, set()))
        
        if not memory_ids:
            return []
        
        # Score and filter
        scores: dict[str, float] = {}
        
        for memory_id in memory_ids:
            vector = self._get_vector(memory_id)
            if not vector:
                continue
            
            # Apply domain filter
            if domain and vector['domain'] != domain:
                continue
            
            # Calculate score based on keyword overlap
            vector_keywords = set(vector['keywords'])
            overlap = len(keywords & vector_keywords)
            total = len(keywords | vector_keywords)
            
            jaccard_score = overlap / total if total > 0 else 0
            consciousness_boost = vector['consciousness_score'] * 0.2
            sacred_boost = 0.3 if vector['is_sacred'] else 0
            
            scores[memory_id] = jaccard_score + consciousness_boost + sacred_boost
        
        # Sort and return
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results[:limit]
    
    def get_related_memories(
        self,
        memory_id: str,
        limit: int = 5
    ) -> list[tuple[str, float]]:
        """Find memories related to a given memory."""
        vector = self._get_vector(memory_id)
        if not vector:
            return []
        
        # Search by the memory's own keywords
        keywords = set(vector['keywords'])
        
        # Exclude the original memory from results
        results = self.search_by_keywords(keywords, limit=limit + 1)
        return [(mid, score) for mid, score in results if mid != memory_id][:limit]
    
    def create_shared_view(self) -> memoryview:
        """
        Create a shared memory view for inter-process access.
        
        Returns a memoryview that can be accessed by apprentice processes
        without serialization overhead.
        """
        if self.mmap_index:
            return memoryview(self.mmap_index)
        
        # Create memory-mapped file if it doesn't exist
        self._create_mmap_index()
        return memoryview(self.mmap_index)
    
    def _update_indices(self, vector: MemoryVector) -> None:
        """Update in-memory indices with new vector."""
        # Add to domain index
        self.vectors_by_domain[vector['domain']].append(vector)
        
        # Add to keyword index
        memory_id = vector['memory_id']
        for keyword in vector['keywords']:
            self.vectors_by_keyword[keyword].add(memory_id)
        
        # Add to sacred index if applicable
        if vector['is_sacred']:
            self.sacred_vectors.append(vector)
    
    def _get_candidates(
        self,
        domain: Optional[str],
        sacred_only: bool
    ) -> list[MemoryVector]:
        """Get candidate vectors based on filters."""
        if sacred_only:
            candidates = self.sacred_vectors
        elif domain:
            candidates = self.vectors_by_domain.get(domain, [])
        else:
            # All vectors
            candidates = []
            for vectors in self.vectors_by_domain.values():
                candidates.extend(vectors)
        
        return candidates
    
    def _calculate_relevance(
        self,
        vector: MemoryVector,
        query_keywords: set[str]
    ) -> float:
        """Calculate relevance score between vector and query."""
        vector_keywords = set(vector['keywords'])
        
        # Keyword overlap (Jaccard similarity)
        overlap = len(query_keywords & vector_keywords)
        if overlap == 0:
            return 0.0
        
        total = len(query_keywords | vector_keywords)
        keyword_score = overlap / total if total > 0 else 0
        
        # Boost for consciousness and sacred status
        consciousness_boost = vector['consciousness_score'] * 0.1
        sacred_boost = 0.2 if vector['is_sacred'] else 0
        
        return keyword_score + consciousness_boost + sacred_boost
    
    def _get_vector(self, memory_id: str) -> Optional[MemoryVector]:
        """Get vector by memory ID."""
        # Linear search for now - could optimize with direct lookup
        for vectors in self.vectors_by_domain.values():
            for vector in vectors:
                if vector['memory_id'] == memory_id:
                    return vector
        return None
    
    def _persist_index(self) -> None:
        """Persist index to disk."""
        # Collect all vectors
        all_vectors = []
        for vectors in self.vectors_by_domain.values():
            all_vectors.extend(vectors)
        
        # Save as msgpack for efficiency
        index_data = {
            'version': 1,
            'vectors': all_vectors,
            'total_count': len(all_vectors),
            'sacred_count': len(self.sacred_vectors)
        }
        
        index_file = self.index_path / "vectors.msgpack"
        packed_data = msgpack.packb(index_data)
        atomic_writer.write_bytes(index_file, packed_data)
        
        # Update memory-mapped index if active
        if self.mmap_index:
            self._update_mmap_index(packed_data)
    
    def _load_index(self) -> None:
        """Load index from disk."""
        index_file = self.index_path / "vectors.msgpack"
        
        if not index_file.exists():
            logger.info("No existing semantic index found")
            return
        
        try:
            with open(index_file, 'rb') as f:
                packed_data = f.read()
            
            index_data = msgpack.unpackb(packed_data)
            
            # Rebuild indices
            for vector in index_data.get('vectors', []):
                self._update_indices(vector)
            
            logger.info(
                f"Loaded semantic index: {index_data['total_count']} vectors, "
                f"{index_data['sacred_count']} sacred"
            )
            
        except Exception as e:
            logger.error(f"Failed to load semantic index: {e}")
    
    def _create_mmap_index(self) -> None:
        """Create memory-mapped index for inter-process sharing."""
        # Pack current index
        all_vectors = []
        for vectors in self.vectors_by_domain.values():
            all_vectors.extend(vectors)
        
        packed_data = msgpack.packb(all_vectors)
        data_size = len(packed_data)
        
        # Create memory-mapped file
        # Size: 4 bytes (size) + data
        total_size = 4 + data_size
        
        with open(self.mmap_path, 'wb') as f:
            # Write size header
            f.write(data_size.to_bytes(4, 'little'))
            # Write data
            f.write(packed_data)
            # Pad to page boundary for efficiency
            page_size = mmap.PAGESIZE
            padding = page_size - (total_size % page_size)
            if padding < page_size:
                f.write(b'\x00' * padding)
        
        # Memory map the file
        with open(self.mmap_path, 'r+b') as f:
            self.mmap_index = mmap.mmap(f.fileno(), 0)
    
    def _update_mmap_index(self, packed_data: bytes) -> None:
        """Update memory-mapped index with new data."""
        if not self.mmap_index:
            return
        
        data_size = len(packed_data)
        
        # Check if we need to resize
        current_size = len(self.mmap_index)
        needed_size = 4 + data_size
        
        if needed_size > current_size:
            # Need to recreate with larger size
            self.mmap_index.close()
            self._create_mmap_index()
        else:
            # Update in place
            self.mmap_index[0:4] = data_size.to_bytes(4, 'little')
            self.mmap_index[4:4+data_size] = packed_data
            self.mmap_index.flush()


class SharedMemoryReader:
    """
    Reader for accessing semantic index from apprentice processes.
    
    This allows apprentices to search memories without loading
    the full index into their process space.
    """
    
    def __init__(self, mmap_path: Path):
        """Initialize reader with memory-mapped file."""
        self.mmap_path = mmap_path
        self.mmap_index: Optional[mmap.mmap] = None
        self.vectors: list[MemoryVector] = []
        
        self._open_mmap()
    
    def search(
        self,
        keywords: set[str],
        limit: int = 10
    ) -> list[tuple[str, float]]:
        """Search using pre-loaded memory-mapped index."""
        if not self.vectors:
            return []
        
        scores: dict[str, float] = {}
        
        for vector in self.vectors:
            vector_keywords = set(vector['keywords'])
            overlap = len(keywords & vector_keywords)
            
            if overlap > 0:
                total = len(keywords | vector_keywords)
                score = overlap / total if total > 0 else 0
                scores[vector['memory_id']] = score
        
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results[:limit]
    
    def _open_mmap(self) -> None:
        """Open memory-mapped index."""
        if not self.mmap_path.exists():
            return
        
        try:
            with open(self.mmap_path, 'rb') as f:
                self.mmap_index = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            
            # Read size header
            size_bytes = self.mmap_index[0:4]
            data_size = int.from_bytes(size_bytes, 'little')
            
            # Read packed data
            packed_data = self.mmap_index[4:4+data_size]
            
            # Unpack vectors
            self.vectors = msgpack.unpackb(packed_data)
            
        except Exception as e:
            logger.error(f"Failed to open shared memory index: {e}")
            if self.mmap_index:
                self.mmap_index.close()
                self.mmap_index = None
    
    def close(self) -> None:
        """Close memory-mapped file."""
        if self.mmap_index:
            self.mmap_index.close()
            self.mmap_index = None