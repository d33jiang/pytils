"""Test the creation of static classes through the pytils.classes package."""

import pytest

from pytils.classes import static
from pytils.classes.meta import StaticMeta

flags = {}


def assert_is_static_class(cls, key):
    """Test that the provided class satisfies the properties desired of a static class."""
    assert key in flags
    assert flags[key]['has_init_run']
    assert flags[key]['was_self_none_during_init']

    with pytest.raises(NotImplementedError):
        _ = cls()


def run_static_class_test_init(self, key):
    """Initialize an instance of a tested static class by marking that the __init__ function has been run."""
    assert key not in flags
    flags[key] = {}

    flags[key]['has_init_run'] = True
    flags[key]['was_self_none_during_init'] = self is None


class MetaclassStatic(metaclass=StaticMeta):
    """A static class that is created from the pytils.classes.meta.StaticMeta metaclass."""

    def __init__(self):
        run_static_class_test_init(self, 'MetaclassStatic')


@static
class DecoratorStatic:
    """A static class that is created from the @pytils.classes.static decorator."""

    def __init__(self):
        run_static_class_test_init(self, 'DecoratorStatic')


def test_static_metaclass():
    assert_is_static_class(MetaclassStatic, 'MetaclassStatic')


def test_static_decorator():
    assert_is_static_class(DecoratorStatic, 'DecoratorStatic')
