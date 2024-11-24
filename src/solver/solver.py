from ..utils.expression import Expression
from ..utils.game_options import GameOptions
from .algorithm import find_solution_for_target


__all__ = ["find_one_solution"]


def find_one_solution(
    numbers: list[int],
    target: int,
    options: GameOptions,
) -> Expression | None:
    return find_solution_for_target(numbers, target, options)
