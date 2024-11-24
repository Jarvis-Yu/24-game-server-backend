from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from .types import number


__all__ = [
    "BinaryOperation",
    "Expression",
    "BiOpExpression",
    "NumberExpression",
]


class BinaryOperation(Enum):
    ADDITION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    DIVISION = "/"

    def precedence(self) -> int:
        return {
            BinaryOperation.ADDITION: 1,
            BinaryOperation.SUBTRACTION: 1,
            BinaryOperation.MULTIPLICATION: 2,
            BinaryOperation.DIVISION: 2,
        }[self]

    def commutative(self) -> bool:
        return {
            BinaryOperation.ADDITION: True,
            BinaryOperation.SUBTRACTION: False,
            BinaryOperation.MULTIPLICATION: True,
            BinaryOperation.DIVISION: False,
        }[self]


class _ElementLocation(Enum):
    BIOP_LEFT = "BIOP_LEFT"
    BIOP_RIGHT = "BIOP_RIGHT"


class Expression(ABC):
    @abstractmethod
    def to_string(
        self,
        parent_expression: Expression | None = None,
        location: _ElementLocation | None = None,
    ) -> str:
        pass

    def __str__(self) -> str:
        return self.to_string()


@dataclass(frozen=True)
class BiOpExpression(Expression):
    binary_operation: BinaryOperation
    left: Expression
    right: Expression

    def to_string(
        self,
        parent_expression: Expression | None = None,
        location: _ElementLocation | None = None,
    ) -> str:
        op = self.binary_operation.value
        left = self.left.to_string(self, _ElementLocation.BIOP_LEFT)
        right = self.right.to_string(self, _ElementLocation.BIOP_RIGHT)
        if parent_expression is None:
            return f"{left} {op} {right}"
        assert isinstance(parent_expression, BiOpExpression)
        this_precedence = self.binary_operation.precedence()
        parent_precedence = parent_expression.binary_operation.precedence()
        should_add_brackets = (
            this_precedence < parent_precedence
            or (
                this_precedence == parent_precedence
                and not parent_expression.binary_operation.commutative()
                and location is _ElementLocation.BIOP_RIGHT
            )
        )
        if should_add_brackets:
            return f"({left} {op} {right})"
        return f"{left} {op} {right}"

    @classmethod
    def add(cls, a: Expression, b: Expression) -> BiOpExpression:
        return cls(BinaryOperation.ADDITION, a, b)

    @classmethod
    def sub(cls, a: Expression, b: Expression) -> BiOpExpression:
        return cls(BinaryOperation.SUBTRACTION, a, b)
    
    @classmethod
    def mul(cls, a: Expression, b: Expression) -> BiOpExpression:
        return cls(BinaryOperation.MULTIPLICATION, a, b)
    
    @classmethod
    def div(cls, a: Expression, b: Expression) -> BiOpExpression:
        return cls(BinaryOperation.DIVISION, a, b)


@dataclass(frozen=True)
class NumberExpression(Expression):
    value: number

    def to_string(
        self,
        parent_expression: Expression | None = None,
        location: _ElementLocation | None = None,
    ) -> str:
        return str(self.value)


if __name__ == "__main__":
    a = NumberExpression(1)
    b = NumberExpression(2)
    c = NumberExpression(3)
    print(BiOpExpression.add(a, b).to_string())
    print(BiOpExpression.add(a, BiOpExpression.add(b, c)).to_string())
    print(BiOpExpression.sub(a, BiOpExpression.add(b, c)).to_string())
    print(BiOpExpression.mul(a, BiOpExpression.add(b, c)).to_string())
    print(BiOpExpression.add(a, BiOpExpression.mul(b, c)).to_string())
    print(BiOpExpression.div(a, BiOpExpression.mul(b, c)).to_string())
    print(BiOpExpression.mul(BiOpExpression.add(a, b), c).to_string())
