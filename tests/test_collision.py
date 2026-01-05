"""Tests for collision detection."""

import pytest

from src.constants import EndReason
from src.game.collision import check_collisions


class TestCollisionIntegration:
    """Test integrated collision detection."""

    def test_no_collision(self) -> None:
        """Test no collision returns None.

        Verifies that when the snake head is not colliding with any
        obstacle (body, walls, or borders), the function returns None.
        """
        head = (5, 5)
        body = [(4, 5), (3, 5)]
        
        result = check_collisions(head, body)
        assert result is None

    def test_self_collision_returns_reason(self) -> None:
        """Test self collision returns correct reason.

        Verifies that when the snake head position overlaps with a body
        segment, the function returns EndReason.SELF_COLLISION.
        """
        head = (5, 5)
        body = [(4, 5), (5, 5)]  # Body includes head position
        
        result = check_collisions(head, body)
        assert result == EndReason.SELF_COLLISION

    def test_border_collision_returns_reason(self) -> None:
        """Test border collision returns correct reason.

        Verifies that when the snake head moves outside the grid bounds
        and border_lethal is True, the function returns EndReason.WALL_COLLISION.
        """
        head = (-1, 5)
        body = [(0, 5), (1, 5)]
        
        result = check_collisions(head, body, border_lethal=True)
        assert result == EndReason.WALL_COLLISION

    def test_wall_collision_returns_reason(self) -> None:
        """Test wall collision returns correct reason.

        Verifies that when the snake head moves into a wall tile,
        the function returns EndReason.WALL_COLLISION.
        """
        head = (5, 5)
        body = [(4, 5), (3, 5)]
        walls = {(5, 5), (6, 5)}
        
        result = check_collisions(head, body, walls=walls)
        assert result == EndReason.WALL_COLLISION

    def test_border_ignored_when_not_lethal(self) -> None:
        """Test border is ignored when not lethal.

        Verifies that when the snake head moves outside the grid bounds
        but border_lethal is False, no collision is detected (returns None).
        This supports wrap-around game modes.
        """
        head = (-1, 5)  # Out of bounds
        body = [(0, 5), (1, 5)]
        
        result = check_collisions(head, body, border_lethal=False)
        assert result is None  # No collision when border not lethal
