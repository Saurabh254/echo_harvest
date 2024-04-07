from typing import List
from gi.repository import GLib
from app import handler
from app.internals.database import create_table
from app.helpers.logger import logging as logger
import sys


class App:
    def __init__(
        self, *argv, players: List[str] = None, redis_url: str = "redis://localhost/23"
    ) -> None:
        if "--create-table" in argv:
            create_table()
        self._mainloop = GLib.MainLoop()
        self.handler = handler
        self.handler.player.connect("playback-status::playing", self.handler.on_play)

    def run(self):
        logger.info("Stated PlayerCTL app")
        self._mainloop.run()

    def init_tables(self):
        create_table()


if __name__ == "__main__":
    app = App(sys.argv)
    try:
        app.run()
    except KeyboardInterrupt:

        exit()
