"""Base scene class."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.app import App


class Scene(ABC):
    """Abstract base class for game scenes."""

    def __init__(self, app: "App") -> None:
        self.app = app

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle a pygame event."""
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update scene state."""
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """Render the scene to the internal surface."""
        pass

    def on_enter(self) -> None:
        """Called when entering this scene."""
        pass

    def on_exit(self) -> None:
        """Called when leaving this scene."""
        pass
