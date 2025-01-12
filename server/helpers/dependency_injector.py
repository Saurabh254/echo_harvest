import functools
import inspect
from typing import Any, Awaitable, Callable, Coroutine, Optional, Type, ParamSpec, TypeVar
from server.utils import get_redis_client


def inject_redis[RT, **P](func: Callable[..., Awaitable[RT]]) -> Callable[...,Awaitable[RT]]:
    if not inspect.iscoroutinefunction(func):
        raise TypeError("function must be a coroutine")
    @functools.wraps(func)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> RT:
        if 'redis' not in kwargs.keys():
            _redis_client = get_redis_client()
            kwargs['redis'] = _redis_client
        return await func(*args, **kwargs)
    return _wrapper
