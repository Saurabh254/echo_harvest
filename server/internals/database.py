from sqlalchemy.orm import Session
from sqlalchemy import MetaData
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from server.internals.models import BaseModel
import config

engine = create_async_engine(config.DATABASE_URL, echo=False)
meta = MetaData()

async def get_async_session() -> AsyncSession:
    while True:
        async with AsyncSession(engine) as session:

            try:
                yield session
            except Exception as e:
                logging.warning(f"DATABASE::Session:{0}".format(e))
            finally:
                await session.close()


def create_table():
    BaseModel.metadata.create_all(engine)
    logging.warning("DATABASE::CREATE_TABLE:tracks_metadata")
