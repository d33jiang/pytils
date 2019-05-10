import abc
from typing import Any

__all__ = [
    'AbstractPath',
    'DotDelimitedPath',
    'UrlPath',
]


class AbstractPath(metaclass=abc.ABCMeta):
    __slots__ = ('_path',)

    def __init__(self, path: str):
        self._path = path

    @property
    def path(self) -> str:
        return self._path

    @staticmethod
    @abc.abstractmethod
    def _join(parent: str, segment: str) -> str:
        raise NotImplementedError

    def _resolve(self, segment: str) -> 'AbstractPath':
        return AbstractPath(self._join(self._path, segment))

    def resolve(self, segment: str) -> 'AbstractPath':
        return self._resolve(segment)

    def __getattr__(self, key: str) -> 'AbstractPath':
        return self._resolve(key)

    def __getitem__(self, key: Any) -> 'AbstractPath':
        return self._resolve(str(key))

    def __str__(self) -> str:
        return self.to_path()


class UrlPath(AbstractPath):
    __slots__ = ()

    @staticmethod
    def _join(parent: str, segment: str) -> str:
        return f'{parent}/{segment}'


class DotDelimitedPath(AbstractPath):
    __slots__ = ()

    @staticmethod
    def _join(parent: str, segment: str) -> str:
        return f'{parent}.{segment}'
