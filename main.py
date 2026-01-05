"""Serpents Per Second - SNES-styled Snake game.

Entry point for the application.
"""

import sys

from src.app import App


def main() -> int:
    """Main entry point for the Serpents Per Second game.

    Initializes the application and runs the main game loop.

    Returns:
        int: Exit code (0 for success, 1 for initialization failure).
    """
    app = App()
    if not app.init():
        return 1
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
