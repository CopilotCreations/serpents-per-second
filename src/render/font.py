"""Bitmap font rendering."""

from pathlib import Path
import pygame

from src.systems.logging_setup import get_logger


class BitmapFont:
    """Renders text using a bitmap font sprite sheet."""

    GLYPH_SIZE = 8
    RENDER_SCALE = 2  # Scale glyphs to 16x16
    
    # Character mapping: row, column in sprite sheet
    CHAR_MAP: dict[str, tuple[int, int]] = {}
    
    @classmethod
    def _init_char_map(cls) -> None:
        """Initialize character mapping."""
        if cls.CHAR_MAP:
            return
        
        # Row 0: A-P
        for i, char in enumerate("ABCDEFGHIJKLMNOP"):
            cls.CHAR_MAP[char] = (0, i)
        
        # Row 1: Q-Z, 0-5
        for i, char in enumerate("QRSTUVWXYZ012345"):
            cls.CHAR_MAP[char] = (1, i)
        
        # Row 2: 6-9, :, -, space
        for i, char in enumerate("6789:- "):
            cls.CHAR_MAP[char] = (2, i)

    def __init__(self, assets_path: Path) -> None:
        self.assets_path = assets_path
        self.sheet: pygame.Surface | None = None
        self.glyphs: dict[str, pygame.Surface] = {}
        self._init_char_map()

    def load(self) -> bool:
        """Load the font sprite sheet."""
        logger = get_logger()
        font_path = self.assets_path / "sprites" / "font.png"
        
        try:
            self.sheet = pygame.image.load(font_path).convert_alpha()
            self._extract_glyphs()
            logger.info("Font loaded successfully")
            return True
        except pygame.error as e:
            logger.error(f"Failed to load font: {e}")
            return False

    def _extract_glyphs(self) -> None:
        """Extract and scale glyphs from the sheet."""
        if self.sheet is None:
            return
        
        for char, (row, col) in self.CHAR_MAP.items():
            x = col * self.GLYPH_SIZE
            y = row * self.GLYPH_SIZE
            rect = pygame.Rect(x, y, self.GLYPH_SIZE, self.GLYPH_SIZE)
            glyph = self.sheet.subsurface(rect).copy()
            
            # Scale to render size
            scaled = pygame.transform.scale(
                glyph,
                (self.GLYPH_SIZE * self.RENDER_SCALE, self.GLYPH_SIZE * self.RENDER_SCALE)
            )
            self.glyphs[char] = scaled

    def render_text(
        self,
        text: str,
        surface: pygame.Surface,
        x: int,
        y: int,
        color: tuple[int, int, int] | None = None,
    ) -> int:
        """
        Render text to a surface.
        Returns the width of rendered text.
        """
        text = text.upper()
        render_x = x
        glyph_width = self.GLYPH_SIZE * self.RENDER_SCALE
        
        for char in text:
            glyph = self.glyphs.get(char)
            if glyph:
                if color:
                    # Tint the glyph
                    tinted = glyph.copy()
                    tinted.fill(color + (0,), special_flags=pygame.BLEND_RGB_MULT)
                    surface.blit(tinted, (render_x, y))
                else:
                    surface.blit(glyph, (render_x, y))
            render_x += glyph_width
        
        return render_x - x

    def get_text_width(self, text: str) -> int:
        """Get the width of text in pixels."""
        return len(text) * self.GLYPH_SIZE * self.RENDER_SCALE

    def render_centered(
        self,
        text: str,
        surface: pygame.Surface,
        y: int,
        color: tuple[int, int, int] | None = None,
    ) -> None:
        """Render text centered horizontally on the surface."""
        width = self.get_text_width(text)
        x = (surface.get_width() - width) // 2
        self.render_text(text, surface, x, y, color)
