from __future__ import annotations

import logging

from PIL import Image, ImageDraw

from display.fonts import get_font
from display.icons import draw_weather_icon
from services.weather_service import WeatherReading, WeatherService
from widgets.base import Scene

logger = logging.getLogger(__name__)


class WeatherScene(Scene):
    duration_seconds = 6.0
    frame_interval_seconds = 5.0  # weather barely changes; no need to redraw fast

    def __init__(self, service: WeatherService):
        self._service = service
        self._reading: WeatherReading | None = None

    def refresh(self) -> None:
        try:
            self._reading = self._service.get_current()
        except Exception:
            logger.exception("Failed to fetch weather")

    def is_available(self) -> bool:
        return self._reading is not None

    def render(self, image: Image.Image, draw: ImageDraw.ImageDraw) -> None:
        reading = self._reading
        if reading is None:
            return
        width, height = image.size

        draw_weather_icon(draw, reading.condition, cx=14, cy=height // 2, r=7)

        draw.text(
            (32, height // 2),
            f"{round(reading.temp_f)}°",
            fill=(255, 255, 255),
            anchor="lm",
            font=get_font(16),
        )
        draw.text(
            (2, height - 2),
            reading.description.title(),
            fill=(150, 160, 170),
            anchor="lb",
            font=get_font(8),
        )
