import random
import time

from .verifier.verifier import is_feasible_game

from .utils.game_options import GameOptions
from .utils.types import number


__all__ = ["create_game"]


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
) -> tuple[list[int], number]:
    randomizer = _get_random(seed)
    start_time = time.time()
    while True:
        numbers = [randomizer.randint(1, 10) for _ in range(quantity)]
        if is_feasible_game(numbers, target, options):
            return numbers, time.time() - start_time
        if timeout is not None and time.time() - start_time > timeout:
            raise TimeoutError("Timeout reached")