from pytils.classes import singleton
from pytils.classes.meta import SingletonMeta


def run_singleton_class_test_init(self):
    self.__class__.has_instantiated = True
    assert self is not None


def assert_is_singleton_class(cls):
    assert not hasattr(cls, 'has_instantiated')

    instance = cls()
    assert hasattr(cls, 'has_instantiated')
    assert instance is not None

    instance2 = cls()
    assert instance2 is instance


class Singleton(metaclass=SingletonMeta):

    def __init__(self):
        run_singleton_class_test_init(self)


@singleton
class DecoratedSingleton:

    def __init__(self):
        run_singleton_class_test_init(self)


def test_singleton():
    assert_is_singleton_class(Singleton)


def test_decorated_singleton():
    assert_is_singleton_class(DecoratedSingleton)
