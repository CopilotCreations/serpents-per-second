"""Mode selection scene."""

import pygame

from src.scenes.base import Scene
from src.systems.input import is_menu_key
from src.constants import COLOR_BG, COLOR_WHITE, COLOR_UI_GOLD, GameMode


class ModeSelectScene(Scene):
    """Mode selection menu."""

    MENU_ITEMS = [
        ("CLASSIC", GameMode.CLASSIC),
        ("BOXED", GameMode.BOXED),
        ("MAZE", GameMode.MAZE),
        ("TIME ATTACK", GameMode.TIME_ATTACK),
        ("BACK", None),
    ]

    def __init__(self, app: "App") -> None:  # type: ignore[name-defined]
        super().__init__(app)
        self.selected_index = 0

    def on_enter(self) -> None:
        self.selected_index = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        
        if is_menu_key(event.key, "up"):
            self.selected_index = (self.selected_index - 1) % len(self.MENU_ITEMS)
            self.app.audio.play_sound("sfx_menu_move")
        elif is_menu_key(event.key, "down"):
            self.selected_index = (self.selected_index + 1) % len(self.MENU_ITEMS)
            self.app.audio.play_sound("sfx_menu_move")
        elif is_menu_key(event.key, "confirm"):
            self.app.audio.play_sound("sfx_menu_confirm")
            self._select_item()
        elif is_menu_key(event.key, "back"):
            self.app.audio.play_sound("sfx_menu_confirm")
            self.app.change_scene("main_menu")

    def _select_item(self) -> None:
        _, mode = self.MENU_ITEMS[self.selected_index]
        if mode is None:
            self.app.change_scene("main_menu")
        else:
            self.app.start_game(mode)

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(COLOR_BG)
        
        # Title
        self.app.font.render_centered("SELECT MODE", surface, 40, COLOR_UI_GOLD)
        
        # Menu items
        start_y = 80
        for i, (name, _) in enumerate(self.MENU_ITEMS):
            color = COLOR_UI_GOLD if i == self.selected_index else COLOR_WHITE
            prefix = "> " if i == self.selected_index else "  "
            self.app.font.render_centered(prefix + name, surface, start_y + i * 24, color)
