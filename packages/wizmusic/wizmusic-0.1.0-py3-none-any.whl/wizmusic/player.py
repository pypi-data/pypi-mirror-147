import os
import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth


if missing_envs := {
    "SPOTIPY_CLIENT_ID",
    "SPOTIPY_CLIENT_SECRET",
    "SPOTIPY_REDIRECT_URI",
} - set(os.environ.keys()):
    print(f"Missing envs: {missing_envs}", file=sys.stderr)
    sys.exit(1)

SCOPE = ["user-read-currently-playing"]

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
