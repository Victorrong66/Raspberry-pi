import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _int(name: str, default: int) -> int:
    return int(os.environ.get(name, default))


@dataclass(frozen=True)
class Config:
    matrix_cols: int
    matrix_rows: int
    matrix_chain_length: int
    matrix_parallel: int
    matrix_brightness: int
    matrix_hardware_mapping: str
    matrix_gpio_slowdown: int

    location: str
    timezone: str
    openweather_api_key: str

    spotify_client_id: str
    spotify_client_secret: str
    spotify_redirect_uri: str
    spotify_refresh_token: str


def load_config() -> Config:
    return Config(
        matrix_cols=_int("MATRIX_COLS", 64),
        matrix_rows=_int("MATRIX_ROWS", 32),
        matrix_chain_length=_int("MATRIX_CHAIN_LENGTH", 1),
        matrix_parallel=_int("MATRIX_PARALLEL", 1),
        matrix_brightness=_int("MATRIX_BRIGHTNESS", 60),
        matrix_hardware_mapping=os.environ.get("MATRIX_HARDWARE_MAPPING", "adafruit-hat"),
        matrix_gpio_slowdown=_int("MATRIX_GPIO_SLOWDOWN", 1),
        location=os.environ.get("LOCATION", "Seattle,US"),
        timezone=os.environ.get("TIMEZONE", "America/Los_Angeles"),
        openweather_api_key=os.environ.get("OPENWEATHER_API_KEY", ""),
        spotify_client_id=os.environ.get("SPOTIFY_CLIENT_ID", ""),
        spotify_client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET", ""),
        spotify_redirect_uri=os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8080/callback"),
        spotify_refresh_token=os.environ.get("SPOTIFY_REFRESH_TOKEN", ""),
    )
