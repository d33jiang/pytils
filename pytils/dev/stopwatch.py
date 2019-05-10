import itertools
from collections import deque
from typing import Any, Deque, NamedTuple, Optional, Sequence, Tuple

from .._config.time import DEFAULT_TIME_SUPPLIER, TimeSupplier, TimeType

__all__ = [
    'Stopwatch'
]


class Mark(NamedTuple):
    """Timestamp recorded by the Stopwatch class."""

    timestamp: TimeType
    key: Any = None


class Stopwatch:
    """Lightweight utility class for managing timestamps."""

    __slots__ = ('_time_supplier', '_reference_time', '_marks')

    def __init__(self, time_supplier: TimeSupplier = DEFAULT_TIME_SUPPLIER):
        """
        Initialize an empty Stopwatch instance.

        Args:
            time_supplier: A function taking no arguments that will provide time values upon invocation.
                (Defaults to time.time.)

        """
        self._time_supplier = time_supplier

        self._reference_time = None  # type: Optional[TimeType]
        self._marks = deque()  # type: Deque[Mark]

    def __repr__(self) -> str:
        """Return a string representation of the Stopwatch instance."""
        return f'<Stopwatch; ref: {self._reference_time!s}; num_marks: {len(self._marks)}>'

    @property
    def reference_time(self) -> Optional[TimeType]:
        """Get the reference timestamp, which is used to calculate the mark offsets."""
        return self._reference_time

    def set_reference_time(self):
        """Renew the reference timestamp, which is used to calculate the mark offsets."""
        self._reference_time = self._time_supplier()

    def add_mark(self, key=None):
        """
        Create a new Mark recording the current time.

        Args:
            key: An optional key to be included in the created Mark.
                (Defaults to None.)

        """
        self._marks.append(Mark(self._time_supplier(), key))

    def clear_marks(self):
        """Clear all recorded marks."""
        self._marks = deque()

    def get_marks(self) -> Sequence[Mark]:
        """Get the currently recorded marks."""
        return tuple(self._marks)

    def get_offsets(self) -> Sequence[Tuple[TimeType, Any]]:
        """
        Get the offsets of the currently recorded marks, as measured relative to the current reference timestamp.

        For each recorded mark (in order of recording), the returned sequence contains a corresponding 2-tuple with, as
        its first element, the offset of the mark relative to the reference timestamp and with, as its second element,
        the key associated with the mark.

        """
        ref_time = self._reference_time
        if ref_time is None:
            raise ValueError('No reference time')

        return tuple((mark - ref_time, key) for mark, key in self._marks)

    def get_intervals(self) -> Sequence[Tuple[TimeType, Any]]:
        """
        Get the inter-mark time intervals.

        For each consecutive pair X, Y of recorded marks (in order of recording), the returned sequence contains a
        corresponding 2-tuple with, as its first element, the time difference from mark X to mark Y and with, as its
        second element, the key associated with mark Y.

        """
        times = self._marks

        ref_time = self._reference_time
        if ref_time is not None:
            times = itertools.chain(((ref_time, None),), times)

        iter_a, iter_b = itertools.tee(times, 2)
        iter_b = itertools.islice(iter_b, 1, None)

        return tuple((time_b - time_a, key) for ((time_a, _), (time_b, key)) in zip(iter_a, iter_b))
