from typing import Any, Tuple, Dict

__all__ = [
    'SingletonMeta'
]


class SingletonMeta(type):

    def __init__(cls, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]):
        cls._Singleton__instance = None
        super(SingletonMeta, cls).__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs):
        if cls._Singleton__instance is None:
            cls._Singleton__instance = super(SingletonMeta, cls).__call__(*args, **kwargs)

        return cls._Singleton__instance
