import struct
from typing import BinaryIO, Optional

__all__ = [
    'OVERHEAD_SIZE',
    'receive',
    'send',
]

_SIZE_FORMAT = struct.Struct('>I')
OVERHEAD_SIZE = _SIZE_FORMAT.size


def send(dst: BinaryIO, msg: bytes):
    size_bytes = _SIZE_FORMAT.pack(len(msg))
    dst.write(size_bytes)

    dst.write(msg)

    dst.flush()


def receive(src: BinaryIO) -> Optional[bytes]:
    try:
        size_bytes = read_bytes(src, _SIZE_FORMAT.size)
        size = _SIZE_FORMAT.unpack(size_bytes)[0]

        return read_bytes(src, size)
    except EOFError:
        return None


def read_bytes(src: BinaryIO, size: int) -> bytes:
    data = b''
    while size > 0:
        read = src.read(size)
        if not read:
            raise EOFError('End of stream reached')

        data += read
        size -= len(read)

    return data
