import inspect
import time
from functools import wraps


def timed(_func=None, *, threshold=None):
    def decorator(func):

        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start = time.time()
                result = await func(*args, **kwargs)
                end = time.time()
                if threshold is not None and end - start > threshold:
                    print(f"{func.__name__} took {end - start} seconds")
                return result
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                end = time.time()
                if threshold is not None and end - start > threshold:
                    print(f"{func.__name__} took {end - start} seconds")
                return result

        return wrapper
    if _func is not None:
        return decorator(_func)
    return decorator
