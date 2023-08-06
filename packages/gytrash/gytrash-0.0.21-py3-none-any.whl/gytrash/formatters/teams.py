import json
from collections import defaultdict
from logging import Formatter, LogRecord
from traceback import format_exception
from typing import Iterable

__all__ = ["Office365CardFormatter", "TeamsCardsFormatter"]


class TeamsCardsFormatter(Formatter):
    """
    This class is the base class for cards formatters.
    https://docs.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/what-are-cards
    """

    def format(self, record: LogRecord) -> str:
        raise NotImplementedError()


class Office365CardFormatter(TeamsCardsFormatter):
    """
    This formatter formats logs records as a simple office 365 connector card.
    The connector card documentation is displayed in the link below:
    https://docs.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-reference#office-365-connector-card
    In addition to the message, each log record attribute (levelname, lineno...etc)
    can be displayed as facts.
    """

    _facts = {"name", "levelname", "levelno", "lineno"}
    _color_map = defaultdict(
        lambda: "#008000",
        {
            "DEBUG": "#0000FF",  # blue
            "INFO": "#008000",  # green
            "WARNING": "#FFA500",  # orange
            "ERROR": "#FF0000",  # red
            "CRITICAL": "#8B0000",  # darkred
        },
    )

    def __init__(self, facts: Iterable[str]):
        """
        :param facts:  LogRecord attributes to be displayed as facts in
                       the message's card.
        """
        self.facts = self._facts.intersection(set(facts))
        super().__init__()

    def format(self, record: LogRecord) -> str:
        message = record.getMessage()
        if record.exc_info:
            etype, value, tb = record.exc_info
            message += "\n" * 2
            message += "<code>"
            message += "".join(format_exception(etype, value, tb))
            message += "</code>"
        return json.dumps(
            {
                "@context": "https://schema.org/extensions",
                "@type": "MessageCard",
                "title": f"{record.levelname.title()} in {record.module}",
                "summary": f"{record.getMessage()}",
                "sections": [{"facts": self._build_facts_list(record)}],
                # Fallback to INFO color if needed
                "themeColor": self._color_map[record.levelname],
                "text": message,
            }
        )

    def _build_facts_list(self, record: LogRecord):
        return [{"name": fact, "value": getattr(record, fact)} for fact in self.facts]
