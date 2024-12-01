import random
import time

from .solver.solver import find_one_solution
from .utils.expression import Expression
from .utils.game_options import GameOptions
from .utils.types import number


__all__ = ["check_game", "create_game"]


def _get_random(seed: int | float | str | None) -> random.Random:
    if seed is None:
        return random
    return random.Random(seed)


def create_game(
        quantity: int,
        target: int,
        options: GameOptions,
        seed: number | str | None = None,
        timeout: number | None = None,
) -> tuple[list[int], Expression, number]:
    assert options.is_valid()[0]
    randomizer = _get_random(seed)
    start_time = time.time()
    while True:
        numbers = [randomizer.randint(1, 10) for _ in range(quantity)]
        if options.float_only():
            int_solution = find_one_solution(numbers, target, options.as_integer_only())
            float_solution = find_one_solution(numbers, target, options)
            if int_solution is None and float_solution is not None:
                return numbers, float_solution, time.time() - start_time
        else:
            if (solution := find_one_solution(numbers, target, options)) is not None:
                return numbers, solution, time.time() - start_time
        if timeout is not None and time.time() - start_time > timeout:
            raise TimeoutError("Timeout reached")

def check_game(
        numbers: list[int],
        target: int,
        options: GameOptions,
) -> tuple[Expression | None, number]:
    start_time = time.time()
    return find_one_solution(numbers, target, options), time.time() - start_time
