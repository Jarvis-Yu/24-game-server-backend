from __future__ import annotations

import datetime
import os
from dataclasses import dataclass

import flask as flk

from .models import GameModel

from .game import check_game, create_game
from .tracker.options import TrackerOptions
from .tracker.tracker import Tracker
from .utils.cipher import get_encryptor_decryptor
from .utils.expression import Expression
from .utils.game_options import GameOptions
from .utils.parse import parse_int, parse_to_bool_dict


__all__ = ["create_app"]


@dataclass(frozen=True)
class _Route:
    classic_24 = "/api/classic/24"
    classic_48 = "/api/classic/48"
    query_classic = "/api/query/classic/<int:target>/<path:numbers_in_path>"
    game_of_the_day = "/api/today"
    solution = "/api/solution/<encoded_solution>"


class _App:
    ROUTES = _Route()

    def __init__(self, app: flk.Flask):
        self.app = app
        self.tracker = Tracker(TrackerOptions())

        self.SALT_TODAY = os.environ.get("SALT_TODAY", "09sdfjgn1o3iua0s9dfij12k34j")

        self.encrypt, self.decrypt = get_encryptor_decryptor()

        @app.route("/favicon.ico", methods=["GET"])
        def favicon():
            assets_path = os.path.join(app.root_path, "assets")
            return flk.send_from_directory(assets_path, "favicon.ico")

        @app.route(self.ROUTES.classic_24, methods=["GET", "POST"])
        def quick_classic_24_game():
            return self.create_game(flk.request, 4, 24)

        @app.route(self.ROUTES.classic_48, methods=["GET", "POST"])
        def quick_classic_48_game():
            return self.create_game(flk.request, 5, 48)

        @app.route(self.ROUTES.game_of_the_day, methods=["GET", "POST"])
        def game_of_the_day():
            seed = datetime.date.today().isoformat() + self.SALT_TODAY
            options = GameOptions.from_solvable()
            numbers, solution, time_taken = create_game(4, 24, options, seed)
            return {
                "numbers": numbers,
                "time_taken": time_taken,
            }

        @app.route(self.ROUTES.query_classic, methods=["GET", "POST"])
        def query_classic_game(target: int, numbers_in_path: str):
            numbers = [
                number
                for number_str in numbers_in_path.split("/")
                if (number := parse_int(number_str)) is not None
            ]
            int_solution, int_time_taken = check_game(numbers, target, GameOptions.from_integer_solvable())
            float_solution, float_time_taken = check_game(numbers, target, GameOptions.from_float_only())
            integer_feasible = int_solution is not None
            return {
                "numbers": numbers,
                "target": target,
                "integer_feasible": integer_feasible,
                "solution": self.get_solution_link(flk.request, int_solution if integer_feasible else float_solution),
                "time_taken": int_time_taken + float_time_taken,
            }

        @app.route(self.ROUTES.solution, methods=["GET", "POST"])
        def decode(encoded_solution: str):
            return {
                "solution": self.decrypt(encoded_solution),
            }

        @app.errorhandler(404)
        def page_not_found(error):
            url = flk.request.url
            return {
                "error": "Page not found",
                "help": {
                    url + self.ROUTES.classic_24: "Get a classic 24 game",
                    url + self.ROUTES.classic_48: "Get a classic 48 game",
                    url + self.ROUTES.game_of_the_day: "Get a game of the day",
                    url + self.ROUTES.query_classic: "Query a classic game",
                },
            }, 404

    def create_game(self, request: flk.Request, quantity: int, target: int) -> dict | tuple[dict, int]:
        options = GameOptions.parse_from_dict(parse_to_bool_dict(request.values))
        options_valid, error = options.is_valid()
        if not options_valid:
            return {
                "error": error,
            }, 400

        numbers, solution, time_taken = create_game(quantity, target, options)
        game = GameModel(
            game_options=options,
            numbers=numbers,
            solution=solution,
            target=target,
        )
        self.tracker.record(game, time_taken, request)
        return {
            "numbers": numbers,
            "target": target,
            "solution": self.get_solution_link(request, solution),
            "time_taken": time_taken,
            "options": options.to_dict(),
        }

    def get_solution_link(self, request: flk.Request, solution: Expression | None) -> str:
        if solution is None:
            return "None"
        return request.url_root + "api/solution/" + self.encrypt(solution.to_string())

    @classmethod
    def init_app(cls, app: flk.Flask) -> None:
        cls(app)


def create_app() -> flk.Flask:
    app = flk.Flask(__name__, root_path=os.path.dirname(os.path.dirname(__file__)))
    _App.init_app(app)
    return app
