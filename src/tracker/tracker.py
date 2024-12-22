from __future__ import annotations

import _io
import datetime
import os

import flask as flk

from ..models import GameModel
from .options import TrackerOptions

__all__ = ["Tracker"]


class Tracker:
    def __init__(self, options: TrackerOptions) -> None:
        self._options = options

    def record(self, game: GameModel, time_taken: float, request: flk.Request) -> None:
        fd = _today_fd_getter.get_fd()
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        fd.write(f"{client_ip}\t{datetime.datetime.now(datetime.timezone.utc).strftime('%d/%m/%Y %H:%M:%S')}\t"
                 f"{game.target}\t{game.numbers}\t{game.game_options.to_dict()}\n")
        fd.flush()


class _TodayFdGetter:
    def __init__(self) -> None:
        self._last_date = datetime.datetime.now(datetime.timezone.utc).date()
        if not os.path.exists("logs"):
            os.makedirs("logs")
        self._fd = open(f"logs/{self._last_date.isoformat()}.log", "a")

    def get_fd(self) -> _io.TextIOWrapper:
        today = datetime.datetime.now(datetime.timezone.utc).date()
        if today != self._last_date:
            self._fd.close()
            self._fd = open(f"logs/{today.isoformat()}.log", "a")
            self._last_date = today
        return self._fd


_today_fd_getter = _TodayFdGetter()

