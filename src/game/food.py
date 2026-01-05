"""Food spawning and animation."""

import random
from typing import Sequence

from src.constants import GRID_WIDTH, GRID_HEIGHT, FOOD_ANIMATION_INTERVAL


class Food:
    """Food item with spawning and animation."""

    def __init__(self, rng: random.Random | None = None) -> None:
        """Initialize a Food instance.

        Args:
            rng: Random number generator for spawning. If None, a new
                Random instance is created.
        """
        self.position: tuple[int, int] = (0, 0)
        self.animation_frame = 0
        self.animation_timer = 0.0
        self.rng = rng or random.Random()

    def spawn(
        self,
        snake_segments: Sequence[tuple[int, int]],
        walls: set[tuple[int, int]] | None = None,
    ) -> bool:
        """Spawn food at a random valid position.

        Args:
            snake_segments: Sequence of positions occupied by the snake.
            walls: Optional set of positions occupied by walls.

        Returns:
            True if spawn was successful, False if no valid positions exist.
        """
        occupied = set(snake_segments)
        if walls:
            occupied.update(walls)

        valid_positions: list[tuple[int, int]] = []
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pos = (x, y)
                if pos not in occupied:
                    valid_positions.append(pos)

        if not valid_positions:
            return False

        self.position = self.rng.choice(valid_positions)
        return True

    def update_animation(self, dt: float, paused: bool = False) -> None:
        """Update food animation frame.

        Args:
            dt: Delta time in seconds since last update.
            paused: If True, animation is paused and no update occurs.
        """
        if paused:
            return

        self.animation_timer += dt
        if self.animation_timer >= FOOD_ANIMATION_INTERVAL:
            self.animation_timer -= FOOD_ANIMATION_INTERVAL
            self.animation_frame = 1 - self.animation_frame

    def get_frame(self) -> int:
        """Get current animation frame.

        Returns:
            The current animation frame index (0 or 1).
        """
        return self.animation_frame

    def is_at(self, pos: tuple[int, int]) -> bool:
        """Check if food is at a position.

        Args:
            pos: The position to check as an (x, y) tuple.

        Returns:
            True if food is at the given position, False otherwise.
        """
        return self.position == pos
