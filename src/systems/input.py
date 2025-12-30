"""Input handling system."""

import pygame

from src.constants import (
    Direction,
    DIRECTION_KEYS,
    OPPOSITE_DIRECTIONS,
    MENU_KEYS,
)


class InputHandler:
    """Handles input for gameplay (no buffered input)."""

    def __init__(self) -> None:
        self.pending_direction: Direction | None = None
        self.current_direction: Direction = Direction.RIGHT

    def reset(self, initial_direction: Direction = Direction.RIGHT) -> None:
        """Reset input state for a new game."""
        self.pending_direction = None
        self.current_direction = initial_direction

    def handle_key_down(self, key: int) -> bool:
        """Process a key press. Returns True if direction was set."""
        if key in DIRECTION_KEYS:
            new_dir = DIRECTION_KEYS[key]
            # No buffered input: always overwrite pending direction
            self.pending_direction = new_dir
            return True
        return False

    def apply_pending_direction(self) -> Direction:
        """Apply pending direction if valid, returning the direction to use."""
        if self.pending_direction is None:
            return self.current_direction
        
        # Check for 180° reversal
        if OPPOSITE_DIRECTIONS.get(self.current_direction) == self.pending_direction:
            # Ignore reversal, continue straight
            self.pending_direction = None
            return self.current_direction
        
        # Apply the new direction
        direction_changed = self.pending_direction != self.current_direction
        self.current_direction = self.pending_direction
        self.pending_direction = None
        return self.current_direction

    def direction_changed_on_tick(self) -> bool:
        """Check if direction actually changed when applying pending."""
        if self.pending_direction is None:
            return False
        if OPPOSITE_DIRECTIONS.get(self.current_direction) == self.pending_direction:
            return False
        return self.pending_direction != self.current_direction


def is_menu_key(key: int, action: str) -> bool:
    """Check if a key matches a menu action."""
    return key in MENU_KEYS.get(action, [])
