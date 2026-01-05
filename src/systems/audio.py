"""Audio system for music and sound effects."""

from pathlib import Path
import pygame

from src.systems.logging_setup import get_logger


class AudioSystem:
    """Manages music and sound effects playback."""

    def __init__(self, assets_path: Path) -> None:
        """Initialize the AudioSystem with default settings.

        Args:
            assets_path: Path to the assets directory containing audio files.
        """
        self.assets_path = assets_path
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.current_music: str | None = None
        self._initialized = False

    def init(self) -> bool:
        """Initialize the pygame audio mixer.

        Configures the mixer with 44100 Hz frequency, 16-bit signed audio,
        stereo channels, and a 512 sample buffer.

        Returns:
            True if initialization succeeded, False otherwise.
        """
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
        """Load all sound effect files from the assets directory.

        Loads WAV files for menu navigation, eating, turning, death,
        and time-up sound effects.

        Returns:
            True if the audio system was initialized and loading was
            attempted, False if the system was not initialized.
        """
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
        """Play a music track in an infinite loop.

        If the requested track is already playing, this method does nothing.

        Args:
            track: Name of the track to play (e.g., "menu" or "game").
                The corresponding file should be at assets/audio/music_{track}.ogg.
        """
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
        """Stop the currently playing music track.

        Resets the current_music state to None.
        """
        if self._initialized:
            pygame.mixer.music.stop()
            self.current_music = None

    def play_sound(self, name: str) -> None:
        """Play a sound effect by name.

        Args:
            name: The name of the sound effect to play (e.g., "sfx_eat").
                Must have been previously loaded via load_sounds().
        """
        if not self._initialized:
            return
        
        sound = self.sounds.get(name)
        if sound:
            sound.set_volume(self.sfx_volume)
            sound.play()

    def set_music_volume(self, volume: float) -> None:
        """Set the music playback volume.

        Args:
            volume: Volume level from 0.0 (silent) to 1.0 (full volume).
                Values outside this range are clamped.
        """
        self.music_volume = max(0.0, min(1.0, volume))
        if self._initialized:
            pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume: float) -> None:
        """Set the sound effects playback volume.

        Args:
            volume: Volume level from 0.0 (silent) to 1.0 (full volume).
                Values outside this range are clamped.
        """
        self.sfx_volume = max(0.0, min(1.0, volume))

    def cleanup(self) -> None:
        """Clean up audio resources and shut down the mixer.

        Should be called when the application exits to properly
        release audio system resources.
        """
        if self._initialized:
            pygame.mixer.quit()
            self._initialized = False
