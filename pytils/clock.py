import functools
import heapq
import logging
from collections import deque
from threading import Condition, RLock
from typing import Any, Callable, List, NamedTuple, Optional

from pytils.mixins import DaemonHandler
from ._config.time import DEFAULT_TIME_SUPPLIER, TimeSupplier, TimeType, ZERO_DURATION

__all__ = [
    'Action',
    'Clock',
    'Handler',
    'Schedule',
    'ScheduleKey',
    'SchedulingQueue',
    'TimeSupplier',
    'TimeType',
]

_DEFAULT_MAX_TASK_QUEUE_SIZE = 4096
_MAX_SLEEP_DURATION = 12.

#
# Convenience Function

wrap_action = functools.partial


#
# Data Definitions

class ScheduleKey(NamedTuple):
    period: Optional[float]
    action: 'Action'


class ScheduleEntry(NamedTuple):
    next_run: float
    key: 'ScheduleKey'


Action = Callable[[], Any]
Handler = Callable[[Action], Any]

#
# Clock

LOGGER = logging.getLogger('pytils.clock')


class Clock:

    def __init__(
            self,
            max_queue_size: int = _DEFAULT_MAX_TASK_QUEUE_SIZE,
            s_time: TimeSupplier = DEFAULT_TIME_SUPPLIER):
        self._scheduling_queue = SchedulingQueue(max_queue_size, s_time)

    @property
    def schedule(self):
        return self._scheduling_queue.schedule

    def run_scheduler(self):
        self.schedule.run()

    def start_scheduler(self):
        self.schedule.start()

    def run_handler(self):
        self._scheduling_queue.run()

    def start_handler(self):
        self._scheduling_queue.start()


class SchedulingQueue(DaemonHandler):

    def __init__(
            self,
            max_queue_size: int = _DEFAULT_MAX_TASK_QUEUE_SIZE,
            s_time: TimeSupplier = DEFAULT_TIME_SUPPLIER):
        self._cv = Condition()
        self._task_queue = deque(maxlen=max_queue_size)

        self._schedule = Schedule(self._enqueue, s_time)

    @property
    def schedule(self):
        return self._schedule

    def handle_one(self):
        with self._cv:
            self._cv.wait_for(self._task_queue.__len__)
            action = self._task_queue.popleft()
            self._cv.notify()

            action()

    def _enqueue(self, action: Action):
        with self._cv:
            self._task_queue.append(action)
            self._cv.notify()


class Schedule(DaemonHandler):

    def __init__(self, handler: Handler, s_time: TimeSupplier = DEFAULT_TIME_SUPPLIER):
        self.s_time = s_time

        self._lock = RLock()
        self._cv = Condition(self._lock)
        self._schedule = []  # type: List[ScheduleEntry]

        self._handler = handler

    def register(
            self,
            action: Action,
            period: Optional[TimeType],
            delay: Optional[TimeType] = None) -> ScheduleKey:
        if period <= ZERO_DURATION:
            raise ValueError('period must be positive or None')
        if delay < ZERO_DURATION:
            raise ValueError('delay must be non-negative or None')
        if not delay:
            delay = ZERO_DURATION

        key = ScheduleKey(period, action)
        entry = ScheduleEntry(self.s_time() + delay, key)

        with self._cv:
            self._enqueue(entry)

        return key

    def handle_one(self):
        with self._cv:
            while not self._cv.wait_for(self.has_expired, self._get_next_sleep_duration()):
                pass

            self._handle_entry(self._dequeue())

    def _handle_entry(self, entry: ScheduleEntry):
        self._handler(self._create_readmittence_action_from_key(entry.key))

    def _create_readmittence_action_from_key(self, key: ScheduleKey) -> Action:
        if key.period is None:
            return key.action

        def perform_action_and_readmit():
            next_run = self.s_time() + key.period

            key.action()

            current_time = self.s_time()
            if next_run < current_time:
                LOGGER.warning('Scheduled task took longer than its period length to complete')

            self._enqueue(ScheduleEntry(max(current_time, next_run), key))

        return perform_action_and_readmit

    def has_expired(self) -> bool:
        with self._lock:
            return bool(self._schedule) and self._schedule[0].next_run - self.s_time() <= 0

    def _get_next_sleep_duration(self) -> TimeType:
        if self._schedule:
            return min(_MAX_SLEEP_DURATION, max(ZERO_DURATION, self._schedule[0].next_run - self.s_time()))
        else:
            return _MAX_SLEEP_DURATION

    def _enqueue(self, entry: ScheduleEntry):
        self._cv.notify()
        heapq.heappush(self._schedule, entry)

    def _dequeue(self) -> Optional[ScheduleEntry]:
        self._cv.notify()
        return heapq.heappop(self._schedule) if self._schedule else None
