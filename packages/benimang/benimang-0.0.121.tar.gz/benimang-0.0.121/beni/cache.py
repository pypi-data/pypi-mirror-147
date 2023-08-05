import inspect
from functools import wraps
from typing import Any, NamedTuple, cast

import beni


class _CachedResult(NamedTuple):
    par: Any
    result: Any


_cached_func_result: dict[Any, list[_CachedResult]] = {}


def wa_cache():
    def wraperfun(func: beni.AsyncFun) -> beni.AsyncFun:
        @wraps(func)
        async def wraper(*args: Any, **kwargs: Any):
            target_func = inspect.unwrap(func)
            par = [args, kwargs]
            _cached_func_result.setdefault(target_func, [])
            _cached_list = _cached_func_result[target_func]
            for cached_result in _cached_list:
                if cached_result.par == par:
                    return cached_result.result
            result = await func(*args, **kwargs)
            _cached_list.append(_CachedResult(par, result))
            return result
        return cast(Any, wraper)
    return wraperfun
