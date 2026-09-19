import time
from typing import OrderedDict, Any


class LRUCacheTTL:
    def __init__(self, capacity: int, ttl: float):
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        if ttl <= 0:
            raise ValueError("ttl must be > 0")
        self.capacity = capacity
        self.ttl = ttl
        self._cache = OrderedDict()

    def get(self, key: Any, default: Any | None = None) -> Any:
        value, expire = self._cache.get(key, default)
        now = time.monotonic()
        if value is None:
            return default

        if expire < now:
            del self._cache[key]
            return default
        self._cache.move_to_end(key)
        return value

    def put(self, key: Any, value: Any) -> None:
        now = time.monotonic()
        expire = now + self.ttl

        self._cache[key] = (value, expire)

        if len(self._cache) > self.capacity:
            self._cache.popitem(last=False)

    def clean(self) -> None:
        now = time.monotonic()
        expired_keys = [key for key, (_, expire) in self._cache.items() if expire < now]
        for key in expired_keys:
            del self._cache[key]