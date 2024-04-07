from typing import List
from gi.repository import GLib
from echo_harvest import handler
from echo_harvest.internals.database import create_table
from echo_harvest.helpers.logger import logging as logger
import sys
from threading import Thread
from echo_harvest.bridge import socket_base


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
        logger.info("Started PlayerCTL app")
        self._mainloop.run()

    def init_tables(self):
        create_table()


import asyncio


def threaded_app_with_socket():
    app = App(sys.argv)
    task1 = Thread(target=app.run)
    task2 = Thread(target=lambda: asyncio.run(socket_base.main()))
    task1.start()
    task2.start()
    task1.join()
    task2.join()


if __name__ == "__main__":
    try:
        threaded_app_with_socket()
    except KeyboardInterrupt:

        ...
