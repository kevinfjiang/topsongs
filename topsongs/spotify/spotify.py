from dataclasses import dataclass
from enum import Enum
from typing import Iterator, Optional

from spotipy import Spotify
from spotipy.oauth2 import SpotifyAuthBase

from topsongs.io.io_manager import IoManager


@dataclass
class Song:
    rank: int
    name: str
    artists: list[str]

class TimeRange(str, Enum):
    LONG_TERM = "long_term"
    MEDIUM_TERM = "medium_term"
    SHORT_TERM = "short_term"

class TopSongs:
    def __init__(self, term: TimeRange, auth: SpotifyAuthBase, io_manager: IoManager):
        self.sp = Spotify(auth_manager=auth)
        self.limit = 20
        self.time_range = term
        self.io_manager = io_manager

    def __iter__(self) -> Iterator[Song]:
        offset: Optional[int] = 0
        while offset is not None:
            resp = self.sp.current_user_top_tracks(self.limit, offset, self.time_range)

            for i, e in enumerate(filter(lambda x: x, resp['items'])):
                artists = sorted(a['name']for a in e['artists'])
                yield Song(rank=offset+i+1, name=e['name'], artists=artists)

            offset = (offset + self.limit) if i + 1 == self.limit else None
            self.io_manager.info(f"Found the next {i + 1} songs, total found: {offset}")
        return