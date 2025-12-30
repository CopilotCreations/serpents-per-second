"""Food spawning and animation."""

import random
from typing import Sequence

from src.constants import GRID_WIDTH, GRID_HEIGHT, FOOD_ANIMATION_INTERVAL


class Food:
    """Food item with spawning and animation."""

    def __init__(self, rng: random.Random | None = None) -> None:
        self.position: tuple[int, int] = (0, 0)
        self.animation_frame = 0
        self.animation_timer = 0.0
        self.rng = rng or random.Random()

    def spawn(
        self,
        snake_segments: Sequence[tuple[int, int]],
        walls: set[tuple[int, int]] | None = None,
    ) -> bool:
        """
        Spawn food at a random valid position.
        Returns True if spawn was successful, False if no valid positions.
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
        """Update food animation frame."""
        if paused:
            return

        self.animation_timer += dt
        if self.animation_timer >= FOOD_ANIMATION_INTERVAL:
            self.animation_timer -= FOOD_ANIMATION_INTERVAL
            self.animation_frame = 1 - self.animation_frame

    def get_frame(self) -> int:
        """Get current animation frame (0 or 1)."""
        return self.animation_frame

    def is_at(self, pos: tuple[int, int]) -> bool:
        """Check if food is at a position."""
        return self.position == pos
