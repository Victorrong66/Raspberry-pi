from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw

from display.fonts import get_font
from widgets.base import Scene


class ClockScene(Scene):
    duration_seconds = 6.0
    frame_interval_seconds = 1.0

    def __init__(self, timezone: str):
        self._tz = ZoneInfo(timezone)

    def render(self, image: Image.Image, draw: ImageDraw.ImageDraw) -> None:
        now = datetime.now(self._tz)
        width, height = image.size

        time_text = now.strftime("%-I:%M")
        date_text = now.strftime("%a %b %-d")

        draw.text(
            (width // 2, height // 2 - 6),
            time_text,
            fill=(255, 255, 255),
            anchor="mm",
            font=get_font(16),
        )
        draw.text(
            (width // 2, height // 2 + 10),
            date_text,
            fill=(120, 180, 255),
            anchor="mm",
            font=get_font(9),
        )
