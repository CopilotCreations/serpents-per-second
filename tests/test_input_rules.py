"""Tests for input handling rules."""

import pytest

from src.constants import Direction
from src.systems.input import InputHandler


class TestInputHandler:
    """Test input handler for no-buffered-input and reversal prevention."""

    def test_initial_direction(self) -> None:
        """Test that the initial direction is RIGHT.

        Verifies that a newly created InputHandler has its current_direction
        set to Direction.RIGHT by default.
        """
        handler = InputHandler()
        assert handler.current_direction == Direction.RIGHT

    def test_pending_direction_overwrites(self) -> None:
        """Test that multiple direction presses overwrite pending direction.

        Verifies that when multiple direction keys are pressed before a tick,
        only the last pressed direction is stored as the pending direction.
        This ensures no input buffering occurs.
        """
        handler = InputHandler()
        
        # Press multiple directions before tick
        import pygame
        handler.handle_key_down(pygame.K_UP)
        assert handler.pending_direction == Direction.UP
        
        handler.handle_key_down(pygame.K_DOWN)
        assert handler.pending_direction == Direction.DOWN
        
        handler.handle_key_down(pygame.K_LEFT)
        assert handler.pending_direction == Direction.LEFT
        
        # Only the last one should be applied
        assert handler.pending_direction == Direction.LEFT

    def test_reversal_prevented(self) -> None:
        """Test that 180-degree reversal is prevented.

        Verifies that attempting to reverse direction (e.g., pressing LEFT
        while moving RIGHT) is ignored. The snake should continue in its
        current direction.
        """
        handler = InputHandler()
        handler.current_direction = Direction.RIGHT
        
        import pygame
        handler.handle_key_down(pygame.K_LEFT)  # Opposite of RIGHT
        
        # Apply should ignore the reversal
        result = handler.apply_pending_direction()
        assert result == Direction.RIGHT
        assert handler.current_direction == Direction.RIGHT

    def test_valid_turn_applied(self) -> None:
        """Test that valid 90-degree turns are applied.

        Verifies that perpendicular direction changes (e.g., pressing UP
        while moving RIGHT) are correctly applied when apply_pending_direction
        is called.
        """
        handler = InputHandler()
        handler.current_direction = Direction.RIGHT
        
        import pygame
        handler.handle_key_down(pygame.K_UP)
        
        result = handler.apply_pending_direction()
        assert result == Direction.UP
        assert handler.current_direction == Direction.UP

    def test_direction_changed_on_tick(self) -> None:
        """Test detection of direction change.

        Verifies that direction_changed_on_tick correctly returns True when
        a new direction is pending and differs from the current direction,
        and returns False when the pending direction matches the current one.
        """
        handler = InputHandler()
        handler.current_direction = Direction.RIGHT
        
        import pygame
        handler.handle_key_down(pygame.K_UP)
        
        assert handler.direction_changed_on_tick() is True
        
        # Same direction should not count as changed
        handler.apply_pending_direction()
        handler.handle_key_down(pygame.K_UP)
        assert handler.direction_changed_on_tick() is False

    def test_reset(self) -> None:
        """Test that reset clears pending direction.

        Verifies that calling reset with a new direction clears any pending
        direction and sets the current direction to the specified value.
        """
        handler = InputHandler()
        
        import pygame
        handler.handle_key_down(pygame.K_UP)
        handler.reset(Direction.DOWN)
        
        assert handler.pending_direction is None
        assert handler.current_direction == Direction.DOWN
