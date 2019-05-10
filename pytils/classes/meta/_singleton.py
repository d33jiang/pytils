from typing import Any, Dict, Tuple

__all__ = [
    'SingletonMeta'
]


class SingletonMeta(type):
    """
    Metaclass for defining singleton classes.

    The resulting singleton class can then be instantiated at most once. The first instance is reused for subsequent
    instantiations and the arguments provided in subsequent instantiations are simply discarded.

    """

    def __init__(cls, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]):
        cls._Singleton__instance = None
        super(SingletonMeta, cls).__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs):
        if cls._Singleton__instance is None:
            cls._Singleton__instance = super(SingletonMeta, cls).__call__(*args, **kwargs)

        return cls._Singleton__instance

    def exists_instance(cls) -> bool:
        """Get whether an instance of this singleton class exists."""
        return cls._Singleton__instance is not None
