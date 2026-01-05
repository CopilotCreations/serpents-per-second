"""Tests for wrap-around and wall collision."""

import pytest

from src.constants import Direction, GRID_WIDTH, GRID_HEIGHT
from src.game.snake import Snake
from src.game.collision import (
    check_border_collision,
    check_wall_collision,
    check_self_collision,
)


class TestWrapAround:
    """Test wrap-around behavior."""

    def test_wrap_left_to_right(self) -> None:
        """Test wrapping from left edge to right edge.

        Verifies that a snake moving left from x=0 wraps around to
        the right edge of the grid (GRID_WIDTH - 1).
        """
        snake = Snake()
        snake.segments = [(0, 7)]
        snake.direction = Direction.LEFT
        
        new_head = snake.get_next_head(wrap=True)
        assert new_head == (GRID_WIDTH - 1, 7)

    def test_wrap_right_to_left(self) -> None:
        """Test wrapping from right edge to left edge.

        Verifies that a snake moving right from x=GRID_WIDTH-1 wraps
        around to the left edge of the grid (x=0).
        """
        snake = Snake()
        snake.segments = [(GRID_WIDTH - 1, 7)]
        snake.direction = Direction.RIGHT
        
        new_head = snake.get_next_head(wrap=True)
        assert new_head == (0, 7)

    def test_wrap_top_to_bottom(self) -> None:
        """Test wrapping from top edge to bottom edge.

        Verifies that a snake moving up from y=0 wraps around to the
        bottom edge of the grid (GRID_HEIGHT - 1).
        """
        snake = Snake()
        snake.segments = [(8, 0)]
        snake.direction = Direction.UP
        
        new_head = snake.get_next_head(wrap=True)
        assert new_head == (8, GRID_HEIGHT - 1)

    def test_wrap_bottom_to_top(self) -> None:
        """Test wrapping from bottom edge to top edge.

        Verifies that a snake moving down from y=GRID_HEIGHT-1 wraps
        around to the top edge of the grid (y=0).
        """
        snake = Snake()
        snake.segments = [(8, GRID_HEIGHT - 1)]
        snake.direction = Direction.DOWN
        
        new_head = snake.get_next_head(wrap=True)
        assert new_head == (8, 0)

    def test_no_wrap_returns_out_of_bounds(self) -> None:
        """Test that without wrap, position goes out of bounds.

        Verifies that when wrap is disabled, moving past the edge returns
        an out-of-bounds position (negative coordinate) instead of wrapping.
        """
        snake = Snake()
        snake.segments = [(0, 7)]
        snake.direction = Direction.LEFT
        
        new_head = snake.get_next_head(wrap=False)
        assert new_head == (-1, 7)


class TestBorderCollision:
    """Test border collision detection."""

    def test_left_border(self) -> None:
        """Test left border collision.

        Verifies that x=-1 triggers a collision while x=0 does not.
        """
        assert check_border_collision((-1, 5)) is True
        assert check_border_collision((0, 5)) is False

    def test_right_border(self) -> None:
        """Test right border collision.

        Verifies that x=GRID_WIDTH triggers a collision while
        x=GRID_WIDTH-1 does not.
        """
        assert check_border_collision((GRID_WIDTH, 5)) is True
        assert check_border_collision((GRID_WIDTH - 1, 5)) is False

    def test_top_border(self) -> None:
        """Test top border collision.

        Verifies that y=-1 triggers a collision while y=0 does not.
        """
        assert check_border_collision((5, -1)) is True
        assert check_border_collision((5, 0)) is False

    def test_bottom_border(self) -> None:
        """Test bottom border collision.

        Verifies that y=GRID_HEIGHT triggers a collision while
        y=GRID_HEIGHT-1 does not.
        """
        assert check_border_collision((5, GRID_HEIGHT)) is True
        assert check_border_collision((5, GRID_HEIGHT - 1)) is False


class TestWallCollision:
    """Test wall collision detection."""

    def test_wall_collision_hit(self) -> None:
        """Test collision with wall tile.

        Verifies that positions matching wall coordinates are detected
        as collisions.
        """
        walls = {(5, 5), (6, 5), (7, 5)}
        assert check_wall_collision((5, 5), walls) is True
        assert check_wall_collision((6, 5), walls) is True

    def test_wall_collision_miss(self) -> None:
        """Test no collision when not on wall.

        Verifies that positions not matching any wall coordinates do not
        trigger a collision.
        """
        walls = {(5, 5), (6, 5), (7, 5)}
        assert check_wall_collision((4, 5), walls) is False
        assert check_wall_collision((5, 6), walls) is False


class TestSelfCollision:
    """Test self collision detection."""

    def test_self_collision(self) -> None:
        """Test collision with own body.

        Verifies that when the head position matches any body segment,
        a self-collision is detected.
        """
        head = (5, 5)
        body = [(4, 5), (3, 5), (2, 5), (5, 5)]  # Last segment overlaps head
        assert check_self_collision(head, body) is True

    def test_no_self_collision(self) -> None:
        """Test no collision with body.

        Verifies that when the head position does not match any body
        segment, no self-collision is detected.
        """
        head = (5, 5)
        body = [(4, 5), (3, 5), (2, 5)]
        assert check_self_collision(head, body) is False
