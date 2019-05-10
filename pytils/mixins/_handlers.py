from threading import Thread
from typing import Any

__all__ = [
    'DaemonHandler'
]


class DaemonHandler:

    def is_active(self) -> Any:
        return self

    def handle_one(self):
        raise NotImplementedError

    def run(self):
        while self.is_active():
            self.handle_one()

    def start(self) -> Thread:
        t = Thread(target=self.run, daemon=True)
        t.start()

        return t
