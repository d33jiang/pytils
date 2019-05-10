"""Test the functionality of the pytils.dev.stopwatch.Stopwatch utility class."""

from typing import Any, Callable, Optional, Sequence, Tuple

import pytest

from pytils.dev.stopwatch import Mark, Stopwatch


def test_initialization():
    """Test the initialization of an empty Stopwatch instance."""
    timing = Stopwatch()

    assert timing.reference_time is None

    marks = timing.get_marks()
    assert marks is not None and not marks

    with pytest.raises(ValueError):
        _ = timing.get_offsets()

    intervals = timing.get_intervals()
    assert intervals is not None and not intervals


@pytest.fixture
def sample_stopwatch() -> Stopwatch:
    """Initialize a Stopwatch instance with a mock TimeSupplier."""
    timing_sequence = (2, 3, 5, 8, 13, 20)
    timings = iter(timing_sequence)

    def get_next_timestamp():
        return next(timings)

    return Stopwatch(get_next_timestamp)


def run_sample_stopwatch_sequence(stopwatch: Stopwatch, action_sequence: Sequence[Callable[[], Any]]):
    """Test Stopwatch functionality with a predefined sequence of Stopwatch interactions."""
    actions = iter(action_sequence)

    def run_next_action():
        next(actions)()

    run_next_action()

    stopwatch.add_mark()
    run_next_action()

    stopwatch.set_reference_time()
    run_next_action()

    stopwatch.add_mark('foo')
    run_next_action()

    stopwatch.add_mark('bar')
    run_next_action()

    stopwatch.set_reference_time()
    run_next_action()

    stopwatch.clear_marks()
    run_next_action()

    stopwatch.set_reference_time()
    run_next_action()


def test_repr(sample_stopwatch: Stopwatch):
    """Test getting a string representation of the Stopwatch instance."""

    def assert_repr_value(expected_value: str) -> Callable[[], Any]:
        def perform_action():
            assert repr(sample_stopwatch) == expected_value

        return perform_action

    run_sample_stopwatch_sequence(
        sample_stopwatch,
        (
            assert_repr_value('<Stopwatch; ref: None; num_marks: 0>'),
            assert_repr_value('<Stopwatch; ref: None; num_marks: 1>'),  # add_mark()
            assert_repr_value('<Stopwatch; ref: 3; num_marks: 1>'),  # set_reference_time()
            assert_repr_value('<Stopwatch; ref: 3; num_marks: 2>'),  # add_mark('foo')
            assert_repr_value('<Stopwatch; ref: 3; num_marks: 3>'),  # add_mark('bar')
            assert_repr_value('<Stopwatch; ref: 13; num_marks: 3>'),  # set_reference_time()
            assert_repr_value('<Stopwatch; ref: 13; num_marks: 0>'),  # clear_marks()
            assert_repr_value('<Stopwatch; ref: 20; num_marks: 0>'),  # set_reference_time()
        )
    )


def test_reference_time(sample_stopwatch: Stopwatch):
    """Test getting and setting the reference timestamp."""

    def assert_reference_timestamp_value(expected_value: Optional[float]) -> Callable[[], Any]:
        def perform_action():
            assert sample_stopwatch.reference_time == expected_value

        return perform_action

    run_sample_stopwatch_sequence(
        sample_stopwatch,
        (
            assert_reference_timestamp_value(None),
            assert_reference_timestamp_value(None),  # add_mark()
            assert_reference_timestamp_value(3),  # set_reference_time()
            assert_reference_timestamp_value(3),  # add_mark('foo')
            assert_reference_timestamp_value(3),  # add_mark('bar')
            assert_reference_timestamp_value(13),  # set_reference_time()
            assert_reference_timestamp_value(13),  # clear_marks()
            assert_reference_timestamp_value(20),  # set_reference_time()
        )
    )


def test_timing_outputs(sample_stopwatch: Stopwatch):
    """Test getting the marks, offsets, and intervals."""

    def assert_timing_output_values(
            expected_marks: Sequence[Mark],
            expected_offsets: Optional[Sequence[Tuple[float, Any]]],
            expected_intervals: Sequence[Tuple[float, Any]]) -> Callable[[], Any]:

        def perform_action():
            assert sample_stopwatch.get_marks() == expected_marks

            if expected_offsets is None:
                with pytest.raises(ValueError):
                    _ = sample_stopwatch.get_offsets()
            else:
                assert expected_offsets == sample_stopwatch.get_offsets()

            assert expected_intervals == sample_stopwatch.get_intervals()

        return perform_action

    run_sample_stopwatch_sequence(
        sample_stopwatch,
        (
            assert_timing_output_values((), None, ()),

            # add_mark()
            assert_timing_output_values(
                (
                    Mark(2, None),
                ),
                None,
                ()
            ),

            # set_reference_time() ; ref: 3
            assert_timing_output_values(
                (
                    Mark(2, None),
                ),
                (
                    (-1, None),
                ),
                (
                    (-1, None),
                )
            ),

            # add_mark('foo') ; ref: 3
            assert_timing_output_values(
                (
                    Mark(2, None),
                    Mark(5, 'foo'),
                ),
                (
                    (-1, None),
                    (2, 'foo'),
                ),
                (
                    (-1, None),
                    (3, 'foo'),
                )
            ),

            # add_mark('bar') ; ref: 3
            assert_timing_output_values(
                (
                    Mark(2, None),
                    Mark(5, 'foo'),
                    Mark(8, 'bar'),
                ),
                (
                    (-1, None),
                    (2, 'foo'),
                    (5, 'bar'),
                ),
                (
                    (-1, None),
                    (3, 'foo'),
                    (3, 'bar'),
                )
            ),

            # set_reference_time() ; ref: 13
            assert_timing_output_values(
                (
                    Mark(2, None),
                    Mark(5, 'foo'),
                    Mark(8, 'bar'),
                ),
                (
                    (-11, None),
                    (-8, 'foo'),
                    (-5, 'bar'),
                ),
                (
                    (-11, None),
                    (3, 'foo'),
                    (3, 'bar'),
                )
            ),

            # clear_marks()
            assert_timing_output_values((), (), ()),

            # set_reference_time() ; ref: 20
            assert_timing_output_values((), (), ()),
        )
    )
