#!/usr/bin/env python3

from email import message
from typing import Any, Callable
from pync import notify  # type: ignore
import time
from .classes import NotifyOptions


def call_args_in_subprocess(args: list[str]):
    """call args in subprocess"""
    import subprocess
    subprocess.run(args)


def macos_say(text: str):
    """speak text with macos say"""
    import subprocess
    subprocess.run(['say', text])


def pync_notify(message: str, title: str = 'Countdown'):
    """notify with pync"""
    notify(message, title=title)


def no_notify():
    """no notify"""
    pass


notify_options_dict = {
    NotifyOptions.say: macos_say,
    NotifyOptions.pync: pync_notify,
    NotifyOptions.none: no_notify
}


def simple_countdown_notify(length: int,
                            interval: int,
                            notify: Callable[[str], Any] = macos_say):
    """notify user with notify every interval seconds"""
    for i in range(length, 0, -interval):
        # notify(f"{i} seconds left")

        # notify user the remaining minutes

        notify(f'{i // 60} minutes left')
        time.sleep(interval)
    notify("Time's up!")
