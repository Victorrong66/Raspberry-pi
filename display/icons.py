from __future__ import annotations

from PIL import ImageDraw

SUN = (255, 200, 40)
CLOUD = (170, 180, 190)
RAIN = (90, 140, 255)
SNOW = (230, 240, 255)
BOLT = (255, 210, 60)


def draw_weather_icon(draw: ImageDraw.ImageDraw, condition: str, cx: int, cy: int, r: int = 7) -> None:
    """Draws a small icon centered at (cx, cy) for an OpenWeatherMap 'main'
    condition string (Clear, Clouds, Rain, Drizzle, Thunderstorm, Snow,
    Mist/Fog/Haze/...)."""
    condition = condition.lower()

    if condition == "clear":
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=SUN)
        return

    if condition in ("mist", "fog", "haze", "smoke"):
        for dy in (-3, 1, 5):
            draw.line((cx - r, cy + dy, cx + r, cy + dy), fill=CLOUD)
        return

    if condition == "thunderstorm":
        _draw_cloud(draw, cx, cy - 2, r)
        draw.polygon(
            [(cx, cy + 2), (cx - 3, cy + 7), (cx + 1, cy + 7), (cx - 2, cy + 12)],
            fill=BOLT,
        )
        return

    if condition == "snow":
        _draw_cloud(draw, cx, cy - 2, r)
        for dx in (-4, 0, 4):
            draw.point((cx + dx, cy + 8), fill=SNOW)
        return

    if condition in ("rain", "drizzle"):
        _draw_cloud(draw, cx, cy - 2, r)
        for dx in (-4, 0, 4):
            draw.line((cx + dx, cy + 6, cx + dx - 1, cy + 10), fill=RAIN)
        return

    # Clouds / default
    _draw_cloud(draw, cx, cy, r)


def _draw_cloud(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int) -> None:
    draw.ellipse((cx - r, cy - 2, cx - r + 8, cy + 6), fill=CLOUD)
    draw.ellipse((cx - 2, cy - r + 2, cx + 8, cy + 6), fill=CLOUD)
    draw.ellipse((cx + 3, cy - 1, cx + r + 3, cy + 6), fill=CLOUD)
