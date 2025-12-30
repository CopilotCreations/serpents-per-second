"""Tests for snake movement and state."""

import pytest

from src.constants import Direction, GRID_WIDTH, GRID_HEIGHT
from src.game.snake import Snake


class TestSnakeMovement:
    """Test snake movement mechanics."""

    def test_initial_state(self) -> None:
        """Test snake initial state after reset."""
        snake = Snake()
        snake.reset()
        
        assert len(snake.segments) == 3
        assert snake.head == (3, 7)
        assert snake.direction == Direction.RIGHT
        assert snake.grow_pending is False

    def test_move_right(self) -> None:
        """Test moving right."""
        snake = Snake()
        snake.reset()
        snake.direction = Direction.RIGHT
        
        snake.move()
        assert snake.head == (4, 7)
        assert len(snake.segments) == 3

    def test_move_up(self) -> None:
        """Test moving up."""
        snake = Snake()
        snake.segments = [(5, 5), (5, 6), (5, 7)]
        snake.direction = Direction.UP
        
        snake.move()
        assert snake.head == (5, 4)

    def test_grow(self) -> None:
        """Test snake growth."""
        snake = Snake()
        snake.reset()
        initial_length = len(snake.segments)
        
        snake.grow()
        snake.move()
        
        assert len(snake.segments) == initial_length + 1

    def test_body_excludes_head(self) -> None:
        """Test body property excludes head."""
        snake = Snake()
        snake.reset()
        
        assert snake.head not in snake.body
        assert len(snake.body) == len(snake.segments) - 1

    def test_occupies(self) -> None:
        """Test occupies check."""
        snake = Snake()
        snake.segments = [(5, 5), (4, 5), (3, 5)]
        
        assert snake.occupies((5, 5)) is True
        assert snake.occupies((4, 5)) is True
        assert snake.occupies((6, 5)) is False


class TestSnakeDirections:
    """Test snake segment direction calculations."""

    def test_segment_directions(self) -> None:
        """Test segment direction calculation for rendering."""
        snake = Snake()
        snake.segments = [(5, 5), (4, 5), (3, 5)]
        snake.direction = Direction.RIGHT
        
        directions = snake.get_segment_directions()
        
        assert len(directions) == 3
        # Head has no incoming, outgoing towards body
        assert directions[0][0] is None
        # Tail has incoming, no outgoing
        assert directions[-1][1] is None

    def test_set_direction(self) -> None:
        """Test setting direction."""
        snake = Snake()
        snake.direction = Direction.RIGHT
        
        snake.set_direction(Direction.UP)
        assert snake.direction == Direction.UP
