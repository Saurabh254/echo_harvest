from collections.abc import Coroutine

import redis.asyncio as aioredis
from server.internals.schemas import MetaData
from . import errors
import logging
import json


class GiEventHandler:
    def __init__(self, redis: aioredis.Redis) -> None:
        self.redis = redis
        self._key = "recent_track_metadata"

    async def get_last_player_metadata(self) -> dict[str, str | int] | None:
        """Get the latest played music metadata
        :returns:  the MetaData fetched from the playerctl
        :raise RecordNotFoundError: when unable to retrieve the recent record MetaData from the redis.
        :rtype: dict[str, str | int]

        """
        metadata = await self.redis.get(self._key)
        if metadata:
            return json.loads(metadata)
        raise errors.RecordNotFoundError("redis_record_not_found_error","No recent record found")

    async def store_track_metadata(self, metadata: MetaData) -> None:
        """SET the current music metadata"""

        if self.get_last_player_metadata():
            await self.redis.delete(self._key)

        await self.redis.set(self._key, json.dumps(metadata.__dict__, default=str))
        logging.debug(f"REDIS::INSERT:{metadata}")
