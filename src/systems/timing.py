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
        self.ticks_per_second = INITIAL_TICKS_PER_SECOND
        self.tick_accumulator = 0.0
        self.elapsed_time = 0.0
        self.time_remaining = TIME_ATTACK_DURATION
        self.paused = False
        self._last_scored_second = 0

    def reset(self, is_time_attack: bool = False) -> None:
        """Reset timing for a new game."""
        self.ticks_per_second = INITIAL_TICKS_PER_SECOND
        self.tick_accumulator = 0.0
        self.elapsed_time = 0.0
        self.time_remaining = TIME_ATTACK_DURATION if is_time_attack else 0.0
        self.paused = False
        self._last_scored_second = 0

    def get_tick_interval(self) -> float:
        """Get the current tick interval in seconds."""
        return 1.0 / self.ticks_per_second

    def update(self, dt: float) -> int:
        """
        Update timing with delta time.
        Returns the number of movement ticks to process.
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
        """
        Update Time Attack timer.
        Returns True if time ran out.
        """
        if self.paused:
            return False

        self.time_remaining -= dt
        return self.time_remaining <= 0

    def check_second_scored(self) -> bool:
        """
        Check if a new second has passed for Time Attack scoring.
        Returns True if score should increment.
        """
        current_second = int(self.elapsed_time)
        if current_second > self._last_scored_second:
            self._last_scored_second = current_second
            return True
        return False

    def increase_speed(self) -> None:
        """Increase speed after eating food."""
        self.ticks_per_second = min(
            self.ticks_per_second + SPEED_INCREMENT,
            MAX_TICKS_PER_SECOND
        )

    def toggle_pause(self) -> bool:
        """Toggle pause state. Returns new pause state."""
        self.paused = not self.paused
        return self.paused
