"""Tests for input handling rules."""

import pytest

from src.constants import Direction
from src.systems.input import InputHandler


class TestInputHandler:
    """Test input handler for no-buffered-input and reversal prevention."""

    def test_initial_direction(self) -> None:
        """Test initial direction is RIGHT."""
        handler = InputHandler()
        assert handler.current_direction == Direction.RIGHT

    def test_pending_direction_overwrites(self) -> None:
        """Test that multiple direction presses overwrite pending direction."""
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
        """Test that 180-degree reversal is prevented."""
        handler = InputHandler()
        handler.current_direction = Direction.RIGHT
        
        import pygame
        handler.handle_key_down(pygame.K_LEFT)  # Opposite of RIGHT
        
        # Apply should ignore the reversal
        result = handler.apply_pending_direction()
        assert result == Direction.RIGHT
        assert handler.current_direction == Direction.RIGHT

    def test_valid_turn_applied(self) -> None:
        """Test that valid 90-degree turns are applied."""
        handler = InputHandler()
        handler.current_direction = Direction.RIGHT
        
        import pygame
        handler.handle_key_down(pygame.K_UP)
        
        result = handler.apply_pending_direction()
        assert result == Direction.UP
        assert handler.current_direction == Direction.UP

    def test_direction_changed_on_tick(self) -> None:
        """Test detection of direction change."""
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
        """Test reset clears pending direction."""
        handler = InputHandler()
        
        import pygame
        handler.handle_key_down(pygame.K_UP)
        handler.reset(Direction.DOWN)
        
        assert handler.pending_direction is None
        assert handler.current_direction == Direction.DOWN
