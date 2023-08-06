import logging

import coloredlogs

from gytrash.__about__ import *  # noqa: F403,F401
from gytrash.filters import MessengerLogFilter
from gytrash.formatters import Office365CardFormatter, SlackFormatter
from gytrash.handlers import SlackHandler, TeamsHandler, TeamsQueueHandler

log = logging.getLogger("gytrash")


def setup_logging(
    log,
    *,
    log_level: int = 10,
    log_from_botocore: bool = False,
    log_to_slack: bool = False,
    log_to_teams: bool = False,
    slack_log_channel: str = None,
    slack_log_level: int = 20,
    slack_bot_token: str = None,
    teams_url: str = None,
    teams_log_level: int = 20,
    teams_nonblocking: bool = True,
    teams_card_formatter: bool = True,
) -> None:
    """Create the Logging handler for the CLI.
        This setups a log handler that support logging in color.

    Args:
        log: Root logging object.
        log_level: int - (keyword) console streamhandler log level
        log_from_botocore: bool - (keyword) Add botocore Logger if using boto
        log_to_slack: bool - (keyword) Add custom streamhandler to log to slack channel
        slack_log_channel: str - (keyword) Name of the slack channel to send logs
        slack_log_level: int - (keyword) slack streamhandler log level
        slack_bot_token: str - (keyword) Bot token to connect to a slack app.
        teams_url: str - (keyword) URL to the Teams incoming webhook for a
                         channel.
        teams_log_level: int - (keyword) Logging level for the teams logger.
        teams_nonblocking: bool - (keyword) Boolean to turn on non-blocking
                                  queue for log delivery.
        teams_card_formatter: bool - (keyword) Boolean for using the Office 365
                                     card format when delivering logs
    Returns:
        None
    """

    log_format = "%(asctime)s %(name)s:%(module)s:%(lineno)d[%(process)d]:: %(levelname)s %(message)s"  # noqa: E501

    log.setLevel(log_level)

    # generic_formatter = logging.Formatter(log_format)

    coloredlogs.install(level=log_level, logger=log, fmt=log_format)
    log.debug(f"Gytrash log level: {log.getEffectiveLevel()}")

    if log_from_botocore:
        log.debug("Tapping Botocore logger.")
        coloredlogs.install(
            level=log_level, logger=logging.getLogger("botocore"), fmt=log_format
        )

    if log_to_slack is True:
        sh = SlackHandler(slack_log_channel, slack_bot_token)
        log.addHandler(sh)
        sf = SlackFormatter(log_format)
        sh.setFormatter(sf)
        sfilt = MessengerLogFilter()
        sh.addFilter(sfilt)
        sh.setLevel(slack_log_level)

    if log_to_teams is True:
        if teams_nonblocking is True:
            th = TeamsQueueHandler(url=teams_url, level=teams_log_level)
        else:
            th = TeamsHandler(url=teams_url, level=teams_log_level)

        if teams_card_formatter is True:
            cf = Office365CardFormatter(facts=["name", "levelname", "lineno"])
            th.setFormatter(cf)

        log.addHandler(th)
        tfilt = MessengerLogFilter()
        th.addFilter(tfilt)
