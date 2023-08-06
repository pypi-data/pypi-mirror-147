# Gytrash

A logging setup module for Python. When setting up logging functionality for new projects I noticed I was always following the same pattern.

Decided to put these practices into a module. The module sets up a logger using `coloredlogs`. You can attach the botocore logs, if you are a regular user of boto3. And the logger can easily ship logging messages to slack.

## Installation

`pip install gytrash`

## Examples

### Simple logging setup

```
import gytrash
import logging
log = logging.getLogger("slack_example")

gytrash.setup_logging(log, log_level=10)

log.info("Test info message")
log.debug("Test debug message")
```

### Setup logger for use with Slack

To use gytrash to ship logging messages to slack, first setup a slack app using this [walkthrough](https://github.com/slackapi/python-slack-sdk/blob/main/tutorial/01-creating-the-slack-app.md)

Once you have generated the bot token, save it as an environment variable.

### Set Slack Environment Variables

`export SLACK_BOT_TOKEN="<BOT TOKEN>"`

Finally setup gytrash using the extended parameters.

### Import Gytrash and setup logger to use Slack

```
import gytrash
import logging
log = logging.getLogger("slack_example")

gytrash.setup_logging(log, log_level=10, log_from_botocore=False, log_to_slack=True, slack_log_channel="<LOG NAME>", slack_log_level=20)

log.info("Test info message")
log.debug("Test debug message")

log.info("Test info message", extra={"notify_slack": True})  # send this log message to slack
```

## Release Process

Create a release branch from main:

`main >> release/v0.0.11` (No change in version number)

Create a feature branch from main:

`main >> feature/new_feature_to_add` (No change in version number)

Work on feature and then PR feature to release branch:

`release/v0.0.11 << feature/new_feature_to_add` (Version bumped to next patch
0.0.12a{PR_NUMBER}.post0 on PR open.)

When release is ready, PR back to main:
`main << release/v0.0.11` (Version is bumped to next version number v0.0.12)

If you have more than one feature PR going into a release, then the feature PR version
must be managed semi-manually. Before the PR is opened, you must pull the commit
that was automatically created during the release test and pypi package upload from the
destination release branch.

After pulling the commit, update these two files back to the version number from main
when you created this feature branch:

```
.bumpversion.cfg
gytrash/__about__.py
```
