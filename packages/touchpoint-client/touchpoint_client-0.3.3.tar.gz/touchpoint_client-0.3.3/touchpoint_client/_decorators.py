from functools import wraps
from typing import ParamSpec, TypeVar, Callable

__all__ = ["use_error_details"]


T = TypeVar("T")
P = ParamSpec("P")


def use_error_details(func: Callable[P, T]):
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        kwargs["params"] = kwargs.get("params", {})
        if "error_details" in kwargs:
            kwargs["params"]["error_details"] = kwargs["error_details"]
        return func(*args, **kwargs)

    return wrapper
