"""Name entry scene for high scores."""

import pygame

from src.scenes.base import Scene
from src.systems.input import is_menu_key
from src.systems.saves import save_highscores
from src.constants import (
    COLOR_BG,
    COLOR_WHITE,
    COLOR_UI_GOLD,
    NAME_CHARSET,
    NAME_LENGTH,
    GameMode,
)


class NameEntryScene(Scene):
    """3-letter name entry for high scores."""

    def __init__(self, app: "App") -> None:  # type: ignore[name-defined]
        super().__init__(app)
        self.mode: GameMode = GameMode.CLASSIC
        self.score: int = 0
        self.chars: list[int] = [0, 0, 0]  # Indices into NAME_CHARSET
        self.cursor_pos = 0
        self.blink_timer = 0.0
        self.show_cursor = True

    def set_data(self, mode: GameMode, score: int) -> None:
        """Set the mode and score for this entry."""
        self.mode = mode
        self.score = score
        self.chars = [0, 0, 0]
        self.cursor_pos = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        
        if is_menu_key(event.key, "up"):
            self.chars[self.cursor_pos] = (self.chars[self.cursor_pos] + 1) % len(NAME_CHARSET)
            self.app.audio.play_sound("sfx_menu_move")
        elif is_menu_key(event.key, "down"):
            self.chars[self.cursor_pos] = (self.chars[self.cursor_pos] - 1) % len(NAME_CHARSET)
            self.app.audio.play_sound("sfx_menu_move")
        elif is_menu_key(event.key, "left"):
            self.cursor_pos = max(0, self.cursor_pos - 1)
            self.app.audio.play_sound("sfx_menu_move")
        elif is_menu_key(event.key, "right"):
            self.cursor_pos = min(NAME_LENGTH - 1, self.cursor_pos + 1)
            self.app.audio.play_sound("sfx_menu_move")
        elif is_menu_key(event.key, "confirm"):
            self._save_and_continue()
        elif is_menu_key(event.key, "back"):
            self.app.audio.play_sound("sfx_menu_confirm")
            self.app.change_scene("main_menu")

    def _save_and_continue(self) -> None:
        """Save the high score and continue."""
        name = "".join(NAME_CHARSET[i] for i in self.chars)
        self.app.highscores.add_score(self.mode, name, self.score)
        save_highscores(self.app.highscores)
        self.app.audio.play_sound("sfx_menu_confirm")
        self.app.change_scene("highscores")

    def update(self, dt: float) -> None:
        # Cursor blink
        self.blink_timer += dt
        if self.blink_timer >= 0.3:
            self.blink_timer = 0.0
            self.show_cursor = not self.show_cursor

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(COLOR_BG)
        
        # Title
        self.app.font.render_centered("ENTER YOUR NAME", surface, 40, COLOR_UI_GOLD)
        
        # Score
        self.app.font.render_centered(f"SCORE: {self.score:04d}", surface, 70, COLOR_WHITE)
        
        # Name entry slots
        name_display = ""
        for i, char_idx in enumerate(self.chars):
            char = NAME_CHARSET[char_idx]
            if i == self.cursor_pos and not self.show_cursor:
                name_display += "_"
            else:
                name_display += char
            name_display += " "
        
        self.app.font.render_centered(name_display.strip(), surface, 110, COLOR_UI_GOLD)
        
        # Up/down arrows above/below current slot
        slot_width = self.app.font.get_text_width("A ")
        total_width = self.app.font.get_text_width(name_display.strip())
        start_x = (surface.get_width() - total_width) // 2
        cursor_x = start_x + self.cursor_pos * slot_width + slot_width // 4
        
        # Arrow indicators
        self.app.font.render_text("^", surface, cursor_x, 94, COLOR_WHITE)
        self.app.font.render_text("V", surface, cursor_x, 130, COLOR_WHITE)
        
        # Instructions
        self.app.font.render_centered("UP-DOWN: CHANGE", surface, 160, COLOR_WHITE)
        self.app.font.render_centered("LEFT-RIGHT: MOVE", surface, 176, COLOR_WHITE)
        self.app.font.render_centered("ENTER: CONFIRM", surface, 192, COLOR_UI_GOLD)
