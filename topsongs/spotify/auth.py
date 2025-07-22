from __future__ import annotations

from spotipy.oauth2 import SpotifyPKCE

from topsongs.io.io_manager import IoManager


class PKCEAuth(SpotifyPKCE):
    def __init__(self, io_manager: IoManager, client_id: str = ""):
        super().__init__(
            client_id=client_id,
            redirect_uri=io_manager.redirect_url,
            scope=["user-top-read"]
        )
        self.io_manager = io_manager

    @staticmethod
    def _get_user_input(self, _: str) -> str:
        return self.io_manager.listen()

