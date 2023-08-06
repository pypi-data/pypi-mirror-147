import os
import sys
from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyOAuth


if missing_envs := {
    "SPOTIPY_CLIENT_ID",
    "SPOTIPY_CLIENT_SECRET",
    "SPOTIPY_REDIRECT_URI",
} - set(os.environ.keys()):
    print(f"Missing envs: {missing_envs}", file=sys.stderr)
    sys.exit(1)

oauth2 = SpotifyOAuth(
    scope=["user-read-currently-playing"],
    cache_path=Path.home() / ".cache" / "wizmusic",
)

spotify = spotipy.Spotify(auth_manager=oauth2)
