from os import PathLike
import sys
from typing import Any, Callable, Optional, Dict, TypeVar, Union, cast, overload
from functools import wraps

from .general import _NoValue
from .cache_provider import CacheProvider, FileCacheProvider, InMemoryCacheProvider

if sys.version_info < (3, 7):
    from typing_extensions import Protocol
else:
    from typing import Protocol



class UniqueKeyType(Protocol):
    def __call__(self, *args: Any, **kwargs: Any) -> str: ...


FuncType = TypeVar('FuncType', bound=Callable)

CACHER_MAP: Dict[Optional[str], "Cacher"] = {}


class Cacher:
    def __init__(self, *, name: Optional[str] = None, tmpDirPath: Optional[Union[str, PathLike]] = None,
                 isExpired: Optional[Callable[[int, Any], bool]] = None, isLocal=False,
                 uniqueKey: Optional[UniqueKeyType] = None, isEnable=True,
                 cacheProvider: Optional[CacheProvider] = None,
                 **kwargs) -> None:
        if not isLocal:
            if CACHER_MAP.get(name):
                raise ValueError('name should be unique across process')
            CACHER_MAP[name] = self
        self._name = name
        self._tmpDirPath = tmpDirPath
        self._isExpired = isExpired
        self._isLocal = isLocal
        self._isEnable = isEnable
        self._uniqueKey = uniqueKey or self._getUniqueKey
        self._cacheProvider = cacheProvider or (FileCacheProvider(tmpDirPath=tmpDirPath, isExpired=isExpired)
                                                if tmpDirPath else InMemoryCacheProvider(isExpired=isExpired))

    def _getUniqueKey(self, *args, **kwargs) -> str:
        res = []
        for a in args:
            try:
                hash(a)
                res.append(a)
            except:
                res.append(None)
        for k, v in kwargs.items():
            try:
                hash(v)
                res.append((k, v))
            except:
                res.append((k, None))
        return str(hash(tuple(res)))

    @overload
    def cache(self, func: FuncType, *, tmpDirPath: Optional[Union[str, PathLike]] = None,
                 isExpired: Optional[Callable[[int, Any], bool]] = None,
                 uniqueKey: Optional[UniqueKeyType] = None, isEnable=True,
                 cacheProvider: Optional[CacheProvider] = None,) -> FuncType:
        ...

    @overload
    def cache(self, func=None, *, tmpDirPath: Optional[Union[str, PathLike]] = None,
                 isExpired: Optional[Callable[[int, Any], bool]] = None,
                 uniqueKey: Optional[UniqueKeyType] = None, isEnable=True,
                 cacheProvider: Optional[CacheProvider] = None,) -> Callable[[FuncType], FuncType]:
        ...

    def cache(self, func: Optional[FuncType]=None, *, tmpDirPath: Optional[Union[str, PathLike]] = None,
                 isExpired: Optional[Callable[[int, Any], bool]] = None,
                 uniqueKey: Optional[UniqueKeyType] = None, isEnable=True,
                 cacheProvider: Optional[CacheProvider] = None,):
        if not func:
            kwargs = {k: v for k, v in locals().items() if k in self.cache.__annotations__}
            newself = Cacher(**{**self.__dict__, **kwargs, 'isLocal': True})
            def dec(func):
                return self._getDecorated(func, newself)
            return dec
        return self._getDecorated(func, self)

    @staticmethod
    def _getDecorated(func: FuncType, self: 'Cacher') -> FuncType:
        if not self._isEnable:
            return func
        @wraps(func)
        def decorated(*args, **kwargs):
            hsh = self._uniqueKey(*args, **kwargs)
            res = self._cacheProvider.getData(hsh, func, *args, **kwargs)
            if res is not _NoValue:
                return res
            res = func(*args, **kwargs)
            self._cacheProvider.setData(hsh, func, res, *args, **kwargs)
            return res
        return cast(FuncType, decorated)



CACHER_MAP[None] = Cacher()


def getCacher(name: Optional[str] = None):
    return CACHER_MAP.get(name, CACHER_MAP[None])
