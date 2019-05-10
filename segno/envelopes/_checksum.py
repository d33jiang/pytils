import hashlib

from ._base import MessageEnvelope

__all__ = [
    'ChecksumEnvelope',
]


class ChecksumEnvelope(MessageEnvelope):

    def __init__(self, algorithm=hashlib.sha256):
        self._algorithm = algorithm

    def wrap(self, msg: bytes) -> bytes:
        checksum = self._algorithm(msg).digest()
        return checksum + msg

    def unwrap(self, msg: bytes) -> bytes:
        digest = self._algorithm()

        expected = msg[:digest.digest_size]
        data = msg[digest.digest_size:]

        digest.update(data)
        actual = digest.digest()

        if actual != expected:
            raise ChecksumError(expected, actual)

        return data


class ChecksumError(ValueError):

    def __init__(self, expected, actual):
        ValueError(f'Checksum discrepancy: expected {expected!s}; got {actual!s}')
