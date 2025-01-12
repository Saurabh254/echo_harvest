from sqlalchemy.orm import Session

from server.helpers.dependency_injector import inject_redis
from server.internals.models import TrackMetaData
from server.internals.redis_handler import GiEventHandler
from server.internals.schemas import MetaData, MetaDataResp
from datetime import datetime, timedelta
import redis.asyncio as aioredis
import logging


def insert_metadata_into_db(metadata: MetaData, db: Session) -> MetaData:
    metadata = TrackMetaData(**metadata.__dict__)
    try:
        logging.debug(f"DATABASE::INSERT:{metadata}")
        db.add(metadata)
        db.commit()
        db.refresh(metadata)
    except Exception as e:
        logging.critical("DATABASE::INSERT:ERROR : Unable to insert ({})".format(e))
    return metadata


def get_tracks_from_db(
    db: Session,
    date: datetime,
) -> list[MetaDataResp]:
    logger.debug("DATABASE::GET : Queried data from db")
    return db.query(TrackMetaData).filter(TrackMetaData.at > date).all()


def get_stored_tracks_metadata(
    db: Session,
    date: datetime = datetime.now() - timedelta(days=1),
) -> dict:
    metadata = {}
    metadata["play_count"] = db.query(TrackMetaData).count()
    metadata["tracks"] = [
        {
            "title": _.title,
            "album": _.album,
            "artist": _.artist,
            "at": _.at,
            "duration": _.duration,
        }
        for _ in get_tracks_from_db(db=db, date=date)
    ]
    # metadata["current_playing"] = handler.get_current_track()
    return metadata

@inject_redis
async def get_current_track_from_redis(metadata: MetaData, player_event: GiEventHandler) -> dict:
    resp = await player_event.get_last_player_metadata()
    if resp:
        return resp
    await player_event.store_track_metadata(metadata=metadata)
    return metadata.__dict__
