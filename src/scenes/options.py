"""Options menu scene."""

import pygame

from src.scenes.base import Scene
from src.systems.input import is_menu_key
from src.systems.saves import save_settings
from src.constants import (
    COLOR_BG,
    COLOR_WHITE,
    COLOR_UI_GOLD,
    MIN_SCALE,
    MAX_SCALE,
    VOLUME_STEP,
)


class OptionsScene(Scene):
    """Options menu for settings."""

    MENU_ITEMS = ["SCALE", "FULLSCREEN", "MUSIC VOLUME", "SFX VOLUME", "BACK"]

    def __init__(self, app: "App") -> None:  # type: ignore[name-defined]
        super().__init__(app)
        self.selected_index = 0

    def on_enter(self) -> None:
        self.selected_index = 0

    def on_exit(self) -> None:
        save_settings(self.app.settings)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        
        if is_menu_key(event.key, "up"):
            self.selected_index = (self.selected_index - 1) % len(self.MENU_ITEMS)
            self.app.audio.play_sound("sfx_menu_move")
        elif is_menu_key(event.key, "down"):
            self.selected_index = (self.selected_index + 1) % len(self.MENU_ITEMS)
            self.app.audio.play_sound("sfx_menu_move")
        elif is_menu_key(event.key, "left"):
            self._adjust_value(-1)
            self.app.audio.play_sound("sfx_menu_move")
        elif is_menu_key(event.key, "right"):
            self._adjust_value(1)
            self.app.audio.play_sound("sfx_menu_move")
        elif is_menu_key(event.key, "confirm"):
            self._handle_confirm()
        elif is_menu_key(event.key, "back"):
            self.app.audio.play_sound("sfx_menu_confirm")
            self.app.change_scene("main_menu")

    def _adjust_value(self, delta: int) -> None:
        item = self.MENU_ITEMS[self.selected_index]
        settings = self.app.settings
        
        if item == "SCALE":
            settings.scale = max(MIN_SCALE, min(MAX_SCALE, settings.scale + delta))
            if not settings.fullscreen:
                self.app.scaling.set_scale(settings.scale)
        elif item == "FULLSCREEN":
            settings.fullscreen = not settings.fullscreen
            self.app.scaling.set_fullscreen(settings.fullscreen)
        elif item == "MUSIC VOLUME":
            settings.music_volume = max(0.0, min(1.0, settings.music_volume + delta * VOLUME_STEP))
            self.app.audio.set_music_volume(settings.music_volume)
        elif item == "SFX VOLUME":
            settings.sfx_volume = max(0.0, min(1.0, settings.sfx_volume + delta * VOLUME_STEP))
            self.app.audio.set_sfx_volume(settings.sfx_volume)

    def _handle_confirm(self) -> None:
        item = self.MENU_ITEMS[self.selected_index]
        if item == "BACK":
            self.app.audio.play_sound("sfx_menu_confirm")
            self.app.change_scene("main_menu")
        elif item == "FULLSCREEN":
            self._adjust_value(1)
            self.app.audio.play_sound("sfx_menu_confirm")

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(COLOR_BG)
        
        # Title
        self.app.font.render_centered("OPTIONS", surface, 40, COLOR_UI_GOLD)
        
        settings = self.app.settings
        values = {
            "SCALE": str(settings.scale),
            "FULLSCREEN": "ON" if settings.fullscreen else "OFF",
            "MUSIC VOLUME": f"{int(settings.music_volume * 100)}%",
            "SFX VOLUME": f"{int(settings.sfx_volume * 100)}%",
            "BACK": "",
        }
        
        # Menu items
        start_y = 80
        for i, item in enumerate(self.MENU_ITEMS):
            color = COLOR_UI_GOLD if i == self.selected_index else COLOR_WHITE
            prefix = "> " if i == self.selected_index else "  "
            
            value = values.get(item, "")
            if value:
                text = f"{prefix}{item}: {value}"
            else:
                text = f"{prefix}{item}"
            
            self.app.font.render_centered(text, surface, start_y + i * 24, color)
