"""Results screen scene."""

import pygame

from src.scenes.base import Scene
from src.systems.input import is_menu_key
from src.constants import COLOR_BG, COLOR_WHITE, COLOR_UI_GOLD, GameMode, EndReason


class ResultsScene(Scene):
    """Game over / results screen."""

    def __init__(self, app: "App") -> None:  # type: ignore[name-defined]
        super().__init__(app)
        self.mode: GameMode = GameMode.CLASSIC
        self.score: int = 0
        self.end_reason: EndReason = EndReason.SELF_COLLISION

    def set_results(self, mode: GameMode, score: int, reason: EndReason) -> None:
        """Set the results to display."""
        self.mode = mode
        self.score = score
        self.end_reason = reason

    def on_enter(self) -> None:
        self.app.audio.play_music("menu")

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        
        if is_menu_key(event.key, "confirm"):
            self.app.audio.play_sound("sfx_menu_confirm")
            # Check if score qualifies for high scores
            if self.app.highscores.qualifies(self.mode, self.score):
                self.app.show_name_entry(self.mode, self.score)
            else:
                # Play again
                self.app.start_game(self.mode)
        elif is_menu_key(event.key, "back"):
            self.app.audio.play_sound("sfx_menu_confirm")
            # Check if score qualifies for high scores
            if self.app.highscores.qualifies(self.mode, self.score):
                self.app.show_name_entry(self.mode, self.score)
            else:
                self.app.change_scene("main_menu")

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(COLOR_BG)
        
        # End reason title
        title = self.end_reason.value
        self.app.font.render_centered(title, surface, 50, COLOR_UI_GOLD)
        
        # Mode
        mode_name = self.mode.value.replace("_", " ").upper()
        self.app.font.render_centered(f"MODE: {mode_name}", surface, 90, COLOR_WHITE)
        
        # Score
        self.app.font.render_centered(f"SCORE: {self.score:04d}", surface, 120, COLOR_UI_GOLD)
        
        # Instructions
        if self.app.highscores.qualifies(self.mode, self.score):
            self.app.font.render_centered("NEW HIGH SCORE!", surface, 160, COLOR_UI_GOLD)
        
        self.app.font.render_centered("ENTER: PLAY AGAIN", surface, 180, COLOR_WHITE)
        self.app.font.render_centered("ESC: MAIN MENU", surface, 200, COLOR_WHITE)
