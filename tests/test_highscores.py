"""Tests for high score persistence."""

import json
import pytest
from pathlib import Path
from datetime import datetime, timezone

from src.constants import GameMode, MAX_HIGHSCORES
from src.systems.saves import (
    Settings,
    HighScores,
    HighScoreEntry,
    load_settings,
    save_settings,
    load_highscores,
    save_highscores,
    _validate_name,
)


class TestSettingsValidation:
    """Test settings validation and clamping."""

    def test_scale_clamping(self) -> None:
        """Test scale is clamped to valid range.

        Verifies that scale values below minimum are clamped to 3
        and values above maximum are clamped to 6.
        """
        settings = Settings()
        
        settings.from_dict({"scale": 1})
        assert settings.scale == 3
        
        settings.from_dict({"scale": 10})
        assert settings.scale == 6

    def test_volume_clamping(self) -> None:
        """Test volumes are clamped to 0-1.

        Verifies that negative volume values are clamped to 0.0
        and values above 1.0 are clamped to 1.0.
        """
        settings = Settings()
        
        settings.from_dict({"music_volume": -0.5})
        assert settings.music_volume == 0.0
        
        settings.from_dict({"sfx_volume": 1.5})
        assert settings.sfx_volume == 1.0

    def test_defaults_on_invalid(self) -> None:
        """Test defaults are used for invalid data types.

        Verifies that the settings object does not crash when
        provided with invalid data types (e.g., string instead of int).
        """
        settings = Settings()
        original_scale = settings.scale
        
        settings.from_dict({"scale": "invalid"})
        # Should not crash, may retain original or use default


class TestNameValidation:
    """Test high score name validation."""

    def test_valid_names(self) -> None:
        """Test valid names pass through.

        Verifies that valid 3-character alphanumeric names
        are returned unchanged.
        """
        assert _validate_name("AAA") == "AAA"
        assert _validate_name("ABC") == "ABC"
        assert _validate_name("123") == "123"
        assert _validate_name("A1B") == "A1B"

    def test_lowercase_converted(self) -> None:
        """Test lowercase is converted to uppercase.

        Verifies that lowercase letters in names are automatically
        converted to uppercase.
        """
        assert _validate_name("abc") == "ABC"
        assert _validate_name("aBc") == "ABC"

    def test_invalid_chars_replaced(self) -> None:
        """Test invalid characters are replaced with A.

        Verifies that non-alphanumeric characters in names are
        replaced with the letter 'A'.
        """
        assert _validate_name("A!B") == "AAB"
        assert _validate_name("@#$") == "AAA"

    def test_wrong_length_handled(self) -> None:
        """Test wrong length names are handled.

        Verifies that names with incorrect length (not exactly 3 characters)
        are reset to the default 'AAA'.
        """
        assert _validate_name("AB") == "AAA"
        assert _validate_name("ABCD") == "AAA"  # Too long gets reset
        assert _validate_name("") == "AAA"


class TestHighScoreSorting:
    """Test high score sorting and truncation."""

    def test_sorted_by_score_descending(self) -> None:
        """Test scores are sorted highest first.

        Verifies that high scores are automatically sorted in
        descending order when retrieved.
        """
        hs = HighScores()
        hs.add_score(GameMode.CLASSIC, "AAA", 100)
        hs.add_score(GameMode.CLASSIC, "BBB", 200)
        hs.add_score(GameMode.CLASSIC, "CCC", 50)
        
        scores = hs.get_scores(GameMode.CLASSIC)
        assert len(scores) == 3
        assert scores[0].score == 200
        assert scores[1].score == 100
        assert scores[2].score == 50

    def test_truncated_to_10(self) -> None:
        """Test only top 10 scores are kept.

        Verifies that when more than MAX_HIGHSCORES entries are added,
        only the top scores are retained.
        """
        hs = HighScores()
        
        for i in range(15):
            hs.add_score(GameMode.CLASSIC, f"A{i:02d}"[:3], i * 10)
        
        scores = hs.get_scores(GameMode.CLASSIC)
        assert len(scores) == MAX_HIGHSCORES
        assert scores[0].score == 140  # Highest
        assert scores[-1].score == 50  # 10th highest

    def test_qualifies_with_room(self) -> None:
        """Test qualification when less than 10 scores.

        Verifies that any score qualifies for the leaderboard when
        there are fewer than MAX_HIGHSCORES entries.
        """
        hs = HighScores()
        hs.add_score(GameMode.CLASSIC, "AAA", 100)
        
        assert hs.qualifies(GameMode.CLASSIC, 0) is True  # Even 0 qualifies

    def test_qualifies_by_score(self) -> None:
        """Test qualification when full leaderboard.

        Verifies that a score must be higher than the lowest score
        on a full leaderboard to qualify.
        """
        hs = HighScores()
        
        for i in range(10):
            hs.add_score(GameMode.CLASSIC, "AAA", (i + 1) * 10)
        
        # Lowest is 10, need to beat it
        assert hs.qualifies(GameMode.CLASSIC, 5) is False
        assert hs.qualifies(GameMode.CLASSIC, 10) is False
        assert hs.qualifies(GameMode.CLASSIC, 11) is True


class TestHighScorePersistence:
    """Test high score file persistence."""

    def test_save_and_load(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test saving and loading high scores.

        Verifies that high scores can be persisted to a file and
        loaded back with the same data intact.

        Args:
            tmp_path: Pytest fixture providing a temporary directory.
            monkeypatch: Pytest fixture for patching module attributes.
        """
        # Redirect save path to temp
        import src.systems.saves as saves_module
        monkeypatch.setattr(saves_module, "SAVES_DIR", tmp_path)
        monkeypatch.setattr(saves_module, "HIGHSCORES_FILE", tmp_path / "highscores.json")
        
        # Create and save
        hs = HighScores()
        hs.add_score(GameMode.CLASSIC, "ABC", 123)
        save_highscores(hs)
        
        # Load and verify
        loaded = load_highscores()
        scores = loaded.get_scores(GameMode.CLASSIC)
        assert len(scores) == 1
        assert scores[0].name == "ABC"
        assert scores[0].score == 123
