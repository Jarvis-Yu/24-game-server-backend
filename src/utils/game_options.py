from dataclasses import asdict, dataclass, replace
from typing import Self


__all__ = ["GameOptions"]


@dataclass(frozen=True, kw_only=True)
class GameOptions:
    integer_solvable: bool = True
    float_solvable: bool = True
    must_use_all: bool = True

    def integer_only(self) -> bool:
        return self.integer_solvable

    def float_only(self) -> bool:
        return not self.integer_solvable and self.float_solvable

    def to_dict(self) -> dict[str, bool]:
        return asdict(self)

    def is_valid(self) -> tuple[bool, str]:
        if not (self.integer_solvable or self.float_solvable):
            return False, "At least one of integer_solvable or float_solvable must be True"
        return True, ""

    def as_integer_only(self) -> Self:
        return replace(self, integer_solvable=True, float_solvable=True)

    @classmethod
    def parse_from_dict(cls, data: dict[str, bool]) -> Self:
        return GameOptions(
            integer_solvable=data.get("integer_solvable", True),
            float_solvable=data.get("float_solvable", True),
            must_use_all=data.get("must_use_all", True),
        )
