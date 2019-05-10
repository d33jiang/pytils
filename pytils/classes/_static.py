from typing import NoReturn, Type

__all__ = [
    'static'
]


def _raise_init():
    raise NotImplementedError('Static classes cannot be instantiated')


def static(cls) -> Type:
    """
    Decorator for defining static classes.

    The resulting static class cannot be instantiated. If the __init__ method is defined, then it is invoked with None
    as the sole argument when the static class is defined.

    """

    def on_init(*_args, **_kwargs) -> NoReturn:
        _raise_init()

    init_function = getattr(cls, '__init__', lambda _: None)
    cls.__new__ = on_init
    cls.__init__ = on_init
    cls.__call__ = on_init

    init_function(None)

    return cls
