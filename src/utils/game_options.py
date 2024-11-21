from dataclasses import asdict, dataclass
from typing import Self


__all__ = ["GameOptions"]


@dataclass(frozen=True, kw_only=True)
class GameOptions:
    integer_only: bool = True
    must_use_all: bool = True

    def to_dict(self) -> dict[str, bool]:
        return asdict(self)

    @classmethod
    def parse_from_dict(cls, data: dict[str, bool]) -> Self:
        return cls(
            integer_only=data.get("integer_only", True),
            must_use_all=data.get("must_use_all", True),
        )
