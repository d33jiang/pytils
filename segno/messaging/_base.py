from typing import BinaryIO, Callable, Optional

from .functional import receive, send

__all__ = [
    'IOReceiver',
    'IOSender',
    'Receiver',
    'Sender',
    'Transformation',
]

Transformation = Callable[[bytes], bytes]


class Sender:

    def send(self, msg: bytes):
        raise NotImplementedError

    def layer(self, pre: Transformation) -> 'Sender':
        return _CompositionSender(self, pre)


class Receiver:

    def receive(self) -> Optional[bytes]:
        raise NotImplementedError

    def layer(self, post: Transformation) -> 'Receiver':
        return _CompositionReceiver(self, post)


class IOSender(Sender):

    def __init__(self, dst: BinaryIO):
        self._dst = dst

    def send(self, msg: bytes):
        send(self._dst, msg)


class IOReceiver(Receiver):

    def __init__(self, src: BinaryIO):
        self._src = src

    def receive(self) -> Optional[bytes]:
        return receive(self._src)


class _CompositionSender(Sender):

    def __init__(self, inner: Sender, pre: Transformation):
        self._inner = inner
        self._pre = pre

    def send(self, msg: bytes):
        self._inner.send(self._pre(msg))


class _CompositionReceiver(Receiver):

    def __init__(self, inner: Receiver, post: Transformation):
        self._inner = inner
        self._post = post

    def receive(self) -> Optional[bytes]:
        msg = self._inner.receive()
        return None if msg is None else self._post(msg)
