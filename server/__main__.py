import json
import logging
import logging.config
from typing import List
from gi.repository import GLib
from server import handler
from server.internals.database import create_table
import os

config_path = os.path.abspath('server/logging.config.json')

print(config_path)
with open(config_path, 'r') as f:
    config = json.load(f)
logging.basicConfig(level=logging.DEBUG)
logging.config.dictConfig(config)
log = logging.getLogger(__name__)

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
        logging.info("Started PlayerCTL app")
        self._mainloop.run()

    def init_tables(self):
        create_table()


App().run()
