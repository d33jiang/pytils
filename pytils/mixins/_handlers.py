from threading import Thread
from typing import Any

__all__ = [
    'DaemonHandler'
]


class DaemonHandler:
    """
    Boilerplate class for handler functionality that is intended to be run in a number of daemon threads.

    One daemon thread is spawned for every call to start. Each daemon thread runs a loop in which it checks that the
    handler is active before proceeding to invoke the handle_one implementation. A daemon thread will terminate if the
    the handler is inactive when it performs the check.

    The handle_one method must be overridden to attempt to perform one handling action. It is run in a loop; thus, care
    should be taken so that the daemon threads do not spin as a result of the handle_one implementation.

    The is_active method may be overridden to signal any running daemon threads to gradually terminate while the Python
    interpreter instance continues to run.

    """

    def is_active(self) -> Any:
        """Get whether this handler is active."""
        return True

    def handle_one(self):
        """Perform one handling action."""
        raise NotImplementedError

    def run(self):
        """Run the handler loop."""
        while self.is_active():
            self.handle_one()

    def start(self) -> Thread:
        """Start a daemon thread to run the handler loop."""
        t = Thread(target=self.run, daemon=True)
        t.start()

        return t
