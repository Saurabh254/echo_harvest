import gi

from app.internals.schemas import MetaData
import redis
from app.internals.redis_handler import RedisHandler
from app.helpers import interface
from app.internals.database import get_db
from sqlalchemy.orm import Session
from app.helpers.logger import logging as logger

gi.require_version("Playerctl", "2.0")

from gi.repository import Playerctl  # noqa: E402

_redis = redis.Redis()
redis = RedisHandler(redis=_redis)
player = Playerctl.Player()


def on_play(player, status):
    db = next(get_db())
    metadata = MetaData(
        title=player.get_title(),
        artist=player.get_artist(),
        album=player.get_album(),
        duration=player.get_position(),
    )
    last_music = redis.get_last_player_metadata()
    if last_music and (last_music["title"] != metadata.title):

        interface.insert_metadata_into_db(metadata=MetaData(**last_music), db=db)

    if last_music is None or last_music["title"] != metadata.title:
        redis.store_track_metadata(metadata)


def get_tracks(player, db: Session = next(get_db())):
    return interface.get_tracks_from_db(db=db)
