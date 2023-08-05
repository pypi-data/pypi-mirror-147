#!/usr/bin/env python3

from countdown_tddschn.utils import simple_countdown_notify
import typer # type: ignore

app = typer.Typer()

@app.command()
def countdown(length: int = 60 * 25, interval: int = 60):
	"""Countdown with notify"""
	import daemon # type: ignore
	with daemon.DaemonContext():
		simple_countdown_notify(length, interval)


if __name__ == "__main__":
	app()


