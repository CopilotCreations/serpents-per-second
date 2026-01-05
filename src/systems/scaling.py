"""Scaling system for pixel-perfect integer scaling."""

import os
import pygame

from src.constants import (
    INTERNAL_WIDTH,
    INTERNAL_HEIGHT,
    MIN_SCALE,
    MAX_SCALE,
    DEFAULT_SCALE,
    COLOR_BLACK,
)


class ScalingSystem:
    """Manages internal surface and integer scaling to display."""

    def __init__(self, initial_scale: int = DEFAULT_SCALE, fullscreen: bool = False) -> None:
        """Initialize the scaling system.

        Args:
            initial_scale: The initial integer scale factor. Clamped between
                MIN_SCALE and MAX_SCALE. Can be overridden by SPS_FORCE_SCALE
                environment variable.
            fullscreen: Whether to start in fullscreen mode. Can be overridden
                by SPS_FORCE_WINDOWED environment variable.
        """
        # Check for environment overrides
        force_scale = os.environ.get("SPS_FORCE_SCALE")
        force_windowed = os.environ.get("SPS_FORCE_WINDOWED")
        
        if force_scale:
            try:
                initial_scale = int(force_scale)
            except ValueError:
                pass
        
        if force_windowed == "1":
            fullscreen = False
        
        self.scale = max(MIN_SCALE, min(MAX_SCALE, initial_scale))
        self.fullscreen = fullscreen
        
        # Internal surface at SNES resolution
        self.internal_surface = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT))
        
        # Display setup
        self.screen: pygame.Surface | None = None
        self.letterbox_rect = pygame.Rect(0, 0, INTERNAL_WIDTH, INTERNAL_HEIGHT)
        
    def init_display(self) -> pygame.Surface:
        """Initialize or reinitialize the display.

        Creates or recreates the pygame display surface based on current
        scale and fullscreen settings. In fullscreen mode, calculates the
        largest integer scale that fits and centers the game with letterboxing.

        Returns:
            The pygame display surface.
        """
        if self.fullscreen:
            display_info = pygame.display.Info()
            display_w, display_h = display_info.current_w, display_info.current_h
            
            # Calculate largest integer scale that fits
            scale_x = display_w // INTERNAL_WIDTH
            scale_y = display_h // INTERNAL_HEIGHT
            self.scale = max(1, min(scale_x, scale_y, MAX_SCALE))
            
            self.screen = pygame.display.set_mode((display_w, display_h), pygame.FULLSCREEN)
            
            # Calculate letterbox positioning
            scaled_w = INTERNAL_WIDTH * self.scale
            scaled_h = INTERNAL_HEIGHT * self.scale
            offset_x = (display_w - scaled_w) // 2
            offset_y = (display_h - scaled_h) // 2
            self.letterbox_rect = pygame.Rect(offset_x, offset_y, scaled_w, scaled_h)
        else:
            window_w = INTERNAL_WIDTH * self.scale
            window_h = INTERNAL_HEIGHT * self.scale
            self.screen = pygame.display.set_mode((window_w, window_h))
            self.letterbox_rect = pygame.Rect(0, 0, window_w, window_h)
        
        pygame.display.set_caption("Serpents Per Second")
        return self.screen
    
    def set_scale(self, scale: int) -> None:
        """Change the display scale.

        Args:
            scale: The new integer scale factor. Will be clamped between
                MIN_SCALE and MAX_SCALE.
        """
        self.scale = max(MIN_SCALE, min(MAX_SCALE, scale))
        if not self.fullscreen:
            self.init_display()
    
    def set_fullscreen(self, fullscreen: bool) -> None:
        """Set fullscreen mode.

        Args:
            fullscreen: True to enable fullscreen mode with letterboxing,
                False for windowed mode.
        """
        self.fullscreen = fullscreen
        self.init_display()
    
    def render_to_screen(self) -> None:
        """Scale internal surface to screen with letterboxing.

        Clears the screen with black (for letterbox bars), scales the
        internal surface using integer scaling, and blits it to the
        display at the letterbox offset position.
        """
        if self.screen is None:
            return
        
        # Clear screen (letterbox bars)
        self.screen.fill(COLOR_BLACK)
        
        # Scale internal surface
        scaled = pygame.transform.scale(
            self.internal_surface,
            (INTERNAL_WIDTH * self.scale, INTERNAL_HEIGHT * self.scale)
        )
        
        # Blit to screen with letterbox offset
        self.screen.blit(scaled, (self.letterbox_rect.x, self.letterbox_rect.y))
        
        pygame.display.flip()
    
    def get_internal_surface(self) -> pygame.Surface:
        """Get the internal rendering surface.

        Returns:
            The internal pygame Surface at SNES resolution (INTERNAL_WIDTH x
            INTERNAL_HEIGHT) that all game rendering should target.
        """
        return self.internal_surface
