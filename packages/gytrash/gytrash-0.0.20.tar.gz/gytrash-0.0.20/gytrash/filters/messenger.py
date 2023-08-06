import logging


class MessengerLogFilter(logging.Filter):
    """
    Logging filter to decide when logging to a Messenger is requested, using
    the `extra` kwargs:
        `logger.info("...", extra={'notify_messenger': True})`

    Inherits:
        logging.Filter: Base log filtering class
    """

    def filter(self, record):
        return getattr(record, "notify_messenger", False)
