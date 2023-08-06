import inspect
import asyncio

from uuid import uuid4
from functools import wraps
from cachecall.expire_time import ExpireTime
from typing import Optional, Tuple, Union

from cachecall.cache import Cache
from cachecall.cache_keys import create_key


def cache(
    max_size: Optional[int] = None,
    group_name: Optional[str] = None,
    ttl: Optional[Union[int, float]] = None,
    expire_time: Optional[ExpireTime] = None,
    ignore_keys: Optional[Tuple[str]] = None,
):
    def inner_cached(func):
        group = group_name if group_name else f"{func.__name__}_{str(uuid4())}"

        cache = Cache(max_size, group, ttl, expire_time)

        @wraps(func)
        async def async_inner(*args, **kwargs):
            nonlocal ignore_keys
            nonlocal cache

            key = create_key(func.__name__, args, kwargs, ignore_keys)

            result = cache.get(key)

            if result:
                return result

            if inspect.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            if cache.is_full():
                cache.remove_first_item()

            cache.set(key, result)

            return result

        @wraps(func)
        def sync_inner(*args, **kwargs):
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:  # pragma: no cover
                loop = asyncio.new_event_loop()

            return loop.run_until_complete(async_inner(*args, **kwargs))

        if inspect.iscoroutinefunction(func):
            return async_inner

        return sync_inner

    return inner_cached
