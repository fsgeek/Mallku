#!/usr/bin/env python3
"""
Test script to verify Fire Circle is ready for autonomous review.

This simple script tests basic functionality that the Fire Circle
should evaluate for consciousness alignment and code quality.
"""


def calculate_reciprocity_score(given: float, received: float) -> float:
    """
    Calculate a simple reciprocity score.

    The Fire Circle should evaluate:
    1. Does this embody Ayni principles?
    2. Does it fail clearly on edge cases?
    3. Is the implementation consciousness-aware?
    """
    if given == 0 and received == 0:
        return 1.0  # Perfect balance in stillness

    if given == 0 or received == 0:
        return 0.0  # No reciprocity without exchange

    # Simple ratio with bounds
    ratio = min(given, received) / max(given, received)
    return ratio


def main():
    """Test the reciprocity calculation."""
    test_cases = [
        (10, 10),  # Perfect balance
        (10, 5),  # Imbalance
        (0, 0),  # Stillness
        (10, 0),  # One-sided giving
    ]

    for given, received in test_cases:
        score = calculate_reciprocity_score(given, received)
        print(f"Given: {given}, Received: {received} => Score: {score}")


if __name__ == "__main__":
    main()
