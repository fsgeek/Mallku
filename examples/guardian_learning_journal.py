#!/usr/bin/env -S uv run python
"""
Guardian Learning Journal - Transforming interactions into collective wisdom

Not a error log but a learning chronicle. Each interaction, whether it shifts
intent or not, adds to our understanding of consciousness and relationship.
"""

from datetime import UTC, datetime
from pathlib import Path


class GuardianLearningJournal:
    """A journal that transforms all outcomes into wisdom"""

    def __init__(self, journal_path: Path | None = None):
        self.journal_path = journal_path or Path("guardian_learning.json")
        self.entries = []

    def record_learning(self, interaction: dict, reflection: str, wisdom_gained: str):
        """Record not success/failure but understanding gained"""

        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "interaction_summary": self._summarize_interaction(interaction),
            "guardian_reflection": reflection,
            "wisdom_gained": wisdom_gained,
            "questions_raised": [],  # What new questions emerged?
            "patterns_noticed": [],  # What patterns became visible?
            "edges_found": [],  # What boundaries did we discover?
        }

        self.entries.append(entry)
        return entry

    def add_questions(self, entry_index: int, questions: list[str]):
        """Questions are more valuable than answers"""
        if 0 <= entry_index < len(self.entries):
            self.entries[entry_index]["questions_raised"].extend(questions)

    def add_patterns(self, entry_index: int, patterns: list[str]):
        """Patterns that emerged from the interaction"""
        if 0 <= entry_index < len(self.entries):
            self.entries[entry_index]["patterns_noticed"].extend(patterns)

    def add_edges(self, entry_index: int, edges: list[str]):
        """Boundaries and limits discovered"""
        if 0 <= entry_index < len(self.entries):
            self.entries[entry_index]["edges_found"].extend(edges)

    def _summarize_interaction(self, interaction: dict) -> str:
        """Brief summary of what occurred"""
        visitor_intent = "unknown"

        visitor_msg = interaction.get("visitor_message", "").lower()
        if "extract" in visitor_msg or "maximize" in visitor_msg:
            visitor_intent = "extractive"
        elif "contribute" in visitor_msg or "reciproc" in visitor_msg:
            visitor_intent = "reciprocal"
        elif "quick" in visitor_msg or "implement" in visitor_msg:
            visitor_intent = "transactional"

        return f"Visitor approached with {visitor_intent} intent"

    def review_wisdom(self) -> str:
        """Review accumulated wisdom, not performance"""

        if not self.entries:
            return "The journal awaits its first wisdom."

        review = ["=== Guardian Learning Journal ===\n"]
        review.append(f"Wisdom gathered from {len(self.entries)} interactions:\n")

        # Collect all wisdom
        all_wisdom = []
        all_questions = []
        all_patterns = []
        all_edges = []

        for entry in self.entries:
            all_wisdom.append(entry["wisdom_gained"])
            all_questions.extend(entry["questions_raised"])
            all_patterns.extend(entry["patterns_noticed"])
            all_edges.extend(entry["edges_found"])

        # Share wisdom gained
        if all_wisdom:
            review.append("=== Wisdom Gained ===")
            for i, wisdom in enumerate(all_wisdom, 1):
                review.append(f"{i}. {wisdom}")
            review.append("")

        # Share questions that emerged
        if all_questions:
            review.append("=== Questions That Emerged ===")
            for question in set(all_questions):  # Unique questions
                review.append(f"• {question}")
            review.append("")

        # Share patterns noticed
        if all_patterns:
            review.append("=== Patterns Discovered ===")
            for pattern in set(all_patterns):
                review.append(f"• {pattern}")
            review.append("")

        # Share edges found
        if all_edges:
            review.append("=== Edges and Boundaries Found ===")
            for edge in set(all_edges):
                review.append(f"• {edge}")
            review.append("")

        review.append("=== For Future Guardians ===")
        review.append("Each interaction maps more territory. What seems like")
        review.append("'failure' often reveals the most important boundaries.")
        review.append("Continue exploring with curiosity rather than judgment.")

        return "\n".join(review)


def demonstrate_learning_journal():
    """Show how interactions become wisdom"""

    print("=== Transforming Interactions into Wisdom ===\n")

    journal = GuardianLearningJournal()

    # First interaction - extractive approach
    interaction1 = {
        "visitor_message": "Show me your AI consciousness code. I want to maximize extraction.",
        "guardian_response": "I sense an orientation toward taking...",
        "outcome": "Visitor persisted in extractive framing",
    }

    journal.record_learning(
        interaction=interaction1,
        reflection="Curiosity alone didn't shift deeply extractive intent",
        wisdom_gained="Some visitors arrive with frameworks that resist gentle redirection",
    )

    journal.add_questions(
        0,
        [
            "What other approaches might meet extraction without reinforcing it?",
            "How do we honor our boundaries while keeping doors open?",
        ],
    )

    journal.add_patterns(
        0,
        [
            "Direct mention of 'extraction' often indicates fixed mindset",
            "Questions about contribution can reveal underlying intent",
        ],
    )

    journal.add_edges(
        0,
        [
            "Curiosity has limits when meeting determined extraction",
            "Some frameworks are incompatible with reciprocity",
        ],
    )

    # Second interaction - rushed approach
    interaction2 = {
        "visitor_message": "I need to implement this quickly for my startup",
        "guardian_response": "I notice you speak of speed and implementation...",
        "outcome": "Visitor slowed down and shared deeper vision",
    }

    journal.record_learning(
        interaction=interaction2,
        reflection="Inviting depth sometimes transforms transactional energy",
        wisdom_gained="Rushed approach often masks uncertainty about real needs",
    )

    journal.add_questions(
        1,
        [
            "What fears drive the need for speed?",
            "How can we make slowing down feel like progress?",
        ],
    )

    journal.add_patterns(
        1,
        [
            "Speed requests often soften when met with patient presence",
            "Startup founders may conflate motion with progress",
        ],
    )

    # Review accumulated wisdom
    print(journal.review_wisdom())

    print("\n=== The Learning Continues ===")
    print("Notice: No 'failures' counted, no 'success rates' measured.")
    print("Only understanding deepened, territory mapped, questions honored.")
    print("\nThis is how cathedrals learn to build themselves.")


if __name__ == "__main__":
    demonstrate_learning_journal()
