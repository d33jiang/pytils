from collections import deque
from threading import Condition
from typing import BinaryIO, Deque, Optional

from pytils.mixins import DaemonHandler
from ._base import IOReceiver, IOSender

__all__ = [
    'QueuedReceiver',
    'QueuedSender',
]

_DEFAULT_MAX_QUEUE_SIZE = 4096


class QueuedSender(DaemonHandler, IOSender):

    def __init__(self, dst: BinaryIO, max_queue_size: int = _DEFAULT_MAX_QUEUE_SIZE):
        super().__init__(dst)

        self.is_closed = False

        self._cv = Condition()
        self._queue = deque(maxlen=max_queue_size)  # type: Optional[Deque[bytes]]

    def send(self, msg: bytes):
        with self._cv:
            self._queue.append(msg)
            self._cv.notify()

    def is_active(self) -> bool:
        return not self.is_closed

    def handle_one(self):
        with self._cv:
            self._cv.wait_for(lambda: self.is_closed or self._queue)
            self._cv.notify()

            if self._queue:
                super().send(self._queue.popleft())

    def close(self):
        self.is_closed = True
        with self._cv:
            self._cv.notify_all()


class QueuedReceiver(DaemonHandler, IOReceiver):

    def __init__(self, src: BinaryIO, max_queue_size: int = _DEFAULT_MAX_QUEUE_SIZE):
        super().__init__(src)

        self.is_closed = False

        self._cv = Condition()
        self._queue = deque(maxlen=max_queue_size)  # type: Optional[Deque[bytes]]

    def receive(self) -> Optional[bytes]:
        with self._cv:
            self._cv.wait_for(lambda: self.is_closed or self._queue)
            self._cv.notify()
            return self._queue.popleft() if self._queue else None

    def is_active(self) -> bool:
        return not self.is_closed

    def handle_one(self):
        msg = super().receive()
        with self._cv:
            if msg is not None:
                self._queue.append(msg)
            else:
                self.is_closed = True

            self._cv.notify()
