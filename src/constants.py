"""Game constants and configuration values."""

from enum import Enum, auto
from pathlib import Path
import os

# Display
INTERNAL_WIDTH = 256
INTERNAL_HEIGHT = 224
TILE_SIZE = 16
GRID_WIDTH = INTERNAL_WIDTH // TILE_SIZE  # 16
GRID_HEIGHT = INTERNAL_HEIGHT // TILE_SIZE  # 14
MIN_SCALE = 3
MAX_SCALE = 6
DEFAULT_SCALE = 4
TARGET_FPS = 60

# Colors (SNES palette-inspired)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BG = (24, 32, 48)
COLOR_SNAKE_GREEN = (72, 160, 72)
COLOR_FOOD_RED = (200, 72, 72)
COLOR_WALL_GRAY = (96, 96, 112)
COLOR_UI_GOLD = (224, 176, 64)
COLOR_UI_BLUE = (64, 128, 192)

# Timing
INITIAL_TICKS_PER_SECOND = 8.0
SPEED_INCREMENT = 0.25
MAX_TICKS_PER_SECOND = 14.0
FOOD_ANIMATION_INTERVAL = 0.25
TIME_ATTACK_DURATION = 120.0

# Scoring
SCORE_PER_FOOD = 10
TIME_ATTACK_SCORE_PER_SECOND = 1

# Audio
DEFAULT_MUSIC_VOLUME = 0.70
DEFAULT_SFX_VOLUME = 0.80
VOLUME_STEP = 0.05

# File paths
APP_NAME = "SerpentsPerSecond"
APPDATA_DIR = Path(os.environ.get("APPDATA", ".")) / APP_NAME
SAVES_DIR = APPDATA_DIR / "saves"
LOG_FILE = APPDATA_DIR / "app.log"
SETTINGS_FILE = SAVES_DIR / "settings.json"
HIGHSCORES_FILE = SAVES_DIR / "highscores.json"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB

# Name entry
NAME_LENGTH = 3
NAME_CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
MAX_HIGHSCORES = 10


class Direction(Enum):
    """Snake movement directions."""
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class GameMode(Enum):
    """Available game modes."""
    CLASSIC = "classic"
    BOXED = "boxed"
    MAZE = "maze"
    TIME_ATTACK = "time_attack"


class EndReason(Enum):
    """Reasons for game ending."""
    SELF_COLLISION = "Game Over: Self"
    WALL_COLLISION = "Game Over: Wall"
    TIME_UP = "Time Up"
    VICTORY = "Victory"


# Direction vectors
DIRECTION_VECTORS: dict[Direction, tuple[int, int]] = {
    Direction.UP: (0, -1),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0),
}

# Opposite directions for reversal check
OPPOSITE_DIRECTIONS: dict[Direction, Direction] = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}

# Key mappings
import pygame

DIRECTION_KEYS: dict[int, Direction] = {
    pygame.K_UP: Direction.UP,
    pygame.K_w: Direction.UP,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_s: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_a: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT,
    pygame.K_d: Direction.RIGHT,
}

MENU_KEYS = {
    "up": [pygame.K_UP, pygame.K_w],
    "down": [pygame.K_DOWN, pygame.K_s],
    "left": [pygame.K_LEFT, pygame.K_a],
    "right": [pygame.K_RIGHT, pygame.K_d],
    "confirm": [pygame.K_RETURN],
    "back": [pygame.K_ESCAPE],
    "pause": [pygame.K_p],
}
