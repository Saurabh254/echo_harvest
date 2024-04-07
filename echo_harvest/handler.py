import gi

from echo_harvest.internals.schemas import MetaData
import redis
from echo_harvest.internals.redis_handler import RedisHandler
from echo_harvest.helpers import interface
from echo_harvest.internals.database import get_db
from sqlalchemy.orm import Session
from echo_harvest.helpers.logger import logging as logger
import config

gi.require_version("Playerctl", "2.0")

from gi.repository import Playerctl  # noqa: E402

_redis = redis.Redis(host=config.REDIS_HOSTNAME)
redis = RedisHandler(redis=_redis)
player = Playerctl.Player()


def on_play(player, status):

    db: Session = next(get_db())
    metadata = MetaData(
        title=player.get_title(),
        artist=player.get_artist(),
        album=player.get_album(),
        duration=player.get_position(),
    )
    logger.info("PlayerCtl::Play : Playing - {}".format(metadata))
    last_music = redis.get_last_player_metadata()
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
