"""Collision detection."""

from src.constants import GRID_WIDTH, GRID_HEIGHT, EndReason


def check_self_collision(
    head: tuple[int, int], body: list[tuple[int, int]]
) -> bool:
    """Check if head collides with body.

    Args:
        head: The (x, y) position of the snake's head.
        body: List of (x, y) positions representing the snake's body segments.

    Returns:
        True if the head position is found within the body, False otherwise.
    """
    return head in body


def check_border_collision(head: tuple[int, int]) -> bool:
    """Check if head is outside grid bounds.

    Args:
        head: The (x, y) position of the snake's head.

    Returns:
        True if the head is outside the grid boundaries, False otherwise.
    """
    x, y = head
    return x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT


def check_wall_collision(
    head: tuple[int, int], walls: set[tuple[int, int]]
) -> bool:
    """Check if head collides with a wall.

    Args:
        head: The (x, y) position of the snake's head.
        walls: Set of (x, y) positions representing wall tiles.

    Returns:
        True if the head position collides with a wall, False otherwise.
    """
    return head in walls


def check_collisions(
    head: tuple[int, int],
    body: list[tuple[int, int]],
    border_lethal: bool = False,
    walls: set[tuple[int, int]] | None = None,
) -> EndReason | None:
    """Check all collision types.

    Args:
        head: The (x, y) position of the snake's head.
        body: List of (x, y) positions representing the snake's body segments.
        border_lethal: If True, border collisions end the game.
        walls: Optional set of (x, y) positions representing wall tiles.

    Returns:
        EndReason if a collision occurred, None otherwise.
    """
    if check_self_collision(head, body):
        return EndReason.SELF_COLLISION
    
    if border_lethal and check_border_collision(head):
        return EndReason.WALL_COLLISION
    
    if walls and check_wall_collision(head, walls):
        return EndReason.WALL_COLLISION
    
    return None
