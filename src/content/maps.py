"""Maze map definitions."""

from src.constants import GRID_WIDTH, GRID_HEIGHT

# Maps are lists of (x, y) wall positions
# Grid is 16x14, coordinates 0-15 for x, 0-13 for y

MAP_1: list[tuple[int, int]] = [
    # Central cross pattern
    (7, 3), (8, 3),
    (7, 4), (8, 4),
    (7, 9), (8, 9),
    (7, 10), (8, 10),
    (3, 6), (4, 6), (3, 7), (4, 7),
    (11, 6), (12, 6), (11, 7), (12, 7),
]

MAP_2: list[tuple[int, int]] = [
    # Corner blocks
    (2, 2), (3, 2), (2, 3), (3, 3),
    (12, 2), (13, 2), (12, 3), (13, 3),
    (2, 10), (3, 10), (2, 11), (3, 11),
    (12, 10), (13, 10), (12, 11), (13, 11),
]

MAP_3: list[tuple[int, int]] = [
    # Horizontal barriers
    *[(x, 4) for x in range(3, 8)],
    *[(x, 4) for x in range(9, 14)],
    *[(x, 9) for x in range(3, 8)],
    *[(x, 9) for x in range(9, 14)],
]

MAP_4: list[tuple[int, int]] = [
    # Vertical barriers
    *[(4, y) for y in range(2, 6)],
    *[(4, y) for y in range(8, 12)],
    *[(11, y) for y in range(2, 6)],
    *[(11, y) for y in range(8, 12)],
]

MAP_5: list[tuple[int, int]] = [
    # Scattered blocks
    (4, 3), (11, 3),
    (3, 6), (12, 6),
    (4, 10), (11, 10),
    (7, 5), (8, 5),
    (7, 8), (8, 8),
    (5, 7), (10, 7),
]

ALL_MAPS: list[list[tuple[int, int]]] = [MAP_1, MAP_2, MAP_3, MAP_4, MAP_5]


def get_map(index: int) -> list[tuple[int, int]]:
    """Get a map by index (wraps around)."""
    return ALL_MAPS[index % len(ALL_MAPS)]


def get_map_set(index: int) -> set[tuple[int, int]]:
    """Get a map as a set for fast lookup."""
    return set(get_map(index))


def get_map_count() -> int:
    """Get the total number of maps."""
    return len(ALL_MAPS)
