import os
import argparse
import urllib.request
from dataclasses import dataclass
from time import sleep

from rich.progress import Progress
import colorgram

from .wiz import Wiz
from .player import spotify
from .utils import default_progress_columns


@dataclass
class Track:
    data: dict
    color: colorgram.Color = None

    def __eq__(self, other) -> bool:
        return isinstance(other, Track) and other.data and self.data["item"]["id"] == other.data["item"]["id"]


class Client:
    def __init__(self, wiz_host=None, wiz_port=None, tick_secs=None):
        self.wiz = Wiz(wiz_host, wiz_port)
        self.tick_secs = tick_secs
        self.current_track: Track = None

    def get_prominent_color(self, url):
        with urllib.request.urlopen(url) as f:
            colors = colorgram.extract(f, 1)
            return colors[0]

    def update(self):
        self.current_track = track = Track(data=spotify.current_user_playing_track())

        # no song playing
        if not track.data:
            return

        # change light color
        track.color = self.get_prominent_color(track.data["item"]["album"]["images"][-1]["url"])
        self.wiz.set_color(track.color.rgb)

        # track progress bar
        with Progress(*default_progress_columns(track.color.rgb), expand=True) as progress:
            task = progress.add_task(track.data["item"]["name"], total=track.data["item"]["duration_ms"])

            while True:
                if self.current_track != track:
                    break
                progress.update(task, completed=track.data["progress_ms"])
                sleep(self.tick_secs)
                track = Track(data=spotify.current_user_playing_track())

    def run(self):
        with self.wiz:
            while True:
                try:
                    self.update()
                    sleep(self.tick_secs)
                except KeyboardInterrupt:
                    break

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--wiz-host", default="192.168.0.176")
    parser.add_argument("-p", "--wiz-port", type=int, default=38899)
    parser.add_argument("-t", "--tick-secs", type=int, default=5)
    args = parser.parse_args()
    client = Client(args.wiz_host, args.wiz_port, args.tick_secs)
    client.run()


if __name__ == "__main__":
    cli()
