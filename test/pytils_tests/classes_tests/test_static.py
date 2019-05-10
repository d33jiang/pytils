import pytest

from pytils.classes import static
from pytils.classes.meta import StaticMeta

flags = {}


def run_static_class_test_init(self, key):
    assert key not in flags
    flags[key] = {}

    flags[key]['has_init_run'] = True
    flags[key]['was_self_none_during_init'] = self is None


def assert_is_static_class(cls, key):
    assert key in flags
    assert flags[key]['has_init_run']
    assert flags[key]['was_self_none_during_init']

    with pytest.raises(NotImplementedError):
        _ = cls()


class Static(metaclass=StaticMeta):

    def __init__(self):
        run_static_class_test_init(self, 'Static')


@static
class DecoratedStatic:

    def __init__(self):
        run_static_class_test_init(self, 'DecoratedStatic')


def test_static():
    assert_is_static_class(Static, 'Static')


def test_decorated_static():
    assert_is_static_class(DecoratedStatic, 'DecoratedStatic')
