"""Tests for content modules."""

import pytest

from src.constants import GameMode, TIME_ATTACK_DURATION
from src.content.modes import get_mode_config, MODE_CONFIGS
from src.content.maps import get_map, get_map_set, get_map_count, ALL_MAPS


class TestModeConfigs:
    """Test mode configuration."""

    def test_all_modes_have_config(self) -> None:
        """Test all game modes have configurations.

        Verifies that every GameMode enum value has a corresponding
        configuration with a non-empty name.

        Raises:
            AssertionError: If any mode lacks a config or has an empty name.
        """
        for mode in GameMode:
            config = get_mode_config(mode)
            assert config is not None
            assert config.name != ""

    def test_classic_mode(self) -> None:
        """Test Classic mode configuration.

        Verifies that Classic mode has wrap-around enabled, non-lethal
        borders, no walls, and no time limit.

        Raises:
            AssertionError: If any Classic mode setting is incorrect.
        """
        config = get_mode_config(GameMode.CLASSIC)
        assert config.wrap_around is True
        assert config.border_lethal is False
        assert config.has_walls is False
        assert config.time_limit == 0

    def test_boxed_mode(self) -> None:
        """Test Boxed mode configuration.

        Verifies that Boxed mode has wrap-around disabled, lethal
        borders, no walls, and no time limit.

        Raises:
            AssertionError: If any Boxed mode setting is incorrect.
        """
        config = get_mode_config(GameMode.BOXED)
        assert config.wrap_around is False
        assert config.border_lethal is True
        assert config.has_walls is False
        assert config.time_limit == 0

    def test_maze_mode(self) -> None:
        """Test Maze mode configuration.

        Verifies that Maze mode has wrap-around disabled, lethal
        borders, walls enabled, and no time limit.

        Raises:
            AssertionError: If any Maze mode setting is incorrect.
        """
        config = get_mode_config(GameMode.MAZE)
        assert config.wrap_around is False
        assert config.border_lethal is True
        assert config.has_walls is True
        assert config.time_limit == 0

    def test_time_attack_mode(self) -> None:
        """Test Time Attack mode configuration.

        Verifies that Time Attack mode has wrap-around enabled, non-lethal
        borders, no walls, and a time limit matching TIME_ATTACK_DURATION.

        Raises:
            AssertionError: If any Time Attack mode setting is incorrect.
        """
        config = get_mode_config(GameMode.TIME_ATTACK)
        assert config.wrap_around is True
        assert config.border_lethal is False
        assert config.has_walls is False
        assert config.time_limit == TIME_ATTACK_DURATION


class TestMazeMaps:
    """Test maze map definitions."""

    def test_map_count(self) -> None:
        """Test there are exactly 5 maps.

        Verifies that both get_map_count() and ALL_MAPS return 5 maps.

        Raises:
            AssertionError: If map count is not exactly 5.
        """
        assert get_map_count() == 5
        assert len(ALL_MAPS) == 5

    def test_get_map_wraps(self) -> None:
        """Test get_map wraps around indices.

        Verifies that get_map uses modulo arithmetic so indices
        beyond the map count wrap back to the beginning.

        Raises:
            AssertionError: If map index wrapping is incorrect.
        """
        map_0 = get_map(0)
        map_5 = get_map(5)
        assert map_0 == map_5
        
        map_1 = get_map(1)
        map_6 = get_map(6)
        assert map_1 == map_6

    def test_get_map_set(self) -> None:
        """Test get_map_set returns a set.

        Verifies that get_map_set returns a non-empty set of wall
        coordinates for map index 0.

        Raises:
            AssertionError: If result is not a set or is empty.
        """
        map_set = get_map_set(0)
        assert isinstance(map_set, set)
        assert len(map_set) > 0

    def test_maps_have_valid_coordinates(self) -> None:
        """Test all map coordinates are within grid bounds.

        Verifies that every coordinate in every map falls within
        the valid grid dimensions (0 to GRID_WIDTH-1, 0 to GRID_HEIGHT-1).

        Raises:
            AssertionError: If any coordinate is out of bounds.
        """
        from src.constants import GRID_WIDTH, GRID_HEIGHT
        
        for i, maze_map in enumerate(ALL_MAPS):
            for x, y in maze_map:
                assert 0 <= x < GRID_WIDTH, f"Map {i} has invalid x: {x}"
                assert 0 <= y < GRID_HEIGHT, f"Map {i} has invalid y: {y}"

    def test_maps_not_empty(self) -> None:
        """Test all maps have walls.

        Verifies that every map in ALL_MAPS contains at least one
        wall coordinate.

        Raises:
            AssertionError: If any map is empty.
        """
        for i, maze_map in enumerate(ALL_MAPS):
            assert len(maze_map) > 0, f"Map {i} is empty"
