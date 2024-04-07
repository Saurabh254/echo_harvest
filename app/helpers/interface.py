from sqlalchemy.orm import Session
from app.internals.models import TrackMetaData
from app.internals.schemas import MetaData
from datetime import datetime, timedelta
from app.helpers.logger import logging as logger
from nanoid import generate


def insert_metadata_into_db(metadata: MetaData, db: Session) -> MetaData:
    metadata = TrackMetaData(**metadata.__dict__)
    db.add(metadata)
    db.commit()
    db.refresh(metadata)
    logger.info(f"DATABASE::INSERT:{metadata}")
    return metadata


def get_tracks_from_db(
    db: Session,
    date: datetime = datetime.now() - timedelta(days=1),
) -> list[MetaData]:
    return db.query(TrackMetaData).filter(TrackMetaData.at > date).all()
