#!/usr/bin/env python3

from pync import notify  # type: ignore
import time


def simple_countdown_notify(length: int, interval: int):
    """notify user with notify every interval seconds"""
    for i in range(length, 0, -interval):
        # notify(f"{i} seconds left")

        # notify user the remaining minutes

        notify(f'{i // 60} minutes left')
        time.sleep(interval)
    notify("Time's up!")
