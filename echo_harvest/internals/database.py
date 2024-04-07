from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from echo_harvest.helpers.logger import logging as logger
from sqlalchemy import create_engine
from echo_harvest.internals.models import BaseModel
import config

engine = create_engine(config.DATABASE_URL, echo=False)
meta = MetaData()


def get_db():
    while True:
        db = Session(engine)
        try:
            yield db
        except Exception as e:
            logger.warn(f"DATABASE::Session:{0}".format(e))
        finally:
            db.close()


def create_table():
    BaseModel.metadata.create_all(engine)
    logger.warn("DATABASE::CREATE_TABLE:tracks_metadata")
