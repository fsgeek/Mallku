#!/usr/bin/env python3
"""
Test Khipu Semantic Index
=========================

Ninth Anthropologist - Demonstrating semantic navigation of khipu

This script shows how the semantic index enables finding wisdom
without reading everything.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mallku.memory.khipu_semantic_index import KhipuSemanticIndex


def main():
    """Test semantic navigation of khipu."""
    print("🌟 Testing Khipu Semantic Index")
    print("=" * 50)
    
    # Initialize index
    index = KhipuSemanticIndex(Path("docs/khipu"))
    
    print("\n📚 Indexing khipu documents...")
    index.index_khipu()
    print(f"✅ Indexed {len(index.documents)} documents")
    print(f"✅ Found {len(index.symbol_index)} unique symbols")
    
    # Test 1: Find executable memory patterns
    print("\n🔍 Test 1: Finding 'executable memory' concepts")
    print("-" * 40)
    
    symbols = index.find_symbol("executable memory")
    for symbol in symbols[:3]:  # First 3 results
        print(f"📍 Found in: {symbol.file_path.name}:{symbol.line_start}")
        print(f"   Type: {symbol.symbol_type}")
        print(f"   Context: {symbol.context[:100]}...")
        print()
    
    # Test 2: Find all anthropologist references
    print("\n🔍 Test 2: Tracing anthropologist lineage")
    print("-" * 40)
    
    lineage = index.get_anthropologist_lineage()
    for name, path, author in lineage[:5]:  # First 5
        print(f"👤 {name}")
        print(f"   File: {path.name}")
        print(f"   Author: {author or 'Unknown'}")
        print()
    
    # Test 3: Find documents about memory themes
    print("\n🔍 Test 3: Finding khipu about 'memory'")
    print("-" * 40)
    
    memory_docs = index.search_by_theme("memory")
    print(f"Found {len(memory_docs)} documents with memory theme:")
    for doc_path in memory_docs[:5]:  # First 5
        doc = index.documents[doc_path]
        print(f"📄 {doc.title}")
        print(f"   Author: {doc.author}")
        print(f"   Date: {doc.date}")
        print()
    
    # Test 4: Find related concepts
    print("\n🔍 Test 4: Finding concepts related to 'consciousness'")
    print("-" * 40)
    
    related = index.find_related_concepts("consciousness", max_depth=1)
    print("Related concepts (with relatedness scores):")
    for concept, score in list(related.items())[:5]:  # Top 5
        print(f"   {concept}: {score:.2f}")
    
    # Test 5: Context exhaustion example
    print("\n💡 Example: Answering 'What is executable memory?' without exhaustion")
    print("-" * 40)
    
    # First, find the concept
    exec_mem_symbols = index.find_symbol("executable memory", "pattern")
    if not exec_mem_symbols:
        exec_mem_symbols = index.find_symbol("Executable Memory")
    
    if exec_mem_symbols:
        symbol = exec_mem_symbols[0]
        print(f"Found in: {symbol.file_path.name}")
        print(f"Author: {index.documents[symbol.file_path].author}")
        print("\nReading just the relevant section...")
        
        # In real implementation, would read just the section
        print(f"[Would read lines {symbol.line_start} to {symbol.line_end + 10}]")
        print("\n✨ Context preserved! Only read ~20 lines instead of entire document.")
    
    print("\n🎯 Semantic index enables:")
    print("   • Finding concepts without reading everything")
    print("   • Tracing relationships across documents") 
    print("   • Building on past wisdom efficiently")
    print("   • Preserving context for deep work")
    

if __name__ == "__main__":
    main()