from typing import Iterable, TypeVar


__all__ = ["flat_chain"]


T = TypeVar("T")


def flat_chain(iterables: Iterable[Iterable[T]]) -> Iterable[T]:
    for iterable in iterables:
        yield from iterable