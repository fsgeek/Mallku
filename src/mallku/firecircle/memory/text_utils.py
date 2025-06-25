"""
Text Utilities for Memory System
=================================

Thirty-Fourth Artisan - Memory Architect
Shared utilities for semantic analysis

Common text processing functions used across the memory system
for semantic similarity, keyword extraction, and text analysis.
"""



def semantic_similarity(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity between two texts.

    Simple implementation based on word overlap.
    Future versions could use embeddings or more sophisticated NLP.

    Args:
        text1: First text to compare
        text2: Second text to compare

    Returns:
        Similarity score between 0 and 1
    """
    if not text1 or not text2:
        return 0.0

    # Normalize and tokenize
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 or not words2:
        return 0.0

    # Calculate Jaccard similarity
    intersection = words1.intersection(words2)
    union = words1.union(words2)

    return len(intersection) / len(union)


def extract_keywords(text: str, min_length: int = 3) -> set[str]:
    """
    Extract meaningful keywords from text.

    Args:
        text: Text to extract keywords from
        min_length: Minimum word length to consider

    Returns:
        Set of keywords
    """
    # Common stop words to filter
    stop_words = {
        "the",
        "is",
        "at",
        "which",
        "on",
        "and",
        "a",
        "an",
        "as",
        "are",
        "was",
        "were",
        "be",
        "have",
        "has",
        "had",
        "to",
        "of",
        "in",
        "for",
        "with",
        "by",
        "from",
        "can",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
    }

    # Tokenize and filter
    words = text.lower().split()
    keywords = {
        word.strip(".,!?;:\"'")
        for word in words
        if len(word) >= min_length and word not in stop_words
    }

    return keywords


def keyword_overlap_score(keywords1: set[str], keywords2: set[str]) -> float:
    """
    Calculate overlap score between two keyword sets.

    Args:
        keywords1: First set of keywords
        keywords2: Second set of keywords

    Returns:
        Overlap score between 0 and 1
    """
    if not keywords1 or not keywords2:
        return 0.0

    intersection = keywords1.intersection(keywords2)
    smaller_set_size = min(len(keywords1), len(keywords2))

    return len(intersection) / smaller_set_size


def contains_transformation_pattern(text: str) -> bool:
    """
    Check if text contains transformation-indicating patterns.

    Args:
        text: Text to analyze

    Returns:
        True if transformation patterns detected
    """
    transformation_patterns = [
        "why don't",
        "what if",
        "imagine if",
        "transform",
        "revolutionary",
        "breakthrough",
        "paradigm",
        "fundamental shift",
        "new understanding",
        "changes everything",
        "never thought",
    ]

    text_lower = text.lower()
    return any(pattern in text_lower for pattern in transformation_patterns)


def extract_question_focus(question: str) -> set[str]:
    """
    Extract the main focus keywords from a question.

    Args:
        question: Question text

    Returns:
        Set of focus keywords
    """
    # Remove common question words
    question_words = {
        "what",
        "why",
        "how",
        "when",
        "where",
        "who",
        "which",
        "does",
        "do",
        "did",
        "can",
        "could",
        "should",
        "would",
    }

    keywords = extract_keywords(question)
    focus_keywords = keywords - question_words

    return focus_keywords


# Domain relationship mappings
DOMAIN_RELATIONSHIPS = {
    "architecture": ["governance", "consciousness", "structure"],
    "governance": ["architecture", "ethics", "reciprocity", "decision"],
    "consciousness": ["architecture", "transformation", "emergence"],
    "ethics": ["governance", "reciprocity", "wisdom"],
    "reciprocity": ["governance", "ethics", "ayni", "balance"],
    "transformation": ["consciousness", "architecture", "change"],
    "memory": ["consciousness", "wisdom", "continuity"],
    "companion": ["relationship", "bond", "human", "ai"],
}


def get_related_domains(domain: str) -> list[str]:
    """
    Get domains related to the given domain.

    Args:
        domain: Domain to find relations for

    Returns:
        List of related domains
    """
    return DOMAIN_RELATIONSHIPS.get(domain.lower(), [])
