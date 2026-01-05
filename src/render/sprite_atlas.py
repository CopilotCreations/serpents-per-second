"""Sprite atlas loading and management."""

from pathlib import Path
import pygame

from src.constants import TILE_SIZE, Direction
from src.systems.logging_setup import get_logger


class SpriteAtlas:
    """Loads and provides access to sprite sheet regions."""

    def __init__(self, assets_path: Path) -> None:
        """Initialize the sprite atlas.

        Args:
            assets_path: Path to the assets directory containing sprite sheets.
        """
        self.assets_path = assets_path
        self.sheets: dict[str, pygame.Surface] = {}
        self.sprites: dict[str, pygame.Surface] = {}

    def load(self) -> bool:
        """Load all sprite sheets from the assets directory.

        Loads required and optional sprite sheets. Required sheets must exist
        for the function to succeed.

        Returns:
            True if all required assets were loaded successfully, False otherwise.
        """
        logger = get_logger()
        sprites_path = self.assets_path / "sprites"
        
        required = ["snake.png", "food.png", "font.png"]
        optional = ["tiles.png", "ui.png"]
        
        for filename in required + optional:
            filepath = sprites_path / filename
            try:
                sheet = pygame.image.load(filepath).convert_alpha()
                self.sheets[filename] = sheet
                logger.info(f"Loaded sprite sheet: {filename}")
            except pygame.error as e:
                if filename in required:
                    logger.error(f"Failed to load required sprite: {filename}: {e}")
                    return False
                logger.warning(f"Failed to load optional sprite: {filename}: {e}")
        
        self._extract_sprites()
        return True

    def _extract_sprites(self) -> None:
        """Extract individual sprites from loaded sprite sheets.

        Processes snake, food, and tile sheets to create individual named
        sprites that can be accessed via get_sprite().
        """
        # Snake sprites (128x64, 8x4 tiles)
        if "snake.png" in self.sheets:
            snake_sheet = self.sheets["snake.png"]
            
            # Row 0: heads and tails
            directions = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
            for i, d in enumerate(directions):
                self.sprites[f"head_{d.name.lower()}"] = self._extract_tile(snake_sheet, i, 0)
            for i, d in enumerate(directions):
                self.sprites[f"tail_{d.name.lower()}"] = self._extract_tile(snake_sheet, i + 4, 0)
            
            # Row 1: body segments
            self.sprites["body_horizontal"] = self._extract_tile(snake_sheet, 0, 1)
            self.sprites["body_vertical"] = self._extract_tile(snake_sheet, 1, 1)
            self.sprites["turn_up_right"] = self._extract_tile(snake_sheet, 2, 1)
            self.sprites["turn_right_down"] = self._extract_tile(snake_sheet, 3, 1)
            self.sprites["turn_down_left"] = self._extract_tile(snake_sheet, 4, 1)
            self.sprites["turn_left_up"] = self._extract_tile(snake_sheet, 5, 1)
        
        # Food sprites (32x16, 2x1 tiles)
        if "food.png" in self.sheets:
            food_sheet = self.sheets["food.png"]
            self.sprites["food_0"] = self._extract_tile(food_sheet, 0, 0)
            self.sprites["food_1"] = self._extract_tile(food_sheet, 1, 0)
        
        # Tile sprites
        if "tiles.png" in self.sheets:
            tiles_sheet = self.sheets["tiles.png"]
            self.sprites["wall"] = self._extract_tile(tiles_sheet, 0, 0)
            self.sprites["floor"] = self._extract_tile(tiles_sheet, 1, 0)

    def _extract_tile(
        self, sheet: pygame.Surface, tile_x: int, tile_y: int
    ) -> pygame.Surface:
        """Extract a single tile from a sprite sheet.

        Args:
            sheet: The source sprite sheet surface.
            tile_x: The x-coordinate of the tile in tile units.
            tile_y: The y-coordinate of the tile in tile units.

        Returns:
            A new surface containing the extracted tile.
        """
        rect = pygame.Rect(tile_x * TILE_SIZE, tile_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        return sheet.subsurface(rect).copy()

    def get_sprite(self, name: str) -> pygame.Surface | None:
        """Get a sprite by its name.

        Args:
            name: The name of the sprite to retrieve.

        Returns:
            The sprite surface if found, None otherwise.
        """
        return self.sprites.get(name)

    def get_head_sprite(self, direction: Direction) -> pygame.Surface | None:
        """Get the snake head sprite for a given direction.

        Args:
            direction: The direction the head is facing.

        Returns:
            The head sprite surface if found, None otherwise.
        """
        return self.get_sprite(f"head_{direction.name.lower()}")

    def get_tail_sprite(self, direction: Direction) -> pygame.Surface | None:
        """Get the snake tail sprite for a given direction.

        Args:
            direction: The direction the tail is pointing.

        Returns:
            The tail sprite surface if found, None otherwise.
        """
        return self.get_sprite(f"tail_{direction.name.lower()}")

    def get_body_sprite(
        self, incoming: Direction | None, outgoing: Direction | None
    ) -> pygame.Surface | None:
        """Get the appropriate body sprite based on segment directions.

        Determines whether to use a straight or turn sprite based on the
        incoming and outgoing directions of a body segment.

        Args:
            incoming: The direction from which the segment is entered.
            outgoing: The direction in which the segment exits.

        Returns:
            The appropriate body sprite surface, or horizontal body as fallback.
        """
        if incoming is None or outgoing is None:
            return self.get_sprite("body_horizontal")
        
        # Check if straight
        if incoming == outgoing:
            if incoming in (Direction.LEFT, Direction.RIGHT):
                return self.get_sprite("body_horizontal")
            return self.get_sprite("body_vertical")
        
        # Determine turn type
        dirs = {incoming, outgoing}
        if dirs == {Direction.UP, Direction.RIGHT}:
            return self.get_sprite("turn_up_right")
        if dirs == {Direction.RIGHT, Direction.DOWN}:
            return self.get_sprite("turn_right_down")
        if dirs == {Direction.DOWN, Direction.LEFT}:
            return self.get_sprite("turn_down_left")
        if dirs == {Direction.LEFT, Direction.UP}:
            return self.get_sprite("turn_left_up")
        
        return self.get_sprite("body_horizontal")

    def get_food_sprite(self, frame: int) -> pygame.Surface | None:
        """Get a food sprite for the specified animation frame.

        Args:
            frame: The animation frame index (0 or 1).

        Returns:
            The food sprite surface if found, None otherwise.
        """
        return self.get_sprite(f"food_{frame}")

    def get_wall_sprite(self) -> pygame.Surface | None:
        """Get the wall tile sprite.

        Returns:
            The wall sprite surface if found, None otherwise.
        """
        return self.get_sprite("wall")
