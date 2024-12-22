from dataclasses import dataclass

from .utils.expression import Expression
from .utils.game_options import GameOptions


__all__ = ["GameModel"]


@dataclass(frozen=True, kw_only=True)
class GameModel:
    game_options: GameOptions
    numbers: list[int]
    solution: Expression | None
    target: int
