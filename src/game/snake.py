"""Snake data structure and movement."""

from src.constants import (
    Direction,
    DIRECTION_VECTORS,
    GRID_WIDTH,
    GRID_HEIGHT,
)


class Snake:
    """Snake data structure with movement and growth."""

    def __init__(self) -> None:
        """Initialize a new snake with empty segments and default direction."""
        self.segments: list[tuple[int, int]] = []
        self.direction = Direction.RIGHT
        self.grow_pending = False

    def reset(self, start_x: int = 3, start_y: int = 7, length: int = 3) -> None:
        """Reset snake to initial state.

        Args:
            start_x: The x-coordinate for the snake's head position.
            start_y: The y-coordinate for the snake's head position.
            length: The initial length of the snake.
        """
        self.segments = [(start_x - i, start_y) for i in range(length)]
        self.direction = Direction.RIGHT
        self.grow_pending = False

    @property
    def head(self) -> tuple[int, int]:
        """Get the head position.

        Returns:
            The (x, y) coordinates of the snake's head.
        """
        return self.segments[0]

    @property
    def body(self) -> list[tuple[int, int]]:
        """Get body segments (excluding head).

        Returns:
            A list of (x, y) coordinates for all body segments.
        """
        return self.segments[1:]

    def get_next_head(self, wrap: bool = False) -> tuple[int, int]:
        """Calculate next head position based on current direction.

        Args:
            wrap: If True, wrap around grid boundaries.

        Returns:
            The (x, y) coordinates of the next head position.
        """
        dx, dy = DIRECTION_VECTORS[self.direction]
        new_x = self.head[0] + dx
        new_y = self.head[1] + dy

        if wrap:
            new_x = new_x % GRID_WIDTH
            new_y = new_y % GRID_HEIGHT

        return (new_x, new_y)

    def move(self, wrap: bool = False) -> tuple[int, int]:
        """Move the snake one step in the current direction.

        Args:
            wrap: If True, wrap around grid boundaries.

        Returns:
            The (x, y) coordinates of the new head position.
        """
        new_head = self.get_next_head(wrap)
        self.segments.insert(0, new_head)

        if self.grow_pending:
            self.grow_pending = False
        else:
            self.segments.pop()

        return new_head

    def grow(self) -> None:
        """Schedule the snake to grow on the next move."""
        self.grow_pending = True

    def set_direction(self, direction: Direction) -> None:
        """Set the movement direction.

        Args:
            direction: The new direction for the snake to move.
        """
        self.direction = direction

    def occupies(self, pos: tuple[int, int]) -> bool:
        """Check if the snake occupies a position.

        Args:
            pos: The (x, y) position to check.

        Returns:
            True if the snake occupies the position, False otherwise.
        """
        return pos in self.segments

    def get_segment_directions(self) -> list[tuple[Direction | None, Direction | None]]:
        """Get incoming and outgoing directions for each segment.

        Used for selecting correct sprite variants.

        Returns:
            A list of (incoming, outgoing) direction tuples for each segment.
        """
        result: list[tuple[Direction | None, Direction | None]] = []
        
        for i, seg in enumerate(self.segments):
            # Previous segment (towards head)
            if i > 0:
                prev = self.segments[i - 1]
                incoming = self._get_direction_between(seg, prev)
            else:
                incoming = None
            
            # Next segment (towards tail)
            if i < len(self.segments) - 1:
                next_seg = self.segments[i + 1]
                outgoing = self._get_direction_between(seg, next_seg)
            else:
                outgoing = None
            
            result.append((incoming, outgoing))
        
        return result

    def _get_direction_between(
        self, from_pos: tuple[int, int], to_pos: tuple[int, int]
    ) -> Direction:
        """Get the direction from one position to another.

        Args:
            from_pos: The starting (x, y) position.
            to_pos: The target (x, y) position.

        Returns:
            The direction from from_pos to to_pos.
        """
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]
        
        # Handle wrap-around
        if dx > 1:
            dx = -1
        elif dx < -1:
            dx = 1
        if dy > 1:
            dy = -1
        elif dy < -1:
            dy = 1
        
        for direction, (vx, vy) in DIRECTION_VECTORS.items():
            if vx == dx and vy == dy:
                return direction
        
        return Direction.RIGHT  # Default fallback
