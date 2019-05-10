"""Test the functionality of the pytils.dev.stopwatch.Stopwatch utility class."""

from pytils.dev.stopwatch import Stopwatch


def test_initialization():
    """Test the initialization of an empty Stopwatch instance."""
    timing = Stopwatch()

    assert timing.reference_time is None

    marks = timing.get_marks()
    assert marks is not None and not marks

    offsets = timing.get_offsets()
    assert offsets is not None and not offsets

    intervals = timing.get_intervals()
    assert intervals is not None and not intervals
