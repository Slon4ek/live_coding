import threading
import time
from collections import OrderedDict
from functools import wraps


def memoize(ttl: float, maxsize: int | None = None):
    def decorator(func):
        if ttl <= 0:
            raise ValueError("ttl must be greater than 0")
        _cache = OrderedDict()
        _lock = threading.Lock()
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                key = (args, tuple(sorted(kwargs.items())))
                hash(key)
            except TypeError:
                raise TypeError("Cannot cache function with non-hashable arguments")

            with _lock:
                now = time.monotonic()
                if key in _cache:
                    value, expire = _cache[key]
                    if now < expire:
                        _cache.move_to_end(key)
                        return value
                    del _cache[key]
            try:
                result = func(*args, **kwargs)
            except Exception:
                raise

            with _lock:
                expire = now + ttl
                _cache[key] = (result, expire)
                if maxsize is not None and len(_cache) > maxsize:
                    _cache.popitem(last=False)
            return result

        def cache_clear():
            with _lock:
                _cache.clear()
        wrapper.cache_clear = cache_clear

        return wrapper

    return decorator