from sqlalchemy.orm import Session
from echo_harvest.internals.models import TrackMetaData
from echo_harvest.internals.schemas import MetaData, MetaDataResp
from datetime import datetime, timedelta
from echo_harvest.helpers.logger import logging as logger
from echo_harvest.internals.redis_handler import RedisHandler


def insert_metadata_into_db(metadata: MetaData, db: Session) -> MetaData:
    metadata = TrackMetaData(**metadata.__dict__)
    try:
        logger.debug(f"DATABASE::INSERT:{metadata}")
        db.add(metadata)
        db.commit()
        db.refresh(metadata)
    except Exception as e:
        logger.critical("DATABASE::INSERT:ERROR : Unable to insert ({})".format(e))
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


def get_current_track_from_redis(metadata, redis: RedisHandler, db: Session) -> dict:

    resp = redis.get_last_player_metadata()
    if resp:
        return resp
    redis.store_track_metadata(metadata=metadata)
    return metadata.__dict__
