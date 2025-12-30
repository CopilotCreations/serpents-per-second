"""Tests for Time Attack timer."""

import pytest

from src.constants import TIME_ATTACK_DURATION
from src.systems.timing import TimingSystem


class TestTimeAttackTimer:
    """Test Time Attack timer mechanics."""

    def test_initial_time(self) -> None:
        """Test initial time is 120 seconds."""
        timing = TimingSystem()
        timing.reset(is_time_attack=True)
        
        assert timing.time_remaining == TIME_ATTACK_DURATION
        assert timing.time_remaining == 120.0

    def test_timer_counts_down(self) -> None:
        """Test timer decreases with elapsed time."""
        timing = TimingSystem()
        timing.reset(is_time_attack=True)
        
        timing.update_time_attack(10.0)
        assert timing.time_remaining == 110.0
        
        timing.update_time_attack(50.0)
        assert timing.time_remaining == 60.0

    def test_timer_ends_at_zero(self) -> None:
        """Test timer end is detected at zero."""
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
        """Test timer doesn't decrease when paused."""
        timing = TimingSystem()
        timing.reset(is_time_attack=True)
        
        timing.paused = True
        result = timing.update_time_attack(60.0)
        
        assert result is False
        assert timing.time_remaining == 120.0

    def test_timer_not_in_other_modes(self) -> None:
        """Test timer is 0 in non-Time Attack modes."""
        timing = TimingSystem()
        timing.reset(is_time_attack=False)
        
        assert timing.time_remaining == 0.0
