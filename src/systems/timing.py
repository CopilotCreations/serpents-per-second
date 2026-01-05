"""Timing system for fixed-step movement."""

from src.constants import (
    INITIAL_TICKS_PER_SECOND,
    SPEED_INCREMENT,
    MAX_TICKS_PER_SECOND,
    TIME_ATTACK_DURATION,
)


class TimingSystem:
    """Manages fixed-timestep movement and timers."""

    def __init__(self) -> None:
        """Initialize the timing system with default values.

        Sets up initial tick rate, accumulators, and timer state for
        managing fixed-timestep game updates.
        """
        self.ticks_per_second = INITIAL_TICKS_PER_SECOND
        self.tick_accumulator = 0.0
        self.elapsed_time = 0.0
        self.time_remaining = TIME_ATTACK_DURATION
        self.paused = False
        self._last_scored_second = 0

    def reset(self, is_time_attack: bool = False) -> None:
        """Reset timing for a new game.

        Args:
            is_time_attack: If True, initializes the countdown timer for
                Time Attack mode. Defaults to False.
        """
        self.ticks_per_second = INITIAL_TICKS_PER_SECOND
        self.tick_accumulator = 0.0
        self.elapsed_time = 0.0
        self.time_remaining = TIME_ATTACK_DURATION if is_time_attack else 0.0
        self.paused = False
        self._last_scored_second = 0

    def get_tick_interval(self) -> float:
        """Get the current tick interval in seconds.

        Returns:
            The time interval between movement ticks based on current speed.
        """
        return 1.0 / self.ticks_per_second

    def update(self, dt: float) -> int:
        """Update timing with delta time.

        Accumulates time and calculates how many fixed-timestep movement
        ticks should be processed this frame.

        Args:
            dt: Delta time in seconds since last update.

        Returns:
            The number of movement ticks to process this frame.
        """
        if self.paused:
            return 0

        self.elapsed_time += dt
        self.tick_accumulator += dt

        tick_interval = self.get_tick_interval()
        ticks = 0
        
        while self.tick_accumulator >= tick_interval:
            self.tick_accumulator -= tick_interval
            ticks += 1

        return ticks

    def update_time_attack(self, dt: float) -> bool:
        """Update Time Attack countdown timer.

        Args:
            dt: Delta time in seconds since last update.

        Returns:
            True if the timer has expired, False otherwise.
        """
        if self.paused:
            return False

        self.time_remaining -= dt
        return self.time_remaining <= 0

    def check_second_scored(self) -> bool:
        """Check if a new second has passed for Time Attack scoring.

        Tracks elapsed whole seconds to award survival points in Time Attack mode.

        Returns:
            True if a new second has elapsed and score should increment,
            False otherwise.
        """
        current_second = int(self.elapsed_time)
        if current_second > self._last_scored_second:
            self._last_scored_second = current_second
            return True
        return False

    def increase_speed(self) -> None:
        """Increase movement speed after eating food.

        Increments the tick rate up to the maximum allowed speed.
        """
        self.ticks_per_second = min(
            self.ticks_per_second + SPEED_INCREMENT,
            MAX_TICKS_PER_SECOND
        )

    def toggle_pause(self) -> bool:
        """Toggle the pause state.

        Returns:
            The new pause state (True if now paused, False if resumed).
        """
        self.paused = not self.paused
        return self.paused
