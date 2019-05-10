import itertools
from collections import deque
from typing import Any, Optional, Iterator, Tuple, Deque, NamedTuple

from .._config.time import TimeType, TimeSupplier, DEFAULT_TIME_SUPPLIER

__all__ = [
    'Stopwatch'
]


class Mark(NamedTuple):
    mark: TimeType
    key: Any = None


class Stopwatch:

    def __init__(self, s_time: TimeSupplier = DEFAULT_TIME_SUPPLIER):
        self.s_time = s_time

        self._reference_time = None  # type: Optional[TimeType]
        self._marks = deque()  # type: Deque[Mark]

    def __repr__(self):
        return f'<Stopwatch; ref: {self._reference_time!s}; num_marks: {len(self._marks)}>'

    @property
    def reference(self) -> Optional[TimeType]:
        return self._reference_time

    def set_reference(self):
        self._reference_time = self.s_time()

    def add_mark(self, key=None):
        self._marks.append(Mark(self.s_time(), key))

    def clear(self):
        self._marks = deque()

    def marks(self) -> Iterator[Mark]:
        yield from self._marks

    def offsets(self) -> Iterator[Tuple[TimeType, Any]]:
        ref_time = self._reference_time
        if ref_time is None:
            raise ValueError('No reference time')

        yield from ((mark - ref_time, key) for mark, key in self._marks)

    def durations(self) -> Iterator[Tuple[TimeType, Any]]:
        times = self._marks

        ref_time = self._reference_time
        if ref_time is not None:
            times = itertools.chain(((ref_time, None),), times)

        iter_a, iter_b = itertools.tee(times, 2)
        iter_b = itertools.islice(iter_b, 1, None)

        yield from ((time_b - time_a, key) for ((time_a, _), (time_b, key)) in zip(iter_a, iter_b))
