from ..utils.game_options import GameOptions
from .algorithm import verify_feasibility


def is_feasible_game(
    numbers: list[int],
    target: int,
    options: GameOptions,
) -> bool:
    return verify_feasibility(numbers, target, options)