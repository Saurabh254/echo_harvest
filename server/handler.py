from typing import Type

import gi

from server.helpers.dependency_injector import inject_redis
from server.internals.schemas import MetaData
import redis.asyncio as aioredis
from server.internals.redis_handler import GiEventHandler
from server.helpers import interface
from server.internals.database import get_db
from sqlalchemy.orm import Session
import logging
import config

gi.require_version("Playerctl", "2.0")
from gi.repository import Playerctl

player_glb = Playerctl.Player()

@inject_redis
def on_play(player: Type[Playerctl.Player], status, redis_conn: aioredis.Redis):
    db: Session = next(get_db())
    player_handler = GiEventHandler(redis_conn)
    metadata = MetaData(
        title=player.get_title(),
        artist=player.get_artist(),
        album=player.get_album(),
        duration=player.get_position(),
    )
    logging.info("PlayerCtl::Play : Playing - {}".format(metadata))
    last_music = player_handler.get_last_player_metadata()
    if last_music and (last_music["title"] != metadata.title):
        interface.insert_metadata_into_db(metadata=MetaData(**last_music), db=db)

    if last_music is None or last_music["title"] != metadata.title:
        redis.store_track_metadata(metadata)


def get_current_track():
    db: Session = next(get_db())
    metadata = MetaData(
        title=player.get_title(),
        artist=player.get_artist(),
        album=player.get_album(),
        duration=player.get_position(),
    )
    return interface.get_current_track_from_redis(metadata, redis=redis, db=db)


def get_tracks():
    db: Session = next(get_db())
    return interface.get_tracks_from_db(db=db)
