from __future__ import annotations

import logging
from pathlib import Path

from PIL import Image

from config import Config

logger = logging.getLogger(__name__)

PREVIEW_PATH = Path(__file__).resolve().parent.parent / "preview.png"


class MatrixDisplay:
    """Wraps the real RGB matrix hardware. On a machine without the
    `rgbmatrix` C bindings installed (i.e. anywhere but the Pi with the
    panel wired up), falls back to writing each frame to a PNG so the
    layout can be developed/previewed without hardware."""

    def __init__(self, config: Config):
        self.width = config.matrix_cols * config.matrix_chain_length
        self.height = config.matrix_rows * config.matrix_parallel
        self._matrix = self._init_hardware(config)
        if self._matrix is None:
            logger.warning(
                "rgbmatrix hardware library not found - running in preview mode, "
                "frames will be written to %s",
                PREVIEW_PATH,
            )

    def _init_hardware(self, config: Config):
        try:
            from rgbmatrix import RGBMatrix, RGBMatrixOptions
        except ImportError:
            return None

        options = RGBMatrixOptions()
        options.cols = config.matrix_cols
        options.rows = config.matrix_rows
        options.chain_length = config.matrix_chain_length
        options.parallel = config.matrix_parallel
        options.brightness = config.matrix_brightness
        options.hardware_mapping = config.matrix_hardware_mapping
        options.gpio_slowdown = config.matrix_gpio_slowdown
        return RGBMatrix(options=options)

    def render(self, image: Image.Image) -> None:
        rgb_image = image.convert("RGB")
        if self._matrix is not None:
            self._matrix.SetImage(rgb_image)
        else:
            rgb_image.save(PREVIEW_PATH)

    def clear(self) -> None:
        if self._matrix is not None:
            self._matrix.Clear()
