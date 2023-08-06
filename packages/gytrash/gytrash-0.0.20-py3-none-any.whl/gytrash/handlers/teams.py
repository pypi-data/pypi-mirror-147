import json
import os
import queue
from logging import NOTSET, Handler, LogRecord
from logging.handlers import QueueHandler, QueueListener

import requests

from gytrash.formatters import TeamsCardsFormatter

__all__ = [
    "TeamsHandler",
    "TeamsQueueHandler",
]


class TeamsHandler(Handler):
    """
    Logging handler for Microsoft Teams webhook integration.

    This handler blocks operation. Use non-blocking NBTeamsHandler for less
    impact on your application performance.
    """

    def __init__(self, url, level=NOTSET):
        """
        :param url: Microsoft Teams incoming webhook url.
        :param level: Logging level (INFO, DEBUG, ERROR...etc)
        """
        super().__init__(level=level)
        if url:
            self.url = url
        else:
            self.url = os.environ["TEAMS_CHANNEL_URL"]

    def format(self, record: LogRecord) -> str:
        if not isinstance(self.formatter, TeamsCardsFormatter):
            return json.dumps({"text": super().format(record)})
        else:
            return self.formatter.format(record)

    def emit(self, record: LogRecord):
        try:
            data = self.format(record)
            requests.post(
                url=self.url, headers={"Content-Type": "application/json"}, data=data
            )
        except Exception:
            self.handleError(record)


class TeamsQueueHandler(QueueHandler):
    """
    Non-blocking logging handler for Microsoft Teams webhook integration.

    This handler reduces impact on your application compared to the (blocking)
    TeamsHandler.

    Queue-based implementation from
    https://docs.python.org/3/howto/logging-cookbook.html#dealing-with-handlers-that-block
    """

    def __init__(self, url, level=NOTSET):
        self._log_queue = queue.Queue(-1)
        super().__init__(self._log_queue)

        self._teams_handler = TeamsHandler(url, level)
        teams_log_listener = QueueListener(self._log_queue, self._teams_handler)
        teams_log_listener.start()

    def setFormatter(self, fmt):
        self._teams_handler.setFormatter(fmt)
        super().setFormatter(fmt)
