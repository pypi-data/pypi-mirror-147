from abc import abstractmethod
import abc
from os import PathLike
import os
import pickle
from typing import Any, Callable, Hashable, Dict, Optional, Union
from time import time

from .general import _NoValue


class CacheProvider(abc.ABC):
    @abstractmethod
    def getData(self, hsh: str, func: Callable, *args, **kwargs):
        ...

    @abstractmethod
    def setData(self, hsh: str, func: Callable, data, *args, **kwargs):
        ...


class FileCacheProvider(CacheProvider):
    def __init__(self, tmpDirPath: Union[str, PathLike] = './tmp',
                 fileNameCreator: Optional[Callable]=None, isExpired: Optional[Callable[[int, Any], bool]] = None,
                 ) -> None:
        self._tmpDirPath = tmpDirPath
        self._fileNameCreator = fileNameCreator or self._getFileName
        self._isExpired = isExpired

    def _getFileName(self, hsh: str, func: Callable, *args, **kwargs):
        return f"{func.__qualname__[:100].replace('<', '').replace('>', '')}C{hsh}.pkl"

    def getData(self, hsh, func: Callable, *args, **kwargs):
        filename = self._fileNameCreator(hsh, func, *args, **kwargs)
        try:
            with open(os.path.join(self._tmpDirPath, filename), 'rb') as f:
                data = pickle.load(f)
                if self._isExpired and self._isExpired(data['timestamp'], data['data']):
                    return _NoValue
                return data['data']
        except:
            return _NoValue

    def setData(self, hsh, func: Callable, data, *args, **kwargs):
        filename = self._fileNameCreator(hsh, func, *args, **kwargs)
        try:
            with open(os.path.join(self._tmpDirPath, filename), 'wb') as f:
                pickle.dump({'data': data, 'timestamp': int(time())}, f)
        except:
            pass


class InMemoryCacheProvider(CacheProvider):
    def __init__(self, isExpired: Optional[Callable[[int, Any], bool]] = None) -> None:
        self._inMemoryCache: Dict[Hashable, Dict[str, Any]] = {}
        self._isExpired = isExpired

    def getData(self, hsh, func: Callable, *args, **kwargs):
        data = self._inMemoryCache.get((func.__class__, hsh), _NoValue)
        if data is _NoValue:
            return data
        if self._isExpired and self._isExpired(data['timestamp'], data['data']):
            return _NoValue
        return data['data']

    def setData(self, hsh, func: Callable, data, *args, **kwargs):
        self._inMemoryCache[(func.__class__, hsh)] = {'data': data, 'timestamp': int(time())}