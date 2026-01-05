"""Main application class."""

from pathlib import Path
import sys
import pygame

from src.constants import TARGET_FPS, GameMode, EndReason
from src.systems.logging_setup import setup_logging, get_logger
from src.systems.scaling import ScalingSystem
from src.systems.audio import AudioSystem
from src.systems.saves import (
    Settings,
    HighScores,
    load_settings,
    load_highscores,
)
from src.render.sprite_atlas import SpriteAtlas
from src.render.font import BitmapFont
from src.scenes.base import Scene
from src.scenes.main_menu import MainMenuScene
from src.scenes.mode_select import ModeSelectScene
from src.scenes.options import OptionsScene
from src.scenes.highscores import HighScoresScene
from src.scenes.play import PlayScene
from src.scenes.results import ResultsScene
from src.scenes.name_entry import NameEntryScene


class App:
    """Main application class."""

    def __init__(self) -> None:
        """Initialize the App instance.

        Sets up initial state including clock, assets path detection,
        and creates instances of all core systems (settings, scaling,
        audio, sprites, font) with default or placeholder values.
        """
        self.running = False
        self.clock = pygame.time.Clock()
        
        # Determine assets path
        if getattr(sys, "frozen", False):
            # Running as PyInstaller bundle
            self.assets_path = Path(sys._MEIPASS) / "assets"  # type: ignore[attr-defined]
        else:
            # Running from source
            self.assets_path = Path(__file__).parent.parent / "assets"
        
        # Systems
        self.settings: Settings = Settings()
        self.highscores: HighScores = HighScores()
        self.scaling: ScalingSystem = ScalingSystem()
        self.audio: AudioSystem = AudioSystem(self.assets_path)
        self.sprites: SpriteAtlas = SpriteAtlas(self.assets_path)
        self.font: BitmapFont = BitmapFont(self.assets_path)
        
        # Scenes
        self.scenes: dict[str, Scene] = {}
        self.current_scene: Scene | None = None
        
        # Maze map index (session-only)
        self.maze_map_index = 0

    def init(self) -> bool:
        """Initialize the application.

        Initializes pygame, loads settings and high scores, sets up display
        scaling, audio system, sprites, fonts, and creates all game scenes.

        Returns:
            bool: True if initialization succeeded, False on fatal error.
        """
        logger = setup_logging()
        logger.info("Application starting")
        
        # Initialize pygame
        pygame.init()
        
        # Load settings and apply
        self.settings = load_settings()
        self.highscores = load_highscores()
        
        # Initialize scaling
        self.scaling = ScalingSystem(self.settings.scale, self.settings.fullscreen)
        self.scaling.init_display()
        
        # Initialize audio
        if not self.audio.init():
            logger.warning("Audio initialization failed, continuing without sound")
        else:
            self.audio.load_sounds()
            self.audio.set_music_volume(self.settings.music_volume)
            self.audio.set_sfx_volume(self.settings.sfx_volume)
        
        # Load sprites
        if not self.sprites.load():
            self._show_fatal_error("Failed to load required sprites")
            return False
        
        # Load font
        if not self.font.load():
            self._show_fatal_error("Failed to load font")
            return False
        
        # Create scenes
        self.scenes = {
            "main_menu": MainMenuScene(self),
            "mode_select": ModeSelectScene(self),
            "options": OptionsScene(self),
            "highscores": HighScoresScene(self),
            "play": PlayScene(self),
            "results": ResultsScene(self),
            "name_entry": NameEntryScene(self),
        }
        
        # Start at main menu
        self.change_scene("main_menu")
        
        logger.info("Application initialized successfully")
        return True

    def _show_fatal_error(self, message: str) -> None:
        """Show fatal error screen.

        Displays an error message on a red background for 5 seconds.
        Logs the error as critical. Fails silently if display is unavailable.

        Args:
            message: The error message to display.
        """
        logger = get_logger()
        logger.critical(message)
        
        # Try to show error on screen
        try:
            surface = self.scaling.get_internal_surface()
            surface.fill((64, 0, 0))
            
            # Simple text rendering without font system
            pygame.font.init()
            font = pygame.font.Font(None, 24)
            text = font.render(message, True, (255, 255, 255))
            rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
            surface.blit(text, rect)
            
            self.scaling.render_to_screen()
            pygame.time.wait(5000)
        except Exception:
            pass

    def run(self) -> int:
        """Main application loop.

        Runs the game loop handling events, updates, and rendering at the
        target frame rate until the application is signaled to stop.

        Returns:
            int: Exit code (0 for normal exit, 1 for critical error).
        """
        logger = get_logger()
        self.running = True
        
        try:
            while self.running:
                dt = self.clock.tick(TARGET_FPS) / 1000.0
                
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif self.current_scene:
                        self.current_scene.handle_event(event)
                
                # Update
                if self.current_scene:
                    self.current_scene.update(dt)
                
                # Render
                surface = self.scaling.get_internal_surface()
                if self.current_scene:
                    self.current_scene.render(surface)
                
                self.scaling.render_to_screen()
            
            logger.info("Application exiting normally")
            return 0
            
        except Exception as e:
            logger.critical(f"Unhandled exception: {e}", exc_info=True)
            self._show_fatal_error(f"Critical error: {e}")
            return 1
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """Clean up resources.

        Releases audio resources and shuts down pygame.
        """
        logger = get_logger()
        self.audio.cleanup()
        pygame.quit()
        logger.info("Application cleanup complete")

    def change_scene(self, scene_name: str) -> None:
        """Change to a different scene.

        Exits the current scene (if any) and enters the new scene.

        Args:
            scene_name: The key of the scene to switch to.
        """
        if self.current_scene:
            self.current_scene.on_exit()
        
        self.current_scene = self.scenes.get(scene_name)
        if self.current_scene:
            self.current_scene.on_enter()

    def start_game(self, mode: GameMode) -> None:
        """Start a new game with the specified mode.

        Configures the play scene for the given game mode and transitions to it.
        For maze mode, cycles through available maze maps.

        Args:
            mode: The game mode to start.
        """
        play_scene = self.scenes.get("play")
        if isinstance(play_scene, PlayScene):
            maze_idx = 0
            if mode == GameMode.MAZE:
                maze_idx = self.maze_map_index
                self.maze_map_index = (self.maze_map_index + 1) % 5
            
            play_scene.start_game(mode, maze_idx)
            self.change_scene("play")

    def show_results(self, mode: GameMode, score: int, reason: EndReason) -> None:
        """Show the results screen.

        Configures and displays the results scene with game outcome data.

        Args:
            mode: The game mode that was played.
            score: The final score achieved.
            reason: The reason the game ended.
        """
        results_scene = self.scenes.get("results")
        if isinstance(results_scene, ResultsScene):
            results_scene.set_results(mode, score, reason)
            self.change_scene("results")

    def show_name_entry(self, mode: GameMode, score: int) -> None:
        """Show the name entry screen.

        Configures and displays the name entry scene for high score recording.

        Args:
            mode: The game mode that was played.
            score: The score to record.
        """
        name_entry_scene = self.scenes.get("name_entry")
        if isinstance(name_entry_scene, NameEntryScene):
            name_entry_scene.set_data(mode, score)
            self.change_scene("name_entry")

    def quit(self) -> None:
        """Quit the application.

        Signals the main loop to stop running.
        """
        self.running = False
