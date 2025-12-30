"""Mode rules and configuration."""

from dataclasses import dataclass

from src.constants import GameMode, TIME_ATTACK_DURATION


@dataclass(frozen=True)
class ModeConfig:
    """Configuration for a game mode."""
    name: str
    wrap_around: bool
    border_lethal: bool
    has_walls: bool
    time_limit: float  # 0 means no limit


MODE_CONFIGS: dict[GameMode, ModeConfig] = {
    GameMode.CLASSIC: ModeConfig(
        name="Classic",
        wrap_around=True,
        border_lethal=False,
        has_walls=False,
        time_limit=0,
    ),
    GameMode.BOXED: ModeConfig(
        name="Boxed",
        wrap_around=False,
        border_lethal=True,
        has_walls=False,
        time_limit=0,
    ),
    GameMode.MAZE: ModeConfig(
        name="Maze",
        wrap_around=False,
        border_lethal=True,
        has_walls=True,
        time_limit=0,
    ),
    GameMode.TIME_ATTACK: ModeConfig(
        name="Time Attack",
        wrap_around=True,
        border_lethal=False,
        has_walls=False,
        time_limit=TIME_ATTACK_DURATION,
    ),
}


def get_mode_config(mode: GameMode) -> ModeConfig:
    """Get configuration for a game mode."""
    return MODE_CONFIGS[mode]
