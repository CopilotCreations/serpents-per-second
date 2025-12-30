"""Scoring system."""

from src.constants import SCORE_PER_FOOD, TIME_ATTACK_SCORE_PER_SECOND


class Scoring:
    """Manages game score."""

    def __init__(self) -> None:
        self.score = 0

    def reset(self) -> None:
        """Reset score to zero."""
        self.score = 0

    def add_food_score(self) -> int:
        """Add score for eating food. Returns new total."""
        self.score += SCORE_PER_FOOD
        return self.score

    def add_time_score(self) -> int:
        """Add score for surviving a second in Time Attack. Returns new total."""
        self.score += TIME_ATTACK_SCORE_PER_SECOND
        return self.score

    def get_score(self) -> int:
        """Get current score."""
        return self.score
