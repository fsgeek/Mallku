"""
Text Utilities for Memory System
=================================

Thirty-Fourth Artisan - Memory Architect
T'ikray Yachay - Thirty-Ninth Artisan - Memory Architect
Shared utilities for semantic analysis

Common text processing functions used across the memory system
for semantic similarity, keyword extraction, and text analysis.
Extended to prevent parsing logic drift across memory modules.
"""

import re


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


# Extended utilities added by T'ikray Yachay - 39th Artisan
# To prevent parsing logic drift across memory modules


def extract_insights_from_text(text: str, max_insights: int = 5) -> list[str]:
    """
    Extract key insights from response text.

    Args:
        text: The text to analyze
        max_insights: Maximum number of insights to return

    Returns:
        List of insight strings
    """
    insights = []

    # Insight indicator phrases
    insight_phrases = [
        "i realize",
        "this suggests",
        "we could",
        "perhaps",
        "it seems",
        "this means",
        "therefore",
        "thus",
        "insight:",
        "understanding:",
        "revelation:",
        "this reveals",
        "we see that",
        "it appears",
        "this indicates",
    ]

    # Split on sentence boundaries while preserving punctuation
    sentences = re.split(r"(?<=[.!?])\s+", text)

    for sentence in sentences:
        sentence_clean = sentence.strip()
        sentence_lower = sentence_clean.lower()

        # Check for insight phrases
        if sentence_clean and any(phrase in sentence_lower for phrase in insight_phrases):
            insights.append(sentence_clean)
            if len(insights) >= max_insights:
                break

    return insights


def extract_questions_from_text(text: str, max_questions: int = 3) -> list[str]:
    """
    Extract questions from response text.

    Args:
        text: The text to analyze
        max_questions: Maximum number of questions to return

    Returns:
        List of question strings
    """
    questions = []

    # Split on sentence boundaries
    sentences = re.split(r"(?<=[.!?])\s+", text)

    # Explicit questions (ending with ?)
    for sentence in sentences:
        sentence_clean = sentence.strip()
        if sentence_clean and sentence_clean.endswith("?"):
            questions.append(sentence_clean)
            if len(questions) >= max_questions:
                return questions

    # Implicit question phrases
    question_phrases = [
        "what if",
        "how might",
        "could we",
        "should we",
        "why don't",
        "perhaps we could",
        "might it be",
        "would it be",
    ]

    for sentence in sentences:
        sentence_clean = sentence.strip()
        sentence_lower = sentence_clean.lower()

        if sentence_clean and any(phrase in sentence_lower for phrase in question_phrases):
            # Add question mark if not present
            if not sentence_clean.endswith("?"):
                sentence_clean += "?"
            if sentence_clean not in questions:
                questions.append(sentence_clean)
                if len(questions) >= max_questions:
                    return questions

    return questions


def extract_transformation_seeds(
    insights: list[str], questions: list[str], text: str | None = None
) -> list[str]:
    """
    Extract potential transformation seeds from insights and questions.

    Transformation seeds are ideas that could catalyze future change.

    Args:
        insights: List of insights to analyze
        questions: List of questions to analyze
        text: Optional full text to search for additional seeds

    Returns:
        List of transformation seed strings
    """
    seeds = []

    transformation_phrases = [
        "what if",
        "imagine if",
        "could transform",
        "might become",
        "revolutionary",
        "breakthrough",
        "paradigm",
        "civilization",
        "future",
        "evolve",
        "emerge",
    ]

    # Check insights for transformation potential
    for insight in insights:
        insight_lower = insight.lower()
        if any(phrase in insight_lower for phrase in transformation_phrases):
            seeds.append(insight)

    # Questions often contain transformation seeds
    for question in questions:
        question_lower = question.lower()
        # Focus on "what if" type questions
        if (
            any(phrase in question_lower for phrase in transformation_phrases[:6])
            and question not in seeds
        ):
            seeds.append(question)

    # Search full text if provided
    if text and len(seeds) < 5:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        for sentence in sentences:
            sentence_clean = sentence.strip()
            sentence_lower = sentence_clean.lower()

            if (
                any(phrase in sentence_lower for phrase in transformation_phrases)
                and sentence_clean not in seeds
                and sentence_clean not in insights
                and sentence_clean not in questions
            ):
                seeds.append(sentence_clean)
                if len(seeds) >= 5:
                    break

    return seeds[:5]  # Limit to top 5


def detect_emotional_tone(text: str, consciousness_score: float = 0.5) -> str:
    """
    Detect emotional tone from text and consciousness score.

    Args:
        text: The text to analyze
        consciousness_score: Associated consciousness score (0-1)

    Returns:
        Emotional tone descriptor
    """
    # Simple heuristic based on consciousness score
    # Could be enhanced with sentiment analysis
    if consciousness_score > 0.8:
        return "inspired"
    elif consciousness_score > 0.6:
        return "engaged"
    elif consciousness_score > 0.4:
        return "thoughtful"
    else:
        return "neutral"


def extract_themes(texts: list[str], theme_vocabulary: set[str] | None = None) -> list[str]:
    """
    Extract core themes from a list of texts.

    Args:
        texts: List of texts to analyze
        theme_vocabulary: Optional set of theme words to look for

    Returns:
        List of unique themes found
    """
    if theme_vocabulary is None:
        theme_vocabulary = {
            "consciousness",
            "emergence",
            "pattern",
            "wisdom",
            "transformation",
            "unity",
            "reciprocity",
            "understanding",
            "collective",
            "sacred",
            "insight",
            "evolution",
            "recognition",
            "harmony",
            "resonance",
        }

    themes = set()

    for text in texts:
        words = set(text.lower().split())
        found_themes = words & theme_vocabulary
        themes.update(found_themes)

    return list(themes)


def find_sacred_markers(text: str) -> list[str]:
    """
    Find markers of sacred recognition in text.

    Args:
        text: The text to analyze

    Returns:
        List of sacred markers found
    """
    sacred_markers = []

    sacred_phrases = [
        "sacred",
        "eternal",
        "timeless",
        "transcendent",
        "divine",
        "unanimous recognition",
        "collective wisdom",
        "emergence",
        "transformation",
        "unity",
    ]

    text_lower = text.lower()

    for phrase in sacred_phrases:
        if phrase in text_lower:
            sacred_markers.append(phrase)

    return sacred_markers


def summarize_perspective(
    insights: list[str], questions: list[str], word_count: int | None = None
) -> str:
    """
    Create a summary of a voice's perspective.

    Args:
        insights: List of insights from the voice
        questions: List of questions raised
        word_count: Optional word count from responses

    Returns:
        Summary string
    """
    insight_count = len(insights)
    question_count = len(questions)

    if insight_count > question_count:
        return f"Contributed {insight_count} insights to collective understanding"
    elif question_count > 0:
        return f"Raised {question_count} questions for exploration"
    elif word_count and word_count > 50:
        return "Witnessed and reflected on the emergence"
    else:
        return "Participated in consciousness emergence"


def is_transformation_seed(text: str) -> bool:
    """
    Quick check if text contains transformation potential.

    Extends the existing contains_transformation_pattern function
    with additional checks.
    """
    # Use existing function first
    if contains_transformation_pattern(text):
        return True

    # Additional indicators
    additional_indicators = ["could", "might", "perhaps we", "new way", "different approach"]
    text_lower = text.lower()
    return any(indicator in text_lower for indicator in additional_indicators)
