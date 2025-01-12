import redis.asyncio as aioredis

import config


def get_redis_client() -> aioredis.Redis:
    """
    returns redis client session from pool
    """
    return aioredis.from_url(config.REDIS_URL)
