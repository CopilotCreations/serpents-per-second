"""Gameplay scene."""

import pygame

from src.scenes.base import Scene
from src.systems.input import InputHandler, is_menu_key
from src.systems.timing import TimingSystem
from src.game.snake import Snake
from src.game.food import Food
from src.game.collision import check_collisions
from src.game.scoring import Scoring
from src.content.modes import get_mode_config
from src.content.maps import get_map_set
from src.render.hud import HUD
from src.constants import (
    COLOR_BG,
    COLOR_SNAKE_GREEN,
    COLOR_FOOD_RED,
    COLOR_WALL_GRAY,
    TILE_SIZE,
    GameMode,
    EndReason,
    DIRECTION_KEYS,
)


class PlayScene(Scene):
    """Main gameplay scene."""

    def __init__(self, app: "App") -> None:  # type: ignore[name-defined]
        """Initialize the play scene.

        Args:
            app: The main application instance.
        """
        super().__init__(app)
        self.mode: GameMode = GameMode.CLASSIC
        self.input_handler = InputHandler()
        self.timing = TimingSystem()
        self.snake = Snake()
        self.food = Food()
        self.scoring = Scoring()
        self.hud = HUD(app.font)
        
        self.config = get_mode_config(GameMode.CLASSIC)
        self.walls: set[tuple[int, int]] = set()
        self.end_reason: EndReason | None = None

    def start_game(self, mode: GameMode, maze_index: int = 0) -> None:
        """Initialize a new game with the specified mode.

        Args:
            mode: The game mode to play.
            maze_index: Index of the maze layout to use for maze mode.
        """
        self.mode = mode
        self.config = get_mode_config(mode)
        
        # Setup walls for maze mode
        if self.config.has_walls:
            self.walls = get_map_set(maze_index)
        else:
            self.walls = set()
        
        # Reset game state
        self.input_handler.reset()
        self.timing.reset(is_time_attack=(mode == GameMode.TIME_ATTACK))
        self.snake.reset()
        self.scoring.reset()
        self.end_reason = None
        
        # Spawn initial food
        self.food.spawn(self.snake.segments, self.walls)

    def on_enter(self) -> None:
        """Handle scene entry by starting game music."""
        self.app.audio.play_music("game")

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events for gameplay input.

        Args:
            event: The pygame event to process.
        """
        if event.type != pygame.KEYDOWN:
            return
        
        if is_menu_key(event.key, "pause"):
            self.timing.toggle_pause()
            return
        
        if is_menu_key(event.key, "back"):
            self.app.audio.play_sound("sfx_menu_confirm")
            self.app.change_scene("main_menu")
            return
        
        if not self.timing.paused and event.key in DIRECTION_KEYS:
            self.input_handler.handle_key_down(event.key)

    def update(self, dt: float) -> None:
        """Update game state each frame.

        Args:
            dt: Delta time in seconds since last update.
        """
        if self.timing.paused:
            return
        
        # Update food animation
        self.food.update_animation(dt, self.timing.paused)
        
        # Time Attack timer
        if self.config.time_limit > 0:
            if self.timing.update_time_attack(dt):
                self._end_game(EndReason.TIME_UP)
                return
            
            # Per-second scoring
            if self.timing.check_second_scored():
                self.scoring.add_time_score()
        
        # Fixed-step movement
        ticks = self.timing.update(dt)
        for _ in range(ticks):
            self._process_tick()
            if self.end_reason:
                return

    def _process_tick(self) -> None:
        """Process a single movement tick.

        Handles direction changes, snake movement, collision detection,
        and food consumption for one game tick.
        """
        # Apply pending direction
        direction_changed = self.input_handler.direction_changed_on_tick()
        new_direction = self.input_handler.apply_pending_direction()
        self.snake.set_direction(new_direction)
        
        if direction_changed:
            self.app.audio.play_sound("sfx_turn")
        
        # Move snake
        new_head = self.snake.move(wrap=self.config.wrap_around)
        
        # Check collisions
        collision = check_collisions(
            new_head,
            self.snake.body,
            self.config.border_lethal,
            self.walls if self.config.has_walls else None,
        )
        
        if collision:
            self._end_game(collision)
            return
        
        # Check food collision
        if self.food.is_at(new_head):
            self.snake.grow()
            self.scoring.add_food_score()
            self.timing.increase_speed()
            self.app.audio.play_sound("sfx_eat")
            
            # Spawn new food
            if not self.food.spawn(self.snake.segments, self.walls):
                self._end_game(EndReason.VICTORY)

    def _end_game(self, reason: EndReason) -> None:
        """Handle game over and transition to results.

        Args:
            reason: The reason the game ended.
        """
        self.end_reason = reason
        
        if reason in (EndReason.SELF_COLLISION, EndReason.WALL_COLLISION):
            self.app.audio.play_sound("sfx_death")
        elif reason == EndReason.TIME_UP:
            self.app.audio.play_sound("sfx_timeup")
        
        # Transition to results
        self.app.show_results(self.mode, self.scoring.get_score(), reason)

    def render(self, surface: pygame.Surface) -> None:
        """Render the game scene.

        Args:
            surface: The pygame surface to render to.
        """
        surface.fill(COLOR_BG)
        
        # Render walls
        self._render_walls(surface)
        
        # Render food
        self._render_food(surface)
        
        # Render snake
        self._render_snake(surface)
        
        # Render HUD
        time_remaining = None
        if self.config.time_limit > 0:
            time_remaining = self.timing.time_remaining
        
        self.hud.render(
            surface,
            self.mode,
            self.scoring.get_score(),
            self.timing.ticks_per_second,
            time_remaining,
            self.timing.paused,
        )

    def _render_walls(self, surface: pygame.Surface) -> None:
        """Render wall tiles.

        Args:
            surface: The pygame surface to render to.
        """
        wall_sprite = self.app.sprites.get_wall_sprite()
        
        for x, y in self.walls:
            px, py = x * TILE_SIZE, y * TILE_SIZE
            if wall_sprite:
                surface.blit(wall_sprite, (px, py))
            else:
                pygame.draw.rect(surface, COLOR_WALL_GRAY, (px, py, TILE_SIZE, TILE_SIZE))

    def _render_food(self, surface: pygame.Surface) -> None:
        """Render food.

        Args:
            surface: The pygame surface to render to.
        """
        fx, fy = self.food.position
        px, py = fx * TILE_SIZE, fy * TILE_SIZE
        
        food_sprite = self.app.sprites.get_food_sprite(self.food.get_frame())
        if food_sprite:
            surface.blit(food_sprite, (px, py))
        else:
            pygame.draw.rect(surface, COLOR_FOOD_RED, (px, py, TILE_SIZE, TILE_SIZE))

    def _render_snake(self, surface: pygame.Surface) -> None:
        """Render snake with appropriate sprites.

        Args:
            surface: The pygame surface to render to.
        """
        segments = self.snake.segments
        directions = self.snake.get_segment_directions()
        
        for i, (pos, (incoming, outgoing)) in enumerate(zip(segments, directions)):
            px, py = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE
            
            if i == 0:
                # Head
                sprite = self.app.sprites.get_head_sprite(self.snake.direction)
            elif i == len(segments) - 1:
                # Tail
                if outgoing:
                    sprite = self.app.sprites.get_tail_sprite(outgoing)
                else:
                    sprite = self.app.sprites.get_tail_sprite(self.snake.direction)
            else:
                # Body
                sprite = self.app.sprites.get_body_sprite(incoming, outgoing)
            
            if sprite:
                surface.blit(sprite, (px, py))
            else:
                pygame.draw.rect(surface, COLOR_SNAKE_GREEN, (px, py, TILE_SIZE, TILE_SIZE))
