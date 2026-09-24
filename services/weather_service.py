from __future__ import annotations

from dataclasses import dataclass
from time import monotonic

import requests

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


@dataclass
class WeatherReading:
    temp_f: float
    condition: str  # OpenWeatherMap "main" field, e.g. "Clear", "Rain"
    description: str


def _is_lat_lon(location: str) -> bool:
    parts = location.split(",")
    if len(parts) != 2:
        return False
    return all(part.strip().lstrip("-").replace(".", "", 1).isdigit() for part in parts)


class WeatherService:
    """Fetches current weather, caching the result for `cache_seconds` so
    the scene rotation doesn't hammer the API on every render."""

    def __init__(self, api_key: str, location: str, cache_seconds: float = 600.0):
        self._api_key = api_key
        self._location = location
        self._cache_seconds = cache_seconds
        self._cached: WeatherReading | None = None
        self._cached_at: float = 0.0

    def get_current(self) -> WeatherReading:
        now = monotonic()
        if self._cached is not None and (now - self._cached_at) < self._cache_seconds:
            return self._cached

        params = {"appid": self._api_key, "units": "imperial"}
        if _is_lat_lon(self._location):
            lat, lon = self._location.split(",")
            params["lat"] = lat.strip()
            params["lon"] = lon.strip()
        else:
            params["q"] = self._location

        response = requests.get(OPENWEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        reading = WeatherReading(
            temp_f=data["main"]["temp"],
            condition=data["weather"][0]["main"],
            description=data["weather"][0]["description"],
        )
        self._cached = reading
        self._cached_at = now
        return reading
