"""Serpents Per Second - SNES-styled Snake game.

Entry point for the application.
"""

import sys

from src.app import App


def main() -> int:
    """Main entry point."""
    app = App()
    if not app.init():
        return 1
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
