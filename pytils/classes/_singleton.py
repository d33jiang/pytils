from typing import Type


def singleton(cls) -> Type:
    """
    Decorator for defining singleton classes.

    The resulting singleton class can then be instantiated at most once. The first instance is reused for subsequent
    instantiations and the arguments provided in subsequent instantiations are simply discarded.

    """
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
