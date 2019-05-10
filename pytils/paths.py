import abc
from typing import Any

__all__ = [
    'AbstractPath',
    'DotDelimitedPath',
    'UrlPath',
]


class AbstractPath(metaclass=abc.ABCMeta):
    """Utility class for generating path strings."""

    __slots__ = ('_path',)

    def __init__(self, path: str):
        """Initialize an AbstractPath instance from an existing path string."""
        self._path = path

    @property
    def path(self) -> str:
        """Get the path string."""
        return self._path

    @staticmethod
    @abc.abstractmethod
    def _join(parent: str, segment: str) -> str:
        """Join the provided path segment to the end of the parent path string."""
        raise NotImplementedError

    def _resolve(self, segment: str) -> 'AbstractPath':
        """Create an AbstractPath from joining the provided path segment to the end of this path string."""
        return AbstractPath(self._join(self._path, segment))

    def resolve(self, segment: str) -> 'AbstractPath':
        """Create an AbstractPath from joining the provided path segment to the end of this path string."""
        return self._resolve(segment)

    def __getattr__(self, key: str) -> 'AbstractPath':
        """Create an AbstractPath from joining the provided path segment to the end of this path string."""
        return self._resolve(key)

    def __getitem__(self, key: Any) -> 'AbstractPath':
        """Create an AbstractPath from joining the provided path segment to the end of this path string."""
        return self._resolve(str(key))

    def __str__(self) -> str:
        """Get the path string."""
        return self.path


class UrlPath(AbstractPath):
    """Utility class for generating URL path strings."""

    __slots__ = ()

    @staticmethod
    def _join(parent: str, segment: str) -> str:
        return f'{parent}/{segment}'


class DotDelimitedPath(AbstractPath):
    """Utility class for generating dot-delimited path strings."""

    __slots__ = ()

    @staticmethod
    def _join(parent: str, segment: str) -> str:
        return f'{parent}.{segment}'
