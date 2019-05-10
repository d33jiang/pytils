"""Test the creation of singleton classes through the pytils.classes package."""

from pytils.classes import singleton
from pytils.classes.meta import SingletonMeta


def assert_is_singleton_class(cls):
    """Test that the provided class satisfies the properties desired of a singleton class."""
    assert not hasattr(cls, 'has_instantiated')

    instance = cls()
    assert hasattr(cls, 'has_instantiated')
    assert instance is not None

    instance2 = cls()
    assert instance2 is instance


def run_singleton_class_test_init(self):
    """Initialize an instance of a tested singleton class by marking that the __init__ function has been run."""
    self.__class__.has_instantiated = True
    assert self is not None


class MetaclassSingleton(metaclass=SingletonMeta):
    """A singleton class that is created from the pytils.classes.meta.SingletonMeta metaclass."""

    def __init__(self):
        run_singleton_class_test_init(self)


@singleton
class DecoratorSingleton:
    """A singleton class that is created from the @pytils.classes.singleton decorator."""

    def __init__(self):
        run_singleton_class_test_init(self)


def test_singleton_metaclass():
    """Test that the SingletonMeta metaclass configures a class to exhibit the behaviour of a singleton class."""
    assert_is_singleton_class(MetaclassSingleton)


def test_singleton_decorator():
    """Test that the @singleton decorator configures a class to exhibit the behaviour of a singleton class."""
    assert_is_singleton_class(DecoratorSingleton)
