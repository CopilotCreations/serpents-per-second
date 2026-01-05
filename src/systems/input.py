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
        """Initialize the input handler with default state.
        
        Sets the initial direction to RIGHT with no pending direction.
        """
        self.pending_direction: Direction | None = None
        self.current_direction: Direction = Direction.RIGHT

    def reset(self, initial_direction: Direction = Direction.RIGHT) -> None:
        """Reset input state for a new game.
        
        Args:
            initial_direction: The direction to start with. Defaults to RIGHT.
        """
        self.pending_direction = None
        self.current_direction = initial_direction

    def handle_key_down(self, key: int) -> bool:
        """Process a key press and update pending direction.
        
        Args:
            key: The pygame key code that was pressed.
            
        Returns:
            True if the key was a valid direction key and pending direction
            was updated, False otherwise.
        """
        if key in DIRECTION_KEYS:
            new_dir = DIRECTION_KEYS[key]
            # No buffered input: always overwrite pending direction
            self.pending_direction = new_dir
            return True
        return False

    def apply_pending_direction(self) -> Direction:
        """Apply pending direction if valid, returning the direction to use.
        
        Validates the pending direction and applies it if it's not a 180-degree
        reversal. Clears the pending direction after processing.
        
        Returns:
            The direction to use for the current tick. Returns current_direction
            if no pending direction or if reversal was attempted.
        """
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
        """Check if direction would actually change when applying pending.
        
        Determines whether applying the pending direction would result in
        a direction change, without actually modifying state.
        
        Returns:
            True if pending direction differs from current and is not a
            180-degree reversal, False otherwise.
        """
        if self.pending_direction is None:
            return False
        if OPPOSITE_DIRECTIONS.get(self.current_direction) == self.pending_direction:
            return False
        return self.pending_direction != self.current_direction


def is_menu_key(key: int, action: str) -> bool:
    """Check if a key matches a menu action.
    
    Args:
        key: The pygame key code to check.
        action: The menu action name to match against (e.g., 'select', 'back').
        
    Returns:
        True if the key is mapped to the specified menu action, False otherwise.
    """
    return key in MENU_KEYS.get(action, [])
