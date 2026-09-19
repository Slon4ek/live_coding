import inspect
import typing
from functools import wraps


def validate_args(func):
    sig = inspect.signature(func)
    hints = typing.get_type_hints(func)
    print(hints)
    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        for name, value in bound.arguments.items():
            if name not in hints:
                continue

            expected_type = hints[name]
            if expected_type is typing.Union:
                args = typing.get_args(expected_type)

                if not any(isinstance(value, arg) for arg in args):
                    raise TypeError(f"{name} must be one of {args} got {type(value).__name__}")

            if not isinstance(value, hints[name]):
                raise TypeError(f"{name} must be {hints[name]} got {type(value).__name__}")
        return func(*args, **kwargs)
    return wrapper