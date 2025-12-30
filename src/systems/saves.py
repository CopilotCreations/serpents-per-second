"""Settings and high scores persistence."""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

from src.constants import (
    SAVES_DIR,
    SETTINGS_FILE,
    HIGHSCORES_FILE,
    DEFAULT_SCALE,
    DEFAULT_MUSIC_VOLUME,
    DEFAULT_SFX_VOLUME,
    MIN_SCALE,
    MAX_SCALE,
    MAX_HIGHSCORES,
    NAME_CHARSET,
    GameMode,
)
from src.systems.logging_setup import get_logger


def _ensure_dirs() -> None:
    """Ensure save directories exist."""
    SAVES_DIR.mkdir(parents=True, exist_ok=True)


def _clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value to a range."""
    return max(min_val, min(max_val, value))


def _validate_name(name: str) -> str:
    """Validate and sanitize a high score name."""
    if not isinstance(name, str) or len(name) != 3:
        return "AAA"
    sanitized = ""
    for char in name.upper():
        if char in NAME_CHARSET:
            sanitized += char
        else:
            sanitized += "A"
    return sanitized[:3] if len(sanitized) >= 3 else "AAA"


class Settings:
    """Game settings with persistence."""

    def __init__(self) -> None:
        self.version = 1
        self.scale = DEFAULT_SCALE
        self.fullscreen = False
        self.music_volume = DEFAULT_MUSIC_VOLUME
        self.sfx_volume = DEFAULT_SFX_VOLUME
        self._dirty = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "scale": self.scale,
            "fullscreen": self.fullscreen,
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
        }

    def from_dict(self, data: dict[str, Any]) -> None:
        logger = get_logger()
        try:
            if "scale" in data:
                scale = int(data["scale"])
                if scale < MIN_SCALE or scale > MAX_SCALE:
                    logger.warning(f"Scale {scale} out of range, clamping")
                self.scale = int(_clamp(scale, MIN_SCALE, MAX_SCALE))
            
            if "fullscreen" in data:
                self.fullscreen = bool(data["fullscreen"])
            
            if "music_volume" in data:
                vol = float(data["music_volume"])
                if vol < 0.0 or vol > 1.0:
                    logger.warning(f"Music volume {vol} out of range, clamping")
                self.music_volume = _clamp(vol, 0.0, 1.0)
            
            if "sfx_volume" in data:
                vol = float(data["sfx_volume"])
                if vol < 0.0 or vol > 1.0:
                    logger.warning(f"SFX volume {vol} out of range, clamping")
                self.sfx_volume = _clamp(vol, 0.0, 1.0)
        except (TypeError, ValueError) as e:
            logger.warning(f"Error parsing settings field: {e}")


def load_settings() -> Settings:
    """Load settings from file or return defaults."""
    logger = get_logger()
    settings = Settings()
    _ensure_dirs()
    
    if not SETTINGS_FILE.exists():
        logger.info("Settings file not found, using defaults")
        return settings
    
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        settings.from_dict(data)
        logger.info("Settings loaded successfully")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in settings file: {e}")
        save_settings(settings)
    except Exception as e:
        logger.error(f"Error loading settings: {e}")
    
    return settings


def save_settings(settings: Settings) -> bool:
    """Save settings to file."""
    logger = get_logger()
    _ensure_dirs()
    
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings.to_dict(), f, indent=2)
        logger.info("Settings saved successfully")
        return True
    except Exception as e:
        logger.error(f"Error saving settings: {e}")
        return False


class HighScoreEntry:
    """A single high score entry."""

    def __init__(self, name: str, score: int, ts: str | None = None) -> None:
        self.name = _validate_name(name)
        self.score = max(0, int(score))
        self.ts = ts or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "score": self.score, "ts": self.ts}

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "HighScoreEntry":
        return HighScoreEntry(
            name=data.get("name", "AAA"),
            score=data.get("score", 0),
            ts=data.get("ts"),
        )


class HighScores:
    """High scores for all game modes."""

    def __init__(self) -> None:
        self.version = 1
        self.scores: dict[str, list[HighScoreEntry]] = {
            GameMode.CLASSIC.value: [],
            GameMode.BOXED.value: [],
            GameMode.MAZE.value: [],
            GameMode.TIME_ATTACK.value: [],
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            **{mode: [e.to_dict() for e in entries] for mode, entries in self.scores.items()},
        }

    def from_dict(self, data: dict[str, Any]) -> None:
        logger = get_logger()
        for mode in self.scores:
            if mode in data and isinstance(data[mode], list):
                try:
                    entries = [HighScoreEntry.from_dict(e) for e in data[mode] if isinstance(e, dict)]
                    self.scores[mode] = sorted(
                        entries, key=lambda e: (-e.score, e.ts)
                    )[:MAX_HIGHSCORES]
                except Exception as e:
                    logger.warning(f"Error parsing {mode} high scores: {e}")

    def qualifies(self, mode: GameMode, score: int) -> bool:
        """Check if a score qualifies for the leaderboard."""
        entries = self.scores.get(mode.value, [])
        if len(entries) < MAX_HIGHSCORES:
            return True
        return score > entries[-1].score

    def add_score(self, mode: GameMode, name: str, score: int) -> bool:
        """Add a score to the leaderboard if it qualifies."""
        if not self.qualifies(mode, score):
            return False
        
        entry = HighScoreEntry(name, score)
        entries = self.scores.get(mode.value, [])
        entries.append(entry)
        entries.sort(key=lambda e: (-e.score, e.ts))
        self.scores[mode.value] = entries[:MAX_HIGHSCORES]
        return True

    def get_scores(self, mode: GameMode) -> list[HighScoreEntry]:
        """Get high scores for a specific mode."""
        return self.scores.get(mode.value, [])


def load_highscores() -> HighScores:
    """Load high scores from file or return empty structure."""
    logger = get_logger()
    highscores = HighScores()
    _ensure_dirs()
    
    if not HIGHSCORES_FILE.exists():
        logger.info("High scores file not found, creating empty")
        save_highscores(highscores)
        return highscores
    
    try:
        with open(HIGHSCORES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        highscores.from_dict(data)
        logger.info("High scores loaded successfully")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in high scores file: {e}")
        save_highscores(highscores)
    except Exception as e:
        logger.error(f"Error loading high scores: {e}")
    
    return highscores


def save_highscores(highscores: HighScores) -> bool:
    """Save high scores to file."""
    logger = get_logger()
    _ensure_dirs()
    
    try:
        with open(HIGHSCORES_FILE, "w", encoding="utf-8") as f:
            json.dump(highscores.to_dict(), f, indent=2)
        logger.info("High scores saved successfully")
        return True
    except Exception as e:
        logger.error(f"Error saving high scores: {e}")
        return False
