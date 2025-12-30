"""Tests for food spawning."""

import random
import pytest

from src.constants import GRID_WIDTH, GRID_HEIGHT
from src.game.food import Food


class TestFoodSpawn:
    """Test food spawning validation."""

    def test_spawn_not_on_snake(self) -> None:
        """Test that food never spawns on snake segments."""
        rng = random.Random(12345)
        food = Food(rng)
        
        snake_segments = [(5, 5), (4, 5), (3, 5)]
        
        for _ in range(100):
            result = food.spawn(snake_segments)
            assert result is True
            assert food.position not in snake_segments

    def test_spawn_not_on_walls(self) -> None:
        """Test that food never spawns on walls."""
        rng = random.Random(12345)
        food = Food(rng)
        
        snake_segments = [(5, 5)]
        walls = {(7, 7), (8, 7), (9, 7), (7, 8), (8, 8), (9, 8)}
        
        for _ in range(100):
            result = food.spawn(snake_segments, walls)
            assert result is True
            assert food.position not in walls
            assert food.position not in snake_segments

    def test_spawn_fails_when_full(self) -> None:
        """Test spawn returns False when no valid positions."""
        food = Food()
        
        # Fill entire grid with snake
        all_positions = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)]
        
        result = food.spawn(all_positions)
        assert result is False

    def test_spawn_uniform_distribution(self) -> None:
        """Test spawn is reasonably uniform over valid cells."""
        rng = random.Random(54321)
        food = Food(rng)
        
        snake_segments = [(0, 0), (1, 0), (2, 0)]
        spawn_counts: dict[tuple[int, int], int] = {}
        
        num_spawns = 10000
        for _ in range(num_spawns):
            food.spawn(snake_segments)
            pos = food.position
            spawn_counts[pos] = spawn_counts.get(pos, 0) + 1
        
        # Check that snake positions were never spawned
        for seg in snake_segments:
            assert spawn_counts.get(seg, 0) == 0
        
        # Check roughly uniform distribution
        valid_cells = GRID_WIDTH * GRID_HEIGHT - len(snake_segments)
        expected_per_cell = num_spawns / valid_cells
        
        # Allow 50% variance
        min_expected = expected_per_cell * 0.5
        max_expected = expected_per_cell * 1.5
        
        for pos, count in spawn_counts.items():
            assert min_expected < count < max_expected, f"Position {pos} had {count} spawns"


class TestFoodAnimation:
    """Test food animation timing."""

    def test_animation_toggle(self) -> None:
        """Test animation toggles every 0.25 seconds."""
        food = Food()
        
        assert food.get_frame() == 0
        
        food.update_animation(0.24)
        assert food.get_frame() == 0
        
        food.update_animation(0.02)  # Total: 0.26s
        assert food.get_frame() == 1
        
        food.update_animation(0.25)  # Total: 0.51s
        assert food.get_frame() == 0

    def test_animation_paused(self) -> None:
        """Test animation doesn't advance when paused."""
        food = Food()
        
        food.update_animation(1.0, paused=True)
        assert food.get_frame() == 0
