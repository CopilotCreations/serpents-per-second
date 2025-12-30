"""Tests for content modules."""

import pytest

from src.constants import GameMode, TIME_ATTACK_DURATION
from src.content.modes import get_mode_config, MODE_CONFIGS
from src.content.maps import get_map, get_map_set, get_map_count, ALL_MAPS


class TestModeConfigs:
    """Test mode configuration."""

    def test_all_modes_have_config(self) -> None:
        """Test all game modes have configurations."""
        for mode in GameMode:
            config = get_mode_config(mode)
            assert config is not None
            assert config.name != ""

    def test_classic_mode(self) -> None:
        """Test Classic mode configuration."""
        config = get_mode_config(GameMode.CLASSIC)
        assert config.wrap_around is True
        assert config.border_lethal is False
        assert config.has_walls is False
        assert config.time_limit == 0

    def test_boxed_mode(self) -> None:
        """Test Boxed mode configuration."""
        config = get_mode_config(GameMode.BOXED)
        assert config.wrap_around is False
        assert config.border_lethal is True
        assert config.has_walls is False
        assert config.time_limit == 0

    def test_maze_mode(self) -> None:
        """Test Maze mode configuration."""
        config = get_mode_config(GameMode.MAZE)
        assert config.wrap_around is False
        assert config.border_lethal is True
        assert config.has_walls is True
        assert config.time_limit == 0

    def test_time_attack_mode(self) -> None:
        """Test Time Attack mode configuration."""
        config = get_mode_config(GameMode.TIME_ATTACK)
        assert config.wrap_around is True
        assert config.border_lethal is False
        assert config.has_walls is False
        assert config.time_limit == TIME_ATTACK_DURATION


class TestMazeMaps:
    """Test maze map definitions."""

    def test_map_count(self) -> None:
        """Test there are exactly 5 maps."""
        assert get_map_count() == 5
        assert len(ALL_MAPS) == 5

    def test_get_map_wraps(self) -> None:
        """Test get_map wraps around indices."""
        map_0 = get_map(0)
        map_5 = get_map(5)
        assert map_0 == map_5
        
        map_1 = get_map(1)
        map_6 = get_map(6)
        assert map_1 == map_6

    def test_get_map_set(self) -> None:
        """Test get_map_set returns a set."""
        map_set = get_map_set(0)
        assert isinstance(map_set, set)
        assert len(map_set) > 0

    def test_maps_have_valid_coordinates(self) -> None:
        """Test all map coordinates are within grid bounds."""
        from src.constants import GRID_WIDTH, GRID_HEIGHT
        
        for i, maze_map in enumerate(ALL_MAPS):
            for x, y in maze_map:
                assert 0 <= x < GRID_WIDTH, f"Map {i} has invalid x: {x}"
                assert 0 <= y < GRID_HEIGHT, f"Map {i} has invalid y: {y}"

    def test_maps_not_empty(self) -> None:
        """Test all maps have walls."""
        for i, maze_map in enumerate(ALL_MAPS):
            assert len(maze_map) > 0, f"Map {i} is empty"
