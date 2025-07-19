import itertools
from typing import Annotated, Optional

import typer
from dotenv import dotenv_values
from rich import print

from topsongs.io.io_manager import CliManager
from topsongs.spotify.auth import PKCEAuth
from topsongs.spotify.spotify import TimeRange, TopSongs

app = typer.Typer()
cli = CliManager()

@app.command()
def top_songs(
    client_id: Annotated[Optional[str],
                         typer.Option(help="Client ID of the Spotify project, if not provided, will use env variable CLIENT_ID")] = None,
    term: TimeRange = TimeRange.MEDIUM_TERM,
    num_songs: int = 50
):
    """Gets top songs from Spotify."""
    if client_id is None:
        client_id = dotenv_values().get("CLIENT_ID")
    pkce = PKCEAuth(cli, client_id)

    for s in itertools.islice(TopSongs(term, pkce, cli), num_songs):
        print(f"{s.rank}. {s.name} - by {', '.join(s.artists)}")

if __name__ == "__main__":
    app()
