from dataclasses import asdict, dataclass, replace
from typing import Self


__all__ = ["GameOptions"]


@dataclass(frozen=True, kw_only=True)
class GameOptions:
    allow_integer: bool = True
    allow_float_only: bool = False
    must_use_all: bool = True

    def integer_solvable(self) -> bool:
        return self.allow_integer and not self.allow_float_only

    def float_only(self) -> bool:
        return not self.allow_integer and self.allow_float_only

    def any_solvable(self) -> bool:
        return self.allow_integer and self.allow_float_only

    def solvable(self) -> bool:
        return self.allow_integer or self.allow_float_only

    def to_dict(self) -> dict[str, bool]:
        return asdict(self)

    def is_valid(self) -> tuple[bool, str]:
        if not (self.allow_integer or self.allow_float_only):
            return False, "At least one of allow_integer or allow_float_only must be True"
        return True, ""

    def as_integer_solvable(self) -> Self:
        return replace(self, allow_integer=True, allow_float_only=False)

    @classmethod
    def from_integer_solvable(cls) -> Self:
        return cls(allow_integer=True, allow_float_only=False)

    @classmethod
    def from_float_only(cls) -> Self:
        return cls(allow_integer=False, allow_float_only=True)

    @classmethod
    def from_solvable(cls) -> Self:
        return cls(allow_integer=True, allow_float_only=True)

    @classmethod
    def parse_from_dict(cls, data: dict[str, bool]) -> Self:
        return GameOptions(
            allow_integer=data.get("allow_integer", True),
            allow_float_only=data.get("allow_float_only", True),
            must_use_all=data.get("must_use_all", True),
        )
