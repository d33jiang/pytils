import io
import sys
from threading import RLock

from segno.envelopes import ChecksumEnvelope
from segno.messaging import send, receive

#
# DEBUG: Test Functionality

_lock = RLock()


def dump(obj):
    import time
    import random
    time.sleep(random.gauss(0, 0.2) ** 2)

    with _lock:
        print(obj, file=sys.stderr)


in_stream = sys.stdin.buffer  # type: io.FileIO
out_stream = sys.stdout.buffer  # type: io.FileIO

buffer = io.BytesIO()

send(buffer, b'Lorem ipsum.')
print(buffer.getvalue())

send(buffer, ChecksumEnvelope().wrap(b'Lorem ipsum.'))
print(buffer.getvalue())

print(receive(buffer))

buffer.seek(0)

print(receive(buffer))
print(ChecksumEnvelope().unwrap(receive(buffer)))
