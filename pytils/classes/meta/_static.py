from typing import Any, Tuple, Dict, NoReturn

__all__ = [
    'StaticMeta'
]


class StaticMeta(type):

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
