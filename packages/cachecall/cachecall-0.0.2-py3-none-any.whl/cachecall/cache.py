from dataclasses import dataclass
from typing import Any, Optional, Union
from datetime import datetime, timedelta
from collections import OrderedDict

from cachecall.data import data
from cachecall.expire_time import ExpireTime


DEFAULT_GROUP = "default"


def clear_cache(group=DEFAULT_GROUP):
    if group in data:
        data[group] = OrderedDict()


@dataclass
class Cache:
    max_size: Optional[int] = 0
    group: str = DEFAULT_GROUP
    ttl: Optional[Union[int, float]] = None  # seconds
    expire_time: Optional[ExpireTime] = None

    def _expire_date(self) -> Optional[datetime]:
        expire_date = None
        ttl_expiration = None

        if self.ttl:
            ttl_expiration = datetime.now() + timedelta(seconds=self.ttl)

        if self.expire_time:
            expire_date = self.expire_time.future_date()

        if not ttl_expiration and not expire_date:
            return None

        elif ttl_expiration and not expire_date:
            return ttl_expiration

        elif not ttl_expiration and expire_date:
            return expire_date

        elif ttl_expiration < expire_date:  # type: ignore
            return ttl_expiration

        elif ttl_expiration >= expire_date:  # type: ignore
            return expire_date  # type: ignore

    def __post_init__(self):
        if self.group not in data:
            data[self.group] = OrderedDict()

    def set(self, key: str, value: Any):
        data[self.group][key] = {"value": value, "expires_at": self._expire_date()}

    def get(self, key: str) -> Optional[Any]:
        value_cached = data[self.group].get(key)

        if not value_cached:
            return None

        if value_cached.get("expires_at") and datetime.now() > value_cached["expires_at"]:
            del data[self.group][key]
            return None

        return value_cached.get("value")

    def is_full(self) -> bool:
        return self.max_size and len(data[self.group]) == self.max_size  # type: ignore

    def remove_first_item(self):
        data[self.group].popitem(last=False)
