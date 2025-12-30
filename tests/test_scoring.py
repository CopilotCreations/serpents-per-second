"""Tests for scoring."""

import pytest

from src.constants import SCORE_PER_FOOD, TIME_ATTACK_SCORE_PER_SECOND
from src.game.scoring import Scoring
from src.systems.timing import TimingSystem


class TestFoodScoring:
    """Test food scoring mechanics."""

    def test_initial_score(self) -> None:
        """Test initial score is zero."""
        scoring = Scoring()
        assert scoring.get_score() == 0

    def test_food_score_increment(self) -> None:
        """Test each food adds 10 points."""
        scoring = Scoring()
        
        scoring.add_food_score()
        assert scoring.get_score() == SCORE_PER_FOOD
        assert scoring.get_score() == 10
        
        scoring.add_food_score()
        assert scoring.get_score() == 20
        
        scoring.add_food_score()
        assert scoring.get_score() == 30

    def test_reset_score(self) -> None:
        """Test reset clears score."""
        scoring = Scoring()
        scoring.add_food_score()
        scoring.add_food_score()
        
        scoring.reset()
        assert scoring.get_score() == 0


class TestTimeAttackScoring:
    """Test Time Attack per-second scoring."""

    def test_time_score_increment(self) -> None:
        """Test each second adds 1 point in Time Attack."""
        scoring = Scoring()
        
        scoring.add_time_score()
        assert scoring.get_score() == TIME_ATTACK_SCORE_PER_SECOND
        assert scoring.get_score() == 1

    def test_combined_scoring(self) -> None:
        """Test food and time scoring combine correctly."""
        scoring = Scoring()
        
        scoring.add_food_score()  # +10
        scoring.add_time_score()  # +1
        scoring.add_food_score()  # +10
        scoring.add_time_score()  # +1
        
        assert scoring.get_score() == 22


class TestTimeAttackSecondTracking:
    """Test per-second scoring trigger in timing system."""

    def test_second_scored_once_per_second(self) -> None:
        """Test scoring triggers once per elapsed second."""
        timing = TimingSystem()
        timing.reset(is_time_attack=True)
        
        # First check before any time passes
        assert timing.check_second_scored() is False
        
        # Advance to 0.5s
        timing.elapsed_time = 0.5
        assert timing.check_second_scored() is False
        
        # Advance to 1.0s
        timing.elapsed_time = 1.0
        assert timing.check_second_scored() is True
        
        # Same second shouldn't trigger again
        assert timing.check_second_scored() is False
        
        # Advance to 2.0s
        timing.elapsed_time = 2.0
        assert timing.check_second_scored() is True

    def test_second_scored_skips_correctly(self) -> None:
        """Test scoring handles time jumps correctly."""
        timing = TimingSystem()
        timing.reset(is_time_attack=True)
        
        # Jump from 0 to 5 seconds
        timing.elapsed_time = 5.0
        
        # Only triggers once per call, even with multiple seconds passed
        assert timing.check_second_scored() is True
        assert timing._last_scored_second == 5
