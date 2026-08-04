from __future__ import annotations

import logging
from typing import Optional

from PIL import Image, ImageDraw

from display.fonts import get_font
from services.spotify_service import NowPlaying, SpotifyService
from widgets.base import Scene

logger = logging.getLogger(__name__)


class SpotifyScene(Scene):
    duration_seconds = 8.0
    frame_interval_seconds = 0.05  # smooth marquee scroll

    def __init__(self, service: SpotifyService):
        self._service = service
        self._now_playing: Optional[NowPlaying] = None
        self._scroll_x = 0

    def refresh(self) -> None:
        self._scroll_x = 0
        try:
            self._now_playing = self._service.get_now_playing()
        except Exception:
            logger.exception("Failed to fetch Spotify now-playing")
            self._now_playing = None

    def is_available(self) -> bool:
        return self._now_playing is not None and self._now_playing.is_playing

    def render(self, image: Image.Image, draw: ImageDraw.ImageDraw) -> None:
        now_playing = self._now_playing
        if now_playing is None:
            return
        width, height = image.size

        title_font = get_font(10)
        text = f"{now_playing.title} - {now_playing.artist}"
        text_width = draw.textlength(text, font=title_font)

        x = width - self._scroll_x
        draw.text((x, 5), text, fill=(30, 215, 96), font=title_font)  # Spotify green

        self._scroll_x += 1
        if self._scroll_x > text_width + width:
            self._scroll_x = 0

        draw.text((2, height - 2), "Spotify", fill=(90, 90, 90), anchor="lb", font=get_font(8))
