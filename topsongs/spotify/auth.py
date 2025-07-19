from __future__ import annotations

from abc import ABC, abstractmethod

from spotipy.oauth2 import SpotifyAuthBase, SpotifyPKCE

from topsongs.io.io_manager import IoManager


class Auth(ABC):
    @property
    @abstractmethod
    def manager(self) -> SpotifyAuthBase:
        pass

class PKCEAuth(Auth):
    def __init__(self, io_manager: IoManager, client_id: str = ""):
        self.pkce = SpotifyPKCE(
            client_id=client_id,
            redirect_uri=io_manager.redirect_url,
            scope=["user-top-read"]
        )
        self.io_manager = io_manager
        self.pkce._get_user_input = self.get_code

    def get_code(self, _: str) -> str:
        return self.io_manager.listen()

    @property
    def manager(self) -> SpotifyAuthBase:
        return self.pkce

