from typing import Any, Dict, NoReturn, Tuple

__all__ = [
    'StaticMeta'
]


class StaticMeta(type):
    """
    Metaclass for defining static classes.

    The resulting static class cannot be instantiated. If the __init__ method is defined, then it is invoked with None
    as the sole argument when the static class is defined.

    """

    @staticmethod
    def _raise_init():
        raise NotImplementedError('Static classes cannot be instantiated')

    def __init__(cls, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]):
        def on_init(*_args, **_kwargs) -> NoReturn:
            StaticMeta._raise_init()

        init_function = dct.get('__init__', lambda _: None)
        dct['__init__'] = on_init

        super(StaticMeta, cls).__init__(name, bases, dct)

        init_function(None)

        dct['__new__'] = on_init

    def __call__(cls, *args, **kwargs) -> NoReturn:
        StaticMeta._raise_init()
