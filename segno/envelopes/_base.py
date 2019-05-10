import abc

__all__ = [
    'MessageEnvelope',
]


class MessageEnvelope(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def wrap(self, msg: bytes) -> bytes:
        raise NotImplementedError

    @abc.abstractmethod
    def unwrap(self, msg: bytes) -> bytes:
        raise NotImplementedError
