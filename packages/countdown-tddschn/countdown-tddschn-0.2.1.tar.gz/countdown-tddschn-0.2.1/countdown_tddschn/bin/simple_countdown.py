#!/usr/bin/env python3

from countdown_tddschn.utils import simple_countdown_notify
import typer
from typer import Argument, Option
import daemon

app = typer.Typer()

DEFAULT_COUNTDOWN_LENGTH = 60 * 25
DEFAULT_COUNTDOWN_NOTIFY_INTERVAL = 60 * 5
DEFAULT_POMODORO_LENGTH = 60 * 25
DEFAULT_POMODORO_NOTIFY_INTERVAL = 60 * 5
DEFAULT_POMODORO_BREAK_LENGTH = 60 * 5


@app.command('c')
@app.command()
def countdown(length: int = Option(DEFAULT_COUNTDOWN_LENGTH,
                                   '--length',
                                   '-l',
                                   help='Time to countdown in seconds'),
              interval: int = Option(
                  DEFAULT_COUNTDOWN_NOTIFY_INTERVAL,
                  '--interval',
                  '-i',
                  help='Time between notifications in seconds')):
    """Countdown with notify"""
    with daemon.DaemonContext():
        simple_countdown_notify(length, interval)


@app.command('p')
@app.command('pomodoro')
def pomodoro_countdown(
        length: int = Option(DEFAULT_POMODORO_LENGTH,
                             '--length',
                             '-l',
                             help='Time to countdown in seconds'),
        interval: int = Option(DEFAULT_POMODORO_NOTIFY_INTERVAL,
                               '--interval',
                               '-i',
                               help='Time between notifications in seconds'),
        break_length: int = Option(DEFAULT_POMODORO_BREAK_LENGTH,
                                   '--break-length',
                                   '-bl',
                                   help='Break length in seconds'),
        is_break: bool = Option(False,
                                '--is-break',
                                '-b',
                                help='Is this a break?')):
    """Countdown with notify"""
    with daemon.DaemonContext():
        if is_break:
            simple_countdown_notify(break_length, interval)
        else:
            simple_countdown_notify(length, interval)


if __name__ == "__main__":
    app()
