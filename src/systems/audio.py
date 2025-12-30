"""Audio system for music and sound effects."""

from pathlib import Path
import pygame

from src.systems.logging_setup import get_logger


class AudioSystem:
    """Manages music and sound effects playback."""

    def __init__(self, assets_path: Path) -> None:
        self.assets_path = assets_path
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.current_music: str | None = None
        self._initialized = False

    def init(self) -> bool:
        """Initialize the audio system."""
        logger = get_logger()
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self._initialized = True
            logger.info("Audio system initialized")
            return True
        except pygame.error as e:
            logger.error(f"Failed to initialize audio: {e}")
            return False

    def load_sounds(self) -> bool:
        """Load all sound effects."""
        if not self._initialized:
            return False
        
        logger = get_logger()
        sfx_files = [
            "sfx_menu_move",
            "sfx_menu_confirm",
            "sfx_eat",
            "sfx_turn",
            "sfx_death",
            "sfx_timeup",
        ]
        
        audio_path = self.assets_path / "audio"
        for sfx_name in sfx_files:
            file_path = audio_path / f"{sfx_name}.wav"
            try:
                self.sounds[sfx_name] = pygame.mixer.Sound(file_path)
                logger.info(f"Loaded sound: {sfx_name}")
            except pygame.error as e:
                logger.warning(f"Failed to load sound {sfx_name}: {e}")
        
        return True

    def play_music(self, track: str) -> None:
        """Play a music track (menu or game)."""
        if not self._initialized:
            return
        
        logger = get_logger()
        if self.current_music == track:
            return
        
        music_file = self.assets_path / "audio" / f"music_{track}.ogg"
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)  # Loop infinitely
            self.current_music = track
            logger.info(f"Playing music: {track}")
        except pygame.error as e:
            logger.warning(f"Failed to play music {track}: {e}")

    def stop_music(self) -> None:
        """Stop the current music."""
        if self._initialized:
            pygame.mixer.music.stop()
            self.current_music = None

    def play_sound(self, name: str) -> None:
        """Play a sound effect."""
        if not self._initialized:
            return
        
        sound = self.sounds.get(name)
        if sound:
            sound.set_volume(self.sfx_volume)
            sound.play()

    def set_music_volume(self, volume: float) -> None:
        """Set music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        if self._initialized:
            pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume: float) -> None:
        """Set sound effects volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))

    def cleanup(self) -> None:
        """Clean up audio resources."""
        if self._initialized:
            pygame.mixer.quit()
            self._initialized = False
