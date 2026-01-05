"""Tests for scene transitions."""

import pytest


class TestSceneTransitions:
    """Test scene navigation and transitions."""

    def test_main_menu_items_order(self) -> None:
        """Test main menu items are in correct order.

        Verifies that the MainMenuScene displays menu items in the expected
        order: PLAY, OPTIONS, HIGH SCORES, QUIT.

        Raises:
            AssertionError: If menu items don't match the expected order.
        """
        from src.scenes.main_menu import MainMenuScene
        
        expected = ["PLAY", "OPTIONS", "HIGH SCORES", "QUIT"]
        assert MainMenuScene.MENU_ITEMS == expected

    def test_mode_select_items_order(self) -> None:
        """Test mode select items are in correct order.

        Verifies that the ModeSelectScene displays game mode options in the
        expected order: CLASSIC, BOXED, MAZE, TIME ATTACK, and BACK.

        Raises:
            AssertionError: If mode select items don't match the expected order
                or associated GameMode values.
        """
        from src.scenes.mode_select import ModeSelectScene
        from src.constants import GameMode
        
        items = ModeSelectScene.MENU_ITEMS
        assert len(items) == 5
        assert items[0] == ("CLASSIC", GameMode.CLASSIC)
        assert items[1] == ("BOXED", GameMode.BOXED)
        assert items[2] == ("MAZE", GameMode.MAZE)
        assert items[3] == ("TIME ATTACK", GameMode.TIME_ATTACK)
        assert items[4] == ("BACK", None)

    def test_options_items(self) -> None:
        """Test options menu items.

        Verifies that the OptionsScene displays settings options in the
        expected order: SCALE, FULLSCREEN, MUSIC VOLUME, SFX VOLUME, BACK.

        Raises:
            AssertionError: If options menu items don't match the expected order.
        """
        from src.scenes.options import OptionsScene
        
        expected = ["SCALE", "FULLSCREEN", "MUSIC VOLUME", "SFX VOLUME", "BACK"]
        assert OptionsScene.MENU_ITEMS == expected

    def test_highscores_modes(self) -> None:
        """Test high scores displays all modes.

        Verifies that the HighScoresScene supports displaying scores for all
        four game modes: CLASSIC, BOXED, MAZE, and TIME_ATTACK.

        Raises:
            AssertionError: If not all game modes are present in the high
                scores scene's supported modes.
        """
        from src.scenes.highscores import HighScoresScene
        from src.constants import GameMode
        
        modes = HighScoresScene.MODES
        assert len(modes) == 4
        assert GameMode.CLASSIC in modes
        assert GameMode.BOXED in modes
        assert GameMode.MAZE in modes
        assert GameMode.TIME_ATTACK in modes
