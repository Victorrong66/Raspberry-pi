from __future__ import annotations

import itertools
import logging
import signal
import time

from PIL import Image, ImageDraw

from config import load_config
from display.matrix import MatrixDisplay
from services.spotify_service import SpotifyService
from services.weather_service import WeatherService
from widgets.base import Scene
from widgets.clock import ClockScene
from widgets.spotify import SpotifyScene
from widgets.weather import WeatherScene

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("dashboard")

_running = True


def _handle_shutdown(signum, frame):
    global _running
    _running = False


def build_scenes(config) -> list[Scene]:
    scenes: list[Scene] = [ClockScene(config.timezone)]

    if config.openweather_api_key:
        scenes.append(WeatherScene(WeatherService(config.openweather_api_key, config.location)))
    else:
        logger.warning("OPENWEATHER_API_KEY not set - skipping weather scene")

    if config.spotify_client_id and config.spotify_refresh_token:
        scenes.append(
            SpotifyScene(
                SpotifyService(
                    client_id=config.spotify_client_id,
                    client_secret=config.spotify_client_secret,
                    redirect_uri=config.spotify_redirect_uri,
                    refresh_token=config.spotify_refresh_token,
                )
            )
        )
    else:
        logger.warning("Spotify credentials not set - skipping Spotify scene (run scripts/spotify_auth.py)")

    return scenes


def run(config, display: MatrixDisplay, scenes: list[Scene]) -> None:
    for scene in itertools.cycle(scenes):
        if not _running:
            return

        scene.refresh()
        if not scene.is_available():
            continue

        deadline = time.monotonic() + scene.duration_seconds
        while _running and time.monotonic() < deadline:
            image = Image.new("RGB", (display.width, display.height), (0, 0, 0))
            draw = ImageDraw.Draw(image)
            scene.render(image, draw)
            display.render(image)
            time.sleep(scene.frame_interval_seconds)


def main() -> None:
    signal.signal(signal.SIGINT, _handle_shutdown)
    signal.signal(signal.SIGTERM, _handle_shutdown)

    config = load_config()
    display = MatrixDisplay(config)
    scenes = build_scenes(config)

    logger.info("Starting dashboard with scenes: %s", [type(s).__name__ for s in scenes])
    try:
        run(config, display, scenes)
    finally:
        display.clear()


if __name__ == "__main__":
    main()
