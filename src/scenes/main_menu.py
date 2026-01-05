"""Main menu scene."""

import pygame

from src.scenes.base import Scene
from src.systems.input import is_menu_key
from src.constants import COLOR_BG, COLOR_WHITE, COLOR_UI_GOLD, INTERNAL_HEIGHT


class MainMenuScene(Scene):
    """Main menu with Play, Options, High Scores, Quit."""

    MENU_ITEMS = ["PLAY", "OPTIONS", "HIGH SCORES", "QUIT"]

    def __init__(self, app: "App") -> None:  # type: ignore[name-defined]
        """Initialize the main menu scene.

        Args:
            app: The application instance managing scenes and resources.
        """
        super().__init__(app)
        self.selected_index = 0

    def on_enter(self) -> None:
        """Handle scene entry by starting menu music."""
        self.app.audio.play_music("menu")

    def handle_event(self, event: pygame.event.Event) -> None:
        """Process input events for menu navigation.

        Args:
            event: The pygame event to process.
        """
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

    def _select_item(self) -> None:
        """Execute the action for the currently selected menu item."""
        item = self.MENU_ITEMS[self.selected_index]
        if item == "PLAY":
            self.app.change_scene("mode_select")
        elif item == "OPTIONS":
            self.app.change_scene("options")
        elif item == "HIGH SCORES":
            self.app.change_scene("highscores")
        elif item == "QUIT":
            self.app.quit()

    def update(self, dt: float) -> None:
        """Update scene state each frame.

        Args:
            dt: Delta time in seconds since the last frame.
        """
        pass

    def render(self, surface: pygame.Surface) -> None:
        """Draw the main menu to the screen.

        Args:
            surface: The pygame surface to render onto.
        """
        surface.fill(COLOR_BG)
        
        # Title
        self.app.font.render_centered("SERPENTS PER SECOND", surface, 40, COLOR_UI_GOLD)
        
        # Menu items
        start_y = 100
        for i, item in enumerate(self.MENU_ITEMS):
            color = COLOR_UI_GOLD if i == self.selected_index else COLOR_WHITE
            prefix = "> " if i == self.selected_index else "  "
            self.app.font.render_centered(prefix + item, surface, start_y + i * 24, color)
