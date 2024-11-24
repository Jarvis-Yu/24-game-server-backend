from __future__ import annotations
import datetime
import os
from dataclasses import dataclass

import flask as flk

from .utils.cipher import get_encryptor_decryptor
from .utils.game_options import GameOptions
from .game import create_game


__all__ = ["create_app"]


@dataclass(frozen=True)
class _Route:
    classic_24 = "/api/classic/24"
    classic_48 = "/api/classic/48"
    game_of_the_day = "/api/today"
    solution = "/api/solution/<encoded_solution>"


class _App:
    ROUTES = _Route()

    def __init__(self, app: flk.Flask):
        self.app = app

        self.SALT_TODAY = os.environ.get("SALT_TODAY", "09sdfjgn1o3iua0s9dfij12k34j")

        self.encrypt, self.decrypt = get_encryptor_decryptor()

        @app.route("/favicon.ico", methods=["GET"])
        def favicon():
            assets_path = os.path.join(app.root_path, "assets")
            print(assets_path)
            return flk.send_from_directory(assets_path, "favicon.ico")

        @app.route(self.ROUTES.classic_24, methods=["GET", "POST"])
        def quick_classic_24_game():
            return self.create_game(flk.request, 4, 24)

        @app.route(self.ROUTES.classic_48, methods=["GET", "POST"])
        def quick_classic_48_game():
            return self.create_game(flk.request, 5, 48)

        @app.route(self.ROUTES.solution, methods=["GET", "POST"])
        def decode(encoded_solution: str):
            return {
                "solution": self.decrypt(encoded_solution),
            }

        @app.route(self.ROUTES.game_of_the_day, methods=["GET", "POST"])
        def game_of_the_day():
            seed = datetime.date.today().isoformat() + self.SALT_TODAY
            options = GameOptions(integer_only=False)
            numbers, solution, time_taken = create_game(4, 24, options, seed)
            return {
                "numbers": numbers,
                "time_taken": time_taken,
            }

        @app.errorhandler(404)
        def page_not_found(error):
            return {
                "error": "Page not found",
                "help": {
                    self.ROUTES.classic_24: "Get a classic 24 game",
                    self.ROUTES.classic_48: "Get a classic 48 game",
                    self.ROUTES.game_of_the_day: "Get a game of the day",
                },
            }, 404

    def create_game(self, request: flk.Request, numbers: int, target: int) -> dict:
        options = GameOptions.parse_from_dict(request.values)
        numbers, solution, time_taken = create_game(numbers, target, options)
        return {
            "numbers": numbers,
            "target": target,
            "solution": request.url_root + "api/solution/" + self.encrypt(solution.to_string()),
            "time_taken": time_taken,
            "options": options.to_dict(),
        }

    @classmethod
    def init_app(cls, app: flk.Flask) -> None:
        cls(app)


def create_app() -> flk.Flask:
    app = flk.Flask(__name__, root_path=os.path.dirname(os.path.dirname(__file__)))
    _App.init_app(app)
    return app
