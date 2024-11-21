from __future__ import annotations

from dataclasses import dataclass
from typing import Self


__all__ = ["NumberCombinationVector"]


@dataclass(frozen=True)
class NumberCombinationVector:
    _vector: tuple[int]
    _number_to_index: dict[int, int]

    def total_count(self) -> int:
        return sum(self._vector)

    def __add__(self, other: Self) -> Self:
        return type(self)(
            tuple(self._vector[i] + other._vector[i] for i in range(len(self._vector))),
            self._number_to_index
        )

    def add_number(self, number: int) -> Self:
        new_vector = list(self._vector)
        new_vector[self._number_to_index[number]] += 1
        return type(self)(tuple(new_vector), self._number_to_index)

    def add_numbers(self, numbers: list[int]) -> Self:
        new_vector = list(self._vector)
        for number in numbers:
            new_vector[self._number_to_index[number]] += 1
        return type(self)(tuple(new_vector), self._number_to_index)

    def __hash__(self) -> int:
        return hash(self._vector)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._vector == other._vector

    def __ge__(self, other: Self) -> bool:
        return all(
            self._vector[i] >= other._vector[i]
            for i in range(len(self._vector))
        )

    def __le__(self, other: Self) -> bool:
        return all(
            self._vector[i] <= other._vector[i]
            for i in range(len(self._vector))
        )

    @classmethod
    def init(cls, numbers: list[int]) -> Self:
        ordered_numbers = set(numbers)
        number_to_index = {number: index for index, number in enumerate(ordered_numbers)}
        vector = tuple([0] * len(ordered_numbers))
        return cls(vector, number_to_index)
