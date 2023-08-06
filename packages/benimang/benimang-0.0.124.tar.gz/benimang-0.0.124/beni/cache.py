import inspect
from functools import wraps
from typing import Any, NamedTuple, cast

import beni


class _CachedResult(NamedTuple):
    par: Any
    result: Any


_cached_func_result: dict[str, dict[Any, list[_CachedResult]]] = {}


def wa_cache(group_name: str = ''):
    def wraperfun(func: beni.AsyncFun) -> beni.AsyncFun:
        @wraps(func)
        async def wraper(*args: Any, **kwargs: Any):
            target_func = inspect.unwrap(func)
            par = [args, kwargs]
            if group_name not in _cached_func_result:
                _cached_func_result[group_name] = {}
            if target_func not in _cached_func_result[group_name]:
                _cached_func_result[group_name][target_func] = []
            _cached_list = _cached_func_result[group_name][target_func]
            for cached_result in _cached_list:
                if cached_result.par == par:
                    return cached_result.result
            result = await func(*args, **kwargs)
            _cached_list.append(_CachedResult(par, result))
            return result
        return cast(Any, wraper)
    return wraperfun


def wa_clear_group(group_name: str = ''):
    def wraperfun(func: beni.AsyncFun) -> beni.AsyncFun:
        @wraps(func)
        async def wraper(*args: Any, **kwargs: Any):
            try:
                return await func(*args, **kwargs)
            finally:
                clear_group(group_name)
        return cast(Any, wraper)
    return wraperfun


def clear(func: Any):
    func = inspect.unwrap(func)
    for data in _cached_func_result.values():
        for k in data.keys():
            if k == func:
                data[k] = []


def clear_group(group_name: str):
    if group_name in _cached_func_result:
        _cached_func_result[group_name] = {}
