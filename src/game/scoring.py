"""Scoring system."""

from src.constants import SCORE_PER_FOOD, TIME_ATTACK_SCORE_PER_SECOND


class Scoring:
    """Manages game score."""

    def __init__(self) -> None:
        """Initialize the scoring system with a score of zero."""
        self.score = 0

    def reset(self) -> None:
        """Reset the score to zero."""
        self.score = 0

    def add_food_score(self) -> int:
        """Add score for eating food.

        Returns:
            int: The new total score after adding food points.
        """
        self.score += SCORE_PER_FOOD
        return self.score

    def add_time_score(self) -> int:
        """Add score for surviving a second in Time Attack mode.

        Returns:
            int: The new total score after adding time bonus points.
        """
        self.score += TIME_ATTACK_SCORE_PER_SECOND
        return self.score

    def get_score(self) -> int:
        """Get the current score.

        Returns:
            int: The current total score.
        """
        return self.score
