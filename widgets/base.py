from __future__ import annotations

from PIL import Image, ImageDraw


class Scene:
    """One full-screen 'page' the dashboard can show, e.g. clock, weather,
    or now-playing. Scenes rotate in the order given to the main loop."""

    #: how long this scene stays on screen before rotating to the next one
    duration_seconds: float = 8.0
    #: how often render() is called while this scene is active
    frame_interval_seconds: float = 1.0

    def refresh(self) -> None:
        """Called once whenever this scene becomes active. Do network calls
        (weather/Spotify) here rather than in render(), which runs every frame."""

    def is_available(self) -> bool:
        """Return False to have the rotation skip this scene entirely,
        e.g. Spotify when nothing is playing."""
        return True

    def render(self, image: Image.Image, draw: ImageDraw.ImageDraw) -> None:
        raise NotImplementedError
