import time
from typing import Callable

__all__ = [
    'TimeType', 'ZERO_DURATION',
    'TimeSupplier', 'DEFAULT_TIME_SUPPLIER'
]

TimeType = float
ZERO_DURATION = 0.

TimeSupplier = Callable[[], TimeType]
DEFAULT_TIME_SUPPLIER = time.time
