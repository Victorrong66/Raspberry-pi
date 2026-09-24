"""One-time interactive helper to get a Spotify refresh token.

Run this once (on the Pi or on your laptop, doesn't matter - it's not the
matrix hardware that needs this) after setting SPOTIFY_CLIENT_ID and
SPOTIFY_CLIENT_SECRET in .env. It prints a SPOTIFY_REFRESH_TOKEN value to
paste into .env, after which the dashboard never needs interactive login.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from spotipy.oauth2 import SpotifyOAuth  # noqa: E402

from config import load_config  # noqa: E402

SCOPE = "user-read-currently-playing user-read-playback-state"


def main() -> None:
    config = load_config()
    if not config.spotify_client_id or not config.spotify_client_secret:
        raise SystemExit("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env first.")

    auth_manager = SpotifyOAuth(
        client_id=config.spotify_client_id,
        client_secret=config.spotify_client_secret,
        redirect_uri=config.spotify_redirect_uri,
        scope=SCOPE,
        open_browser=False,
    )

    print("1. Open this URL on any device (your phone is fine) and log in:\n")
    print(f"   {auth_manager.get_authorize_url()}\n")
    print("2. After approving, you'll be redirected to a URL starting with")
    print(f"   {config.spotify_redirect_uri} - the page will look like it failed to")
    print("   load. That's expected - just copy the full URL from the address bar.\n")

    redirected_url = input("3. Paste that full redirect URL here: ").strip()
    code = auth_manager.parse_response_code(redirected_url)
    token_info = auth_manager.get_access_token(code, as_dict=True)

    print("\nSuccess! Add this line to your .env file:\n")
    print(f"SPOTIFY_REFRESH_TOKEN={token_info['refresh_token']}")


if __name__ == "__main__":
    main()
