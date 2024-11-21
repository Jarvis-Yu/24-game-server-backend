import datetime

import flask as flk

from .utils.game_options import GameOptions
from .game import create_game


__all__ = ["create_app"]


def create_app() -> flk.Flask:
    app = flk.Flask(__name__)

    @app.route("/favicon.ico", methods=["GET"])
    def favicon():
        return flk.send_from_directory("assets", "favicon.ico")

    @app.route("/api/classic/24", methods=["GET", "POST"])
    def quick_classic_24_game():
        options = GameOptions.parse_from_dict(flk.request.values)
        numbers, time_taken = create_game(4, 24, options)
        return {
            "numbers": numbers,
            "time_taken": time_taken,
            "options": options.to_dict(),
        }

    @app.route("/api/classic/48", methods=["GET", "POST"])
    def quick_classic_48_game():
        options = GameOptions.parse_from_dict(flk.request.values)
        numbers, time_taken = create_game(5, 48, options)
        return {
            "numbers": numbers,
            "time_taken": time_taken,
            "options": options.to_dict(),
        }

    @app.route("/api/today", methods=["GET", "POST"])
    def game_of_the_day():
        seed = datetime.date.today().isoformat()
        options = GameOptions(integer_only=False)
        numbers, time_taken = create_game(4, 24, options, seed)
        return {
            "numbers": numbers,
            "time_taken": time_taken,
        }

    @app.errorhandler(404)
    def page_not_found(error):
        return {
            "error": "Page not found",
            "help": {
                "/api/classic/24": "Get a classic 24 game",
                "/api/classic/48": "Get a classic 48 game",
                "/api/today": "Get a game of the day",
            },
        }, 404

    return app