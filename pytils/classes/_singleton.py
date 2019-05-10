from typing import Type


def singleton(cls) -> Type:
    new_function = cls.__new__

    def get_instance(_cls, *args, **kwargs):
        if not hasattr(cls, '_Singleton__instance'):
            cls.__new__ = new_function
            cls._Singleton__instance = cls(*args, **kwargs)
            cls.__new__ = get_instance

            def get_none(*_args, **_kwargs) -> None:
                pass

            cls.__init__ = get_none
            cls.__call__ = get_instance

        return cls._Singleton__instance

    cls.__new__ = get_instance
    return cls
