from typing import Type, NoReturn

__all__ = [
    'static'
]


def _raise_init():
    raise NotImplementedError('Static classes cannot be instantiated')


def static(cls) -> Type:
    def on_init(*_args, **_kwargs) -> NoReturn:
        _raise_init()

    init_function = getattr(cls, '__init__', lambda _: None)
    cls.__new__ = on_init
    cls.__init__ = on_init
    cls.__call__ = on_init

    init_function(None)

    return cls
