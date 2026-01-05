"""High scores display scene."""

import pygame

from src.scenes.base import Scene
from src.systems.input import is_menu_key
from src.constants import COLOR_BG, COLOR_WHITE, COLOR_UI_GOLD, GameMode


class HighScoresScene(Scene):
    """High scores viewer with mode switching."""

    MODES = [GameMode.CLASSIC, GameMode.BOXED, GameMode.MAZE, GameMode.TIME_ATTACK]

    def __init__(self, app: "App") -> None:  # type: ignore[name-defined]
        """Initialize the high scores scene.

        Args:
            app: The main application instance.
        """
        super().__init__(app)
        self.mode_index = 0

    def on_enter(self) -> None:
        """Reset the mode index when entering the scene."""
        self.mode_index = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle keyboard input for navigation and mode switching.

        Args:
            event: The pygame event to process.
        """
        if event.type != pygame.KEYDOWN:
            return
        
        if is_menu_key(event.key, "left"):
            self.mode_index = (self.mode_index - 1) % len(self.MODES)
            self.app.audio.play_sound("sfx_menu_move")
        elif is_menu_key(event.key, "right"):
            self.mode_index = (self.mode_index + 1) % len(self.MODES)
            self.app.audio.play_sound("sfx_menu_move")
        elif is_menu_key(event.key, "back") or is_menu_key(event.key, "confirm"):
            self.app.audio.play_sound("sfx_menu_confirm")
            self.app.change_scene("main_menu")

    def update(self, dt: float) -> None:
        """Update the scene state.

        Args:
            dt: Delta time since last update in seconds.
        """
        pass

    def render(self, surface: pygame.Surface) -> None:
        """Render the high scores display.

        Args:
            surface: The pygame surface to render to.
        """
        surface.fill(COLOR_BG)
        
        mode = self.MODES[self.mode_index]
        mode_name = mode.value.replace("_", " ").upper()
        
        # Title with arrows
        arrow_left = "<" if self.mode_index > 0 else " "
        arrow_right = ">" if self.mode_index < len(self.MODES) - 1 else " "
        title = f"{arrow_left} {mode_name} {arrow_right}"
        self.app.font.render_centered(title, surface, 20, COLOR_UI_GOLD)
        
        # High scores
        scores = self.app.highscores.get_scores(mode)
        start_y = 50
        
        if not scores:
            self.app.font.render_centered("NO SCORES YET", surface, start_y + 40, COLOR_WHITE)
        else:
            for i, entry in enumerate(scores):
                rank = f"{i + 1:2d}."
                name = entry.name
                score = f"{entry.score:04d}"
                text = f"{rank} {name} {score}"
                self.app.font.render_centered(text, surface, start_y + i * 16, COLOR_WHITE)
        
        # Back hint
        self.app.font.render_centered("ESC TO RETURN", surface, 200, COLOR_UI_GOLD)
