"""HUD rendering."""

import pygame

from src.constants import (
    INTERNAL_WIDTH,
    COLOR_WHITE,
    COLOR_UI_GOLD,
    GameMode,
)
from src.render.font import BitmapFont


class HUD:
    """Renders in-game HUD elements."""

    def __init__(self, font: BitmapFont) -> None:
        """Initialize the HUD renderer.

        Args:
            font: The bitmap font used for rendering text.
        """
        self.font = font

    def render(
        self,
        surface: pygame.Surface,
        mode: GameMode,
        score: int,
        ticks_per_second: float,
        time_remaining: float | None = None,
        paused: bool = False,
    ) -> None:
        """Render the HUD.

        Args:
            surface: The pygame surface to render the HUD onto.
            mode: The current game mode to display.
            score: The player's current score.
            ticks_per_second: The current game speed in ticks per second.
            time_remaining: Time remaining in seconds for Time Attack mode,
                or None for other modes.
            paused: Whether the game is currently paused.
        """
        # Mode name (top left)
        mode_name = mode.value.replace("_", " ").upper()
        self.font.render_text(mode_name, surface, 4, 4, COLOR_UI_GOLD)
        
        # Score (top right)
        score_text = f"SCORE:{score:04d}"
        score_width = self.font.get_text_width(score_text)
        self.font.render_text(score_text, surface, INTERNAL_WIDTH - score_width - 4, 4, COLOR_WHITE)
        
        # Speed (below mode name)
        speed_text = f"{ticks_per_second:.2f}TPS"
        self.font.render_text(speed_text, surface, 4, 20, COLOR_WHITE)
        
        # Time remaining (for Time Attack)
        if time_remaining is not None:
            time_remaining = max(0, time_remaining)
            minutes = int(time_remaining) // 60
            seconds = int(time_remaining) % 60
            time_text = f"TIME:{minutes:02d}:{seconds:02d}"
            time_width = self.font.get_text_width(time_text)
            self.font.render_text(
                time_text, surface, INTERNAL_WIDTH - time_width - 4, 20, COLOR_UI_GOLD
            )
        
        # Pause overlay
        if paused:
            self._render_pause_overlay(surface)

    def _render_pause_overlay(self, surface: pygame.Surface) -> None:
        """Render pause overlay.

        Draws a semi-transparent dark overlay and centered pause text.

        Args:
            surface: The pygame surface to render the overlay onto.
        """
        # Semi-transparent overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        surface.blit(overlay, (0, 0))
        
        # Pause text
        self.font.render_centered("PAUSED", surface, 100, COLOR_UI_GOLD)
        self.font.render_centered("PRESS P TO RESUME", surface, 120, COLOR_WHITE)
