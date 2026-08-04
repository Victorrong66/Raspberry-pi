from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import spotipy
from spotipy.oauth2 import SpotifyOAuth

SCOPE = "user-read-currently-playing user-read-playback-state"


@dataclass
class NowPlaying:
    title: str
    artist: str
    is_playing: bool


class SpotifyService:
    """Reads what's currently playing on the user's Spotify account.

    Auth uses a long-lived refresh token obtained once via
    scripts/spotify_auth.py, so the Pi never needs an interactive login.
    """

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, refresh_token: str):
        self._auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=SCOPE,
            open_browser=False,
        )
        self._auth_manager.cache_handler.save_token_to_cache(
            {
                "refresh_token": refresh_token,
                "scope": SCOPE,
                "expires_at": 0,
                "access_token": "",
                "token_type": "Bearer",
            }
        )
        self._client = spotipy.Spotify(auth_manager=self._auth_manager)

    def get_now_playing(self) -> Optional[NowPlaying]:
        data = self._client.current_user_playing_track()
        if not data or not data.get("item"):
            return None
        item = data["item"]
        return NowPlaying(
            title=item["name"],
            artist=", ".join(a["name"] for a in item["artists"]),
            is_playing=data.get("is_playing", False),
        )
