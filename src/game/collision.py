"""Collision detection."""

from src.constants import GRID_WIDTH, GRID_HEIGHT, EndReason


def check_self_collision(
    head: tuple[int, int], body: list[tuple[int, int]]
) -> bool:
    """Check if head collides with body."""
    return head in body


def check_border_collision(head: tuple[int, int]) -> bool:
    """Check if head is outside grid bounds."""
    x, y = head
    return x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT


def check_wall_collision(
    head: tuple[int, int], walls: set[tuple[int, int]]
) -> bool:
    """Check if head collides with a wall."""
    return head in walls


def check_collisions(
    head: tuple[int, int],
    body: list[tuple[int, int]],
    border_lethal: bool = False,
    walls: set[tuple[int, int]] | None = None,
) -> EndReason | None:
    """
    Check all collision types.
    Returns EndReason if collision occurred, None otherwise.
    """
    if check_self_collision(head, body):
        return EndReason.SELF_COLLISION
    
    if border_lethal and check_border_collision(head):
        return EndReason.WALL_COLLISION
    
    if walls and check_wall_collision(head, walls):
        return EndReason.WALL_COLLISION
    
    return None
