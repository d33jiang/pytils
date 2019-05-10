import json
from typing import List, Dict, NamedTuple

import pytest

from pytils.object_view import ObjectView


class BasicTestEntry(NamedTuple):
    json_string: str
    repr_string: str


basic_tests = [
    BasicTestEntry('null', 'None'),

    BasicTestEntry('true', 'True'),
    BasicTestEntry('false', 'False'),

    BasicTestEntry('0', '0'),
    BasicTestEntry('1', '1'),
    BasicTestEntry('-1', '-1'),

    BasicTestEntry('0.0', repr(0.0)),
    BasicTestEntry('1e1', repr(1e1)),
    BasicTestEntry('1.2', '1.2'),
    BasicTestEntry('-3.14159', '-3.14159'),

    BasicTestEntry('\"asdf\"', repr('asdf')),
    BasicTestEntry('\"\"', repr('')),

    BasicTestEntry('[]', 'ObjectView([])'),
    BasicTestEntry('[1, 2, 3]', 'ObjectView([1, 2, 3])'),
    BasicTestEntry('[\"apple\", 2, {}]', f'ObjectView([{"apple"!r}, 2, {{}}])'),

    BasicTestEntry('{}', 'ObjectView({})'),
    BasicTestEntry(
        '{\"a\": 2, \"b\": {\"a\": 4}, \"c\": [1, 2, 3]}',
        f'ObjectView({{{"a"!r}: 2, {"b"!r}: {{{"a"!r}: 4}}, {"c"!r}: [1, 2, 3]}})'
    )
]


@pytest.mark.parametrize('basic_test', basic_tests)
def test_basic_test(basic_test):
    assert repr(ObjectView.of(json.loads(basic_test.json_string))) == basic_test.repr_string


def test_view_of_none():
    assert ObjectView.of(None) is None


def test_view_of_bool():
    assert ObjectView.of(True) is True
    assert ObjectView.of(False) is False


def test_view_of_int():
    test_cases = [
        0,
        1,
        -1,
        2,
        -42
    ]

    for val in test_cases:
        assert ObjectView.of(val) == val


def test_view_of_float():
    import math
    test_cases = [
        0.0,
        1.0,
        -1.0,
        2.0,
        1.2,
        math.e,
        math.tau,
        math.pi,
        math.inf,
        -math.inf,
        math.tan(1)
    ]

    for val in test_cases:
        assert ObjectView.of(val) == val


def test_view_of_str():
    test_cases = [
        'Alice --> Eve --> Bob',
        '^Lorem ipsum.|blah|asdf$',
        ''
    ]

    for val in test_cases:
        assert ObjectView.of(val) == val


def test_view_of_bytes():
    test_cases = [
        b'foo.bar',
        b'NullPointerException',
        b''
    ]

    for val in test_cases:
        assert ObjectView.of(val) == val


def _assert_same_item(actual, expected):
    if isinstance(expected, Dict):
        _assert_same_dict(actual, expected)
    elif isinstance(expected, List):
        _assert_same_list(actual, expected)
    else:
        assert actual == expected


def _assert_same_list(actual, expected: List):
    assert isinstance(actual, ObjectView)
    assert len(actual) == len(expected)

    for actual_item, expected_item in zip(actual, expected):
        _assert_same_item(actual_item, expected_item)


def _assert_same_dict(actual, expected: Dict):
    assert isinstance(actual, ObjectView)
    assert len(actual) == len(expected)

    for expected_key, expected_value in expected.items():
        assert expected_key in actual
        _assert_same_item(actual[expected_key], expected_value)


def test_view_of_list():
    test_cases = [
        [None, 1, True, 3.14, 'META-INF', b''],
        ['car', ['cons', 2, ['cons', 1, []]]]
    ]

    for test_case in test_cases:
        _assert_same_item(ObjectView.of(test_case), test_case)


def test_view_of_unequal_lists():
    val_a = ['car', ['cons', 2, ['cons', 1, []]]]
    val_b = ['car', ['cons', 2, ['cons', 3, []]]]

    _assert_same_item(ObjectView.of(val_a), val_a)
    _assert_same_item(ObjectView.of(val_b), val_b)

    with pytest.raises(AssertionError):
        _assert_same_item(ObjectView.of(val_a), val_b)

    with pytest.raises(AssertionError):
        _assert_same_item(ObjectView.of(val_b), val_a)


def test_view_of_dict():
    test_cases = {
        1: 2,
        None: True,
        'pi': 4,
        42: {},
        list: [],
        'inverse_map': {
            2: 1,
            True: None,
            4: 'pi',
            TypeError: list,
            RecursionError: {}
        }
    }

    _assert_same_item(ObjectView.of(test_cases), test_cases)


def test_view_of_dict_keys():
    test_case = {
        1: 2,
        None: True,
        'pi': 4,
        42: {},
        list: [],
        'inverse_map': {
            2: 1,
            True: None,
            4: 'pi',
            TypeError: list,
            RecursionError: {}
        }
    }

    test_keys = {1, None, 'pi', 42, list, 'inverse_map'}
    assert {ObjectView.get_value(key) for key in test_case} == test_keys

    test_case_view = ObjectView.of(test_case)

    for key, value in test_case.items():
        _assert_same_item(test_case_view[key], value)

    for key_view, value_view in test_case_view.items():
        assert test_case[ObjectView.get_value(key_view)] == ObjectView.get_value(value_view)

    assert 42 in test_case
    assert 43 not in test_case
