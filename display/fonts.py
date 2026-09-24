from __future__ import annotations

from functools import lru_cache

from PIL import ImageFont


@lru_cache(maxsize=None)
def get_font(size: int) -> ImageFont.FreeTypeFont:
    """Pillow's bundled scalable font at a given pixel size. Swap this out
    for a proper pixel-art .ttf (e.g. Press Start 2P) if you want a crisper
    look on the matrix - just point load_default's callers at ImageFont.truetype(...)."""
    return ImageFont.load_default(size=size)
