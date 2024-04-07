from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from app.helpers.logger import logging as logger
from sqlalchemy import create_engine
from app.internals.models import BaseModel

engine = create_engine(
    "postgresql+psycopg2://postgres:12345678@localhost/player", echo=False
)
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
    logger.info("DATABASE::CREATE_TABLE:tracks_metadata")
