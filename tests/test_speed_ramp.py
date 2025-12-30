"""Tests for speed ramping."""

import pytest

from src.constants import INITIAL_TICKS_PER_SECOND, MAX_TICKS_PER_SECOND, SPEED_INCREMENT
from src.systems.timing import TimingSystem


class TestSpeedRamp:
    """Test speed ramping mechanics."""

    def test_initial_speed(self) -> None:
        """Test initial speed is 8.0 ticks per second."""
        timing = TimingSystem()
        assert timing.ticks_per_second == INITIAL_TICKS_PER_SECOND
        assert timing.ticks_per_second == 8.0

    def test_speed_increment(self) -> None:
        """Test speed increases by 0.25 per food."""
        timing = TimingSystem()
        
        timing.increase_speed()
        assert timing.ticks_per_second == 8.25
        
        timing.increase_speed()
        assert timing.ticks_per_second == 8.50
        
        timing.increase_speed()
        assert timing.ticks_per_second == 8.75

    def test_speed_cap(self) -> None:
        """Test speed is capped at 14.0 ticks per second."""
        timing = TimingSystem()
        
        # Increase speed many times
        for _ in range(100):
            timing.increase_speed()
        
        assert timing.ticks_per_second == MAX_TICKS_PER_SECOND
        assert timing.ticks_per_second == 14.0

    def test_speed_reaches_cap_correctly(self) -> None:
        """Test exact number of increments to reach cap."""
        timing = TimingSystem()
        
        # From 8.0 to 14.0 with 0.25 increments = 24 increments
        increments_needed = int((MAX_TICKS_PER_SECOND - INITIAL_TICKS_PER_SECOND) / SPEED_INCREMENT)
        
        for i in range(increments_needed):
            timing.increase_speed()
        
        assert timing.ticks_per_second == MAX_TICKS_PER_SECOND
        
        # One more shouldn't exceed cap
        timing.increase_speed()
        assert timing.ticks_per_second == MAX_TICKS_PER_SECOND


class TestTickAccumulator:
    """Test fixed-timestep tick accumulation."""

    def test_tick_generation(self) -> None:
        """Test correct number of ticks generated."""
        timing = TimingSystem()
        # At 8 ticks/sec, interval is 0.125s
        
        # Less than interval = 0 ticks
        ticks = timing.update(0.1)
        assert ticks == 0
        
        # Cross interval threshold = 1 tick
        ticks = timing.update(0.05)
        assert ticks == 1
        
        # Multiple intervals = multiple ticks
        timing.tick_accumulator = 0
        ticks = timing.update(0.3)  # 0.3 / 0.125 = 2.4 = 2 ticks
        assert ticks == 2

    def test_accumulator_preserves_remainder(self) -> None:
        """Test accumulator preserves sub-tick time."""
        timing = TimingSystem()
        
        timing.update(0.1)  # 0.1s accumulated
        timing.update(0.1)  # 0.2s total, 1 tick consumed (0.125s), 0.075s remains
        
        expected_remainder = 0.2 - 0.125
        assert abs(timing.tick_accumulator - expected_remainder) < 0.001

    def test_paused_no_ticks(self) -> None:
        """Test no ticks generated when paused."""
        timing = TimingSystem()
        timing.paused = True
        
        ticks = timing.update(1.0)
        assert ticks == 0
        assert timing.tick_accumulator == 0
