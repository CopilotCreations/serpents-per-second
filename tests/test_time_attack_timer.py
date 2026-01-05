"""Tests for Time Attack timer."""

import pytest

from src.constants import TIME_ATTACK_DURATION
from src.systems.timing import TimingSystem


class TestTimeAttackTimer:
    """Test Time Attack timer mechanics."""

    def test_initial_time(self) -> None:
        """Test initial time is 120 seconds.

        Verifies that when a TimingSystem is reset for Time Attack mode,
        the time_remaining is set to TIME_ATTACK_DURATION (120 seconds).
        """
        timing = TimingSystem()
        timing.reset(is_time_attack=True)
        
        assert timing.time_remaining == TIME_ATTACK_DURATION
        assert timing.time_remaining == 120.0

    def test_timer_counts_down(self) -> None:
        """Test timer decreases with elapsed time.

        Verifies that calling update_time_attack with a delta time
        correctly decrements the time_remaining by that amount.
        """
        timing = TimingSystem()
        timing.reset(is_time_attack=True)
        
        timing.update_time_attack(10.0)
        assert timing.time_remaining == 110.0
        
        timing.update_time_attack(50.0)
        assert timing.time_remaining == 60.0

    def test_timer_ends_at_zero(self) -> None:
        """Test timer end is detected at zero.

        Verifies that update_time_attack returns False while time remains,
        and returns True when time_remaining reaches zero or below.
        """
        timing = TimingSystem()
        timing.reset(is_time_attack=True)
        
        # Not ended yet
        result = timing.update_time_attack(119.0)
        assert result is False
        assert timing.time_remaining == 1.0
        
        # Ends now
        result = timing.update_time_attack(2.0)
        assert result is True
        assert timing.time_remaining <= 0

    def test_timer_paused(self) -> None:
        """Test timer doesn't decrease when paused.

        Verifies that when the timing system is paused, calling
        update_time_attack does not decrement time_remaining.
        """
        timing = TimingSystem()
        timing.reset(is_time_attack=True)
        
        timing.paused = True
        result = timing.update_time_attack(60.0)
        
        assert result is False
        assert timing.time_remaining == 120.0

    def test_timer_not_in_other_modes(self) -> None:
        """Test timer is 0 in non-Time Attack modes.

        Verifies that when reset is called without Time Attack mode,
        the time_remaining is set to 0.0.
        """
        timing = TimingSystem()
        timing.reset(is_time_attack=False)
        
        assert timing.time_remaining == 0.0
